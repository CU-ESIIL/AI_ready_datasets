"""Explicit metadata/native access and deterministic PCA inverse retrieval, no hidden lookup."""
import argparse,csv,json,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.observed_state import NAMES
from evaluate_fire_vase_milestone8 import scalar_neighbors


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));x=(np.column_stack([np.where(ds['mask'],ds['y'],prep['median']),ds['mask'].astype(float)])-prep['mean'])/prep['scale'];rows=list(csv.DictReader((out/'retrieval-results.csv').open()));all_rows=[r for r in rows if r['stratum']=='all'];exact={r['property']:r for r in all_rows if r['method']=='cached_native'};access=[]
 for row in rows:
  for condition in ('A','B','C'):
   r=dict(row);r['condition']=condition;r['native_fallback']=condition=='C' and row['method'] not in ('cached_native','interpretable_exact');r['information_source']='coordinates/declared supervised decoder' if row['method'] not in ('cached_native','interpretable_exact') else 'native property operations'
   if condition=='C' or condition=='B' and row['property']=='log_observed_span':
    ref=next(v for v in rows if v['method']=='cached_native' and v['stratum']==row['stratum'] and v['property']==row['property'])
    for name in ('precision_at10','recall_at10_all_cutoff_ties','reference_top10_overlap','exact_reference_set_fraction','mean_retrieval_error'):r[name]=ref[name]
    r['information_source']='native cached-property-index fallback (not coordinate preservation)' if condition=='C' else 'original date sidecar operation and index (not coordinate preservation)'
   access.append(r)
 with (out/'retrieval-access-conditions.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(access[0]));w.writeheader();w.writerows(access)
 # Verify the sidecar's span index using only original dates and offsets.
 offsets=ds['offsets'];span=np.log1p(ds['date_ordinals'][offsets[1:]-1]-ds['date_ordinals'][offsets[:-1]]);assert np.allclose(span,ds['y'][:,9],atol=1e-14,rtol=0)
 pcainverse=[]
 for d in (4,8,16,32,64):
  component=np.load(private/f'pca-{d}-1p0.npz')['components'];back=(x@component@component.T)*prep['scale']+prep['mean']
  for j in (0,4,5,6,9):
   ref=dict(np.load(private/f'retrieval-reference-{j}.npz'));gi=ref['gallery_indices'];qi=ref['query_indices'];t=time.perf_counter();order=np.argsort(back[gi,j]);index_time=time.perf_counter()-t;t=time.perf_counter();neighbors=scalar_neighbors(back[gi,j],back[qi,j]);query_time=time.perf_counter()-t;dist=abs(ds['y'][gi[neighbors],j]-ds['y'][qi,j,None]);scale=np.load(private/'evaluation-scales.npz')['scale'][j];relevant=dist<=ref['threshold'][:,None]*scale
   pcainverse.append({'requested_dimension':d,'effective_rank':component.shape[1],'property':NAMES[j],'queries':len(qi),'gallery':len(gi),'precision_at10':float(relevant.mean()),'recall_at10_all_ties':float(np.mean(relevant.sum(1)/ref['relevant_count'])),'retrieval_error_original_transformed_scale':float(dist.mean()),'index_seconds':index_time,'query_seconds':query_time,'scope':'deterministic PCA inverse, no supervised head labels; no ecological validity claim'})
 with (out/'pca-inverse-retrieval.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(pcainverse[0]));w.writeheader();w.writerows(pcainverse)
 # Access-cost trace is measured rather than inventing filesystem bytes.
 costs=[]
 for j in (0,4,5,6,9):
  ref=dict(np.load(private/f'retrieval-reference-{j}.npz'));gi=ref['gallery_indices'];qi=ref['query_indices'];scale=np.load(private/'evaluation-scales.npz')['scale'][j];t=time.perf_counter();g=ds['y'][gi,j].copy()/scale;q=ds['y'][qi,j].copy()/scale;payload_copy=time.perf_counter()-t;t=time.perf_counter();idx=scalar_neighbors(g,q);elapsed=time.perf_counter()-t;assert np.array_equal(idx,ref['reference']);costs.append({'property':NAMES[j],'query_fires':len(qi),'gallery_fires':len(gi),'native_operation':'cached-native-observed-property-index','native_gallery_and_query_value_bytes_copied':g.nbytes+q.nbytes,'query_scalar_value_bytes':q.nbytes,'filesystem_physical_bytes_read':None,'payload_copy_seconds':payload_copy,'native_rank_query_seconds':elapsed,'exact_reference_recovered':True,'scope':'conditionC shared index fallback after native preparation; not embedding-preserved scientific values'})
 (out/'retrieval-fallback-costs.json').write_text(json.dumps(costs,indent=2)+'\n')
 print('RETRIEVAL ACCESS AND PCA INVERSE COMPLETE',flush=True)
if __name__=='__main__':main()
