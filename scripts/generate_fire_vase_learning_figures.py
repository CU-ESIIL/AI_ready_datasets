"""Publication-style static diagnostics from the frozen synthetic M4 outputs."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',default='docs/assets/figures');a=p.parse_args()
    root=Path(a.results);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    e=json.loads((root/'evaluation.json').read_text());m=json.loads((root/'materialization.json').read_text())
    methods=['training_mean','persistence','interpretable_ridge','pca4_ridge','raw_ridge','learned4_ridge','tcn_end_to_end','mlp_end_to_end']
    labels=['Train mean','Persistence','Prefix summaries + ridge','PCA4 + ridge','Raw prefix + ridge','Learned4 + ridge','Temporal network','Matched tabular MLP']
    colors=['#777777']*4+['#2579b8','#e68020','#e68020','#2579b8']
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained')
    axes[0].barh(labels,[e[k]['test']['mse_log1p'] for k in methods],color=colors);axes[0].invert_yaxis()
    axes[0].set_xlabel('Held-out log(1 + growth) MSE (lower is better)');axes[0].set_title('256 transitions / 64 synthetic fires')
    for k,label in zip(methods[2:],labels[2:]):
        depths=sorted(e[k]['by_depth'],key=int);axes[1].plot([int(d) for d in depths],[e[k]['by_depth'][d]['mse_log1p'] for d in depths],marker='o',label=label)
    axes[1].set_xlabel('Observed prefix depth (days)');axes[1].set_ylabel('Held-out MSE');axes[1].legend(fontsize=7);axes[1].set_title('Depth strata; prefixes within fire are dependent')
    fig.suptitle('Synthetic future-observation task; no real-fire validity claim');fig.savefig(out/'fire-vase-learning-skill.png',dpi=170);plt.close(fig)
    n=np.logspace(0,4,200);c=m['construction_total_ns']/m['prefix_count']+(m['json_write_ns']+m['json_read_ns'])/m['prefix_count']
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
    ax.loglog(n,n*m['on_demand_encoder_plus_probe']['median_ns']/1e6,label='Encoder + same ridge head each query')
    ax.loglog(n,(c+n*m['stored_embedding_plus_same_probe']['median_ns'])/1e6,label='Stored embedding + same ridge head')
    ax.loglog(n,(m['on_demand_encoder_plus_probe']['median_ns']+(n-1)*m['cached_complete_prediction']['median_ns'])/1e6,label='Cached complete learned prediction')
    ax.loglog(n,(m['direct_interpretable_features_plus_probe']['median_ns']+(n-1)*m['cached_direct_feature_prediction']['median_ns'])/1e6,label='Cached direct-feature prediction')
    ax.set_xlabel('Identical queries per prefix');ax.set_ylabel('Scoped workload cost (ms)');ax.legend(fontsize=8)
    ax.set_title('Repeated-query accounting from local timings\nCommon encoder training excluded',fontsize=11)
    fig.savefig(out/'fire-vase-learning-reuse.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()
