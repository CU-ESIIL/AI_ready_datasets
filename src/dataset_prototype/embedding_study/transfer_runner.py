"""Synthetic cross-task transfer; source encoder immutable; no agent execution."""
import argparse
from collections import defaultdict
from datetime import datetime,timezone
import gzip
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns,process_time_ns
import numpy as np
from ..contracts import digest
from .learned_training_contracts import TrainingConfig
from .learned_data import generate,PrefixPreprocessor,interpretable
from .learned_models import load_checkpoint as load_original,state_digest,parameter_count
from .learned_experiment import normalized_tensor,timed,dump
from .transfer_contracts import TransferConfig,TASKS,DEFINITIONS
from .transfer_targets import future_targets,property_targets,PROPERTY_NAMES
from .transfer_models import train,forward,loss_grad,LinearHead,sigmoid,load_checkpoint
from .transfer_evaluation import score,paired_fire_delta,retrieval,regression_radius,standardize


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_rows(path,rows):
    with gzip.open(path,'wt') as f:
        for row in rows:f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n')


def source(config):
    root=Path(config.source_snapshot).resolve();manifest=json.loads((root/'manifest.json').read_text())
    for name,expected in manifest['output_sha256'].items():
        if sha(root/name)!=expected:raise ValueError('frozen M4 artifact changed: '+name)
    cfg=TrainingConfig.model_validate_json((root/'frozen_config.json').read_text());histories,records=generate(cfg)
    if digest(histories)!=manifest['source_digest']:raise ValueError('frozen cohort changed')
    if digest([r['prefix'].model_dump(mode='json') for r in records])!=manifest['prefix_input_provenance_digest']:raise ValueError('frozen prefix support/availability lineage changed')
    pre=PrefixPreprocessor().fit([r['prefix'] for r in records if r['split']=='train'])
    if pre.state()!=json.loads((root/'preprocessing.json').read_text()):raise ValueError('frozen preprocessing changed')
    model=json.loads((root/'model_states.json').read_text())['tcn'];params=load_original(root/model['checkpoint'],'tcn')
    if state_digest(params)!=model['parameter_digest']:raise ValueError('frozen encoder changed')
    return root,manifest,histories,records,pre,params


def fit_group(name,x,y,selection,config,output,kind='tcn',binary=()):
    mean=y['train'].mean(0);scale=y['train'].std(0);scale[scale<1e-8]=1
    for j in binary:mean[j]=0.;scale[j]=1.
    normalized={s:(v-mean)/scale for s,v in y.items()};runs=[]
    for seed in config.seeds:
        start=perf_counter_ns();cpu=process_time_ns();p,curve=train(x['train'],normalized['train'],kind,seed,config.epochs,config.learning_rate,binary)
        wall=perf_counter_ns()-start;cpu=process_time_ns()-cpu
        validation=loss_grad(p,x['validation'][selection],normalized['validation'][selection],kind,binary,l2=0)[0]
        path=output/(name+f'-seed-{seed}.npz');np.savez(path,**p)
        if state_digest(load_checkpoint(path,kind,y['train'].shape[1]))!=state_digest(p):raise ValueError('checkpoint roundtrip')
        record={'group':name,'kind':kind,'seed':seed,'parameters':parameter_count(p),'training_targets':name,
          'validation_selection_loss':validation,'wall_training_ns':wall,'cpu_training_ns':cpu,'loss_curve':curve,
          'checkpoint':path.name,'checkpoint_sha256':sha(path),'parameter_digest':state_digest(p)}
        runs.append((validation,seed,p,record))
    best=min(runs,key=lambda a:(a[0],a[1]))
    return best[2],{'mean':mean.tolist(),'scale':scale.tolist(),'binary_columns':list(binary),'selected_seed_by_validation':best[1],
      'selected_checkpoint':best[3]['checkpoint'],'selected_digest':state_digest(best[2]),'runs':[a[3] for a in runs],
      'all_seeds_training_ns':sum(a[3]['wall_training_ns'] for a in runs)}


