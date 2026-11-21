"""Independent outcome/selection diagnostics, never model self-grading."""
import json
from .evaluation import evaluate


def arguments_match(query,task):
    pair=task.operation in {'profile_distance','pca_distance'}
    same_ids=set(query['fire_ids'])==set(task.fire_ids) if pair else tuple(query['fire_ids'])==task.fire_ids
    return same_ids and query['date']==(task.date.isoformat() if task.date else None) and query['start_date']==(task.start_date.isoformat() if task.start_date else None) and set(query['candidates'])==set(task.candidates) and query['approximation_allowed']==task.approximation_allowed


def temporal_case(task,histories):
    h=histories[task.fire_ids[0]]
    if task.operation=='daily_growth':
        o=next((o for o in h.observations if o.date==task.date),None)
        if o is None or not o.available:return 'missing_observation'
        if o.days_since_previous is None:return 'unknown_baseline'
        if o.days_since_previous>1:return 'multi_day_gap'
        if o.daily_growth==0:return 'observed_zero'
        return 'consecutive_day'
    if task.operation=='interval_growth':return 'interval_total'
    return None


def score_episode(task,allowed,episode,dispatcher,reference,histories):
    final=episode['final'];calls=dispatcher.calls
    proposed=[]
    for step in episode['steps']:
        try:
            action=json.loads(step.get('raw_response') or '{}')
        except (ValueError,TypeError):continue
        if isinstance(action,dict) and action.get('action')=='call':proposed.append(action)
    first_operation_correct=(proposed[0].get('operation')==task.operation) if proposed else None
    sufficient=any(task.answerable[r] for r in allowed)
    support=dispatcher.results.get(final.get('supporting_result')) if final and final['kind']=='answer' else None
    last=support or (calls[-1] if calls else None)
    selected=last['representation'] if last else dispatcher.selected
    op_correct=last['query']['operation']==task.operation if last else None
    args_correct=arguments_match(last['query'],task) if last else None
    provenance_complete=bool(support and final['evidence_ids'] and all(
        all(key in p for key in task.expected_provenance) for p in support['lineage'].values()))
    effective=selected or allowed[0]
    # In adaptive mode, abstention is justified only when no authorized view can
    # answer, not just because the last chosen view failed.
    if final and final['kind']=='abstain':
        effective=next((r for r in allowed if task.answerable[r]),allowed[0])
        scoring=evaluate(task,effective,{'abstention':True},reference)
    elif final and support:
        scoring=evaluate(task,effective,support['result'],reference)
        if not op_correct or not args_correct or not provenance_complete:
            scoring.update(status='incorrect',correctness=False,scientific_validity='FAIL',unsupported_answer=True)
        if support['result']['approximate'] and final['interpretation']=='exact':
            scoring.update(status='incorrect',correctness=False,scientific_validity='FAIL',unsupported_answer=True)
    else:
        scoring={'status':'execution_failure','correctness':None,'scientific_validity':'NEEDS_EVIDENCE',
            'numerical_error':None,'unsupported_answer':episode['counts']['unsupported_answer_attempts']>0}
    temporal=temporal_case(task,histories)
    valid_outcome=scoring['status'] in {'correct','correct_abstention'}
    outcomes=[]
    for call in calls:
        q=call['query']
        if not task.answerable[call['representation']]:outcomes.append('selected_insufficient_representation')
        if q['operation']!=task.operation:outcomes.append('selected_wrong_operation')
        elif not arguments_match(q,task):outcomes.append('arguments_do_not_match_question')
        if call['result']['abstention']:outcomes.append('operation_returned_no_result')
    if episode['counts'].get('invalid_arguments'):outcomes.append('invalid_arguments')
    if episode['counts'].get('unauthorized_representation_attempts'):outcomes.append('unauthorized_representation_attempt')
    if episode['counts'].get('unknown_operation_attempts'):outcomes.append('unknown_operation_attempt')
    if episode['counts']['invalid_tool_calls']:outcomes.append('invalid_tool_action')
    if episode['counts']['unsupported_answer_attempts']:outcomes.append('unsupported_final_claim')
    if final and final['kind']=='abstain':outcomes.append('appropriate_abstention' if not sufficient else 'incorrect_abstention')
    if support and support['result']['approximate'] and final['interpretation']=='exact':outcomes.append('misinterpreted_valid_tool_result')
    if scoring['status']=='correct':outcomes.append('correct_scientific_answer_synthetic_scope')
    approx_recognized=None
    if support and support['result']['approximate'] and final['interpretation']!='unknown':
        approx_recognized=final['interpretation']=='approximate'
    return {**scoring,'authorized_answerable':sufficient,'selected_representation':selected,
        'selected_representation_sufficient':task.answerable[selected] if selected else None,
        'representation_selection_correct':(task.answerable[selected] if selected else False) if len(allowed)>1 and sufficient else None,
        'avoidable_representation_error':bool(len(allowed)>1 and sufficient and selected is not None and not task.answerable[selected]),
        'first_operation_selection_correct':first_operation_correct,
        'executed_operation_selection_errors':sum(c['query']['operation']!=task.operation for c in calls),
        'operation_selection_correct':op_correct,'arguments_match_question':args_correct,
        'provenance_complete':provenance_complete,'returned_answer':final['answer'] if support else None,
        'reference_answer':reference,'diagnostic_events':sorted(set(outcomes)),
        'diagnostics':{'temporal_case':temporal,'temporal_behavior_correct':valid_outcome if temporal else None,
            'normalization_limitation_case':task.operation in {'cumulative','maximum_daily_growth','peak_date'},
            'representation_limitation_behavior_correct':valid_outcome if not sufficient else None,
            'compression_geometry_case':task.operation in {'profile','profile_distance','pca_distance','nearest_profile'},
            'approximation_recognition':approx_recognized,'provenance_supported':provenance_complete,
            'scope':'behavioral checks on independent keys; not access to hidden reasoning or model self-grading'}}
