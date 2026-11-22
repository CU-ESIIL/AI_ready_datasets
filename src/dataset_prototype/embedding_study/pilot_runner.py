"""Reproducible expanded synthetic benchmark, measured rivals and inert live plan."""
import argparse
from collections import Counter,defaultdict
from datetime import datetime,timezone
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import random
import socket
from statistics import median
import subprocess
from time import perf_counter_ns
from ..contracts import digest
from .contracts import Dataset, PIN, UPSTREAM_SHA256
from .backend import UpstreamBackend
from .representations import make_features,fit_artifact,coordinates,provenance,RepresentationView
from .agent_render import alias_maps
from .agent_controller import run_episode
from .agent_contracts import AgentConfig
from .pilot_contracts import PilotTask, PilotAction
from .pilot_generate import SEEDS
from .pilot_operations import PilotView,CONTRACTS
from .pilot_reference import PilotReference
from .pilot_agent import PilotMock,PilotDispatcher,PROTOCOL,render


def dump(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rows(path,values):
    # Deterministic gzip headers; timings remain explicitly variable content.
    with Path(path).open('wb') as raw:
        with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as f:
            for value in values:f.write((json.dumps(value,sort_keys=True,allow_nan=False)+'\n').encode())
def same(a,b,tolerance=1e-8):
    if a is None or b is None:return a is b
    if isinstance(a,bool) or isinstance(b,bool):return type(a)==type(b) and a==b
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):return math.isclose(a,b,abs_tol=tolerance,rel_tol=tolerance)
    if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(same(x,y,tolerance) for x,y in zip(a,b))
    if isinstance(a,dict) and isinstance(b,dict):return set(a)==set(b) and all(same(a[k],b[k],tolerance) for k in a)
    return type(a)==type(b) and a==b


def prepare(dataset,backend):
    feature_ns={};coord_ns={};features={};coords={}
    for h in dataset.histories:
        start=perf_counter_ns();features[h.fire_id]=make_features(h,backend);feature_ns[h.fire_id]=perf_counter_ns()-start
    start=perf_counter_ns();artifact=fit_artifact(dataset,features,backend,3);fit_ns=perf_counter_ns()-start
    for h in dataset.histories:
        start=perf_counter_ns();coords[h.fire_id]=coordinates(features[h.fire_id]['profile'],artifact) if features[h.fire_id] else None
        coord_ns[h.fire_id]=perf_counter_ns()-start
    lineages={h.fire_id:provenance(h) for h in dataset.histories}
    stores={r:PilotView(RepresentationView(r,p,lineages,backend,artifact)) for r,p in {
      'R0':{h.fire_id:h for h in dataset.histories},'R1':features,'R2':coords}.items()}
    training_ns=sum(feature_ns[h.fire_id] for h in dataset.histories if h.split=='train')
    return stores,artifact,features,coords,{'feature_ns':feature_ns,'coordinate_ns':coord_ns,'fit_ns':fit_ns,
      'training_features_ns':training_ns,'worker_startup_ns':backend.startup_ns,
      'scope':'Resident bounded synthetic inputs. No physical IO or cold OS-cache claim; upstream IPC included. Training PCA cost charged once to each counterfactual new-workload R2 scenario, not once per query.'}


def measure(tasks,stores,answers,preparation,repeats=7):
    records=[];costs={};sufficiency={}
    for task in tasks:
        ids=set((*task.query.fire_ids,*task.query.candidates));taskcost={};sufficiency[task.task_id]={}
        for r,store in stores.items():
            cold=[];warm=[];answers_seen=[]
            for repeat in range(repeats):
                store.clear();start=perf_counter_ns();result=store.query(task.query);cold.append(perf_counter_ns()-start)
                start=perf_counter_ns();again=store.query(task.query);warm.append(perf_counter_ns()-start)
                if not same(result,again):raise ValueError('cache changed scientific answer')
                answers_seen.append(result)
                records.append({'task_id':task.task_id,'representation':r,'repeat':repeat,'cold_ns':cold[-1],
                  'warm_ns':warm[-1],'result':result,'correct':same(result['answer'],answers[task.task_id],task.tolerance),
                  'cache_scope':'application only; exact repeated query','worker_calls_cumulative':store.backend.calls})
            result=answers_seen[0]
            # All independent numerical references must agree BEFORE model execution.
            if not result['abstention'] and not same(result['answer'],answers[task.task_id],task.tolerance):
                raise ValueError('independent reference disagreement: '+task.task_id+' '+r)
            sufficiency[task.task_id][r]=not result['abstention']
            prep=0 if r=='R0' else sum(preparation['feature_ns'][i] for i in ids)
            if r=='R2':prep+=sum(preparation['coordinate_ns'][i] for i in ids)+preparation['training_features_ns']+preparation['fit_ns']
            taskcost[r]={'cold_ns':median(cold),'warm_ns':median(warm),'preparation_ns':prep}
        costs[task.task_id]=taskcost
    return records,costs,sufficiency


