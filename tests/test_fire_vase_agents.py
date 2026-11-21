"""Controlled-agent protocol tests; mock scores never stand in for LLM capability."""
from copy import deepcopy
import gzip
import json
import os
from pathlib import Path
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.agent_contracts import AgentAction,AgentConfig,QueryArguments,ScientificQuery,Usage
from dataset_prototype.embedding_study.agent_environment import load_environment,Dispatcher
from dataset_prototype.embedding_study.agent_render import render_initial,CONTRACTS,TOOLS,SYSTEM
from dataset_prototype.embedding_study.agent_providers import MockProvider,RuleProvider,ScriptedProvider,ProviderReply,OpenClawProvider,redact_transport
from dataset_prototype.embedding_study.agent_controller import run_episode
from dataset_prototype.embedding_study.agent_evaluation import score_episode
from dataset_prototype.embedding_study.agent_policy import proposed_call
from dataset_prototype.embedding_study.agent_runner import run_experiment
from dataset_prototype.embedding_study.agent_report import build_report
from dataset_prototype.embedding_study.reference import ReferenceAnswers
from dataset_prototype.embedding_study.backend import UpstreamBackend

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'reports/embedding_utility/fire_vase/config/agent-mock-v1.json'


@pytest.fixture
def config():return AgentConfig.model_validate_json(CONFIG.read_text())


@pytest.fixture
def environment(config):
    return load_environment(ROOT,config.snapshot,config.fixture,config.tasks,None)


def setup(environment,config,index=0,allowed=('R0',),metadata='M0'):
    data,tasks,stores,aliases,reverse,_=environment
    task=tasks.tasks[index]
    conditions=json.loads((ROOT/config.metadata).read_text())
    initial=render_initial(task,allowed,metadata,stores,aliases,conditions,
        {'max_steps':config.max_steps,'max_tool_calls':config.max_tool_calls,'seconds':config.max_episode_seconds})
    dispatcher=Dispatcher(task,allowed,stores,aliases,reverse)
    return task,initial,dispatcher


def test_no_task_gold_or_source_names_in_model_view(environment,config):
    _,tasks,_,_,_,_=environment
    forbidden={'task_id','family','operation','required_operations','answerable','reference_answer','ground_truth_method','tolerance','expected_provenance'}
    for i,t in enumerate(tasks.tasks):
        _,initial,_=setup(environment,config,i,('R0','R1','R2'),'M2')
        assert not (set(initial)&forbidden)
        content=json.dumps(initial)
        assert 'eval-' not in content and 'train-' not in content
        assert 'answerable' not in content and 'reference_answer' not in content
        assert initial['context']['fire_ids'][0].startswith('F')
        assert 'task_id' not in json.dumps(AgentAction.model_json_schema())
        assert not set(t.required_observation_ids)&set(json.loads(content).get('required_observation_ids',[]))


def test_metadata_changes_only_intended_evidence(environment,config):
    initial=[]
    for m in ('M0','M1','M2'):
        _,view,_=setup(environment,config,0,('R0','R1','R2'),m)
        initial.append({k:v for k,v in view.items() if k not in {'metadata','scientific_operation_contracts'}})
    assert len({digest(v) for v in initial})==1
    assert 'absolute' not in SYSTEM.lower()
    assert set(TOOLS)==set(CONTRACTS)


@pytest.mark.parametrize('bad',[
 {'action':'call','representation':'R0','operation':'python','arguments':{'fire_ids':['F000']}},
 {'action':'call','representation':'R0','operation':'cumulative','arguments':{'fire_ids':['F000'],'date':'bad'}},
 {'action':'call','representation':'R0','operation':'cumulative','arguments':{'fire_ids':['F000'],'date':'2020-01-01','path':'/tmp/hidden'}},
 {'action':'inspect','representation':'R0','path':'references.json'},
 {'action':'abstain','reason':'no evidence','operation':'profile'},
 {'action':'call','representation':'R0','operation':'profile','arguments':{'fire_ids':['F000'],'date':'2020-01-01'}},
])
def test_typed_actions_reject_code_files_and_invalid_arguments(bad):
    with pytest.raises(ValidationError):AgentAction.model_validate(bad)