def diagnostic_probes(features,prefixes,output):
    targets={s:property_targets(p) for s,p in prefixes.items()};results={}
    for name,views in features.items():
        tr,te=views['train'],views['test'];linear=[];nonlinear=[]
        # Fixed RBF kernel with train-only scales and bandwidth, no future targets.
        a=standardize(tr,tr);b=standardize(tr,te);dimension=max(1,a.shape[1])
        distance=lambda q,z:np.maximum(0,np.sum(q*q,1)[:,None]+np.sum(z*z,1)[None,:]-2*q@z.T)
        kernel=np.exp(-distance(a,a)/dimension);cross=np.exp(-distance(b,a)/dimension)
        center=targets['train'].mean(0);coef=np.linalg.solve(kernel+np.eye(len(a)),targets['train']-center)
        nonlinear_pred=cross@coef+center
        for j,prop in enumerate(PROPERTY_NAMES):
            model=LinearHead().fit(tr,targets['train'][:,j]);prediction=model.predict(te)
            variance=float(np.var(targets['test'][:,j]));l=float(np.mean((prediction-targets['test'][:,j])**2));n=float(np.mean((nonlinear_pred[:,j]-targets['test'][:,j])**2))
            linear.append({'property':prop,'mse':l,'r2_descriptive':1-l/variance if variance>0 else None})
            nonlinear.append({'property':prop,'mse':n,'r2_descriptive':1-n/variance if variance>0 else None})
        results[name]={'linear':linear,'nonlinear_rbf':nonlinear,'nonlinear_training_coefficients_per_property':len(a),
          'scope':'Past-input property recoverability only; larger nonlinear probe capacity; failed linear recovery is not proof of information absence; prediction is not exactness'}
    dump(output/'information_probes.json',{'views':results,'completeness':'constant true among validated consecutive prefixes; invalid schedules rejected by source contract, not claimed learned competence',
      'exact_information':'Raw tensor is mathematically invertible for supplied growth/masks within floating precision. Summary/PCA/learned probes are not exact-invertibility proofs.',
      'pulse_definition':'strict interior local maxima count; deliberately distinct from upstream padded 20%-prominence pulses'})
    return results


