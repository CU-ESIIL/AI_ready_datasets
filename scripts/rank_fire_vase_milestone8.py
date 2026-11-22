"""Rank correlations over all eligible sampled queries, with a fixed hash-selected gallery."""
import argparse,csv,hashlib,time
from pathlib import Path
import numpy as np
from scipy.stats import rankdata
from evaluate_fire_vase_milestone8 import decode


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));x=(np.column_stack([np.where(ds['mask'],ds['y'],prep['median']),ds['mask'].astype(float)])-prep['mean'])/prep['scale'];queries=np.load(private/'retrieval-query-indices.npz')['indices'];models={'raw_state':x};result=[];rng=np.random.default_rng(20260828)
 for d in (4,8,16,32,64):
  models['pca-request'+str(d)]=x@np.load(private/f'pca-{d}-1p0.npz')['components']
  for family in ('supervised','self_supervised','multitask'):models[family+'-'+str(d)]=np.load(private/f'{family}-{d}-materialized.npz')['z']
 for j in (0,4,5,6,9):
  gallery=np.flatnonzero((ds['fold']=='train')&ds['mask'][:,j]);g=np.array(sorted(gallery,key=lambda i:hashlib.sha256(('m8-rank-gallery:'+str(ds['ids'][i])).encode()).digest())[:1024]);q=queries[ds['mask'][queries,j]];true_distance=abs(ds['y'][q,j,None]-ds['y'][g,j][None,:]);rtrue=rankdata(true_distance,axis=1);rtrue-=rtrue.mean(1)[:,None];true_norm=np.sqrt((rtrue*rtrue).sum(1))
  for label,z in models.items():
   for route in ('coordinates','supervised_linear'):
    if route=='coordinates':gg=np.asarray(z[g],float);qq=np.asarray(z[q],float);distance=(qq*qq).sum(1)[:,None]+(gg*gg).sum(1)[None,:]-2*qq@gg.T
    else:
     hp=private/'raw-linear_ridge-1p0.npz' if label=='raw_state' else private/f'{label}-linear_ridge-1p0-head.npz';v=decode(dict(np.load(hp)),z)[:,j];distance=abs(v[q,None]-v[g][None,:])
    ranks=rankdata(distance,axis=1);ranks-=ranks.mean(1)[:,None];den=np.sqrt((ranks*ranks).sum(1))*true_norm;correlation=np.divide((ranks*rtrue).sum(1),den,out=np.full(len(q),np.nan),where=den>0)
    for stratum,use in [('all',np.ones(len(q),bool)),('one',ds['n'][q]==1),('two',ds['n'][q]==2),('three_plus',ds['n'][q]>=3)]:
     values=correlation[use];values=values[np.isfinite(values)]
     if not len(values):continue
     boot=np.array([values[rng.integers(0,len(values),len(values))].mean() for _ in range(256)])
     result.append({'method':label,'route':route,'property_index':j,'stratum':stratum,'queries':len(values),'diagnostic_gallery_fires':len(g),'mean_spearman_rank_correlation':float(values.mean()),'conditional_query_ci_low':float(np.quantile(boot,.025)),'conditional_query_ci_high':float(np.quantile(boot,.975)),'scope':'all eligible queries in fixed4096 stratified query sample; independent hash1024 training gallery, not full-gallery correlation or ecological validity'})
   print('RANK '+label+' '+str(j),flush=True)
  with (out/'rank-correlation-results.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
 # Remove the superseded first128/first4096 convenience diagnostic from main
 # stratum rows rather than repeating a pooled statistic as stratum-specific.
 path=out/'retrieval-results.csv';rows=list(csv.DictReader(path.open()))
 for row in rows:row['rank_correlation_diagnostic']=''
 with path.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print('RANK STUDY COMPLETE',flush=True)
if __name__=='__main__':main()
