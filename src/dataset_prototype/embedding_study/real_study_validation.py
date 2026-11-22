"""Pure preconditions on supplied evidence; no source reader or scientific adapter."""
from .real_study_contracts import DOMAINS


def assess_preconditions(packet,review,verifications=()):
    """Technical readiness only; never authenticates a human or authorizes execution."""
    reasons=[]
    if review.packet_digest!=packet.packet_digest:reasons.append('review_digest_mismatch')
    if review.origin!='HUMAN_REVIEW':reasons.append('no_external_human_review')
    if review.decision!='APPROVE_BOUNDED_AUDIT':reasons.append('bounded_audit_not_approved')
    for item in review.findings:
        permitted={'PASS'}
        if item.domain=='availability' and packet.proposed_claim=='retrospective_reconstructed':permitted.add('NOT_APPLICABLE')
        if item.status not in permitted:reasons.append(item.domain+':'+item.status)
    verified={v.source_id:v for v in verifications}
    if len(verified)!=len(verifications):reasons.append('duplicate_verification')
    if set(verified)-{s.source_id for s in packet.sources}:reasons.append('unoffered_verification')
    for source in packet.sources:
        if source.source_id not in verified:reasons.append(source.source_id+':current_container_hash_missing')
        elif verified[source.source_id].checksum_sha256!=source.reported_sha256:reasons.append(source.source_id+':container_hash_mismatch')
    return {'technical_evidence_complete':not reasons,'reasons':reasons,
      'scientific_status':{f.domain:f.status for f in review.findings},
      'human_decision':review.decision,'packet_digest':packet.packet_digest,
      'source_rows_read':0,'models_trained':0,'source_reader_implemented':False,
      'execution_permission_granted':False,
      'meaning':'Evidence precondition check only. External human attribution must be verified; no source IO, runtime HumanDecision or execution authority is produced.'}


def inspect_calendar_support(rows,*,require_origin=False,origin_evidenced=False):
    """Validate generated evidence windows; do not calculate scientific growth or map fields."""
    reasons=[]
    if not rows:return {'eligible_support':False,'reasons':['empty_window']}
    if len({r.event_id for r in rows})!=1:reasons.append('event_boundary_crossed')
    if len({r.source_observation_id for r in rows})!=len(rows):reasons.append('duplicate_source_id')
    dates=[r.native_date for r in rows]
    if len(set(dates))!=len(dates):reasons.append('duplicate_native_date')
    if dates!=sorted(dates):reasons.append('unordered_source_dates')
    if any((b-a).days!=1 for a,b in zip(dates,dates[1:])):reasons.append('calendar_gap_or_non_daily_support')
    if not all(r.available for r in rows):reasons.append('missing_observation')
    if require_origin and not origin_evidenced:reasons.append('event_prefix_origin_not_evidenced')
    return {'eligible_support':not reasons,'reasons':reasons,
      'observed_zero_ids':[r.source_observation_id for r in rows if r.available and r.native_area_km2==0],
      'native_quality_flags':{r.source_observation_id:list(r.quality_flags) for r in rows},
      'scope':'Calendar support of supplied generated rows only; not source semantics, availability, rights or scientific approval'}


def prospective_availability_check(dates,availability,issued_at):
    """Unknown source availability cannot be replaced by synthetic midnight timestamps."""
    if len(dates)!=len(availability):return {'supported':False,'reason':'shape_mismatch'}
    if issued_at is None or issued_at.utcoffset() is None:return {'supported':False,'reason':'unknown_issue_time'}
    if any(t is None for t in availability):return {'supported':False,'reason':'unknown_observation_availability'}
    if any(t.utcoffset() is None for t in availability):return {'supported':False,'reason':'unknown_availability_timezone'}
    if any(t>issued_at for t in availability):return {'supported':False,'reason':'observation_unavailable_at_issue'}
    if any(t.date()<d for d,t in zip(dates,availability)):return {'supported':False,'reason':'availability_predates_observation'}
    return {'supported':True,'reason':None,'scope':'supplied timestamp consistency only; no operational provenance verification'}
