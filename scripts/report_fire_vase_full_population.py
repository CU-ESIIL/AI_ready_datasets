"""Regenerate observed-population figure and short-prefix eligibility, no model fitting."""
import argparse,csv,json,sqlite3,statistics
from pathlib import Path
from dataset_prototype.embedding_study.population_profile import window_count


def main():
    p=argparse.ArgumentParser();p.add_argument('--census',required=True);p.add_argument('--results',required=True);a=p.parse_args();out=Path(a.results);r=json.loads((out/'short-history-audit.json').read_text());rows=[]
    with sqlite3.connect(Path(a.census)/'cohort-metadata.sqlite') as db:
        lengths=list(db.execute("SELECT length,count(*) FROM runs WHERE source='native' GROUP BY length"))
        for d in (1,2):
            for h in (1,3,7):
                per=list(db.execute("SELECT id,sum(length-?-?+1),count(*) FROM runs WHERE source='native' AND length>=? GROUP BY id",(d,h,d+h)))
                independent=db.execute("SELECT count(DISTINCT id),sum(length-?-?+1),count(*) FROM runs WHERE source='native' AND length>=?",(d,h,d+h)).fetchone()
                assert (len(per),sum(x[1] for x in per),sum(x[2] for x in per))==independent
                assert sum(window_count(length,d,h)*n for length,n in lengths)==independent[1]
                if (d,h)==(1,1):assert independent[1]==db.execute("SELECT sum(exact_day_intervals) FROM fire WHERE source='native'").fetchone()[0]
                rows.append({'input_depth':d,'future_horizon':h,'eligible_fires':len(per),'dependent_windows':sum(x[1] for x in per),'local_runs':sum(x[2] for x in per),'median_windows_per_fire':statistics.median(x[1] for x in per),'max_windows_per_fire':max(x[1] for x in per),'scope':'secondary short-prefix prediction eligibility; no outcomes/models evaluated'})
    with (out/'short-prefix-eligibility.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained');labels=['1 observation','2 observations','3+ observations'];values=[x['fires'] for x in r['primary_populations']]
    ax.bar(labels,values,color=['#176b87','#64a6bd','#afbec5'])
    for i,n in enumerate(values):ax.text(i,n+3500,f'{n:,}\n{100*n/r["all_native_fire_ids"]:.2f}%',ha='center',va='bottom')
    ax.set_ylim(0,max(values)*1.22);ax.set(ylabel='Native fire IDs',title='Primary benchmark: the full observed fire population');ax.spines[['top','right']].set_visible(False)
    for ext in ('png','pdf','svg'):fig.savefig(out/('primary-population.'+ext),dpi=200)
    plt.close(fig)
    print(json.dumps({'short_prefix_eligibility':rows,'primary_population':values},indent=2))
if __name__=='__main__':main()