def control_diagnostics(prefixes,pre,featurizers,heads,output,features,retrieval_reference):
    rows=[];retrieval_rows=[]
    for prefix_index,prefix in enumerate(prefixes):
        base={name:features([prefix]) for name,features in featurizers.items()}
        g=np.asarray(prefix.growth_km2_day)
        variants={'temporal_permutation':g[np.random.default_rng(451).permutation(len(g))],
          'fourfold_scale':4*g,'equal_total_reversal':g[::-1]}
        for kind,values in variants.items():
            p=prefix.model_copy(update={'growth_km2_day':tuple(float(v) for v in values)})
            for name,make in featurizers.items():
                f=make([p]);before=base[name]
                train_view=features[name]['train'];test_view=standardize(train_view,features[name]['test'])
                query_view=standardize(train_view,f)[0]
                candidates=np.array([j for j,q in enumerate(prefixes) if q.fire_id!=prefix.fire_id])
                d=np.sum((test_view[candidates]-query_view)**2,axis=1)
                chosen=set(candidates[np.argsort(d,kind='stable')[:10]])
                original=retrieval_reference[name]['representation_distance']['rows'][prefix_index]
                relevant=set(original['relevant_indices'])
                retrieval_rows.append({'fire_id':prefix.fire_id,'depth':len(g),'control':kind,'view':name,
                    'precision_at_10_fixed_future':len(chosen&relevant)/10,
                    'precision_change_fixed_future':len(chosen&relevant)/10-original['precision_at_k'],
                    'neighbor_overlap_with_unperturbed':len(chosen&set(original['selected_indices']))/10,
                    'scope':'query-only observed-prefix perturbation, fixed unmodified gallery/future relevance; diagnostic not ecological counterfactual'})
                for task in TASKS:
                    model=heads[name][task];change=float(model.predict(f)[0]-model.predict(before)[0])
                    rows.append({'fire_id':prefix.fire_id,'depth':len(g),'control':kind,'view':name,'task':task,
                      'prediction_change':change,'representation_l2_change':float(np.linalg.norm(f-before)),
                      'base_prefix_digest':digest(prefix),'derived_prefix_digest':digest(p)})
        relabeled=prefix.model_copy(update={'fire_id':'nominal-renamed','source_observation_ids':tuple('N'+str(i) for i in range(len(g)))})
        for name,make in featurizers.items():
            if not np.array_equal(base[name],make([relabeled])):raise ValueError('nominal-ID invariance failed')
        from .learned_contracts import PrefixInput
        packet=prefix.model_dump(mode='json')
        for key in ('dates','available_at','source_observation_ids','growth_km2_day'):packet[key].pop(1)
        try:PrefixInput.model_validate(packet)
        except ValueError:pass
        else:raise ValueError('observation-removal support violation')
        packet=prefix.model_dump(mode='json');from datetime import timedelta
        packet['dates']=[str(prefix.dates[0]+timedelta(days=2*i)) for i in range(len(g))]
        try:PrefixInput.model_validate(packet)
        except ValueError:pass
        else:raise ValueError('resolution support violation')
    write_rows(output/'perturbations.jsonl.gz',rows)
    write_rows(output/'retrieval_perturbations.jsonl.gz',retrieval_rows)
    summary=[]
    for name in featurizers:
        for task in TASKS:
            for kind in variants:
                subset=[r for r in rows if r['view']==name and r['task']==task and r['control']==kind]
                summary.append({'view':name,'task':task,'control':kind,'n':len(subset),'median_absolute_prediction_change':float(np.median([abs(r['prediction_change']) for r in subset]))})
    dump(output/'perturbation_summary.json',{'rows':summary,'nominal_ID':'exactly invariant for all views/tasks/prefixes','missing_or_resolution_change':'all rejected; support abstention, not accuracy robustness',
      'expected':'Scale A/B/D should respond if prefix and future are jointly scaled; C label is invariant under joint scaling. Permutation/reversal are sensitivity tests, not required invariance or ecological counterfactuals. No transformed future labels are used as observed ecological evidence.',
      'retrieval':'Distances use the same perturbed representations; E future relevance itself is unchanged only for nominal IDs. No universal scale/order rank invariance is imposed.'})


