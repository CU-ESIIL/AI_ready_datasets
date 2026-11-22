"""Prespecified temporal/geographic refits and direct neural raw-state controls."""
import argparse,csv,json,time
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import train,forward,imputer_fit,probe_fit
from dataset_prototype.embedding_study.observed_state import NAMES
from dataset_prototype.embedding_study.lake_design import learning_fraction


def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));y=ds['y'];mask=ds['mask'];rows=[];times=[]
 splits={'random':(ds['fold']=='train',ds['fold']=='test'),'temporal':((ds['year']>=2000)&(ds['year']<=2016),ds['year']>=2019),'geographic_west':((ds['region']!='west')&(ds['region']!='unknown'),ds['region']=='west')}
 for split,(tr,te) in splits.items():
  prep,x=imputer_fit(y,mask,tr);mu=np.array([y[tr&mask[:,j],j].mean() for j in range(y.shape[1])]);sd=np.array([y[tr&mask[:,j],j].std() for j in range(y.shape[1])]);sd[sd<1e-9]=1.;target=(y-mu)/sd
  def evaluate(label,pred):
   for stratum,use in [('all',te),('one',te&(ds['n']==1)),('two',te&(ds['n']==2)),('three_plus',te&(ds['n']>=3))]:
    for j,name in enumerate(NAMES):
     eligible=use&mask[:,j];err=(pred[eligible,j]-y[eligible,j])/sd[j]
     rows.append({'split':split,'method':label,'stratum':stratum,'property':name,'test_fires':int(eligible.sum()),'standardized_mse':float(np.mean(err**2)) if len(err) else None,'training_fires':int(tr.sum())})
  for nonlinear in (False,True):
   head,pred=probe_fit(x,y,mask,tr,nonlinear=nonlinear);evaluate('raw_nonlinear' if nonlinear else 'raw_linear',pred)
  # Direct neural model receives the same observed state and ALL downstream labels.
  # Compare as a matched downstream-information control, not a zero-shot arm.
  t=time.perf_counter();params,curve=train(x[tr],target[tr],mask[tr],16,epochs=12);pred,z,_=forward(params,x);evaluate('direct_neural_all_properties',pred*sd+mu);np.savez_compressed(private/f'direct-neural-{split}.npz',**params);times.append({'split':split,'method':'direct_neural_all_properties','seconds':time.perf_counter()-t,'parameters':sum(v.size for v in params.values()),'loss_curve':curve})
  if split=='random':continue
  # Fixed16-dimensional generalization refits, selected by the plan rather than scores.
  for family,cols in [('supervised',[1]),('self_supervised',None),('multitask',[0,1,4])]:
   yy=x if cols is None else target[:,cols];mm=np.ones_like(x,dtype=bool) if cols is None else mask[:,cols];t=time.perf_counter();params,curve=train(x[tr],yy[tr],mm[tr],16,epochs=12);_,z,_=forward(params,x);np.savez_compressed(private/f'{family}-16-{split}.npz',**params)
   for nonlinear in (False,True):
    head,pred=probe_fit(z,y,mask,tr,nonlinear=nonlinear);evaluate(family+('_nonlinear_probe' if nonlinear else '_linear_probe'),pred)
   times.append({'split':split,'method':family+'16','seconds':time.perf_counter()-t,'parameters':sum(v.size for v in params.values()),'loss_curve':curve})
  csvwrite(out/'blocked-generalization.csv',rows);(out/'blocked-fit-runtime.json').write_text(json.dumps(times,indent=2)+'\n');print('COMPLETED GENERALIZATION '+split,flush=True)
 csvwrite(out/'blocked-generalization.csv',rows);(out/'blocked-fit-runtime.json').write_text(json.dumps(times,indent=2)+'\n')
if __name__=='__main__':main()
