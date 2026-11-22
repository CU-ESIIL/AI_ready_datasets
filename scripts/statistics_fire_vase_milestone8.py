"""Fixed-family paired recovery comparisons, rank diagnostics and query post-stratification."""
import argparse,csv,itertools,json,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import forward
from dataset_prototype.embedding_study.observed_state import NAMES
from dataset_prototype.embedding_study.lake_design import holm_adjust
from evaluate_fire_vase_milestone8 import decode


def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));y=ds['y'];mask=ds['mask'];tr=ds['fold']=='train';te=ds['fold']=='test';idx=np.flatnonzero(te);scale=dict(np.load(private/'evaluation-scales.npz'))['scale'];x=(np.column_stack([np.where(mask,y,prep['median']),mask.astype(float)])-prep['mean'])/prep['scale'];ranks={}
 for label,use in [('all',tr),('one',tr&(ds['n']==1)),('two',tr&(ds['n']==2)),('three_plus',tr&(ds['n']>=3))]:ranks[label]=int(np.linalg.matrix_rank(np.cov(x[use],rowvar=False),tol=1e-10))
 (out/'rank-diagnostics.json').write_text(json.dumps({'model_input_columns':20,'training_covariance_ranks':ranks,'pca_effective_requested_dimensions':{str(d):min(d,ranks['all']) for d in (4,8,16,32,64)},'interpretation':'real support-mask channels and nonlinear scientific features; covariance rank is not intrinsic native degrees of freedom. One-point numerical state has rank1; two-point state additionally includes observed gap and nonlinear feature functions, so rank8 is not8 independent native observations.','no_sequence_zero_padding':True,'hidden_neural_width':16},indent=2)+'\n')
 strata=[];predictions={}
 methods=['raw_state']+[f'{family}-{d}' for d in (4,8,16,32,64) for family in ('supervised','self_supervised','multitask')]+['pca-request'+str(d) for d in (4,8,16,32,64)]
 for method in methods:
  if method=='raw_state':z=x;hp=private/'raw-linear_ridge-1p0.npz'
  else:
   hp=private/f'{method}-linear_ridge-1p0-head.npz'
   if method.startswith('pca'):component=np.load(private/f'pca-{method[len("pca-request"):]}-1p0.npz')['components'];z=x@component
   else:params=dict(np.load(private/f'{method}-1p0.npz'));_,z,_=forward(params,x)
  pred=decode(dict(np.load(hp)),z)[te];predictions[method]=pred;np.savez_compressed(private/f'paired-{method}-fullprecision.npz',prediction=pred,test_indices=idx)
  errors=((pred-y[te])/scale)**2
  for dimension in ('region','year'):
   labels=ds[dimension][te]
   for group in sorted(set(labels.tolist()),key=str):
    use=labels==group
    for j,name in enumerate(NAMES):
     valid=use&mask[te,j];v=errors[valid,j]
     strata.append({'method':method,'dimension':dimension,'stratum':str(group),'property':name,'eligible_test_fires':int(valid.sum()),'mse':float(v.mean()) if len(v) else None,'scope':'primary random-split stratification, not a held-out-region/year refit'})
 csvwrite(out/'geographic-temporal-strata.csv',strata)
 rng=np.random.default_rng(20260828);comparisons=[]
 for d in (4,8,16,32,64):
  a=predictions['self_supervised-'+str(d)];b=predictions['supervised-'+str(d)]
  for j,name in enumerate(NAMES):
   valid=mask[te,j];delta=((a[valid,j]-y[te][valid,j])/scale[j])**2-((b[valid,j]-y[te][valid,j])/scale[j])**2;regions=ds['region'][te][valid];labels=sorted(set(regions.tolist())-{'unknown'});sums=np.array([delta[regions==g].sum() for g in labels]);counts=np.array([np.sum(regions==g) for g in labels]);known_effect=float(sums.sum()/counts.sum());null=np.array([np.dot(sums,signs)/counts.sum() for signs in itertools.product((-1,1),repeat=len(labels))]);pval=float(np.mean(abs(null)>=abs(known_effect)-1e-14));bootstrap=np.array([delta[rng.integers(0,len(delta),len(delta))].mean() for _ in range(256)]);region_draws=rng.integers(0,len(labels),(256,len(labels)));region_boot=sums[region_draws].sum(1)/counts[region_draws].sum(1)
   comparisons.append({'dimension':d,'property':name,'test_fires':len(delta),'effect_ssl_minus_count_supervised':float(delta.mean()),'conditional_fire_ci_low':float(np.quantile(bootstrap,.025)),'conditional_fire_ci_high':float(np.quantile(bootstrap,.975)),'known_region_effect':known_effect,'region_clusters':len(labels),'region_bootstrap_low':float(np.quantile(region_boot,.025)),'region_bootstrap_high':float(np.quantile(region_boot,.975)),'exact_region_signflip_p':pval,'inferential_scope':'conditional fitted-model diagnostics, coarse source regions; no training-refit or general ecological population claim'})
 adjusted=holm_adjust([r['exact_region_signflip_p'] for r in comparisons])
 for r,pval in zip(comparisons,adjusted):r['holm_adjusted_50_family_p']=pval
 csvwrite(out/'paired-statistical-comparisons.csv',comparisons)
 # Balanced query sampling is not the native population's mixture: retain both.
 retrieval=list(csv.DictReader((out/'retrieval-results.csv').open()));weighted=[]
 for method,route,prop in sorted({(r['method'],r['route'],r['property']) for r in retrieval}):
  j=NAMES.index(prop);parts=[r for r in retrieval if r['method']==method and r['route']==route and r['property']==prop and r['stratum']!='all'];weights=[]
  for r in parts:
   use=te&mask[:,j]&(ds['n']==1 if r['stratum']=='one' else ds['n']==2 if r['stratum']=='two' else ds['n']>=3);weights.append(int(use.sum()))
  total=sum(weights)
  row={'method':method,'route':route,'property':prop,'estimand':'post-stratified to eligible native test-fire1/2/3+ composition','eligible_test_fires':total,'sampled_queries':sum(int(r['queries']) for r in parts)}
  for metric in ('precision_at10','recall_at10_all_cutoff_ties','reference_top10_overlap','mean_retrieval_error'):row[metric]=sum(w*float(r[metric]) for w,r in zip(weights,parts))/total
  weighted.append(row)
 csvwrite(out/'retrieval-population-weighted.csv',weighted)
 # Coordinate-retrieval uncertainty uses the actual stratified query units.
 retrieval_ci=[]
 for path in sorted(private.glob('retrieval-*-errors.npz')):
  v=dict(np.load(path));q=v['query_indices'];precision=v['precision'];property_index=int(path.stem.rsplit('-',2)[1]);j=property_index;test_eligible=te&mask[:,j];population_count=int(test_eligible.sum());groups=[]
  for label,select in [('one',ds['n'][q]==1),('two',ds['n'][q]==2),('three_plus',ds['n'][q]>=3)]:
   if not select.any():continue
   popmask=ds['n']==1 if label=='one' else ds['n']==2 if label=='two' else ds['n']>=3;weight=np.sum(test_eligible&popmask)/population_count;groups.append((precision[select],weight))
  boot=np.zeros(256)
  for values,weight in groups:
   for k in range(256):boot[k]+=weight*values[rng.integers(0,len(values),len(values))].mean()
  retrieval_ci.append({'artifact':path.name,'property':NAMES[j],'queries':len(q),'population_weighted_precision':float(sum(v.mean()*w for v,w in groups)),'conditional_stratified_query_ci_low':float(np.quantile(boot,.025)),'conditional_stratified_query_ci_high':float(np.quantile(boot,.975)),'scope':'finite query diagnostic conditional on fitted models/gallery; spatial/year dependence and refitting not estimated'})
 csvwrite(out/'retrieval-uncertainty.csv',retrieval_ci)
 # Secondary paired forecast comparison is descriptive and separately labeled.
 forecast=[]
 for depth in (1,2):
  for h in (1,3,7):
   baseline=dict(np.load(private/f'prediction-{depth}-{h}-raw_state-linear.npz'))
   for family in ('supervised','self_supervised','multitask'):
    candidate=dict(np.load(private/f'prediction-{depth}-{h}-{family}-16-linear.npz'));assert np.array_equal(baseline['fire_indices'],candidate['fire_indices']);diff=candidate['per_fire_error']-baseline['per_fire_error'];boot=np.array([diff[rng.integers(0,len(diff),len(diff))].mean() for _ in range(256)])
    forecast.append({'depth':depth,'horizon':h,'method':family+'16-linear','test_fires':len(diff),'effect_vs_raw_linear':float(diff.mean()),'conditional_fire_ci_low':float(np.quantile(boot,.025)),'conditional_fire_ci_high':float(np.quantile(boot,.975)),'scope':'secondary fixed-model, random whole-fire split; extra observed-state pretraining and single-seed uncertainty not controlled by this bootstrap'})
 csvwrite(out/'secondary-prediction-paired.csv',forecast)
 print('STATISTICS COMPLETE',flush=True)
if __name__=='__main__':main()