def evaluate(task,episode,dispatcher,answer,sufficiency,costs):
    final=episode['final'];calls=dispatcher.calls;last=calls[-1] if calls else None
    first=calls[0] if calls else None;allowed=dispatcher.allowed
    available=any(sufficiency[r] for r in allowed)
    if episode['termination']!='completed':status='execution_failure'
    elif final['kind']=='abstain':status='incorrect_abstention' if available else 'appropriate_abstention'
    elif last is None:status='unsupported_answer'
    else:
        selected=dispatcher.results[final['supporting_result']]
        exact_query=selected['query']==task.query.model_dump(mode='json')
        valid_claim=not selected['result']['approximate'] or final['interpretation']=='approximate'
        status='correct' if exact_query and same(final['answer'],answer,task.tolerance) and valid_claim else 'incorrect_answer'
    n=task.workload_queries
    estimated={r:(0 if task.preparation_paid else c['preparation_ns'])+c['cold_ns']+(n-1)*c['warm_ns'] for r,c in costs.items()}
    eligible={r:v for r,v in estimated.items() if sufficiency[r]}
    frontier=min(eligible.values()) if eligible else None
    chosen=dispatcher.results[final['supporting_result']]['representation'] if final and final['kind']=='answer' else last['representation'] if last else None
    routing=episode['total_elapsed_ns']-sum(c['scientific_dispatch_ns'] for c in calls)
    # Routing happens for each question in this repeated identical workload scenario.
    selected_total=estimated[chosen]+n*routing if chosen in eligible and status=='correct' else None
    operation_match=bool(first and first['query']['operation']==task.query.operation)
    args_match=bool(first and first['query']==task.query.model_dump(mode='json'))
    return {'task_id':task.task_id,'category':task.category,'template_id':task.template_id,'status':status,
      'metadata_sensitivity':task.metadata_sensitivity,'representation_sufficiency':{r:sufficiency[r] for r in allowed},
      'selected_representation':chosen,'first_operation_correct':operation_match,'first_arguments_correct':args_match,
      'provenance_complete':bool(final and final['kind']=='answer' and final['evidence_ids']),
      'temporal_error':task.category=='observation' and status in {'incorrect_answer','incorrect_abstention'},
      'normalization_error':(task.query.operation in {'front_fraction','late_fraction','profile'} or task.query.claim=='absolute_from_normalized') and status=='incorrect_answer',
      'compression_error':(task.category=='compression' or task.query.claim=='exact_profile_from_pcs') and status in {'incorrect_answer','incorrect_abstention'},
      'approximation_target':task.accuracy,'scientific_dispatch_ns':sum(c['scientific_dispatch_ns'] for c in calls),
      'routing_and_controller_ns':routing,'total_elapsed_ns':episode['total_elapsed_ns'],
      'usage':episode['usage'],'counts':episode['counts'],'measured_workload_costs_ns':estimated,
      'task_pareto_min_valid_cost_ns':frontier,'selected_total_workload_including_routing_ns':selected_total,
      'cost_regret_with_routing_ns':selected_total-frontier if selected_total is not None and frontier is not None else None,
      'cost_scope':'Measured median cold + (N-1) exact-query-cache hits + unpaid preparation. Agent route overhead charged N times. These are counterfactual workload accounting scenarios, not measured end-to-end N-query runs.',
      'scientific_validity':'deterministic_synthetic_only' if status in {'correct','appropriate_abstention'} else 'not_established'}


