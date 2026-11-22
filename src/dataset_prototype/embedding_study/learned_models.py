"""Small NumPy causal temporal network; static audited training, no runtime code."""
import numpy as np
from ..contracts import digest


def initialize(kind,seed):
    rng=np.random.default_rng(seed)
    def weight(shape):return rng.normal(0,np.sqrt(1/shape[0]),shape)
    if kind=='tcn':return {'conv':weight((3,4,8))*.5,'conv_b':np.zeros(8),'embed':weight((16,4)),
      'embed_b':np.zeros(4),'head':weight((4,1)),'head_b':np.zeros(1)}
    if kind=='mlp':return {'dense':weight((48,3)),'dense_b':np.zeros(3),'embed':weight((3,4)),
      'embed_b':np.zeros(4),'head':weight((4,1)),'head_b':np.zeros(1)}
    raise ValueError('registered network kind required')


def forward(params,x,kind):
    if x.ndim!=3 or x.shape[1:]!=(12,4) or not np.isfinite(x).all():raise ValueError('bounded finite prefix tensor')
    if kind=='tcn':
        padded=np.pad(x,((0,0),(2,0),(0,0)))
        shifts=[padded[:,k:k+12,:] for k in range(3)]
        a=sum(np.einsum('ntc,ch->nth',v,params['conv'][k]) for k,v in enumerate(shifts))+params['conv_b']
        h=np.tanh(a);mask=x[:,:,2:3];den=mask.sum(1)
        if (den<=0).any():raise ValueError('nonempty observed prefix required')
        f=np.concatenate([(h*mask).sum(1)/den,h[:,-1,:]],axis=1)
        memo=(shifts,h,mask,den)
    elif kind=='mlp':
        flat=x.reshape(len(x),-1);h=np.tanh(flat@params['dense']+params['dense_b']);f=h;memo=(flat,h)
    else:raise ValueError('unknown architecture')
    z=np.tanh(f@params['embed']+params['embed_b']);pred=(z@params['head']+params['head_b'])[:,0]
    return pred,z,(f,z,memo)


def loss_and_grad(params,x,y,kind,l2=1e-4):
    prediction,z,(f,z,memo)=forward(params,x,kind);error=prediction-y
    loss=float(np.mean(error**2)+l2*sum((v*v).sum() for k,v in params.items() if not k.endswith('_b')))
    dp=2*error[:,None]/len(y);grad={'head':z.T@dp,'head_b':dp.sum(0)}
    dz=(dp@params['head'].T)*(1-z*z);grad.update(embed=f.T@dz,embed_b=dz.sum(0));df=dz@params['embed'].T
    if kind=='tcn':
        shifts,h,mask,den=memo;dh=df[:,:8][:,None,:]*mask/den[:,None,:]
        dh[:,-1,:]+=df[:,8:];da=dh*(1-h*h)
        grad['conv']=np.stack([np.einsum('ntc,nth->ch',v,da) for v in shifts]);grad['conv_b']=da.sum((0,1))
    else:
        flat,h=memo;dh=df*(1-h*h);grad['dense']=flat.T@dh;grad['dense_b']=dh.sum(0)
    for key in grad:
        if not key.endswith('_b'):grad[key]+=2*l2*params[key]
    return loss,grad


def fit_network(x,y,kind,seed,epochs,learning_rate):
    params=initialize(kind,seed);m={k:np.zeros_like(v) for k,v in params.items()};v={k:np.zeros_like(a) for k,a in params.items()}
    rng=np.random.default_rng(seed+1000);steps=0;losses=[]
    for epoch in range(epochs):
        order=rng.permutation(len(y))
        for start in range(0,len(y),64):
            batch=order[start:start+64];_,g=loss_and_grad(params,x[batch],y[batch],kind);steps+=1
            norm=np.sqrt(sum((a*a).sum() for a in g.values()));factor=min(1.,5/max(norm,1e-12))
            for k in params:
                g[k]*=factor;m[k]=.9*m[k]+.1*g[k];v[k]=.999*v[k]+.001*g[k]*g[k]
                params[k]-=learning_rate*(m[k]/(1-.9**steps))/(np.sqrt(v[k]/(1-.999**steps))+1e-8)
        if epoch%10==0 or epoch==epochs-1:losses.append({'epoch':epoch+1,'training_loss':loss_and_grad(params,x,y,kind)[0]})
    return params,losses


def state_digest(params):return digest({k:v.tolist() for k,v in sorted(params.items())})
def parameter_count(params):return sum(a.size for a in params.values())


def save_checkpoint(path,params):np.savez(path,**params)
def load_checkpoint(path,kind):
    expected=initialize(kind,0)
    with np.load(path,allow_pickle=False) as arrays:
        if set(arrays.files)!=set(expected):raise ValueError('checkpoint parameter registry mismatch')
        result={k:arrays[k].copy() for k in arrays.files}
    if any(result[k].shape!=expected[k].shape or not np.isfinite(result[k]).all() for k in expected):raise ValueError('checkpoint integrity/shape')
    return result


class Ridge:
    def fit(self,x,y,alpha=1.):
        self.mean=x.mean(0);self.scale=x.std(0);self.scale[self.scale<1e-8]=1
        a=(x-self.mean)/self.scale;self.intercept=float(y.mean());self.coef=np.linalg.solve(a.T@a+alpha*np.eye(x.shape[1]),a.T@(y-self.intercept));return self
    def predict(self,x):return (x-self.mean)/self.scale@self.coef+self.intercept
    def state(self):return {k:v.tolist() if hasattr(v,'tolist') else v for k,v in vars(self).items()}
