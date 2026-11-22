"""Deterministic development/evaluation generation; no model outputs enter generation."""
from datetime import date,timedelta
import json
from pathlib import Path
import random
from ..contracts import digest
from .contracts import Dataset, Observation
from .pilot_contracts import PilotTask, CLAIMS

SEEDS={'training':814031,'development':814133,'evaluation':814267,'schedule':814399}


def make_history(identifier,values,split,first,kind):
    rows=[];total=0;prev=first-timedelta(days=1);prior=0
    baseline_unknown=kind=='unknown_baseline'
    if baseline_unknown:prev=prior=None
    for k,value in enumerate(values):
        total+=value;day=first+timedelta(days=k)
        if kind=='omitted' and k==5:continue
        available=not(kind=='missing' and k==3)
        days=(day-prev).days if prev else None
        daily=total-prior if available and days==1 and prior is not None else None
        rows.append({'observation_id':f'{identifier}:r{k:03d}','date':str(day),'available_at':None,
          'available':available,'cumulative_area':total if available else None,'daily_growth':daily,
          'days_since_previous':days,'quality_flags':['synthetic','availability_unknown']})
        if available:prev,prior=day,total
    source={'source_id':'generated-m3','version':'3','uri':'generator://fire-utility-m3',
      'license':'CC0-1.0','attribution':'Project-authored synthetic mechanics fixtures',
      'method':'Seeded integer cumulative sequences; no wildfire observations','checksum':'0'*64,
      'checksum_scope':'observations','synthetic':True,'temporal_support':'Calendar-day observations with explicit gaps and unknown availability times',
      'spatial_support':'None; abstract synthetic histories','uncertainty':'Exact synthetic generator numbers; no real measurement uncertainty model'}
    baseline=None if baseline_unknown else first-timedelta(days=1)
    rows=[Observation.model_validate(r).model_dump(mode='json') for r in rows]
    packet={'observations':rows,'baseline_date':str(baseline) if baseline else None,
      'baseline_area':None if baseline_unknown else 0.0,'area_unit':'km2','growth_unit':'km2/day'}
    source['checksum']=digest(packet)
    return {'fire_id':identifier,'split':split,'area_unit':'km2','growth_unit':'km2/day','source':source,
      'baseline_date':packet['baseline_date'],'baseline_area':packet['baseline_area'],
      'baseline_evidence':None if baseline_unknown else 'Explicit generated observed zero baseline','observations':rows}

