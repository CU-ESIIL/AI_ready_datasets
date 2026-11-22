"""Bounded canonical streams and task eligibility, with gated real Parquet reads."""
from dataclasses import dataclass
from collections import deque,Counter
from datetime import date,datetime
import math,json,hashlib,sqlite3
from pathlib import Path
from ..contracts import digest
from .lake_authorization import require_scope,contained

@dataclass(frozen=True)
class NativeDay:
    event_key: str
    observation_key: str
    native_date: date | None
    area_km2: float | None
    quality_flags: tuple[str,...]=()
    available_at: datetime | None=None
    native_unit: str='km2'
    native_date_text: str | None=None
    source_checksum: str='generated_offline_control'
    native_event_id: object=None
    native_area_value: object=None
    native_cumulative_area_km2: float | None=None
    uncertainty_evidence: str | None=None


def raw_parquet_batches(root,binding,verification,plan,authorization):
    # Checks happen BEFORE a ParquetFile is created, metadata opened or rows read.
    require_scope(plan,authorization,'profile_rows');require_scope(plan,authorization,'harmonize')
    if binding.binding_digest not in plan.scientific_binding_digests:raise PermissionError('scientific binding not reviewed in plan')
    if not binding.sorted_by_event_and_date:raise PermissionError('reviewed grouping/order precondition required')
    if verification.get('plan_digest')!=plan.plan_digest or verification.get('sha256')!=binding.expected_sha256 or verification.get('relative_path')!=binding.source_relative_path:raise PermissionError('verified source identity missing/mismatched')
    path=contained(root,binding.source_relative_path);stat=path.stat()
    if stat.st_size!=verification.get('bytes') or stat.st_mtime_ns!=verification.get('mtime_ns'):raise PermissionError('source changed after verification')
    import pyarrow.parquet as pq
    columns=list(dict.fromkeys([binding.event_field,binding.date_field,binding.area_field,*binding.quality_fields,*([binding.availability_field] if binding.availability_field else []),*([binding.cumulative_field] if binding.cumulative_field else [])]))
    file=pq.ParquetFile(path)
    if not set(columns)<=set(file.schema_arrow.names):raise ValueError('reviewed schema fields missing')
    for batch in file.iter_batches(batch_size=plan.batch_rows,columns=columns):
        yield batch.to_pylist()
    after=path.stat()
    if (stat.st_size,stat.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('source changed during streaming')


def canonical_rows(batches,binding,*,date_decoder=None):
    # date_decoder is a fixed ENUM, never a function/expression or model code.
    if date_decoder is not None and date_decoder!=binding.date_interpretation:raise ValueError('date interpretation differs from reviewed binding')
    date_decoder=binding.date_interpretation
    if date_decoder not in ('native_iso_date','reviewed_midnight_date_bin'):raise ValueError('unregistered date interpretation')
    for batch in batches:
        for record in batch:
            event=record.get(binding.event_field);native=record.get(binding.date_field);value=record.get(binding.area_field)
            if event is None:raise ValueError('missing native event ID')
            event_key=digest({'native_value':event,'native_type':type(event).__name__,'source':binding.source_relative_path})
            day=None
            if native is not None:
                if isinstance(native,datetime):
                    if date_decoder!='reviewed_midnight_date_bin' or native.time().isoformat() not in ('00:00:00','00:00:00+00:00'):raise ValueError('unreviewed timestamp/date support')
                    day=native.date()
                elif isinstance(native,date):day=native
                else:
                    text=str(native)
                    if date_decoder=='native_iso_date':day=date.fromisoformat(text)
                    else:
                        dt=datetime.fromisoformat(text)
                        if dt.hour or dt.minute or dt.second or dt.microsecond:raise ValueError('not a native midnight date bin')
                        day=dt.date()
            if value is not None:
                if isinstance(value,bool) or not math.isfinite(float(value)) or float(value)<0:raise ValueError('invalid native area, no clipping/imputation')
                value=float(value)
            available=record.get(binding.availability_field) if binding.availability_field else None
            if available is not None and not isinstance(available,datetime):available=datetime.fromisoformat(str(available))
            if available is not None and available.utcoffset() is None:raise ValueError('unknown source availability timezone')
            cumulative=record.get(binding.cumulative_field) if binding.cumulative_field else None
            if cumulative is not None and (not math.isfinite(float(cumulative)) or float(cumulative)<0):raise ValueError('invalid native cumulative evidence')
            flags=tuple(k+':'+json.dumps(record.get(k),default=str,sort_keys=True) for k in binding.quality_fields)
            yield NativeDay(event_key,digest({'event':event_key,'date':str(native)}),day,value,flags,available,
                binding.native_area_unit,str(native) if native is not None else None,binding.expected_sha256,event,record.get(binding.area_field),float(cumulative) if cumulative is not None else None,binding.uncertainty_evidence)


def profile_events(rows,index_path):
    """One event in memory; SQLite stores only completed event keys, no observations."""
    path=Path(index_path)
    if path.exists():raise FileExistsError('use a fresh private metadata index')
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE completed_events (event_key TEXT PRIMARY KEY)')
        current=None;stats=None;previous=None;run=0;hasher=None
        def begin(key,native_id):
            if db.execute('SELECT 1 FROM completed_events WHERE event_key=?',(key,)).fetchone():raise ValueError('source not grouped; no silent external sorting/persistence')
            return {'event_key':key,'native_event_id':native_id,'observations':0,'valid_area_observations':0,'observed_zero':0,'missing_area':0,'missing_dates':0,
                'adjacent_intervals':0,'exact_day_intervals':0,'gap_intervals':0,'max_consecutive_run':0,
                'sequences':{str(k):0 for k in (3,7,14,30)},'quality_flags':Counter(),'complete':True}
        def finish():
            db.execute('INSERT INTO completed_events VALUES (?)',(current,));db.commit()
            result={**stats,'quality_flags':dict(stats['quality_flags']),'native_evidence_digest':hasher.hexdigest(),
              'spatially_supported':None,'environmentally_supported':None}
            result['cohort_A_basic_observed']=stats['valid_area_observations']>=1
            result['cohort_B_supported_run']=stats['max_consecutive_run']>=4
            result['cohort_C_long_run']=stats['max_consecutive_run']>=14
            return result
        for row in rows:
            if current!=row.event_key:
                if stats is not None:yield finish()
                current=row.event_key;stats=begin(current,row.native_event_id);previous=None;run=0;hasher=hashlib.sha256()
            stats['observations']+=1;stats['quality_flags'].update(row.quality_flags)
            hasher.update(digest({'key':row.observation_key,'date':row.native_date_text or str(row.native_date),'value':row.area_km2,'unit':row.native_unit,'source':row.source_checksum}).encode())
            valid=row.area_km2 is not None and row.native_date is not None
            if row.area_km2 is None:stats['missing_area']+=1;stats['complete']=False
            else:
                if row.area_km2<0 or not math.isfinite(row.area_km2):raise ValueError('invalid area')
                stats['valid_area_observations']+=1;stats['observed_zero']+=row.area_km2==0
            if row.native_date is None:stats['missing_dates']+=1;stats['complete']=False
            if previous is not None:
                stats['adjacent_intervals']+=1
                gap=(row.native_date-previous.native_date).days if row.native_date and previous.native_date else None
                if gap is not None and gap<=0:raise ValueError('duplicate/unordered source dates; fix scientific evidence, never repair')
                if gap==1:stats['exact_day_intervals']+=1
                else:stats['gap_intervals']+=1;stats['complete']=False
            else:gap=None
            run=(run+1 if previous is not None and gap==1 and previous.area_km2 is not None else 1) if valid else 0
            stats['max_consecutive_run']=max(stats['max_consecutive_run'],run)
            for n in (3,7,14,30):stats['sequences'][str(n)]+=run>=n
            previous=row
        if stats is not None:yield finish()


def prefix_examples(rows,depths=(3,7,14,30),horizons=(1,3,7),*,invalid_event_keys=frozenset()):
    """Run after whole-source support preflight; 37 daily records max in memory."""
    if any(d not in (3,7,14,30) for d in depths) or any(h not in (1,3,7) for h in horizons):raise ValueError('unregistered support')
    queue=deque(maxlen=max(depths)+max(horizons));event=None;previous=None
    for row in rows:
        if row.event_key!=event:queue.clear();event=row.event_key;previous=None
        if row.event_key in invalid_event_keys:continue
        if row.native_date is None or row.area_km2 is None:queue.clear();previous=None;continue
        if previous is not None and (row.native_date-previous.native_date).days!=1:queue.clear()
        if row.area_km2<0 or not math.isfinite(row.area_km2):raise ValueError('invalid native increment')
        queue.append(row);previous=row
        for depth in depths:
            for horizon in horizons:
                if len(queue)<depth+horizon:continue
                window=list(queue)[-depth-horizon:];past=window[:depth];future=window[depth:]
                # Local observed window, not invented ignition time or completed duration.
                yield {'event_key':event,'depth':depth,'horizon':horizon,'cutoff':past[-1].native_date,
                    'past':tuple(past),'future':tuple(future),'claim':'retrospective_reconstructed',
                    'origin':'contiguous_observed_window_not_assumed_event_ignition',
                    'lineage_digest':digest([r.observation_key for r in window])}


def tasks(example):
    """Independent future tasks on complete supported windows; no ecological labels."""
    from fractions import Fraction
    p=[r.area_km2 for r in example['past']];f=[r.area_km2 for r in example['future']]
    if not p or not f or any(v is None or not math.isfinite(v) or v<0 for v in p+f):raise ValueError('unsupported target values')
    target={'next_day_area':f[0],'horizon_total':math.fsum(f),'horizon':len(f)}
    if len(f)>=3:
        recent=p[-3:];target.update(acceleration=math.fsum(b-a for a,b in zip(f,f[1:]))/(len(f)-1),
          future_mean_exceeds_recent=float(math.fsum(f)/len(f)>math.fsum(recent)/len(recent)),
          future_std=math.sqrt(math.fsum((v-math.fsum(f)/len(f))**2 for v in f)/len(f)),future_pattern=tuple(math.log1p(v) for v in f))
    reference=sum(Fraction(str(v)) for v in f)
    if not math.isclose(target['horizon_total'],float(reference),rel_tol=0,abs_tol=1e-9):raise ValueError('independent total mismatch')
    return target
