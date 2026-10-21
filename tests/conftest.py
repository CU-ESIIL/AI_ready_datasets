from pathlib import Path
import pytest
from dataset_prototype.adapters import MockMESAClient
from dataset_prototype.orchestration import load_track
from dataset_prototype.contracts import ScientificRequest, Operation
from dataset_prototype.agents import SemanticAgent, HarmonizationAgent


@pytest.fixture
def client():
    return MockMESAClient(Path('data/fixtures'))


@pytest.fixture
def config():
    return load_track('tracks/food_security/config.json')


@pytest.fixture
def request_model(config):
    return ScientificRequest(question=config.question, support=config.support, variables=config.variables, modalities=config.modalities)


@pytest.fixture
def bundle(client):
    r = client.resources[0]
    v = r.variables[0]
    mapping = SemanticAgent().propose(r, v.name, v)
    recipe = HarmonizationAgent().propose((mapping,), (Operation(operation='validate', source_variable=v.name),)).model_copy(update={'status':'approved'})
    return r, mapping, recipe, client.fetch(r.asset_id)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    import socket
    def forbidden(*args, **kwargs):
        raise AssertionError('Tests must not access the network')
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    monkeypatch.setattr(socket.socket, 'connect', forbidden)


@pytest.fixture
def evidence_review_factory():
    """Explicit generated review records for offline gate tests, not scientific approval."""
    from dataset_prototype.contracts import digest, recipe_content_digest
    from dataset_prototype.review import REQUIRED_DOMAINS, synthesize, source_set_digest
    from dataset_prototype.review_contracts import Evidence, ReviewFinding, SpecialistReview
    def build(plan, recipe):
        ledger=[];reviews=[]
        for domain in REQUIRED_DOMAINS:
            identifier=domain.value+'.generated_test'
            ledger.append(Evidence(evidence_id=identifier, domain=domain,
                kind='DERIVED_DETERMINISTICALLY', source='offline-generated-test-only',
                statement='Generated contract fixture; no scientific approval.', content_digest=digest(identifier)))
            finding=ReviewFinding(finding_id=identifier, reviewer_domain=domain, status='PASS',
                claim='Generated contract fixture.', evidence=(identifier,), source='offline-generated-test-only',
                required_action='Test gate behavior only.', confidence=1)
            reviews.append(SpecialistReview(reviewer_domain=domain,
                recipe_content_digest=recipe_content_digest(recipe), findings=(finding,)))
        report=synthesize(reviews,ledger,recipe_content_digest=recipe_content_digest(recipe),
                          source_digest=source_set_digest(plan.resources))
        return report.model_copy(update={'qa_decision':'accept',
            'qa_finding_ids': tuple(f.finding_id for f in report.unique_findings)})
    return build