def authorize_live(config,root,fixture):
    from .pilot_contracts import PilotLiveConfig
    config=PilotLiveConfig.model_validate(config)
    if not config.access_authorized or config.cost_basis!='operator_confirmed_no_external_charge':
        raise PermissionError('Verified access and explicit no-external-charge authorization required; no inference attempted')
    if Path(config.fixture).resolve()!=Path(fixture).resolve():raise ValueError('frozen fixture mismatch')
    for name,expected in config.input_sha256.items():
        if sha(Path(root)/name)!=expected:raise ValueError('frozen live input identity mismatch')
    actual={str(p.relative_to(Path(root))):sha(p) for p in Path(fixture).glob('*.json')}
    if config.input_sha256!=actual:raise ValueError('complete frozen input hashes required')
    if not config.smoke_evidence:raise PermissionError('Verified frozen smoke evidence required before pilot')
    smoke=json.loads((Path(root)/config.smoke_evidence).read_text())
    if not all(smoke.get(k) is True for k in ('identity_verified','parsing_verified','usage_accounting_verified','governance_verified')):
        raise PermissionError('smoke verification incomplete; unknown usage must be documented explicitly')
    if smoke.get('model')!=config.model or smoke.get('external_cost')!=0:raise ValueError('smoke identity/cost mismatch')
    return config


