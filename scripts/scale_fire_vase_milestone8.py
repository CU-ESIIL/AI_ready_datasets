"""Controlled gallery/query scaling for the all-fire observed-area retrieval task."""
import argparse,csv,hashlib,time
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from dataset_prototype.embedding_study.utility_learning import forward
from evaluate_fire_vase_milestone8 import scalar_neighbors,decode


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));x=(np.column_stack([np.where(ds['mask'],ds['y'],prep['median']),ds['mask'].astype(float)])-prep['mean'])/prep['scale'];base=np.load(private/'retrieval-query-indices.npz')['indices'];groups=[base[ds['n'][base]==1],base[ds['n'][base]==2],base[ds['n'][base]>=3]];queries=np.array([group[i] for i in range(max(map(len,groups))) for group in groups if i<len(group)]);gallery=np.flatnonzero(ds['fold']=='train');gallery=np.array(sorted(gallery,key=lambda i:hashlib.sha256(('m8-scale-gallery:'+str(ds['ids'][i])).encode()).digest()));models={'cached_native':None,'raw_state':x};pca=np.load(private/'pca-16-1p0.npz')['components'];models['pca-request16']=x@pca
 for family in ('supervised','self_supervised','multitask'):models[family+'-16']=np.load(private/f'{family}-16-materialized.npz')['z']
 results=[]
 for size in (1000,10000,50000,len(gallery)):
  g=gallery[:size];truth=ds['y'][g,0];query_truth=ds['y'][queries,0];reference=scalar_neighbors(truth,query_truth);cutoff=np.max(abs(truth[reference]-query_truth[:,None]),axis=1)+1e-8
  for name,z in models.items():
   if z is None:
    t=time.perf_counter();idx=np.argsort(truth);build=time.perf_counter()-t;buffers=truth.nbytes+idx.nbytes
   else:
    t=time.perf_counter();tree=cKDTree(z[g].astype(float),leafsize=64);build=time.perf_counter()-t;buffers=sum(v.nbytes for v in tree.__getstate__() if isinstance(v,np.ndarray))
   for qn in (128,1024,4096):
    q=queries[:qn];t=time.perf_counter();neighbors=scalar_neighbors(truth,query_truth[:qn]) if z is None else tree.query(z[q].astype(float),k=10,workers=1)[1];elapsed=time.perf_counter()-t;error=abs(truth[neighbors]-query_truth[:qn,None]);results.append({'method':name,'gallery_fires':size,'queries':qn,'precision_at10_ties':float(np.mean(error<=cutoff[:qn,None])),'mean_retrieval_error_log1p_source_area':float(error.mean()),'index_build_seconds':build,'query_seconds':elapsed,'index_numeric_bytes':buffers,'scope':'observed-area task only; nested deterministic gallery and balanced nested test query subsets; no production extrapolation'})
   if z is not None:
    headpath=private/'raw-linear_ridge-1p0.npz' if name=='raw_state' else private/f'{name}-linear_ridge-1p0-head.npz';pred=decode(dict(np.load(headpath)),z)[:,0];t=time.perf_counter();order=np.argsort(pred[g]);buildhead=time.perf_counter()-t
    for qn in (128,1024,4096):
     q=queries[:qn];t=time.perf_counter();neighbors=scalar_neighbors(pred[g],pred[q]);elapsed=time.perf_counter()-t;error=abs(truth[neighbors]-query_truth[:qn,None]);results.append({'method':name+'-supervised_head','gallery_fires':size,'queries':qn,'precision_at10_ties':float(np.mean(error<=cutoff[:qn,None])),'mean_retrieval_error_log1p_source_area':float(error.mean()),'index_build_seconds':buildhead,'query_seconds':elapsed,'index_numeric_bytes':pred[g].nbytes+order.nbytes,'scope':'supervised scalar head, not zero-shot; observed-area controlled scaling only'})
  with (out/'retrieval-scaling.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
  print('COMPLETED GALLERY '+str(size),flush=True)
if __name__=='__main__':main()
