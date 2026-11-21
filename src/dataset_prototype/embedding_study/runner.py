"""Reproducible synthetic factorial benchmark, explicit preparation and cache costs."""
import argparse
from collections import Counter
import hashlib
import gzip
import json
from pathlib import Path
import platform
import random
import statistics
import sys
from time import perf_counter_ns
import tracemalloc
from ..contracts import digest
from .backend import UpstreamBackend
from .contracts import Dataset, TaskSet, BenchmarkConfig, PIN, CoordinateArtifact
from .evaluation import evaluate
from .metadata import metadata_views, OP_UNITS, REGISTRY
from .reference import ReferenceAnswers
from .representations import (RepresentationView, make_features, fit_artifact, coordinates,
    provenance, save_artifact, load_artifact, InvalidOperation)


def dump(path, obj):
    path.write_text(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n')


def measured(label, callback, backend=None, **notes):
    if tracemalloc.is_tracing():
        raise RuntimeError('nested memory measurement is unsupported')
    before_compute = backend.compute_ns if backend else 0
    before_ipc = backend.ipc_bytes if backend else 0
    tracemalloc.start(); started = perf_counter_ns()
    try:
        value = callback()
    finally:
        elapsed = perf_counter_ns()-started
        _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return value, {'phase':label,'runtime_ns':elapsed,'python_traced_peak_bytes':peak,
        'worker_compute_ns':backend.compute_ns-before_compute if backend else 0,
        'worker_ipc_bytes':backend.ipc_bytes-before_ipc if backend else 0,
        'file_read_bytes':0, **notes}


def run_benchmark(config_path, output, *, upstream, upstream_python, repository_root=None):
    run_started=perf_counter_ns()
    import numpy as np
    import pydantic
    root = Path(repository_root or Path.cwd()).resolve()
    config_path, output = Path(config_path).resolve(), Path(output).resolve()
    config = BenchmarkConfig.model_validate_json(config_path.read_text())
    output.mkdir(parents=True,exist_ok=False)
    manifest = {'format':'fire-vase-benchmark-run-v1','status':'incomplete','synthetic':True,
        'agent_calls':0,'network_reads':0,'real_data_evaluation':'pending rights/support/input contract review',
        'upstream_commit':PIN,'config':config.model_dump(mode='json'),'config_hash':digest(config),
        'python':sys.version,'platform':platform.platform(),'consumer_versions':{'numpy':np.__version__,'pydantic':pydantic.__version__},
        'cache_scope':'cold clears application query cache, not OS caches; warm prefill measured separately',
        'memory_scope':'parent Python traced allocations; worker cumulative process high-water RSS recorded separately',
        'read_scope':'file byte counts are serialized bytes read, not physical disk I/O; logical query payload and worker IPC bytes separate',
        'timing_scope':'wall-clock nanoseconds with per-query instrumentation; local synthetic workload, not throughput',
        'scientific_scope':'synthetic correctness and geometric fidelity only; no real wildfire findings',
        'nearest_profile_scope':'R2 backprojects frozen coordinates to original profile units before Euclidean distance; no clipping or probability claim',
        'metadata_scope':'evidence views recorded but deterministic operations do not interpret metadata; no metadata efficacy measured'}
    preparation=[]
    dump(output/'manifest.json',manifest)
    try:
        fixture_path, tasks_path, metadata_path = (root/getattr(config,n) for n in ('fixture','tasks','metadata'))
        dataset, phase = measured('load_observations',lambda:Dataset.model_validate_json(fixture_path.read_text()),
            file_read_bytes=fixture_path.stat().st_size,attribution=['R0','R1 preparation','R2 preparation'])
        preparation.append(phase)
        task_set = TaskSet.model_validate_json(tasks_path.read_text())
        conditions = json.loads(metadata_path.read_text())
        views,phase = measured('metadata_views',lambda:metadata_views(dataset,conditions),
            file_read_bytes=metadata_path.stat().st_size,attribution=['all conditions; evidence size varies'])
        preparation.append(phase)
        dump(output/'metadata_views.json',views)
        references,phase = measured('independent_reference_preparation',lambda:ReferenceAnswers(dataset,config.components),
            attribution=['evaluation only; excluded from system costs'])
        preparation.append(phase)
        ids = {h.fire_id for h in dataset.histories}
        evaluation_ids = {h.fire_id for h in dataset.histories if h.split=='evaluation'}
        for task in task_set.tasks:
            if not set((*task.fire_ids,*task.candidates)) <= evaluation_ids:
                raise ValueError('benchmark tasks must use declared evaluation fires only')
            available_ids={o.observation_id for h in dataset.histories if h.fire_id in (*task.fire_ids,*task.candidates) for o in h.observations}
            if set(task.required_observation_ids)!=available_ids:
                raise ValueError('task required-observation manifest differs from source histories')
            if task.unit != OP_UNITS[task.operation]:
                raise ValueError('task unit differs from fixed operation contract')
            if (references.answer(task) is not None) != task.answerable['R0']:
                raise ValueError('declared direct answerability differs from independent evidence')
        input_paths=[config_path,fixture_path,tasks_path,metadata_path]
        manifest['input_sha256']={(str(p.relative_to(root)) if p.is_relative_to(root) else 'external_config/'+p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}
        manifest['dataset_digest']=digest(dataset)
        manifest['training_ids']=[h.fire_id for h in dataset.histories if h.split=='train' and h.profile_eligible]
        manifest['evaluation_ids']=sorted(evaluation_ids)
        manifest['task_count']=len(task_set.tasks)
        manifest['registry_digest']=digest(REGISTRY)
        source_files=[*sorted((Path(__file__).parent).glob('*.py')),Path(__file__).parents[1]/'contracts.py']
        manifest['code_sha256']={str(p.relative_to(Path(__file__).parents[1])):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
        backend_started=perf_counter_ns()
        with UpstreamBackend(upstream,upstream_python) as backend:
            manifest['backend_versions']=backend.versions
            manifest['upstream_checkout_clean']=not bool(backend.checkout_status)
            preparation.append({'phase':'worker_startup_and_import','runtime_ns':perf_counter_ns()-backend_started,
                'file_read_bytes':None,'python_traced_peak_bytes':None,'attribution':['all upstream operations; once per run']})
            feature_payloads,phase = measured('compute_vase_features',lambda:{h.fire_id:make_features(h,backend) for h in dataset.histories},backend,
                attribution=['R1 preparation','R2 preparation; training and evaluation features, fit only training'])
            preparation.append(phase)
            artifact,phase = measured('fit_training_only_pca',lambda:fit_artifact(dataset,feature_payloads,backend,config.components),backend,
                attribution=['R2 preparation','R0/R1 only when requesting PCA geometry'])
            preparation.append(phase)
            _,phase=measured('write_pca_artifact',lambda:save_artifact(artifact,output/'pca_artifact.json'),attribution=['PCA publication'])
            preparation.append(phase)
            artifact,phase=measured('load_pca_artifact',lambda:load_artifact(output/'pca_artifact.json',dataset),
                file_read_bytes=(output/'pca_artifact.json').stat().st_size,attribution=['PCA consumers'])
            preparation.append(phase)
            coordinate_payloads,phase=measured('compute_pca_coordinates',lambda:{i:coordinates(f['profile'],artifact) if f else None for i,f in feature_payloads.items()},
                attribution=['R2 preparation'])
            preparation.append(phase)
            _,phase=measured('publish_feature_artifact',lambda:dump(output/'features.json',feature_payloads),attribution=['R1/R2 artifact publication'])
            preparation.append(phase)
            coordinate_doc=CoordinateArtifact(version='fire-vase-coordinates-v1',artifact_digest=artifact.artifact_digest,
                dataset_digest=digest(dataset),dimensions=len(artifact.components),coordinates=coordinate_payloads).model_dump(mode='json')
            _,phase=measured('publish_coordinate_artifact',lambda:dump(output/'coordinates.json',coordinate_doc),attribution=['R2 artifact publication'])
            preparation.append(phase)
            coordinate_file_sha=hashlib.sha256((output/'coordinates.json').read_bytes()).hexdigest()
            def load_coordinates():
                path=output/'coordinates.json'
                data=path.read_bytes()
                if hashlib.sha256(data).hexdigest()!=coordinate_file_sha:
                    raise ValueError('coordinate file integrity failure')
                values=CoordinateArtifact.model_validate_json(data).model_dump(mode='json')
                if values['artifact_digest']!=artifact.artifact_digest or values['dataset_digest']!=digest(dataset) or set(values['coordinates'])!=ids or values['dimensions']!=len(artifact.components):
                    raise ValueError('coordinate scientific identity mismatch')
                return values['coordinates']
            coordinate_payloads,phase=measured('load_existing_pca_coordinates',load_coordinates,
                file_read_bytes=(output/'coordinates.json').stat().st_size,attribution=['R2 ready-artifact use; preceding preparation is not free'])
            preparation.append(phase)
            manifest['artifact_digest']=artifact.artifact_digest
            lineages={h.fire_id:provenance(h) for h in dataset.histories}
            data={'R0':{h.fire_id:h for h in dataset.histories},'R1':feature_payloads,'R2':coordinate_payloads}
            stores={r:RepresentationView(r,payloads,lineages,backend,artifact) for r,payloads in data.items()}
            schedule=[(task,r,m,mode) for task in task_set.tasks for r in stores for m in views for mode in config.query_cache_modes]
            random.Random(config.order_seed).shuffle(schedule)
            records=[]
            with gzip.open(output/'results.jsonl.gz','xt') as file:
                for task,r,m,mode in schedule:
                    store=stores[r];store.cache.clear()
                    reference=references.answer(task)
                    # Warm every cell equally; no M0-first/M2-later cache advantage.
                    if mode=='warm':
                        _,phase=measured('warmup_query',lambda:store.query(task),backend,
                            task_id=task.task_id,representation=r,metadata=m,attribution=['warm cache preparation'])
                        preparation.append(phase)
                    for repeat in range(config.repeats):
                        if mode=='cold':
                            store.cache.clear()
                        def query():
                            try:
                                if task.unit!=OP_UNITS[task.operation]:
                                    raise InvalidOperation('operation/answer unit mismatch')
                                return store.query(task),None
                            except Exception as exc:
                                failure={'answer':None,'abstention':False,'unit':task.unit,
                                    'approximate':False,'reason':str(exc)}
                                return failure,(type(exc).__name__,str(exc))
                        (result,error),cost=measured('query',query,backend)
                        score=evaluate(task,r,result,reference,execution_error=error)
                        used_ids=tuple(dict.fromkeys((*task.fire_ids,*task.candidates)))
                        evidence={i:lineages[i] for i in used_ids}
                        complete=all(all(k in evidence[i] for k in task.expected_provenance) for i in evidence)
                        row={'task_id':task.task_id,'family':task.family,'representation':r,'metadata_condition':m,
                            'cache_mode':mode,'repeat':repeat,'operation':task.operation,'required_observation_ids':list(task.required_observation_ids),'execution_status':'failure' if error else 'abstained' if result['abstention'] else 'executed',
                            'returned_answer':result['answer'],'reference_answer':reference,'unit':task.unit,
                            'abstention':result['abstention'],'reason':result['reason'],'approximate':result['approximate'],
                            'evidence_kind':task.evidence_kind,**score,'provenance_complete':complete,'provenance':evidence,
                            'artifact_digest':artifact.artifact_digest if r=='R2' or task.operation=='pca_distance' else None,
                            'source_version':dataset.version,'upstream_commit':PIN,'config_hash':digest(config),
                            'metadata_digest':digest(views[m]),'cache_hit':store.last_cache_hit,
                            'logical_input_bytes':store.last_logical_bytes,'worker_cumulative_peak_rss_bytes':backend.peak_rss_bytes,
                            'error':error,**{k:v for k,v in cost.items() if k!='phase'}}
                        records.append(row);file.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n');file.flush()
            summary=make_summary(records)
            manifest['status']='complete' if not any(r['execution_status']=='failure' for r in records) else 'complete_with_failures'
            manifest['records']=len(records)
            manifest['worker_total_calls']=backend.calls
            dump(output/'summary.json',summary)
            dump(output/'preparation.json',preparation)
            (output/'report.md').write_text(report(summary,preparation))
        manifest['deterministic_results_digest']=digest(sorted([{k:r[k] for k in ('task_id','family','representation','metadata_condition','cache_mode','repeat','returned_answer','reference_answer','status','scientific_validity','answerable','abstention','provenance','artifact_digest')} for r in records],key=lambda r:(r['task_id'],r['representation'],r['metadata_condition'],r['cache_mode'],r['repeat'])))
        manifest['end_to_end_runtime_ns']=perf_counter_ns()-run_started
        manifest['end_to_end_scope']='run_benchmark function wall time including evaluation, telemetry and publication; interpreter/module startup excluded'
        manifest['output_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name!='manifest.json'}
    except BaseException as exc:
        manifest.update(status='failed',error_type=type(exc).__name__,error=str(exc))
        dump(output/'preparation.json',preparation)
        raise
    finally:
        dump(output/'manifest.json',manifest)
    return manifest,summary


def make_summary(records):
    summary={'status_counts':dict(Counter(r['status'] for r in records)), 'representations':{},'metadata_invariance':True,'task_costs':{}}
    for r in ('R0','R1','R2'):
        rows=[x for x in records if x['representation']==r]
        sufficient=[x for x in rows if x['answerable']]
        summary['representations'][r]={'statuses':dict(Counter(x['status'] for x in rows)),
            'answerable_attempts':len(sufficient),'answerable_correct':sum(x['status']=='correct' for x in sufficient),
            'cold_query_median_ns':statistics.median(x['runtime_ns'] for x in rows if x['cache_mode']=='cold' and x['runtime_ns'] is not None),
            'warm_query_median_ns':statistics.median(x['runtime_ns'] for x in rows if x['cache_mode']=='warm' and x['runtime_ns'] is not None)}
    for task_id in sorted({r['task_id'] for r in records}):
        summary['task_costs'][task_id]={}
        for representation in ('R0','R1','R2'):
            for mode in ('cold','warm'):
                successful=[r for r in records if r['task_id']==task_id and r['representation']==representation
                    and r['cache_mode']==mode and r['status']=='correct' and r['runtime_ns'] is not None]
                if successful:
                    summary['task_costs'][task_id][representation+'_'+mode]={
                        'median_ns':statistics.median(r['runtime_ns'] for r in successful),
                        'attempts':len(successful),'scope':'correct answerable queries only; local instrumentation included'}
    cells={}
    for row in records:
        key=(row['task_id'],row['representation'],row['cache_mode'],row['repeat'])
        value=digest({k:row[k] for k in ('returned_answer','status','answerable','scientific_validity','abstention')})
        if key in cells and cells[key]!=value:
            summary['metadata_invariance']=False
        cells[key]=value
    return summary


def report(summary, preparation):
    text=['# Fire VASE deterministic synthetic benchmark','','Synthetic mechanics only. No agent calls, observed wildfire findings, independent scientific analog labels or metadata-effect estimates.','',
        '| Representation | Answerable correct / attempts | Correct abstentions | Cold query median (µs) | Warm query median (µs) |',
        '| --- | --- | --- | --- | --- |']
    for r,s in summary['representations'].items():
        text.append(f"| {r} | {s['answerable_correct']} / {s['answerable_attempts']} | {s['statuses'].get('correct_abstention',0)} | {s['cold_query_median_ns']/1000:.2f} | {s['warm_query_median_ns']/1000:.2f} |")
    text += ['', 'Counts include metadata/cache/repeat cells, not independent scientific samples. All-task coverage and accuracy conditional on answerability must be read separately.',
        '',f"Metadata answer invariance: {summary['metadata_invariance']}. Views are recorded, not interpreted by this deterministic consumer.",
        '', 'Cold means application query-cache cold; materialized R1/R2 artifacts are resident. OS caches are uncontrolled. Warm prefill costs are retained in preparation.json. Timings include Python instrumentation and worker IPC when used.',
        '', 'Preparation (not free or folded silently into per-query latency):','', '| Phase | Wall time (ms) |', '| --- | --- |']
    for p in preparation:
        if p['phase']!='warmup_query':
            text.append(f"| {p['phase']} | {p['runtime_ns']/1e6:.3f} |")
    text += ['', 'Example of matched correct queries: first-half allocation fraction. R0 on-demand feature calls include worker IPC; R1 resident lookup does not, so the difference is not pure algorithm time.','', '| Interface | Cold median (µs) | Warm median (µs) |', '| --- | --- | --- |']
    for r in ('R0','R1'):
        timing=summary['task_costs'].get('front-fraction',{}).get(r+'_cold')
        if timing:
            warm=summary['task_costs']['front-fraction'][r+'_warm']
            text.append(f"| {r} | {timing['median_ns']/1000:.2f} | {warm['median_ns']/1000:.2f} |")
    text += ['', 'No universal cost winner or empirical break-even is claimed: supported tasks differ and this tiny local run includes preparation shared by several interfaces. Compare measured task-specific cumulative costs at equal correctness, including warmup, artifact refresh and direct caching.',
        '', 'Direct data retain area/date information; normalized profiles intentionally discard those values; truncated PCA cannot exactly invert the profile. Exact compressed-only queries abstain. Neighbor outputs are explicitly approximate geometric diagnostics. Scientific analog evidence remains pending.',
        '', 'Real-data contract validation remains pending selected-input rights/support and availability review. No archive was downloaded or ingested. Numerical outputs/config/artifact identities reproduce; runtime/memory and serialized output hashes vary by environment.','']
    return '\n'.join(text)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='reports/embedding_utility/fire_vase/config/benchmark.json')
    parser.add_argument('--output',required=True)
    parser.add_argument('--upstream',required=True)
    parser.add_argument('--upstream-python',required=True)
    args=parser.parse_args()
    manifest,_=run_benchmark(args.config,args.output,upstream=args.upstream,upstream_python=args.upstream_python)
    print(json.dumps({'status':manifest['status'],'records':manifest['records'],'output':args.output}))


if __name__=='__main__':
    main()
