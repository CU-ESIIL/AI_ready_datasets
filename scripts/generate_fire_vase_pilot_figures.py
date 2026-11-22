"""Static scientific diagnostics from retained measurements; no model invocation."""
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',default='docs/assets/figures');args=p.parse_args()
    results=Path(args.results);target=Path(args.output);target.mkdir(parents=True,exist_ok=True)
    summary=json.loads((results/'summary.json').read_text());costs=json.loads((results/'cost_calibration.json').read_text())
    fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
    for ax,op in zip(axes,('front_fraction','profile_distance','pca_distance')):
        row=next(x for x in summary['direct_comparisons'] if x['operation']==op)
        labels=[];cold=[];warm=[]
        for r in ('R0','R1','R2'):
            if row[r]['median_cold_ns'] is not None:
                labels.append(r);cold.append(row[r]['median_cold_ns']/1000);warm.append(row[r]['median_warm_ns']/1000)
        x=np.arange(len(labels));ax.bar(x-.18,cold,.36,label='Cold application query');ax.bar(x+.18,warm,.36,label='Exact-query cache hit')
        ax.set_xticks(x,labels);ax.set_yscale('log');ax.set_title(op.replace('_',' '));ax.set_ylabel('Local interface time (µs)');ax.grid(axis='y',alpha=.2)
    axes[0].legend(fontsize=8);fig.suptitle('Synthetic operations: optimized and cached direct rivals (resident inputs)')
    fig.savefig(target/'fire-vase-pilot-costs.png',dpi=170);plt.close(fig)
    import gzip
    with gzip.open(results/'episodes.jsonl.gz','rt') as f:episodes=[json.loads(line) for line in f]
    row=next(e for e in episodes if e['category']=='efficiency' and e['task_pareto_min_valid_cost_ns'] is not None and all(e['representation_sufficiency'].values()) and e['regime']=='adaptive')
    c=costs[row['task_id']];n=np.logspace(0,4,200)
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    for ax,paid in zip(axes,(False,True)):
        for r,v in c.items():
            total=(0 if paid else v['preparation_ns'])+v['cold_ns']+(n-1)*v['warm_ns']
            ax.loglog(n,total/1e6,label=r)
        ax.set_title('Preparation already paid' if paid else 'Preparation charged');ax.set_xlabel('Identical queries N (accounting scenario)');ax.set_ylabel('Workload computation cost (ms)');ax.grid(alpha=.2);ax.legend()
    fig.suptitle('Counterfactual amortization from measured inputs; excludes agent routing')
    fig.savefig(target/'fire-vase-pilot-amortization.png',dpi=170);plt.close(fig)
    print('Wrote two synthetic diagnostic figures')

if __name__=='__main__':main()
