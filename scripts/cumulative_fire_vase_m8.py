"""Actual short cumulative recovery and algebraic consistency, without inventing long histories."""
import argparse,csv,json
from pathlib import Path
import numpy as np


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';ds=dict(np.load(private/'observed-state.npz'));raw=np.load(private/'native-property-reference.npz')['reference'];results=[]
 for path in private.glob('paired-*-fullprecision.npz'):
  label=path.stem[len('paired-'):-len('-fullprecision')];v=dict(np.load(path));idx=v['test_indices'];pred=v['prediction'];total=np.expm1(pred[:,0]);first=np.expm1(pred[:,2]);last=np.expm1(pred[:,3])
  for n in (1,2):
   use=ds['n'][idx]==n;reference_total=raw[idx[use],0];errors=[(total[use]-reference_total)**2]
   if n==2:errors.append((first[use]-raw[idx[use],2])**2)
   per_fire=np.mean(np.stack(errors),axis=0);identity=abs(total[use]-first[use]) if n==1 else abs(total[use]-first[use]-last[use]);results.append({'method':label,'observations':n,'test_fires':int(use.sum()),'raw_source_unit_cumulative_prefix_rmse':float(np.sqrt(per_fire.mean())),'mean_absolute_sum_identity_residual':float(identity.mean()),'negative_cumulative_predictions':int(np.sum(total[use]<0)),'decreasing_two_point_cumulative_predictions':int(np.sum(total[use]<first[use])) if n==2 else None,'scope':'short observed-cumulative sequence only; longer full series not determined by this summary, no clipping'})
 with (out/'short-cumulative-recovery.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
 p=out/'exactness-register.json';m=json.loads(p.read_text());m['full_cumulative_sequence']='R0 computes retained-observation cumulative sums. R1 raw first/last/total exactly suffices for1/2 observations; PCA numerical inverse and learned probes can approximate those short cumulative sequences. General longer-history reconstruction is not uniquely determined: algebraic six-point state collision is unit-tested. Neither missing days nor physical full-fire area is filled/inferred.';m['R1']='Original-unit scientific scalar state retained as a derived reference artifact; numerical log/asinh model input is a separate preprocessing view, not source-bit preservation.';p.write_text(json.dumps(m,indent=2)+'\n');print('SHORT CUMULATIVE RECOVERY AND CONSISTENCY RECORDED',flush=True)
if __name__=='__main__':main()
