"""Independent M3 arithmetic, splits, public boundary, cost scope and protocol checks."""
from copy import deepcopy
from datetime import date
from fractions import Fraction
import gzip
import json
import os
from pathlib import Path
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.pilot_contracts import PilotAction,PilotArguments,PilotQuery,PilotTask,OPS
from dataset_prototype.embedding_study.pilot_generate import generate,make_history,SEEDS
from dataset_prototype.embedding_study.pilot_reference import PilotReference,pulse_oracle,rational_fraction
from dataset_prototype.embedding_study.pilot_operations import direct_fraction,observed,assess_claim
from dataset_prototype.embedding_study.pilot_agent import PROTOCOL,render,PilotDispatcher,PilotMock,serialize
from dataset_prototype.embedding_study.pilot_runner import prepare,measure,evaluate,same,run,report
from dataset_prototype.embedding_study.agent_render import alias_maps
from dataset_prototype.embedding_study.agent_controller import run_episode
from dataset_prototype.embedding_study.agent_contracts import AgentConfig
from dataset_prototype.embedding_study.agent_providers import ScriptedProvider
from dataset_prototype.embedding_study.backend import UpstreamBackend
from dataset_prototype.embedding_study.contracts import FireHistory
from dataset_prototype.embedding_study.representations import InsufficientInformation

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/'data/fixtures/embedding_utility/milestone-3-v3'

@pytest.fixture(scope='module')
def inputs():return generate()

@pytest.fixture(scope='module')
def environment(inputs):
    upstream=os.environ.get('FIRE_VASE_ROOT');python=os.environ.get('FIRE_VASE_PYTHON')
    if not upstream or not python:pytest.skip('explicit pinned Fire VASE installation required')
    with UpstreamBackend(upstream,python) as backend:
        stores,artifact,features,coords,prep=prepare(inputs[0],backend)
        yield stores,artifact,features,coords,prep


def test_generation_frozen_inputs_and_separation(inputs):
    dataset,tasks,cohorts=inputs
    assert len(dataset.histories)==60
    assert digest(dataset)==digest(generate()[0])
    assert dataset.model_dump_json(indent=2)+'\n'==(FIXTURE/'histories.json').read_text()
    dev=[t for t in tasks if t.split=='development'];evaluation=[t for t in tasks if t.split=='evaluation']
    assert len(evaluation)==120 and len(dev)==30
    assert len({t.template_id for t in evaluation})==24
    assert set(cohorts['training']).isdisjoint(cohorts['development']+cohorts['evaluation'])
    assert set(cohorts['development']).isdisjoint(cohorts['evaluation'])
    assert {t.template_id for t in dev}.isdisjoint(t.template_id for t in evaluation)
    assert set(t.query.operation for t in evaluation)==set(OPS)
    assert {t.category for t in evaluation}=={'observation','morphology','compression','validity','cross_representation','efficiency'}
    assert {t.metadata_sensitivity for t in evaluation}=={'hypothesized','negative_control'}
    assert all(t.query.fire_ids[0] in cohorts[t.split] for t in tasks)


def test_temporal_edges_and_exact_zero(inputs):
    byid={h.fire_id:h for h in inputs[0].histories}
    missing=byid['m3-evaluation-12'];omitted=byid['m3-evaluation-13'];unknown=byid['m3-evaluation-14'];zero=byid['m3-evaluation-16']
    with pytest.raises(InsufficientInformation):observed(missing,missing.observations[4].date,True)
    with pytest.raises(InsufficientInformation):observed(omitted,omitted.observations[5].date,True)
    with pytest.raises(InsufficientInformation):observed(unknown,unknown.observations[0].date,True)
    assert observed(zero,zero.observations[4].date,True)==0
    assert observed(missing,missing.observations[4].date)-observed(missing,missing.observations[2].date)>0
    assert not missing.profile_eligible and not byid['m3-evaluation-15'].profile_eligible


