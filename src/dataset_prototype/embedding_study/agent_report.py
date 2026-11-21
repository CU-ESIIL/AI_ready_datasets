"""Regenerate pilot tables and paired task summaries without provider invocation."""
from collections import Counter
import gzip
import json
from pathlib import Path
import statistics
import numpy as np

METRICS=('scientific_correct','appropriate_abstention','appropriate_abstention_when_insufficient','operation_selection_correct','first_operation_selection_correct','executed_operation_selection_errors','representation_selection_correct',
    'selected_representation_sufficient','invalid_tool_calls','tool_calls','model_latency_ns','tool_latency_ns',
    'total_elapsed_ns','input_tokens','output_tokens','reasoning_tokens','cached_tokens','provider_cost')


def aggregate(rows):
    groups={}
    for row in rows:
        key=f"{row['condition']}:{row['metadata']}"
        groups.setdefault(key,[]).append(row)
    result={}
    for key,values in sorted(groups.items()):
        rates={}
        for metric in METRICS:
            known=[r[metric] for r in values if r.get(metric) is not None]
            rates[metric]={'known':len(known),'mean':float(statistics.mean(known)) if known else None,
                'sum':float(sum(known)) if known else None}
        result[key]={'episodes':len(values),'status_counts':dict(Counter(r['status'] for r in values)),
            'metrics':rates,'unsupported_answer_attempts':sum(r['unsupported_answer_attempts'] for r in values),
            'provenance_complete_answers':sum(r['provenance_complete'] for r in values)}
    return result


def paired_metadata(rows):
    output=[]
    for condition in sorted({r['condition'] for r in rows}):
        per={}
        for r in rows:
            if r['condition']==condition:
                per.setdefault((r['task_id'],r['metadata']),[]).append(r)
        for m in ('M1','M2'):
            for metric in METRICS:
                pairs=[]
                for task in sorted({t for t,_ in per}):
                    a=[r[metric] for r in per.get((task,'M0'),[]) if r.get(metric) is not None]
                    b=[r[metric] for r in per.get((task,m),[]) if r.get(metric) is not None]
                    if a and b:pairs.append(float(statistics.mean(b)-statistics.mean(a)))
                # Repeats first collapsed within task. Synthetic convenience cases
                # do not justify population-level confidence intervals or p-values.
                output.append({'condition':condition,'contrast':m+'-M0','metric':metric,'paired_tasks':len(pairs),
                    'mean_task_delta':float(statistics.mean(pairs)) if pairs else None,
                    'min_task_delta':min(pairs) if pairs else None,'max_task_delta':max(pairs) if pairs else None,
                    'confidence_interval':None,'inference_scope':'descriptive paired synthetic-task pilot; no population inference'})
    return output


