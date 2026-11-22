"""Gated source profiling and explicit generated dry validation; no silent fallback."""
import argparse,json,hashlib
from pathlib import Path
from datetime import date,timedelta
import numpy as np
from ..contracts import digest
from .lake_contracts import LakePlan,LakeAuthorization,SourceBinding
from .lake_authorization import require_scope
from .lake_stream import NativeDay,raw_parquet_batches,canonical_rows,profile_events,prefix_examples,tasks
from .lake_methods import prefix_tensor,prefix_summaries,incremental_svd,fit_conventional,CAPABILITIES,exact_neighbors
from .lake_models import initialize,forward,train_epoch,masked_training_view,ssl_inference_view,incremental_pca
from .lake_design import learning_fraction,pareto,lifecycle_cost


def dump(path,value):Path(path).write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def run_real_profile(root,plan,authorization,binding,verification,output):
    require_scope(plan,authorization,'profile_rows');require_scope(plan,authorization,'harmonize')
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    batches=raw_parquet_batches(root,binding,verification,plan,authorization)
    rows=canonical_rows(batches,binding)
    totals={'fires':0,'observations':0,'exact_day_intervals':0,'sequences':{str(n):0 for n in (3,7,14,30)}}
    try:
        with (output/'per-fire-metadata.jsonl').open('w') as file:
            for event in profile_events(rows,output/'private-event-key-index.sqlite'):
                file.write(json.dumps(event,sort_keys=True)+'\n');totals['fires']+=1;totals['observations']+=event['observations'];totals['exact_day_intervals']+=event['exact_day_intervals']
                for n,v in event['sequences'].items():totals['sequences'][n]+=v
    except Exception as error:
        dump(output/'failure.json',{'status':'FAILED_NOT_COMPLETE','error_type':type(error).__name__,'partial_metadata_counts':totals,'no_raw_or_harmonized_rows_persisted':True});raise
    dump(output/'profile.json',{'status':'PROFILED_ONLY','counts':totals,'plan_digest':plan.plan_digest,'binding_digest':binding.binding_digest,
      'models_trained':0,'source_verification':verification,'warning':'Metadata counts do not authorize subsequent model, spatial, environmental or publication phases.'})
    return totals


def dry_validate(output):
    """Generated numerical fixtures are wiring tests, never substitutes for real science."""
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    def source():
        for event in range(12):
            for t in range(45):
                yield NativeDay('GENERATED-'+str(event),'GENERATED-'+str(event)+':'+str(t),date(2000,1,1)+timedelta(days=t),float((event+t)%9),('generated',))
    profiles=list(profile_events(source(),output/'generated-event-index.sqlite'))
    examples=list(prefix_examples(source()));selected=[e for e in examples if e['depth']==14 and e['horizon']==7][:24]
    x=prefix_tensor([e['past'] for e in selected]);summary=prefix_summaries([e['past'] for e in selected]);labels=np.array([[np.log1p(tasks(e)['horizon_total'])] for e in selected])
    neural=[]
    for dimension in (4,8,16,32,64):
        p=initialize(dimension,1,731);result=train_epoch(p,[(x,labels)],rate=.001);pred,z,_=forward(p,x)
        masked,target,_=masked_training_view(x,731);ssl=initialize(dimension,1,731);ssl_result=train_epoch(ssl,[(masked,target)],rate=.001)
        assert np.all(ssl_inference_view(x)[:,:,1]==0)
        neural.append({'dimension':dimension,'parameters':sum(v.size for v in p.values()),'supervised_batches':result['batches'],'ssl_batches':ssl_result['batches'],'embedding_shape':list(z.shape)})
    raw=x.reshape(len(x),-1);pca=incremental_pca([raw[:12],raw[12:]],4);svd=incremental_svd([raw],4)
    ridge=fit_conventional('raw_ridge_logistic',raw,labels[:,0]);neighbors=exact_neighbors(raw[0],raw,['same']+['different']*(len(raw)-1),'same',3)
    report={'version':'fire-full-lake-offline-validation-v1','mode':'EXPLICIT_GENERATED_WIRING_TEST',
      'source_observation_rows_read':0,'real_models_trained':0,'generated_fires':len(profiles),'generated_observations':sum(p['observations'] for p in profiles),
      'generated_task_examples':len(examples),'stream_window_bound':37,'neural_kernel_checks':neural,
      'pca_components':list(pca['components'].shape),'svd_components':list(svd['components'].shape),'ridge_predictions_finite':bool(np.isfinite(ridge.predict(raw)).all()),
      'same_fire_excluded_neighbors':neighbors,'capabilities':CAPABILITIES,
      'real_execution':'BLOCKED_PENDING_FULL_LAKE_REVIEW; no fallback from real execution to this fixture',
      'scientific_results':None,'effect_sizes':None,'real_eligibility_counts':None}
    dump(output/'dry-validation.json',report);return report


def main():
    p=argparse.ArgumentParser();p.add_argument('--dry-validate',action='store_true');p.add_argument('--output',required=True)
    p.add_argument('--plan');p.add_argument('--authorization');p.add_argument('--binding');p.add_argument('--verification');p.add_argument('--lake');a=p.parse_args()
    if a.dry_validate:
        print(json.dumps(dry_validate(a.output)));return
    if not all((a.plan,a.authorization,a.binding,a.verification,a.lake)):p.error('real profiling requires explicit plan, external authorization, reviewed binding, current verification and canonical lake')
    plan=LakePlan.model_validate_json(Path(a.plan).read_text());auth=LakeAuthorization.model_validate_json(Path(a.authorization).read_text())
    require_scope(plan,auth,'profile_rows') # fail before loading source/binding/verification or creating outputs
    binding=SourceBinding.model_validate_json(Path(a.binding).read_text());verification=json.loads(Path(a.verification).read_text())
    print(json.dumps(run_real_profile(a.lake,plan,auth,binding,verification,a.output)))

if __name__=='__main__':main()
