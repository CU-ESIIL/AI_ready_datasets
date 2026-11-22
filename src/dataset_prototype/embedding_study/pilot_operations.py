"""Prewritten bounded synthetic operations, optimized direct baselines and view isolation."""
from time import perf_counter_ns
import math
import numpy as np
from ..contracts import digest
from .representations import InsufficientInformation, coordinates
from .pilot_contracts import PilotQuery, OPS, CLAIMS

CONTRACTS = {
 'cumulative':'Available dated cumulative observation; absolute km2. No inferred missing values.',
 'daily_growth':'One calendar-day evidenced difference; no result for unknown baseline or gap.',
 'interval_growth':'Difference of available dated cumulative endpoints, km2; not a daily rate.',
 'growth_compare':'First fire interval total minus second fire interval total, km2; both endpoints required.',
 'front_fraction':'Mass allocated to first half of completed development, exact normalized linear-time integration.',
 'late_fraction':'Mass allocated to last quarter of completed development, exact normalized integration.',
 'profile':'Exact mass-conserving 20-bin full profile, not a PCA reconstruction.',
 'profile_distance':'Exact Euclidean distance in full 20-bin profile units.',
 'pulse_count':'Pinned padded 20%-prominence detector on original increments, count only; R1 retains this trait.',
 'pca_distance':'Exact Euclidean distance in frozen standardized three-PC coordinates; no ecological meaning asserted.',
 'projected_distance':'Euclidean distance between backprojected three-PC profiles in original profile units; exact for this projected target, approximate for full-profile geometry.',
 'reconstruction_error':'L2 distance between original 20-bin profile and its three-PC backprojection. Coordinates alone lack discarded residual.',
 'neighbor_stability':'Compare top-one full-profile and backprojected-profile rankings on exactly three candidates; ties broken by offered ID. Needs both full and projected geometry.',
 'assess_claim':'Evidence assessment for a supplied general scientific claim; unsupported claims remain unsupported, no ecological gold invented.',
 'source_evidence':'Return retained source version, checksum scope, license, synthetic status and availability/uncertainty evidence. Provenance is not scientific approval.'}
REQUIRES_PROFILE = {'front_fraction','late_fraction','profile','profile_distance','pulse_count','pca_distance',
 'projected_distance','reconstruction_error','neighbor_stability'}


def direct_fraction(h, start, stop):
    """Integral of constant daily allocation density over [start, stop].

    Equivalent to upstream CDF interpolation, without constructing all traits/profile.
    Preconditions match the primary completed-profile definition.
    """
    if not h.profile_eligible:raise InsufficientInformation('primary profile preconditions')
    g=h.growth;n=len(g);total=math.fsum(g)
    return math.fsum(value*max(0., min(stop*n,i+1)-max(start*n,i)) for i,value in enumerate(g))/total


def observed(h, day, daily=False, index=None):
    row=index.get(day) if index is not None else next((r for r in h.observations if r.date==day and r.available),None)
    if row is None:raise InsufficientInformation('unavailable observation')
    if not daily:return row.cumulative_area
    prior=[r for r in h.observations if r.available and r.date<day]
    previous_day,previous_value=(prior[-1].date,prior[-1].cumulative_area) if prior else (h.baseline_date,h.baseline_area)
    if previous_day is None or previous_value is None or (day-previous_day).days!=1:
        raise InsufficientInformation('not evidenced daily support')
    return row.cumulative_area-previous_value


def assess_claim(claim, lineage):
    # Fixed evidence-scope rules, never a model judgment or ecological equivalence.
    if claim=='duration_from_sidecar':
        return {'supported':True,'value':len(lineage['observation_ids']),'scope':'validated_consecutive_intervals'} if lineage['primary_profile_eligible'] else {'supported':False,'value':None,'scope':'insufficient_support'}
    scopes={'absolute_from_normalized':'normalization_discards_absolute_scale',
      'exact_profile_from_pcs':'truncation_loses_residual','ecological_analog':'no_independent_relevance_labels',
      'measurement_uncertainty':'no_real_measurement_model','forecast_availability':'availability_times_unknown'}
    if claim not in CLAIMS:raise ValueError('unknown scientific claim')
    return {'supported':False,'value':None,'scope':scopes[claim]}


