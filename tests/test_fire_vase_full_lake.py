"""Full-lake metadata, gated source access, streaming and method dry-run contracts."""
from datetime import date,datetime,timedelta,timezone
from pathlib import Path
import json,hashlib,struct
import numpy as np
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.lake_contracts import LakePlan,LakeAuthorization,SourceBinding,ScopeFinding,SCOPES,JURISDICTIONS
from dataset_prototype.embedding_study.lake_authorization import require_scope,scope_reasons,verify_container
from dataset_prototype.embedding_study.lake_inventory import nc3_header,schema_metadata
from dataset_prototype.embedding_study.lake_stream import NativeDay,profile_events,prefix_examples,tasks,raw_parquet_batches,canonical_rows
from dataset_prototype.embedding_study.lake_models import initialize,forward,loss_gradient,train_epoch,masked_training_view,ssl_inference_view,incremental_pca
from dataset_prototype.embedding_study.lake_methods import prefix_tensor,prefix_summaries,incremental_svd,exact_neighbors
from dataset_prototype.embedding_study.lake_design import learning_fraction,fold_for_fire,clustered_effect,holm_adjust,pareto,lifecycle_cost
from dataset_prototype.embedding_study.lake_experiment import dry_validate

ROOT=Path(__file__).resolve().parents[1]
METADATA=ROOT/'reports/embedding_utility/fire_vase/milestone-7/metadata-v1'


def plan():return LakePlan(inventory_digest='1'*64,source_release='GENERATED_TEST_ONLY')
def authorization(p,scopes=SCOPES):
    return LakeAuthorization(plan_digest=p.plan_digest,origin='EXTERNAL_HUMAN_REVIEW',reviewer='GENERATED TEST REVIEWER',
      timestamp=datetime(2026,11,21,tzinfo=timezone.utc),human_receipt_reference='OFFLINE_TEST_NOT_REAL_APPROVAL',receipt_verified_by='OFFLINE_TEST',approved_scopes=scopes,
      findings=tuple(ScopeFinding(scope=s,jurisdiction=j,status='PASS',evidence_ids=('TEST_ONLY',),rationale='generated gate test') for s in scopes for j in JURISDICTIONS))
def rows(n=45,events=2):
    for e in range(events):
        for i in range(n):yield NativeDay(str(e),str(e)+':'+str(i),date(2020,1,1)+timedelta(days=i),float(i%7))


def test_full_inventory_is_metadata_and_draft_not_authorization():
    inventory=json.loads((METADATA/'inventory-summary.json').read_text());p=LakePlan.model_validate_json((METADATA/'amendment.json').read_text());auth=LakeAuthorization.model_validate_json((METADATA/'authorization-template.json').read_text())
    assert inventory['current_files_stat']>=inventory['historical_files'] and inventory['observation_rows_read']==0 and inventory['data_array_values_read']==0
    assert all(v is None for v in inventory['eligibility_counts'].values())
    assert p.row_limit is None and p.population=='all_task_eligible_fires'
    for scope in SCOPES:
        with pytest.raises(PermissionError):require_scope(p,auth,scope)
    catalog=json.loads((METADATA/'catalog.json').read_text());assert digest(catalog)==p.inventory_digest
    assert all(row['current_complete_checksum'] is None for row in catalog)


def test_scientific_changes_and_scope_vetoes_invalidate_authorization():
    p=plan();a=authorization(p,('profile_rows',));require_scope(p,a,'profile_rows')
    with pytest.raises(PermissionError):require_scope(p,a,'harmonize')
    with pytest.raises(PermissionError):require_scope(p.model_copy(update={'window_days':14}),a,'profile_rows')
    failed=a.model_copy(update={'findings':tuple(f.model_copy(update={'status':'FAIL'}) if f.jurisdiction=='rights' else f for f in a.findings)})
    with pytest.raises(PermissionError):require_scope(p,failed,'profile_rows')
    assert 'scientist_effect_sizes_not_reviewed' in scope_reasons(p,authorization(p),'train_neural')
    with pytest.raises(ValidationError):LakeAuthorization(plan_digest=p.plan_digest,approved_scopes=('profile_rows',))


def test_denied_read_does_not_open_or_create_files(tmp_path,monkeypatch):
    p=plan();draft=LakeAuthorization(plan_digest=p.plan_digest)
    binding=SourceBinding(source_relative_path='absent.parquet',expected_sha256='0'*64,event_field='id',date_field='date',area_field='area',sorted_by_event_and_date=True,date_interpretation='native_iso_date',semantic_evidence='test',uncertainty_evidence='unknown_test')
    def forbidden(*a,**kw):raise AssertionError('source open before approval')
    monkeypatch.setattr(Path,'open',forbidden)
    with pytest.raises(PermissionError):next(raw_parquet_batches(tmp_path,binding,{},p,draft))
    with pytest.raises(PermissionError):verify_container(tmp_path,'absent','0'*64,p,draft)


