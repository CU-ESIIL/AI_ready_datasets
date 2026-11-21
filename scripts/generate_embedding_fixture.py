"""Generate tiny, explicit CC0 synthetic histories and independently specified tasks."""
from datetime import date, timedelta
import json
from pathlib import Path
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.contracts import Dataset, TaskSet
from dataset_prototype.embedding_study.metadata import OP_UNITS

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT/'data/fixtures/embedding_utility'


def history(identifier, growth, split='evaluation', missing=(), omitted=(), unknown_baseline=False):
    first = date(2020,1,1)
    source = {'source_id':'generated-fire-histories','version':'1','uri':'generator://fire-vase-utility-v1',
        'license':'CC0-1.0','attribution':'Project-authored synthetic mechanics fixtures',
        'method':'Explicit generated cumulative observations; no wildfire observations',
        'checksum':digest({'generator':'generate_embedding_fixture-v1'}),'checksum_scope':'metadata',
        'synthetic':True,'temporal_support':'Evidenced synthetic one-calendar-day increments; missing days explicit',
        'spatial_support':'None: abstract generated fire histories, not mapped fires','uncertainty':'Exact generator numbers; no real measurement-uncertainty claim'}
    rows=[]; cumulative=0; prev=first-timedelta(days=1) if not unknown_baseline else None
    previous_area=0 if not unknown_baseline else None
    for i,value in enumerate(growth):
        cumulative+=value; day=first+timedelta(days=i)
        if i in omitted:
            continue
        available=i not in missing
        days=(day-prev).days if prev else None
        daily=cumulative-previous_area if available and days==1 and previous_area is not None else None
        rows.append({'observation_id':f'{identifier}:observation-{i:02d}', 'date':day.isoformat(),
            'available_at':None,'available':available,'cumulative_area':cumulative if available else None,
            'daily_growth':daily,'days_since_previous':days,
            'quality_flags':['synthetic','availability_time_unknown']+(['missing_observation'] if not available else [])+
                (['observed_zero_growth'] if daily==0 else [])+(['temporal_gap'] if days and days>1 else [])})
        if available:
            prev,previous_area=day,cumulative
    return {'fire_id':identifier,'split':split,'area_unit':'km2','growth_unit':'km2/day','source':source,
        'baseline_date':None if unknown_baseline else '2019-12-31','baseline_area':None if unknown_baseline else 0,
        'baseline_evidence':None if unknown_baseline else 'Explicit synthetic observed zero baseline before first growth day',
        'observations':rows}


