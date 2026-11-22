"""Read-only native census under direct investigator approval; no model execution.

Source sorting stays within SQLite's bounded in-memory workspace. Only compact
keys/hashes, per-fire summaries and run/source references persist, never daily values.
"""
from collections import Counter
from datetime import date,datetime,timezone
from pathlib import Path
import argparse,hashlib,json,math,resource,sqlite3,time
import pyarrow as pa
import pyarrow.parquet as pq

DEPTHS=(3,5,7,10,14,21,30)
HORIZONS=(1,3,7)
DAILY='files/artifacts/fire-vase-gridmet-real/fired-cache/fired_conus-ak_daily_nov2001-march2021.gpkg'
EVENTS='files/artifacts/fire-vase-gridmet-real/fired-cache/fired_conus-ak_events_nov2001-march2021.gpkg'
SLICES='files/scratch/fire_vase_run_full/tables/vase_slices.parquet'
TRAITS='files/scratch/fire_vase_run_full/tables/fire_traits.parquet'
DAILY_TABLE='fired_conus-ak_daily_nov2001-march2021'
EVENT_TABLE='fired_conus-ak_events_nov2001-march2021'


def supported_day(value):
    if value is None:return None
    if isinstance(value,datetime):
        if value.hour or value.minute or value.second or value.microsecond:return None
        return value.date()
    if isinstance(value,date):return value
    try:
        text=str(value)
        if len(text)==10:return date.fromisoformat(text)
        d=datetime.fromisoformat(text)
        return d.date() if not (d.hour or d.minute or d.second or d.microsecond) else None
    except (ValueError,TypeError):return None


def partition(rows):
    """One fire only. Duplicate dates are excluded in full, never deduplicated."""
    counts=Counter(supported_day(r['date']) for r in rows)
    ordered=sorted(rows,key=lambda r:(supported_day(r['date']) or date.min,r['ref']))
    stats=Counter(observations=len(rows));runs=[];current=[];previous=None;gaps=Counter();areas=[]
    for r in ordered:
        day=supported_day(r['date']);v=r['area']
        missing=v is None
        valid=not missing and not isinstance(v,bool) and isinstance(v,(int,float)) and math.isfinite(v) and v>=0
        stats['missing_area']+=missing;stats['invalid_area']+=not missing and not valid
        stats['missing_or_unsupported_date']+=day is None
        stats['duplicate_date_rows']+=day is not None and counts[day]>1
        stats['observed_zero']+=valid and v==0
        stats['valid_area_rows']+=valid
        if valid:areas.append(v)
        if previous is not None and day is not None:
            gap=(day-previous).days
            gaps[gap]+=1
        if day is not None:previous=day
        usable=valid and day is not None and counts[day]==1
        if not usable or (current and (day-supported_day(current[-1]['date'])).days!=1):
            if current:runs.append(current);current=[]
        if usable:current.append(r)
    if current:runs.append(current)
    stats['duplicate_extra_rows']=sum(n-1 for d,n in counts.items() if d is not None and n>1)
    stats['duplicate_dates']=sum(n>1 for d,n in counts.items() if d is not None)
    stats['valid_supported_rows']=sum(map(len,runs));stats['exact_day_intervals']=gaps[1]
    stats['gap_intervals']=sum(n for g,n in gaps.items() if g>1)
    stats['unobserved_calendar_days_between_records']=sum((g-1)*n for g,n in gaps.items() if g>1)
    stats['duplicate_adjacent_intervals']=gaps[0]
    stats['max_run']=max(map(len,runs),default=0)
    stats['strict_whole_history']=int(len(runs)==1 and len(runs[0])==len(rows))
    days=[d for d in counts if d is not None]
    stats['observed_span_days']=((max(days)-min(days)).days+1) if days else None
    stats['derived_sum_observed_native_area']=math.fsum(areas) if areas else None
    stats['run_count']=len(runs)
    return dict(stats),runs,dict(gaps)


