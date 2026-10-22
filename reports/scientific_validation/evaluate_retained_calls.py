"""Re-evaluate immutable retained model calls; no new model requests or execution."""
import json,hashlib
from pathlib import Path
from collections import defaultdict
from statistics import mean,median
from dataset_prototype.decision_experiment import evaluate_response,summarize
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent

def main():
 source=ROOT/'run/scientific-validation-verde';out=HERE/'data/model_experiment';out.mkdir(exist_ok=True)
 calls=[json.loads(x) for x in (source/'calls.jsonl').read_text().splitlines()];tasks={t['task_id']:t for t in json.loads((ROOT/'data/fixtures/validation/decision_tasks.json').read_text())};rows=[]
 # Original call timestamps were labeled started_at after receipt in this runner version.
 for c in calls:
  raw=c['response'] if c['response'] is not None else c['trace']['output_json']
  for arm in ['A'] if c['arm']=='A' else ['B','C','D']:
   row=evaluate_response(raw,tasks[c['task_id']],arm);row.update(repeat=c['repeat'],model=c['trace']['model'],provider=c['trace']['provider'],call_status=c['status'],elapsed_seconds=c['elapsed_seconds']);rows.append(row)
 summary=summarize(rows);summary['call_counts']={'total':len(calls),'returned':sum(c['status']=='returned' for c in calls),'failed':sum(c['status']=='failed' for c in calls)}
 summary['latency_seconds']={arm:{'mean':mean(c['elapsed_seconds'] for c in calls if c['arm']==arm),'median':median(c['elapsed_seconds'] for c in calls if c['arm']==arm)} for arm in ['A','B']}
 summary['reproducibility']={}
 for arm in ['A','B']:
  grouped=defaultdict(list)
  for c in calls:
   if c['arm']==arm:grouped[c['task_id']].append(c)
  comparable=[v for v in grouped.values() if len(v)==2 and all(x['response'] is not None for x in v)]
  summary['reproducibility'][arm]={'successful_repeat_pairs':len(comparable),'exact_response_matches':sum(v[0]['response']==v[1]['response'] for v in comparable),'stable_action_and_operation':sum(all(v[0]['response'].get(k)==v[1]['response'].get(k) for k in ['action','operation_id','concept_id','parameter_ref']) for v in comparable) if arm=='B' else None,'scope':'exact response equality includes rationale; structured stability separately compares action/operation/concept/parameter reference'}
 summary['protocol']={'model':'js2/gpt-oss-120b','provider':'verde','models_compared':1,'weaker_model_hypothesis':'NOT TESTED by this one-model pilot','arms':'A free prose content in mandatory transport JSON envelope; B decision schema; C/D paired deterministic re-evaluations, not additional inference','A_schema_rate':None,'A_scientific_accuracy':None,'human_gold':'pending; assistant-authored draft reference only','cost_and_token_usage':None,'provider_weights_digest':None,'response_scope':'plugin-normalized JSON, not raw provider text','grounding_metric':'syntactic evidence-ID citation presence/membership only, not truth of natural-language justification','unsupported_code_scoring':'lexical indicators only; not an expert-adjudicated unsafe-proposal rate','execution_rate':'zero by construction; never evidence of model competence','timestamp_caveat':'Original started_at field was recorded after the response; use elapsed_seconds for duration. Exact trace timestamp remains preserved.'}
 summary['input_calls_sha256']=hashlib.sha256((source/'calls.jsonl').read_bytes()).hexdigest()
 for name,value in [('evaluations.json',rows),('summary.json',summary)]: (out/name).write_text(json.dumps(value,indent=2)+'\n')
 (out/'calls.jsonl').write_bytes((source/'calls.jsonl').read_bytes())
 print(summary['call_counts'])
if __name__=='__main__':main()
