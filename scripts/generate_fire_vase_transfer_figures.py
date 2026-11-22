"""Static figures from immutable synthetic multitask results, no training/inference."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',default='docs/assets/figures');a=p.parse_args();root=Path(a.results);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    e=json.loads((root/'evaluation.json').read_text());r=json.loads((root/'retrieval.json').read_text());c=json.loads((root/'reuse_economics.json').read_text())
    methods=['raw','interpretable','PCA4','frozen_A','shared_AD','task_specific','direct_MLP'];labels=['Raw heads','Prefix summaries','PCA4','Frozen A-only','Shared A–D','Aligned specific','Direct tabular MLP']
    ratio=np.array([[e[n][t]['test']['brier' if t=='C' else 'mse_log1p']/e['raw'][t]['test']['brier' if t=='C' else 'mse_log1p'] for t in 'ABCD'] for n in methods])
    fig,axes=plt.subplots(1,2,figsize=(12,4.9),layout='constrained')
    image=axes[0].imshow(ratio,cmap='RdBu_r',norm=LogNorm(vmin=1/float(ratio.max()),vmax=float(ratio.max())))
    axes[0].set_yticks(range(len(labels)),labels);axes[0].set_xticks(range(4),['A next day','B 3-day sum','C acceleration','D variability'],rotation=18)
    for i in range(len(methods)):
        for j in range(4):axes[0].text(j,i,f'{ratio[i,j]:.3f}',ha='center',va='center',fontsize=9,color='white' if ratio[i,j]>1.8 else 'black')
    axes[0].set_title('Task loss / raw-head loss (lower is better)');bar=fig.colorbar(image,ax=axes[0],shrink=.65);bar.set_ticks([.5,1.,2.]);bar.set_ticklabels(['0.5','1.0','2.0']);bar.set_label('Loss/raw (log colour scale)',fontsize=8)
    names=['raw','interpretable','PCA4','frozen_A','shared_AD','specific_E'];x=np.arange(len(names));direct=[r[n]['representation_distance']['mean_fire_precision_at_k'] for n in names];supervised=[r[n]['E_supervised_head_distance']['mean_fire_precision_at_k'] for n in names]
    axes[1].bar(x-.18,direct,.36,label='Representation distance');axes[1].bar(x+.18,supervised,.36,label='New E-supervised head distance')
    axes[1].axhline(r['raw']['representation_distance']['chance_precision_at_k'],linestyle='--',color='#777777',label='k / candidate count')
    axes[1].set_xticks(x,['Raw','Summaries','PCA4','Frozen A','Shared AD','E-specific'],rotation=25);axes[1].set_ylabel('Future-outcome precision@10');axes[1].set_title('No same-fire candidates; no ecological labels');axes[1].legend(fontsize=7,labelspacing=.25)
    fig.suptitle('Task-conditioned synthetic transfer and retrieval');fig.savefig(out/'fire-vase-transfer-tasks.png',dpi=170);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.2),layout='constrained')
    for name,label in [('raw','Raw prefix + heads'),('interpretable','Prefix summaries + heads'),('frozen_A','Frozen A encoder once + heads'),('shared_AD','Shared AD encoder once + heads')]:
        ax.plot(range(1,5),[b['on_demand_shared_encoding_plus_heads_ns']/1000 for b in c['views'][name]['bundles']],marker='o',label=label)
    ax.plot(range(1,5),[v['separate_encoders_plus_heads_ns']/1000 for v in c['task_specific_encoders']],marker='s',label='Separate task-specific encoders')
    ax.plot(range(1,5),[b['materialized_heads_ns']/1000 for b in c['views']['shared_AD']['bundles']],marker='^',label='Stored shared vector + heads')
    ax.set_xticks(range(1,5));ax.set_xlabel('Distinct task heads in one prefix bundle');ax.set_ylabel('Local warm bundle cost (µs)');ax.set_title('Heterogeneous task reuse; preparation/training excluded');ax.legend(fontsize=8);ax.grid(alpha=.2)
    fig.savefig(out/'fire-vase-transfer-reuse.png',dpi=170);plt.close(fig)

if __name__=='__main__':main()
