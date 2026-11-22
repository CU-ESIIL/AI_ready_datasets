"""Analyze only existing upstream aggregate reports; never open observation tables.

This produces historical-cohort arithmetic, not a fresh population profiling run.
"""
import argparse,csv,hashlib,json,math
from pathlib import Path


def main():
    p=argparse.ArgumentParser();p.add_argument('--upstream',required=True);p.add_argument('--output',required=True);args=p.parse_args()
    source=Path(args.upstream).resolve();out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
    names=['analysis/v2/input_audit.json','analysis/v2/semantic_summary.json','analysis/scientific_validation/observation_counts.csv','analysis/scientific_validation/weather_selection_counts.csv','analysis/scientific_validation/final_report.md','scripts/fire_vase_v2.py']
    hashes={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in names}
    def rows(name):
        with (source/name).open() as f:return list(csv.DictReader(f))
    audit=json.loads((source/names[0]).read_text());semantic=json.loads((source/names[1]).read_text());selection=rows(names[3]);observations=rows(names[2])
    full={int(r['value']):int(r['n']) for r in selection if r['population']=='all_events' and r['dimension']=='observation_count'}
    primary={int(r['value']):int(r['n']) for r in selection if r['population']=='primary' and r['dimension']=='observation_count'}
    assert sum(full.values())==audit['raw_events']==semantic['n']
    assert sum(k*v for k,v in full.items())==audit['rows']
    assert sum(primary.values())==semantic['primary_n']
    assert audit['rows']-audit['cached_events']==audit['one_day_transitions']+audit['longer_gaps']
    assert audit['raw_daily_rows']-audit['rows']==audit['source_rows_absent_from_cache']
    depths=[]
    for depth in (3,5,7,10,14,21,30):
        a=sum(v for k,v in full.items() if k>=depth);c=sum(v for k,v in primary.items() if k>=depth)
        depths.append({'depth':depth,'all_histories_observation_count_at_least_depth':a,'whole_history_consecutive_fires':c,'whole_history_consecutive_windows':sum((k-depth+1)*v for k,v in primary.items() if k>=depth),'whole_history_consecutive_fraction_of_catalog':c/audit['raw_events'], 'local_runs_in_gappy_histories':None})
    for record in observations:
        if record['observations'] in ('>=3','>=5','>=7'):
            d=int(record['observations'][2:]);assert next(r for r in depths if r['depth']==d)['whole_history_consecutive_fires']==int(record['consecutive'])
    predictions=[]
    for d in (3,7,14,30):
        for h in (1,3,7):
            fires=sum(v for k,v in primary.items() if k>=d+h);windows=sum((k-d-h+1)*v for k,v in primary.items() if k>=d+h)
            # Independent expression: number of windows is the sum of tail counts.
            assert windows==sum(sum(v for k,v in primary.items() if k>=length) for length in range(d+h,max(primary)+1))
            predictions.append({'depth':d,'horizon':h,'eligible_historical_whole_consecutive_fires':fires,'dependent_windows':windows,'supports_acceleration_and_variability':h>=3,'scope':'historical whole-consecutive-history subset only; gappy-history local windows unknown'})
    def table(dimension):
        a={r['value']:r for r in selection if r['population']=='all_events' and r['dimension']==dimension}
        b={r['value']:r for r in selection if r['population']=='primary' and r['dimension']==dimension}
        result=[]
        for key,v in a.items():
            n=int(v['n']);m=int(b.get(key,{}).get('n',0));result.append({'stratum':key,'all_events':n,'historical_primary':m,'selection_fraction':m/n,'all_event_share':n/audit['raw_events'],'primary_share':m/semantic['primary_n'],'weather_complete':int(v['complete'])})
        assert sum(r['all_events'] for r in result)==audit['raw_events'] and sum(r['historical_primary'] for r in result)==semantic['primary_n']
        return result
    report={'scope':'HISTORICAL_AGGREGATE_REANALYSIS_NOT_FRESH_FULL_LAKE_PROFILING','source_observation_rows_read':0,'source_arrays_read':0,'aggregate_rows_read':len(selection)+len(observations),'input_audit_historical':audit,'primary_fraction':semantic['primary_n']/audit['raw_events'],'one_observation_fraction':full[1]/audit['raw_events'],'two_observation_fraction':full[2]/audit['raw_events'],'consecutive_pair_fraction':audit['one_day_transitions']/(audit['one_day_transitions']+audit['longer_gaps']),'temporal_depth':depths,'prediction_windows_historical_subset':predictions,'region_selection':table('region'),'year_selection':table('year'),'exact_current_population_counts':None,'source_specific_scientific_power':None,'source_root':str(source),'source_hashes':hashes}
    (out/'historical-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    for name,data in [('temporal-depth',depths),('prediction-windows',predictions),('region-selection',report['region_selection']),('year-selection',report['year_selection'])]:
        with (out/(name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,3,figsize=(14,4.7),layout='constrained')
    x=[r['depth'] for r in depths]
    axes[0].plot(x,[r['all_histories_observation_count_at_least_depth'] for r in depths],'o-',label='Observation count only')
    axes[0].plot(x,[r['whole_history_consecutive_fires'] for r in depths],'s-',label='Whole history consecutive')
    axes[0].set(yscale='log',xlabel='Required observed depth',ylabel='Historical fires (log scale)',title='Temporal-support attrition');axes[0].legend(fontsize=8)
    r=report['region_selection'];axes[1].barh([v['stratum']+' ('+str(v['historical_primary'])+'/'+str(v['all_events'])+')' for v in r],[100*v['selection_fraction'] for v in r]);axes[1].set(xlabel='Whole-consecutive ≥3 / regional fires (%)',title='Historical region selection')
    y=report['year_selection'];axes[2].plot([int(v['stratum']) for v in y],[100*v['selection_fraction'] for v in y],'o-');axes[2].set(xlabel='Upstream event-year label',ylabel='Selected fires (%)',title='Historical year selection')
    fig.suptitle('Existing Fire VASE aggregate reports — not fresh full-lake profiling',fontsize=12)
    for suffix in ('png','pdf','svg'):fig.savefig(out/('historical-population.'+suffix),dpi=220)
    plt.close(fig)
    print(json.dumps({'historical_fires':audit['raw_events'],'historical_cached_rows':audit['rows'],'primary_fraction':report['primary_fraction'],'depths':depths,'output':str(out)},indent=2))

if __name__=='__main__':main()