def test_targeted_fraction_independent_every_eligible_history(inputs):
    for h in inputs[0].histories:
        if h.profile_eligible:
            assert direct_fraction(h,0,.5)==pytest.approx(rational_fraction(h,Fraction(0),Fraction(1,2)),abs=1e-12)
            assert direct_fraction(h,.75,1)==pytest.approx(rational_fraction(h,Fraction(3,4),Fraction(1)),abs=1e-12)
        else:
            with pytest.raises(InsufficientInformation):direct_fraction(h,0,.5)


def test_independent_pulse_edges():
    for g,expected in [([1,10,1,1,10,1],2),([0,0,0,0],0),([2,2,2,2],1),([3,3,1,9,9,1],2),([10,1,2,1,10],2)]:
        h=FireHistory.model_validate(make_history('pulse',g,'evaluation',date(2031,1,1),'ordinary'))
        assert pulse_oracle(h)==expected

@pytest.mark.parametrize('query',[
 {'operation':'cumulative','fire_ids':['F0']},
 {'operation':'daily_growth','fire_ids':['F0'],'date':'2031-01-01','claim':'ecological_analog'},
 {'operation':'front_fraction','fire_ids':['F0','F0']},
 {'operation':'interval_growth','fire_ids':['F0'],'date':'2031-01-01','start_date':'2031-01-02'},
 {'operation':'neighbor_stability','fire_ids':['F0'],'candidates':['F1','F1','F2']},
 {'operation':'eval','fire_ids':['F0']},
 {'operation':'profile','fire_ids':['F0'],'code':'print(1)'},
])
def test_closed_query_rejects_invalid_and_code(query):
    with pytest.raises(ValidationError):PilotQuery.model_validate(query)


def test_all_operations_agree_with_independent_references(inputs,environment):
    dataset,tasks,_=inputs;stores,artifact,features,coords,prep=environment;reference=PilotReference(dataset)
    assert set(artifact.training_ids)=={h.fire_id for h in dataset.histories if h.split=='train'}
    for task in tasks:
        answer=reference.answer(task.query)
        for r,store in stores.items():
            store.clear();result=store.query(task.query)
            assert (not result['abstention'])==reference.sufficient(task.query,r),(task.task_id,r)
            if not result['abstention']:assert same(result['answer'],answer,task.tolerance),(task.task_id,r)
            assert store.query(task.query)==result and store.last_cache_hit
    for h in dataset.histories:
        if h.profile_eligible:
            assert features[h.fire_id]['traits']['pulse_count']==pulse_oracle(h)
            assert features[h.fire_id]['traits']['front_loaded_fraction']==pytest.approx(direct_fraction(h,0,.5))
            assert features[h.fire_id]['traits']['late_growth_fraction']==pytest.approx(direct_fraction(h,.75,1))


def test_targeted_scalar_avoids_upstream_worker(inputs,environment):
    stores=environment[0];h=next(h for h in inputs[0].histories if h.profile_eligible)
    count=stores['R0'].backend.calls
    for op in ('front_fraction','late_fraction','cumulative','daily_growth','interval_growth'):
        q={'operation':op,'fire_ids':[h.fire_id]}
        if op in ('cumulative','daily_growth','interval_growth'):q['date']=h.observations[3].date
        if op=='interval_growth':q['start_date']=h.observations[1].date
        stores['R0'].clear();assert not stores['R0'].query(PilotQuery(**q))['abstention']
    assert stores['R0'].backend.calls==count


def public_setup(inputs,environment,op='front_fraction'):
    task=next(t for t in inputs[1] if t.split=='evaluation' and t.query.operation==op and all(i in PilotReference(inputs[0]).profiles for i in t.query.fire_ids))
    aliases,reverse=alias_maps(inputs[0]);stores=environment[0]
    costs={r:{'cold_ns':300 if r=='R0' else 100,'warm_ns':10,'preparation_ns':1000} for r in stores}
    config=AgentConfig.model_validate_json((ROOT/'reports/embedding_utility/fire_vase/config/agent-mock-frozen-v2.json').read_text())
    return task,aliases,reverse,stores,costs,config


