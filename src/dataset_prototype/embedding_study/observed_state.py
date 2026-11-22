"""Versioned observed-property state, not a complete-history/physical-rate recipe."""
from datetime import date
from fractions import Fraction
import math
import numpy as np
NAMES=('log_observed_total','log_observation_count','log_first_increment','log_last_increment','log_observed_std','first_allocation','asinh_mean_consecutive_change','strict_interior_peak_count','first_half_allocation','log_observed_span')


def calculate(areas,days):
    a=np.asarray(areas,dtype=float);d=np.asarray(days,dtype=np.int64);n=len(a)
    if n<1 or len(d)!=n or not np.isfinite(a).all() or (a<0).any() or (np.diff(d)<=0).any():raise ValueError('unique increasing dates and finite nonnegative observed areas required')
    total=math.fsum(areas);reference=float(sum(Fraction(str(v)) for v in areas))
    if not math.isclose(total,reference,rel_tol=1e-12,abs_tol=1e-9):raise ValueError('independent observed sum mismatch')
    values=np.full(10,np.nan);mask=np.zeros(10,dtype=bool)
    values[:4]=[math.log1p(total),math.log1p(n),math.log1p(a[0]),math.log1p(a[-1])];mask[:4]=True
    if n>=2:
        sd=math.sqrt(math.fsum((float(v)-total/n)**2 for v in a)/n)
        if not math.isclose(sd,float(np.std(a)),rel_tol=1e-10,abs_tol=1e-9):raise ValueError('variance reference mismatch')
        values[4]=math.log1p(sd);mask[4]=True
        if total>0:values[5]=a[0]/total;values[8]=math.fsum(a[:n//2])/total;mask[[5,8]]=True
    gaps=np.diff(d);eligible=gaps==1
    if eligible.any():values[6]=math.asinh(float(np.diff(a)[eligible].mean()));mask[6]=True
    triples=(gaps[:-1]==1)&(gaps[1:]==1)
    if triples.any():
        peaks=int(np.sum((a[1:-1]>a[:-2])&(a[1:-1]>a[2:])&triples));ref=sum(1 for i in range(1,n-1) if d[i]-d[i-1]==1 and d[i+1]-d[i]==1 and a[i]>a[i-1] and a[i]>a[i+1]);assert peaks==ref
        values[7]=peaks;mask[7]=True
    values[9]=math.log1p(int(d[-1]-d[0]));mask[9]=True
    return values,mask


def prediction_examples(areas,days,depth,horizon):
    """Exact supported short prefixes; future labels never enter their state."""
    if depth not in (1,2) or horizon not in (1,3,7):raise ValueError('registered short-prefix support')
    for start in range(len(areas)-depth-horizon+1):
        stop=start+depth+horizon
        if any(days[k+1]-days[k]!=1 for k in range(start,stop-1)):continue
        values,mask=calculate(areas[start:start+depth],days[start:start+depth]);future=areas[start+depth:stop];target=math.fsum(future);reference=float(sum(Fraction(str(v)) for v in future))
        if not math.isclose(target,reference,rel_tol=1e-12,abs_tol=1e-9):raise ValueError('future reference mismatch')
        yield start,values,mask,math.log1p(target),math.log1p(areas[start+depth-1]*horizon)
