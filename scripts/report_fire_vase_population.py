"""Summarize actual native/cache cohort metadata; no prediction outcomes or models."""
import argparse,csv,hashlib,json,math,sqlite3,statistics
from collections import Counter
from pathlib import Path
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from dataset_prototype.embedding_study.population_profile import DEPTHS,HORIZONS,size_class
from dataset_prototype.embedding_study.lake_design import learning_fraction


def write_csv(path,rows):
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);a=p.parse_args();out=Path(a.results);db=sqlite3.connect(out/'cohort-metadata.sqlite');db.row_factory=sqlite3.Row
    census=json.loads((out/'census.json').read_text());matrix=[];strata=[];training=[]
    db.execute('CREATE TABLE IF NOT EXISTS proposed_splits(id TEXT PRIMARY KEY,random_fold TEXT,temporal_fold TEXT,region TEXT)')
    db.execute('DELETE FROM proposed_splits')
    # Candidate splits only: no target values or model outcomes are used.
    for r in db.execute('SELECT id,year,region FROM events UNION ALL SELECT f.id,NULL,NULL FROM fire f WHERE f.source="native" AND NOT EXISTS(SELECT 1 FROM events e WHERE e.id=f.id)').fetchall():
        u=int(hashlib.sha256(('split:20260828:'+r['id']).encode()).hexdigest()[:16],16)/2**64
        fold='train' if u<.7 else 'validation' if u<.85 else 'test'
        y=r['year'];temporal='unknown_year' if y is None else 'train' if y<=2013 else 'selection' if y<=2016 else 'calibration' if y<=2018 else 'temporal_test'
        db.execute('INSERT INTO proposed_splits VALUES (?,?,?,?)',(r['id'],fold,temporal,r['region'] or 'unknown'))
    db.commit()
    assert db.execute('SELECT count(*) FROM proposed_splits').fetchone()[0]==db.execute('SELECT count(DISTINCT id) FROM proposed_splits').fetchone()[0]
    pq.write_table(pa.Table.from_pylist([dict(r) for r in db.execute('SELECT * FROM proposed_splits ORDER BY id')]),out/'proposed-fire-splits.parquet')
    for source in ('native','cache'):
        for d in DEPTHS:
            for h in HORIZONS:
                rs=list(db.execute('SELECT w.*,e.year,e.region,e.size_class AS catalog_size_class,f.observed_sum,f.observations,f.max_run,s.random_fold FROM windows w LEFT JOIN events e ON e.id=w.id JOIN fire f ON f.source=w.source AND f.id=w.id LEFT JOIN proposed_splits s ON s.id=w.id WHERE w.source=? AND w.depth=? AND w.horizon=?',(source,d,h)))
                values=[r['windows'] for r in rs];fires=len(rs);runs=sum(r['runs'] for r in rs);windows=sum(values)
                independent=db.execute('SELECT count(DISTINCT id),count(*),coalesce(sum(length-?-?+1),0) FROM runs WHERE source=? AND length>=? ',(d,h,source,d+h)).fetchone()
                assert (fires,runs,windows)==tuple(independent)
                strict=db.execute('SELECT count(*) FROM fire WHERE source=? AND strict=1 AND observations>=?',(source,d+h)).fetchone()[0]
                row={'source':source,'depth':d,'horizon':h,'eligible_fires':fires,'eligible_local_runs':runs,'dependent_windows':windows,'median_windows_per_eligible_fire':statistics.median(values) if values else None,'max_windows_per_fire':max(values,default=0),'strict_whole_history_fires':strict,'local_to_strict_fire_ratio':fires/strict if strict else None,'quality':'native measurement QA/uncertainty unknown; climate flags are not fire QA'};matrix.append(row)
                for dimension,fn in [('year',lambda r:str(r['year']) if r['year'] is not None else 'unknown'),('region',lambda r:r['region'] or 'unknown'),('observed_sum_size_km2',lambda r:size_class(r['observed_sum'])),('catalog_size_km2',lambda r:r['catalog_size_class'] or 'unknown'),('quality',lambda r:'unknown_native_measurement_QA')]:
                    c=Counter(fn(r) for r in rs)
                    for label,n in sorted(c.items()):strata.append({'source':source,'depth':d,'horizon':h,'dimension':dimension,'stratum':label,'eligible_fires':n})
                folds=Counter(r['random_fold'] or 'unknown' for r in rs)
                for fraction in (.01,.03,.1,.3,1.):
                    training.append({'source':source,'depth':d,'horizon':h,'training_fraction':fraction,'candidate_training_fires':sum(r['random_fold']=='train' and learning_fraction(r['id'],fraction,20260828) for r in rs),'candidate_validation_fires':folds['validation'],'candidate_test_fires':folds['test'],'design':'PROPOSED hash whole-fire70/15/15; not reviewed experimental split'})
    write_csv(out/'depth-horizon-eligibility.csv',matrix);write_csv(out/'eligibility-strata.csv',strata);write_csv(out/'learning-curve-sizes.csv',training)
    native=[r for r in matrix if r['source']=='native'];tasks=[]
    for task,d,h,meaning in [('A',3,1,'next supported day'),('B',3,3,'three consecutive future increments'),('C',3,3,'future/recent reference comparison; target interpretation remains explicit'),('D',3,3,'future population SD; no predictive performance measured'),('E',3,7,'future-pattern retrieval candidate only; same-fire exclusion required')]:
        row=next(r for r in native if (r['depth'],r['horizon'])==(d,h));tasks.append({'task':task,'depth':d,'horizon':h,'fires':row['eligible_fires'],'dependent_windows':row['dependent_windows'],'input_and_future_support':'complete exact-calendar bins for every counted window','meaning':meaning,'quality_limit':'native measurement QA and uncertainty unknown','scientific_validity':'candidate mathematical support, not independent ecological validation'})
    write_csv(out/'task-cohort-summary.csv',tasks)
    selection=[];populations={};depthcounts=[]
    queries={
      'A_catalog':'SELECT e.*,NULL AS observed_sum,NULL AS observations,NULL AS span,NULL AS gap_intervals FROM events e',
      'B_valid_native':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.valid_supported_rows>0',
      'C_local3':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.max_run>=3',
      'D_depth3_h1':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.max_run>=4',
      'E_depth7_h3':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.max_run>=10',
      'F_depth14_h7':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.max_run>=21',
      'G_strict':'SELECT e.*,f.observed_sum,f.observations,f.span,f.gap_intervals FROM fire f LEFT JOIN events e ON e.id=f.id WHERE f.source="native" AND f.strict=1'}
    for population,q in queries.items():
        rs=list(db.execute(q));populations[population]=len(rs)
        for dimension,fn in [('year',lambda r:str(r['year']) if r['year'] is not None else 'unknown'),('region',lambda r:r['region'] or 'unknown'),('catalog_size_km2',lambda r:r['size_class'] or 'unknown'),('observed_sum_size_km2',lambda r:size_class(r['observed_sum'])),('observation_count',lambda r:str(r['observations']) if r['observations'] is not None else 'not_applicable'),('span_days',lambda r:str(r['span']) if r['span'] is not None else 'not_applicable'),('gap_intervals',lambda r:str(r['gap_intervals']) if r['gap_intervals'] is not None else 'not_applicable')]:
            for label,n in sorted(Counter(fn(r) for r in rs).items()):selection.append({'population':population,'dimension':dimension,'stratum':label,'fires':n,'fraction':n/len(rs) if rs else None})
    for d in DEPTHS:
        row=db.execute('SELECT sum(max_run>=?),sum(strict=1 AND observations>=?) FROM fire WHERE source="native"',(d,d)).fetchone()
        runrow=db.execute('SELECT count(*),coalesce(sum(length-?+1),0) FROM runs WHERE source="native" AND length>=?',(d,d)).fetchone()
        depthcounts.append({'depth':d,'local_run_fires':row[0],'strict_whole_history_fires':row[1],'local_runs':runrow[0],'dependent_windows':runrow[1]})
    write_csv(out/'selection-distributions.csv',selection);write_csv(out/'temporal-depth.csv',depthcounts)
    # Source-native and cache joins stay diagnostic, never ecological support approval.
    extra={'populations':populations,'native_only_by_year':[dict(r) for r in db.execute("SELECT substr(date_key,1,4) AS year,count(*) AS observations,count(DISTINCT event) AS fires FROM keys a WHERE source='native' AND NOT EXISTS(SELECT 1 FROM keys b WHERE b.source='cache' AND b.key=a.key) GROUP BY year")],
    'native_only_catalog_membership':[dict(r) for r in db.execute("SELECT e.id IS NOT NULL AS in_catalog,count(*) AS rows,count(DISTINCT a.event) AS fires FROM keys a LEFT JOIN events e ON e.id=a.event WHERE a.source='native' AND NOT EXISTS(SELECT 1 FROM keys b WHERE b.source='cache' AND b.key=a.key) GROUP BY in_catalog")],
    'cache_climate_flags':[dict(r) for r in db.execute("SELECT sum(observations) AS rows,sum(climate_available) AS reported_climate_available_rows,sum(climate_available=observations) AS all_rows_flagged_available_fires FROM fire WHERE source='cache'")],
    'gaps':[dict(r) for r in db.execute('SELECT * FROM gaps ORDER BY source,days')],
    'observation_distribution':[dict(r) for r in db.execute("SELECT observations,count(*) AS fires FROM fire WHERE source='native' GROUP BY observations")],
    'run_distribution':[dict(r) for r in db.execute("SELECT length,count(*) AS runs,count(DISTINCT id) AS fires FROM runs WHERE source='native' GROUP BY length")],
    'quality':'Native measurement QA and uncertainty unprovided; source availability timestamps unprovided.',
    'region':'Reported fire_traits.region joined only by documented native ID string; no newly calculated geometry/CRS association.'}
    (out/'population-summary.json').write_text(json.dumps(extra,indent=2)+'\n')
    # Charts use measured summaries only, never synthetic cases or historical substitutes.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    figs=out/'figures';figs.mkdir(exist_ok=True)
    def save(fig,name):
        for ext in ('pdf','svg','png'):fig.savefig(figs/(name+'.'+ext),dpi=200,bbox_inches='tight')
        plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4),layout='constrained');labels=list(populations);ax.bar(labels,[populations[k] for k in labels]);ax.set(yscale='log',ylabel='Unique fires (log scale)',title='Measured populations: overlapping definitions, not a sequential funnel');ax.tick_params(axis='x',rotation=25);save(fig,'population-attrition')
    for key,x,name,y in [('observation_distribution','observations','observation-counts','fires'),('run_distribution','length','maximal-run-lengths','runs')]:
        rows=extra[key];fig,ax=plt.subplots(figsize=(7,4),layout='constrained');ax.bar([r[x] for r in rows],[r[y] for r in rows]);ax.set(yscale='log',xlabel='Observations per fire' if x=='observations' else 'Length of maximal local run (days)',ylabel=y+' (log scale)',title='Measured native '+name.replace('-',' '));save(fig,name)
    for metric,name in [('eligible_fires','eligible-fire-heatmap'),('dependent_windows','window-heatmap')]:
        vals=np.array([[next(r[metric] for r in native if r['depth']==d and r['horizon']==h) for h in HORIZONS] for d in DEPTHS]);fig,ax=plt.subplots(figsize=(7,5),layout='constrained');im=ax.imshow(np.log10(vals+1),aspect='auto',cmap='viridis');ax.set(xticks=range(3),xticklabels=HORIZONS,yticks=range(7),yticklabels=DEPTHS,xlabel='Future horizon (days)',ylabel='Input depth (days)',title='Measured native '+metric.replace('_',' '))
        for i in range(7):
            for j in range(3):ax.text(j,i,f'{vals[i,j]:,}',ha='center',va='center',color='white' if np.log10(vals[i,j]+1)<np.log10(vals.max()+1)*.6 else 'black')
        fig.colorbar(im,ax=ax,label='log10(count + 1)');save(fig,name)
    for dimension,name in [('region','geographic-selection'),('year','temporal-selection'),('catalog_size_km2','fire-size-selection')]:
        groups=['A_catalog','C_local3','D_depth3_h1','E_depth7_h3','F_depth14_h7'];keys=sorted({r['stratum'] for r in selection if r['dimension']==dimension})
        if dimension=='catalog_size_km2':keys=[k for k in ('<1','1–<10','10–<100','100–<1000','≥1000','unknown') if k in keys]
        fig,ax=plt.subplots(figsize=(10,4.5),layout='constrained');x=np.arange(len(keys))
        for k,g in enumerate(groups):
            vals={r['stratum']:r['fraction'] for r in selection if r['population']==g and r['dimension']==dimension};ax.plot(x,[100*vals.get(label,0) for label in keys],marker='o',label=g)
        ax.set(xticks=x,xticklabels=keys,ylabel='Share of cohort (%)',title='Measured selection by '+dimension+'; unknown strata retained');ax.tick_params(axis='x',rotation=45);ax.legend(fontsize=8);save(fig,name)
    fig,ax=plt.subplots(figsize=(7,4),layout='constrained');ax.plot(DEPTHS,[r['local_run_fires'] for r in depthcounts],'o-',label='Any supported local run');ax.plot(DEPTHS,[r['strict_whole_history_fires'] for r in depthcounts],'s-',label='Entire retained history consecutive');ax.set(yscale='log',xlabel='Required run length (days)',ylabel='Unique fires (log scale)',title='Measured local-run versus whole-history eligibility');ax.legend();save(fig,'local-versus-strict')
    print(json.dumps({'populations':populations,'native_matrix':native},indent=2))
    db.close()
if __name__=='__main__':main()
