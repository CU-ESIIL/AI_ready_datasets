"""Predeclared splits, learning curves, clustered comparisons and cost frontiers."""
import hashlib
import numpy as np


def fold_for_fire(event_year,region,*,selection_years,calibration_years,test_years,heldout_regions,training_years):
    groups=[set(training_years),set(selection_years),set(calibration_years),set(test_years)]
    if any(groups[i]&groups[j] for i in range(4) for j in range(i+1,4)):raise ValueError('year blocks overlap')
    if region is None:return 'NEEDS_REGION_EVIDENCE'
    if region in heldout_regions:return 'geographic_test'
    for fold,years in zip(('train','selection','calibration','temporal_test'),groups):
        if event_year in years:return fold
    return 'excluded_year_support'


def learning_fraction(event_key,fraction,seed):
    if not 0<fraction<=1:raise ValueError('fraction in (0,1]')
    value=int(hashlib.sha256((str(seed)+':'+event_key).encode()).hexdigest()[:16],16)/2**64
    return value<fraction


def clustered_effect(differences,clusters,replicates,seed):
    if len(differences)!=len(clusters) or not differences:raise ValueError('paired cluster contributions required')
    labels=sorted(set(clusters));values=np.array([np.mean([d for d,c in zip(differences,clusters) if c==label]) for label in labels])
    rng=np.random.default_rng(seed);boot=values[rng.integers(0,len(values),(replicates,len(values)))].mean(1)
    return {'clusters':len(labels),'effect':float(values.mean()),'interval':np.quantile(boot,[.025,.975]).tolist(),
      'scope':'conditional fitted-model empirical cluster resampling, not automatically wildfire-population or training uncertainty'}


def holm_adjust(pvalues):
    p=np.asarray(pvalues,dtype=float)
    if p.ndim!=1 or not np.isfinite(p).all() or ((p<0)|(p>1)).any():raise ValueError('valid prespecified family p-values required')
    order=np.argsort(p);adjusted=np.maximum.accumulate([(len(p)-i)*p[j] for i,j in enumerate(order)])
    out=np.empty_like(p);out[order]=np.minimum(1,adjusted);return out.tolist()


def pareto(rows):
    """Same predeclared task/metric/acceptance target only; unknown costs not zero."""
    if not rows:return []
    if len({(r['task'],r['metric'],r['requirements_digest']) for r in rows})!=1:raise ValueError('incomparable scientific tasks/requirements')
    valid=[r for r in rows if r['scientifically_valid'] and r['cost'] is not None and r['loss'] is not None]
    for r in valid:
        if not np.isfinite(r['cost']) or not np.isfinite(r['loss']) or r['cost']<0:raise ValueError('finite measured cost/loss required')
    return [r['method'] for r in valid if not any(o['cost']<=r['cost'] and o['loss']<=r['loss'] and (o['cost']<r['cost'] or o['loss']<r['loss']) for o in valid)]


def lifecycle_cost(*,training,loading,harmonization,features,materialization,query,count,refresh,refreshes):
    values=(training,loading,harmonization,features,materialization,query,refresh)
    if any(v is None for v in values):return None
    if any(not np.isfinite(v) or v<0 for v in values) or count<0 or refreshes<0:raise ValueError('nonnegative finite costs')
    return training+loading+harmonization+features+materialization+query*count+refresh*refreshes