def test_public_projection_isolation_no_keys_and_bounded(inputs,environment):
    aliases,_=alias_maps(inputs[0]);stores=environment[0];cost={r:{'cold_ns':10,'warm_ns':5,'preparation_ns':30} for r in stores}
    for t in (t for t in inputs[1] if t.split=='evaluation'):
        views=[render(t,('R0','R1','R2'),m,stores,aliases,cost) for m in ('M0','M1','M2')]
        assert len({digest({k:v for k,v in x.items() if k!='metadata'}) for x in views})==1
        prompt=serialize(views[-1],[])
        assert len(prompt.encode())<44000 # headroom for proposals and evidence receipts
        for forbidden in ('task_id','template_id','answerability','reference_answer','ground_truth','m3-evaluation-','m3-training-'):
            assert forbidden not in prompt
        assert 'operation' not in views[-1]['context']
        assert 'correct' not in views[-1]['workload']['measured_costs']


def test_v3_controller_receipts_authorization_and_independent_scoring(inputs,environment):
    task,aliases,reverse,stores,costs,config=public_setup(inputs,environment)
    public=render(task,('R0','R1','R2'),'M2',stores,aliases,costs)
    dispatcher=PilotDispatcher(task,('R0','R1','R2'),stores,aliases,reverse)
    for s in stores.values():s.clear()
    episode=run_episode(PilotMock(),public,config,dispatcher,protocol=PROTOCOL)
    assert episode['termination']=='completed' and episode['final']['evidence_ids']
    oracle=PilotReference(inputs[0]);suff={r:oracle.sufficient(task.query,r) for r in stores}
    result=evaluate(task,episode,dispatcher,oracle.answer(task.query),suff,costs)
    assert result['status']=='correct' and result['provenance_complete']
    assert result['usage']['provider_cost'] is None
    assert result['selected_total_workload_including_routing_ns']>=result['measured_workload_costs_ns']['R0']
    wrong=task.model_copy(update={'query':PilotQuery(operation='late_fraction',fire_ids=task.query.fire_ids)})
    assert evaluate(wrong,episode,dispatcher,episode['final']['answer'],suff,costs)['status']=='incorrect_answer'
    restricted=PilotDispatcher(task,('R2',),stores,aliases,reverse)
    with pytest.raises(PermissionError):restricted.call('R0','front_fraction',PilotArguments(fire_ids=[aliases[task.query.fire_ids[0]]]))
    with pytest.raises(PermissionError):dispatcher.call('R0','front_fraction',PilotArguments(fire_ids=['F999']))


def test_malformed_v3_recovery_no_repairs(inputs,environment):
    task,aliases,reverse,stores,costs,config=public_setup(inputs,environment)
    public=render(task,('R0',),'M0',stores,aliases,costs)
    provider=ScriptedProvider(['{broken',{'action':'abstain','reason':'Unsupported','interpretation':'insufficient'}])
    dispatcher=PilotDispatcher(task,('R0',),stores,aliases,reverse)
    episode=run_episode(provider,public,config,dispatcher,protocol=PROTOCOL)
    assert episode['counts']['rejections']==1 and episode['counts']['recovery_attempts']==1
    assert episode['steps'][0]['raw_response']=='{broken'
    assert episode['steps'][0]['response']=={'status':'rejected','code':'invalid_action'}


def test_live_plan_is_disabled_and_input_bound():
    from dataset_prototype.embedding_study.pilot_runner import authorize_live
    config=json.loads((ROOT/'reports/embedding_utility/fire_vase/config/agent-live-pilot-m3-v1.json').read_text())
    with pytest.raises(PermissionError,match='authorization|authorized'):
        authorize_live(config,ROOT,FIXTURE)
    enabled={**config,'access_authorized':True,'cost_basis':'operator_confirmed_no_external_charge'}
    with pytest.raises(PermissionError,match='smoke'):
        authorize_live(enabled,ROOT,FIXTURE)
    changed={**enabled,'input_sha256':{}}
    with pytest.raises(ValueError,match='hash|inputs|integrity|identity|frozen|required'):
        authorize_live(changed,ROOT,FIXTURE)


