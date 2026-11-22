"""Budgeted proposal loop over synthetic deterministic operations; no model execution."""
from datetime import datetime, timezone
import json
import math
import numbers
from time import perf_counter_ns
from ..contracts import digest
from .agent_contracts import AgentAction, QueryArguments, ScientificQuery
from .agent_render import SYSTEM, serialize_prompt
from .contracts import OPERATIONS


def equivalent(a,b):
    """Exact value copying, not new computation or tolerance-based correction."""
    if isinstance(a,bool) or isinstance(b,bool): return type(a)==type(b) and a==b
    if isinstance(a,numbers.Real) and isinstance(b,numbers.Real):
        return math.isfinite(a) and math.isfinite(b) and a==b
    if isinstance(a,list) and isinstance(b,list): return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    if isinstance(a,dict) and isinstance(b,dict): return set(a)==set(b) and all(equivalent(a[k],b[k]) for k in a)
    return type(a)==type(b) and a==b


def run_episode(provider,initial,config,dispatcher,*,invoke=None,protocol=None):
    # A versioned development-time contract, never supplied by runtime models.
    Action, Arguments, Query, operation_ids, render = (protocol if protocol is not None else
        (AgentAction, QueryArguments, ScientificQuery, OPERATIONS, serialize_prompt))
    start=perf_counter_ns();history=[];steps=[];final=None
    counts={'tool_calls':0,'invalid_tool_calls':0,'rejections':0,'recovery_attempts':0,
        'unsupported_answer_attempts':0,'model_calls':0,'inspect_calls':0,
        'invalid_arguments':0,'unknown_operation_attempts':0,'unauthorized_representation_attempts':0,'unoffered_identifier_attempts':0}
    usage=[];pending_rejection=False;termination='step_limit'
    params={'temperature':config.temperature,'max_output_tokens':config.max_output_tokens,
        'timeout_seconds':config.provider_timeout_seconds,'seed':None}
    for step in range(config.max_steps):
        if (perf_counter_ns()-start)/1e9 >= config.max_episode_seconds:
            termination='time_limit';break
        known_tokens=sum((u['input_tokens'] or 0)+(u['output_tokens'] or 0) for u in usage)
        if known_tokens >= config.max_episode_tokens:
            termination='reported_token_limit';break
        prompt=render(initial,history)
        if len(prompt.encode())>config.max_prompt_bytes:
            termination='prompt_byte_limit';break
        record={'step':step,'timestamp':datetime.now(timezone.utc).isoformat(),
            'prompt':prompt,'prompt_hash':digest(prompt),'schema_hash':digest(Action.model_json_schema()),
            'tool_descriptions_hash':digest(initial['operations']),'sampling_parameters':params}
        try:
            reply=(invoke or provider.invoke)(prompt,parameters=params)
        except Exception as exc:
            record.update(provider_error_type=type(exc).__name__,raw_response=None)
            steps.append(record);termination='provider_failure';break
        counts['model_calls']+=1
        usage.append(reply.usage.model_dump(mode='json'))
        record.update(raw_response=reply.content,response_scope=reply.response_scope,
            provider=reply.provider,model=reply.model,model_snapshot=reply.model_snapshot,
            model_latency_ns=reply.latency_ns,usage=usage[-1],transport=reply.transport,
            response_hash=digest(reply.content),provider_error=reply.error)
        if reply.error:
            steps.append(record);termination='provider_failure';break
        if (perf_counter_ns()-start)/1e9 >= config.max_episode_seconds:
            steps.append(record);termination='time_limit';break
        history.append({'kind':'proposal','content':reply.content})
        request=None;parsed=None;response=None;tool_start=perf_counter_ns()
        try:
            if pending_rejection:
                counts['recovery_attempts']+=1;pending_rejection=False
            parsed=json.loads(reply.content)
            request=Action.model_validate(parsed)
            if request.action=='select':
                dispatcher.authorize(request.representation);dispatcher.selected=request.representation
                response={'status':'selected','representation':request.representation}
            elif request.action in {'call','inspect'}:
                counts['tool_calls']+=1
                if counts['tool_calls']>config.max_tool_calls:
                    termination='tool_call_limit';response={'status':'rejected','code':'budget_limit'}
                    record['response']=response;steps.append(record);break
                if request.action=='inspect':
                    counts['inspect_calls']+=1
                    response={'status':'data','data':dispatcher.inspect(request.representation)}
                else:
                    response=dispatcher.call(request.representation,request.operation,request.arguments)
                    dispatcher.selected=request.representation
            elif request.action=='answer':
                found=dispatcher.results.get(request.result_id)
                if (found is None or found['public_result']['status']!='value'
                    or set(request.evidence_ids)!=set(found['public_result']['evidence_ids'])
                    or not request.evidence_ids
                    or (request.value is not None and not equivalent(request.value,found['public_result']['value']))):
                    counts['unsupported_answer_attempts']+=1
                    raise PermissionError('unsupported_answer')
                final={'kind':'answer','supporting_result':request.result_id,
                    'answer':found['result']['answer'],'interpretation':request.interpretation,
                    'evidence_ids':list(request.evidence_ids)}
                termination='completed';response={'status':'final_answer_accepted'}
            elif request.action=='abstain':
                final={'kind':'abstain','reason':request.reason,'interpretation':request.interpretation}
                termination='completed';response={'status':'abstention_accepted'}
        except Exception as exc:
            from pydantic import ValidationError
            from .representations import InvalidOperation
            if not isinstance(exc,(ValueError,ValidationError,PermissionError,InvalidOperation)):
                record.update(tool_latency_ns=perf_counter_ns()-tool_start,execution_error_type=type(exc).__name__,response={'status':'rejected','code':'execution_failed'})
                steps.append(record);termination='execution_failure';break
            counts['rejections']+=1;pending_rejection=True
            # No underlying scientific reason, validator text, file paths or hidden
            # answerability feedback crosses this condition-invariant boundary.
            raw_is_call=isinstance(locals().get('parsed'),dict) and parsed.get('action') in {'call','inspect'}
            if request is not None and request.action in {'call','inspect'}:
                counts['invalid_tool_calls']+=1
            elif raw_is_call:
                counts['tool_calls']+=1;counts['invalid_tool_calls']+=1
            if request is None and isinstance(locals().get('parsed'),dict) and parsed.get('action')=='answer':
                counts['unsupported_answer_attempts']+=1
            category='invalid_action'
            if isinstance(parsed,dict) and parsed.get('action') in {'call','inspect','select'}:
                if parsed.get('action')=='call' and parsed.get('operation') not in operation_ids:
                    category='unknown_operation_attempts'
                elif parsed.get('representation') not in dispatcher.allowed:
                    category='unauthorized_representation_attempts'
                elif isinstance(exc,PermissionError):category='unoffered_identifier_attempts'
                elif parsed.get('action')=='call':
                    try:
                        args=Arguments.model_validate(parsed.get('arguments'))
                        Query(operation=parsed['operation'],**args.model_dump())
                    except ValueError:category='invalid_arguments'
            if category in counts:counts[category]+=1
            record['private_rejection_category']=category
            code='unauthorized_request' if isinstance(exc,PermissionError) else 'invalid_action'
            response={'status':'rejected','code':code}
            record['rejection_type']=type(exc).__name__
        record['tool_latency_ns']=perf_counter_ns()-tool_start
        record['response']=response
        if request is not None:record['validated_action']=request.model_dump(mode='json')
        steps.append(record)
        history.append({'kind':'tool' if request is not None and request.action in {'call','inspect'} else 'control','response':response})
        if final is not None:break
        if counts['tool_calls']>=config.max_tool_calls and pending_rejection:
            termination='tool_call_limit';break
    usage_total={}
    for name in ('input_tokens','output_tokens','reasoning_tokens','cached_tokens','provider_cost'):
        values=[u[name] for u in usage]
        usage_total[name]=sum(values) if values and all(v is not None for v in values) else None
    usage_total['cost_currency']=next((u['cost_currency'] for u in usage if u['cost_currency']),None)
    return {'final':final,'termination':termination,'steps':steps,'counts':counts,'usage':usage_total,
        'usage_complete':bool(usage) and all(u['input_tokens'] is not None and u['output_tokens'] is not None for u in usage),
        'total_elapsed_ns':perf_counter_ns()-start,'model_latency_ns':sum(s.get('model_latency_ns',0) for s in steps),
        'tool_latency_ns':sum(s.get('tool_latency_ns',0) for s in steps),
        'token_budget_scope':'reported usage only; unknown usage is never treated as zero consumption; step/output/byte caps also apply',
        'scientific_authority':'deterministic synthetic controller only; no real-data human approval'}
