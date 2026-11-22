"""Native short-history state and explicit task answerability; no model fitting."""
from dataclasses import dataclass
from datetime import date
import math

@dataclass(frozen=True)
class ShortObservation:
    area: float
    day: date
    source_ref: str


def views(observations):
    """One/two retained observations, including gappy pairs; never fill support."""
    obs=tuple(observations)
    if len(obs) not in (1,2):raise ValueError('short-history view requires one or two observations')
    if any(isinstance(o.area,bool) or not math.isfinite(o.area) or o.area<0 or not isinstance(o.day,date) for o in obs):raise ValueError('supported native values and dates required')
    obs=tuple(sorted(obs,key=lambda o:o.day))
    if len(obs)==2 and obs[0].day==obs[1].day:raise ValueError('ambiguous duplicate date')
    values=tuple(o.area for o in obs);total=math.fsum(values)
    sidecar={'observation_count':len(obs),'dates':tuple(o.day.isoformat() for o in obs),'source_refs':tuple(o.source_ref for o in obs),'date_gap_days':(obs[-1].day-obs[0].day).days if len(obs)==2 else None}
    # first/last are sufficient to retain the actual values for n<=2, with no
    # subtraction-based reconstruction and no final-event metadata.
    summary={'first':values[0],'second':values[1] if len(obs)==2 else None,'observed_total':total}
    normalized=tuple(v/total for v in values) if total>0 else None
    return {'sidecar':sidecar,'native':values,'summary':summary,'normalized_allocation':normalized,
      'normalization_defined':total>0,'observed_total':total,'change_between_observed_increments':values[1]-values[0] if len(obs)==2 else None}


def summary_values(view):
    s=view['summary'];return (s['first'],) if view['sidecar']['observation_count']==1 else (s['first'],s['second'])


def capabilities(length):
    if length<1:raise ValueError('observed history must be nonempty')
    return {'observed_count':'SUPPORTED','observed_absolute_area':'SUPPORTED','observed_support':'SUPPORTED',
      'between_observation_order':'NOT_APPLICABLE' if length==1 else 'SUPPORTED_WHERE_DATES_UNAMBIGUOUS',
      'observed_allocation_shape':'NOT_APPLICABLE' if length==1 else 'SUPPORTED_IF_POSITIVE_TOTAL',
      'physical_lifetime':'UNKNOWN','physical_extinction':'UNKNOWN',
      'future_growth_from_completed_record':'REQUIRES_SEPARATE_PAST_FUTURE_SUPPORT'}
