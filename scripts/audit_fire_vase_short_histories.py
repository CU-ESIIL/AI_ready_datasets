"""Execute real short-history information/access audit; no neural/PCA/model fitting."""
import argparse,csv,hashlib,json,math,sqlite3,time,resource
from collections import Counter
from datetime import date
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.population_profile import DAILY,DAILY_TABLE,readonly,supported_day
from dataset_prototype.embedding_study.short_history import ShortObservation,views,summary_values,capabilities


def main():
    p=argparse.ArgumentParser();p.add_argument('--census',required=True);p.add_argument('--lake',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    census=Path(a.census);lake=Path(a.lake).resolve();out=Path(a.output);out.mkdir(parents=True,exist_ok=False)
    identity=next(r for r in json.loads((census/'source-verification.json').read_text()) if r['relative_path']==DAILY)
    stat=(lake/DAILY).stat()
    if (stat.st_size,stat.st_mtime_ns)!=(identity['bytes'],identity['mtime_ns']):raise ValueError('source identity changed; reverify before audit')
    started=time.perf_counter();counts=Counter();aggregates={1:Counter(),2:Counter()};min_area={1:float('inf'),2:float('inf')};max_area={1:0.,2:0.};sample={1:[],2:[]}
    totals={1:0.,2:0.};native_payload_bytes=Counter();summary_payload_bytes=Counter();normalized_payload_bytes=Counter()
    source_groups=0
    def process(identity_value,rows):
        nonlocal source_groups
        source_groups+=1;counts['all_observations']+=len(rows)
        if len(rows)>2:counts['three_plus']+=1;return
        n=len(rows);v=views([ShortObservation(float(area),supported_day(day),str(fid)) for fid,day,area in rows]);counts['one' if n==1 else 'two']+=1
        assert summary_values(v)==v['native']
        assert v['sidecar']['observation_count']==len(rows)
        assert v['sidecar']['dates']==tuple(sorted(day for _,day,_ in rows))
        aggregates[n]['native_values_exactly_preserved']+=1;aggregates[n]['dates_and_source_refs_retained']+=1
        aggregates[n]['normalization_defined']+=v['normalization_defined']
        aggregates[n]['normalized_payload_absolute_scale_unavailable_without_source_read']+=v['normalization_defined']
        aggregates[n]['consecutive_pairs']+=n==2 and v['sidecar']['date_gap_days']==1
        aggregates[n]['gappy_pairs']+=n==2 and v['sidecar']['date_gap_days']>1
        if n==1:
            assert v['normalized_allocation'] in ((1.,),None)
            aggregates[n]['one_value_allocation_is_constant']+=v['normalized_allocation']==(1.,)
        total=v['observed_total'];totals[n]+=total;min_area[n]=min(min_area[n],total);max_area[n]=max(max_area[n],total)
        sidecar={**v['sidecar'],'native_event_id':identity_value,'source_checksum':identity['sha256']}
        # The same full sidecar survives each condition; it never contains source values.
        for payload,destination in [(v['native'],native_payload_bytes),(v['summary'],summary_payload_bytes),(v['normalized_allocation'],normalized_payload_bytes)]:
            destination[n]+=len(json.dumps({'payload':payload,'lineage':sidecar},separators=(',',':'),sort_keys=True).encode())
        if len(sample[n])<64:sample[n].append((identity_value,tuple(rows)))
    with readonly(lake/DAILY) as source:
        current=None;buffer=[]
        for fid,identity_value,day,area in source.execute('SELECT fid,id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" ORDER BY id,date,fid'):
            if identity_value!=current:
                if buffer:process(current,buffer)
                current=identity_value;buffer=[]
            if len(buffer)>=8192:raise MemoryError('bounded native history exceeded')
            buffer.append((fid,day,area))
        if buffer:process(current,buffer)
        # Optimized source access uses the existing native primary key, never a
        # scan per query. Fixed first64 per stratum is a wiring/cost sample, not
        # representative latency inference; OS cache is warm from the full stream.
        latencies=[];checks=0
        for n,entries in sample.items():
            for identity_value,rows in entries:
                start=time.perf_counter_ns();recovered=[]
                for fid,day,area in rows:
                    original=source.execute('SELECT id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" WHERE fid=?',(fid,)).fetchone()
                    if original!=(identity_value,day,area):raise AssertionError('source fallback evidence mismatch')
                    recovered.append(original[2])
                latencies.append(time.perf_counter_ns()-start);checks+=1
                assert math.fsum(recovered)==math.fsum(r[2] for r in rows)
    after=(lake/DAILY).stat();assert (after.st_size,after.st_mtime_ns)==(stat.st_size,stat.st_mtime_ns)
    with sqlite3.connect(census/'cohort-metadata.sqlite') as db:
        expected=dict(db.execute("SELECT observations,count(*) FROM fire WHERE source='native' GROUP BY observations"))
        assert counts['one']==expected[1] and counts['two']==expected[2] and source_groups==sum(expected.values())
        total_fires=source_groups;population=[]
        for n,label in [(1,'one_observation'),(2,'two_observations'),(3,'three_or_more')]:
            count=counts['one'] if n==1 else counts['two'] if n==2 else counts['three_plus']
            population.append({'stratum':label,'fires':count,'fraction_of_native_ids':count/total_fires,'primary_full_population':True})
        cohort={}
        for label,where in [('one','f.observations=1'),('two','f.observations=2'),('three_plus','f.observations>=3')]:
            cohort[label]={dim:[{'stratum':key if key is not None else 'unknown','fires':n} for key,n in db.execute('SELECT '+col+',count(*) FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND '+where+' GROUP BY '+col)] for dim,col in [('year','e.year'),('region','e.region'),('catalog_size','e.size_class')]}
    report={'status':'REAL_NATIVE_SHORT_HISTORY_INFORMATION_AUDIT_COMPLETE','mode':'deterministic information/access diagnostics, not embedding or predictive performance','source_sha256':identity['sha256'],'source_records_decoded':counts['all_observations'],'all_native_fire_ids':total_fires,'primary_populations':population,'short_history_share':(counts['one']+counts['two'])/total_fires,'stratum_diagnostics':{str(n):{**dict(aggregates[n]),'observed_total_min_source_units':min_area[n],'observed_total_max_source_units':max_area[n],'mean_complete_native_json_bytes':native_payload_bytes[n]/(counts['one'] if n==1 else counts['two']),'mean_complete_summary_json_bytes':summary_payload_bytes[n]/(counts['one'] if n==1 else counts['two']),'mean_complete_normalized_json_bytes':normalized_payload_bytes[n]/(counts['one'] if n==1 else counts['two'])} for n in (1,2)},'retained_interface':'all representations retain native IDs, original dates, source row refs and checksum; optional source fallback is explicit and paid','source_fallback':{'checks':checks,'all_exact':True,'median_lookup_ns':float(np.median(latencies)),'sample':'first64 fires in each short-history stratum; diagnostic warm-source lookup, not representative latency benchmark','source_values_persisted':False},'cohort_strata':cohort,'physical_duration':'not measured by observation count','learned_models_trained':0,'pca_fitted':False,'task_capabilities':{str(n):capabilities(n) for n in (1,2,3)},'seconds':time.perf_counter()-started,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (out/'short-history-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    with (out/'primary-population.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(population[0]));w.writeheader();w.writerows(population)
    storage=[]
    for n in (1,2):
        storage.append({'observations':n,'representation':'compact native','numeric_values':n,'float64_payload_bytes_only':n*8,'interpretation':'dates, provenance, indexes and serving costs excluded from this numerical byte count'})
        for d in (4,8,16,32,64):storage.append({'observations':n,'representation':'proposed learned vector dimension'+str(d),'numeric_values':d,'float64_payload_bytes_only':d*8,'interpretation':'analytical footprint only; no learned vector trained, no skill or total-storage claim'})
    with (out/'numeric-payload-footprints.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(storage[0]));w.writeheader();w.writerows(storage)
    print(json.dumps({k:report[k] for k in ('status','all_native_fire_ids','primary_populations','short_history_share','source_fallback','seconds')},indent=2))
if __name__=='__main__':main()