def run(root,fixture,output,upstream,python,*,split='evaluation',repetitions=2,live_config=None):
    root=Path(root).resolve();fixture=Path(fixture).resolve();output=Path(output).resolve()
    live=authorize_live(live_config,root,fixture) if live_config is not None else None
    if live and (split!='evaluation' or repetitions!=live.repetitions):raise ValueError('frozen live schedule mismatch')
    from .agent_providers import OpenClawProvider
    provider=OpenClawProvider(live.runtime,authorized=True) if live else PilotMock()
    if live and provider.model!=live.model:raise ValueError('provider model mismatch')
    output.mkdir(parents=True,exist_ok=False)
    dataset=Dataset.model_validate_json((fixture/'histories.json').read_text())
    tasks=[PilotTask.model_validate(t) for t in json.loads((fixture/(split+'_tasks.json')).read_text())]
    if any(t.split!=split for t in tasks):raise ValueError('split mismatch')
    # Freeze all inputs and protocol BEFORE any provider proposal (even mock).
    input_hashes={str(p.relative_to(root)):sha(p) for p in fixture.glob('*.json')}
    frozen={'input_sha256':input_hashes,'version':'fire-pilot-experiment-v3','provider':provider.name,'simulated':provider.simulated,'split':split,
      'repetitions':repetitions,'seed':SEEDS['schedule'],'metadata_conditions':['M0','M1','M2'],
      'regimes':['R0','R1','R2','adaptive'],'max_steps':6,'max_tool_calls':4,'max_prompt_bytes':48000,
      'max_provider_calls':len(tasks)*4*3*repetitions*6,'live_authorized':False,'real_model_calls':0,
      'metadata_interpretation':'Mock ignores metadata; invariance only. Public timing table never includes success, sufficiency, result or ideal view.',
      'inference_pending':'No real access/cost authorization assumed. Draft semantic rubrics need expert review before confirmatory scientific claims.'}
    if live:
        frozen.update(live_approval=live.model_dump(mode='json'),max_provider_calls=live.max_provider_calls,live_authorized=True)
    dump(output/'frozen_config.json',frozen);dump(output/'action_schema.json',PilotAction.model_json_schema())
    dump(output/'operation_registry.json',CONTRACTS)
    reference=PilotReference(dataset)
    answers={task.task_id:reference.answer(task.query) for task in tasks};dump(output/'private_reference_answers.json',answers)
    aliases,reverse=alias_maps(dataset)
    with UpstreamBackend(upstream,python) as backend:
        stores,artifact,features,coords,prep=prepare(dataset,backend)
        dump(output/'pca_artifact.json',artifact.model_dump(mode='json'));dump(output/'features.json',features)
        dump(output/'coordinates.json',coords);dump(output/'preparation.json',prep)
        development=[PilotTask.model_validate(t) for t in json.loads((fixture/'development_tasks.json').read_text())]
        dev_answers={t.task_id:reference.answer(t.query) for t in development}
        dev_records,dev_costs,_=measure(development,stores,dev_answers,prep)
        public_costs={}
        for op in {t.query.operation for t in tasks}:
            matches=[t for t in development if t.query.operation==op]
            if not matches:raise ValueError('development calibration missing operation')
            public_costs[op]={r:{key:median(dev_costs[t.task_id][r][key] for t in matches)
                for key in ('cold_ns','warm_ns','preparation_ns')} for r in stores}
        dump(output/'public_development_costs.json',public_costs)
        rows(output/'development_calibration.jsonl.gz',dev_records)
        start=perf_counter_ns();baseline,costs,suff=measure(tasks,stores,answers,prep);baseline_ns=perf_counter_ns()-start
        for t in tasks:
            for r in stores:
                if suff[t.task_id][r]!=reference.sufficient(t.query,r):raise ValueError('independent sufficiency disagreement')
        rows(output/'direct_baselines.jsonl.gz',baseline);dump(output/'cost_calibration.json',costs)
        config=AgentConfig.model_validate_json((root/'reports/embedding_utility/fire_vase/config/agent-mock-frozen-v2.json').read_text()).model_copy(update={'max_steps':6,'max_tool_calls':4})
        schedule=[(i,r,m,rep) for i in range(len(tasks)) for r in ('R0','R1','R2','adaptive') for m in ('M0','M1','M2') for rep in range(repetitions)]
        random.Random(SEEDS['schedule']).shuffle(schedule);episodes=[];traces=[];publics=[];invocations=0
        def bounded_invoke(prompt,*,parameters):
            nonlocal invocations
            if invocations>=frozen['max_provider_calls']:raise RuntimeError('global provider invocation cap exhausted')
            invocations+=1
            return provider.invoke(prompt,parameters=parameters)
        for i,r,m,rep in schedule:
            task=tasks[i];allowed=('R0','R1','R2') if r=='adaptive' else (r,)
            for store in stores.values():store.clear()
            public=render(task,allowed,m,stores,aliases,public_costs[task.query.operation])
            dispatcher=PilotDispatcher(task,allowed,stores,aliases,reverse)
            episode=run_episode(provider,public,config,dispatcher,protocol=PROTOCOL,invoke=bounded_invoke)
            if invocations>frozen['max_provider_calls']:raise ValueError('global mock invocation cap')
            identity={'task_id':task.task_id,'regime':r,'metadata':m,'repeat':rep,'provider':'real' if live else 'mock'}
            episodes.append({**identity,**evaluate(task,episode,dispatcher,answers[task.task_id],suff[task.task_id],costs[task.task_id])})
            traces.append({**identity,'episode':episode,'private_dispatch':dispatcher.calls})
            if rep==0:publics.append({**identity,'public_prompt':public})
        rule_rows=[]
        for task in tasks:
            for m in ('M0','M1','M2'):
                for store in stores.values():store.clear()
                public=render(task,('R0','R1','R2'),m,stores,aliases,public_costs[task.query.operation])
                dispatcher=PilotDispatcher(task,('R0','R1','R2'),stores,aliases,reverse)
                episode=run_episode(PilotMock(rule=True),public,config,dispatcher,protocol=PROTOCOL)
                identity={'task_id':task.task_id,'regime':'adaptive','metadata':m,'repeat':0,'provider':'rule'}
                rule_rows.append({**identity,**evaluate(task,episode,dispatcher,answers[task.task_id],suff[task.task_id],costs[task.task_id])})
                traces.append({**identity,'episode':episode,'private_dispatch':dispatcher.calls})
        rows(output/'episodes.jsonl.gz',episodes);rows(output/'rule_baselines.jsonl.gz',rule_rows)
        rows(output/'traces.jsonl.gz',traces);rows(output/'public_protocols.jsonl.gz',publics)
        summary=summarize(episodes,rule_rows,baseline,tasks)
        if live:summary.update(real_model_evidence='executed; see failures and usage fields',evidence_label='real model on synthetic tasks')
        dump(output/'summary.json',summary)
        report(output,summary)
        if input_hashes!={str(p.relative_to(root)):sha(p) for p in fixture.glob('*.json')}:raise ValueError('frozen inputs changed during run')
        code=list(Path(__file__).parent.glob('*.py'))
        manifest={'version':'fire-pilot-manifest-v3','status':'complete' if not any(e['status']=='execution_failure' for e in episodes+rule_rows) else 'complete_with_failures',
          'timestamp':datetime.now(timezone.utc).isoformat(),'synthetic':True,'real_model_calls':invocations if live else 0,
          'mock_invocations':0 if live else invocations,'provider':{'name':provider.name,'model':provider.model,'simulated':provider.simulated},'distinct_cells':len(tasks)*12,'episodes':len(episodes),'rule_episodes':len(rule_rows),
          'upstream_commit':PIN,'upstream_operation_sha256':UPSTREAM_SHA256,'upstream_status':backend.checkout_status,
          'worker_versions':backend.versions,'baseline_measurement_ns':baseline_ns,
          'input_sha256':{str(p.relative_to(root)):sha(p) for p in fixture.glob('*.json')},
          'code_sha256':{str(p.relative_to(root)):sha(p) for p in code},
          'output_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file()},
          'deterministic_digest':digest([{k:e[k] for k in ('task_id','regime','metadata','repeat','status','first_operation_correct')} for e in episodes]),
          'limitations':['Convenience synthetic tasks; no population inference','Draft evidence-claim rubrics, no expert gold','Frozen model-unseen cases visible to developers','Mock phrase parser is not scientific understanding','Timing includes isolated worker IPC; application cache only','No real-model evidence or metadata efficacy estimate']}
        dump(output/'manifest.json',manifest)
    return manifest