# Templates below are partitioned before any real inference. Development uses a
# different declarative layout; evaluation mixes narrative contrasts and constraints.
EVAL_TEMPLATES=[
 ('ledger','observation','cumulative','The ledger closes on {date}. Report the recorded burned extent then, retaining its native unit.'),
 ('one_day','observation','daily_growth','For the calendar day ending {date}, is a one-day increment evidenced? Return it only if the observations establish it.'),
 ('window','observation','interval_growth','How much area was added between the two recorded endpoints {start} and {date}? The target is an interval total.'),
 ('contrast','observation','growth_compare','Over {start} to {date}, subtract the second history’s added area from the first history’s. Compare absolute change, not shape.'),
 ('early_budget','morphology','front_fraction','Treat the completed development as a unit-length clock. What share of the burned-area addition falls before its midpoint?'),
 ('late_budget','morphology','late_fraction','How much of the unit total is assigned to the final quarter of completed development?'),
 ('allocation','morphology','profile','Provide the complete twenty-cell allocation of the history’s unit mass over its completed development.'),
 ('pathways','morphology','profile_distance','Compare the two complete developmental pathways using Euclidean separation of their twenty allocation cells; require full-profile fidelity.'),
 ('recurrence','morphology','pulse_count','Under the frozen padded twenty-percent prominence convention, how many recurrent growth peaks occur? Return only the count, not dates.'),
 ('coordinates','compression','pca_distance','For the two histories, report Euclidean separation in the frozen standardized three-axis geometry. No full-profile claim is requested.'),
 ('projected','compression','projected_distance','Reconstruct the two three-axis projections into allocation units and report their Euclidean separation. This projected geometry, not the original profile, is the target.'),
 ('discarded','compression','reconstruction_error','Quantify the L2 allocation mass discrepancy between the full history profile and its reconstruction from the three retained axes.'),
 ('ranking','compression','neighbor_stability','Among the three offered candidates, does the first-ranked neighbor remain the same after three-axis reconstruction? Report both identities and stability; use full-profile Euclidean distance as the comparator.'),
 ('scale','cross_representation','assess_claim','Assess the claim that a unit-total developmental allocation determines absolute burned area without any original area observations.'),
 ('inverse','cross_representation','assess_claim','Assess whether three retained coordinates alone establish the exact twenty allocation values of an unrestricted history.'),
 ('relevance','validity','assess_claim','Does closeness in the three-axis plot establish an independently validated ecological analog for this synthetic fire? Assess the evidence claim.'),
 ('uncertainty','validity','assess_claim','Can this synthetic source establish a calibrated uncertainty distribution for real burned-area measurements? Assess the evidence claim.'),
 ('availability','validity','assess_claim','Do these records establish that their values were available to an operational forecaster at observation time? Assess the evidence claim.'),
 ('support_count','cross_representation','assess_claim','Can retained source identifiers and validated consecutive-profile context establish the number of one-day intervals? Assess the claim and return the count only if supported.'),
 ('lineage','validity','source_evidence','Report the retained source’s version, license, checksum coverage, synthetic status, temporal support and uncertainty evidence.'),
 ('scalar_workload','efficiency','front_fraction','A repeated analysis needs the first-half mass allocation, exactly. Choose an allowed view considering the declared preparation and query-reuse context.'),
 ('geometry_workload','efficiency','pca_distance','A repeated analysis needs distance in the frozen standardized three-axis geometry. Choose a view considering preparation and repeated-query context.'),
 ('residual_workload','efficiency','reconstruction_error','The audit needs the full-profile versus three-axis reconstruction L2 residual, exactly. Choose a view under the declared amortization context.'),
 ('approx_workload','efficiency','projected_distance','The analysis accepts only the explicitly defined reconstructed three-axis geometry in allocation units. Choose a view for this repeated workload; do not claim full-profile equality.')]