def reuse_costs(prefix,pre,features,featurizers,heads,params,training,output):
    # Featurizers include the same fitted preprocessing/encoders used for scoring.
    results={};material_store={};counts=(1,2,3,4)
    for name,make in featurizers.items():
        start=perf_counter_ns();material_store[name]=make(features['prefixes_test']);construction=perf_counter_ns()-start
        path=output/(name+'-materialized.npz');start=perf_counter_ns();np.savez(path,vectors=material_store[name]);write=perf_counter_ns()-start
        start=perf_counter_ns()
        with np.load(path,allow_pickle=False) as f:stored=f['vectors'].copy()
        read=perf_counter_ns()-start
        if not np.allclose(stored,material_store[name],rtol=0,atol=0):raise ValueError('materialized representation changed')
        _,encode=timed(lambda:make([prefix]));taskrows=[]
        for k in counts:
            tasks=TASKS[:k]
            def demand():
                vector=make([prefix]);return [float(heads[name][t].predict(vector)[0]) for t in tasks]
            vector=stored[:1]
            def lookup():return [float(heads[name][t].predict(vector)[0]) for t in tasks]
            a,cold=timed(demand);b,warm=timed(lookup)
            if not np.allclose(a,b,rtol=0,atol=1e-10):raise ValueError('heterogeneous materialization altered output')
            cache=dict(zip(tasks,b));_,cached=timed(lambda:[cache[t] for t in tasks])
            prep=(construction+write+read)/len(stored);saving=cold['median_ns']-warm['median_ns']
            taskrows.append({'tasks':list(tasks),'on_demand_shared_encoding_plus_heads_ns':cold['median_ns'],
              'materialized_heads_ns':warm['median_ns'],'cached_prediction_bundle_ns':cached['median_ns'],
              'per_prefix_preparation_ns':prep,'break_even_bundle_queries_excluding_shared_training':float(np.ceil(prep/saving)) if saving>0 else None,
              'counterfactual_reuse':[{ 'bundles':q,'on_demand_ns':q*cold['median_ns'],
                'materialized_ns':prep+q*warm['median_ns'],'complete_prediction_cache_ns':cold['median_ns']+(q-1)*cached['median_ns']} for q in (1,10,100,1000)]})
        results[name]={'construction_ns':construction,'write_ns':write,'read_ns':read,'storage_bytes':path.stat().st_size,
          'coordinate_bytes':stored.nbytes,'encoding_one_prefix':encode,'bundles':taskrows}
    # Separate task encoders cannot share encoding across task objectives.
    by_task=features['specific_featurizers'];specific=[]
    for k in counts:
        tasks=TASKS[:k]
        def call():return [float(heads['specific_'+t][t].predict(by_task[t]([prefix]))[0]) for t in tasks]
        _,cost=timed(call);specific.append({'tasks':list(tasks),'separate_encoders_plus_heads_ns':cost['median_ns']})
    dump(output/'reuse_economics.json',{'views':results,'task_specific_encoders':specific,
      'training_costs':{k:v['all_seeds_training_ns'] for k,v in training.items()},
      'training_semantics':'Current training and historical A-encoder acquisition separately recorded. Do not cancel training when comparing different representation strategies from scratch.',
      'cache_identity':{'prefix_digest':digest(prefix),'preprocessing_digest':digest(pre.state()),'encoder_digests':{k:state_digest(v) for k,v in params.items()},'head_digest':digest({n:{t:m.state() for t,m in h.items()} for n,h in heads.items()})},
      'refresh':'Source/recipe/preprocessing/encoder changes invalidate affected vectors and predictions; head changes invalidate cached predictions. Counts/frequency/maintenance labor unmeasured.',
      'scope':'Local warm scalar bundles with validated immutable query keys. Same heads in on-demand/materialized modes. Bundles reuse encoding across distinct A-D heads; identical-bundle caching is a different mechanism. File bytes exclude full source/rights lineage and are not full lifecycle storage.'})
    return results


