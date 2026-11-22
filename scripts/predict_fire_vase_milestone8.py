"""Real short-prefix forecast extension, separate from all-fire observed-property tasks."""
import argparse,csv,json,sqlite3,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.observed_state import prediction_examples
from dataset_prototype.embedding_study.population_profile import DAILY,DAILY_TABLE,readonly,supported_day
from dataset_prototype.embedding_study.utility_learning import train,forward,probe_fit,imputer_fit


def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--lake',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));mapping={v:i for i,v in enumerate(ds['ids'])};buckets={(d,h):{'state':[],'mask':[],'target':[],'persistence':[],'fire':[]} for d in (1,2) for h in (1,3,7)};current=None;buffer=[]
 t=time.perf_counter()
 def flush():
  if not buffer:return
  areas=[r[1] for r in buffer];days=[r[0] for r in buffer];parent=mapping[str(current)]
  for (d,h),b in buckets.items():
   for start,state,mask,target,persistence in prediction_examples(areas,days,d,h):b['state'].append(state);b['mask'].append(mask);b['target'].append(target);b['persistence'].append(persistence);b['fire'].append(parent)
 with readonly(Path(a.lake)/DAILY) as source:
  for identity,day,area in source.execute('SELECT id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" ORDER BY id,date,fid'):
   if identity!=current:flush();current=identity;buffer=[]
   buffer.append((supported_day(day).toordinal(),area))
  flush()
 extraction=time.perf_counter()-t;results=[];runtime=[];prep=dict(np.load(private/'preprocess-1p0.npz'));expected={(1,1):(75953,196982),(1,3):(19004,61342),(1,7):(3386,16547),(2,1):(34911,101035),(2,3):(11195,40724),(2,7):(2452,13072)}
 for (depth,horizon),b in buckets.items():
  y=np.asarray(b['state']);mask=np.asarray(b['mask']);target=np.asarray(b['target'])[:,None];fire=np.asarray(b['fire']);assert (len(set(fire)),len(fire))==expected[(depth,horizon)];tr=ds['fold'][fire]=='train';te=ds['fold'][fire]=='test';prefix_prep,x=imputer_fit(y,mask,tr);frozen_x=(np.column_stack([np.where(mask,y,prep['median']),mask.astype(float)])-prep['mean'])/prep['scale'];candidates={'raw_state':x}
  for dim in (4,8,16,32,64):
   pca=dict(np.load(private/f'pca-{dim}-1p0.npz'));candidates['pca-request'+str(dim)]=frozen_x@pca['components']
   for family in ('supervised','self_supervised','multitask'):
    params=dict(np.load(private/f'{family}-{dim}-1p0.npz'));_,z,_=forward(params,frozen_x);candidates[family+'-'+str(dim)]=z
  def evaluate(label,pred):
   idx=np.flatnonzero(te);unique,inverse=np.unique(fire[idx],return_inverse=True);errors=(pred[idx,0]-target[idx,0])**2;perfire=np.bincount(inverse,weights=errors)/np.bincount(inverse)
   for stratum,use in [('all',np.ones(len(unique),bool)),('two',ds['n'][unique]==2),('three_plus',ds['n'][unique]>=3)]:
    if not use.any():continue
    results.append({'input_depth':depth,'horizon':horizon,'method':label,'parent_history_stratum':stratum,'test_fires':int(use.sum()),'dependent_test_windows':int(np.sum(np.isin(fire[idx],unique[use]))),'fire_mean_log_growth_mse':float(perfire[use].mean()),'negative_log_growth_prediction_windows':int(np.sum((pred[idx,0]<0)&np.isin(fire[idx],unique[use]))),'scope':'retrospective selected-cohort; no operational availability claim; predictions not clipped'})
   np.savez_compressed(private/f'prediction-{depth}-{horizon}-{label}.npz',fire_indices=unique,per_fire_error=perfire)
  evaluate('last_increment_persistence',np.asarray(b['persistence'])[:,None]);evaluate('training_mean',np.full_like(target,target[tr].mean()))
  for label,z in candidates.items():
   for nonlinear in (False,True):
    start=time.perf_counter();head,pred=probe_fit(z,target,np.ones_like(target,bool),tr,nonlinear=nonlinear);name=label+('-nonlinear' if nonlinear else '-linear');evaluate(name,pred);runtime.append({'depth':depth,'horizon':horizon,'method':name,'head_fit_and_predict_seconds':time.perf_counter()-start});np.savez_compressed(private/f'forecast-head-{depth}-{horizon}-{name}.npz',**{k:v for k,v in head.items() if v is not None})
  mu=target[tr].mean();sd=target[tr].std();np.savez_compressed(private/f'forecast-preprocess-{depth}-{horizon}.npz',**prefix_prep,target_mean=mu,target_scale=sd);start=time.perf_counter();params,curve=train(x[tr],(target[tr]-mu)/max(sd,1e-8),np.ones_like(target[tr],bool),16,epochs=12);pred,_,_=forward(params,x);evaluate('direct_neural',pred*sd+mu);np.savez_compressed(private/f'direct-forecast-{depth}-{horizon}.npz',**params);runtime.append({'depth':depth,'horizon':horizon,'method':'direct_neural','fit_predict_seconds':time.perf_counter()-start,'parameters':sum(v.size for v in params.values()),'loss_curve':curve})
  csvwrite(out/'secondary-prediction.csv',results);(out/'secondary-prediction-runtime.json').write_text(json.dumps({'prefix_construction_seconds':extraction,'methods':runtime},indent=2)+'\n');print('PREDICTION COMPLETE '+str((depth,horizon)),flush=True)
if __name__=='__main__':main()
