"""Retain original-unit native scientific references and grade reconstruction in those units."""
import argparse,csv,json,math
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.population_profile import DAILY,DAILY_TABLE,readonly,supported_day
from dataset_prototype.embedding_study.observed_state import NAMES


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--lake',required=True);a=p.parse_args();out=Path(a.output);ds=dict(np.load(out/'private/observed-state.npz'));references=[];current=None;rows=[];identities=[]
 def flush():
  if not rows:return
  area=[r[1] for r in rows];days=[r[0] for r in rows];n=len(rows);total=math.fsum(area);r=np.full(10,np.nan);r[:4]=[total,n,area[0],area[-1]]
  if n>=2:
   r[4]=math.sqrt(math.fsum((v-total/n)**2 for v in area)/n)
   if total>0:r[5]=area[0]/total;r[8]=math.fsum(area[:n//2])/total
  diffs=[b-a for a,b,da,db in zip(area,area[1:],days,days[1:]) if db-da==1]
  if diffs:r[6]=float(np.mean(diffs))
  triples=[i for i in range(1,n-1) if days[i]-days[i-1]==1 and days[i+1]-days[i]==1]
  if triples:r[7]=sum(area[i]>area[i-1] and area[i]>area[i+1] for i in triples)
  r[9]=days[-1]-days[0];references.append(r);identities.append(str(current))
 with readonly(Path(a.lake)/DAILY) as source:
  for identity,day,value in source.execute('SELECT id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" ORDER BY id,date,fid'):
   if identity!=current:flush();current=identity;rows=[]
   rows.append((supported_day(day).toordinal(),value))
  flush()
 raw=np.asarray(references);assert np.array_equal(ds['ids'],identities) and np.array_equal(np.isfinite(raw),ds['mask']);transformed=raw.copy();transformed[:,[0,1,2,3,4,9]]=np.log1p(transformed[:,[0,1,2,3,4,9]]);transformed[:,6]=np.arcsinh(transformed[:,6]);assert np.allclose(transformed,ds['y'],equal_nan=True,atol=1e-12,rtol=1e-12)
 np.savez_compressed(out/'private/native-property-reference.npz',reference=raw,mask=ds['mask'])
 results=[]
 for path in sorted((out/'private').glob('*-test.npz')):
  label=path.name[:-len('-test.npz')];predfile=dict(np.load(path));idx=predfile['test_indices'];pred=predfile['prediction'].astype(float);pred[:,[0,1,2,3,4,9]]=np.expm1(pred[:,[0,1,2,3,4,9]]);pred[:,6]=np.sinh(pred[:,6])
  for stratum,subset in [('all',np.ones(len(idx),bool)),('one',ds['n'][idx]==1),('two',ds['n'][idx]==2),('three_plus',ds['n'][idx]>=3)]:
   for j,name in enumerate(NAMES):
    valid=subset&ds['mask'][idx,j];error=pred[valid,j]-raw[idx[valid],j];finite=np.isfinite(error)
    results.append({'method_probe':label,'stratum':stratum,'property':name,'eligible_fires':int(valid.sum()),'nonfinite_predictions':int((~finite).sum()),'mae_original_units':float(np.mean(abs(error[finite]))) if finite.any() else None,'rmse_original_units':float(np.sqrt(np.mean(error[finite]**2))) if finite.any() else None,'negative_predictions_for_nonnegative_property':int(np.sum(pred[valid,j]<0)) if j!=6 else None,'units':'source-reported km2' if j in (0,2,3,4,6) else 'days' if j==9 else 'dimensionless/count','scientific_scope':'approximate reconstruction, not exact preservation; no clipping'})
 with (out/'original-unit-reconstruction.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
 (out/'independent-reference-validation.json').write_text(json.dumps({'source_fire_ids':len(raw),'original_unit_reference_schema':NAMES,'transformed_reference_matches_training_labels':True,'tolerance':1e-12,'scope':'original raw-unit derived scientific properties; not a copied source daily-observation table','one_point_undefined_preserved':True,'no_prediction_clipping':True},indent=2)+'\n')
 print('ORIGINAL UNIT REFERENCES VERIFIED '+str(len(raw)),flush=True)
if __name__=='__main__':main()
