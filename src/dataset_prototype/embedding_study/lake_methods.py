"""Independently callable offline methods; real callers must pass the scientific gates."""
import numpy as np
from .lake_models import incremental_pca
from .transfer_models import LinearHead

CAPABILITIES={
 'raw_ridge_logistic':'WORKING_OFFLINE','raw_histogram_tree':'WORKING_OFFLINE_OPTIONAL_SKLEARN',
 'incremental_pca':'WORKING_OFFLINE','incremental_svd':'WORKING_OFFLINE',
 'compact_supervised_tcn':'WORKING_OFFLINE','masked_observation_tcn':'WORKING_OFFLINE',
 'multitask_tcn':'WORKING_OFFLINE','specific_tcn':'WORKING_OFFLINE',
 'native_direct_query':'WORKING_OFFLINE_IN_MEMORY','whole_answer_cache':'WORKING_OFFLINE_IN_MEMORY',
 'materialized_embedding_heads':'WORKING_OFFLINE_ARRAY_INTERFACE',
 'pinned_vase_full_profiles':'EXISTING_BOUNDED_WORKER_ONLY_REVIEW_SCALING',
 'spatial_fragmentation':'NEEDS_SCIENTIFIC_DEFINITION','environmental_alignment':'NEEDS_SCIENTIFIC_DEFINITION',
 'developmental_stage_classes':'NEEDS_SCIENTIFIC_CRITERIA',
 'full_lake_model_selection_and_publication':'PENDING_AUTHORIZATION_AND_REVIEWED_BINDINGS'}


def prefix_tensor(windows,max_days=30):
    if not 3<=max_days<=30:raise ValueError('registered observed-window bound')
    x=np.zeros((len(windows),max_days,4))
    for i,window in enumerate(windows):
        if not 3<=len(window)<=max_days:raise ValueError('no truncation or shorter-than-reviewed window')
        if any(r.area_km2 is None or r.native_date is None for r in window):raise ValueError('unknown observations are not zeros')
        if any((b.native_date-a.native_date).days!=1 or a.event_key!=b.event_key for a,b in zip(window,window[1:])):raise ValueError('unsupported temporal/event support')
        g=np.asarray([r.area_km2 for r in window])
        if not np.isfinite(g).all() or (g<0).any():raise ValueError('invalid native increments')
        n=len(g);x[i,-n:,0]=np.log1p(g);x[i,-n:,1]=np.log1p(np.cumsum(g));x[i,-n:,2]=1.;x[i,-n:,3]=np.log1p(n)
    return x


def prefix_summaries(windows):
    x=prefix_tensor(windows);out=[]
    for a in x:
        use=a[:,2]==1;g=np.expm1(a[use,0]);v=a[use,0]
        out.append([v[-1],v.mean(),v.std(),np.log1p(g.sum()),v[-1]-v[-2],float(np.mean(g==0)),np.log1p(len(g)),np.log1p(g[:len(g)//2].sum()),v[-3:].mean()])
    return np.asarray(out)


def incremental_svd(batches,components):
    gram=None;n=0
    for a in batches:
        a=np.asarray(a,dtype=float)
        if a.ndim!=2 or not np.isfinite(a).all():raise ValueError('finite scientific features required')
        if gram is None:gram=np.zeros((a.shape[1],a.shape[1]))
        if a.shape[1]!=len(gram):raise ValueError('layout changed')
        gram+=a.T@a;n+=len(a)
    if gram is None or not 1<=components<=min(n,len(gram)):raise ValueError('unsupported SVD rank')
    values,vectors=np.linalg.eigh(gram);order=np.argsort(values)[::-1][:components]
    return {'components':vectors[:,order].T,'singular_values':np.sqrt(np.maximum(0,values[order])),'training_samples':n,'definition':'uncentered truncated SVD; not interchangeable with centered PCA'}


def fit_conventional(method,x,y,*,binary=False,seed=731):
    if method=='raw_ridge_logistic':return LinearHead().fit(x,y,binary=binary)
    if method=='raw_histogram_tree':
        # Optional dependency; absence is an explicit error, never a different model.
        from sklearn.ensemble import HistGradientBoostingClassifier,HistGradientBoostingRegressor
        cls=HistGradientBoostingClassifier if binary else HistGradientBoostingRegressor
        model=cls(max_iter=100,max_leaf_nodes=15,learning_rate=.05,random_state=seed)
        return model.fit(x,y)
    raise ValueError('unregistered conventional model')


def exact_neighbors(query,gallery,event_keys,query_event,k):
    allowed=np.flatnonzero(np.asarray(event_keys)!=query_event)
    if k<1 or len(allowed)<k:raise ValueError('unsupported distinct-fire gallery')
    # O(gallery) memory, no N-by-N distance matrix. Caller can partition gallery.
    distances=np.sum((np.asarray(gallery)[allowed]-np.asarray(query))**2,axis=1)
    order=np.lexsort((allowed,distances))[:k]
    return allowed[order].tolist()
