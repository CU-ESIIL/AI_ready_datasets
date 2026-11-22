"""Closed multihead training; existing M4 encoder remains untouched and frozen."""
import numpy as np
from .learned_models import initialize,forward as base_forward


def sigmoid(a):return 1/(1+np.exp(-np.clip(a,-35,35)))

def init(kind,seed,outputs):
    if outputs not in (1,3,4):raise ValueError('registered head count')
    params=initialize(kind,seed);rng=np.random.default_rng(seed+81)
    params['head']=rng.normal(0,.5,(4,outputs));params['head_b']=np.zeros(outputs);return params


def forward(params,x,kind):
    _,z,memo=base_forward(params,x,kind)
    return z@params['head']+params['head_b'],z,memo


def loss_grad(params,x,y,kind,binary_columns=(),l2=1e-4):
    pred,z,(f,z,memo)=forward(params,x,kind);error=pred-y;terms=error*error;dp=2*error
    for j in binary_columns:
        terms[:,j]=np.logaddexp(0,pred[:,j])-y[:,j]*pred[:,j];dp[:,j]=sigmoid(pred[:,j])-y[:,j]
    loss=float(terms.mean()+l2*sum((v*v).sum() for k,v in params.items() if not k.endswith('_b')))
    dp/=y.size;g={'head':z.T@dp,'head_b':dp.sum(0)}
    dz=(dp@params['head'].T)*(1-z*z);g.update(embed=f.T@dz,embed_b=dz.sum(0));df=dz@params['embed'].T
    if kind=='tcn':
        shifts,h,mask,den=memo;dh=df[:,:8][:,None,:]*mask/den[:,None,:];dh[:,-1,:]+=df[:,8:];da=dh*(1-h*h)
        g['conv']=np.stack([np.einsum('ntc,nth->ch',v,da) for v in shifts]);g['conv_b']=da.sum((0,1))
    else:
        flat,h=memo;da=df*(1-h*h);g['dense']=flat.T@da;g['dense_b']=da.sum(0)
    for k in g:
        if not k.endswith('_b'):g[k]+=2*l2*params[k]
    return loss,g


def train(x,y,kind,seed,epochs,rate,binary_columns=()):
    p=init(kind,seed,y.shape[1]);m={k:np.zeros_like(v) for k,v in p.items()};v={k:np.zeros_like(a) for k,a in p.items()};rng=np.random.default_rng(seed+1000);step=0;curve=[]
    for epoch in range(epochs):
        order=rng.permutation(len(y))
        for start in range(0,len(y),64):
            b=order[start:start+64];_,g=loss_grad(p,x[b],y[b],kind,binary_columns);step+=1
            norm=np.sqrt(sum((a*a).sum() for a in g.values()));factor=min(1.,5/max(norm,1e-12))
            for k in p:
                g[k]*=factor;m[k]=.9*m[k]+.1*g[k];v[k]=.999*v[k]+.001*g[k]*g[k]
                p[k]-=rate*(m[k]/(1-.9**step))/(np.sqrt(v[k]/(1-.999**step))+1e-8)
        if epoch%10==0 or epoch==epochs-1:curve.append({'epoch':epoch+1,'training_loss':loss_grad(p,x,y,kind,binary_columns)[0]})
    return p,curve


class LinearHead:
    def fit(self,x,y,binary=False,alpha=1.):
        self.mean=x.mean(0);self.scale=x.std(0);self.scale[self.scale<1e-8]=1;self.binary=binary
        a=(x-self.mean)/self.scale
        if binary:
            a=np.column_stack([np.ones(len(a)),a]);w=np.zeros(a.shape[1]);reg=np.diag([0.,*([alpha]*x.shape[1])])
            for _ in range(25):
                prob=sigmoid(a@w);h=a.T@((prob*(1-prob))[:,None]*a)+reg+1e-8*np.eye(a.shape[1]);grad=a.T@(prob-y)+reg@w
                delta=np.linalg.solve(h,grad);w-=delta
                if np.linalg.norm(delta)<1e-8:break
            self.coef=w[1:];self.intercept=float(w[0])
        else:
            self.intercept=float(y.mean());self.coef=np.linalg.solve(a.T@a+alpha*np.eye(a.shape[1]),a.T@(y-self.intercept))
        return self
    def predict(self,x):
        values=(x-self.mean)/self.scale@self.coef+self.intercept
        return sigmoid(values) if self.binary else values
    def state(self):return {k:v.tolist() if hasattr(v,'tolist') else v for k,v in vars(self).items()}


def load_checkpoint(path,kind,outputs):
    expected=init(kind,0,outputs)
    with np.load(path,allow_pickle=False) as file:
        if set(file.files)!=set(expected):raise ValueError('unknown checkpoint parameters')
        p={k:file[k].copy() for k in file.files}
    if any(p[k].shape!=expected[k].shape or not np.isfinite(p[k]).all() for k in p):raise ValueError('checkpoint shape/finite mismatch')
    return p
