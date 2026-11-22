"""Independent calendar/run checks and a generated end-to-end source fixture."""
from datetime import date,timedelta
from pathlib import Path
import hashlib,json,sqlite3
import pytest
pa=pytest.importorskip('pyarrow')
import pyarrow.parquet as pq
from dataset_prototype.embedding_study.population_profile import partition,window_count,supported_day,run,DAILY,EVENTS,SLICES,TRAITS,DAILY_TABLE,EVENT_TABLE


def observations(days,areas=None):
    return [{'date':None if d is None else (date(2020,1,1)+timedelta(days=d)).isoformat(),'area':1. if areas is None else areas[i],'ref':str(i)} for i,d in enumerate(days)]


def test_missing_zero_duplicates_and_maximal_runs():
    records=observations([0,1,2,4,5,6,6,7,8,9],[0.,1.,1.,None,1.,1.,1.,1.,1.,1.])
    stats,runs,gaps=partition(records)
    assert [len(r) for r in runs]==[3,1,3]
    assert stats['observed_zero']==1 and stats['missing_area']==1
    assert stats['duplicate_date_rows']==2 and stats['duplicate_extra_rows']==1
    assert stats['strict_whole_history']==0 and stats['gap_intervals']==1
    assert all(all((supported_day(b['date'])-supported_day(a['date'])).days==1 for a,b in zip(r,r[1:])) for r in runs)
    assert sum(window_count(len(r),3,1) for r in runs)==0


def test_unsupported_dates_invalid_area_and_sorting():
    stats,runs,_=partition(observations([3,0,1,2,None],[1.,1.,-1.,float('nan'),1.]))
    assert stats['invalid_area']==2 and stats['missing_or_unsupported_date']==1
    assert [len(r) for r in runs]==[1,1]
    assert supported_day('2020-01-01T12:00:00') is None
    assert supported_day('2020-01-01T00:00:00')==date(2020,1,1)


@pytest.mark.parametrize('length',[0,1,3,4,8,21,37,81])
def test_window_counts_against_explicit_index_sets(length):
    for d in (3,5,7,10,14,21,30):
        for h in (1,3,7):
            legal=[tuple(range(start,start+d+h)) for start in range(length) if start+d+h<=length]
            assert window_count(length,d,h)==len(legal)


def test_generated_end_to_end_reconciliation_and_stage_restart(tmp_path):
    lake=tmp_path/'GENERATED_LAKE';out=tmp_path/'output';out.mkdir()
    for rel in (DAILY,EVENTS,SLICES,TRAITS):(lake/rel).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(lake/EVENTS) as db:
        db.execute('CREATE TABLE "'+EVENT_TABLE+'" (id INTEGER,ig_year INTEGER,tot_ar_km2 REAL)')
        db.executemany('INSERT INTO "'+EVENT_TABLE+'" VALUES (?,?,?)',[(1,2020,7.),(2,2020,7.)])
    records=[]
    for identity,days in [(1,[0,1,2,6,7,8,9]),(2,list(range(7)))]:
        records.extend((len(records)+j+1,identity,r['date'],r['area']) for j,r in enumerate(observations(days)))
    with sqlite3.connect(lake/DAILY) as db:
        db.execute('CREATE TABLE "'+DAILY_TABLE+'" (fid INTEGER,id INTEGER,date TEXT,dy_ar_km2 REAL)')
        db.executemany('INSERT INTO "'+DAILY_TABLE+'" VALUES (?,?,?,?)',records)
    cache=[{'fire_id':str(i),'timestamp':d,'ring_area_km2':a,'cumulative_area_km2':float(j+1),'climate_available':False} for j,(f,i,d,a) in enumerate(records) if not (i==1 and d=='2020-01-10')]
    pq.write_table(pa.Table.from_pylist(cache),lake/SLICES)
    pq.write_table(pa.Table.from_pylist([{'fire_id':str(i),'region':'TEST_ONLY','year':2020,'total_area_km2':7.} for i in (1,2)]),lake/TRAITS)
    (out/'direct-execution-authorization.json').write_text(json.dumps({'origin':'DIRECT_USER_INSTRUCTION','statement':'stop with all the stops and make this happen.'}))
    verified=[]
    for rel in (DAILY,EVENTS,SLICES,TRAITS):
        p=lake/rel;s=p.stat();verified.append({'relative_path':rel,'historical_match':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns})
    (out/'source-verification.json').write_text(json.dumps(verified))
    result=run(lake,out)
    assert result['counts']['native']['fires']==2 and result['counts']['native']['rows']==14
    assert result['counts']['cache']['rows']==13 and result['reconciliation']['native_only_rows']==1
    assert result['reconciliation']['cache_only_rows']==0 and result['reconciliation']['overlap_area_hash_mismatches']==0
    with sqlite3.connect(out/'cohort-metadata.sqlite') as db:
        assert db.execute("SELECT sum(windows) FROM windows WHERE source='native' AND depth=3 AND horizon=1").fetchone()[0]==5
        assert db.execute("SELECT count(*) FROM fire WHERE source='native' AND strict=1").fetchone()[0]==1
        before=list(db.execute('SELECT source,id,observations,evidence_hash FROM fire ORDER BY source,id'))
    again=run(lake,out);assert again==result
    with sqlite3.connect(out/'cohort-metadata.sqlite') as db:assert list(db.execute('SELECT source,id,observations,evidence_hash FROM fire ORDER BY source,id'))==before


def test_arrow_export_all_null_later_batch_keeps_schema(tmp_path):
    from dataset_prototype.embedding_study.population_profile import parquet_export
    with sqlite3.connect(':memory:') as db:
        db.execute('CREATE TABLE metadata(id INTEGER, nullable_count INTEGER)')
        db.executemany('INSERT INTO metadata VALUES (?,?)',[(i,1 if i<2048 else None) for i in range(4096)])
        parquet_export(db,'SELECT * FROM metadata ORDER BY id',tmp_path/'metadata.parquet')
    table=pq.read_table(tmp_path/'metadata.parquet')
    assert table.num_rows==4096 and table.column('nullable_count').null_count==2048