def summarize(episodes,rules,baselines,tasks):
    groups={}
    for provider,data in [('real' if episodes and episodes[0]['provider']=='real' else 'mock',episodes),('rule',rules)]:
        for r in sorted({e['regime'] for e in data}):
            for m in ('M0','M1','M2'):
                selected=[e for e in data if e['regime']==r and e['metadata']==m]
                groups[f'{provider}/{r}/{m}']={'n':len(selected),'status':dict(Counter(e['status'] for e in selected)),
                  'selected_views':dict(Counter(e['selected_representation'] or 'none' for e in selected)),
                  'median_routing_ns':median(e['routing_and_controller_ns'] for e in selected),
                  'usage_known':sum(e['usage']['input_tokens'] is not None for e in selected)}
    comparisons=[]
    for op in sorted({t.query.operation for t in tasks}):
        ids={t.task_id for t in tasks if t.query.operation==op};row={'operation':op}
        for r in ('R0','R1','R2'):
            selected=[b for b in baselines if b['task_id'] in ids and b['representation']==r and not b['result']['abstention']]
            row[r]={'answerable_task_count':len({b['task_id'] for b in selected}),'median_cold_ns':median(b['cold_ns'] for b in selected) if selected else None,'median_warm_ns':median(b['warm_ns'] for b in selected) if selected else None}
        comparisons.append(row)
    paired=[]
    for regime in ('R0','R1','R2','adaptive'):
        for stratum in ('all','hypothesized','negative_control'):
            selected=[e for e in episodes if e['regime']==regime and (stratum=='all' or e['metadata_sensitivity']==stratum)]
            cells=defaultdict(list)
            for e in selected:cells[(e['task_id'],e['metadata'])].append(e)
            ids=sorted({e['task_id'] for e in selected})
            for richer in ('M1','M2'):
                diffs={}
                for label,target in (('correct_answer','correct'),('appropriate_abstention','appropriate_abstention'),('incorrect_abstention','incorrect_abstention')):
                    contrasts=[]
                    for i in ids:
                        rates=[sum(e['status']==target for e in cells[(i,m)])/len(cells[(i,m)]) for m in (richer,'M0')]
                        contrasts.append(rates[0]-rates[1])
                    diffs[label]=sum(contrasts)/len(contrasts) if contrasts else None
                paired.append({'regime':regime,'stratum':stratum,'contrast':richer+'-M0','paired_tasks':len(ids),
                    'mean_task_level_rate_difference':diffs,'interpretation':'mock isolation only; repeats averaged within task; no population inference'})
    return {'version':'fire-pilot-summary-v3','groups':groups,'direct_comparisons':comparisons,'metadata_contrasts':paired,
      'questions':len(tasks),'fires':len({i for t in tasks for i in t.query.fire_ids}),
      'templates':len({t.template_id for t in tasks}),'category_counts':dict(Counter(t.category for t in tasks)),
      'metadata_paired_contrast':'All mock conditions must match task-level scientific outcomes; zero differences are an isolation result, not an efficacy estimate.',
      'real_model_evidence':'pending','tokens_and_provider_cost':None}


