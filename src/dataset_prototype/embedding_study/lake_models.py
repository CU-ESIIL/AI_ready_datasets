"""Compact dimension-grid TCN and train-only masked-value objective, no source IO."""
import numpy as np
from .transfer_models import sigmoid

DIMS=(4,8,16,32,64)


def initialize(dimension,outputs,seed):
    if dimension not in DIMS or outputs not in (1,3,4,5,7):raise ValueError('registered architecture dimension/head count required')
    r=np.random.default_rng(seed)
    return {'conv':r.normal(0,.2,(3,4,8)),'conv_b':np.zeros(8),'embed':r.normal(0,.25,(16,dimension)),
      'embed_b':np.zeros(dimension),'head':r.normal(0,1/np.sqrt(dimension),(dimension,outputs)),'head_b':np.zeros(outputs)}


def forward(p,x):
    if x.ndim!=3 or not 3<=x.shape[1]<=30 or x.shape[2]!=4 or not np.isfinite(x).all():raise ValueError('bounded finite scientific window required')
    mask=x[:,:,2:3]
    if not np.isin(mask,(0,1)).all() or (mask.sum(1)<1).any():raise ValueError('explicit valid/pretext mask required')
    n=x.shape[1];padded=np.pad(x,((0,0),(2,0),(0,0)));shifts=[padded[:,k:k+n] for k in range(3)]
    h=np.tanh(sum(v@p['conv'][k] for k,v in enumerate(shifts))+p['conv_b']);den=mask.sum(1)
    f=np.concatenate([(h*mask).sum(1)/den,h[:,-1]],axis=1);z=np.tanh(f@p['embed']+p['embed_b'])
    return z@p['head']+p['head_b'],z,(shifts,h,mask,den,f,z)


def loss_gradient(p,x,y,binary_columns=(),l2=1e-4,target_mask=None):
    pred,z,(shifts,h,temporal_mask,temporal_den,f,z)=forward(p,x)
    if pred.shape!=y.shape:raise ValueError('declared target shape required')
    mask=np.ones_like(y,dtype=bool) if target_mask is None else np.asarray(target_mask,dtype=bool)
    if mask.shape!=y.shape or not mask.any() or not np.isfinite(y[mask]).all():raise ValueError('finite supported targets required; no synthetic fallback')
    target=np.where(mask,y,0.)
    dp=2*(pred-target);terms=(pred-target)**2
    for j in binary_columns:
        if not np.isin(target[mask[:,j],j],(0,1)).all():raise ValueError('binary target required')
        terms[:,j]=np.logaddexp(0,pred[:,j])-target[:,j]*pred[:,j];dp[:,j]=sigmoid(pred[:,j])-target[:,j]
    counts=mask.sum(0);active=counts>0;den=np.maximum(counts,1)*max(1,active.sum())
    loss=float(np.sum(np.sum(terms*mask,axis=0)/den)+l2*sum(np.sum(v*v) for k,v in p.items() if not k.endswith('_b')))
    dp=dp*mask/den
    grad={'head':z.T@dp,'head_b':dp.sum(0)};dz=(dp@p['head'].T)*(1-z*z)
    grad.update(embed=f.T@dz,embed_b=dz.sum(0));df=dz@p['embed'].T
    dh=df[:,:8][:,None,:]*temporal_mask/temporal_den[:,None,:];dh[:,-1]+=df[:,8:];da=dh*(1-h*h)
    grad['conv']=np.stack([np.einsum('ntc,nth->ch',a,da) for a in shifts]);grad['conv_b']=da.sum((0,1))
    for k in grad:
        if not k.endswith('_b'):grad[k]+=2*l2*p[k]
    return loss,grad


def train_epoch(p,batches,*,rate=.001,binary_columns=()):
    """Bounded statically implemented SGD; caller supplies approved batches, not code."""
    if not 0<rate<=.1:raise ValueError('bounded learning rate')
    losses=[]
    for batch in batches:
        if len(batch) not in (2,3):raise ValueError('registered x/y/optional-support-mask batch')
        x,y=batch[:2];support=batch[2] if len(batch)==3 else None
        loss,grad=loss_gradient(p,x,y,binary_columns,target_mask=support);norm=np.sqrt(sum(np.sum(v*v) for v in grad.values()));scale=min(1.,5/max(norm,1e-12))
        for k in p:p[k]-=rate*scale*grad[k]
        losses.append(loss)
    if not losses:raise ValueError('no eligible training batches; never fallback to synthetic')
    return {'batches':len(losses),'mean_loss':float(np.mean(losses))}


def masked_training_view(x,seed):
    """Training-only pretext: no future labels; remove cumulative shortcuts.

    Cumulative channel is zeroed for BOTH SSL training and later SSL inference.
    The artificial mask is a model pretext, never a claim of source missingness.
    """
    if x.ndim!=3 or x.shape[2]!=4:raise ValueError('prefix tensor required')
    r=np.random.default_rng(seed);masked=ssl_inference_view(x);y=[];positions=[]
    for i in range(len(x)):
        observed=np.flatnonzero(x[i,:,2]==1)
        if len(observed)<3:raise ValueError('at least three observed source points')
        j=int(r.choice(observed));y.append([float(x[i,j,0])]);positions.append(j)
        masked[i,j,0]=0;masked[i,j,2]=0
    return masked,np.array(y),positions


def ssl_inference_view(x):
    out=np.array(x,copy=True);out[:,:,1]=0
    return out


def incremental_pca(batches,components):
    """Train-only classical covariance PCA without accumulating raw examples."""
    n=0;mean=None;m2=None
    for batch in batches:
        a=np.asarray(batch,dtype=float)
        if a.ndim!=2 or not np.isfinite(a).all() or len(a)==0:raise ValueError('finite nonempty feature batch required')
        if mean is None:mean=np.zeros(a.shape[1]);m2=np.zeros((a.shape[1],a.shape[1]))
        if a.shape[1]!=len(mean):raise ValueError('feature layout changed')
        k=len(a);b=a.mean(0);delta=b-mean;centered=a-b;total=n+k
        m2+=centered.T@centered+np.outer(delta,delta)*n*k/total;mean+=delta*k/total;n=total
    if mean is None or not 1<=components<=min(len(mean),n-1):raise ValueError('insufficient training support for components')
    values,vectors=np.linalg.eigh(m2/max(1,n-1));order=np.argsort(values)[::-1][:components]
    return {'mean':mean,'components':vectors[:,order].T,'eigenvalues':values[order],'training_samples':n,
      'definition':'mean-centered unscaled covariance PCA; distinct from historical standardized PCA unless matching preprocessing is reviewed'}