def test_real_expense_and_unsupported_parameters_fail_closed():
    from dataset_prototype.embedding_study.pilot_contracts import PilotLiveConfig
    with pytest.raises(ValidationError):PilotLiveConfig(fixture='x',input_sha256={},model='x',approved_external_cost_cap=1)
    with pytest.raises(ValidationError):PilotAction(action='call',representation='R0',operation='profile',arguments={'fire_ids':['F0']},value=[1])
    with pytest.raises(ValidationError):PilotAction(action='answer',value=float('inf'))


def test_cost_frontier_includes_cached_direct_and_agent_routing(inputs,environment):
    task,aliases,reverse,stores,costs,config=public_setup_for_cost(inputs,environment)
    for store in stores.values():store.clear()
    public=render(task,('R0','R1','R2'),'M2',stores,aliases,costs)
    dispatcher=PilotDispatcher(task,('R0','R1','R2'),stores,aliases,reverse)
    episode=run_episode(PilotMock(rule=True),public,config,dispatcher,protocol=PROTOCOL)
    reference=PilotReference(inputs[0]);suff={r:reference.sufficient(task.query,r) for r in stores}
    grade=evaluate(task,episode,dispatcher,reference.answer(task.query),suff,costs)
    assert grade['status']=='correct' and grade['selected_representation']=='R1'
    assert grade['task_pareto_min_valid_cost_ns']==100
    assert grade['selected_total_workload_including_routing_ns']>=100
    assert grade['usage']['input_tokens'] is None
    changed=deepcopy(episode);changed['final']['interpretation']='exact'
    if task.query.operation=='projected_distance':assert evaluate(task,changed,dispatcher,reference.answer(task.query),suff,costs)['status']=='incorrect_answer'


def public_setup_for_cost(inputs,environment):
    task,aliases,reverse,stores,costs,config=public_setup(inputs,environment)
    return task.model_copy(update={'preparation_paid':True,'workload_queries':1}),aliases,reverse,stores,costs,config



def test_runner_replay_matrix_and_report_regeneration(inputs,environment,tmp_path):
    upstream=os.environ['FIRE_VASE_ROOT'];python=os.environ['FIRE_VASE_PYTHON']
    first=run(ROOT,FIXTURE,tmp_path/'a',upstream,python,split='development',repetitions=1)
    second=run(ROOT,FIXTURE,tmp_path/'b',upstream,python,split='development',repetitions=1)
    assert first['status']==second['status']=='complete'
    assert first['episodes']==360 and first['real_model_calls']==0
    assert first['deterministic_digest']==second['deterministic_digest']
    summary=json.loads((tmp_path/'a/summary.json').read_text());original=(tmp_path/'a/report.md').read_bytes()
    report(tmp_path/'a',summary)
    assert (tmp_path/'a/report.md').read_bytes()==original
    assert all(all(x==0 for x in row['mean_task_level_rate_difference'].values()) for row in summary['metadata_contrasts'] if row['paired_tasks'])
    with gzip.open(tmp_path/'a/episodes.jsonl.gz','rt') as f:episodes=[json.loads(x) for x in f]
    assert len({(e['task_id'],e['regime'],e['metadata']) for e in episodes})==360
    with gzip.open(tmp_path/'a/public_protocols.jsonl.gz','rt') as f:
        for line in f:
            public=json.loads(line)['public_prompt']
            assert 'task_id' not in json.dumps(public) and 'answerable' not in json.dumps(public)


def test_projection_error_bound_and_nullspace_dimension(inputs):
    import numpy as np
    reference=PilotReference(inputs[0]);ids=list(reference.profiles)
    assert np.linalg.matrix_rank(reference.components)==3
    # The simplex has 19 affine degrees of freedom; 3 PCs leave >=16 local.
    constraint=np.vstack([reference.components/reference.scale,np.ones(20)])
    assert 20-np.linalg.matrix_rank(constraint)>=16
    for i,j in zip(ids,ids[1:]):
        p,q=np.array(reference.profiles[i]),np.array(reference.profiles[j])
        a,b=reference.recon[i],reference.recon[j]
        assert abs(np.linalg.norm(p-q)-np.linalg.norm(a-b))<=np.linalg.norm(p-a)+np.linalg.norm(q-b)+1e-12