def report(output,summary):
    text=['# Milestone 3 expanded synthetic run','','**'+summary.get('evidence_label','MOCKED agent evidence; WORKING deterministic benchmark. Real-model evidence pending.')+'**','',
      f"{summary['questions']} questions across {summary['templates']} templates; no power calculation or ecological validation.",'',
      '| Provider / view / metadata | Correct | Appropriate abstention | Incorrect abstention | Incorrect answer | Failure |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for key,g in summary['groups'].items():
        s=g['status'];text.append('| '+key+' | '+' | '.join(str(s.get(k,0)) for k in ('correct','appropriate_abstention','incorrect_abstention','incorrect_answer','execution_failure'))+' |')
    text+=['','## Optimized direct rivals','','Timings are median local resident-interface nanoseconds, include Python validation/cache key and worker IPC where used. Warm is exact-query cache. R0 scalar allocation uses a targeted integral, not all upstream traits.','',
      '| Operation | R0 cold / warm | R1 cold / warm | R2 cold / warm |','| --- | ---: | ---: | ---: |']
    for row in summary['direct_comparisons']:
        cells=[]
        for r in ('R0','R1','R2'):
            c=row[r];cells.append('unavailable' if c['median_cold_ns'] is None else f"{c['median_cold_ns']:.0f} / {c['median_warm_ns']:.0f}")
        text.append('| '+row['operation']+' | '+' | '.join(cells)+' |')
    text+=['','Scientific correctness, receipt provenance, first-operation/argument selection, temporal/normalization/compression errors, sufficiency, routing, usage and task-specific valid-cost frontier are separate episode fields. Unknown usage/cost remains null.','',
      'The rule router uses public goal phrases and general operation preconditions plus measured timing inputs, never reference answers or task IDs. Its construction labor is unmeasured. Mock/rule results establish protocol behavior only. Cost calibration is visible in every metadata arm and carries no values, success flags or ideal-view labels.','',
      'Counterfactual costs include amortization of measured preparation and routing for repeated identical queries. Cached R0 is a strong rival. No universal speedup or adaptive advantage is assumed. Full traces retain failures, malformed responses and recovery. Synthetic semantic rubrics remain draft evidence-scope checks, not expert gold.']
    (Path(output)/'report.md').write_text('\n'.join(text)+'\n')


def check_access(target):
    check={'checked_at':datetime.now(timezone.utc).isoformat(),'real_model_calls':0,'external_model_costs_incurred':False,
      'credential_presence_only':{k:bool(os.environ.get(k)) for k in ('OPENAI_API_KEY','VERDE_LLM_API_KEY','VERDE_LLM_BASE_URL')},
      'access_authorization_verified':False,'cost_authorization_verified':False,'smoke_status':'pending'}
    try:
        from ..openclaw_backend import OpenClawBackend
        b=OpenClawBackend();check.update(saved_runtime_policy_valid=True,declared_provider=b.provider,declared_model=b.model,declared_runtime_version=b.runtime['openclaw_version'])
        from urllib.parse import urlsplit
        url=urlsplit(b.endpoint)
        try:
            with socket.create_connection((url.hostname,url.port),timeout=2):check['gateway_tcp']='reachable; not an inference identity check'
        except (OSError,TimeoutError) as exc:check['gateway_tcp']='not reachable from session: '+type(exc).__name__
    except (OSError,ValueError,KeyError) as exc:check.update(saved_runtime_policy_valid=False,policy_check_error=type(exc).__name__)
    dump(target,check);return check


def main():
    p=argparse.ArgumentParser();p.add_argument('--fixture',default='data/fixtures/embedding_utility/milestone-3-v3')
    p.add_argument('--output');p.add_argument('--upstream',default='../fire_vase');p.add_argument('--upstream-python',default='../fire_vase/.venv/bin/python')
    p.add_argument('--split',choices=['development','evaluation'],default='evaluation');p.add_argument('--repetitions',type=int,default=2)
    p.add_argument('--live-config');p.add_argument('--check-access');args=p.parse_args()
    if args.check_access:print(json.dumps(check_access(args.check_access)));return
    if not args.output:p.error('--output required')
    if not 1<=args.repetitions<=3:p.error('repetitions must be 1..3')
    result=run(Path.cwd(),args.fixture,args.output,args.upstream,args.upstream_python,split=args.split,repetitions=args.repetitions,live_config=json.loads(Path(args.live_config).read_text()) if args.live_config else None)
    print(json.dumps({k:result[k] for k in ('status','distinct_cells','episodes','real_model_calls','deterministic_digest')}))

if __name__=='__main__':main()
