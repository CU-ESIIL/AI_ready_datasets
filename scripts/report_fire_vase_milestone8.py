"""Render publication-quality measured M8 figures and manuscript-ready scoped report."""
import argparse,csv,json,math
from pathlib import Path
import numpy as np


def read(path):
 with path.open() as f:return list(csv.DictReader(f))

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);private=out/'private';figdir=out/'figures';figdir.mkdir(exist_ok=True);ds=dict(np.load(private/'observed-state.npz'));info=read(out/'information-preservation.csv');ret=read(out/'retrieval-population-weighted.csv');life=read(out/'lifecycle-workload.csv');pred=read(out/'secondary-prediction.csv');pair=read(out/'secondary-prediction-paired.csv');general=read(out/'blocked-generalization.csv');ranks=json.loads((out/'rank-diagnostics.json').read_text());names=['Observed total','Observation count','First increment','Last increment','Variability','First share','Consecutive change','Local maxima','First-half share','Observed span'];from dataset_prototype.embedding_study.observed_state import NAMES
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
 def save(fig,name):
  for ext in ('pdf','svg','png'):fig.savefig(figdir/(name+'.'+ext),dpi=220,bbox_inches='tight')
  plt.close(fig)
 def score(method,property,stratum='all',fraction='1.0',probe='linear_ridge'):
  row=next(r for r in info if r['method']==method and r['property']==property and r['stratum']==stratum and r['fraction']==fraction and r['probe']==probe);return float(row['mse']) if row['mse'] else np.nan
 colors={'supervised':'#a44832','self_supervised':'#317a9b','multitask':'#517e3c','pca':'#795799'}
 # 1 measured full source population, not selected sequences.
 fig,ax=plt.subplots(figsize=(8,4),layout='constrained');counts=[int(np.sum(ds['n']==1)),int(np.sum(ds['n']==2)),int(np.sum(ds['n']>=3))];ax.bar(['1 observation','2 observations','3+ observations'],counts,color=['#176b87','#64a6bd','#b3c5cd'])
 for k,c in enumerate(counts):ax.text(k,c+3500,f'{c:,}\n{100*c/len(ds["n"]):.2f}%',ha='center')
 ax.set(ylim=(0,max(counts)*1.2),ylabel='Native fire IDs',title='Primary population: every observed fire history');save(fig,'01-population')
 # 2 exact, numerical, approximate and unsupported are different categories.
 labels=['Native source operations','Retained raw scientific state','PCA inverse at rank13','Learned state + fitted head','Common date/support metadata','Explicit native fallback'];categories=np.array([[0,0,0,0],[0,0,3,3],[1,1,3,3],[2,2,3,3],[3,0,0,3],[0,0,0,0]])
 fig,ax=plt.subplots(figsize=(10,4.7),layout='constrained');from matplotlib.colors import ListedColormap
 ax.imshow(categories,cmap=ListedColormap(['#5b9a76','#8ac2cf','#f0c371','#dadada']),vmin=0,vmax=3,aspect='auto');ax.set(xticks=range(4),xticklabels=['Defined scalar properties','Count / elapsed span','Original absolute\ndates','General longer\ncumulative series'],yticks=range(6),yticklabels=labels,title='Information status of the declared scientific-state pipeline')
 text={0:'Direct/reference',1:'Numerical roundtrip',2:'Model-dependent',3:'Not in this payload'}
 for i in range(6):
  for j in range(4):ax.text(j,i,text[categories[i,j]],ha='center',va='center',fontsize=8)
 save(fig,'02-information-status')
 # 3 full held-out property recovery. zero-native reference distinguished from display floor.
 methods=['raw_state']+['pca-request'+str(d) for d in (4,8,16)]+[f'{f}-{d}' for f in ('supervised','self_supervised','multitask') for d in (4,16,64)];data=np.array([[score(m,p) for p in NAMES] for m in methods]);fig,ax=plt.subplots(figsize=(12,7),layout='constrained');im=ax.imshow(np.log10(np.maximum(data,1e-12)),aspect='auto',cmap='viridis_r',vmin=-12,vmax=1);ax.set(xticks=range(10),xticklabels=names,yticks=range(len(methods)),yticklabels=methods,title='Held-out linear-probe recovery: standardized MSE');ax.tick_params(axis='x',rotation=45);fig.colorbar(im,ax=ax,label='log10 MSE (display floor1e-12)');save(fig,'03-property-recovery')
 # 4 property-based retrieval, population post-stratified, same full galleries.
 taskids=['log_observed_total','log_observed_std','first_allocation','asinh_mean_consecutive_change','log_observed_span'];fig,ax=plt.subplots(figsize=(11,4.5),layout='constrained')
 for method,route in [('cached_native','exact_property_index'),('pca-request16','coordinates'),('pca-request16','supervised_linear_ridge'),('supervised-16','coordinates'),('self_supervised-16','coordinates'),('multitask-16','coordinates'),('multitask-16','supervised_linear_ridge')]:
  v=[float(next(r['precision_at10'] for r in ret if r['method']==method and r['route']==route and r['property']==t)) for t in taskids];ax.plot(range(5),v,'o-',label=method+' / '+route)
 ax.set(xticks=range(5),xticklabels=['Observed area','Variability','First share','Consecutive change','Observed span'],ylim=(0,1.04),ylabel='Precision@10, native-test-population weighted',title='Declared-property retrieval, not ecological analog discovery');ax.legend(fontsize=7,loc='lower left');save(fig,'04-retrieval')
 # 5 frozen transfer versus objective. First/last/share/change are not supervised objectives.
 transfer=['log_observed_total','log_first_increment','log_last_increment','log_observed_std','first_allocation','asinh_mean_consecutive_change','strict_interior_peak_count'];fig,ax=plt.subplots(figsize=(11,4.8),layout='constrained')
 for family in ('supervised','self_supervised','multitask'):ax.plot(range(len(transfer)),[score(family+'-16',p) for p in transfer],'o-',label=family,color=colors[family])
 ax.set(yscale='log',xticks=range(len(transfer)),xticklabels=['Total','First','Last','Variability','First share','Change','Local maxima'],ylabel='Held-out standardized MSE',title='Frozen16-D state + linear heads: task-dependent transfer');ax.legend();save(fig,'05-cross-task-transfer')
 # 6 one-/two-/long-history errors, no NA fields converted to zero.
 fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,prop,title in zip(axes,['log_observed_total','log_observed_std'],['Observed total','Observed variability']):
  for family in ('supervised','self_supervised','multitask'):ax.plot(range(3),[score(family+'-16',prop,s) for s in ('one','two','three_plus')],'o-',label=family,color=colors[family])
  ax.set(yscale='log',xticks=range(3),xticklabels=['1 observation','2 observations','3+ observations'],ylabel='Standardized MSE',title=title)
 axes[0].legend();save(fig,'06-history-strata')
 # 7 all requested dimensions, not selecting a favorable test dimension.
 fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,prop in zip(axes,['log_observed_total','first_allocation']):
  for family in ('supervised','self_supervised','multitask'):ax.plot([4,8,16,32,64],[score(family+'-'+str(d),prop) for d in (4,8,16,32,64)],'o-',label=family,color=colors[family])
  ax.plot([4,8,16,32,64],[score('pca-request'+str(d),prop) for d in (4,8,16,32,64)],'s--',label='PCA (effective rank capped13)',color=colors['pca']);ax.set(xscale='log',yscale='log',xlabel='Requested coordinate dimension',ylabel='Standardized MSE',title=prop)
 axes[0].legend(fontsize=8);save(fig,'07-dimension-sensitivity')
 # 8 fixed held-out cases for all fractions.
 fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,prop in zip(axes,['log_observed_total','first_allocation']):
  for family in ('supervised','self_supervised','multitask'):ax.plot([.01,.03,.1,.3,1.],[score(family+'-16',prop,fraction=str(f)) for f in (.01,.03,.1,.3,1.)],'o-',label=family,color=colors[family])
  ax.plot([.01,.03,.1,.3,1.],[score('raw_state',prop,fraction=str(f)) for f in (.01,.03,.1,.3,1.)],'k--',label='same-label raw-state ridge');ax.set(xscale='log',yscale='log',xlabel='Fraction of training fires',ylabel='Standardized MSE',title=prop)
 axes[0].legend(fontsize=8);save(fig,'08-learning-curves')
 # 9 actual same-workload batch-serving cost versus accuracy, not universal production economics.
 fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
 for row in life:
  error=max(float(row['standardized_fire_mean_property_mse']),1e-16);latency=float(row['batch_serving_seconds'])*1000;method=row['method'];color='#222222' if method.startswith(('cached','interpretable','adaptive')) else colors['pca'] if method.startswith('pca') else colors['self_supervised'] if method.startswith('self') else colors['multitask'] if method.startswith('multi') else colors['supervised'];ax.scatter(latency,error,c=color)
  if method in ('cached_native','interpretable_exact','pca-request16','supervised-16','self_supervised-16','multitask-16','multitask-16-on-demand'):ax.annotate(method,(latency,error),fontsize=7,xytext={'cached_native':(5,19),'interpretable_exact':(5,3),'supervised-16':(-70,3),'multitask-16':(5,-14)}.get(method,(5,5)),textcoords='offset points',arrowprops={'arrowstyle':'-','lw':.5})
 ax.set(xscale='log',yscale='log',xlabel='Measured4096-fire warm batch kernel (ms)',ylabel='Standardized property-bundle MSE (zero at display floor)',title='Same requests: native caching versus approximate representation serving');save(fig,'09-cost-accuracy')
 # 10 utility depends on the scientific task; prediction is explicitly secondary.
 primary=np.array([[score(f+'-16',p) for p in ('log_observed_total','log_last_increment','log_observed_std','first_allocation')] for f in ('supervised','self_supervised','multitask')]);fig,axes=plt.subplots(1,2,figsize=(12,4.7),layout='constrained');im=axes[0].imshow(np.log10(np.maximum(primary,1e-12)),aspect='auto',cmap='viridis_r');axes[0].set(xticks=range(4),xticklabels=['Total','Last','Variability','Allocation'],yticks=range(3),yticklabels=['Count-supervised16','Autoencoder16','Multitask16'],title='Primary observed-property recovery');fig.colorbar(im,ax=axes[0],label='log10 standardized MSE')
 models=['last_increment_persistence','raw_state-linear','raw_state-nonlinear','self_supervised-16-linear','multitask-16-linear','direct_neural'];values=[float(next(r['fire_mean_log_growth_mse'] for r in pred if r['input_depth']=='1' and r['horizon']=='1' and r['parent_history_stratum']=='all' and r['method']==m)) for m in models];axes[1].barh(range(len(models)),values);axes[1].set(yticks=range(len(models)),yticklabels=models,xlabel='Fire-mean log1p future-growth MSE',title='Secondary: one observed day → next day');save(fig,'10-task-dependent-utility')
 # Additional measured diagnostics: blocked refits, controlled retrieval scaling and access.
 fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for ax,split in zip(axes,['temporal','geographic_west']):
  subset=[r for r in general if r['split']==split and r['stratum']=='all' and r['property']=='log_observed_total'];ax.barh([r['method'] for r in subset],[float(r['standardized_mse']) for r in subset]);ax.set(xscale='log',xlabel='Standardized area MSE',title='Refit transfer: '+split)
 save(fig,'11-blocked-generalization')
 scaling=read(out/'retrieval-scaling.csv');fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
 for method in ('cached_native','pca-request16','supervised-16','self_supervised-16','multitask-16','multitask-16-supervised_head'):
  rs=sorted([r for r in scaling if r['method']==method and r['queries']=='4096'],key=lambda r:int(r['gallery_fires']));axes[0].plot([int(r['gallery_fires']) for r in rs],[float(r['precision_at10_ties']) for r in rs],'o-',label=method);axes[1].plot([int(r['gallery_fires']) for r in rs],[float(r['query_seconds']) for r in rs],'o-',label=method)
 axes[0].set(xscale='log',ylabel='Precision@10',xlabel='Training-gallery fires',title='Controlled observed-area retrieval');axes[1].set(xscale='log',yscale='log',ylabel='4096-query batch seconds',xlabel='Training-gallery fires',title='Measured query scaling');axes[0].legend(fontsize=7);save(fig,'12-retrieval-scaling')
 # Full lifecycle cost/accuracy frontiers use declared component-sum scenarios.
 scenarios=read(out/'cost-accuracy-pareto.csv');fig,axes=plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
 for ax,queries in zip(axes,(1,1000,1000000)):
  for row in scenarios:
   if int(row['query_fire_count'])!=queries:continue
   method=row['method'];error=max(float(row['property_mse']),1e-16);cost=float(row['component_sum_seconds']);color='#222222' if method.startswith(('cached','interpretable','adaptive')) else colors['pca'] if method.startswith('pca') else colors['self_supervised'] if method.startswith('self') else colors['multitask'] if method.startswith('multi') else colors['supervised'];ax.scatter(cost,error,color=color,marker='x' if row['dominated']=='True' else 'o',s=25)
   if method in ('adaptive_native_exact','pca-request16','self_supervised-16'):
    ax.annotate(method,(cost,error),xytext=(3,4),textcoords='offset points',fontsize=6)
  ax.set(xscale='log',yscale='log',xlabel='Preparation + fitting + encoding + serving (s)',title=f'{queries:,} fire queries',ylim=(1e-17,2))
 axes[0].set_ylabel('Property-bundle MSE (zero at display floor)');fig.suptitle('Lifecycle frontier: measured component sums, not empirical production totals');save(fig,'13-lifecycle-frontier')
 # Task eligibility and unavailable features remain visible.
 eligibility=[{'property':name,'eligible_all_native_fires':int(ds['mask'][:,j].sum()),'undefined_all_native_fires':int((~ds['mask'][:,j]).sum()),'eligible_test_fires':int(ds['mask'][ds['fold']=='test',j].sum()),'native_quality':'unknown'} for j,name in enumerate(NAMES)]
 with (out/'property-eligibility.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(eligibility[0]));w.writeheader();w.writerows(eligibility)
 print('FIGURES AND ELIGIBILITY GENERATED',flush=True)
if __name__=='__main__':main()