def test_current_checksum_has_scope_and_no_decoding(tmp_path):
    f=tmp_path/'GENERATED.bin';f.write_bytes(b'not real observations');p=plan();a=authorization(p,('verify_container_bytes',));expected=hashlib.sha256(f.read_bytes()).hexdigest()
    evidence=verify_container(tmp_path,f.name,expected,p,a)
    assert evidence['sha256']==expected and evidence['scope']=='complete_container_bytes_no_decoding'
    with pytest.raises(ValueError):verify_container(tmp_path,f.name,'0'*64,p,a)
    with pytest.raises(ValueError):verify_container(tmp_path,'../outside','0'*64,p,a)


def test_no_guessing_csv_headers_or_json_rows(tmp_path):
    p=tmp_path/'possible_observations.csv';p.write_text('1,actual-looking-row\n')
    assert schema_metadata(p)['status']=='NOT_INSPECTED'
    assert p.read_text()=='1,actual-looking-row\n'


def test_netcdf_header_parser_never_reads_array_payload(tmp_path):
    # Minimal NetCDF classic header, no dimensions/attrs/vars, then a sentinel payload.
    data=b'CDF\x01'+struct.pack('>IIIIIII',0,0,0,0,0,0,0)
    p=tmp_path/'generated.nc';p.write_bytes(data+b'SENTINEL_DO_NOT_READ')
    result=nc3_header(p)
    assert result['header_bytes_read']==len(data) and result['data_values_read']==0 and result['variables']==[]


def test_streaming_profiles_and_supported_windows(tmp_path):
    profile=list(profile_events(rows(),tmp_path/'metadata.sqlite'))
    assert len(profile)==2 and all(p['observations']==45 for p in profile)
    assert profile[0]['sequences']=={'3':43,'7':39,'14':32,'30':16}
    assert profile[0]['observed_zero']==7 and profile[0]['spatially_supported'] is None
    examples=list(prefix_examples(rows(),depths=(3,),horizons=(1,3,7)))
    assert len(examples)==2*(42+40+36)
    for example in examples:
        target=tasks(example);assert target['horizon_total']==sum(r.area_km2 for r in example['future'])
        if len(example['future'])>=3:
            f=[r.area_km2 for r in example['future']]
            assert target['acceleration']==pytest.approx((f[-1]-f[0])/(len(f)-1))
        assert set(r.observation_key for r in example['past']).isdisjoint(r.observation_key for r in example['future'])
    with pytest.raises(ValueError):list(profile_events([*rows(3,2),*rows(1,1)],tmp_path/'bad-order.sqlite'))


def test_missing_is_not_zero_and_unsupported_windows_reset():
    data=list(rows(12,1));data[3]=NativeDay('0','missing',data[3].native_date,None)
    examples=list(prefix_examples(data,depths=(3,),horizons=(3,)))
    assert all(not any(r.observation_key=='missing' for r in e['past']+e['future']) for e in examples)
    x=prefix_tensor([tuple(list(rows(3,1)))])
    assert x[0,-3,2]==1 and x[0,-3,0]==0 # evidenced zero, not padding

@pytest.mark.parametrize('dimension',[4,8,16,32,64])
def test_dimension_grid_ssl_and_independent_gradients(dimension):
    rng=np.random.default_rng(2);x=rng.normal(size=(3,14,4));x[:,:,2]=1;y=rng.normal(size=(3,4));y[:,2]=(y[:,2]>0).astype(float)
    p=initialize(dimension,4,31);_,g=loss_gradient(p,x,y,binary_columns=(2,))
    for key in ('conv','embed','head'):
        index=tuple(0 for _ in p[key].shape);value=p[key][index];epsilon=1e-6
        p[key][index]=value+epsilon;hi=loss_gradient(p,x,y,binary_columns=(2,))[0]
        p[key][index]=value-epsilon;lo=loss_gradient(p,x,y,binary_columns=(2,))[0];p[key][index]=value
        assert g[key][index]==pytest.approx((hi-lo)/(2*epsilon),abs=2e-6)
    masked,targets,positions=masked_training_view(x,5)
    assert np.all(masked[:,:,1]==0) and np.all(ssl_inference_view(x)[:,:,1]==0)
    for i,j in enumerate(positions):assert masked[i,j,0]==0 and masked[i,j,2]==0 and targets[i,0]==x[i,j,0]


