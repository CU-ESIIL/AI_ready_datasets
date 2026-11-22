"""Independent future-observation targets, no encoder or training imports."""
from datetime import date,timedelta
from fractions import Fraction
import math
import numpy as np
from ..contracts import digest


def future_targets(prefix,history,horizon=3):
    if horizon!=3 or prefix.fire_id!=history['fire_id']:raise ValueError('fixed cohort/horizon')
    start=(prefix.dates[-1]-date.fromisoformat(history['first_date'])).days+1
    values=history['growth_km2_day'][start:start+horizon]
    if len(values)!=horizon:raise ValueError('unavailable future support')
    f=np.asarray(values,dtype=float);recent=np.array(prefix.growth_km2_day[-3:])
    targets=np.array([np.log1p(f[0]),np.log1p(f.sum()),float(f.mean()>recent.mean()),np.log1p(f.std(ddof=0))])
    # Separate rational/pairwise references avoid grading by model/executor outputs.
    rational=[Fraction(str(v)) for v in values]
    reference=[math.log1p(values[0]),math.log1p(float(sum(rational))),
      float(sum(rational)>sum(Fraction(str(v)) for v in prefix.growth_km2_day[-3:])),
      math.log1p(math.sqrt(float(sum((a-b)**2 for j,a in enumerate(rational) for b in rational[j+1:])))/horizon)]
    if not np.allclose(targets,reference,rtol=0,atol=1e-12):raise ValueError('independent future target disagreement')
    return targets,np.log1p(f),{'prefix_digest':digest(prefix),'future_observation_ids':[prefix.fire_id+f':D{start+j}' for j in range(horizon)],
      'future_dates':[str(prefix.dates[-1]+timedelta(days=j+1)) for j in range(horizon)],'canonical_future_growth':values,
      'target_values':targets.tolist(),'scientific_scope':'synthetic observed outcomes; mathematical relevance only'}


def property_targets(prefixes):
    rows=[]
    for p in prefixes:
        g=np.asarray(p.growth_km2_day);n=len(g)
        if g.sum()<=0:raise ValueError('centroid diagnostic needs positive observed total')
        peaks=sum(g[j]>g[j-1] and g[j]>g[j+1] for j in range(1,n-1))
        rows.append([np.log1p(g.sum()),float(np.dot(np.arange(n)/(n-1),g)/g.sum()),np.log1p(g[-1]),
          np.arcsinh(g[-1]-g[-2]),np.log1p(peaks),np.log1p(g.std(ddof=0))])
    return np.asarray(rows)

PROPERTY_NAMES=('absolute_scale_log_total','order_mass_centroid','recent_log_growth','recent_acceleration_asinh',
 'strict_interior_local_maxima_log_count','observed_variability_log_std')