def test_representation_and_source_authorization(environment,config):
    _,initial,dispatcher=setup(environment,config,0,('R1',))
    with pytest.raises(PermissionError):dispatcher.inspect('R0')
    with pytest.raises(PermissionError):dispatcher.call('R0','cumulative',QueryArguments(fire_ids=tuple(initial['context']['fire_ids']),date='2020-01-06'))
    with pytest.raises(PermissionError):dispatcher.call('R1','profile',QueryArguments(fire_ids=('F999',)))
    assert 'R0' not in initial['data'] and 'R2' not in initial['data']


def test_mock_executes_supported_provenance_and_null_usage(environment,config):
    task,initial,dispatcher=setup(environment,config)
    episode=run_episode(MockProvider(),initial,config,dispatcher)
    data=environment[0]
    grade=score_episode(task,('R0',),episode,dispatcher,ReferenceAnswers(data,3).answer(task),{h.fire_id:h for h in data.histories})
    assert grade['status']=='correct' and grade['provenance_complete']
    assert episode['counts']['model_calls']==2 and episode['counts']['tool_calls']==1
    assert episode['usage']['input_tokens'] is None and episode['usage']['provider_cost'] is None
    for step in episode['steps']:
        assert step['prompt_hash']==digest(step['prompt'])
        assert step['response_hash']==digest(step['raw_response'])
        assert task.task_id not in json.dumps(json.loads(step['prompt'])['initial'].get('context',{}))


class RecoveringProvider(MockProvider):
    def __init__(self,fault):self.fault=fault;self.first=True
    def invoke(self,prompt,*,parameters):
        if self.first:
            self.first=False
            return ProviderReply(json.dumps(self.fault) if not isinstance(self.fault,str) else self.fault,self.name,self.model,'test_fault',0)
        return super().invoke(prompt,parameters=parameters)


def test_unknown_action_and_malformed_output_recovery_are_preserved(environment,config):
    for fault in ('{truncated',{'action':'call','representation':'R0','operation':'eval','arguments':{'fire_ids':['F000']}}):
        _,initial,dispatcher=setup(environment,config)
        episode=run_episode(RecoveringProvider(fault),initial,config,dispatcher)
        assert episode['final']['kind']=='answer'
        assert episode['counts']['rejections']==1 and episode['counts']['recovery_attempts']==1
        assert episode['steps'][0]['response']=={'status':'rejected','code':'invalid_action'}
        assert episode['steps'][0]['raw_response']==(fault if isinstance(fault,str) else json.dumps(fault))


def test_rejection_feedback_identical_across_metadata(environment,config):
    feedback=[]
    for m in ('M0','M1','M2'):
        _,initial,dispatcher=setup(environment,config,0,('R1',),m)
        first={'action':'call','representation':'R0','operation':'cumulative','arguments':{'fire_ids':initial['context']['fire_ids'],'date':'2020-01-06'}}
        episode=run_episode(RecoveringProvider(first),initial,config,dispatcher)
        feedback.append(episode['steps'][0]['response'])
    assert len({digest(v) for v in feedback})==1


def test_no_result_is_not_a_richer_metadata_error(environment,config):
    for m in ('M0','M1','M2'):
        _,initial,dispatcher=setup(environment,config,0,('R2',),m)
        episode=run_episode(MockProvider(),initial,config,dispatcher)
        response=episode['steps'][0]['response']
        assert response['status']=='no_result' and 'reason' not in response
        assert 'answerable' not in response and 'reference_answer' not in response


