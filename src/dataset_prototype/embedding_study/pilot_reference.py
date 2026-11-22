"""Independent Fraction/SVD and exhaustive prominence oracles; no executor imports."""
from fractions import Fraction as F
import math
import numpy as np
from .reference import profile_oracle, growth_oracle


def pulse_oracle(h):
    """Exhaustive contour prominence with padded zeros, independent of scipy peaks.

    For each maximal plateau, seek the first strictly higher sample each way;
    prominence is height minus the higher of the two intervening minima.
    """
    x=[0.,*growth_oracle(h),0.];peaks=[];j=1
    while j<len(x)-1:
        k=j
        while k+1<len(x) and x[k+1]==x[j]:k+=1
        if k<len(x)-1 and x[j]>x[j-1] and x[k]>x[k+1]:
            left=j-1;right=k+1
            while left>0 and x[left]<=x[j]:left-=1
            while right<len(x)-1 and x[right]<=x[j]:right+=1
            prominence=x[j]-max(min(x[left:j+1]),min(x[k:right+1]))
            if prominence>=.2*max(x):peaks.append((j+k)//2-1)
        j=k+1
    return len(peaks)


def rational_fraction(h,start,stop):
    g=[F(str(v)) for v in growth_oracle(h)];n=len(g)
    return float(sum(v*n*max(F(0),min(stop,F(k+1,n))-max(start,F(k,n))) for k,v in enumerate(g))/sum(g))


class PilotReference:
    def __init__(self,dataset):
        self.histories={h.fire_id:h for h in dataset.histories}
        self.profiles={i:profile_oracle(h) for i,h in self.histories.items() if h.profile_eligible}
        training=[h.fire_id for h in dataset.histories if h.split=='train' and h.profile_eligible]
        x=np.asarray([self.profiles[i] for i in training]);self.mean=x.mean(0);self.scale=x.std(0)
        self.scale[self.scale<1e-12]=1
        _,s,vt=np.linalg.svd((x-self.mean)/self.scale,full_matrices=False)
        if abs(s[2]-s[3])<1e-9:raise ValueError('ambiguous truncation')
        self.components=vt[:3]
        self.coordinates={i:(np.asarray(p)-self.mean)/self.scale@self.components.T for i,p in self.profiles.items()}
        self.recon={i:z@self.components*self.scale+self.mean for i,z in self.coordinates.items()}
    def daily(self,h,day):
        prev,area=h.baseline_date,h.baseline_area
        for row in h.observations:
            if row.date==day:
                if not row.available or prev is None or (day-prev).days!=1:return None
                return float(F(str(row.cumulative_area))-F(str(area)))
            if row.available:prev,area=row.date,row.cumulative_area
        return None
    def answer(self,q):
        op=q.operation;i=q.fire_ids[0];h=self.histories[i]
        if op=='source_evidence':
            return {k:getattr(h.source,k) for k in ('version','checksum_scope','license','synthetic','uncertainty','temporal_support')}
        if op=='assess_claim':
            rubric={'absolute_from_normalized':'normalization_discards_absolute_scale','exact_profile_from_pcs':'truncation_loses_residual',
              'ecological_analog':'no_independent_relevance_labels','measurement_uncertainty':'no_real_measurement_model',
              'forecast_availability':'availability_times_unknown'}
            if q.claim=='duration_from_sidecar':
                if h.profile_eligible:return {'supported':True,'value':len(h.observations),'scope':'validated_consecutive_intervals'}
                return {'supported':False,'value':None,'scope':'insufficient_support'}
            return {'supported':False,'value':None,'scope':rubric[q.claim]}
        if op in {'cumulative','interval_growth','growth_compare','daily_growth'}:
            def area(identifier,day):
                return next((F(str(r.cumulative_area)) for r in self.histories[identifier].observations if r.date==day and r.available),None)
            def interval(identifier):
                a,b=area(identifier,q.date),area(identifier,q.start_date)
                return None if a is None or b is None else a-b
            if op=='daily_growth':return self.daily(h,q.date)
            if op=='cumulative':
                v=area(i,q.date);return float(v) if v is not None else None
            v=interval(i)
            if op=='growth_compare':
                w=interval(q.fire_ids[1]);v=None if v is None or w is None else v-w
            return float(v) if v is not None else None
        if i not in self.profiles or any(j not in self.profiles for j in (*q.fire_ids,*q.candidates)):return None
        if op=='front_fraction':return rational_fraction(h,F(0),F(1,2))
        if op=='late_fraction':return rational_fraction(h,F(3,4),F(1))
        if op=='pulse_count':return pulse_oracle(h)
        if op=='profile':return self.profiles[i]
        distance=lambda a,b:math.sqrt(math.fsum((float(x)-float(y))**2 for x,y in zip(a,b)))
        if op in {'profile_distance','pca_distance','projected_distance'}:
            source={'profile_distance':self.profiles,'pca_distance':self.coordinates,'projected_distance':self.recon}[op]
            return distance(source[i],source[q.fire_ids[1]])
        if op=='reconstruction_error':return distance(self.profiles[i],self.recon[i])
        if op=='neighbor_stability':
            a=min((distance(self.profiles[i],self.profiles[c]),c) for c in q.candidates)[1]
            b=min((distance(self.recon[i],self.recon[c]),c) for c in q.candidates)[1]
            return {'stable':a==b,'full_neighbor':a,'projected_neighbor':b}
        raise ValueError('missing independent reference')
    def sufficient(self,q,r):
        if self.answer(q) is None:return False
        if q.operation in {'assess_claim','source_evidence'}:return True
        if q.operation in {'cumulative','daily_growth','interval_growth','growth_compare'}:return r=='R0'
        if q.operation in {'pca_distance','projected_distance'}:return True
        return r!='R2'
