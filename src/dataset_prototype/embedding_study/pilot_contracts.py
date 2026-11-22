"""Version-three synthetic experiment contracts; separate from historical tasks."""
from datetime import date as CalendarDate
from typing import Literal, Any
import math
from pydantic import Field, model_validator, field_validator
from ..contracts import Contract
from .agent_contracts import AgentAction

Op = Literal['cumulative','daily_growth','interval_growth','growth_compare','front_fraction',
 'late_fraction','profile','profile_distance','pulse_count','pca_distance','projected_distance',
 'reconstruction_error','neighbor_stability','assess_claim','source_evidence']
OPS = tuple(Op.__args__)
CLAIMS = ('absolute_from_normalized','exact_profile_from_pcs','ecological_analog',
 'measurement_uncertainty','forecast_availability','duration_from_sidecar')
UNITS = {op:'1' for op in OPS} | {'cumulative':'km2','daily_growth':'km2/day',
 'interval_growth':'km2','growth_compare':'km2','pulse_count':'count',
 'pca_distance':'standardized_PC_distance','assess_claim':'assessment','source_evidence':'evidence'}

class PilotArguments(Contract):
    fire_ids: tuple[str,...] = Field(min_length=1,max_length=2)
    date: CalendarDate | None = None
    start_date: CalendarDate | None = None
    candidates: tuple[str,...] = Field(default=(),max_length=3)
    claim: Literal['absolute_from_normalized','exact_profile_from_pcs','ecological_analog',
        'measurement_uncertainty','forecast_availability','duration_from_sidecar'] | None = None

class PilotQuery(PilotArguments):
    operation: Op
    @property
    def unit(self):return UNITS[self.operation]
    @model_validator(mode='after')
    def valid(self):
        pair = self.operation in {'growth_compare','profile_distance','pca_distance','projected_distance'}
        if len(self.fire_ids)!=(2 if pair else 1) or len(set(self.fire_ids)) != len(self.fire_ids):raise ValueError('primary source arity')
        dated=self.operation in {'cumulative','daily_growth','interval_growth','growth_compare'}
        interval=self.operation in {'interval_growth','growth_compare'}
        if (self.date is not None)!=dated:raise ValueError('date precondition')
        if (self.start_date is not None)!=interval:raise ValueError('start precondition')
        if interval and self.start_date>=self.date:raise ValueError('ordered endpoints')
        if (self.claim is not None)!=(self.operation=='assess_claim'):raise ValueError('claim precondition')
        if self.operation=='neighbor_stability':
            if len(set(self.candidates))!=3 or self.fire_ids[0] in self.candidates:raise ValueError('three distinct candidates')
        elif self.candidates:raise ValueError('inactive candidates')
        return self

class PilotAction(Contract):
    version: Literal['fire-pilot-action-v3']='fire-pilot-action-v3'
    action: Literal['select','inspect','call','answer','abstain']
    representation: Literal['R0','R1','R2'] | None = None
    operation: Op | None = None
    arguments: PilotArguments | None = None
    result_id: str | None = Field(default=None,max_length=64)
    evidence_ids: tuple[str,...] = Field(default=(),max_length=64)
    value: Any = None
    reason: str = Field(default='',max_length=1200)
    interpretation: Literal['exact','approximate','insufficient','unknown']='unknown'
    @field_validator('value')
    @classmethod
    def finite(cls,v):return AgentAction.finite_value(v)
    @model_validator(mode='after')
    def valid(self):
        if self.action=='call':
            if self.representation is None or self.operation is None or self.arguments is None:raise ValueError('complete call required')
            PilotQuery(operation=self.operation,**self.arguments.model_dump())
        elif self.operation is not None or self.arguments is not None:raise ValueError('inactive scientific query')
        if self.action in {'select','inspect'} and self.representation is None:raise ValueError('view required')
        if self.action in {'answer','abstain'} and self.representation is not None:raise ValueError('inactive view')
        if self.action!='answer' and (self.result_id is not None or self.evidence_ids or self.value is not None):raise ValueError('inactive answer')
        if self.action=='abstain' and not self.reason.strip():raise ValueError('reason required')
        return self

class PilotTask(Contract):
    task_id: str
    split: Literal['development','evaluation']
    template_id: str
    category: Literal['observation','morphology','compression','validity','cross_representation','efficiency']
    question: str
    query: PilotQuery
    accuracy: Literal['exact','projected_geometry']='exact'
    tolerance: float = Field(default=1e-8,ge=0)
    metadata_sensitivity: Literal['hypothesized','negative_control']
    preparation_paid: bool = True
    workload_queries: int = Field(default=1,ge=1,le=10000)
    @field_validator('tolerance')
    @classmethod
    def finite(cls,v):
        if not math.isfinite(v):raise ValueError('finite tolerance required')
        return v
    @model_validator(mode='after')
    def compatible(self):
        if (self.query.operation=='projected_distance') != (self.accuracy=='projected_geometry'):
            raise ValueError('explicit geometry target required')
        return self

class PilotLiveConfig(Contract):
    version: Literal['fire-pilot-live-v3']='fire-pilot-live-v3'
    fixture: str
    input_sha256: dict[str,str]
    provider: Literal['openclaw']='openclaw'
    model: str
    runtime: str = 'run/openclaw'
    access_authorized: bool = False
    cost_basis: Literal['unverified','operator_confirmed_no_external_charge']='unverified'
    approved_external_cost_cap: float = Field(default=0,ge=0,le=0)
    max_provider_calls: int = Field(default=6,ge=1,le=20000)
    repetitions: int = Field(default=2,ge=1,le=3)
    smoke_evidence: str | None = None