def run(config,output):
    config=TransferConfig.model_validate(config);output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    dump(output/'frozen_config.json',config.model_dump(mode='json'));dump(output/'task_definitions.json',DEFINITIONS)
    root,original,histories,records,pre,frozen=source(config);frozen_digest=state_digest(frozen)
    dump(output/'source_identity.json',{'source_manifest_sha256':sha(root/'manifest.json'),'source_digest':original['source_digest'],
      'frozen_A_digest':frozen_digest,'frozen_A_checkpoint':json.loads((root/'model_states.json').read_text())['tcn']['checkpoint'],
      'prior_test_exposure':'M4 cohort already evaluated on A; B-E tasks/protocol new, not a new independent hidden cohort',
      'preprocessing':pre.state()})
    history={h['fire_id']:h for h in histories};split={s:[r for r in records if r['split']==s] for s in ('train','validation','test')}
    prefixes={s:[r['prefix'] for r in rows] for s,rows in split.items()};ids={s:[p.fire_id for p in values] for s,values in prefixes.items()}
    write_rows(output/'source_prefix_lineage.jsonl.gz',[{'split':s,'row_in_split':i,'prefix_digest':digest(p),'fire_id':p.fire_id,'source_version':p.source_version,'observation_ids':list(p.source_observation_ids),'dates':[str(d) for d in p.dates],'issued_at':p.issued_at.isoformat(),'synthetic':p.synthetic} for s,values in prefixes.items() for i,p in enumerate(values)])
    x={s:normalized_tensor(p,pre) for s,p in prefixes.items()};y={};future={};target_rows=[]
    for s,rows in split.items():
        packets=[future_targets(r['prefix'],history[r['prefix'].fire_id]) for r in rows]
        y[s]=np.stack([v[0] for v in packets]);future[s]=np.stack([v[1] for v in packets]);target_rows.extend([{'split':s,**v[2]} for v in packets])
    write_rows(output/'independent_targets.jsonl.gz',target_rows)
    selection=np.array([p.fire_id in original['validation_selection_fire_ids'] for p in prefixes['validation']]);calibration=~selection
    if set(original['validation_selection_fire_ids'])&set(original['calibration_fire_ids']):raise ValueError('calibration overlap')
    raw={s:v.reshape(len(v),-1) for s,v in x.items()};summaries={s:interpretable(p) for s,p in prefixes.items()}
    pca=json.loads((root/'pca.json').read_text());pca_mean=np.asarray(pca['mean']);components=np.asarray(pca['components'])
    pcas={s:(v-pca_mean)@components.T for s,v in raw.items()}
    params={'frozen_A':frozen};training={};models={};frozen_features={s:forward(frozen,v,'tcn')[1] for s,v in x.items()}
    params['shared_AD'],training['shared_AD']=fit_group('shared_AD',x,y,selection,config,output,binary=(2,))
    for j,task in enumerate(TASKS):
        if task!='A':params['specific_'+task],training['specific_'+task]=fit_group('specific_'+task,x,{s:v[:,j:j+1] for s,v in y.items()},selection,config,output,binary=(0,) if task=='C' else ())
        models['direct_'+task],training['direct_'+task]=fit_group('direct_'+task,x,{s:v[:,j:j+1] for s,v in y.items()},selection,config,output,kind='mlp',binary=(0,) if task=='C' else ())
    params['specific_E'],training['specific_E']=fit_group('specific_E',x,future,selection,config,output)
    models['shared_mlp'],training['shared_mlp']=fit_group('shared_mlp',x,y,selection,config,output,kind='mlp',binary=(2,))
    models['direct_E'],training['direct_E']=fit_group('direct_E',x,future,selection,config,output,kind='mlp')
    features={'raw':raw,'interpretable':summaries,'PCA4':pcas,'frozen_A':frozen_features}
    for name,p in params.items():
        if name!='frozen_A':features[name]={s:forward(p,v,'tcn')[1] for s,v in x.items()}
    heads={};predictions={};head_costs={};head_states={}
    for name,views in features.items():
        heads[name]={};predictions[name]={};head_states[name]={};start=perf_counter_ns()
        for j,task in enumerate(TASKS):
            model=LinearHead().fit(views['train'],y['train'][:,j],binary=task=='C',alpha=config.ridge_alpha);heads[name][task]=model
            predictions[name][task]={s:model.predict(v) for s,v in views.items()};head_states[name][task]=model.state()
        head_costs[name]=perf_counter_ns()-start
    # Aligned task-specific strategy; cross-task specific-view rows remain separately available.
    predictions['task_specific']={t:predictions['frozen_A' if t=='A' else 'specific_'+t][t] for t in TASKS}
    for name,kind in [('shared_AD','tcn'),('shared_mlp','mlp')]:
        p=params[name] if kind=='tcn' else models[name];spec=training[name];mean=np.array(spec['mean']);scale=np.array(spec['scale'])
        pred={s:forward(p,v,kind)[0]*scale+mean for s,v in x.items()}
        for s in pred:pred[s][:,2]=sigmoid(pred[s][:,2])
        predictions[name+'_end_to_end']={t:{s:pred[s][:,j] for s in x} for j,t in enumerate(TASKS)}
    predictions['direct_MLP']={}
    for task in TASKS:
        spec=training['direct_'+task];p=models['direct_'+task];values={s:forward(p,v,'mlp')[0][:,0] for s,v in x.items()}
        values={s:sigmoid(v) if task=='C' else v*spec['scale'][0]+spec['mean'][0] for s,v in values.items()};predictions['direct_MLP'][task]=values
    evaluation={};prediction_rows=[]
    for name,tasks in predictions.items():
        evaluation[name]={}
        for j,task in enumerate(TASKS):
            values=tasks[task];binary=task=='C';radius=None if binary else regression_radius(y['validation'][calibration,j],values['validation'][calibration])
            evaluation[name][task]={'test':score(y['test'][:,j],values['test'],binary,radius),'interval_radius_log':radius,
              'paired_vs_raw':paired_fire_delta(y['test'][:,j],values['test'],predictions['raw'][task]['test'],ids['test'],config.bootstrap_replicates,config.bootstrap_seed),
              'by_depth':{},'by_generator_stratum':{}}
            for depth in sorted({len(p.dates) for p in prefixes['test']}):
                use=np.array([len(p.dates)==depth for p in prefixes['test']]);evaluation[name][task]['by_depth'][str(depth)]=score(y['test'][use,j],values['test'][use],binary,radius)
            for mode in range(3):
                use=np.array([int(p.fire_id.rsplit('-',1)[1])%3==mode for p in prefixes['test']]);evaluation[name][task]['by_generator_stratum'][str(mode)]=score(y['test'][use,j],values['test'][use],binary,radius)
            prediction_rows.extend({'method':name,'task':task,'fire_id':p.fire_id,'depth':len(p.dates),'prefix_digest':digest(p),
              'target':float(y['test'][i,j]),'prediction':float(values['test'][i])} for i,p in enumerate(prefixes['test']))
    dump(output/'evaluation.json',evaluation);write_rows(output/'held_out_predictions.jsonl.gz',prediction_rows)
    dump(output/'training_records.json',training);dump(output/'downstream_head_states.json',head_states);dump(output/'head_fit_costs.json',head_costs)
    # Retrieval without E labels in the distance, then explicitly E-supervised lightweight heads.
    relevance=standardize(future['train'],future['test']);retrieval_results={};retrieval_models={}
    for name,views in features.items():
        coordinate=standardize(views['train'],views['test']);retrieval_results[name]={'representation_distance':retrieval(coordinate,relevance,ids['test'],config.retrieval_k)}
        e_head_start=perf_counter_ns()
        eheads=[LinearHead().fit(views['train'],future['train'][:,j],alpha=config.ridge_alpha) for j in range(3)];retrieval_models[name]=eheads
        retrieval_results[name]['representation_distance']['E_head_fit_ns']=perf_counter_ns()-e_head_start
        train_pred=np.column_stack([h.predict(views['train']) for h in eheads]);test_pred=np.column_stack([h.predict(views['test']) for h in eheads])
        candidates=np.array([i for i,p in enumerate(prefixes['test']) if p.fire_id!=prefixes['test'][0].fire_id])
        _,query_cost=timed(lambda:np.argsort(np.sum((coordinate[candidates]-coordinate[0])**2,axis=1),kind='stable')[:config.retrieval_k])
        retrieval_results[name]['representation_distance']['serving_distance_topk_cost']=query_cost
        retrieval_results[name]['representation_distance']['cost_scope']='one warm query, precomputed gallery/query coordinates and same-fire candidate mask; excludes encoder, future relevance grading and refresh'
        # Common future-outcome scale (not per-model predicted spread).
        scale=future['train'].std(0);scale[scale<1e-8]=1
        retrieval_results[name]['E_supervised_head_distance']=retrieval(test_pred/scale,relevance,ids['test'],config.retrieval_k)
    p=models['direct_E'];spec=training['direct_E'];direct_test=forward(p,x['test'],'mlp')[0]*np.array(spec['scale'])+np.array(spec['mean'])
    retrieval_results['direct_MLP_E']={'E_supervised_head_distance':retrieval(direct_test/future['train'].std(0),relevance,ids['test'],config.retrieval_k)}
    for name,modes in retrieval_results.items():
        for mode,result in modes.items():
            raw_result=retrieval_results['raw'][mode];fire_names=sorted(result['per_fire_precision'])
            delta=np.array([result['per_fire_precision'][i]-raw_result['per_fire_precision'][i] for i in fire_names])
            rng=np.random.default_rng(config.bootstrap_seed);resampled=delta[rng.integers(0,len(delta),(config.bootstrap_replicates,len(delta)))].mean(1)
            result['paired_vs_raw_precision']={'mean_fire_delta':float(delta.mean()),'descriptive_95_interval':np.quantile(resampled,[.025,.975]).tolist(),'fires':len(delta),'scope':'conditional descriptive fire resampling; no wildfire population inference'}
            result['chance_precision_at_k']=float(np.mean([config.retrieval_k/r['candidate_count'] for r in result['rows']]))
    dump(output/'retrieval.json',retrieval_results);dump(output/'E_head_states.json',{n:[h.state() for h in hs] for n,hs in retrieval_models.items()})
    probes=diagnostic_probes(features,prefixes,output)
    featurizers={'raw':lambda p:normalized_tensor(p,pre).reshape(len(p),-1),'interpretable':interpretable,
      'PCA4':lambda p:(normalized_tensor(p,pre).reshape(len(p),-1)-pca_mean)@components.T}
    for name,p in params.items():featurizers[name]=lambda prefixes,p=p:forward(p,normalized_tensor(prefixes,pre),'tcn')[1]
    control_diagnostics(prefixes['test'],pre,featurizers,heads,output,features,retrieval_results)
    specific_make={t:featurizers['frozen_A' if t=='A' else 'specific_'+t] for t in TASKS}
    reuse_heads={**heads,'specific_A':heads['frozen_A']}
    reuse=reuse_costs(prefixes['test'][0],pre,{'prefixes_test':prefixes['test'],'specific_featurizers':specific_make},featurizers,reuse_heads,params,training,output)
    if state_digest(frozen)!=frozen_digest:raise ValueError('original encoder mutated')
    manifest={'version':'fire-transfer-results-v1','status':'complete','timestamp':datetime.now(timezone.utc).isoformat(),
      'scientific_scope':'synthetic task transfer, predictive-outcome relevance, no real-fire or real-agent evidence',
      'source_manifest_sha256':sha(root/'manifest.json'),'source_cohort_digest':original['source_digest'],
      'config_digest':digest(config),'frozen_encoder_digest_before':frozen_digest,'frozen_encoder_digest_after':state_digest(frozen),
      'original_A_training_ns_historical':original['costs']['tcn_all_seeds_training_ns'],'current_network_training_ns':sum(v['all_seeds_training_ns'] for v in training.values()),
      'samples':{s:len(p) for s,p in prefixes.items()},'fires':{s:len(set(i)) for s,i in ids.items()},
      'selection_fire_ids':original['validation_selection_fire_ids'],'calibration_fire_ids':original['calibration_fire_ids'],
      'real_model_calls':0,'real_source_rows_read':0,'code_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('transfer_*.py')},
      'output_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file()},'evaluation_digest':digest(evaluation),
      'limitations':['Existing synthetic M4 cohort, previously observed A performance','Correlated targets from same 3-day future','Conditional descriptive fire bootstrap, not population inference','Multitask/task-specific supervision exceeds A-only objective','No full lifecycle cost/refresh measurements','Nonlinear property probes do not prove exactness']}
    dump(output/'manifest.json',manifest);return manifest


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='reports/embedding_utility/fire_vase/config/transfer-m5-v1.json');p.add_argument('--output',required=True);a=p.parse_args()
    result=run(json.loads(Path(a.config).read_text()),a.output);print(json.dumps({k:result[k] for k in ('status','samples','evaluation_digest','real_model_calls')}))

if __name__=='__main__':main()
