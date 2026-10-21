"""Offline jurisdiction and evidence regression tests; no source downloads."""
import pytest
from dataset_prototype.contracts import digest
from dataset_prototype.review import synthesize, validate_qa_references
from dataset_prototype.review_contracts import (Domain, Evidence, EvidenceKind,
    ReviewFinding, SpecialistReview, Status)

HASH = digest({'recipe': 'frozen'})

def case(domain=Domain.UNITS, status=Status.PASS, kind=EvidenceKind.SOURCE_DOCUMENTED):
    evidence = Evidence(evidence_id='coefficients', domain=domain, kind=kind,
        source='native-stac:/assets/nir', statement='scale=0.0001; offset=-0.1; unit=1',
        content_digest=digest({'scale': .0001, 'offset': -.1}))
    finding = ReviewFinding(finding_id=domain.value+'.coefficients', reviewer_domain=domain,
        status=status, claim='Documented coefficients define dimensionless reflectance.',
        evidence=('coefficients',), source=evidence.source, required_action='Retain coefficients.', confidence=1)
    return SpecialistReview(reviewer_domain=domain, recipe_content_digest=HASH, findings=(finding,)), evidence

def report(review, evidence, **kwargs):
    return synthesize((review,), (evidence,), recipe_content_digest=HASH,
        source_digest=HASH, required_domains=(review.reviewer_domain,), **kwargs)

def test_eligibility_never_authorizes_execution():
    result = report(*case())
    assert result.model_consensus == 'eligible_for_approval'
    assert result.human_approval == 'pending' and result.execution_authorized is False

def test_missing_evidence_is_not_failure():
    result = report(*case(status=Status.NEEDS_EVIDENCE, kind=EvidenceKind.MISSING_EVIDENCE))
    assert result.model_consensus == 'needs_review'
    assert result.unresolved_findings == ('units.coefficients',)

def test_documented_failure_vetoes():
    assert report(*case(status=Status.FAIL)).model_consensus == 'needs_revision'
    with pytest.raises(ValueError, match='FAIL requires'):
        report(*case(status=Status.FAIL, kind=EvidenceKind.MODEL_JUDGMENT))

def test_opinion_cannot_be_pass():
    with pytest.raises(ValueError, match='PASS requires'):
        report(*case(kind=EvidenceKind.MODEL_JUDGMENT))

def test_jurisdiction_and_recipe_bindings():
    review, evidence = case()
    with pytest.raises(ValueError, match='cross-jurisdiction'):
        report(review, evidence.model_copy(update={'domain': Domain.RIGHTS}))
    with pytest.raises(ValueError, match='different scientific recipe'):
        report(review.model_copy(update={'recipe_content_digest': digest('changed')}), evidence)
    with pytest.raises(ValueError, match='jurisdiction'):
        report(review.model_copy(update={'findings': (review.findings[0].model_copy(update={'finding_id': 'rights.terms'}),)}), evidence)

def test_duplicates_missing_roles_and_qa_references():
    review, evidence = case()
    with pytest.raises(ValueError, match='one review'):
        synthesize((review, review), (evidence,), recipe_content_digest=HASH, source_digest=HASH)
    result = synthesize((review,), (evidence,), recipe_content_digest=HASH, source_digest=HASH)
    assert result.model_consensus == 'needs_review' and Domain.RIGHTS in result.missing_domains
    assert validate_qa_references(result, ['units.coefficients']*2) == ('units.coefficients',)
    with pytest.raises(ValueError, match='unknown findings'):
        validate_qa_references(result, ['rights.speculation'])