class PilotView:
    def __init__(self, base):
        self.base=base;self.representation=base.representation
        self.payloads=base.payloads;self.lineages=base.lineages;self.backend=base.backend;self.artifact=base.artifact
        self.cache={};self.last_cache_hit=False;self.last_logical_bytes=0
        import json
        self.payload_bytes={i:len((p.model_dump_json() if self.representation=='R0' else json.dumps(p)).encode()) for i,p in self.payloads.items()}
        self.native_indexes={}
        if self.representation=='R0':
            self.native_indexes={i:{o.date:o for o in h.observations if o.available} for i,h in self.payloads.items()}
    def clear(self):self.cache.clear();self.base.cache.clear()
    def profile(self,i):return np.array(self.base._profile(i)['profile'])
    def coords(self,i):return np.asarray(self.base._coordinates(i))
    def backproject(self,i):return (self.coords(i)@np.asarray(self.artifact.components))*self.artifact.scale+self.artifact.mean
    def query(self,q):
        PilotQuery.model_validate(q.model_dump())
        key=digest({'query':q.model_dump(mode='json'),'artifact':self.artifact.artifact_digest,
            'sources':[self.lineages[i]['history_digest'] for i in (*q.fire_ids,*q.candidates)],'version':'pilot-operations-v3'})
        self.last_cache_hit=key in self.cache;self.last_logical_bytes=0
        if key in self.cache:return self.cache[key]
        self.last_logical_bytes=sum(self.payload_bytes[i] for i in (*q.fire_ids,*q.candidates))
        try:value=self.execute(q)
        except InsufficientInformation as exc:result={'answer':None,'abstention':True,'reason':str(exc),'unit':q.unit,'approximate':False}
        else:result={'answer':value,'abstention':False,'reason':None,'unit':q.unit,'approximate':q.operation=='projected_distance'}
        self.cache[key]=result;return result
    def execute(self,q):
        op=q.operation;i=q.fire_ids[0];r=self.representation
        if op not in OPS:raise ValueError('closed operation registry')
        if op=='assess_claim':return assess_claim(q.claim,self.lineages[i])
        if op=='source_evidence':
            s=self.lineages[i]['source']
            return {k:s[k] for k in ('version','checksum_scope','license','synthetic','uncertainty','temporal_support')}
        if op in {'cumulative','daily_growth','interval_growth','growth_compare'}:
            if r!='R0':raise InsufficientInformation('native dated values required')
            def interval(identifier):
                h=self.payloads[identifier]
                return observed(h,q.date,index=self.native_indexes[identifier])-observed(h,q.start_date,index=self.native_indexes[identifier])
            if op=='growth_compare':return interval(i)-interval(q.fire_ids[1])
            if op=='interval_growth':return interval(i)
            return observed(self.payloads[i],q.date,op=='daily_growth',self.native_indexes[i])
        if op in {'front_fraction','late_fraction'}:
            if r=='R0':return direct_fraction(self.payloads[i],0.,.5) if op=='front_fraction' else direct_fraction(self.payloads[i],.75,1.)
            if r!='R1' or self.payloads[i] is None:raise InsufficientInformation('exact allocation required')
            return self.payloads[i]['traits']['front_loaded_fraction' if op=='front_fraction' else 'late_growth_fraction']
        if op=='pulse_count':
            if r=='R0':
                h=self.payloads[i]
                if not h.profile_eligible:raise InsufficientInformation('primary profile preconditions')
                return self.backend.call('pulses',list(h.growth))['pulse_count']
            if r=='R1' and self.payloads[i] is not None:return int(self.payloads[i]['traits']['pulse_count'])
            raise InsufficientInformation('pulse trait absent')
        if op=='profile':return self.profile(i).tolist()
        if op=='profile_distance':return float(np.linalg.norm(self.profile(i)-self.profile(q.fire_ids[1])))
        if op=='pca_distance':return float(np.linalg.norm(self.coords(i)-self.coords(q.fire_ids[1])))
        if op=='projected_distance':return float(np.linalg.norm(self.backproject(i)-self.backproject(q.fire_ids[1])))
        if op=='reconstruction_error':return float(np.linalg.norm(self.profile(i)-self.backproject(i)))
        if op=='neighbor_stability':
            distances=lambda f:sorted((float(np.linalg.norm(f(i)-f(c))),c) for c in q.candidates)
            a,b=distances(self.profile)[0][1],distances(self.backproject)[0][1]
            return {'stable':a==b,'full_neighbor':a,'projected_neighbor':b}
        raise ValueError('unimplemented registered operation')
