"""Mock transports test real backend protocols; live evidence stays under run/."""
import json
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import Operation, digest
from dataset_prototype.model_agents import (OllamaBackend, CandidateChoice, SemanticJudgment, RecipePlan,
    ModelSemanticAgent, ModelHarmonizationAgent, ModelDiscoveryAgent, source_evidence)
from dataset_prototype.harmonization import assess, run
from dataset_prototype.discovery import run as discover


def test_ollama_schema_no_tools_and_trace():
    calls=[]
    def http(url,**kwargs):
        calls.append((url,kwargs))
        if url.endswith('/api/tags'):
            return {'models':[{'name':'test-model','digest':'sha256:actual-model-id'}]}
        payload=kwargs['payload']
        assert 'tools' not in payload
        assert payload['stream'] is False and payload['format']['additionalProperties'] is False
        return {'done':True,'done_reason':'stop','message':{'content':'{"asset_ids":[],"rationale":"No adequate source evidence"}'},'eval_count':12,'prompt_eval_count':100}
    backend=OllamaBackend('test-model',http=http)
    result=backend.generate('discovery','select sources',{'source':'test'},CandidateChoice)
    assert result.asset_ids==()
    trace=backend.traces[0]
    assert trace.model_digest=='sha256:actual-model-id' and trace.output_tokens==12
    assert trace.response_digest==digest(trace.output_json)
    assert len(calls)==2


@pytest.mark.parametrize('response',[
    {'done':False,'message':{'content':'{}'}},
    {'done':True,'done_reason':'length','message':{'content':'{}'}},
    {'done':True,'message':{'content':'```json\n{}\n```'}},
    {'done':True,'message':{'content':'{"asset_ids":[],"rationale":"x","arbitrary_code":"exec()"}'}}
])
def test_malformed_or_incomplete_never_repaired(response):
    def http(url,**kwargs): return {'models':[{'name':'m','digest':'id'}]} if url.endswith('/api/tags') else response
    backend=OllamaBackend('m',http=http)
    with pytest.raises(ValueError): backend.generate('discovery','task',{},CandidateChoice)
    assert len(backend.traces)==1


def test_missing_model_no_download_and_transport_bounds():
    backend=OllamaBackend('absent',http=lambda *a,**k:{'models':[]})
    with pytest.raises(ValueError,match='not installed'): backend.generate('discovery','task',{},CandidateChoice)
    with pytest.raises(ValueError,match='loopback'): OllamaBackend('m',endpoint='http://external.example')
    with pytest.raises(ValueError,match='endpoint'): OllamaBackend('m',endpoint='https://user:secret@example.org')


class StubBackend:
    model='test-model'
    _model_digest='sha256:test-model-version'
    def __init__(self,result): self.result=result;self.inputs=[]
    def generate(self,role,instruction,evidence,schema):
        self.inputs.append((role,evidence,schema))
        return self.result


def test_model_only_controls_judgment_and_cannot_self_approve(bundle):
    r,m,p,raw=bundle
    backend=StubBackend(SemanticJudgment(relationship='equivalent_to',evidence=('Exact supplied definition/method/unit comparison',),confidence=1))
    mapping=ModelSemanticAgent(backend).propose(r,m.source_variable,m.target)
    assert mapping.source_asset==r.asset_id and mapping.target==m.target
    assert mapping.novel and mapping.review_status=='needs_review'
    assert 'target' not in SemanticJudgment.model_fields and 'source_asset' not in SemanticJudgment.model_fields
    recipe=p.model_copy(update={'mappings':(mapping,)})
    assert assess(recipe,(r,)).outcome=='require_human_review'
    with pytest.raises(ValueError,match='human review'): tuple(run((r,),recipe,raw))


def test_generated_operation_scope_and_source_identity(bundle):
    r,m,p,raw=bundle
    from dataset_prototype.decision_ir import build_capabilities, RecipeDecision, SelectDecision
    cap=build_capabilities((r,),(m,)); option=cap.options[0]
    decision=RecipeDecision(capability_digest=cap.identity,status='PROPOSED',rationale='Keep source-native observations',
        steps=(SelectDecision(operation_id=option.operation_id,option_id=option.option_id),))
    backend=StubBackend(decision)
    recipe=ModelHarmonizationAgent(backend).propose((m,),(r,))
    assert recipe.status=='needs_review' and recipe.proposals[0].agent=='ollama:test-model'
    backend.result=decision.model_copy(update={'steps':(SelectDecision(operation_id=option.operation_id,option_id='invented'),)})
    with pytest.raises(ValueError,match='not offered'): ModelHarmonizationAgent(backend).propose((m,),(r,))


def test_discovery_cannot_invent_source(client,request_model):
    backend=StubBackend(CandidateChoice(asset_ids=('invented',),rationale='bad source'))
    with pytest.raises(ValueError,match='invented'): ModelDiscoveryAgent(backend).propose(request_model,discover(request_model,client))
