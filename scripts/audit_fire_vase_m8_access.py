"""Independently measure metadata recovery and strict native fallback on every test fire."""
import argparse,csv,json,time
from pathlib import Path
from datetime import date
import numpy as np
from dataset_prototype.embedding_study.population_profile import readonly,DAILY,DAILY_TABLE
from dataset_prototype.embedding_study.observed_state import calculate


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--lake',required=True);a=p.parse_args();out=Path(a.output);ds=dict(np.load(out/'private/observed-state.npz'));idx=np.flatnonzero(ds['fold']=='test');offsets=ds['offsets'];dates=ds['date_ordinals'];counts=np.diff(offsets);spans=dates[offsets[1:]-1]-dates[offsets[:-1]];side_count=np.log1p(counts);side_span=np.log1p(spans)
 assert np.array_equal(counts,ds['n']) and np.allclose(side_count,ds['y'][:,1],rtol=0,atol=1e-14) and np.allclose(side_span,ds['y'][:,9],rtol=0,atol=1e-14)
 dump={'status':'ALL_FIRE_SIDECAR_AND_WHOLE_TEST_NATIVE_ACCESS_VERIFIED','sidecar_fire_ids':len(counts),'sidecar_fields_used':['original date ordinals','ragged record offsets'],'scientific_area_values_in_sidecar':False,'native_recovery_calls':len(idx)};maxerr=np.zeros(10);sumsq=np.zeros(10);den=np.zeros(10,int);calls=[];bytes_per=[];exact=0;start=time.perf_counter()
 with readonly(Path(a.lake)/DAILY) as db:
  for i in idx:
   t=time.perf_counter_ns();lo,hi=offsets[i:i+2];rows=[db.execute('SELECT id,date,dy_ar_km2 FROM "'+DAILY_TABLE+'" WHERE fid=?',(int(ref),)).fetchone() for ref in ds['native_fid_refs'][lo:hi]];assert all(str(r[0])==ds['ids'][i] for r in rows);value,mask=calculate([r[2] for r in rows],[date.fromisoformat(r[1]).toordinal() for r in rows]);assert np.array_equal(mask,ds['mask'][i]);valid=mask;diff=value[valid]-ds['y'][i,valid];maxerr[valid]=np.maximum(maxerr[valid],abs(diff));sumsq[valid]+=diff*diff;den[valid]+=1;exact+=np.array_equal(value[valid],ds['y'][i,valid]);calls.append(time.perf_counter_ns()-t);bytes_per.append(len(json.dumps(rows,separators=(',',':')).encode()))
 dump.update(seconds=time.perf_counter()-start,numerically_identical_fire_states=int(exact),max_absolute_property_error=maxerr.tolist(),returned_native_response_bytes=sum(bytes_per),filesystem_physical_bytes_read=None,median_call_ns=float(np.median(calls)),total_call_ns=int(sum(calls)),native_values_persisted=False,metadata_recovery_scope='counts/elapsed spans verified from metadata fields; full date sequence stays in original sidecar; source identity and quality not inferred')
 (out/'access-independent-validation.json').write_text(json.dumps(dump,indent=2)+'\n');np.savez_compressed(out/'private/native-access-costs.npz',test_indices=idx,call_ns=np.asarray(calls),returned_response_bytes=np.asarray(bytes_per))
 assert exact==len(idx),dump
 print(json.dumps(dump,indent=2))
if __name__=='__main__':main()