class FakeBackend:
    """Explicit offline transport; never used as a live-service fallback."""
    traces = ()
    def __init__(self, bad_role=None):
        self.calls = []
        self.bad_role = bad_role

    def generate(self, role, instruction, data, schema):
        self.calls.append((role, data))
        if role == 'qa':
            return schema(finding_ids=[f['finding_id'] for f in data['unique_findings']],
                          summary='Existing findings require human review.', decision='accept')
        domain = Domain(role)
        item = data['evidence'][0]
        status = 'NEEDS_EVIDENCE' if item['kind'] == 'MISSING_EVIDENCE' else 'PASS'
        identifier = role+'.evidence'
        if role == self.bad_role:
            identifier = 'rights.outside_scope'
        return schema(reviewer_domain=domain, recipe_content_digest=data['recipe_content_digest'],
            findings=[dict(finding_id=identifier, reviewer_domain=domain, status=status,
                claim='Review supplied evidence within this domain.', evidence=[item['evidence_id']],
                source=item['source'], required_action='Human review.', confidence=.8)])


def review_bundle(bundle):
    from dataset_prototype.review import REQUIRED_DOMAINS
    from dataset_prototype.scoped_review import ReviewBundle
    recipe = bundle[2]
    ledger = tuple(Evidence(evidence_id=domain.value+'.record', domain=domain,
        kind=EvidenceKind.MISSING_EVIDENCE if domain == Domain.RIGHTS else EvidenceKind.SOURCE_DOCUMENTED,
        source='explicit-generated-review-fixture', statement='Generated evidence for contract testing only.',
        content_digest=digest(domain.value)) for domain in REQUIRED_DOMAINS)
    return ReviewBundle(recipe=recipe, sources=(bundle[0],), source_digest=digest([bundle[0].model_dump(mode="json")]),
        intended_operation='Offline generated contract exercise.', evidence=ledger, fixture=True)


def test_scoped_pipeline_same_recipe_domains_and_failure_checkpoint(bundle, tmp_path):
    import json
    from dataset_prototype.scoped_review import review_metadata
    inputs = review_bundle(bundle)
    backend = FakeBackend()
    result = review_metadata(inputs, backend, tmp_path/'good')
    assert result.model_consensus == 'needs_review'
    assert len(backend.calls) == 7
    hashes = {data['recipe_content_digest'] for role, data in backend.calls if role != 'qa'}
    assert len(hashes) == 1
    for role, data in backend.calls[:-1]:
        assert all(e['domain'] == role for e in data['evidence'])
    manifest = json.loads((tmp_path/'good/manifest.json').read_text())
    assert manifest['status'] == 'complete' and not manifest['source_data_read']
    with pytest.raises(ValueError):
        review_metadata(inputs, FakeBackend('support'), tmp_path/'bad')
    failure = json.loads((tmp_path/'bad/failure.json').read_text())
    assert failure['accepted_reviews'] == 2 and failure['execution_authorized'] is False
    assert (tmp_path/'bad/traces.json').exists()
    assert json.loads((tmp_path/'bad/manifest.json').read_text())['status'] == 'failed'


def test_negative_calibrated_reflectance_is_retained(bundle):
    from dataset_prototype.contracts import Operation
    from dataset_prototype.harmonization import run
    r, mapping, recipe, rows = bundle
    source = r.model_copy(update={'variables': (r.variables[0].model_copy(update={'unit': 'DN'}),),
        'metadata': r.metadata.model_copy(update={'calibration_scale': .0001, 'calibration_offset': -.1})})
    target = mapping.target.model_copy(update={'unit': '1'})
    mapping = mapping.model_copy(update={'target': target, 'relationship': 'convertible_to'})
    recipe = recipe.model_copy(update={'mappings': (mapping,), 'operations': (
        Operation(operation='calibrate', source_asset=r.asset_id, source_variable=rows[0].variable,
                  from_unit='DN', to_unit='1', scale=.0001, offset=-.1),)})
    raw = rows[0].model_copy(update={'value': 10, 'unit': 'DN'})
    outputs = list(run((source,), recipe, (raw,)))
    assert outputs[0].value == pytest.approx(-.099)
    assert outputs[0].unit == '1'
    assert raw.value == 10


