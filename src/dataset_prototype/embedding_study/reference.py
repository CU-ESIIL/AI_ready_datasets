"""Independent synthetic answer keys: rational interval integration and SVD.

No upstream call, representation-store output or model answer enters this module.
The fractional integration is an independent oracle for a declared synthetic task,
not a new real-data harmonization recipe.
"""
from fractions import Fraction
import math
import numpy as np
from .contracts import Dataset


def growth_oracle(history):
    """Independent cumulative-area differences, ignoring supplied derived growth."""
    previous_date,previous_area=history.baseline_date,history.baseline_area
    values=[]
    for row in history.observations:
        if (not row.available or previous_date is None or previous_area is None
                or (row.date-previous_date).days != 1):
            raise ValueError('independent daily oracle needs evidenced consecutive observations')
        values.append(float(Fraction(str(row.cumulative_area))-Fraction(str(previous_area))))
        previous_date,previous_area=row.date,row.cumulative_area
    return tuple(values)


def profile_oracle(history):
    """Integrate original daily mass on overlapping rational [0,1] intervals."""
    g = [Fraction(str(x)) for x in growth_oracle(history)]
    probabilities = [x/sum(g) for x in g]
    n = len(g)
    result = []
    for j in range(20):
        lo, hi = Fraction(j,20), Fraction(j+1,20)
        result.append(float(sum(p*n*max(Fraction(0),min(hi,Fraction(i+1,n))-max(lo,Fraction(i,n)))
            for i,p in enumerate(probabilities))))
    return result


def front_oracle(history):
    g = [Fraction(str(x)) for x in growth_oracle(history)]
    n = len(g)
    return float(sum(x*n*max(Fraction(0), min(Fraction(1,2),Fraction(i+1,n))-Fraction(i,n))
        for i,x in enumerate(g))/sum(g))


class ReferenceAnswers:
    def __init__(self, dataset: Dataset, components):
        self.histories = {h.fire_id:h for h in dataset.histories}
        self.profiles = {h.fire_id:profile_oracle(h) for h in dataset.histories if h.profile_eligible}
        training = [h.fire_id for h in dataset.histories if h.split=='train' and h.profile_eligible]
        if not 1 <= components <= min(10,len(training)-1):
            raise ValueError('independent PCA reference requires enough declared training fires')
        x = np.array([self.profiles[i] for i in training])
        mean, scale = x.mean(0), x.std(0)
        scale[scale<1e-12] = 1
        _, singular, vt = np.linalg.svd((x-mean)/scale, full_matrices=False)
        # Distance is invariant to eigenvector signs. Degenerate truncation would
        # make this reference ambiguous; fail rather than pick a hidden rotation.
        if components < len(singular) and abs(singular[components-1]-singular[components]) < 1e-9:
            raise ValueError('PCA reference truncates a tied subspace')
        self.coordinates = {i:((np.array(p)-mean)/scale)@vt[:components].T for i,p in self.profiles.items()}

    def answer(self, task):
        h = self.histories[task.fire_ids[0]]
        rows = {o.date:o for o in h.observations if o.available}
        op = task.operation
        if op == 'cumulative':
            return rows[task.date].cumulative_area if task.date in rows else None
        if op == 'interval_growth':
            if task.date not in rows or task.start_date not in rows:
                return None
            return rows[task.date].cumulative_area-rows[task.start_date].cumulative_area
        if op == 'daily_growth':
            if task.date not in rows:
                return None
            previous_date,previous_area=h.baseline_date,h.baseline_area
            for row in h.observations:
                if row.available:
                    if row.date==task.date:
                        return row.cumulative_area-previous_area if previous_date is not None and (row.date-previous_date).days==1 else None
                    previous_date,previous_area=row.date,row.cumulative_area
            return None
        if op == 'scientific_analog':
            return None  # independent relevance is unavailable, never manufactured
        if op in {'maximum_daily_growth','peak_date','sequence_days','pulses'}:
            if not h.complete_sequence:
                return None
            g = growth_oracle(h)
        elif not h.profile_eligible:
            return None
        else:
            g = growth_oracle(h)
        if op == 'maximum_daily_growth':
            return max(g)
        if op == 'peak_date':
            return h.observations[g.index(max(g))].date.isoformat()
        if op == 'sequence_days':
            return len(g)  # evidenced baseline through final observation, not final−first
        if op == 'pulses':
            # Analytic truth declared in fixture task: test oracles must not call
            # the upstream prominence detector they are checking.
            if h.fire_id != 'eval-pulses':
                raise ValueError('no independently authored pulse oracle for this history')
            return {'count':2,'dates':[h.observations[i].date.isoformat() for i in (1,4)]}
        if op == 'profile':
            return self.profiles[h.fire_id]
        if op == 'front_fraction':
            return front_oracle(h)
        if op in {'profile_distance','pca_distance'}:
            other = task.fire_ids[1]
            source = self.profiles if op=='profile_distance' else self.coordinates
            if other not in source:
                return None
            return math.sqrt(sum((a-b)**2 for a,b in zip(source[h.fire_id],source[other])))
        if op == 'nearest_profile':
            q = self.profiles[h.fire_id]
            pairs = [(sum((a-b)**2 for a,b in zip(q,self.profiles[c])),c) for c in task.candidates]
            return [c for _,c in sorted(pairs)[:2]]
        raise ValueError('no independent reference for operation')