def test_step_tool_token_and_byte_budgets(environment,config):
    _,initial,dispatcher=setup(environment,config)
    bad={'action':'call','representation':'R0','operation':'bad','arguments':{'fire_ids':['F000']}}
    episode=run_episode(ScriptedProvider([bad]*8),initial,config.model_copy(update={'max_tool_calls':2}),dispatcher)
    assert episode['termination']=='tool_call_limit' and episode['counts']['tool_calls']==2
    _,initial,dispatcher=setup(environment,config)
    select={'action':'select','representation':'R0'}
    episode=run_episode(ScriptedProvider([select]*8),initial,config.model_copy(update={'max_steps':2}),dispatcher)
    assert episode['termination']=='step_limit' and len(episode['steps'])==2
    _,initial,dispatcher=setup(environment,config)
    episode=run_episode(ScriptedProvider([select]*8,Usage(input_tokens=100,output_tokens=20)),initial,config.model_copy(update={'max_episode_tokens':100}),dispatcher)
    assert episode['termination']=='reported_token_limit' and episode['usage']['input_tokens']==100
    episode=run_episode(MockProvider(),initial,config.model_copy(update={'max_prompt_bytes':10}),dispatcher)
    assert episode['termination']=='prompt_byte_limit' and not episode['steps']


def test_right_number_without_receipt_is_rejected(environment,config):
    _,initial,dispatcher=setup(environment,config)
    episode=run_episode(RecoveringProvider({'action':'answer','value':30,'result_id':'made-up','evidence_ids':['fake']}),initial,config,dispatcher)
    assert episode['counts']['unsupported_answer_attempts']==1 and episode['counts']['rejections']==1
    assert episode['final']['kind']=='answer'  # later evidence-backed recovery, not silent repair


def test_appropriate_vs_incorrect_abstention(environment,config):
    data=environment[0];histories={h.fire_id:h for h in data.histories};refs=ReferenceAnswers(data,3)
    for allowed,expected in [(('R2',),'correct_abstention'),(('R0',),'incorrect_abstention'),(('R0','R1','R2'),'incorrect_abstention')]:
        task,initial,dispatcher=setup(environment,config,0,allowed)
        episode=run_episode(ScriptedProvider([{'action':'abstain','reason':'insufficient'}]),initial,config,dispatcher)
        assert score_episode(task,allowed,episode,dispatcher,refs.answer(task),histories)['status']==expected


def test_valid_but_wrong_operation_cannot_get_accidental_numeric_credit(environment,config):
    task,initial,dispatcher=setup(environment,config,0,('R0',))
    # Count = 6, not 30; grade must track the operation error separately as well.
    q=AgentAction(action='call',representation='R0',operation='sequence_days',arguments=QueryArguments(fire_ids=tuple(initial['context']['fire_ids'])))
    class WrongThenAnswer(MockProvider):
        def invoke(self,prompt,*,parameters):
            from dataset_prototype.embedding_study.agent_policy import finish_action
            history=json.loads(prompt)['history']
            action=finish_action(history) or q
            return ProviderReply(action.model_dump_json(),self.name,self.model,'test',0)
    episode=run_episode(WrongThenAnswer(),initial,config,dispatcher)
    grade=score_episode(task,('R0',),episode,dispatcher,30,{h.fire_id:h for h in environment[0].histories})
    assert grade['operation_selection_correct'] is False and grade['status']=='incorrect'
    assert grade['first_operation_selection_correct'] is False and grade['executed_operation_selection_errors']==1
    assert 'selected_wrong_operation' in grade['diagnostic_events']


def test_provenance_mismatch_and_inspect_select_protocol(environment,config):
    _,initial,dispatcher=setup(environment,config)
    actions=[{'action':'select','representation':'R0'},{'action':'inspect','representation':'R0'},
        {'action':'answer','result_id':'unknown','evidence_ids':[]}]
    episode=run_episode(ScriptedProvider(actions+[{'action':'abstain','reason':'no valid receipt'}]),initial,config,dispatcher)
    assert episode['steps'][0]['response']['status']=='selected'
    assert episode['steps'][1]['response']['status']=='data'
    assert episode['counts']['unsupported_answer_attempts']==1


def test_router_uses_public_question_not_hidden_labels(environment,config):
    for i in range(29):
        task,initial,_=setup(environment,config,i,('R0','R1','R2'))
        selected=proposed_call(initial)
        assert selected.action=='abstain' or selected.operation==task.operation
        altered=task.model_copy(update={'task_id':'secret-changed','answerable':{'R0':False,'R1':False,'R2':False}})
        data,tasks,stores,aliases,reverse,_=environment
        conditions=json.loads((ROOT/config.metadata).read_text())
        rerender=render_initial(altered,('R0','R1','R2'),'M0',stores,aliases,conditions,initial['interaction_budget'])
        assert proposed_call(rerender)==selected


