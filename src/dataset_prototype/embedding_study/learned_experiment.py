"""Synthetic future-observation task, independent evaluation and lifecycle accounting."""
import argparse
from collections import defaultdict
from datetime import datetime,timezone,timedelta
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter_ns,process_time_ns
from statistics import median
import numpy as np
from ..contracts import digest
from .learned_contracts import PrefixInput
from .learned_data import generate,validate_pair,raw_tensor,interpretable,PrefixPreprocessor,cache_identity,RECIPE
from .learned_models import Ridge,fit_network,forward,state_digest,parameter_count,save_checkpoint,load_checkpoint


def dump(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def normalized_tensor(prefixes,pre):
    x=raw_tensor(prefixes);mask=x[:,:,2].copy()
    for c in (0,1,3):x[:,:,c]=(x[:,:,c]-pre.mean[c])/pre.scale[c]*mask
    return x


def conformal_radius(y,prediction,coverage=.9):
    residual=np.sort(np.abs(y-prediction));index=min(len(y),int(np.ceil((len(y)+1)*coverage)))-1
    return float(residual[index])


def metrics(y,prediction,radius):
    original=np.expm1(y);point=np.expm1(np.maximum(0,prediction))
    lo=np.expm1(np.maximum(0,prediction-radius));hi=np.expm1(np.maximum(0,prediction+radius))
    return {'n':len(y),'mse_log1p':float(np.mean((y-prediction)**2)),
      'mae_km2_day':float(np.mean(np.abs(original-point))),
      'coverage_90':float(np.mean((original>=lo)&(original<=hi))),
      'mean_interval_width_km2_day':float(np.mean(hi-lo))}


def timed(call,repeats=31):
    values=[];answer=None
    for _ in range(repeats):
        start=perf_counter_ns();answer=call();values.append(perf_counter_ns()-start)
    return answer,{'median_ns':median(values),'min_ns':min(values),'repeats':repeats}


def checked_embedding_lookup(store,key,expected_identity):
    entry=store[key]
    if entry['identity']!=expected_identity:raise ValueError('stale source/encoder/preprocessing identity')
    value=np.asarray(entry['embedding'],dtype=float)
    if value.shape!=(4,) or not np.isfinite(value).all():raise ValueError('invalid stored embedding')
    return value


def materialization(prefixes,pre,params,probe,output):
    identity=state_digest(params);prestate=pre.state()
    start=perf_counter_ns();store={}
    for p in prefixes:
        z=forward(params,normalized_tensor([p],pre),'tcn')[1][0]
        key=digest(p);store[key]={'identity':cache_identity(p,identity,prestate),'embedding':z.tolist(),
            'fire_id':p.fire_id,'observation_ids':list(p.source_observation_ids),'issued_at':p.issued_at.isoformat()}
    construction=perf_counter_ns()-start
    path=output/'materialized_embeddings.json';start=perf_counter_ns();dump(path,store);write_ns=perf_counter_ns()-start
    start=perf_counter_ns();reloaded=json.loads(path.read_text());read_ns=perf_counter_ns()-start
    prefix=prefixes[0];key=digest(prefix);expected=cache_identity(prefix,identity,prestate)
    def on_demand():
        z=forward(params,normalized_tensor([prefix],pre),'tcn')[1]
        return float(probe.predict(z)[0])
    def stored():return float(probe.predict(checked_embedding_lookup(reloaded,key,expected)[None,:])[0])
    a,cold=timed(on_demand);b,lookup=timed(stored)
    if not np.isclose(a,b,rtol=0,atol=1e-12):raise ValueError('materialization changed prediction')
    identity_start=perf_counter_ns();prediction_key=digest({'prefix':prefix.model_dump(mode='json'),'checkpoint':identity,'probe':probe.state()});identity_ns=perf_counter_ns()-identity_start
    cached={prediction_key:a}
    _,cached_cost=timed(lambda:cached[prediction_key])
    per_construct=construction/len(prefixes);saving=cold['median_ns']-lookup['median_ns']
    n=np.ceil((per_construct+(write_ns+read_ns)/len(prefixes))/saving) if saving>0 else None
    rows=[]
    for frequency in (1,10,100,1000,10000):
        rows.append({'queries_per_prefix':frequency,'on_demand_ns':frequency*cold['median_ns'],
          'materialized_ns':per_construct+(write_ns+read_ns)/len(prefixes)+frequency*lookup['median_ns'],
          'cached_prediction_ns':cold['median_ns']+(frequency-1)*cached_cost['median_ns']})
    return {'embedding_dimension':4,'construction_total_ns':construction,'json_write_ns':write_ns,'json_read_ns':read_ns,
      'query_identity_construction_ns':identity_ns,'stored_bytes':path.stat().st_size,'coordinate_numeric_bytes':len(prefixes)*4*8,'prefix_count':len(prefixes),
      'on_demand_encoder_plus_probe':cold,'stored_embedding_plus_same_probe':lookup,'cached_complete_prediction':cached_cost,
      'measured_prediction_equal':True,'per_prefix_break_even_queries_formula':float(n) if n is not None else None,
      'reuse_scenarios':rows,'refresh':'Changed source/prefix, preprocessing, checkpoint or probe invalidates relevant caches; all affected embeddings must be regenerated after retraining.',
      'scope':'Warm local scalar queries on validated immutable prefixes. Cache identity construction recorded separately, precomputed keys used for cached results. Preprocessing/lookup key scopes explicit. No remote storage/maintenance labor/refresh rate measured; training costs recorded separately; identical trained encoder/probe in both modes.'}


def perturbations(prefix,pre,params):
    base=forward(params,normalized_tensor([prefix],pre),'tcn')[1][0];g=np.array(prefix.growth_km2_day)
    variants={'temporal_order':g[np.random.default_rng(451).permutation(len(g))],
      'same_shape_different_scale':g*4,'equal_total_reversed_development':g[::-1]}
    result=[]
    for kind,values in variants.items():
        p=prefix.model_copy(update={'growth_km2_day':tuple(float(x) for x in values)})
        z=forward(params,normalized_tensor([p],pre),'tcn')[1][0]
        result.append({'control':kind,'base_prefix_digest':digest(prefix),'derived_prefix_digest':digest(p),'recipe':'prefix-perturbation-v1','embedding_l2_change':float(np.linalg.norm(z-base)),
          'expected':'sensitivity diagnostic, not a required invariant for absolute next-day growth',
          'observed_prefix_total_ratio':float(sum(values)/sum(g))})
    # Removing a dated observation changes calendar support. Contract must abstain,
    # not compress the gap into consecutive sequence positions or impute zeros.
    packet=prefix.model_dump(mode='json')
    for key in ('dates','growth_km2_day','available_at','source_observation_ids'):packet[key].pop(1)
    try:PrefixInput.model_validate(packet)
    except ValueError:removal='rejected_gap'
    else:raise ValueError('missing-observation control failed closed support')
    result.append({'control':'observation_removal','outcome':removal,'expected':'abstain; missing is not zero'})
    packet=prefix.model_dump(mode='json');packet['dates']=[str(prefix.dates[0]+timedelta(days=2*i)) for i in range(len(g))]
    try:PrefixInput.model_validate(packet)
    except ValueError:resolution='rejected_non_daily_support'
    else:raise ValueError('resolution control failed')
    result.append({'control':'temporal_resolution','outcome':resolution,'expected':'requires a new support recipe, not automatic invariance'})
    relabeled=prefix.model_copy(update={'fire_id':'opaque-renamed-fire','source_observation_ids':tuple('renamed-'+str(i) for i in range(len(g)))})
    renamed=forward(params,normalized_tensor([relabeled],pre),'tcn')[1][0]
    if not np.array_equal(base,renamed):raise ValueError('nominal identifier invariance failed')
    result.append({'control':'nominal_id_relabeling','embedding_l2_change':float(np.linalg.norm(base-renamed)),'expected':'exact invariance; identifiers are lineage, never model inputs'})
    result.append({'control':'spatial_geometry','outcome':'not_available','expected':'no invented geometry or spatial robustness'})
    return result


def run(config,output):
    from .learned_training_contracts import TrainingConfig
    config=TrainingConfig.model_validate(config);output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    dump(output/'frozen_config.json',config.model_dump(mode='json'))
    started=perf_counter_ns();histories,records=generate(config)
    dump(output/'synthetic_histories.json',histories)
    history_lookup={h['fire_id']:h for h in histories}
    for record in records:
        validate_pair(record['prefix'],record['outcome'])
        if record['outcome'].growth_km2_day!=history_lookup[record['prefix'].fire_id]['growth_km2_day'][len(record['prefix'].dates)]:raise ValueError('independent future-observation reference mismatch')
    split={s:[r for r in records if r['split']==s] for s in ('train','validation','test')}
    groups={s:{r['prefix'].fire_id for r in rows} for s,rows in split.items()}
    if any(groups[a]&groups[b] for a,b in (('train','test'),('train','validation'),('validation','test'))):raise ValueError('fire split leakage')
    prefixes={s:[r['prefix'] for r in rows] for s,rows in split.items()}
    pre=PrefixPreprocessor().fit(prefixes['train']);dump(output/'preprocessing.json',pre.state())
    x={s:normalized_tensor(p,pre) for s,p in prefixes.items()}
    y={s:np.log1p([r['outcome'].growth_km2_day for r in rows]) for s,rows in split.items()}
    target_mean=float(y['train'].mean());target_scale=float(y['train'].std()) or 1
    validation_ids=sorted(groups['validation']);half=len(validation_ids)//2
    selection_ids=set(validation_ids[:half]);calibration_ids=set(validation_ids[half:])
    selection_mask=np.array([p.fire_id in selection_ids for p in prefixes['validation']])
    calibration_mask=~selection_mask
    f={s:interpretable(p) for s,p in prefixes.items()}
    predictions={};models={};costs={};states={};all_seeds=[]
    raw={s:a.reshape(len(a),-1) for s,a in x.items()}
    start=perf_counter_ns();_,_,vt=np.linalg.svd(raw['train']-raw['train'].mean(0),full_matrices=False)
    pca_mean=raw['train'].mean(0);pca_components=vt[:4];pca={s:(a-pca_mean)@pca_components.T for s,a in raw.items()};costs['pca_preparation_ns']=perf_counter_ns()-start
    dump(output/'pca.json',{'mean':pca_mean.tolist(),'components':pca_components.tolist(),'training_fire_ids':sorted(groups['train']),'dimension':4})
    for name,features in [('raw_ridge',raw),('interpretable_ridge',f),('pca4_ridge',pca)]:
        start=perf_counter_ns();model=Ridge().fit(features['train'],y['train'],config.ridge_alpha);costs[name+'_fit_ns']=perf_counter_ns()-start
        predictions[name]={s:model.predict(features[s]) for s in split};states[name]=model.state();models[name]=model
    predictions['persistence']={s:np.log1p([p.growth_km2_day[-1] for p in prefixes[s]]) for s in split}
    predictions['training_mean']={s:np.full(len(rows),target_mean) for s,rows in split.items()}
    best_params=None
    for kind in ('tcn','mlp'):
        candidates=[]
        for seed in config.training_seeds:
            wall=perf_counter_ns();cpu=process_time_ns()
            params,losses=fit_network(x['train'],(y['train']-target_mean)/target_scale,kind,seed,config.epochs,config.learning_rate)
            wall=perf_counter_ns()-wall;cpu=process_time_ns()-cpu
            pred={s:forward(params,x[s],kind)[0]*target_scale+target_mean for s in split}
            score=float(np.mean((pred['validation'][selection_mask]-y['validation'][selection_mask])**2));filename=f'{kind}-seed-{seed}.npz';save_checkpoint(output/filename,params)
            restored=load_checkpoint(output/filename,kind)
            if state_digest(params)!=state_digest(restored):raise ValueError('checkpoint replay mismatch')
            item={'kind':kind,'seed':seed,'architecture':{'kind':kind,'window':12,'input_channels':4,'hidden_channels':8 if kind=='tcn' else 3,'kernel':3 if kind=='tcn' else None,'activation':'tanh','objective':'MSE of training-standardized log1p next-day growth','optimizer':'Adam beta=(0.9,0.999), global norm clip 5, weight L2 1e-4'},'parameters':parameter_count(params),'embedding_dimension':4,
              'wall_training_ns':wall,'cpu_training_ns':cpu,'validation_mse_log1p':score,
              'checkpoint':filename,'checkpoint_sha256':sha(output/filename),'parameter_digest':state_digest(params),'loss_curve':losses}
            all_seeds.append(item);candidates.append((score,seed,params,pred,item))
        _,seed,params,pred,item=min(candidates,key=lambda c:(c[0],c[1]))
        predictions[kind+'_end_to_end']=pred;costs[kind+'_all_seeds_training_ns']=sum(a['wall_training_ns'] for a in all_seeds if a['kind']==kind)
        states[kind]={'selected_seed_by_validation':seed,'checkpoint':item['checkpoint'],'parameter_digest':state_digest(params),'target_mean':target_mean,'target_scale':target_scale}
        if kind=='tcn':
            best_params=params;z={s:forward(params,x[s],kind)[1] for s in split}
            start=perf_counter_ns();probe=Ridge().fit(z['train'],y['train'],config.ridge_alpha);costs['learned_probe_fit_ns']=perf_counter_ns()-start
            predictions['learned4_ridge']={s:probe.predict(z[s]) for s in split};states['learned_probe']=probe.state()
        for a in candidates:
            pp=a[3];radius=conformal_radius(y['validation'][calibration_mask],pp['validation'][calibration_mask]);a[4]['test_metrics_descriptive_only']=metrics(y['test'],pp['test'],radius)
    dump(output/'model_states.json',states);dump(output/'training_records.json',all_seeds)
    evaluation={};rows=[]
    for name,pred in predictions.items():
        radius=conformal_radius(y['validation'][calibration_mask],pred['validation'][calibration_mask]);evaluation[name]={'test':metrics(y['test'],pred['test'],radius),'calibration_log_radius':radius,'by_depth':{},'synthetic_group_strata':{}}
        for depth in config.depths:
            keep=np.array([len(p.dates)==depth for p in prefixes['test']]);evaluation[name]['by_depth'][str(depth)]=metrics(y['test'][keep],pred['test'][keep],radius)
        for region in ('A','B'):
            keep=np.array([r['synthetic_region']==region for r in split['test']]);evaluation[name]['synthetic_group_strata'][region]=metrics(y['test'][keep],pred['test'][keep],radius)
        for i,r in enumerate(split['test']):rows.append({'method':name,'fire_id':r['prefix'].fire_id,'depth':len(r['prefix'].dates),
            'target_observation_id':r['outcome'].observation_id,'target_date':str(r['outcome'].date),'target_km2_day':r['outcome'].growth_km2_day,
            'prediction_log1p':float(pred['test'][i]),'issued_at':r['prefix'].issued_at.isoformat(),'prefix_digest':digest(r['prefix']),
            'source_observation_ids':list(r['prefix'].source_observation_ids),'synthetic':True})
    dump(output/'evaluation.json',evaluation);dump(output/'held_out_predictions.json',rows)
    material=materialization(prefixes['test'],pre,best_params,probe,output)
    # Matched direct feature costs, preprocessing included; target never enters timing.
    p=prefixes['test'][0]
    _,direct=timed(lambda:float(models['interpretable_ridge'].predict(interpretable([p]))[0]))
    _,rawcost=timed(lambda:float(models['raw_ridge'].predict(normalized_tensor([p],pre).reshape(1,-1))[0]))
    direct_key=digest({'prefix':p.model_dump(mode='json'),'recipe':RECIPE,'model':models['interpretable_ridge'].state()})
    direct_value=float(models['interpretable_ridge'].predict(interpretable([p]))[0]);direct_cache={direct_key:direct_value}
    _,cached_direct=timed(lambda:direct_cache[direct_key])
    material.update(direct_interpretable_features_plus_probe=direct,raw_features_plus_probe=rawcost,cached_direct_feature_prediction=cached_direct)
    dump(output/'materialization.json',material)
    controls=perturbations(prefixes['test'][0],pre,best_params)
    # Neighborhood fidelity is raw-input geometry agreement, not analog relevance.
    from itertools import combinations
    zp=z['test'];rp=raw['test'];overlaps=[]
    for i in range(min(64,len(zp))):
        a=np.argsort(np.sum((zp-zp[i])**2,1));b=np.argsort(np.sum((rp-rp[i])**2,1))
        aa=[int(j) for j in a if j!=i][:5];bb=[int(j) for j in b if j!=i][:5];overlaps.append(len(set(aa)&set(bb))/5)
    dump(output/'representation_controls.json',{'controls':controls,'raw_vs_embedding_top5_overlap_mean':float(np.mean(overlaps)),
      'scope':'Raw-input geometry fidelity diagnostic only; same-fire prefixes may neighbor; no ecological relevance labels','reconstruction_error':'not_applicable; supervised future task, no reconstruction objective'})
    manifest={'version':'fire-learned-experiment-v1','status':'complete','timestamp':datetime.now(timezone.utc).isoformat(),
      'scientific_scope':'synthetic future-observation control only; no real-fire or real-agent evidence',
      'task':'one next-calendar-day observed growth increment from available prefix; log1p(km2/day) MSE',
      'recipe':RECIPE,'source_rights':'CC0-1.0 generated synthetic controls','config_digest':digest(config),
      'source_digest':digest(histories),'split_fire_ids':{s:sorted(ids) for s,ids in groups.items()},
      'sample_counts':{s:len(rows) for s,rows in split.items()},'prefix_input_provenance_digest':digest([r['prefix'].model_dump(mode='json') for r in records]),
      'validation_selection_fire_ids':sorted(selection_ids),'calibration_fire_ids':sorted(calibration_ids),
      'architecture':{'tcn':'causal Conv1D kernel3 channels4 to8; masked mean plus last state; tanh embedding4; linear head1','mlp':'flatten48 -> tanh3 -> tanh4 -> linear1','loss':'training-only standardized next-calendar-day log1p growth MSE + weight L2 1e-4','optimization':'Adam .9/.999, epsilon1e-8, batch64, global gradient norm clip5'},
      'real_source_rows_read':0,'real_model_calls':0,'runtime':{'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform()},
      'total_wall_ns':perf_counter_ns()-started,'costs':costs,
      'code_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('learned_*.py')},
      'output_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file()},
      'evaluation_digest':digest(evaluation),'unsupported':['Real predictive validity','Operational availability for real fires','Real year/region transfer','Ecological analog relevance','Complete lifecycle costs','Real agent/metadata benefit']}
    dump(output/'manifest.json',manifest);return manifest


def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='reports/embedding_utility/fire_vase/config/learned-synthetic-m4-v1.json');p.add_argument('--output',required=True);args=p.parse_args()
    result=run(json.loads(Path(args.config).read_text()),args.output);print(json.dumps({k:result[k] for k in ('status','sample_counts','evaluation_digest','real_source_rows_read','real_model_calls')}))

if __name__=='__main__':main()
