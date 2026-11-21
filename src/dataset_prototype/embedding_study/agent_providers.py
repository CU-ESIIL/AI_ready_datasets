"""Independent mock and optional verified OpenClaw transport; no implicit fallback."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import uuid
from pathlib import Path
from time import perf_counter_ns
from typing import Protocol
from ..contracts import digest
from .agent_contracts import AgentAction, Usage
from .agent_policy import proposed_call, finish_action


@dataclass(frozen=True)
class ProviderReply:
    content: str
    provider: str
    model: str
    response_scope: str
    latency_ns: int
    usage: Usage = field(default_factory=Usage)
    model_snapshot: str | None = None
    transport: dict | None = None
    error: str | None = None


class Provider(Protocol):
    name: str
    model: str
    simulated: bool
    def invoke(self, prompt: str, *, parameters: dict) -> ProviderReply: ...


class MockProvider:
    """Protocol simulator: public-goal phrase parser plus first allowed interface.

    Metadata is deliberately ignored. This is not an LLM or evidence for H1-H4.
    """
    name='deterministic-mock'
    model='deterministic-contract-mock-v1'
    simulated=True

    def invoke(self,prompt,*,parameters):
        start=perf_counter_ns(); envelope=json.loads(prompt)
        action=finish_action(envelope['history'])
        if action is None:
            action=proposed_call(envelope['initial'],rule_router=False)
        return ProviderReply(action.model_dump_json(),self.name,self.model,'mock_json',perf_counter_ns()-start)


class RuleProvider(MockProvider):
    name='deterministic-operation-contract-router'
    model='reviewed-question-parser-contract-router-v1'
    def invoke(self,prompt,*,parameters):
        start=perf_counter_ns(); envelope=json.loads(prompt)
        action=finish_action(envelope['history']) or proposed_call(envelope['initial'],rule_router=True)
        return ProviderReply(action.model_dump_json(),self.name,self.model,'deterministic_rule_json',perf_counter_ns()-start)


class ScriptedProvider:
    """Explicit test double for rejection/recovery and malformed outputs only."""
    name='scripted-offline-test';model='script-v1';simulated=True
    def __init__(self,outputs,usage=None):
        self.outputs=iter(outputs);self.usage=usage or Usage()
    def invoke(self,prompt,*,parameters):
        value=next(self.outputs)
        return ProviderReply(value if isinstance(value,str) else json.dumps(value),self.name,self.model,
            'scripted_test_json',0,self.usage)


class OpenClawProvider:
    name='openclaw-llm-task';simulated=False
    def __init__(self,runtime='run/openclaw',*,authorized=False,backend=None):
        if not authorized:
            raise ValueError('live access requires explicit verified cost/access authorization; no automatic model calls')
        from ..openclaw_backend import OpenClawBackend
        self.backend=backend or OpenClawBackend(Path(runtime))
        self.model=self.backend.model
        self.snapshot=self.backend.runtime.get('provider_model_digest')

    def invoke(self,prompt,*,parameters):
        # Reuse verified installed llm-task schema/route, not the old role prompt.
        start=perf_counter_ns();b=self.backend
        args={'prompt':json.loads(prompt)['system'],'input':json.loads(prompt),
            'schema':{'type':'object'},'provider':b.provider,'model':f'{b.provider}/{b.model}',
            'temperature':parameters['temperature'],'maxTokens':parameters['max_output_tokens'],
            'timeoutMs':parameters['timeout_seconds']*1000}
        payload={'tool':'llm-task','sessionKey':'agent:prototype-harmonization:fire-utility-'+uuid.uuid4().hex, 'args':args}
        # llm-task is task inference; it does not supply native model tools or files.
        raw=None;failure=None;content=''
        try:
            if len(json.dumps(payload).encode())>48000:raise ValueError('request exceeds verified plugin byte bound')
            raw=b.http(b.endpoint+'/tools/invoke',payload=payload,
                headers={'Authorization':'Bearer '+b._token},timeout=parameters['timeout_seconds']+5,max_bytes=2_000_000)
            result=raw.get('result',{});details=result.get('details',{})
            if raw.get('ok') is not True or result.get('isError'):raise ValueError('gateway_task_failed')
            if details.get('provider')!=b.provider or details.get('model')!=b.model:raise ValueError('provider_model_substitution')
            if 'json' not in details:raise ValueError('plugin_validated_json_missing')
            content=json.dumps(details['json'],sort_keys=True,allow_nan=False)
        except Exception as error:
            # Transport errors are recorded without credential-bearing HTTP/config text.
            failure=type(error).__name__
        # This installed plugin exposes normalized JSON, not raw text or usage.
        return ProviderReply(content,self.name,self.model,'gateway_validated_json',perf_counter_ns()-start,
            model_snapshot=self.snapshot,error=failure,
            transport={'payload':payload,'config_digest':b.runtime['config_digest'],
                'openclaw_version':b.runtime['openclaw_version'],
                'transport_schema_scope':'JSON object only; full action schema stays in prompt and is enforced by deterministic controller',
                'expected_provider':b.provider,'expected_model':b.model,
                'returned_provider':raw.get('result',{}).get('details',{}).get('provider') if raw else None,
                'returned_model':raw.get('result',{}).get('details',{}).get('model') if raw else None,
                'identity_verified':failure is None,'gateway_response_hash':digest(raw),
                'gateway_response':redact_transport(raw,[b._token]),
                'normalized_output':content,'error_type':failure})


def redact_transport(value,secrets):
    """Security redaction is explicit; hashes preserve original response identity."""
    if isinstance(value,dict):
        return {k:('[REDACTED]' if k.lower().replace('_','') in {'authorization','apikey','credential','secret','password'}
            else redact_transport(v,secrets)) for k,v in value.items()}
    if isinstance(value,list):return [redact_transport(v,secrets) for v in value]
    if isinstance(value,str):
        for secret in secrets:
            if secret:value=value.replace(secret,'[REDACTED]')
    return value