def test_qa_veto_cannot_become_eligibility(bundle, tmp_path):
    from dataset_prototype.scoped_review import review_metadata
    class RejectingQA(FakeBackend):
        def generate(self, role, instruction, data, schema):
            if role == 'qa':
                return schema(finding_ids=[data['unique_findings'][0]['finding_id']],
                              summary='Revise the synthesis before proceeding.', decision='reject')
            return super().generate(role, instruction, data, schema)
    result = review_metadata(review_bundle(bundle), RejectingQA(), tmp_path/'qa-veto')
    assert result.qa_decision == 'reject'
    assert result.model_consensus == 'needs_revision' and result.execution_authorized is False


def test_real_gate_requires_scoped_report_and_checks_veto_bindings(bundle, monkeypatch, evidence_review_factory):
    from dataset_prototype.streaming import preflight
    from dataset_prototype.stream_contracts import StreamPlan, StreamBinding
    from dataset_prototype.review import source_set_digest
    import dataset_prototype.stream_sources as sources
    r, mapping, recipe, rows = bundle
    plan = StreamPlan(question='Generated real-boundary gate test', reader='sentinel-pixel',
        bindings=(StreamBinding(binding_id='generated',source=r,source_variable=mapping.source_variable,
            target=mapping.target,longitude=rows[0].longitude,latitude=rows[0].latitude),))
    monkeypatch.setattr(sources, 'validated_native', lambda binding: {})
    with pytest.raises(ValueError,match='matching evidence-bound'):
        preflight(plan,recipe)
    report = evidence_review_factory(plan,recipe)
    assert preflight(plan,recipe,evidence_review=report)
    for changed in [report.model_copy(update={'qa_decision':'reject'}),
                    report.model_copy(update={'recipe_content_digest':digest('stale')}),
                    report.model_copy(update={'source_digest':digest('changed source')}),
                    report.model_copy(update={'qa_finding_ids':('unknown.finding',)})]:
        with pytest.raises(ValueError):preflight(plan,recipe,evidence_review=changed)
    # Alter a nested finding while retaining a forged top-level eligibility label.
    review = report.reviews[0]
    changed = review.model_copy(update={'findings':(review.findings[0].model_copy(update={'status':Status.NEEDS_EVIDENCE}),)})
    with pytest.raises(ValueError):
        preflight(plan,recipe,evidence_review=report.model_copy(update={'reviews':(changed,*report.reviews[1:])}))
    assert source_set_digest(plan.resources) == report.source_digest


def test_not_applicable_needs_scope_evidence_and_sources_are_bound(bundle):
    from dataset_prototype.scoped_review import ReviewBundle
    from dataset_prototype.review import source_set_digest
    with pytest.raises(ValueError,match='requires evidence'):
        report(*case(status=Status.NOT_APPLICABLE,kind=EvidenceKind.MODEL_JUDGMENT))
    inputs=review_bundle(bundle)
    with pytest.raises(ValueError,match='source digest'):
        ReviewBundle.model_validate({**inputs.model_dump(mode='json'),'source_digest':digest('wrong')})
    with pytest.raises(ValueError,match='duplicate review source'):
        source_set_digest((bundle[0],bundle[0]))


def test_support_requires_actual_reference_and_source_provenance():
    review,evidence=case()
    second,other=case(Domain.SUPPORT)
    other=other.model_copy(update={'evidence_id':'support-evidence'})
    second=second.model_copy(update={'findings':(second.findings[0].model_copy(update={
        'evidence':('support-evidence',),'references':('units.coefficients',),'supports':('units.coefficients',)}),)})
    result=synthesize((review,second),(evidence,other),recipe_content_digest=HASH,source_digest=HASH,
        required_domains=(Domain.UNITS,Domain.SUPPORT))
    assert result.unique_findings[0].supporting_reviewers==(Domain.SUPPORT,)
    bad=review.model_copy(update={'findings':(review.findings[0].model_copy(update={'source':'invented source'}),)})
    with pytest.raises(ValueError,match='evidence provenance'):report(bad,evidence)
    bad=review.model_copy(update={'findings':(review.findings[0].model_copy(update={'supporting_reviewers':(Domain.SUPPORT,)}),)})
    with pytest.raises(ValueError,match='not submitted'):report(bad,evidence)