def build_report(directory):
    directory=Path(directory)
    with gzip.open(directory/'episodes.jsonl.gz','rt') as f:rows=[json.loads(line) for line in f]
    with gzip.open(directory/'baselines.jsonl.gz','rt') as f:baseline=[json.loads(line) for line in f]
    simulated=all(r.get('simulated',False) for r in rows)
    evidence_label='mock wiring only; no LLM evidence' if simulated else 'limited real-model smoke; not a confirmatory population test'
    summary={'simulated':simulated,'agents':aggregate(rows),'deterministic_baselines':aggregate(baseline),
        'metadata_contrasts':paired_metadata(rows),'hypotheses':{k:evidence_label for k in ('H1','H2','H3','H4')},
        'claims':'Synthetic protocol simulator and rule-based results are not LLM capability or metadata efficacy evidence.'}
    (directory/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    text=['# Fire VASE controlled-agent milestone 2','',('Complete mock-provider protocol matrix; **no real-model evidence**.' if simulated else 'Limited real-model smoke only; inspect exact run identities and failures. No full real-model matrix or confirmatory evidence is claimed.'),
        '', ('The deterministic simulator ignores metadata and selects operations using public question phrases. Its scores test dispatch and grading, not language-model reasoning. ' if simulated else '')+'Fixed and adaptive access are separate regimes. Questions are public synthetic development diagnostics, not a hidden generalization benchmark.',
        '', '## Scientific correctness and abstention','',
        '| Condition | Metadata | Episodes | Correct answers | Correct abstentions | Incorrect | Failures |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for key,g in summary['agents'].items():
        condition,m=key.split(':');c=g['status_counts']
        text.append(f"| {condition} | {m} | {g['episodes']} | {c.get('correct',0)} | {c.get('correct_abstention',0)} | {c.get('incorrect',0)+c.get('incorrect_abstention',0)} | {c.get('execution_failure',0)} |")
    text+=['','## Selection errors and computational accounting','',
        '| Condition | Metadata | Wrong first operation selections | Insufficient selected view | Tool calls | Invalid calls | Input/output tokens |',
        '| --- | --- | --- | --- | --- | --- | --- |']
    for key,g in summary['agents'].items():
        selected=[r for r in rows if r['condition']+':'+r['metadata']==key]
        wrong=sum(r['first_operation_selection_correct'] is False for r in selected)
        insufficient=sum(r['selected_representation_sufficient'] is False for r in selected)
        token_label='not applicable (mock)' if simulated else 'unavailable unless recorded in structured results'
        text.append(f"| {key.split(':')[0]} | {key.split(':')[1]} | {wrong} | {insufficient} | {int(g['metrics']['tool_calls']['sum'])} | {int(g['metrics']['invalid_tool_calls']['sum'])} | {token_label} |")
    text+=['','## Abstention and avoidable representation errors','',
        '| Condition | Metadata | Appropriate abstention | Incorrect abstention | Avoidable adaptive view errors |',
        '| --- | --- | --- | --- | --- |']
    for key,g in summary['agents'].items():
        selected=[r for r in rows if r['condition']+':'+r['metadata']==key]
        text.append(f"| {key.split(':')[0]} | {key.split(':')[1]} | {g['status_counts'].get('correct_abstention',0)} | {g['status_counts'].get('incorrect_abstention',0)} | {sum(r['avoidable_representation_error'] for r in selected)} |")
    text+=['','Insufficient assigned fixed views are not agent representation-selection errors. Adaptive errors require an authorized sufficient alternative. Source-wide unavailable evidence is not repairable by choosing another view.',
        '', '## Measured orchestration costs','',
        '| Condition | Metadata | Provider latency mean (ms) | Tool mean (ms) | Episode mean (ms) | Reported cost |',
        '| --- | --- | --- | --- | --- | --- |']
    for key,g in summary['agents'].items():
        metrics=g['metrics']
        provider_ms=metrics['model_latency_ns']['mean']/1e6
        tool_ms=metrics['tool_latency_ns']['mean']/1e6
        episode_ms=metrics['total_elapsed_ns']['mean']/1e6
        cost=metrics['provider_cost']['sum']
        text.append(f"| {key.split(':')[0]} | {key.split(':')[1]} | {provider_ms:.3f} | {tool_ms:.3f} | {episode_ms:.3f} | {'unavailable / not applicable' if cost is None else str(cost)} |")
    text+=['','For simulated providers, provider latency is local policy CPU time, not LLM inference. Missing usage and cost remain null. Source preparation, artifact reuse and rule construction/maintenance are separate in preparation_accounting.json.',
        '', '## Deterministic fixed and contract-routing baselines','',
        '| Baseline | Metadata | Correct | Correct abstention | Other |','| --- | --- | --- | --- | --- |']
    for key,g in summary['deterministic_baselines'].items():
        c=g['status_counts'];text.append(f"| {key.split(':')[0]} | {key.split(':')[1]} | {c.get('correct',0)} | {c.get('correct_abstention',0)} | {g['episodes']-c.get('correct',0)-c.get('correct_abstention',0)} |")
    text+=['','## Failure cases and diagnostics','']
    failures=[r for r in rows if r['status'] not in {'correct','correct_abstention'}]
    text+=['| Case | Condition | Status | Independent diagnostic |','| --- | --- | --- | --- |']
    seen=set()
    for row in failures:
        key=(row['task_id'],row['condition'],row['status'])
        if key in seen:continue
        seen.add(key);text.append(f"| `{row['task_id']}` | {row['condition']} | {row['status']} | {', '.join(row['diagnostic_events'])} |")
        if len(seen)>=6:break
    if not failures:text.append('No failed mock episodes; this does not establish scientific model competence.')
    text+=['', 'Behavioral diagnostics separately identify temporal gaps/zero observations, normalized-size limitations, approximate geometry and evidence support. They use independent keys, never a model grading itself.',
        '', 'Paired M1−M0 and M2−M0 contrasts are retained in summary.json after averaging repetitions within each task. No confidence interval or significance claim is made for this selected synthetic task set. Runtime variation in a deterministic simulator is not a metadata mechanism.',
        '', '## Reproduction and limits','',
        'Regenerate this report with `python -m dataset_prototype.embedding_study.agent_runner --report RUN_DIRECTORY`; this makes no model calls.',
        'Exact prompts, schemas, proposal outputs, sanitized tool responses, rejected actions, private evaluation traces and usage availability are retained in compressed JSONL. Preparation is separately recorded. Application query caches start cold for each episode; no second cache factorial is added.',
        'The explicit router is handcrafted from scientific operation requirements and a small public-question parser, not task IDs or reference answers. Construction/maintenance labor is unmeasured, not free. The mock adaptive policy uses the first offered interface; it is not learned routing.',
        'Provider usage/cost fields absent from a transport stay null. Mock calls have no language-model token consumption measurement; live billing is not inferred. Parent orchestration/tool time and shared upstream preparation are separate from inference latency.',
        'Real-model access, genuinely held-out events/templates and operational/general ecological conclusions remain pending. No scientific authority, real-data approval, neural embedding or unrestricted code execution is added.','']
    (directory/'report.md').write_text('\n'.join(text))
    return summary
