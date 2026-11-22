"""Independent finite/mask/cohort/checkpoint and immutable-source M8 postflight."""
import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.observed_state import NAMES


def read(path):
 with path.open() as f:return list(csv.DictReader(f))


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--lake',required=True);p.add_argument('--census',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz',allow_pickle=False));assert len(ds['ids'])==278865 and len(set(ds['ids']))==278865;assert int(ds['n'].sum())==627033;assert [int((ds['n']==k).sum()) for k in (1,2)]==[161200,47992];assert int((ds['n']>=3).sum())==69673;assert not ds['mask'][ds['n']==1,4:9].any();assert np.isfinite(ds['y'][ds['mask']]).all();assert np.isnan(ds['y'][~ds['mask']]).all()
 for r in read(out/'information-preservation.csv'):
  use=ds['fold']=='test';n=ds['n'];use &= np.ones(len(n),bool) if r['stratum']=='all' else n==1 if r['stratum']=='one' else n==2 if r['stratum']=='two' else n>=3;j=NAMES.index(r['property']);assert int(r['eligible_test_fires'])==int((use&ds['mask'][:,j]).sum());assert bool(r['mse'])==bool(int(r['eligible_test_fires']));assert not r['mse'] or np.isfinite(float(r['mse']))
 checkpoints=[]
 for path in sorted(private.glob('*.npz')):
  with np.load(path,allow_pickle=False) as f:
   if set(f.files)!={'w','b','v','c','o','a'}:continue
   q=dict(f)
  assert all(np.isfinite(v).all() for v in q.values());assert q['w'].shape==(20,16);d=q['v'].shape[1];assert q['v'].shape==(16,d) and q['o'].shape[0]==d
  checkpoints.append({'path':path.relative_to(out).as_posix(),'dimension':d,'encoder_parameters':sum(q[k].size for k in ('w','b','v','c')),'objective_head_parameters':q['o'].size+q['a'].size,'total_parameters':sum(v.size for v in q.values())})
 assert len(checkpoints)==96,len(checkpoints)
 primary=[p for p in private.glob('*-training.json') if not p.name.startswith(('blocked','forecast','update','direct'))];assert len(primary)==75,len(primary)
 configs=[json.loads(p.read_text()) for p in primary];assert {(r['family'],r['dimension'],r['fraction']) for r in configs}=={(f,d,t) for f in ('supervised','self_supervised','multitask') for d in (4,8,16,32,64) for t in (.01,.03,.1,.3,1.)}
 for ref in private.glob('retrieval-reference-*.npz'):
  q=dict(np.load(ref,allow_pickle=False));gi=q['gallery_indices'];qi=q['query_indices'];assert np.all(ds['fold'][gi]=='train') and np.all(ds['fold'][qi]=='test');assert not set(ds['ids'][gi])&set(ds['ids'][qi])
 for pred in private.glob('prediction-*.npz'):
  q=dict(np.load(pred,allow_pickle=False));assert np.all(ds['fold'][q['fire_indices']]=='test');assert np.isfinite(q['per_fire_error']).all()
 for r in read(out/'original-unit-reconstruction.csv'):assert int(r['nonfinite_predictions'])==0
 comparisons=read(out/'paired-statistical-comparisons.csv');assert len(comparisons)==50;assert all(float(r['holm_adjusted_50_family_p'])==1 for r in comparisons)
 expected={(1,1):(75953,196982),(1,3):(19004,61342),(1,7):(3386,16547),(2,1):(34911,101035),(2,3):(11195,40724),(2,7):(2452,13072)}
 cohort=read(out.parent/'full-population-v1/short-prefix-eligibility.csv');assert {(int(r['input_depth']),int(r['future_horizon'])):(int(r['eligible_fires']),int(r['dependent_windows'])) for r in cohort}==expected
 sources=[]
 for v in json.loads((Path(a.census)/'source-verification.json').read_text()):
  path=Path(a.lake)/v['relative_path'];stat=path.stat();assert (stat.st_size,stat.st_mtime_ns)==(v['bytes'],v['mtime_ns']);h=hashlib.sha256()
  with path.open('rb') as f:
   for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
  assert h.hexdigest()==v['sha256'];sources.append({'relative_path':v['relative_path'],'sha256':h.hexdigest(),'bytes':stat.st_size,'unchanged':True})
 (out/'checkpoint-inventory.json').write_text(json.dumps(checkpoints,indent=2)+'\n');(out/'validation/postflight.json').write_text(json.dumps({'status':'PASS_DETERMINISTIC_IMPLEMENTATION_CHECKS','scientific_approval':False,'native_ids':len(ds['ids']),'daily_rows':int(ds['n'].sum()),'neural_parameter_checkpoints':len(checkpoints),'primary_fits':len(primary),'masked_eligibility_rows_validated':len(read(out/'information-preservation.csv')),'source_postflight':sources,'prediction_count_reference':{f'{k[0]}-{k[1]}':v for k,v in expected.items()},'scope':'implementation, artifact and source integrity; not measurement QA or independent ecological validity'},indent=2)+'\n');print('M8 POSTFLIGHT PASS')
if __name__=='__main__':main()