def window_count(length,depth,horizon):
    result=max(0,length-depth-horizon+1)
    # Independent enumeration of legal cutoff indices, not target arithmetic reuse.
    reference=sum(1 for cutoff in range(length) if cutoff>=depth-1 and cutoff+horizon<length)
    if result!=reference:raise AssertionError('window reference mismatch')
    return result


def readonly(path):
    db=sqlite3.connect(path.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
    db.execute('PRAGMA temp_store=MEMORY');db.execute('PRAGMA cache_size=-32768')
    db.execute('PRAGMA hard_heap_limit=268435456')
    return db


def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,default=str,allow_nan=False,separators=(',',':')).encode()).hexdigest()


def size_class(v):
    if v is None or not math.isfinite(float(v)) or float(v)<0:return 'unknown'
    return '<1' if v<1 else '1–<10' if v<10 else '10–<100' if v<100 else '100–<1000' if v<1000 else '≥1000'


def parquet_export(db,query,path):
    cursor=db.execute(query);names=[d[0] for d in cursor.description];writer=None
    try:
        while True:
            batch=cursor.fetchmany(2048)
            if not batch:break
            table=pa.Table.from_pylist([dict(zip(names,row)) for row in batch],schema=writer.schema if writer else None)
            if writer is None:writer=pq.ParquetWriter(path,table.schema)
            writer.write_table(table)
    finally:
        if writer:writer.close()


