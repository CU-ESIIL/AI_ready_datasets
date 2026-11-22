"""Two-point order contrast at fixed dates; counterfactual sensitivity, not a new source."""
import argparse,json
from pathlib import Path
import numpy as np
from dataset_prototype.embedding_study.observed_state import calculate


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);out=Path(p.parse_args().output);ds=dict(np.load(out/'private/observed-state.npz',allow_pickle=False));raw=np.load(out/'private/native-property-reference.npz',allow_pickle=False)['reference'];indices=np.flatnonzero(ds['n']==2);different=0;pair=0
 for i in indices:
  start=ds['offsets'][i];days=ds['date_ordinals'][start:start+2].tolist();a,m=calculate(raw[i,[2,3]].tolist(),days);b,mb=calculate(raw[i,[3,2]].tolist(),days);assert np.array_equal(m,mb);assert np.allclose(a[[0,1,4,9]],b[[0,1,4,9]]);assert a[2]==b[3] and a[3]==b[2];assert np.isclose(a[5],1-b[5]);assert m[6]==(days[1]-days[0]==1)
  if m[6]:assert np.isclose(a[6],-b[6]);pair+=1
  different+=bool(raw[i,2]!=raw[i,3])
 (out/'two-point-order-sensitivity.json').write_text(json.dumps({'native_two_point_fires':len(indices),'unequal_increment_pairs':different,'consecutive_pairs':pair,'invariant':'total/count/SD/span','order_sensitive':'first/last/first-share/first-half-share; consecutive change reverses sign where defined','scope':'controlled swap of native two-point values at fixed observed dates; recipe sensitivity, not a biological time reversal or encoder-equivariance claim'},indent=2)+'\n');print('TWO-POINT ORDER CONTRAST VERIFIED')
if __name__=='__main__':main()