def test_live_adapter_cost_guard_and_transport_identity(config):
    with pytest.raises(ValueError):OpenClawProvider(authorized=False)
    class FakeBackend:
        provider='verde';model='js2/gpt-oss-120b';endpoint='http://127.0.0.1:18891';_token='private-test-secret'
        runtime={'config_digest':'known','openclaw_version':'2026.5.18','provider_model_digest':None}
        def http(self,*args,**kwargs):
            assert kwargs['payload']['args']['model']=='verde/js2/gpt-oss-120b'
            assert kwargs['payload']['args']['schema']=={'type':'object'}
            assert kwargs['headers']['Authorization']=='Bearer private-test-secret'
            return {'ok':True,'result':{'details':{'provider':'verde','model':self.model,'json':{'action':'abstain','reason':'insufficient'}}}}
    prompt=json.dumps({'system':SYSTEM,'initial':{},'history':[]})
    provider=OpenClawProvider(authorized=True,backend=FakeBackend())
    reply=provider.invoke(prompt,parameters={'temperature':0,'max_output_tokens':256,'timeout_seconds':1})
    assert reply.error is None and reply.usage.input_tokens is None
    assert 'private-test-secret' not in json.dumps(reply.transport)
    provider.backend.model='different'
    # A returned identity differing from configured identity is rejected.
    provider.backend.http=lambda *a,**k:{'ok':True,'result':{'details':{'provider':'other','model':'different','json':{}}}}
    assert provider.invoke(prompt,parameters={'temperature':0,'max_output_tokens':256,'timeout_seconds':1}).error
    assert redact_transport({'Authorization':'secret','text':'abcsecret'},['secret'])=={'Authorization':'[REDACTED]','text':'abc[REDACTED]'}


def test_live_and_heldout_configs_are_inert_without_approval(tmp_path):
    base=json.loads(CONFIG.read_text());base.update(provider='openclaw',model='js2/gpt-oss-120b',max_real_calls=2,approved_external_cost_cap=0)
    path=tmp_path/'live.json';path.write_text(json.dumps(base))
    with pytest.raises(ValueError,match='authorization'):run_experiment(path,tmp_path/'live',upstream='unused',upstream_python='unused')
    base.update(provider='mock',model='deterministic-contract-mock-v1',phase='held_out_pending')
    path.write_text(json.dumps(base))
    with pytest.raises(ValueError,match='held-out'):run_experiment(path,tmp_path/'held',upstream='unused',upstream_python='unused')


def test_full_mock_matrix_replay_and_report_rebuild(tmp_path,config):
    upstream,python=os.getenv('FIRE_VASE_ROOT'),os.getenv('FIRE_VASE_PYTHON')
    if not upstream or not python:pytest.skip('explicit pinned worker required for full agent matrix; no substitute operations')
    changed=config.model_dump(mode='json');changed['repetitions']=1
    cfg=tmp_path/'config.json';cfg.write_text(json.dumps(changed))
    digests=[]
    for n in ('first','second'):
        directory=tmp_path/n
        manifest,_=run_experiment(cfg,directory,upstream=upstream,upstream_python=python,root=ROOT)
        assert manifest['distinct_cells']==348 and manifest['episodes']==348 and manifest['baseline_episodes']==348
        assert manifest['real_model_calls']==0 and manifest['provider_calls']==696
        with gzip.open(directory/'episodes.jsonl.gz','rt') as f:rows=[json.loads(line) for line in f]
        assert len({(r['task_id'],r['condition'],r['metadata']) for r in rows})==348
        assert not any(r['status']=='execution_failure' for r in rows)
        before=(directory/'report.md').read_bytes();build_report(directory);assert before==(directory/'report.md').read_bytes()
        digests.append(manifest['deterministic_results_digest'])
    assert len(set(digests))==1


