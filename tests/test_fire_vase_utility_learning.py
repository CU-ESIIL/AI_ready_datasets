import numpy as np
import pytest
from dataset_prototype.embedding_study.observed_state import calculate
from dataset_prototype.embedding_study.utility_learning import initialize,loss_gradient,imputer_fit,probe_fit


def test_observed_properties_keep_undefined_and_calendar_support():
    y,m=calculate([2.],[10]);assert not m[4:9].any() and y[9]==0
    y,m=calculate([2.,8.],[10,14]);assert not m[6] and not m[7] and y[5]==.2 and y[8]==.2
    y,m=calculate([2.,8.,1.],[10,11,12]);assert m[6] and y[7]==1 and y[6]==pytest.approx(np.arcsinh(-.5))
    with pytest.raises(ValueError):calculate([2.,1.],[10,10])
    with pytest.raises(ValueError):calculate([-1.],[10])


@pytest.mark.parametrize('dimension',[4,8,16,32,64])
def test_observed_encoder_gradients(dimension):
    rng=np.random.default_rng(3);x=rng.normal(size=(4,5));y=rng.normal(size=(4,3));mask=np.ones_like(y,dtype=bool);mask[0,1]=False;y[0,1]=np.nan;p=initialize(5,dimension,3,2);_,g=loss_gradient(p,x,y,mask)
    for k,i in [('w',(1,2)),('v',(2,1)),('o',(1,2)),('b',(2,)),('c',(1,)),('a',(2,))]:
        orig=p[k][i];eps=1e-6;p[k][i]=orig+eps;hi=loss_gradient(p,x,y,mask)[0];p[k][i]=orig-eps;lo=loss_gradient(p,x,y,mask)[0];p[k][i]=orig
        assert g[k][i]==pytest.approx((hi-lo)/(2*eps),abs=1e-6)


def test_preprocessing_train_only_and_masked_probes():
    y=np.array([[1.,np.nan],[3.,2.],[999.,999.]]);mask=np.isfinite(y);train=np.array([True,True,False]);s,x=imputer_fit(y,mask,train)
    assert s['median'].tolist()==[2.,2.]
    state,p=probe_fit(x,y,mask,train,nonlinear=True);assert np.isfinite(p).all()


def test_state_does_not_claim_full_cumulative_history_or_absolute_dates():
    a=[1.,2.,3.,5.,4.,6.];b=[1.,3.,2.,4.,5.,6.];days=list(range(6))
    ya,ma=calculate(a,days);yb,mb=calculate(b,days)
    assert np.array_equal(ma,mb) and np.allclose(ya,yb,equal_nan=True)
    assert not np.array_equal(np.cumsum(a),np.cumsum(b))
    shifted,mask=calculate(a,[d+50 for d in days])
    assert np.array_equal(mask,ma) and np.array_equal(ya,shifted,equal_nan=True)


def test_prediction_prefix_has_no_future_or_gap_leakage():
    from dataset_prototype.embedding_study.observed_state import prediction_examples
    a=[1.,2.,3.,4.];b=[1.,200.,300.,400.]
    x=list(prediction_examples(a,[0,1,2,3],1,3))[0];z=list(prediction_examples(b,[0,1,2,3],1,3))[0]
    assert np.array_equal(x[1],z[1],equal_nan=True) and np.array_equal(x[2],z[2]) and x[3]!=z[3]
    assert not list(prediction_examples(a,[0,1,4,5],1,3))
    assert len(list(prediction_examples(a,[0,1,4,5],1,1)))==2


def test_masked_probe_intercept_matches_independent_centered_ridge():
    x=np.arange(120,dtype=float)[:,None];y=np.column_stack([3*x[:,0]+5,7*x[:,0]-2]);mask=np.ones_like(y,bool);mask[:40,1]=False;tr=np.arange(120)<100
    state,pred=probe_fit(x,y,mask,tr)
    a=(x-state['mean'])/state['scale'];use=tr&mask[:,1];c=a[use].mean(0);target=y[use,1];mu=target.mean();coef=np.linalg.solve((a[use]-c).T@(a[use]-c)+np.eye(1),(a[use]-c).T@(target-mu));reference=(a-c)@coef+mu
    assert np.allclose(pred[:,1],reference)


def test_access_fallback_never_turns_undefined_properties_into_zero():
    from dataset_prototype.embedding_study.utility_learning import access_rows
    rows=[{'fraction':'1.0','eligible_test_fires':'0','property':'log_observed_std','mse':'','mae':''},
          {'fraction':'1.0','eligible_test_fires':'2','property':'log_observation_count','mse':'.2','mae':'.3'}]
    result=access_rows(rows)
    assert all(r['mse']=='' and not r['native_fallback'] for r in result[:3])
    assert result[3]['mse']=='.2' and result[4]['mse']=='0' and result[5]['native_fallback']


def test_optimized_encoder_is_identical_without_pretext_head():
    from dataset_prototype.embedding_study.utility_learning import encode,forward
    rng=np.random.default_rng(4);x=rng.normal(size=(20,5));p=initialize(5,16,20,1)
    assert np.array_equal(encode(p,x),forward(p,x)[1])


def test_two_point_order_contrast_preserves_scale_but_changes_allocation():
    a, ma = calculate([2., 8.], [10, 11])
    b, mb = calculate([8., 2.], [10, 11])
    assert np.array_equal(ma, mb)
    assert np.allclose(a[[0, 1, 4, 9]], b[[0, 1, 4, 9]])
    assert a[2] == b[3] and a[3] == b[2]
    assert a[5] == pytest.approx(1 - b[5])
    assert a[6] == pytest.approx(-b[6])
    assert not ma[7] and np.isnan(a[7])
