"""Measured retrieval, access conditions, paired effects and lifecycle on real M8 artifacts."""
import argparse,csv,hashlib,itertools,json,math,sqlite3,time
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import rankdata
from dataset_prototype.embedding_study.utility_learning import forward,probe_fit,access_rows
from dataset_prototype.embedding_study.population_profile import DAILY,DAILY_TABLE,readonly
from dataset_prototype.embedding_study.observed_state import calculate,NAMES
from dataset_prototype.embedding_study.lake_design import holm_adjust


def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def scalar_neighbors(gallery,queries,k=10):
 order=np.argsort(gallery,kind='stable');sorted_values=gallery[order];output=[]
 for q in queries:
  pos=np.searchsorted(sorted_values,q);lo=max(0,pos-k);hi=min(len(order),pos+k);idx=order[lo:hi];output.append(idx[np.lexsort((idx,abs(gallery[idx]-q)))[:k]])
 return np.asarray(output)


def decode(head,z):
 a=(z-head['mean'])/head['scale']
 if 'projection' in head:a=np.column_stack([a,np.tanh(a@head['projection'])])
 return a@head['coefficients']+head['intercepts']


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--lake',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz',allow_pickle=False));ids=ds['ids'];y=ds['y'];mask=ds['mask'];n=ds['n'];train=ds['fold']=='train';test=ds['fold']=='test';test_idx=np.flatnonzero(test);scale=dict(np.load(private/'evaluation-scales.npz'))['scale'];prep=dict(np.load(private/'preprocess-1p0.npz'));x=(np.column_stack([np.where(mask,y,prep['median']),mask.astype(float)])-prep['mean'])/prep['scale']
 chosen=[]
 for s in (1,2,3):
  eligible=test_idx[(n[test_idx]==s) if s<3 else n[test_idx]>=3];order=sorted(eligible,key=lambda i:hashlib.sha256(('m8-query-v1:'+str(ids[i])).encode()).digest());chosen.extend(order[:1366 if s==3 else 1365])
 queries=np.array(chosen);assert len(queries)==4096 and not np.any(train[queries]);np.savez(private/'retrieval-query-indices.npz',indices=queries)
 tasks=(0,4,5,6,9);retrieval=[];timings=[];gradings={};models={'raw_state':x}
 for d in (4,8,16,32,64):
  pca=dict(np.load(private/f'pca-{d}-1p0.npz'));models['pca-request'+str(d)]=x@pca['components']
  for family in ('supervised','self_supervised','multitask'):models[family+'-'+str(d)]=np.load(private/f'{family}-{d}-materialized.npz')['z']
 for j in tasks:
  gallery_idx=np.flatnonzero(train&mask[:,j]);qi=queries[mask[queries,j]];g=y[gallery_idx,j]/scale[j];q=y[qi,j]/scale[j];reference=scalar_neighbors(g,q);relevance_threshold=np.max(abs(g[reference]-q[:,None]),axis=1)+1e-8
  # Count all cutoff ties using sorted scientific values, not embedding distances.
  sorted_g=np.sort(g);relevant_count=np.searchsorted(sorted_g,q+relevance_threshold,side='right')-np.searchsorted(sorted_g,q-relevance_threshold,side='left')
  gradings[j]=(gallery_idx,qi,g,q,reference,relevance_threshold,relevant_count)
  np.savez_compressed(private/f'retrieval-reference-{j}.npz',gallery_indices=gallery_idx,query_indices=qi,reference=reference,threshold=relevance_threshold,relevant_count=relevant_count)
 def evaluate(label,route,j,indices,query_time,index_time,index_bytes,rank_correlations=None):
  gi,qi,g,q,reference,threshold,relcount=gradings[j];dist=abs(g[indices]-q[:,None]);precision=(dist<=threshold[:,None]).mean(1);recall=np.sum(dist<=threshold[:,None],axis=1)/relcount;reference_overlap=np.array([len(set(a)&set(b))/10 for a,b in zip(indices,reference)])
  for stratum,use in [('all',np.ones(len(qi),bool)),('one',n[qi]==1),('two',n[qi]==2),('three_plus',n[qi]>=3)]:
   if not use.any():continue
   retrieval.append({'method':label,'route':route,'property':NAMES[j],'stratum':stratum,'queries':int(use.sum()),'gallery':len(gi),'precision_at10':float(precision[use].mean()),'recall_at10_all_cutoff_ties':float(recall[use].mean()),'reference_top10_overlap':float(reference_overlap[use].mean()),'exact_reference_set_fraction':float(np.mean(reference_overlap[use]==1)),'mean_retrieval_error':float(dist[use].mean()),'query_seconds_total':query_time,'index_seconds':index_time,'numeric_index_bytes':index_bytes,'rank_correlation_diagnostic':float(np.nanmean(rank_correlations)) if rank_correlations is not None else None})
  if route=='coordinates':np.savez_compressed(private/f'retrieval-{label}-{j}-errors.npz',query_indices=qi,precision=precision,retrieval_error=dist.mean(1))
 for label,z in [('cached_native',None),('interpretable_exact',None),*models.items()]:
  print('RETRIEVAL '+label,flush=True)
  for j in tasks:
   gi,qi,g,q,reference,threshold,relcount=gradings[j]
   if z is None:
    t=time.perf_counter();index=np.argsort(g,kind='stable');build=time.perf_counter()-t;t=time.perf_counter();idx=scalar_neighbors(g,q);querytime=time.perf_counter()-t;evaluate(label,'exact_property_index',j,idx,querytime,build,g.nbytes+index.nbytes)
    np.savez_compressed(private/f'{label}-property-index-{j}.npz',order=index,values=g[index]);continue
   t=time.perf_counter();tree=cKDTree(np.asarray(z[gi],dtype=np.float64),leafsize=64);build=time.perf_counter()-t;buffers=sum(v.nbytes for v in tree.__getstate__() if isinstance(v,np.ndarray));t=time.perf_counter();_,idx=tree.query(np.asarray(z[qi],dtype=np.float64),k=10,workers=1);querytime=time.perf_counter()-t
   # Rank correlation is explicitly a separate128-query/4096-gallery diagnostic.
   small=np.arange(min(4096,len(gi)));correlations=[]
   for k in range(min(128,len(qi))):
    scientific=abs(g[small]-q[k]);geometric=np.sum((z[gi[small]]-z[qi[k]])**2,axis=1)
    if np.std(scientific)>0 and np.std(geometric)>0:correlations.append(float(np.corrcoef(rankdata(scientific),rankdata(geometric))[0,1]))
   evaluate(label,'coordinates',j,idx,querytime,build,buffers,correlations)
   # A trained scalar-property head is supervised retrieval, not zero-shot.
   for probe in ('linear_ridge','nonlinear_tanh32_ridge'):
    head_path=private/f'{label}-{probe}-1p0-head.npz' if label!='raw_state' else private/f'raw-{probe}-1p0.npz';head=dict(np.load(head_path));pred=decode(head,z)[:,j]/scale[j];t=time.perf_counter();order=np.argsort(pred[gi],kind='stable');buildhead=time.perf_counter()-t;t=time.perf_counter();neighbors=scalar_neighbors(pred[gi],pred[qi]);elapsed=time.perf_counter()-t;evaluate(label,'supervised_'+probe,j,neighbors,elapsed,buildhead,pred[gi].nbytes+order.nbytes)
   timings.append({'method':label,'property':NAMES[j],'coordinates_query_seconds':querytime,'index_build_seconds':build,'gallery':len(gi),'queries':len(qi),'index_numeric_buffers':buffers})
  csvwrite(out/'retrieval-results.csv',retrieval);dump(out/'retrieval-runtime.json',timings)
 # Actual source fallback on every test fire, computed once, with costs distinct
 # from representation preservation. Full source values never enter sidecars.
 fallback_path=out/'native-fallback.json'
 if not fallback_path.exists():
  start=time.perf_counter();latencies=[];decoded_bytes=0;decoded_records=0
  with readonly(Path(a.lake)/DAILY) as db:
   for i in test_idx:
    begin=time.perf_counter_ns();lo,hi=ds['offsets'][i:i+2];rows=[db.execute('SELECT id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" WHERE fid=?',(int(fid),)).fetchone() for fid in ds['native_fid_refs'][lo:hi]]
    assert all(str(r[0])==ids[i] for r in rows);values,valid=calculate([r[2] for r in rows],[__import__('datetime').date.fromisoformat(r[1]).toordinal() for r in rows]);assert np.array_equal(mask[i],valid) and np.allclose(y[i],values,equal_nan=True,rtol=1e-12,atol=1e-12)
    latencies.append(time.perf_counter_ns()-begin);decoded_records+=len(rows);decoded_bytes+=len(json.dumps(rows,separators=(',',':')).encode())
  dump(fallback_path,{'fire_calls':len(test_idx),'operation':'native fid indexed reads followed by observed-state-v1 deterministic operations','native_records_decoded':decoded_records,'returned_native_response_bytes':decoded_bytes,'filesystem_physical_bytes_read':None,'all_recovered_to_reference_tolerance':True,'seconds_including_validation':time.perf_counter()-start,'median_call_ns':float(np.median(latencies)),'total_call_ns':int(sum(latencies)),'source_values_persisted':False,'policy':'always use native for uncertified approximate property answers; no test-error oracle used to decide fallback'})
 # Access-condition table: dates/source support are shared sidecar fields, not hidden areas.
 metric=list(csv.DictReader((out/'information-preservation.csv').open()));access=access_rows(metric)
 csvwrite(out/'access-condition-results.csv',access)
 dump(out/'exactness-register.json',{'R0':'native values/dates/source refs with independently checked operations','R1':'defined scalar property values retained directly; does not uniquely preserve full cumulative histories or absolute dates without metadata','PCA':'floating-point numerical reconstruction/probes, not exact source-bit preservation','learned':'model-dependent recovery only; successful probes do not establish exact sufficiency','A_date_sequence':'not present in selected scientific-state input; raw record retains it','B_date_sequence':'retained original dates support exact recovery from common metadata','C':'native fallback can recover; not embedding information preservation','full_cumulative_sequence':'state collision demonstrated by algebraic unit-test counterexample; undefined exact reconstruction for R1/PCA/learned without source fallback','native_quality':'unknown; masks describe mathematical support, not sensor quality'})
 print('PRIMARY RETRIEVAL AND ACCESS COMPLETE',flush=True)
if __name__=='__main__':main()
