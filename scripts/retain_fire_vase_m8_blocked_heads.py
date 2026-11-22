"""Retain the deterministic blocked-refit preprocessing/heads and verify their scores."""
import argparse,csv,json
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import imputer_fit,probe_fit,forward
from dataset_prototype.embedding_study.observed_state import NAMES


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));y=ds['y'];mask=ds['mask'];reference=list(csv.DictReader((out/'blocked-generalization.csv').open()));checks=[]
 for split,(tr,te) in {'random':(ds['fold']=='train',ds['fold']=='test'),'temporal':((ds['year']>=2000)&(ds['year']<=2016),ds['year']>=2019),'geographic_west':((ds['region']!='west')&(ds['region']!='unknown'),ds['region']=='west')}.items():
  prep,x=imputer_fit(y,mask,tr);mu=np.array([y[tr&mask[:,j],j].mean() for j in range(10)]);sd=np.array([y[tr&mask[:,j],j].std() for j in range(10)]);sd[sd<1e-9]=1.;np.savez_compressed(private/f'blocked-{split}-preprocess.npz',**prep,target_mean=mu,target_scale=sd)
  models={'raw':x}
  if split!='random':
   for family in ('supervised','self_supervised','multitask'):models[family]=forward(dict(np.load(private/f'{family}-16-{split}.npz')),x)[1]
  for name,z in models.items():
   for nonlinear in (False,True):
    head,pred=probe_fit(z,y,mask,tr,nonlinear=nonlinear);probe='nonlinear' if nonlinear else 'linear';label=('raw_'+probe) if name=='raw' else name+('_nonlinear_probe' if nonlinear else '_linear_probe');np.savez_compressed(private/f'blocked-{split}-{name}-{probe}-head.npz',**{k:v for k,v in head.items() if v is not None})
    for j,prop in enumerate(NAMES):
     valid=te&mask[:,j];score=float(np.mean(((pred[valid,j]-y[valid,j])/sd[j])**2));expected=float(next(r['standardized_mse'] for r in reference if r['split']==split and r['stratum']=='all' and r['property']==prop and r['method']==label));assert np.isclose(score,expected,rtol=1e-10,atol=1e-12),(split,label,prop,score,expected)
    checks.append({'split':split,'method':label,'same_score':True})
 (out/'blocked-checkpoint-validation.json').write_text(json.dumps(checks,indent=2)+'\n');print('BLOCKED HEADS RETAINED AND REPRODUCED',flush=True)
if __name__=='__main__':main()
