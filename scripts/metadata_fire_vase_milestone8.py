"""ConditionB recovery with genuine date/support metadata, never native area in sidecars."""
import argparse,csv,json,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import forward,probe_fit,imputer_fit
from dataset_prototype.embedding_study.observed_state import NAMES
from evaluate_fire_vase_milestone8 import scalar_neighbors


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));prep=dict(np.load(private/'preprocess-1p0.npz'));tr=ds['fold']=='train';te=ds['fold']=='test';y=ds['y'];mask=ds['mask'];x=(np.column_stack([np.where(mask,y,prep['median']),mask.astype(float)])-prep['mean'])/prep['scale'];scale=np.load(private/'evaluation-scales.npz')['scale'];offsets=ds['offsets'];dates=ds['date_ordinals'];n=np.diff(offsets);span=dates[offsets[1:]-1]-dates[offsets[:-1]];maxgap=np.full(len(n),np.nan)
 for i in np.flatnonzero(n>1):maxgap[i]=np.diff(dates[offsets[i]:offsets[i+1]]).max()
 metadata=np.column_stack([np.log1p(n),dates[offsets[:-1]],np.log1p(span),np.log1p(maxgap)]);metadata_mask=np.isfinite(metadata);metadata_prep,metadata_x=imputer_fit(metadata,metadata_mask,tr);np.savez_compressed(private/'metadataB-preprocessing.npz',**metadata_prep);models={'raw_state':x};results=[];retrieval=[];times=[]
 for d in (4,8,16,32,64):
  models['pca-request'+str(d)]=x@np.load(private/f'pca-{d}-1p0.npz')['components']
  for family in ('supervised','self_supervised','multitask'):models[family+'-'+str(d)]=np.load(private/f'{family}-{d}-materialized.npz')['z']
 for label,z in models.items():
  augmented=np.column_stack([z,metadata_x])
  for nonlinear in (False,True):
   t=time.perf_counter();head,pred=probe_fit(augmented,y,mask,tr,nonlinear=nonlinear);elapsed=time.perf_counter()-t;probe='nonlinear_tanh32' if nonlinear else 'linear';pred[:,1]=metadata[:,0];pred[:,9]=metadata[:,2];times.append({'method':label,'probe':probe,'fit_predict_seconds':elapsed});np.savez_compressed(private/f'metadataB-{label}-{probe}-head.npz',**{k:v for k,v in head.items() if v is not None})
   for stratum,use in [('all',te),('one',te&(ds['n']==1)),('two',te&(ds['n']==2)),('three_plus',te&(ds['n']>=3))]:
    for j,name in enumerate(NAMES):
     valid=use&mask[:,j];error=(pred[valid,j]-y[valid,j])/scale[j]
     results.append({'condition':'B','method':label,'probe':probe,'stratum':stratum,'property':name,'eligible_test_fires':int(valid.sum()),'mse':float(np.mean(error**2)) if len(error) else None,'scope':'coordinate plus common original-date/support metadata; exact count/span routing, other fields supervised recovery'})
   for j in (0,4,5,6,9):
    ref=dict(np.load(private/f'retrieval-reference-{j}.npz'));g=ref['gallery_indices'];q=ref['query_indices'];t=time.perf_counter();idx=scalar_neighbors(pred[g,j]/scale[j],pred[q,j]/scale[j]);query_time=time.perf_counter()-t;dist=abs(y[g[idx],j]-y[q,j,None])/scale[j];relevant=dist<=ref['threshold'][:,None]
    for stratum,use in [('all',np.ones(len(q),bool)),('one',ds['n'][q]==1),('two',ds['n'][q]==2),('three_plus',ds['n'][q]>=3)]:
     if not use.any():continue
     retrieval.append({'condition':'B','method':label,'probe':probe,'property':NAMES[j],'stratum':stratum,'queries':int(use.sum()),'gallery':len(g),'precision_at10':float(relevant[use].mean()),'recall_at10_all_cutoff_ties':float(np.mean(relevant[use].sum(1)/ref['relevant_count'][use])),'mean_retrieval_error':float(dist[use].mean()),'query_seconds':query_time,'scope':'supervised metadata-augmented scalar ranking; not zero-shot ecological retrieval'})
  print('METADATA COMPLETE '+label,flush=True)
 for name,rows in [('metadataB-recovery.csv',results),('metadataB-retrieval.csv',retrieval)]:
  with (out/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'metadataB-runtime.json').write_text(json.dumps({'allowed_metadata_fields':['original record count from offsets','first observation date ordinal','elapsed observed span','maximum original inter-record gap (undefined for1 observation)'],'no_native_area_or_property_values_in_metadata':True,'preprocessing':'training-only model imputation with support bits; no source gaps filled','model_scope':'additional declared-access consumer sensitivity, not semantic-prose metadata efficacy','fit_predict':times},indent=2)+'\n')
if __name__=='__main__':main()
