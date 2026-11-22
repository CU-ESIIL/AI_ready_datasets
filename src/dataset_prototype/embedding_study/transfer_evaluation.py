"""Task-level scoring, fire-paired uncertainty and future-outcome retrieval."""
import numpy as np
from .transfer_models import sigmoid


def score(y,p,binary=False,radius=None):
    if binary:
        q=np.clip(p,1e-12,1-1e-12);bins=np.minimum((q*10).astype(int),9);ece=0.;reliability=[]
        for b in range(10):
            use=bins==b
            if use.any():
                mean_p=float(q[use].mean());rate=float(y[use].mean());ece+=use.mean()*abs(mean_p-rate);reliability.append({'bin':b,'n':int(use.sum()),'probability':mean_p,'observed_rate':rate})
        return {'n':len(y),'brier':float(np.mean((q-y)**2)),'log_loss':float(-np.mean(y*np.log(q)+(1-y)*np.log(1-q))),
          'accuracy':float(np.mean((q>=.5)==y)),'ece_10_fixed_bins':float(ece),'reliability':reliability}
    result={'n':len(y),'mse_log1p':float(np.mean((p-y)**2)),
      'mae_original_units':float(np.mean(np.abs(np.expm1(np.maximum(0,p))-np.expm1(y))))}
    if radius is not None:
        result.update(coverage_90=float(np.mean(np.abs(y-p)<=radius)),mean_interval_width_original=float(np.mean(np.expm1(np.maximum(0,p+radius))-np.expm1(np.maximum(0,p-radius)))))
    return result


def paired_fire_delta(y,p,raw,fire_ids,replicates,seed):
    ids=sorted(set(fire_ids));values=[]
    for identifier in ids:
        keep=np.asarray(fire_ids)==identifier;values.append(float(np.mean((raw[keep]-y[keep])**2-(p[keep]-y[keep])**2)))
    values=np.asarray(values);rng=np.random.default_rng(seed);means=values[rng.integers(0,len(values),(replicates,len(values)))].mean(1)
    return {'fires':len(ids),'raw_minus_method_mean_squared_loss':float(values.mean()),
      'descriptive_fire_resampling_95_interval':np.quantile(means,[.025,.975]).tolist(),
      'per_fire_differences':dict(zip(ids,values.tolist())),
      'scope':'paired descriptive empirical-fire resampling conditional on fitted/selected models; no refit, wildfire population or multiplicity-adjusted significance'}


def ranks(values):
    a=np.asarray(values);order=np.argsort(a,kind='stable');out=np.empty(len(a));j=0
    while j<len(a):
        k=j+1
        while k<len(a) and a[order[k]]==a[order[j]]:k+=1
        out[order[j:k]]=(j+k-1)/2;j=k
    return out


def retrieval(vectors,future,fire_ids,k=10):
    rows=[];ids=np.asarray(fire_ids)
    for i in range(len(vectors)):
        candidates=np.flatnonzero(ids!=ids[i])
        if len(candidates)<k:raise ValueError('insufficient distinct-fire candidate support')
        distance=np.sum((vectors[candidates]-vectors[i])**2,axis=1)
        truth=np.sum((future[candidates]-future[i])**2,axis=1)
        # Stable row order resolves exact ties in both spaces; tied ranks averaged for correlation.
        chosen=candidates[np.argsort(distance,kind='stable')[:k]];relevant=candidates[np.argsort(truth,kind='stable')[:k]]
        overlap=len(set(chosen)&set(relevant))/k;a,b=ranks(distance),ranks(truth)
        corr=float(np.corrcoef(a,b)[0,1]) if np.std(a)>0 and np.std(b)>0 else None
        rows.append({'query_index':i,'fire_id':str(ids[i]),'candidate_count':len(candidates),'precision_at_k':overlap,'recall_at_k':overlap,
          'spearman_distance_rank':corr,'selected_indices':chosen.tolist(),'relevant_indices':relevant.tolist()})
    by_fire={i:float(np.mean([r['precision_at_k'] for r in rows if r['fire_id']==i])) for i in sorted(set(fire_ids))}
    return {'k':k,'query_prefixes':len(rows),'fires':len(by_fire),'mean_fire_precision_at_k':float(np.mean(list(by_fire.values()))),
      'mean_fire_recall_at_k':float(np.mean(list(by_fire.values()))),'mean_rank_correlation':float(np.mean([r['spearman_distance_rank'] for r in rows if r['spearman_distance_rank'] is not None])) if any(r['spearman_distance_rank'] is not None for r in rows) else None,
      'per_fire_precision':by_fire,'rows':rows,'scope':'future-observation mathematical relevance, not ecological analogs; same-fire prefixes excluded; recall equals precision because both sets have k elements'}


def regression_radius(y,p):
    a=np.sort(np.abs(y-p));return float(a[min(len(a),int(np.ceil(.9*(len(a)+1))))-1])


def standardize(train,other):
    mean=train.mean(0);scale=train.std(0);scale[scale<1e-8]=1
    return (other-mean)/scale
