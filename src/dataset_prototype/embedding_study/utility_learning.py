"""Closed observed-state encoders/probes; no source tools, future labels or code eval."""
import numpy as np


def initialize(inputs,dimension,outputs,seed):
    if dimension not in (4,8,16,32,64):raise ValueError('registered embedding dimension')
    rng=np.random.default_rng(seed)
    return {'w':rng.normal(0,1/np.sqrt(inputs),(inputs,16)),'b':np.zeros(16),
      'v':rng.normal(0,1/4,(16,dimension)),'c':np.zeros(dimension),
      'o':rng.normal(0,1/np.sqrt(dimension),(dimension,outputs)),'a':np.zeros(outputs)}


def forward(p,x):
    h=np.tanh(x@p['w']+p['b']);z=np.tanh(h@p['v']+p['c']);return z@p['o']+p['a'],z,h


def loss_gradient(p,x,y,mask,l2=1e-5):
    if x.ndim!=2 or y.ndim!=2 or mask.shape!=y.shape or not np.isfinite(x).all() or not np.isfinite(y[mask]).all():raise ValueError('finite supported model inputs/labels required')
    pred,z,h=forward(p,x);counts=mask.sum(0);den=np.maximum(counts,1)*max(1,np.sum(counts>0));error=np.where(mask,pred-np.where(mask,y,0),0)
    loss=float(np.sum(error*error/den)+l2*sum(np.sum(p[k]**2) for k in ('w','v','o')));dp=2*error/den
    g={'o':z.T@dp,'a':dp.sum(0)};dz=(dp@p['o'].T)*(1-z*z);g.update(v=h.T@dz,c=dz.sum(0));dh=(dz@p['v'].T)*(1-h*h);g.update(w=x.T@dh,b=dh.sum(0))
    for k in ('w','v','o'):g[k]+=2*l2*p[k]
    return loss,g


def train(x,y,mask,dimension,*,epochs=12,seed=20260828,rate=.003):
    if not len(x) or not mask.any():raise ValueError('no eligible training data; no fallback')
    p=initialize(x.shape[1],dimension,y.shape[1],seed);m={k:np.zeros_like(v) for k,v in p.items()};v={k:np.zeros_like(a) for k,a in p.items()};rng=np.random.default_rng(seed+1);step=0;curve=[]
    for epoch in range(epochs):
        order=rng.permutation(len(x));losses=[]
        for start in range(0,len(x),1024):
            b=order[start:start+1024];loss,g=loss_gradient(p,x[b],y[b],mask[b]);step+=1;norm=np.sqrt(sum(np.sum(a*a) for a in g.values()));factor=min(1.,5/max(norm,1e-12))
            for k in p:
                gg=g[k]*factor;m[k]=.9*m[k]+.1*gg;v[k]=.999*v[k]+.001*gg*gg;p[k]-=rate*(m[k]/(1-.9**step))/(np.sqrt(v[k]/(1-.999**step))+1e-8)
            losses.append(loss)
        curve.append(float(np.mean(losses)))
    return p,curve


def imputer_fit(values,mask,train_rows):
    med=np.array([np.median(values[train_rows & mask[:,j],j]) if (train_rows & mask[:,j]).any() else 0. for j in range(values.shape[1])])
    # Zero here is a declared model-input default for an entirely unsupported
    # channel, accompanied by its support bit; never a native observation.
    filled=np.where(mask,values,med);features=np.column_stack([filled,mask.astype(float)])
    mean=features[train_rows].mean(0);scale=features[train_rows].std(0);scale[scale<1e-10]=1
    return {'median':med,'mean':mean,'scale':scale},(features-mean)/scale


def probe_fit(x,y,mask,train_rows,*,nonlinear=False,seed=20260828):
    mean=x[train_rows].mean(0);scale=x[train_rows].std(0);scale[scale<1e-9]=1.;a=(x-mean)/scale
    projection=None
    if nonlinear:
        rng=np.random.default_rng(seed);projection=rng.normal(0,1/np.sqrt(x.shape[1]),(x.shape[1],32));a=np.column_stack([a,np.tanh(a@projection)])
    coefficients=[];intercepts=[]
    for j in range(y.shape[1]):
        use=train_rows & mask[:,j]
        if not use.any():coefficients.append(np.zeros(a.shape[1]));intercepts.append(np.nan);continue
        target=y[use,j];mu=target.mean();xx=a[use];center=xx.mean(0);centered=xx-center;coef=np.linalg.solve(centered.T@centered+np.eye(a.shape[1]),centered.T@(target-mu));coefficients.append(coef);intercepts.append(mu-center@coef)
    state={'mean':mean,'scale':scale,'projection':projection,'coefficients':np.stack(coefficients,axis=1),'intercepts':np.asarray(intercepts)}
    return state,a@state['coefficients']+state['intercepts']


def access_rows(metrics):
    """Access treatment never makes an undefined scientific property zero."""
    result=[]
    for row in metrics:
        if float(row['fraction'])!=1.:continue
        eligible=int(row['eligible_test_fires'])
        for condition in ('A','B','C'):
            r=dict(row);r['condition']=condition;r['native_fallback']=condition=='C' and eligible>0;r['source_access_scope']='shared measured whole-fire native fallback for defined properties' if r['native_fallback'] else 'none'
            if eligible==0:r['exact_preservation']='NOT_APPLICABLE: no defined target; no recovery score'
            elif condition=='C' or condition=='B' and row['property'] in ('log_observation_count','log_observed_span'):
                r['mse']='0';r['mae']='0';r['approx_1e_6_fraction']='1';r['exact_preservation']='native recovery, not coordinate preservation' if condition=='C' else 'exact common-sidecar count/support, not coordinate preservation'
            result.append(r)
    return result


def encode(p,x):
    """Serving encoder omits the unused pretext-training head."""
    h=np.tanh(x@p['w']+p['b'])
    return np.tanh(h@p['v']+p['c'])
