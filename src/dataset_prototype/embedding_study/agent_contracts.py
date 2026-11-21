"""JSON-only proposals and explicit budgets for synthetic agent experiments."""
from datetime import date as CalendarDate
from typing import Literal, Any
from pydantic import Field, model_validator, field_validator
from ..contracts import Contract
from .contracts import OPERATIONS

Representation = Literal['R0','R1','R2']
Operation = Literal['cumulative','interval_growth','daily_growth','maximum_daily_growth',
    'peak_date','sequence_days','pulses','profile','front_fraction','profile_distance',
    'pca_distance','nearest_profile','scientific_analog']


class QueryArguments(Contract):
    fire_ids: tuple[str,...] = Field(min_length=1,max_length=2)
    date: CalendarDate | None = None
    start_date: CalendarDate | None = None
    candidates: tuple[str,...] = Field(default=(),max_length=64)
    approximation_allowed: bool = Field(default=False,strict=True)


class ScientificQuery(QueryArguments):
    operation: Operation

    @property
    def unit(self):
        from .metadata import OP_UNITS
        return OP_UNITS[self.operation]

    @model_validator(mode='after')
    def parameters(self):
        op=self.operation
        if self.date is not None and op not in {'cumulative','daily_growth','interval_growth'}:
            raise ValueError('date argument not allowed')
        if self.start_date is not None and op!='interval_growth':
            raise ValueError('start argument not allowed')
        if op in {'cumulative','daily_growth','interval_growth'} and self.date is None:
            raise ValueError('date required')
        if op=='interval_growth' and (self.start_date is None or self.start_date>=self.date):
            raise ValueError('ordered interval endpoints required')
        if len(self.fire_ids)!=(2 if op in {'profile_distance','pca_distance'} else 1):
            raise ValueError('incorrect primary identifier count')
        if op=='nearest_profile':
            if len(set(self.candidates))<2 or len(set(self.candidates))!=len(self.candidates) or self.fire_ids[0] in self.candidates or not self.approximation_allowed:
                raise ValueError('declared approximate candidates required')
        elif self.candidates or self.approximation_allowed:
            raise ValueError('candidate arguments belong to nearest_profile only')
        return self


class AgentAction(Contract):
    version: Literal['fire-agent-action-v1']='fire-agent-action-v1'
    action: Literal['select','inspect','call','answer','abstain']
    representation: Representation | None = None
    operation: Operation | None = None
    arguments: QueryArguments | None = None
    result_id: str | None = Field(default=None,max_length=64)
    evidence_ids: tuple[str,...] = Field(default=(),max_length=64)
    value: Any = None
    reason: str = Field(default='',max_length=1200)
    interpretation: Literal['exact','approximate','insufficient','unknown'] = 'unknown'

    @field_validator('value')
    @classmethod
    def finite_value(cls,value):
        import math
        def check(v):
            if isinstance(v,float) and not math.isfinite(v):raise ValueError('nonfinite result claim')
            if isinstance(v,list):
                for item in v:check(item)
            if isinstance(v,dict):
                for item in v.values():check(item)
        check(value)
        return value

    @model_validator(mode='after')
    def shape(self):
        if self.action in {'select','inspect'} and self.representation is None:
            raise ValueError('representation required')
        if self.action in {'select','inspect','abstain'} and (self.operation is not None or self.arguments is not None or self.result_id is not None or self.evidence_ids or self.value is not None):
            raise ValueError('inactive fields must be absent')
        if self.action=='abstain' and self.representation is not None:
            raise ValueError('abstention cannot select representation')
        if self.action=='answer' and (self.representation is not None or self.operation is not None or self.arguments is not None):
            raise ValueError('answer selects returned evidence, not new execution')
        if self.action=='call':
            if self.representation is None or self.operation is None or self.arguments is None:
                raise ValueError('call requires representation, registered operation and arguments')
            if self.result_id is not None or self.evidence_ids or self.value is not None:
                raise ValueError('calls cannot supply scientific results')
            ScientificQuery(operation=self.operation,**self.arguments.model_dump())
        elif self.action in {'select','inspect'}:
            if self.representation is None:
                raise ValueError('representation required')
        if self.action not in {'call'} and (self.operation is not None or self.arguments is not None):
            raise ValueError('operation parameters only allowed on call')
        if self.action!='answer' and (self.result_id is not None or self.evidence_ids or self.value is not None):
            raise ValueError('answer evidence only allowed on answer')
        if self.action=='abstain' and not self.reason.strip():
            raise ValueError('abstention requires a reason')
        return self


class Usage(Contract):
    input_tokens: int | None = Field(default=None,ge=0)
    output_tokens: int | None = Field(default=None,ge=0)
    reasoning_tokens: int | None = Field(default=None,ge=0)
    cached_tokens: int | None = Field(default=None,ge=0)
    provider_cost: float | None = Field(default=None,ge=0)
    cost_currency: str | None = None


class AgentConfig(Contract):
    version: Literal['fire-agent-experiment-v1']
    prompt_version: Literal['fire-agent-prompt-v1','fire-agent-prompt-v2']
    phase: Literal['development','frozen_pilot','held_out_pending']
    fixture: str
    tasks: str
    snapshot: str
    metadata: str
    provider: Literal['mock','openclaw']
    model: str
    repetitions: int = Field(ge=1,le=10)
    metadata_conditions: tuple[Literal['M0','M1','M2'],...]
    fixed_representations: tuple[Representation,...]
    adaptive: bool
    cache_policy: Literal['cold_application_per_episode']
    max_steps: int = Field(ge=2,le=12)
    max_tool_calls: int = Field(ge=1,le=8)
    max_episode_seconds: float = Field(gt=0,le=900)
    max_provider_calls: int = Field(ge=1,le=20000)
    max_episode_tokens: int = Field(ge=1,le=100000)
    max_prompt_bytes: int = Field(ge=1000,le=48000)
    temperature: float = Field(ge=0,le=2)
    seed: int = Field(ge=0)
    max_output_tokens: int = Field(default=2048,ge=128,le=4096)
    provider_timeout_seconds: int = Field(default=60,ge=1,le=120)
    live_access_authorized: bool = False
    live_cost_basis: Literal['unverified','operator_confirmed_no_external_charge'] = 'unverified'
    max_real_calls: int = Field(ge=0,le=6)
    approved_external_cost_cap: float | None = Field(ge=0)
    smoke_task_indexes: tuple[int,...] = ()

    @model_validator(mode='after')
    def unique(self):
        if len(set(self.metadata_conditions))!=len(self.metadata_conditions) or len(set(self.fixed_representations))!=len(self.fixed_representations):
            raise ValueError('duplicate experimental conditions')
        if self.provider=='mock' and self.model!='deterministic-contract-mock-v1':
            raise ValueError('mock identity must be explicit')
        if self.provider=='openclaw' and (self.max_real_calls==0 or self.approved_external_cost_cap is None):
            raise ValueError('live smoke requires explicit call and cost approval bounds')
        return self
