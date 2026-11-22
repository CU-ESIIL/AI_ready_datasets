"""Isolated same-workload observed-state serving, cache, refresh and model-update costs."""
import argparse,csv,json,time,hashlib,resource
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import forward,train,encode
from evaluate_fire_vase_milestone8 import decode


def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));y=ds['y'];mask=ds['mask'];tr=ds['fold']=='train';scale=np.load(private/'evaluation-scales.npz')['scale'];x=(np.column_stack([np.where(mask,y,prep['median']),mask.astype(float)])-prep['mean'])/prep['scale'];q=np.load(private/'retrieval-query-indices.npz')['indices'];truth=y[q];valid=mask[q];rows=[];materialization=[];construction=json.loads((out/'feature-construction.json').read_text())['seconds'];stages=json.loads((out/'runtime-stages.json').read_text());dtype='float64 scientific state; learned serving vectors float32'
 n_from_dates=np.diff(ds['offsets']);span=ds['date_ordinals'][ds['offsets'][1:]-1]-ds['date_ordinals'][ds['offsets'][:-1]]
 def timed(fn,repeats=20):
  times=[]
  for _ in range(repeats):
   start=time.perf_counter();value=fn();times.append(time.perf_counter()-start)
  return value,float(np.median(times))
 def add(label,fn,fixed,storage,kind):
  pred,seconds=timed(fn);pred=pred.copy()
  # The common metadata sidecar supplies counts/spans in this serving workload.
  pred[:,1]=np.log1p(n_from_dates[q]);pred[:,9]=np.log1p(span[q]);error=np.where(valid,((pred-truth)/scale)**2,0);perfire=error.sum(1)/valid.sum(1)
  rows.append({'method':label,'mode':kind,'workload':'4096 fixed stratified test fires, all defined transformed observed-property answers (declared log/asinh conventions); common sidecar conditionB; original-unit errors reported separately','fires_per_batch':len(q),'defined_property_queries_per_batch':int(valid.sum()),'standardized_fire_mean_property_mse':float(perfire.mean()),'batch_serving_seconds':seconds,'seconds_per_fire_amortized_batch':seconds/len(q),'measured_fixed_component_seconds':fixed,'numeric_representation_storage_bytes':storage,'precision':dtype,'physical_IO_bytes':None})
 add('cached_native',lambda:y[q].copy(),construction,y.nbytes,'cached exact scientific operations')
 add('interpretable_exact',lambda:y[q].copy(),construction,y.nbytes,'materialized scalar scientific state')
 # Exact answer cache is keyed by native fire ID and this complete scientific request.
 t=time.perf_counter();cache={str(ds['ids'][i]):y[i].copy() for i in q};cache_build=time.perf_counter()-t
 add('cached_complete_answers',lambda:np.asarray([cache[str(ds['ids'][i])] for i in q]),construction+cache_build,sum(v.nbytes for v in cache.values()),'warm identical-bundle cache; source refresh invalidates')
 add('adaptive_native_exact',lambda:y[q].copy(),construction,y.nbytes,'deterministic native-operation routing, not LLM reasoning')
 for d in (4,8,16,32,64):
  label='pca-request'+str(d);pca=dict(np.load(private/f'pca-{d}-1p0.npz'));t=time.perf_counter();z=x@pca['components'];elapsed=time.perf_counter()-t
  t=time.perf_counter();storage_path=private/f'lifecycle-store-{label}.npz';np.savez_compressed(storage_path,z=z);write_seconds=time.perf_counter()-t;materialization.append({'method':label,'all_fire_encoding_seconds':elapsed,'materialization_write_seconds':write_seconds,'on_disk_bytes':storage_path.stat().st_size,'numeric_bytes':z.nbytes,'effective_rank':z.shape[1]});head=dict(np.load(private/f'{label}-linear_ridge-1p0-head.npz'));fit=next(r['seconds'] for r in stages if r['method']==label and r['fraction']==1. and r['stage']=='pca_fit_shared');probe=next(r['seconds'] for r in stages if r['method']==label and r.get('probe')=='linear_ridge' and r['fraction']==1. and r['stage']=='probe_fit_and_predict');add(label,lambda z=z,h=head:decode(h,z[q]),construction+fit+elapsed+probe+write_seconds,z.nbytes,'materialized PCA plus supervised linear recovery head')
 for family in ('supervised','self_supervised','multitask'):
  for d in (4,8,16,32,64):
   label=family+'-'+str(d);params=dict(np.load(private/f'{label}-1p0.npz'));t=time.perf_counter();optimized=encode(params,x);optimized_encoding=time.perf_counter()-t;stored=np.load(private/f'{label}-materialized.npz')['z'];assert np.array_equal(optimized.astype(np.float32),stored);z=optimized.astype(np.float32);head=dict(np.load(private/f'{label}-linear_ridge-1p0-head.npz'));fit=next(r['seconds'] for r in stages if r['method']==label and r['fraction']==1. and r['stage']=='training');encoding_seconds=optimized_encoding;probe=next(r['seconds'] for r in stages if r['method']==label and r.get('probe')=='linear_ridge' and r['fraction']==1. and r['stage']=='probe_fit_and_predict');t=time.perf_counter();storage_path=private/f'lifecycle-store-{label}.npz';np.savez_compressed(storage_path,z=z);write_seconds=time.perf_counter()-t;materialization.append({'method':label,'materialization_write_seconds':write_seconds,'on_disk_bytes':storage_path.stat().st_size,'numeric_bytes':z.nbytes});add(label,lambda z=z,h=head:decode(h,z[q]),construction+fit+encoding_seconds+probe+write_seconds,z.nbytes,'materialized float32 embedding plus supervised linear head')
   if d==16:
    add(label+'-on-demand',lambda p=params,h=head:decode(h,encode(p,x[q])),construction+fit+probe,0,'on-demand from already constructed cached native state; native state cost included in fixed component')
    # Fresh materialization under an unchanged identity checks refresh cost; no
    # raw source refresh was simulated or claimed.
    t=time.perf_counter();refreshed=encode(params,x);refresh=time.perf_counter()-t;materialization.append({'method':label,'all_fire_reencoding_seconds':refresh,'numeric_bytes':refreshed.nbytes,'scope':'unchanged-source encoder refresh only; source updates require re-verification'})
 csvwrite(out/'lifecycle-workload.csv',rows);(out/'refresh-measurements.json').write_text(json.dumps(materialization,indent=2)+'\n')
 # Component-sum cumulative costs are explicitly scenarios using measured terms.
 scenarios=[]
 for count in (1,10,100,1000,10000,100000,1000000):
  for row in rows:scenarios.append({'method':row['method'],'query_fire_count':count,'component_sum_seconds':row['measured_fixed_component_seconds']+count*row['seconds_per_fire_amortized_batch'],'property_mse':row['standardized_fire_mean_property_mse'],'scope':'measured warm batch components, not an empirical million-query production run'})
 csvwrite(out/'lifecycle-reuse-scenarios.csv',scenarios)
 # Pareto comparisons use exactly the same request bundle and equal-fire query set.
 fronts=[]
 for count in (1,1000,1000000):
  candidates=[r for r in scenarios if r['query_fire_count']==count]
  for r in candidates:
   dominated=any(s['component_sum_seconds']<=r['component_sum_seconds'] and s['property_mse']<=r['property_mse'] and (s['component_sum_seconds']<r['component_sum_seconds'] or s['property_mse']<r['property_mse']) for s in candidates)
   fronts.append({**r,'dominated':dominated})
 csvwrite(out/'cost-accuracy-pareto.csv',fronts)
 updates=[];target=(y-prep['target_mean'])/prep['target_scale']
 for family,cols in [('supervised',[1]),('self_supervised',None),('multitask',[0,1,4])]:
  for cycle in (1,2):
   yy=x if cols is None else target[:,cols];mm=np.ones_like(x,bool) if cols is None else mask[:,cols];t=time.perf_counter();p,curve=train(x[tr],yy[tr],mm[tr],16,epochs=12,seed=20260828+100+cycle);fit=time.perf_counter()-t;t=time.perf_counter();z=encode(p,x);encoding=time.perf_counter()-t;path=private/f'lifecycle-update-{family}-{cycle}.npz';np.savez_compressed(path,**p);identity=hashlib.sha256(b''.join(p[k].tobytes() for k in sorted(p))).hexdigest();updates.append({'family':family,'cycle':cycle,'model_digest':identity,'training_seconds':fit,'all_fire_encoding_seconds':encoding,'checkpoint_bytes':path.stat().st_size,'scope':'measured update cost only; no predictive evaluation, not independent primary seeds'})
 (out/'model-update-costs.json').write_text(json.dumps(updates,indent=2)+'\n')
 (out/'lifecycle-scope.json').write_text(json.dumps({'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_raw_area_numeric_bytes_float64':627033*8,'source_dates_provenance_storage':'shared and retained for every representation, not included in numeric-vector bytes','prepared_scientific_state_seconds':construction,'native_direct_fallback_cost':'actual whole-test-fires measurement in access-independent-validation.json; not substituted with encoding latency','unknown_components':['filesystem physical read bytes','production concurrency','true source updates','end-to-end remote network serving','index/recipe rights or independent ecological validity'],'fitted_model_costs':'observed actual fitting and probe stages; probe-fit-and-predict timing includes full-population inference, so not pure training CPU','retrieval_index_costs':'separately measured in retrieval-runtime.json; not silently charged to property-query workload'},indent=2)+'\n');print('LIFECYCLE COMPLETE',flush=True)
if __name__=='__main__':main()
