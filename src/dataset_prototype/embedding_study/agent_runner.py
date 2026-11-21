"""Frozen fixed/adaptive synthetic episodes, provider isolation and independent replay."""
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
import platform
from pathlib import Path
import random
import subprocess
import sys
from time import perf_counter_ns
from ..contracts import digest
from .backend import UpstreamBackend
from .agent_contracts import AgentConfig, AgentAction
from .agent_controller import run_episode
from .agent_environment import load_environment, Dispatcher
from .agent_evaluation import score_episode
from .agent_render import render_initial, TOOLS, CONTRACTS
from .agent_providers import MockProvider, RuleProvider, OpenClawProvider
from .agent_report import build_report
from .reference import ReferenceAnswers


def write_json(path,value):
    path.write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n')


def run_experiment(config_path,output,*,upstream,upstream_python,root=None,provider_override=None):
    root=Path(root or Path.cwd()).resolve();config_path=Path(config_path).resolve();output=Path(output).resolve()
    cfg=AgentConfig.model_validate_json(config_path.read_text())
    if cfg.phase=='held_out_pending':raise ValueError('held-out events/templates not yet supplied; cannot claim evaluation')
    if cfg.provider=='openclaw' and not cfg.live_access_authorized:
        raise ValueError('live-model testing pending verified runtime and explicit cost/access authorization')
    output.mkdir(parents=True,exist_ok=False)
    manifest={'version':'fire-agent-run-v1','status':'incomplete','created_at':datetime.now(timezone.utc).isoformat(),
        'config':cfg.model_dump(mode='json'),'config_hash':digest(cfg),'simulated':cfg.provider=='mock',
        'real_model_calls':0,'provider_calls':0,'scientific_scope':'synthetic selection/abstention experiment only',
        'upstream_commit':'2e20e15a42610f77cdd0583bb5a43fcc6f6c8959','cache_policy':cfg.cache_policy,
        'python':sys.version,'platform':platform.platform(),'repository_commit':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
        'repository_dirty':bool(subprocess.check_output(['git','-C',str(root),'status','--porcelain'],text=True)),
        'real_model_evidence':'pending; mock results cannot establish H1-H4',
        'response_scope':'provider-scoped; normalized plugin JSON is not raw model text',
        'source_authority':'model proposals are inert data; deterministic fixture controller executes only reviewed synthetic operations',
        'historical_results':'milestone-1 files read-only; all new outputs in this distinct directory'}
    write_json(output/'manifest.json',manifest)
    rows=[];baselines=[];protocols={};provider_calls=0
    try:
        conditions=json.loads((root/cfg.metadata).read_text())
        from .metadata import validate_conditions
        validate_conditions(conditions)
        provider=provider_override or (MockProvider() if cfg.provider=='mock' else OpenClawProvider(authorized=True))
        if provider.model!=cfg.model:raise ValueError('configured model identity mismatch; no substitutions')
        manifest['provider']={'name':provider.name,'model':provider.model,'simulated':provider.simulated}
        manifest['code_sha256']={str(p.relative_to(root/'src/dataset_prototype')):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [*sorted((root/'src/dataset_prototype/embedding_study').glob('*.py')),
                *[root/'src/dataset_prototype'/n for n in ('contracts.py','openclaw_backend.py','openclaw_runtime.py','model_agents.py','network.py')]]}
        manifest['input_sha256']={str(p.relative_to(root)) if p.is_relative_to(root) else 'external_config/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (config_path,root/cfg.fixture,root/cfg.tasks,root/cfg.metadata)}
        write_json(output/'action_schema.json',AgentAction.model_json_schema())
        write_json(output/'frozen_config.json',cfg.model_dump(mode='json'))
        write_json(output/'metadata_conditions.json',conditions)
        preparation_start=perf_counter_ns()
        with UpstreamBackend(upstream,upstream_python) as backend:
            dataset,tasks,stores,aliases,reverse,old=load_environment(root,cfg.snapshot,cfg.fixture,cfg.tasks,backend)
            references=ReferenceAnswers(dataset,len(stores['R2'].artifact.components))
            histories={h.fire_id:h for h in dataset.histories}
            manifest.update(backend_versions=backend.versions,artifact_digest=stores['R2'].artifact.artifact_digest,
                inherited_preparation='milestone-1 preparation.json, including fit/materialization; reused artifacts are not free',
                upstream_source_sha256=stores['R2'].artifact.upstream_sha256,
                input_preparation_ns=perf_counter_ns()-preparation_start,
                question_set_version=tasks.version,fixture_version=dataset.version,
                metadata_version='metadata-view-v1',operation_registry_version='fire-agent-operations-v1',
                operation_registry_hash=digest(TOOLS),evaluation_version='fire-agent-evaluation-v1')
            task_list=list(tasks.tasks)
            if cfg.provider=='openclaw':
                if not cfg.smoke_task_indexes:raise ValueError('live smoke subset must be frozen before invocation')
                task_list=[task_list[i] for i in cfg.smoke_task_indexes]
            cells=[(t,(r,),m,'fixed_'+r) for t in task_list for r in cfg.fixed_representations for m in cfg.metadata_conditions]
            if cfg.adaptive:cells += [(t,('R0','R1','R2'),m,'adaptive') for t in task_list for m in cfg.metadata_conditions]
            manifest['distinct_cells']=len(cells);manifest['planned_episodes']=len(cells)*cfg.repetitions
            if cfg.provider=='mock' and (len(task_list)!=29 or len(cells)!=348):raise ValueError('complete mock matrix must retain 29 questions and 348 cells')
            manifest['schema_hash']=digest(AgentAction.model_json_schema())
            # Frozen protocol and prompts written before first model invocation.
            budgets={'max_steps':cfg.max_steps,'max_tool_calls':cfg.max_tool_calls,'seconds':cfg.max_episode_seconds}
            for t,allowed,m,label in cells:
                initial=render_initial(t,allowed,m,stores,aliases,conditions,budgets,prompt_version=cfg.prompt_version)
                key=t.task_id+':'+label+':'+m
                protocols[key]=initial
            write_json(output/'public_protocols.json',protocols)
            manifest['public_protocol_hash']=digest(protocols)
            write_json(output/'manifest.json',manifest)
            schedule=[(t,allowed,m,label,repeat) for t,allowed,m,label in cells for repeat in range(cfg.repetitions)]
            random.Random(cfg.seed).shuffle(schedule)
            def invoke(prompt,*,parameters):
                nonlocal provider_calls
                bound=min(cfg.max_provider_calls,cfg.max_real_calls) if not provider.simulated else cfg.max_provider_calls
                if provider_calls>=bound:raise RuntimeError('global_provider_call_budget_exhausted')
                provider_calls+=1
                return provider.invoke(prompt,parameters=parameters)
            with gzip.open(output/'episodes.jsonl.gz','xt') as episodes,gzip.open(output/'traces.jsonl.gz','xt') as traces:
                for t,allowed,m,label,repeat in schedule:
                    for s in stores.values():s.cache.clear()
                    dispatcher=Dispatcher(t,allowed,stores,aliases,reverse)
                    initial=protocols[t.task_id+':'+label+':'+m]
                    episode=run_episode(provider,initial,cfg,dispatcher,invoke=invoke)
                    grade=score_episode(t,allowed,episode,dispatcher,references.answer(t),histories)
                    row={'episode_id':f'C{len(rows):05d}','task_id':t.task_id,'condition':label,'metadata':m,'repeat':repeat,
                        'allowed_representations':list(allowed),'simulated':provider.simulated,'provider':provider.name,'model':provider.model,
                        'scientific_correct':grade['status']=='correct','appropriate_abstention':grade['status']=='correct_abstention',
                        'appropriate_abstention_when_insufficient':None if grade['authorized_answerable'] else grade['status']=='correct_abstention',
                        **grade,**episode['counts'],**episode['usage'],
                        'provider_invocations':episode['counts']['model_calls'],'model_calls':0 if provider.simulated else episode['counts']['model_calls'],
                        'termination':episode['termination'],'model_latency_ns':episode['model_latency_ns'],
                        'tool_latency_ns':episode['tool_latency_ns'],'total_elapsed_ns':episode['total_elapsed_ns'],
                        'usage_complete':episode['usage_complete'],'cache_policy':cfg.cache_policy,
                        'tool_cache_hits':sum(c['cache_hit'] for c in dispatcher.calls),
                        'logical_input_bytes':sum(c['logical_input_bytes'] for c in dispatcher.calls),
                        'worker_compute_ns':sum(c['worker_compute_ns'] for c in dispatcher.calls),
                        'worker_ipc_bytes':sum(c['worker_ipc_bytes'] for c in dispatcher.calls),
                        'prompt_initial_hash':digest(initial),'config_hash':digest(cfg)}
                    trace={'episode_id':row['episode_id'],'evaluator_only_task_id':t.task_id,
                        'steps':episode['steps'],'final':episode['final'],'private_dispatch_records':dispatcher.calls,
                        'termination':episode['termination'],'usage':episode['usage']}
                    rows.append(row);episodes.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n')
                    traces.write(json.dumps(trace,sort_keys=True,allow_nan=False)+'\n')
                    episodes.flush();traces.flush()
            # Same public questions and conditions; fixed baselines and router know
            # scientific contracts, never task IDs, reference keys or answerability.
            rule=RuleProvider()
            with gzip.open(output/'baselines.jsonl.gz','xt') as file:
                for t,allowed,m,label in cells:
                    for s in stores.values():s.cache.clear()
                    dispatcher=Dispatcher(t,allowed,stores,aliases,reverse)
                    episode=run_episode(rule,protocols[t.task_id+':'+label+':'+m],cfg,dispatcher)
                    grade=score_episode(t,allowed,episode,dispatcher,references.answer(t),histories)
                    row={'task_id':t.task_id,'condition':'rule_adaptive' if label=='adaptive' else 'rule_'+label,
                        'metadata':m,'repeat':0,**grade,'scientific_correct':grade['status']=='correct',
                        'appropriate_abstention':grade['status']=='correct_abstention',
                        'appropriate_abstention_when_insufficient':None if grade['authorized_answerable'] else grade['status']=='correct_abstention',**episode['counts'],**episode['usage'],
                        'provider_invocations':episode['counts']['model_calls'],'model_calls':0,'simulated':True,
                        'model_latency_ns':0,'tool_latency_ns':episode['tool_latency_ns'],'total_elapsed_ns':episode['total_elapsed_ns']}
                    baselines.append(row);file.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n')
            write_json(output/'preparation_accounting.json',{'this_run_preparation_ns':manifest['input_preparation_ns'],
                'inherited':json.loads((root/cfg.snapshot/'preparation.json').read_text()),
                'router_construction_labor':None,'router_maintenance_labor':None,
                'note':'historical preparation timings are retained context, not newly measured here; rule engineering effort unmeasured'})
        summary=build_report(output)
        manifest.update(status=('complete_with_failures' if any(r['termination']!='completed' for r in rows) else 'complete'),episodes=len(rows),baseline_episodes=len(baselines),
            provider_calls=provider_calls,real_model_calls=0 if provider.simulated else provider_calls,
            finished_at=datetime.now(timezone.utc).isoformat())
        # Runtime is expected to vary; deterministic choices/scores have a separate digest.
        keys=('task_id','condition','metadata','repeat','status','returned_answer','reference_answer','diagnostics',
              'operation_selection_correct','first_operation_selection_correct','selected_representation_sufficient','termination','provenance_complete',
              'tool_calls','invalid_tool_calls','unsupported_answer_attempts','recovery_attempts','model_calls')
        manifest['deterministic_results_digest']=digest(sorted([{k:r[k] for k in keys} for r in rows],key=lambda r:(r['task_id'],r['condition'],r['metadata'],r['repeat'])))
        manifest['output_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name!='manifest.json'}
    except BaseException as error:
        manifest.update(status='failed',error_type=type(error).__name__,provider_calls=provider_calls)
        raise
    finally:write_json(output/'manifest.json',manifest)
    return manifest,summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='reports/embedding_utility/fire_vase/config/agent-mock-frozen-v2.json')
    parser.add_argument('--output');parser.add_argument('--report');parser.add_argument('--upstream');parser.add_argument('--upstream-python')
    args=parser.parse_args()
    if args.report:build_report(args.report);print('Report regenerated without provider calls.');return
    if not args.output or not args.upstream or not args.upstream_python:parser.error('execution requires output and explicit pinned upstream installation')
    manifest,_=run_experiment(args.config,args.output,upstream=args.upstream,upstream_python=args.upstream_python)
    print(json.dumps({k:manifest[k] for k in ('status','distinct_cells','episodes','baseline_episodes','provider_calls','real_model_calls')}))


if __name__=='__main__':main()
