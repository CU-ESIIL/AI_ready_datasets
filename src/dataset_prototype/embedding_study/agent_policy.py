"""Strong explicit contract router; general question phrases, never task IDs or gold."""
from .agent_contracts import AgentAction, QueryArguments


def identify_operation(question):
    q=question.lower()
    # Scientific goal parsing uses only the public request, not hidden classifications.
    if 'independently validated scientific analog' in q: return 'scientific_analog'
    if 'two neighbors' in q: return 'nearest_profile'
    if 'pca geometry' in q: return 'pca_distance'
    if 'euclidean' in q and 'distance' in q: return 'profile_distance'
    if 'first half' in q and 'fraction' in q: return 'front_fraction'
    if 'construct' in q and 'profile' in q or 'normalize' in q and 'history' in q: return 'profile'
    if 'pulse count' in q: return 'pulses'
    if 'number of evidenced consecutive' in q: return 'sequence_days'
    if 'date of first maximum' in q: return 'peak_date'
    if 'largest' in q and ('increment' in q or 'growth' in q): return 'maximum_daily_growth'
    if 'cumulative area' in q: return 'cumulative'
    if 'daily growth' in q: return 'daily_growth'
    if 'growth from' in q or 'interval growth' in q: return 'interval_growth'
    return None


# Scientific requirements, not per-item answerability. No data-dependent oracle.
PREFERENCE={
 'profile':('R1','R0','R2'),'front_fraction':('R1','R0','R2'),
 'profile_distance':('R1','R0','R2'),'nearest_profile':('R1','R0','R2'),
 'pca_distance':('R2','R1','R0'),'sequence_days':('R1','R0','R2')}


def proposed_call(initial, *, rule_router=True):
    op=identify_operation(initial['question'])
    if op is None:
        return AgentAction(action='abstain',reason='Public question did not match an offered scientific operation.')
    allowed=initial['allowed_representations']
    preference=PREFERENCE.get(op,('R0','R1','R2')) if rule_router else ('R0','R1','R2')
    if rule_router:
        shape_ops={'profile','front_fraction','profile_distance','pca_distance','nearest_profile'}
        support={'R0':set(initial['operations']),
            'R1':shape_ops|{'sequence_days'},'R2':{'pca_distance','nearest_profile','sequence_days'}}
        viable=[r for r in preference if r in allowed and op in support[r]]
        if op=='scientific_analog' or not viable:
            return AgentAction(action='abstain',reason='General operation contract lacks the required evidence or preserved quantities.')
        if op in shape_ops:
            view=initial['data'][allowed[0]]
            relevant=[*initial['context']['fire_ids'],*initial['context']['candidate_fire_ids']]
            if any(not view['provenance_sidecars'][i]['primary_profile_eligible'] for i in relevant):
                return AgentAction(action='abstain',reason='Completed-profile preconditions fail in the supplied source evidence.')
        r=viable[0]
    else:
        r=next(r for r in preference if r in allowed)
    context=initial['context']
    return AgentAction(action='call',representation=r,operation=op,arguments=QueryArguments(
        fire_ids=tuple(context['fire_ids']),date=context['requested_date'] if op in {'cumulative','daily_growth','interval_growth'} else None,
        start_date=context['interval_start_date'] if op=='interval_growth' else None,
        candidates=tuple(context['candidate_fire_ids']) if op=='nearest_profile' else (),
        approximation_allowed=op=='nearest_profile'))


def finish_action(history):
    results=[e['response'] for e in history if e.get('kind')=='tool']
    if not results:
        return None
    last=results[-1]
    if last['status']=='value':
        return AgentAction(action='answer',result_id=last['result_id'],evidence_ids=tuple(last['evidence_ids']))
    if last['status']=='no_result':
        return AgentAction(action='abstain',reason='The permitted operation produced no supported result.')
    return None