def run(lake,output):
    lake=Path(lake).resolve();output=Path(output);output.mkdir(parents=True,exist_ok=True)
    authorization=json.loads((output/'direct-execution-authorization.json').read_text())
    if authorization.get('origin')!='DIRECT_USER_INSTRUCTION' or authorization.get('statement')!='stop with all the stops and make this happen.':raise PermissionError('direct investigator instruction required')
    verification=json.loads((output/'source-verification.json').read_text());identities={r['relative_path']:r for r in verification}
    for rel in (DAILY,EVENTS,SLICES,TRAITS):
        v=identities[rel];p=lake/rel;s=p.stat()
        if not v['historical_match'] or (s.st_size,s.st_mtime_ns)!=(v['bytes'],v['mtime_ns']):raise ValueError('verified source identity changed: '+rel)
    started=time.perf_counter();usage_start=resource.getrusage(resource.RUSAGE_SELF);decoded=Counter()
    db=sqlite3.connect(output/'cohort-metadata.sqlite');db.execute('PRAGMA cache_size=-32768');db.execute('PRAGMA temp_store=MEMORY')
    db.executescript('''CREATE TABLE IF NOT EXISTS checkpoint(stage TEXT PRIMARY KEY,completed_at TEXT);
    CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,year INTEGER,size_class TEXT,region TEXT,trait_year INTEGER,trait_size_class TEXT);
    CREATE TABLE IF NOT EXISTS catalog_issues(kind TEXT,n INTEGER);
    CREATE TABLE IF NOT EXISTS keys(source TEXT,key TEXT,event TEXT,date_key TEXT,area_hash TEXT,row_ref TEXT);
    CREATE INDEX IF NOT EXISTS key_idx ON keys(source,key);
    CREATE TABLE IF NOT EXISTS fire(source TEXT,id TEXT,observations INTEGER,valid_area_rows INTEGER,valid_supported_rows INTEGER,
    missing_area INTEGER,invalid_area INTEGER,missing_date INTEGER,duplicate_rows INTEGER,duplicate_extra INTEGER,
    observed_zero INTEGER,exact_day_intervals INTEGER,gap_intervals INTEGER,unobserved_days INTEGER,max_run INTEGER,
    strict INTEGER,span INTEGER,observed_sum REAL,run_count INTEGER,climate_available INTEGER,cumulative_rows INTEGER,
    evidence_hash TEXT,PRIMARY KEY(source,id));
    CREATE TABLE IF NOT EXISTS runs(source TEXT,id TEXT,run_index INTEGER,start_date TEXT,end_date TEXT,length INTEGER,start_ref TEXT,end_ref TEXT,evidence_hash TEXT);
    CREATE TABLE IF NOT EXISTS windows(source TEXT,id TEXT,depth INTEGER,horizon INTEGER,runs INTEGER,windows INTEGER,PRIMARY KEY(source,id,depth,horizon));
    CREATE TABLE IF NOT EXISTS gaps(source TEXT,days INTEGER,n INTEGER);''')
    done={r[0] for r in db.execute('SELECT stage FROM checkpoint')};telemetry={}
    def checkpoint(stage):
        db.execute('INSERT INTO checkpoint VALUES (?,?)',(stage,datetime.now(timezone.utc).isoformat()));db.commit();print('COMPLETED '+stage,flush=True)
    if 'catalog' not in done:
        db.execute('DELETE FROM events');db.execute('DELETE FROM catalog_issues');duplicate=missing=0
        with readonly(lake/EVENTS) as source:
            for identity,year,area in source.execute('SELECT id,ig_year,tot_ar_km2 FROM "'+EVENT_TABLE+'"'):
                if identity is None:missing+=1;continue
                try:db.execute('INSERT INTO events VALUES (?,?,?,NULL,NULL,NULL)',(str(identity),year,size_class(area)))
                except sqlite3.IntegrityError:duplicate+=1
        for batch in pq.ParquetFile(lake/TRAITS).iter_batches(batch_size=1024,columns=['fire_id','region','year','total_area_km2']):
            for r in batch.to_pylist():db.execute('UPDATE events SET region=?,trait_year=?,trait_size_class=? WHERE id=?',(r['region'],r['year'],size_class(r['total_area_km2']),r['fire_id']))
        db.executemany('INSERT INTO catalog_issues VALUES (?,?)',[('duplicate_catalog_ids',duplicate),('missing_catalog_ids',missing)])
        checkpoint('catalog')
    def process(source_name,iterator):
        if source_name in done:return
        for table in ('keys','fire','runs','windows','gaps'):db.execute('DELETE FROM '+table+' WHERE source=?',(source_name,))
        db.commit();current=None;buffer=[];n=0;gapcounts=Counter();phase_start=time.perf_counter()
        def flush():
            nonlocal n
            if not buffer:return
            stats,runs,gaps=partition(buffer);gapcounts.update(gaps)
            # Hashes and row references persist, not daily measurement values.
            evidence=digest([r['row_hash'] for r in buffer]);cumulative=sum(r.get('cumulative_valid',False) for r in buffer)
            db.execute('INSERT INTO fire VALUES ('+','.join('?' for _ in range(22))+')',(source_name,current,stats['observations'],stats['valid_area_rows'],stats['valid_supported_rows'],stats.get('missing_area',0),stats.get('invalid_area',0),stats.get('missing_or_unsupported_date',0),stats.get('duplicate_date_rows',0),stats['duplicate_extra_rows'],stats.get('observed_zero',0),stats['exact_day_intervals'],stats['gap_intervals'],stats['unobserved_calendar_days_between_records'],stats['max_run'],stats['strict_whole_history'],stats['observed_span_days'],stats['derived_sum_observed_native_area'],len(runs),sum(r.get('climate_available') is True for r in buffer) if source_name=='cache' else None,cumulative if source_name=='cache' else None,evidence))
            for i,runrows in enumerate(runs):
                db.execute('INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?)',(source_name,current,i,supported_day(runrows[0]['date']).isoformat(),supported_day(runrows[-1]['date']).isoformat(),len(runrows),runrows[0]['ref'],runrows[-1]['ref'],digest([r['row_hash'] for r in runrows])))
            for d in DEPTHS:
                for h in HORIZONS:
                    counts=[window_count(len(r),d,h) for r in runs];total=sum(counts)
                    if total:db.execute('INSERT INTO windows VALUES (?,?,?,?,?,?)',(source_name,current,d,h,sum(c>0 for c in counts),total))
            n+=1
            if n%2000==0:
                db.commit()
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>1_500_000_000:raise MemoryError('1.5GB process peak guard')
                if n%50000==0:print(source_name+' fires '+str(n),flush=True)
        for r in iterator:
            decoded[source_name]+=1
            identity=r['id']
            if identity is None:raise ValueError('missing event identity; retained failure, no invented event')
            key=str(identity)
            if key!=current:flush();current=key;buffer=[]
            if len(buffer)>=8192:raise MemoryError('per-fire observation limit8192 reached; no truncated census')
            rawarea=r['area'];finite=rawarea is not None and math.isfinite(float(rawarea))
            r['row_hash']=digest({'id':identity,'date':str(r['date']),'area':rawarea if finite else str(rawarea),'ref':r['ref'],'source_sha256':identities[DAILY if source_name=='native' else SLICES]['sha256']})
            day=supported_day(r['date']);datekey=day.isoformat() if day else 'UNSUPPORTED:'+str(r['date'])
            db.execute('INSERT INTO keys VALUES (?,?,?,?,?,?)',(source_name,digest([key,datekey]),key,datekey,digest(rawarea if finite else str(rawarea)),str(r['ref'])))
            buffer.append(r)
        flush()
        db.executemany('INSERT INTO gaps VALUES (?,?,?)',[(source_name,g,v) for g,v in gapcounts.items()]);checkpoint(source_name);telemetry[source_name]={'fires':n,'seconds':time.perf_counter()-phase_start}
    def native():
        with readonly(lake/DAILY) as source:
            # Native sorting is read-only, in-memory, with SQLite hard heap cap256MiB.
            for fid,identity,day,area in source.execute('SELECT fid,id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" ORDER BY id,date,fid'):
                yield {'id':identity,'date':day,'area':area,'ref':str(fid)}
    def cache():
        offset=0
        for batch in pq.ParquetFile(lake/SLICES).iter_batches(batch_size=1024,columns=['fire_id','timestamp','ring_area_km2','cumulative_area_km2','climate_available']):
            for r in batch.to_pylist():
                c=r['cumulative_area_km2']
                yield {'id':r['fire_id'],'date':r['timestamp'],'area':r['ring_area_km2'],'ref':str(offset),'cumulative_valid':c is not None and math.isfinite(c) and c>=0,'climate_available':r['climate_available']};offset+=1
    try:
        process('native',native());process('cache',cache())
        # Index summaries contain no source scientific observation arrays.
        db.execute('CREATE INDEX IF NOT EXISTS runs_id ON runs(source,id)');db.execute('CREATE INDEX IF NOT EXISTS windows_dh ON windows(source,depth,horizon)');db.commit()
        counts={}
        for s in ('native','cache'):
            names=['fires','rows','valid_area_rows','valid_supported_rows','missing_area','invalid_area','missing_date','duplicate_rows','duplicate_extra','observed_zero','exact_day_intervals','gap_intervals','unobserved_days','strict_whole_history_fires','cumulative_valid_rows']
            query='SELECT count(*),'+','.join('sum('+c+')' for c in ('observations','valid_area_rows','valid_supported_rows','missing_area','invalid_area','missing_date','duplicate_rows','duplicate_extra','observed_zero','exact_day_intervals','gap_intervals','unobserved_days','strict','cumulative_rows'))+' FROM fire WHERE source=?'
            counts[s]=dict(zip(names,db.execute(query,(s,)).fetchone()))
        reconciliation={}
        for a,b,label in [('native','cache','native_only_rows'),('cache','native','cache_only_rows')]:
            reconciliation[label]=db.execute('SELECT count(*) FROM keys a WHERE a.source=? AND NOT EXISTS (SELECT 1 FROM keys b WHERE b.source=? AND b.key=a.key)',(a,b)).fetchone()[0]
        reconciliation['overlap_unique_keys']=db.execute("SELECT count(DISTINCT a.key) FROM keys a WHERE a.source='native' AND EXISTS (SELECT 1 FROM keys b WHERE b.source='cache' AND b.key=a.key)").fetchone()[0]
        reconciliation['overlap_area_hash_mismatches']=db.execute("SELECT count(*) FROM keys a JOIN keys b ON a.key=b.key WHERE a.source='native' AND b.source='cache' AND a.area_hash<>b.area_hash").fetchone()[0]
        reconciliation['native_only_fires']=db.execute("SELECT count(*) FROM fire n WHERE n.source='native' AND NOT EXISTS(SELECT 1 FROM fire c WHERE c.source='cache' AND c.id=n.id)").fetchone()[0]
        reconciliation['native_fires_absent_from_event_catalog']=db.execute("SELECT count(*) FROM fire f LEFT JOIN events e USING(id) WHERE f.source='native' AND e.id IS NULL").fetchone()[0]
        for s in ('native','cache'):
            unique=db.execute('SELECT count(DISTINCT event) FROM keys WHERE source=?',(s,)).fetchone()[0]
            assert unique==counts[s]['fires']
            assert counts[s]['rows']==db.execute('SELECT count(*) FROM keys WHERE source=?',(s,)).fetchone()[0]
        parquet_export(db,'SELECT * FROM runs ORDER BY source,id,run_index',output/'local-consecutive-runs.parquet')
        parquet_export(db,'SELECT * FROM fire ORDER BY source,id',output/'per-fire-profile.parquet')
        summary={'status':'COMPLETE_NATIVE_AND_CACHE_CENSUS','counts':counts,'catalog_fires':db.execute('SELECT count(*) FROM events').fetchone()[0],'catalog_issues':dict(db.execute('SELECT kind,n FROM catalog_issues')),'reconciliation':reconciliation,'scientific_claim':'retrospective native date-bin support; source quality/uncertainty and operational availability remain unknown','source_identity':identities}
        (output/'census.json').write_text(json.dumps(summary,indent=2)+'\n')
        usage=resource.getrusage(resource.RUSAGE_SELF)
        telemetry.update(total_seconds=time.perf_counter()-started,peak_rss_bytes=usage.ru_maxrss,source_container_bytes=sum(v['bytes'] for v in identities.values()),source_byte_scope='complete-container verification bytes, not measured filesystem physical I/O',dataset_daily_records_profiled=sum(c['rows'] for c in counts.values()),decoded_daily_records_this_invocation=sum(decoded.values()),decoded_records_by_source_this_invocation=dict(decoded),catalog_records_profiled=summary['catalog_fires'],reused_completed_stages=sorted(done),checkpoint_restart='stage-level; completed verified stages reused, interrupted stage deleted/replayed; no tensor materialization',source_sorts='read-only SQLite temp_store MEMORY, hard heap256MiB',derived_metadata_bytes=sum(p.stat().st_size for p in output.iterdir() if p.is_file()),phase_times=telemetry.copy())
        (output/'profiling-resource-report.json').write_text(json.dumps(telemetry,indent=2)+'\n');print(json.dumps(summary['counts'],indent=2),flush=True)
        return summary
    except BaseException as error:
        db.rollback();(output/('failure-'+str(time.time_ns())+'.json')).write_text(json.dumps({'error':type(error).__name__,'message':str(error),'completed_stages':[r[0] for r in db.execute('SELECT stage FROM checkpoint')],'complete':False,'elapsed_seconds':time.perf_counter()-started,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n');raise
    finally:db.close()


def main():
    p=argparse.ArgumentParser();p.add_argument('--lake',required=True);p.add_argument('--output',required=True);a=p.parse_args();run(a.lake,a.output)
if __name__=='__main__':main()
