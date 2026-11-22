"""Future references, frozen transfer, task losses, retrieval and reuse boundaries."""
from copy import deepcopy
from pathlib import Path
import json
import numpy as np
import pytest
from pydantic import ValidationError
from dataset_prototype.embedding_study.transfer_contracts import TransferConfig
from dataset_prototype.embedding_study.transfer_targets import future_targets,property_targets
from dataset_prototype.embedding_study.transfer_models import init,loss_grad,train,forward,LinearHead,load_checkpoint
from dataset_prototype.embedding_study.transfer_evaluation import paired_fire_delta,retrieval,ranks,score
from dataset_prototype.embedding_study.transfer_runner import source,run
from dataset_prototype.embedding_study.learned_data import generate,PrefixPreprocessor
from dataset_prototype.embedding_study.learned_training_contracts import TrainingConfig
from dataset_prototype.embedding_study.learned_experiment import run as run_original,normalized_tensor
from dataset_prototype.embedding_study.learned_models import state_digest

ROOT=Path(__file__).resolve().parents[1]


def test_independent_future_targets_and_support():
    histories,records=generate(TrainingConfig(train_fires=8,validation_fires=4,test_fires=4,epochs=1,training_seeds=(1,)))
    h={x['fire_id']:x for x in histories}
    for r in records:
        p=r['prefix'];a,vector,receipt=future_targets(p,h[p.fire_id]);v=np.array(h[p.fire_id]['growth_km2_day'][len(p.dates):len(p.dates)+3])
        assert a[0]==pytest.approx(np.log1p(v[0])) and a[1]==pytest.approx(np.log1p(sum(v)))
        assert a[2]==float(sum(v)>sum(p.growth_km2_day[-3:])) and a[3]==pytest.approx(np.log1p(np.std(v)))
        assert not set(receipt['future_observation_ids'])&set(p.source_observation_ids)
        assert np.allclose(vector,np.log1p(v))
    short=deepcopy(h[records[0]['prefix'].fire_id]);short['growth_km2_day']=short['growth_km2_day'][:3]
    with pytest.raises(ValueError):future_targets(records[0]['prefix'],short)

@pytest.mark.parametrize('kind',['tcn','mlp'])
@pytest.mark.parametrize('outputs,binary',[(1,(0,)),(3,()),(4,(2,))])
def test_mixed_objective_gradients(kind,outputs,binary):
    rng=np.random.default_rng(23);x=rng.normal(size=(4,12,4));x[:,:,2]=1;y=rng.normal(size=(4,outputs))
    for j in binary:y[:,j]=(y[:,j]>0).astype(float)
    p=init(kind,17,outputs);_,g=loss_grad(p,x,y,kind,binary)
    for name,a in p.items():
        i=tuple(0 for _ in a.shape);original=a[i];epsilon=1e-6
        a[i]=original+epsilon;hi=loss_grad(p,x,y,kind,binary)[0]
        a[i]=original-epsilon;lo=loss_grad(p,x,y,kind,binary)[0];a[i]=original
        assert g[name][i]==pytest.approx((hi-lo)/(2*epsilon),abs=2e-6,rel=2e-5)


def test_logistic_and_regression_heads():
    x=np.arange(-8,9,dtype=float)[:,None];y=(x[:,0]>0).astype(float)
    model=LinearHead().fit(x,y,binary=True);p=model.predict(x)
    assert np.all((p>=0)&(p<=1)) and np.mean((p>=.5)==y)>.9
    reg=LinearHead().fit(x,2*x[:,0]+3,alpha=.01)
    assert np.mean((reg.predict(x)-(2*x[:,0]+3))**2)<.001


def test_retrieval_excludes_same_fire_and_known_perfect_ranks():
    future=np.arange(32,dtype=float).reshape(16,2);ids=[str(i//4) for i in range(16)]
    result=retrieval(future,future,ids,k=3)
    assert result['mean_fire_precision_at_k']==1 and result['mean_rank_correlation']==pytest.approx(1)
    for row in result['rows']:
        assert all(ids[j]!=row['fire_id'] for j in row['selected_indices'])
    assert np.array_equal(ranks([2,1,1]),[2,.5,.5])
    with pytest.raises(ValueError):retrieval(future,future,['same']*16,k=3)


def test_fire_pairing_preserves_clusters():
    y=np.array([0.,1.,1.,0.]);p=np.zeros(4);raw=np.ones(4);ids=['a','a','b','b']
    a=paired_fire_delta(y,p,raw,ids,100,3);b=paired_fire_delta(y,p,raw,ids,100,3)
    assert a==b and a['fires']==2 and a['raw_minus_method_mean_squared_loss']==0
    assert a['descriptive_fire_resampling_95_interval']==[0,0]


def test_config_and_binary_scoring_contracts():
    with pytest.raises(ValidationError):TransferConfig(scope='real')
    with pytest.raises(ValidationError):TransferConfig(horizon=4)
    with pytest.raises(ValidationError):TransferConfig(seeds=(1,1))
    s=score(np.array([0.,1.]),np.array([.1,.9]),binary=True)
    assert s['accuracy']==1 and s['brier']==pytest.approx(.01)


def test_source_checkpoint_is_immutable_and_task_A_matches_original():
    root,manifest,histories,records,pre,params=source(TransferConfig())
    identity=state_digest(params);p=[r['prefix'] for r in records if r['split']=='test']
    x=normalized_tensor(p,pre);z=forward(params,x,'tcn')[1]
    assert z.shape==(256,4) and state_digest(params)==identity
    original=json.loads((root/'model_states.json').read_text())['learned_probe'];trainp=[r['prefix'] for r in records if r['split']=='train']
    trainz=forward(params,normalized_tensor(trainp,pre),'tcn')[1];lookup={h['fire_id']:h for h in histories}
    yt=np.array([future_targets(q,lookup[q.fire_id])[0][0] for q in trainp]);head=LinearHead().fit(trainz,yt)
    prediction=head.predict(z);reference=(z-np.array(original['mean']))/np.array(original['scale'])@np.array(original['coef'])+original['intercept']
    assert np.allclose(prediction,reference,atol=1e-12)


def test_full_tiny_transfer_run(tmp_path):
    source_path=tmp_path/'m4';run_original(TrainingConfig(train_fires=8,validation_fires=4,test_fires=4,epochs=1,training_seeds=(271,)),source_path)
    config=TransferConfig(source_snapshot=str(source_path),epochs=1,seeds=(271,),bootstrap_replicates=20)
    before={p.name:p.read_bytes() for p in source_path.iterdir()}
    result=run(config,tmp_path/'m5')
    assert result['status']=='complete' and result['real_model_calls']==0 and result['real_source_rows_read']==0
    assert result['frozen_encoder_digest_before']==result['frozen_encoder_digest_after']
    assert all(p.read_bytes()==before[p.name] for p in source_path.iterdir())
    evaluation=json.loads((tmp_path/'m5/evaluation.json').read_text())
    assert set(evaluation['frozen_A'])=={'A','B','C','D'}
    retrieval_data=json.loads((tmp_path/'m5/retrieval.json').read_text())
    assert 'E_supervised_head_distance' in retrieval_data['frozen_A']
    import hashlib
    for name,expected in result['output_sha256'].items():assert hashlib.sha256((tmp_path/'m5'/name).read_bytes()).hexdigest()==expected
    with pytest.raises(FileExistsError):run(config,tmp_path/'m5')