def test_approximation_claim_checked_against_tool_not_self_grade(environment,config):
    index=next(i for i,t in enumerate(environment[1].tasks) if t.operation=='nearest_profile')
    task,initial,dispatcher=setup(environment,config,index,('R2',))
    class ExactClaim(MockProvider):
        def invoke(self,prompt,*,parameters):
            reply=super().invoke(prompt,parameters=parameters)
            value=json.loads(reply.content)
            if value['action']=='answer':value['interpretation']='exact'
            return ProviderReply(json.dumps(value),self.name,self.model,'test_claim',0)
    episode=run_episode(ExactClaim(),initial,config,dispatcher)
    reference=ReferenceAnswers(environment[0],3).answer(task)
    grade=score_episode(task,('R2',),episode,dispatcher,reference,{h.fire_id:h for h in environment[0].histories})
    assert grade['scientific_validity']=='FAIL' and grade['diagnostics']['approximation_recognition'] is False
    assert 'misinterpreted_valid_tool_result' in grade['diagnostic_events']


def test_wrong_date_valid_operation_is_not_a_valid_answer(environment,config):
    task,initial,dispatcher=setup(environment,config,0,('R0',))
    class WrongDate(MockProvider):
        def invoke(self,prompt,*,parameters):
            reply=super().invoke(prompt,parameters=parameters);value=json.loads(reply.content)
            if value['action']=='call':value['arguments']['date']='2020-01-05'
            return ProviderReply(json.dumps(value),self.name,self.model,'test_date',0)
    episode=run_episode(WrongDate(),initial,config,dispatcher)
    grade=score_episode(task,('R0',),episode,dispatcher,30,{h.fire_id:h for h in environment[0].histories})
    assert grade['operation_selection_correct'] and grade['status']=='incorrect'
    assert 'arguments_do_not_match_question' in grade['diagnostic_events']


def test_rule_router_ignores_metadata_and_model_prompts_never_include_gold(environment,config):
    _,a,_=setup(environment,config,0,('R0','R1','R2'),'M0')
    _,b,_=setup(environment,config,0,('R0','R1','R2'),'M2')
    assert proposed_call(a)==proposed_call(b)
    assert a['operations']==b['operations']


def test_global_provider_budget_keeps_scheduled_cells(tmp_path,config):
    upstream,python=os.getenv('FIRE_VASE_ROOT'),os.getenv('FIRE_VASE_PYTHON')
    if not upstream or not python:pytest.skip('explicit pinned worker required')
    payload=config.model_dump(mode='json');payload.update(repetitions=1,max_provider_calls=1)
    cfg=tmp_path/'limited.json';cfg.write_text(json.dumps(payload))
    manifest,_=run_experiment(cfg,tmp_path/'limited',upstream=upstream,upstream_python=python,root=ROOT)
    assert manifest['episodes']==348 and manifest['provider_calls']==1
    with gzip.open(tmp_path/'limited/episodes.jsonl.gz','rt') as f:rows=[json.loads(line) for line in f]
    assert len(rows)==348 and any(r['termination']=='provider_failure' for r in rows)


def test_nonfinite_claims_are_rejected_without_losing_raw_trace(environment,config):
    for value in ('NaN','1e1000'):
        _,initial,dispatcher=setup(environment,config)
        raw='{"action":"answer","value":'+value+'}'
        episode=run_episode(RecoveringProvider(raw),initial,config,dispatcher)
        assert episode['final']['kind']=='answer'
        assert episode['steps'][0]['raw_response']==raw
        assert episode['steps'][0]['response']['status']=='rejected'
        json.dumps(episode,allow_nan=False)


def test_invalid_argument_category_is_private_and_recoverable(environment,config):
    _,initial,dispatcher=setup(environment,config)
    fault={'action':'call','representation':'R0','operation':'cumulative','arguments':{'fire_ids':initial['context']['fire_ids'],'date':'not-a-date'}}
    episode=run_episode(RecoveringProvider(fault),initial,config,dispatcher)
    assert episode['counts']['invalid_arguments']==1
    assert episode['steps'][0]['private_rejection_category']=='invalid_arguments'
    assert episode['steps'][0]['response']=={'status':'rejected','code':'invalid_action'}
    assert episode['final']['kind']=='answer'
