"""Preapproval evidence checks using generated support rows; never reads real rows."""
from datetime import date,datetime,timedelta,timezone
import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from dataset_prototype.embedding_study.real_study_contracts import (
 RealStudyPacket,RealStudyReview,ScientificReviewItem,ContainerVerification,SupportCheckRow,BoundedReadProposal,DOMAINS)
from dataset_prototype.embedding_study.real_study_validation import assess_preconditions,inspect_calendar_support,prospective_availability_check

ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/'reports/embedding_utility/fire_vase/milestone-6/review-v2'

@pytest.fixture
def packet():return RealStudyPacket.model_validate_json((PACKET/'packet.json').read_text())


def human_review(packet,**changes):
    value=dict(packet_digest=packet.packet_digest,origin='HUMAN_REVIEW',reviewer='OFFLINE TEST HUMAN FIXTURE',
      reviewed_at=datetime(2026,11,21,tzinfo=timezone.utc),decision='APPROVE_BOUNDED_AUDIT',
      findings=tuple(ScientificReviewItem(domain=d,status='PASS',evidence_ids=('generated-test-evidence',),rationale='Offline validation fixture, not an actual approval') for d in DOMAINS))
    value.update(changes);return RealStudyReview(**value)


def verification(packet):
    return tuple(ContainerVerification(source_id=s.source_id,checksum_sha256=s.reported_sha256,verified_at=datetime(2026,11,21,tzinfo=timezone.utc)) for s in packet.sources)


def rows():
    return [SupportCheckRow(source_observation_id=f'generated-{i}',event_id='generated-event',native_date=date(2020,1,1)+timedelta(days=i),available=True,native_area_km2=x,quality_flags=('explicit_generated',)) for i,x in enumerate((2.,0.,4.,3.))]


def test_frozen_packet_has_local_lake_and_no_approval(packet):
    review=RealStudyReview.model_validate_json((PACKET/'review-template.json').read_text());result=assess_preconditions(packet,review)
    assert len(packet.sources)==4 and all('fire_vase/data_lake/fire-vase-data-lake-v0.1/files/' in s.local_path for s in packet.sources)
    assert review.packet_digest==packet.packet_digest and not result['technical_evidence_complete']
    assert all(v=='NEEDS_EVIDENCE' for v in result['scientific_status'].values())
    assert result['source_rows_read']==0 and not result['execution_permission_granted'] and not result['source_reader_implemented']
    assert not packet.sample.train_models and not packet.sample.persist_raw_or_harmonized


def test_preconditions_are_not_permissions_and_need_current_identity(packet):
    review=human_review(packet);missing=assess_preconditions(packet,review)
    assert not missing['technical_evidence_complete']
    result=assess_preconditions(packet,review,verification(packet))
    assert result['technical_evidence_complete'] and result['execution_permission_granted'] is False
    assert not result['source_reader_implemented']


def test_agent_cannot_create_an_approval(packet):
    with pytest.raises(ValidationError):RealStudyReview(packet_digest=packet.packet_digest,decision='APPROVE_BOUNDED_AUDIT',findings=human_review(packet).findings)
    with pytest.raises(ValidationError):human_review(packet,reviewer=None)


def test_scientific_edits_invalidate_review(packet):
    reviewed=human_review(packet);changed=packet.model_copy(update={'proposed_claim':'prospective_available_at_issue'})
    assert 'review_digest_mismatch' in assess_preconditions(changed,reviewed,verification(packet))['reasons']

@pytest.mark.parametrize('status',['FAIL','NEEDS_EVIDENCE','NOT_APPLICABLE'])
def test_rights_unknown_or_failure_cannot_be_overridden(packet,status):
    review=human_review(packet);findings=tuple(f.model_copy(update={'status':status}) if f.domain=='rights' else f for f in review.findings)
    result=assess_preconditions(packet,review.model_copy(update={'findings':findings}),verification(packet))
    assert not result['technical_evidence_complete'] and 'rights:'+status in result['reasons']