def test_partial_multitask_labels_not_global_complete_case():
    x=np.ones((2,7,4));y=np.array([[1.,np.nan],[np.nan,2.]]);mask=np.isfinite(y);p=initialize(4,3,2)
    # Use registered three-output head with independently unsupported target columns.
    y=np.column_stack([y,np.full(2,np.nan)]);mask=np.column_stack([mask,np.zeros(2,dtype=bool)])
    loss,g=loss_gradient(p,x,y,target_mask=mask)
    assert np.isfinite(loss) and np.isfinite(g['head']).all()
    with pytest.raises(ValueError):loss_gradient(p,x,y)


def test_incremental_classical_methods_match_dense_references():
    r=np.random.default_rng(4);x=r.normal(size=(50,8));a=incremental_pca([x[:17],x[17:]],3);b=incremental_svd([x[:17],x[17:]],3)
    _,s,v=np.linalg.svd(x-x.mean(0),full_matrices=False);_,ss,vv=np.linalg.svd(x,full_matrices=False)
    assert np.allclose(a['components'].T@a['components'],v[:3].T@v[:3])
    assert np.allclose(b['components'].T@b['components'],vv[:3].T@vv[:3])
    assert np.allclose(b['singular_values'],ss[:3])


def test_learning_curves_splits_cost_and_frontier_science():
    small={str(i) for i in range(100) if learning_fraction(str(i),.1,1)};large={str(i) for i in range(100) if learning_fraction(str(i),.3,1)}
    assert small<=large and all(learning_fraction(str(i),1.,1) for i in range(100))
    with pytest.raises(ValueError):fold_for_fire(2001,'A',selection_years=[2001],calibration_years=[2002],test_years=[2003],heldout_regions=[],training_years=[2001])
    assert lifecycle_cost(training=1,loading=1,harmonization=1,features=1,materialization=1,query=1,count=10,refresh=None,refreshes=0) is None
    assert holm_adjust([.01,.04,.03])==pytest.approx([.03,.06,.06])
    base={'task':'A','metric':'mse','requirements_digest':'same','scientifically_valid':True}
    assert pareto([{**base,'method':'raw','cost':1,'loss':1},{**base,'method':'embedding','cost':2,'loss':2}])==['raw']
    with pytest.raises(ValueError):pareto([{**base,'method':'x','cost':1,'loss':1},{**base,'task':'B','method':'y','cost':1,'loss':1}])


def test_complete_explicit_dry_validation(tmp_path):
    report=dry_validate(tmp_path/'dry')
    assert report['mode']=='EXPLICIT_GENERATED_WIRING_TEST' and report['source_observation_rows_read']==0 and report['real_models_trained']==0
    assert [r['dimension'] for r in report['neural_kernel_checks']]==[4,8,16,32,64]
    assert report['scientific_results'] is None and report['real_eligibility_counts'] is None


def test_generated_parquet_stream_preserves_native_evidence_and_rejects_stale(tmp_path):
    pa=pytest.importorskip('pyarrow');pq=pytest.importorskip('pyarrow.parquet')
    path=tmp_path/'GENERATED_ONLY.parquet'
    pq.write_table(pa.table({'id':[17,17,17],'day':['2020-01-01','2020-01-02','2020-01-03'],
        'area':[0.,None,2.5],'qa':['ok','unknown','ok']}),path)
    binding=SourceBinding(source_relative_path=path.name,expected_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        event_field='id',date_field='day',area_field='area',quality_fields=('qa',),sorted_by_event_and_date=True,
        date_interpretation='native_iso_date',semantic_evidence='GENERATED_ONLY',uncertainty_evidence='GENERATED_UNKNOWN')
    p=plan().model_copy(update={'scientific_binding_digests':(binding.binding_digest,),'batch_rows':2});a=authorization(p)
    verified=verify_container(tmp_path,path.name,binding.expected_sha256,p,a)
    batches=list(raw_parquet_batches(tmp_path,binding,verified,p,a));assert [len(b) for b in batches]==[2,1]
    stream=list(canonical_rows(batches,binding))
    assert [r.area_km2 for r in stream]==[0.,None,2.5]
    assert all(r.native_event_id==17 and r.source_checksum==binding.expected_sha256 and r.available_at is None for r in stream)
    assert stream[-1].native_area_value==2.5 and stream[-1].quality_flags==('qa:"ok"',)
    with pytest.raises(PermissionError):next(raw_parquet_batches(tmp_path,binding,{**verified,'mtime_ns':0},p,a))
    with pytest.raises(ValueError):list(canonical_rows(batches,binding,date_decoder='reviewed_midnight_date_bin'))
