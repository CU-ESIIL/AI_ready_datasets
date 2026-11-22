"""Critical real short-history normalization controls, separate from learned encoders."""
import argparse,csv,json
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.utility_learning import probe_fit


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);ds=dict(np.load(out/'private/observed-state.npz'));raw=np.load(out/'private/native-property-reference.npz')['reference'];scale=np.load(out/'private/evaluation-scales.npz')['scale'];results=[];collision=[]
 for n in (1,2):
  eligible=np.flatnonzero(ds['n']==n);train=ds['fold'][eligible]=='train';test=ds['fold'][eligible]=='test';areas=raw[eligible,2:3] if n==1 else raw[eligible][:,[2,3]];shape=areas/areas.sum(1)[:,None];y=ds['y'][eligible];mask=ds['mask'][eligible]
  if n==1:assert np.all(shape==1.)
  for nonlinear in (False,True):
   head,pred=probe_fit(shape,y,mask,train,nonlinear=nonlinear)
   for j in (0,2,3,4,5,6,8):
    valid=test&mask[:,j];error=(pred[valid,j]-y[valid,j])/scale[j]
    results.append({'stratum_observations':n,'probe':'nonlinear_tanh32' if nonlinear else 'linear','property_index':j,'eligible_test_fires':int(valid.sum()),'standardized_mse':float(np.mean(error**2)) if len(error) else None,'scope':'normalized allocation only, no scientific scale in metadata or source fallback; not ecological shape validation'})
  groups={}
  for i,row in enumerate(shape):
   key=tuple(row.tolist());total=raw[eligible[i],0]
   if key not in groups:groups[key]=[1,total,total]
   else:g=groups[key];g[0]+=1;g[1]=min(g[1],total);g[2]=max(g[2],total)
  collided=[g for g in groups.values() if g[0]>1 and g[2]-g[1]>1e-9]
  collision.append({'observations':n,'fire_ids':len(eligible),'distinct_float64_allocation_payloads':len(groups),'payload_groups_with_different_absolute_totals':len(collided),'fires_in_those_groups':sum(g[0] for g in collided),'interpretation':'actual payload collisions; retained source IDs can still enable an explicitly charged lookup'})
 with (out/'normalization-controls.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
 (out/'normalization-collisions.json').write_text(json.dumps(collision,indent=2)+'\n');print(json.dumps(collision,indent=2))
if __name__=='__main__':main()
