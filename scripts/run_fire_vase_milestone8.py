"""Execute real full-population observed-state representation experiment, no raw persistence."""
import argparse,csv,hashlib,json,math,os,resource,sqlite3,time,inspect,sys
from pathlib import Path
from datetime import date,datetime,timezone
import numpy as np
from dataset_prototype.embedding_study.population_profile import DAILY,DAILY_TABLE,readonly,supported_day
from dataset_prototype.embedding_study.observed_state import calculate,NAMES
from dataset_prototype.embedding_study.utility_learning import train,forward,imputer_fit,probe_fit,initialize,loss_gradient
from dataset_prototype.embedding_study.lake_design import learning_fraction


def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def csvwrite(p,rows):
 with p.open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def features(census,lake,out):
 path=out/'private/observed-state.npz'
 if path.exists():
  meta=json.loads((out/'feature-construction.json').read_text());verification=next(r for r in json.loads((census/'source-verification.json').read_text()) if r['relative_path']==DAILY);stat=(lake/DAILY).stat()
  if (stat.st_size,stat.st_mtime_ns)!=(verification['bytes'],verification['mtime_ns']) or meta['source_sha256']!=verification['sha256'] or meta.get('recipe_function_sha256')!=hashlib.sha256(inspect.getsource(calculate).encode()).hexdigest():raise ValueError('cached state source/recipe identity changed; use fresh versioned output')
  identity=json.loads((out/'training-cache-identity.json').read_text())
  if identity.get('state_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest() or identity.get('census_manifest_sha256')!=hashlib.sha256((census/'execution-manifest.json').read_bytes()).hexdigest():raise ValueError('derived state or split/provenance identity changed; no stale product reuse')
  return dict(np.load(path,allow_pickle=False))
 start=time.perf_counter();verifications=json.loads((census/'source-verification.json').read_text());identity=next(r for r in verifications if r['relative_path']==DAILY);p=lake/DAILY;stat=p.stat()
 if (stat.st_size,stat.st_mtime_ns)!=(identity['bytes'],identity['mtime_ns']):raise ValueError('source changed; verify current identity')
 with sqlite3.connect(census/'cohort-metadata.sqlite') as db:
  metadata={r[0]:r[1:] for r in db.execute('SELECT s.id,s.random_fold,s.region,e.year FROM proposed_splits s LEFT JOIN events e USING(id)')}
 ids=[];yy=[];mm=[];nn=[];fold=[];regions=[];years=[];ref=[];days=[];offsets=[0];group=[];current=None
 def finish():
  if not group:return
  a=[r[2] for r in group];d=[supported_day(r[1]).toordinal() for r in group];y,m=calculate(a,d);ids.append(str(current));yy.append(y);mm.append(m);nn.append(len(group));meta=metadata[str(current)];fold.append(meta[0]);regions.append(meta[1]);years.append(meta[2] if meta[2] is not None else -1);ref.extend(r[0] for r in group);days.extend(d);offsets.append(len(ref))
 with readonly(p) as db:
  for fid,event,day,area in db.execute('SELECT fid,id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" ORDER BY id,date,fid'):
   if event!=current:finish();current=event;group=[]
   if len(group)>=8192:raise MemoryError('bounded event limit')
   group.append((fid,day,area))
  finish()
 assert len(ids)==278865 and len(ref)==627033 and len(set(ids))==len(ids)
 s=p.stat();assert (s.st_size,s.st_mtime_ns)==(stat.st_size,stat.st_mtime_ns)
 result={'ids':np.asarray(ids),'y':np.asarray(yy),'mask':np.asarray(mm),'n':np.asarray(nn),'fold':np.asarray(fold),'region':np.asarray(regions),'year':np.asarray(years),'native_fid_refs':np.asarray(ref,dtype=np.int64),'date_ordinals':np.asarray(days,dtype=np.int64),'offsets':np.asarray(offsets,dtype=np.int64)}
 np.savez_compressed(path,**result)
 dump(out/'feature-construction.json',{'seconds':time.perf_counter()-start,'native_rows_decoded':len(ref),'native_fire_ids':len(ids),'property_names':NAMES,'source_sha256':identity['sha256'],'recipe_function_sha256':hashlib.sha256(inspect.getsource(calculate).encode()).hexdigest(),'source_bytes_scope':'verified source container, not filesystem I/O','source_changed':False,'storage':'derived R1 scientific state and lineage only; original daily-value arrays not persisted','native_quality':'unknown','physical_duration':'unknown'})
 return result


def metric_rows(pred,y,mask,test,n,label,probe,fraction,rank):
 result=[]
 for stratum,use in [('all',test),('one',test&(n==1)),('two',test&(n==2)),('three_plus',test&(n>=3))]:
  for j,name in enumerate(NAMES):
   eligible=use&mask[:,j]&np.isfinite(pred[:,j]);error=pred[eligible,j]-y[eligible,j]
   result.append({'method':label,'probe':probe,'fraction':fraction,'dimension_or_rank':rank,'stratum':stratum,'property':name,'eligible_test_fires':int(eligible.sum()),'undefined_test_fires':int((use&~mask[:,j]).sum()),'mse':float(np.mean(error**2)) if len(error) else None,'mae':float(np.mean(abs(error))) if len(error) else None,'approx_1e_6_fraction':float(np.mean(abs(error)<1e-6)) if len(error) else None,'exact_preservation':'not established by approximate probes'})
 return result


def main():
 p=argparse.ArgumentParser();p.add_argument('--census',required=True);p.add_argument('--lake',required=True);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);(out/'private').mkdir(exist_ok=True,parents=True)
 cfg=json.loads((out/'preregistered-design.json').read_text());identity_path=out/'training-cache-identity.json';encoder_digest=hashlib.sha256(''.join(inspect.getsource(f) for f in (initialize,forward,loss_gradient,train,imputer_fit)).encode()).hexdigest();design_digest=hashlib.sha256((out/'preregistered-design.json').read_bytes()).hexdigest()
 if identity_path.exists():
  previous=json.loads(identity_path.read_text())
  if previous['design_sha256']!=design_digest or previous['encoder_training_sha256']!=encoder_digest or previous.get('numpy_version')!=np.__version__ or previous.get('python_version')!=sys.version:raise ValueError('encoder or training design changed; no stale checkpoint reuse')
 elif any((out/'private').glob('*-training.json')):raise ValueError('existing checkpoints lack verified training identity; preserve and use fresh output')
 else:dump(identity_path,{'design_sha256':design_digest,'encoder_training_sha256':encoder_digest,'source_sha256':json.loads((Path(a.census)/'source-verification.json').read_text())[0]['sha256'],'recipe_function_sha256':hashlib.sha256(inspect.getsource(calculate).encode()).hexdigest(),'numpy_version':np.__version__,'python_version':sys.version})
 dataset=features(Path(a.census),Path(a.lake).resolve(),out);binding=json.loads(identity_path.read_text());binding.update(state_sha256=hashlib.sha256((out/'private/observed-state.npz').read_bytes()).hexdigest(),census_manifest_sha256=hashlib.sha256((Path(a.census)/'execution-manifest.json').read_bytes()).hexdigest());dump(identity_path,binding);y=dataset['y'];mask=dataset['mask'];n=dataset['n'];base_train=dataset['fold']=='train';test=dataset['fold']=='test';ids=dataset['ids'];runtime=[];metrics=[]
 mean=np.array([y[base_train&mask[:,j],j].mean() for j in range(y.shape[1])]);scale=np.array([y[base_train&mask[:,j],j].std() for j in range(y.shape[1])]);scale[scale<1e-9]=1.;normalized=(y-mean)/scale
 np.savez(out/'private/evaluation-scales.npz',mean=mean,scale=scale)
 for fraction in cfg['training_fractions']:
  use=base_train&np.array([learning_fraction(str(k),fraction,cfg['seed']) for k in ids]);prep,x=imputer_fit(y,mask,use);target_mu=np.array([y[use&mask[:,j],j].mean() for j in range(y.shape[1])]);target_sd=np.array([y[use&mask[:,j],j].std() for j in range(y.shape[1])]);target_sd[target_sd<1e-9]=1.;target=(y-target_mu)/target_sd
  ftag=str(fraction).replace('.','p');np.savez(out/f'private/preprocess-{ftag}.npz',**prep,target_mean=target_mu,target_scale=target_sd)
  # Same-label raw-state probes are controls for all downstream learned probes.
  for nonlinear in (False,True):
   t=time.perf_counter();state,pred=probe_fit(x,y,mask,use,nonlinear=nonlinear);label='raw_state';probe='nonlinear_tanh32_ridge' if nonlinear else 'linear_ridge';metrics.extend(metric_rows((pred-mean)/scale,normalized,mask,test,n,label,probe,fraction,x.shape[1]));runtime.append({'method':label,'probe':probe,'fraction':fraction,'stage':'probe_fit_and_predict','seconds':time.perf_counter()-t})
   np.savez_compressed(out/f'private/raw-{probe}-{ftag}.npz',**{k:v for k,v in state.items() if v is not None})
  # All PCA axes are real training covariance eigenvectors; no padded dimensions.
  t=time.perf_counter();cov=np.cov(x[use],rowvar=False);values,vectors=np.linalg.eigh(cov);actual_rank=int(np.sum(values>max(values.max(),1)*1e-10));pca_time=time.perf_counter()-t
  for dimension in cfg['embedding_dimensions']:
   rank=min(dimension,actual_rank);components=vectors[:,-rank:][:,::-1];z=x@components;pca_label='pca-request'+str(dimension)
   pca_path=out/f'private/pca-{dimension}-{ftag}.npz';np.savez_compressed(pca_path,components=components,eigenvalues=values[-rank:][::-1],actual_rank=actual_rank)
   runtime.append({'method':pca_label,'fraction':fraction,'stage':'pca_fit_shared','seconds':pca_time,'requested_dimension':dimension,'effective_rank':rank})
   methods=[(pca_label,z,rank)]
   for family in ('supervised','self_supervised','multitask'):
    label=family+'-'+str(dimension);checkpoint=out/f'private/{label}-{ftag}.npz';record=out/f'private/{label}-{ftag}-training.json'
    if family=='supervised':target_y=target[:,[1]];target_mask=mask[:,[1]]
    elif family=='self_supervised':target_y=x;target_mask=np.ones_like(x,dtype=bool)
    else:target_y=target[:,[0,1,4]];target_mask=mask[:,[0,1,4]]
    t=time.perf_counter()
    if checkpoint.exists() and record.exists():params=dict(np.load(checkpoint,allow_pickle=False));training_record=json.loads(record.read_text())
    else:
     params,curve=train(x[use],target_y[use],target_mask[use],dimension,epochs=cfg['epochs'],seed=cfg['seed']);training_record={'family':family,'dimension':dimension,'fraction':fraction,'training_fires':int(use.sum()),'loss_curve':curve,'seconds':time.perf_counter()-t,'parameters':sum(v.size for v in params.values()),'objectives':cfg['training_objectives'][family]};np.savez_compressed(checkpoint,**params);dump(record,training_record)
    t=time.perf_counter();_,embedding,_=forward(params,x);materialization=time.perf_counter()-t
    runtime.append({'method':label,'fraction':fraction,'stage':'training','seconds':training_record['seconds'],'parameters':training_record['parameters']});runtime.append({'method':label,'fraction':fraction,'stage':'encoding_all_fires','seconds':materialization})
    if fraction==1.:np.savez_compressed(out/f'private/{label}-materialized.npz',z=embedding.astype(np.float32))
    methods.append((label,embedding,dimension))
    print(json.dumps({'completed_training':label,'fraction':fraction,'fires':int(use.sum()),'seconds':training_record['seconds']}),flush=True)
   for label,z,rank in methods:
    for nonlinear in (False,True):
     probe='nonlinear_tanh32_ridge' if nonlinear else 'linear_ridge';t=time.perf_counter();head,pred=probe_fit(z,y,mask,use,nonlinear=nonlinear);runtime.append({'method':label,'probe':probe,'fraction':fraction,'stage':'probe_fit_and_predict','seconds':time.perf_counter()-t});metrics.extend(metric_rows((pred-mean)/scale,normalized,mask,test,n,label,probe,fraction,rank));np.savez_compressed(out/f'private/{label}-{probe}-{ftag}-head.npz',**{k:v for k,v in head.items() if v is not None})
     if fraction==1.:
      np.savez_compressed(out/f'private/{label}-{probe}-test.npz',prediction=pred[test].astype(np.float32),test_indices=np.flatnonzero(test))
   csvwrite(out/'information-preservation.csv',metrics);dump(out/'runtime-stages.json',runtime)
  print('COMPLETED FRACTION '+str(fraction),flush=True)
 dump(out/'training-complete.json',{'status':'REAL_OBSERVED_STATE_TRAINING_AND_PROBES_COMPLETE','neural_checkpoints':75,'fire_ids':len(ids),'train_fires':int(base_train.sum()),'test_fires':int(test.sum()),'target_names':NAMES,'undefined_counts':{name:int((~mask[:,j]).sum()) for j,name in enumerate(NAMES)},'pca_rank':'requested dimensions capped to measured rank; see checkpoint records','population':'all fires; strata not excluded','scientific_scope':'observed-state feature encoders, not raw-sequence or physical-mechanism models','epoch_count':cfg['epochs'],'single_seed':True,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
if __name__=='__main__':main()
