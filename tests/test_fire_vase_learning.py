"""Prefix leakage, independent network gradients, synthetic controls and cache identity."""
from datetime import timedelta
import json
from pathlib import Path
import numpy as np
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.learned_contracts import PrefixInput
from dataset_prototype.embedding_study.learned_training_contracts import TrainingConfig
from dataset_prototype.embedding_study.learned_data import generate,validate_pair,raw_tensor,interpretable,PrefixPreprocessor,cache_identity
from dataset_prototype.embedding_study.learned_models import initialize,forward,loss_and_grad,fit_network,Ridge,state_digest,save_checkpoint,load_checkpoint
from dataset_prototype.embedding_study.learned_experiment import normalized_tensor,conformal_radius,metrics,checked_embedding_lookup,perturbations,run

@pytest.fixture
def tiny():return TrainingConfig(train_fires=12,validation_fires=4,test_fires=4,training_seeds=(271,),epochs=3)


def test_observation_targets_split_and_reproducibility(tiny):
    histories,records=generate(tiny);other=generate(tiny)
    assert digest(histories)==digest(other[0])
    lookup={h['fire_id']:h for h in histories};ids={s:set() for s in ('train','validation','test')}
    for r in records:
        p,y=r['prefix'],r['outcome'];validate_pair(p,y);ids[r['split']].add(p.fire_id)
        assert y.growth_km2_day==lookup[p.fire_id]['growth_km2_day'][len(p.dates)]
        assert p.growth_km2_day==tuple(lookup[p.fire_id]['growth_km2_day'][:len(p.dates)])
        assert y.available_at>p.issued_at
    assert not ids['train']&ids['test'] and not ids['validation']&ids['test']


def test_prefix_never_uses_future_and_preprocessing_train_only(tiny):
    h,records=generate(tiny);train=[r['prefix'] for r in records if r['split']=='train'];pre=PrefixPreprocessor().fit(train)
    identity=digest(pre.state());before=normalized_tensor(train,pre);features=interpretable(train)
    for r in records:r['outcome']=r['outcome'].model_copy(update={'growth_km2_day':999999.})
    assert np.array_equal(before,normalized_tensor(train,pre)) and np.array_equal(features,interpretable(train))
    _=normalized_tensor([r['prefix'] for r in records if r['split']=='test'],pre)
    assert digest(pre.state())==identity
    assert set(pre.state()['training_ids'])=={p.fire_id for p in train}

@pytest.mark.parametrize('change',['gap','availability','negative','nan','duplicate_id'])
def test_invalid_prefix_fails_closed(tiny,change):
    p=generate(tiny)[1][0]['prefix'];packet=p.model_dump(mode='json')
    if change=='gap':packet['dates'][1]=str(p.dates[1]+timedelta(days=2))
    elif change=='availability':packet['available_at'][0]=(p.issued_at+timedelta(days=1)).isoformat()
    elif change=='negative':packet['growth_km2_day'][0]=-1
    elif change=='nan':packet['growth_km2_day'][0]=float('nan')
    else:packet['source_observation_ids'][1]=packet['source_observation_ids'][0]
    with pytest.raises(ValidationError):PrefixInput.model_validate(packet)

@pytest.mark.parametrize('kind',['tcn','mlp'])
def test_analytic_gradients_match_independent_finite_difference(kind):
    rng=np.random.default_rng(7);x=rng.normal(size=(3,12,4));x[:,:,2]=1;target=rng.normal(size=3)
    params=initialize(kind,42);_,grad=loss_and_grad(params,x,target,kind)
    for key,arr in params.items():
        for idx in [tuple(0 for _ in arr.shape),tuple(s-1 for s in arr.shape)]:
            original=arr[idx];eps=1e-6
            arr[idx]=original+eps;hi=loss_and_grad(params,x,target,kind)[0]
            arr[idx]=original-eps;lo=loss_and_grad(params,x,target,kind)[0];arr[idx]=original
            assert grad[key][idx]==pytest.approx((hi-lo)/(2*eps),abs=2e-6,rel=2e-5),(kind,key,idx)


