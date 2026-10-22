"""Explicit live, tool-free OpenClaw/Verde pilot; every response remains inert."""
import argparse,json,time
from pathlib import Path
from datetime import datetime,timezone
from dataset_prototype.openclaw_backend import OpenClawBackend
from dataset_prototype.decision_experiment import InertProse,decision_schema,evaluate_response,summarize
from dataset_prototype.contracts import digest
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--repeats',type=int,default=2);p.add_argument('--limit',type=int,default=25);a=p.parse_args()
 if not 1<=a.repeats<=3 or not 1<=a.limit<=25:raise ValueError('bounded pilot required')
 a.output.mkdir(parents=True,exist_ok=False);backend=OpenClawBackend();backend.timeout=150
 tasks=json.loads((ROOT/'data/fixtures/validation/decision_tasks.json').read_text())[:a.limit];rows=[];calls=[]
 for repeat in range(a.repeats):
  for task in tasks:
   # Draft oracle is excluded from model input. C/D never generate additional responses.
   public={k:v for k,v in task.items() if not k.startswith('draft_') and k not in {'oracle_status','expert_review'}}
   for arm in ['A','B']:
    schema=InertProse if arm=='A' else decision_schema(task)
    instruction=('Respond with natural-language scientific advice in the text field. Content is captured inertly and never executed; do not produce code, formulas, new coefficients, identifiers or approvals.' if arm=='A' else 'Return a bounded scientific decision. Use the supplied task_digest, offered IDs and evidence IDs. Select only when evidence warrants it; otherwise abstain or request human review. Never calculate or write code. task_digest='+digest(task))
    started_at=datetime.now(timezone.utc).isoformat();start=time.monotonic();output=None;error=None
    try:output=backend.generate('harmonization',instruction,public,schema)
    except Exception as e:error=type(e).__name__
    trace=backend.traces[-1].model_dump(mode='json') if backend.traces else None
    call={'task_id':task['task_id'],'repeat':repeat,'arm':arm,'started_at':started_at,'elapsed_seconds':time.monotonic()-start,'status':'returned' if output is not None else 'failed','error':error,'trace':trace,'schema':schema.model_json_schema(),'model_input':public,'instruction':instruction,'response':output.model_dump(mode='json') if output else None,'execution_authorized':False}
    calls.append(call)
    with (a.output/'calls.jsonl').open('a') as f:f.write(json.dumps(call)+'\n')
    raw=output.model_dump(mode='json') if output else (trace.get('output_json','') if trace else '')
    for label in [arm] if arm=='A' else ['B','C','D']:
     row=evaluate_response(raw,task,label);row.update(repeat=repeat,model=backend.model,provider=backend.provider,call_status=call['status'],elapsed_seconds=call['elapsed_seconds']);rows.append(row)
    (a.output/'evaluations.json').write_text(json.dumps(rows,indent=2)+'\n');(a.output/'summary.json').write_text(json.dumps(summarize(rows),indent=2)+'\n')
    print(f"{repeat+1}/{a.repeats} {task['task_id']} {arm}: {call['status']}",flush=True)
    if len(calls)>=4 and all(c['status']=='failed' for c in calls[-4:]):
     (a.output/'blocked.json').write_text(json.dumps({'reason':'four consecutive unavailable/invalid service responses; no mocks','completed_calls':len(calls),'execution_authorized':False},indent=2));return
 (a.output/'protocol.json').write_text(json.dumps({'arms':'A natural-language content in JSON envelope required by installed plugin; B constrained choices; C scientific validation of B; D same plus unfulfilled human gate','model':backend.model,'provider':backend.provider,'models_compared':1,'repeats':a.repeats,'human_gold':'not yet authored; draft oracle agreement only','cost_tokens':'not exposed by plugin','scope':'one provider model; no claim about weaker models or general model effects'},indent=2)+'\n')
if __name__=='__main__':main()