def test_prospective_availability_cannot_be_waived(packet):
    retrospective=human_review(packet);findings=tuple(f.model_copy(update={'status':'NOT_APPLICABLE'}) if f.domain=='availability' else f for f in retrospective.findings)
    retrospective=retrospective.model_copy(update={'findings':findings})
    assert assess_preconditions(packet,retrospective,verification(packet))['technical_evidence_complete']
    prospective=packet.model_copy(update={'proposed_claim':'prospective_available_at_issue'})
    review=retrospective.model_copy(update={'packet_digest':prospective.packet_digest})
    assert not assess_preconditions(prospective,review,verification(prospective))['technical_evidence_complete']


def test_verification_mismatch_and_duplicate_fail_closed(packet):
    v=list(verification(packet));v[0]=v[0].model_copy(update={'checksum_sha256':'0'*64})
    assert not assess_preconditions(packet,human_review(packet),v)['technical_evidence_complete']
    v=list(verification(packet));v.append(v[0]);assert 'duplicate_verification' in assess_preconditions(packet,human_review(packet),v)['reasons']


def test_sample_bounds_and_no_hidden_execution():
    with pytest.raises(ValidationError):BoundedReadProposal(max_total_decoded_rows=513)
    with pytest.raises(ValidationError):BoundedReadProposal(train_models=True)
    with pytest.raises(ValidationError):BoundedReadProposal(read_geometries=True)
    with pytest.raises(ValidationError):BoundedReadProposal(max_total_decoded_rows=1,batch_rows=128)


def test_observed_zero_and_quality_survive_validation():
    data=rows();result=inspect_calendar_support(data)
    assert result['eligible_support'] and result['observed_zero_ids']==['generated-1']
    assert result['native_quality_flags']['generated-1']==['explicit_generated']
    assert data[1].native_area_km2==0
    with pytest.raises(ValidationError):data[1].model_validate({**data[1].model_dump(),'available':False})

@pytest.mark.parametrize('problem',['gap','missing','duplicate_date','duplicate_id','cross_event','ordering','origin'])
def test_bad_support_is_not_silently_repaired(problem):
    data=rows();before=[r.model_dump(mode='json') for r in data]
    if problem=='gap':data.pop(1)
    elif problem=='missing':data[1]=data[1].model_copy(update={'available':False,'native_area_km2':None})
    elif problem=='duplicate_date':data[1]=data[1].model_copy(update={'native_date':data[0].native_date})
    elif problem=='duplicate_id':data[1]=data[1].model_copy(update={'source_observation_id':data[0].source_observation_id})
    elif problem=='cross_event':data[1]=data[1].model_copy(update={'event_id':'other-event'})
    elif problem=='ordering':data.reverse()
    result=inspect_calendar_support(data,require_origin=problem=='origin')
    assert not result['eligible_support']
    if problem=='origin':assert [r.model_dump(mode='json') for r in data]==before


def test_unknown_availability_is_not_synthetic_midnight():
    days=[date(2020,1,1)];issued=datetime(2020,1,3,tzinfo=timezone.utc)
    assert prospective_availability_check(days,[None],issued)['reason']=='unknown_observation_availability'
    assert not prospective_availability_check(days,[datetime(2020,1,4,tzinfo=timezone.utc)],issued)['supported']
    assert not prospective_availability_check(days,[datetime(2020,1,2)],issued)['supported']
    assert prospective_availability_check(days,[datetime(2020,1,2,tzinfo=timezone.utc)],issued)['supported']


def test_validators_never_open_source_files(monkeypatch,packet):
    review=human_review(packet);v=verification(packet)
    def forbidden(*args,**kwargs):raise AssertionError('precondition checker attempted IO')
    monkeypatch.setattr('builtins.open',forbidden)
    assert assess_preconditions(packet,review,v)['source_rows_read']==0
    assert inspect_calendar_support(rows())['eligible_support']