def test_training_replays_and_checkpoint_integrity(tmp_path,tiny):
    records=generate(tiny)[1];prefixes=[r['prefix'] for r in records if r['split']=='train'];pre=PrefixPreprocessor().fit(prefixes);x=normalized_tensor(prefixes,pre)
    y=np.array([np.log1p(r['outcome'].growth_km2_day) for r in records if r['split']=='train'])
    a,loss=fit_network(x,y,'tcn',3,8,.01);b,_=fit_network(x,y,'tcn',3,8,.01)
    assert state_digest(a)==state_digest(b) and loss[-1]['training_loss']<loss[0]['training_loss']
    save_checkpoint(tmp_path/'good.npz',a);assert state_digest(load_checkpoint(tmp_path/'good.npz','tcn'))==state_digest(a)
    np.savez(tmp_path/'bad.npz',code=np.array(['arbitrary']))
    with pytest.raises(ValueError):load_checkpoint(tmp_path/'bad.npz','tcn')


def test_cache_refresh_and_support_perturbations(tiny):
    prefixes=[r['prefix'] for r in generate(tiny)[1] if r['split']=='train'];pre=PrefixPreprocessor().fit(prefixes);p=prefixes[0];params=initialize('tcn',3)
    key=digest(p);identity=cache_identity(p,state_digest(params),pre.state());store={key:{'identity':identity,'embedding':[0.,1.,2.,3.]}}
    assert checked_embedding_lookup(store,key,identity).shape==(4,)
    with pytest.raises(ValueError):checked_embedding_lookup(store,key,cache_identity(p,'changed-model',pre.state()))
    changed=p.model_copy(update={'growth_km2_day':tuple(v*2 for v in p.growth_km2_day)})
    assert cache_identity(changed,state_digest(params),pre.state())!=identity
    controls=perturbations(p,pre,params)
    by_name={c['control']:c for c in controls}
    assert by_name['observation_removal']['outcome']=='rejected_gap' and by_name['temporal_resolution']['outcome']=='rejected_non_daily_support'
    assert by_name['nominal_id_relabeling']['embedding_l2_change']==0


def test_metrics_independent_known_case():
    y=np.log1p([0,1,3]);pred=np.log1p([0,1,3]);m=metrics(y,pred,0)
    assert m['mse_log1p']==0 and m['mae_km2_day']==0 and m['coverage_90']==1
    assert conformal_radius(np.array([1,2,3,4]),np.zeros(4))==4


def test_full_offline_run_replay_no_real_fallback(tmp_path,tiny):
    a=run(tiny,tmp_path/'a');b=run(tiny,tmp_path/'b')
    assert a['evaluation_digest']==b['evaluation_digest'] and a['real_source_rows_read']==0 and a['real_model_calls']==0
    assert not set(a['split_fire_ids']['train'])&set(a['split_fire_ids']['test'])
    assert not set(a['validation_selection_fire_ids'])&set(a['calibration_fire_ids'])
    root=tmp_path/'a';evaluation=json.loads((root/'evaluation.json').read_text())
    assert set(evaluation)=={'raw_ridge','interpretable_ridge','pca4_ridge','learned4_ridge','tcn_end_to_end','mlp_end_to_end','persistence','training_mean'}
    material=json.loads((root/'materialization.json').read_text());assert material['measured_prediction_equal']
    for name,expected in a['output_sha256'].items():
        import hashlib
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected


def test_configuration_boundary_and_model_capacity():
    from dataset_prototype.embedding_study.learned_models import parameter_count
    with pytest.raises(ValidationError):TrainingConfig(mode='real')
    with pytest.raises(ValidationError):TrainingConfig(depths=(3,20))
    with pytest.raises(ValidationError):TrainingConfig(training_seeds=(1,1))
    assert parameter_count(initialize('tcn',1))==177
    assert parameter_count(initialize('mlp',1))==168


def test_prefix_input_has_no_future_fields_or_full_history_normalization(tiny):
    p=generate(tiny)[1][0]['prefix'];packet=p.model_dump(mode='json');packet['final_area']=9999
    with pytest.raises(ValidationError):PrefixInput.model_validate(packet)
    x=raw_tensor([p]);assert np.all(x[0,:-len(p.dates)]==0)
    assert np.allclose(x[0,-len(p.dates):,0],np.log1p(p.growth_km2_day))
    features=interpretable([p]);assert features[0,3]==pytest.approx(np.log1p(sum(p.growth_km2_day)))