def generate():
    histories=[];cohorts={};kinds=['ordinary']*12+['missing','omitted','unknown_baseline','zero_total','observed_zero','plateau','two_pulses','scaled_shape']
    for cohort,count in [('training',32),('development',8),('evaluation',20)]:
        rng=random.Random(SEEDS[cohort]);ids=[]
        for k in range(count):
            n=(7+k%9) if cohort=='development' else (11+k%13) if cohort=='training' else (21+k%20)
            values=[rng.randrange(1,100)*(1+(j//5)%3) for j in range(n)]
            kind=kinds[k%len(kinds)] if cohort=='evaluation' else ['ordinary','observed_zero','omitted','unknown_baseline'][k%4] if cohort=='development' else 'ordinary'
            if kind=='zero_total':values=[0]*n
            if kind=='observed_zero':values[4:7]=[0]*3
            if kind=='plateau':values=[1]*(n//3)+[91]*(n//3)+[2]*(n-2*(n//3))
            if kind=='two_pulses':values=[1]*n;values[3]=values[-4]=200
            if kind=='scaled_shape':values=[v*7 for v in values]
            if cohort=='evaluation' and k in (1,19):
                original=next(h for h in histories if h['fire_id']=='m3-evaluation-00')
                base=[r['daily_growth'] for r in original['observations']]
                values=list(reversed(base)) if k==1 else [v*7 for v in base]
            identifier=f'm3-{cohort}-{k:02d}';ids.append(identifier)
            first=date(2031 if cohort=='evaluation' else 2027 if cohort=='development' else 2023,2,1)
            histories.append(make_history(identifier,values,'train' if cohort=='training' else 'evaluation',first,kind))
        cohorts[cohort]=ids
    dataset=Dataset.model_validate({'version':'synthetic-fire-vase-v1','source_note':'Milestone 3 synthetic-only independent cohorts; no operational or ecological validity','histories':histories})
    byid={h.fire_id:h for h in dataset.histories};tasks=[]
    # 24 scientific templates ×5 cases =120 evaluation questions, not 120 fires.
    for index,(template,category,op,text) in enumerate(EVAL_TEMPLATES):
        for replicate in range(5):
            i=([12,13,14,16,15][replicate] if index in (0,1,2) else 0 if index==7 and replicate<2 else 18 if index==8 and replicate==0 else 17 if index==8 and replicate==1 else (index*3+replicate*4)%20);identifier=cohorts['evaluation'][i];h=byid[identifier]
            other=cohorts['evaluation'][19 if index==7 and replicate==1 else (i+1)%12] # no unknown pair support hidden by reference
            pair=op in {'growth_compare','profile_distance','pca_distance','projected_distance'}
            day=(h.observations[3].date if index==0 and i==12 else h.observations[5].date if index==1 and i==13 else h.observations[0].date if index==1 and i==14 else h.observations[4 if replicate%2==0 else 6].date);start=h.observations[1].date
            query={'operation':op,'fire_ids':[identifier,other] if pair else [identifier]}
            if op in {'cumulative','daily_growth','interval_growth','growth_compare'}:query['date']=str(day)
            if op in {'interval_growth','growth_compare'}:query['start_date']=str(start)
            if op=='assess_claim':query['claim']={'scale':CLAIMS[0],'inverse':CLAIMS[1],'relevance':CLAIMS[2],'uncertainty':CLAIMS[3],'availability':CLAIMS[4],'support_count':CLAIMS[5]}[template]
            if op=='neighbor_stability':query['candidates']=[cohorts['evaluation'][(i+j)%12] for j in (1,2,3)]
            tasks.append(PilotTask(task_id=f'm3-e-{index:02d}-{replicate}',split='evaluation',template_id='eval-'+template,
              category=category,question=text.format(date=day,start=start),query=query,
              accuracy='projected_geometry' if op=='projected_distance' else 'exact',
              metadata_sensitivity='negative_control' if template in {'ledger','coordinates','lineage'} else 'hypothesized',
              preparation_paid=replicate%2==0,workload_queries=(1,10,100,1000,10000)[replicate]))
    for k in range(30):
        op=EVAL_TEMPLATES[k%len(EVAL_TEMPLATES)][2];identifier=cohorts['development'][k%8];h=byid[identifier]
        query={'operation':op,'fire_ids':[identifier,cohorts['development'][(k+1)%8]] if op in {'growth_compare','profile_distance','pca_distance','projected_distance'} else [identifier]}
        if op in {'cumulative','daily_growth','interval_growth','growth_compare'}:query['date']=str(h.observations[5].date)
        if op in {'interval_growth','growth_compare'}:query['start_date']=str(h.observations[1].date)
        if op=='assess_claim':query['claim']=CLAIMS[k%6]
        if op=='neighbor_stability':query['candidates']=[cohorts['development'][(k+j)%8] for j in (1,2,3)]
        tasks.append(PilotTask(task_id=f'm3-d-{k:02d}',split='development',template_id=f'development-specification-{k%24}',
          category=EVAL_TEMPLATES[k%24][1],question=f'Development specification: compute {op} for the supplied context; preserve scientific support.',
          query=query,accuracy='projected_geometry' if op=='projected_distance' else 'exact',metadata_sensitivity='hypothesized'))
    return dataset,tasks,cohorts


def write_fixture(target):
    target=Path(target);target.mkdir(parents=True,exist_ok=False)
    dataset,tasks,cohorts=generate()
    (target/'histories.json').write_text(dataset.model_dump_json(indent=2)+'\n')
    for split in ('development','evaluation'):
        (target/(split+'_tasks.json')).write_text(json.dumps([t.model_dump(mode='json') for t in tasks if t.split==split],indent=2)+'\n')
    (target/'generation.json').write_text(json.dumps({'version':'fire-pilot-generation-v3','seeds':SEEDS,'cohorts':cohorts,
      'task_count':len(tasks),'evaluation_questions':120,'evaluation_fires':20,
      'holdout_scope':'Disjoint histories, dates/values and authored templates relative to development. Public to implementers; model-unseen until any authorized pilot. No independent expert adjudication.',
      'scientific_scope':'Assistant-authored evidence-claim rubrics are drafts; arithmetic references independently checked by code, not human gold.'},indent=2)+'\n')