def main():
    histories=[]
    for i in range(24):
        n=3+i%7
        growth=[1+((i+3)*(j+1)*(j+2)+7*i+3*j*j)%29 for j in range(n)]
        histories.append(history(f'train-{i:02d}',growth,'train'))
    cases=[('constant',[5]*6,{}),('scaled',[50]*6,{}),('front',[15,8,3,2,1,1],{}),
        ('back',[1,1,2,3,8,15],{}),('pulses',[1,10,1,1,10,1],{}),('zeros',[0,10,0,0,10,0],{}),
        ('missing',[3]*6,{'missing':(2,)}),('omitted',[3]*6,{'omitted':(2,)}),
        ('unknown-baseline',[5]*6,{'unknown_baseline':True}),('all-zero',[0]*6,{})]
    histories.extend(history('eval-'+name,values,**kwargs) for name,values,kwargs in cases)
    dataset=Dataset.model_validate({'version':'synthetic-fire-vase-v1','source_note':'Synthetic only. No real Fire VASE or ecological results.', 'histories':histories})
    (TARGET/'histories.json').write_text(dataset.model_dump_json(indent=2)+'\n')
    tasks=[]
    by_id={h.fire_id:h for h in dataset.histories}
    def task(identifier,family,op,ids,question,suff=('R0',),**kwargs):
        typ={'peak_date':'date','profile':'profile','pulses':'pulses','nearest_profile':'ids','scientific_analog':'ids'}.get(op,'number')
        constraints=['source units unchanged','no raw fallback from R1/R2','synthetic retrospective task, not forecast']
        if op in {'profile','front_fraction','profile_distance','pca_distance','nearest_profile'}:
            constraints+=['>=3 consecutive evidenced daily increments and positive total','training-only frozen PCA if used']
        tasks.append({'task_id':identifier,'family':family,'question':question,'fire_ids':ids,'operation':op,'required_operations':[op],
            'required_observation_ids':[o.observation_id for identifier in dict.fromkeys([*ids,*kwargs.get('candidates',[])]) for o in by_id[identifier].observations],
            'answer_type':typ,'unit':OP_UNITS[op],'tolerance':1e-8 if typ in {'number','profile'} else 0,
            'permitted_representations':['R0','R1','R2'],'answerable':{r:r in suff for r in ('R0','R1','R2')},
            'ground_truth_method':'Independent Fraction interval integration; analytic generated observations; SVD PCA geometry where requested',
            'validity_constraints':constraints,'expected_provenance':['source','history_digest','observation_ids','upstream_commit'],
            'evidence_kind':'geometry_diagnostic' if family=='C' else 'exact',**kwargs})
    for name in ('constant','scaled','front','back','zeros'):
        task(f'area-{name}','A','cumulative',[f'eval-{name}'],'Observed cumulative area on 2020-01-06?',date='2020-01-06')
    task('daily-zero','A','daily_growth',['eval-zeros'],'Evidenced daily growth on observed zero-growth day?',date='2020-01-03')
    task('daily-missing','A','daily_growth',['eval-missing'],'Daily growth on missing observation date?',suff=(),date='2020-01-03')
    task('daily-after-gap','A','daily_growth',['eval-missing'],'Daily growth on first observation after a two-day interval?',suff=(),date='2020-01-04')
    task('daily-unknown-baseline','A','daily_growth',['eval-unknown-baseline'],'Daily growth without a prior evidenced baseline?',suff=(),date='2020-01-01')
    task('interval-known','A','interval_growth',['eval-front'],'Observed growth from January 2 to January 3?',start_date='2020-01-02',date='2020-01-03')
    task('interval-gap','A','interval_growth',['eval-missing'],'Total interval growth January 2 to January 4 (not daily rate)?',start_date='2020-01-02',date='2020-01-04')
    task('max-front','A','maximum_daily_growth',['eval-front'],'Largest observed daily increment in complete sequence?')
    task('max-zero','A','maximum_daily_growth',['eval-all-zero'],'Largest daily increment when all observations show zero growth?')
    task('peak-back','A','peak_date',['eval-back'],'Date of first maximum observed daily growth?')
    task('duration','A','sequence_days',['eval-constant'],'Number of evidenced consecutive one-day growth intervals from baseline (source-ID sidecar available)?',suff=('R0','R1','R2'))
    task('pulses','A','pulses',['eval-pulses'],'Observed pulse count and dates under upstream 20%-prominence rule?')
    for name in ('constant','front','back','zeros'):
        task(f'profile-{name}','B','profile',[f'eval-{name}'],'Construct the 20-bin mass-conserving allocation profile.',suff=('R0','R1'))
    task('front-fraction','B','front_fraction',['eval-front'],'Fraction of observed allocation in first half of development?',suff=('R0','R1'))
    task('back-fraction','B','front_fraction',['eval-back'],'Fraction of observed allocation in first half of development?',suff=('R0','R1'))
    task('profile-gap','B','profile',['eval-missing'],'Construct primary calendar-time developmental profile despite missing data?',suff=())
    task('profile-zero','B','profile',['eval-all-zero'],'Normalize a zero-total history?',suff=())
    task('distance-scaled','B','profile_distance',['eval-constant','eval-scaled'],'Euclidean distance of normalized profiles (absolute sizes differ)?',suff=('R0','R1'))
    task('distance-order','C','profile_distance',['eval-front','eval-back'],'Exact unscaled 20-bin Euclidean developmental distance?',suff=('R0','R1'))
    task('pca-geometry','C','pca_distance',['eval-front','eval-back'],'Distance in declared frozen three-component standardized PCA geometry?',suff=('R0','R1','R2'))
    task('neighbor-fidelity','C','nearest_profile',['eval-front'],'Retrieve two neighbors by full-profile Euclidean distance; PCA uses backprojected approximations in original profile units.',
        suff=('R0','R1','R2'),candidates=['eval-back','eval-constant','eval-pulses','eval-zeros'],approximation_allowed=True)
    task('scientific-analogs','C','scientific_analog',['eval-front'],'Which fires are independently validated scientific analogs?',suff=(),evidence_kind='pending_external_validation')
    # No assistant-authored expert relevance labels: the final task must abstain.
    spec=TaskSet.model_validate({'version':'fire-vase-tasks-v1','tasks':tasks})
    (TARGET/'tasks.json').write_text(spec.model_dump_json(indent=2)+'\n')


if __name__=='__main__':
    main()
