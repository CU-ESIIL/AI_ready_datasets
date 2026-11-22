"""Full-lake proposal and externally supplied scoped review; never self-approval."""
from datetime import datetime
import math
from typing import Literal
from pydantic import Field,model_validator
from ..contracts import Contract,digest

SCOPES=('verify_container_bytes','profile_rows','harmonize','features','train_neural','retrospective_prediction',
 'retrieval','spatial_environment','benchmark','publish_outputs')
JURISDICTIONS=('semantic','units','support','rights','integrity','quality','availability','execution','publication')

class LakePlan(Contract):
    version: Literal['fire-full-lake-plan-v1']='fire-full-lake-plan-v1'
    claim: Literal['retrospective_reconstructed']='retrospective_reconstructed'
    inventory_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    source_release: str
    scientific_binding_digests: tuple[str,...]=()
    reviewed_geometry_capabilities: tuple[str,...]=()
    reviewed_environment_capabilities: tuple[str,...]=()
    scope: tuple[str,...]=SCOPES
    population: Literal['all_task_eligible_fires']='all_task_eligible_fires'
    row_limit: None=None
    batch_rows: int=Field(default=1024,ge=1,le=8192)
    window_days: int=Field(default=30,ge=3,le=30)
    horizons: tuple[int,...]=(1,3,7)
    lengths: tuple[int,...]=(3,7,14,30)
    embedding_dimensions: tuple[int,...]=(4,8,16,32,64)
    training_fractions: tuple[float,...]=(.01,.03,.1,.3,1.)
    primary_metrics: tuple[str,...]=('fire_mean_log_mse','fire_mean_brier','future_relevance_precision_at_10','scoped_total_cost')
    minimum_effect_sizes: dict[str,float | None]=Field(default_factory=lambda:{'prediction':None,'classification':None,'retrieval':None,'cost':None})
    meaning_of_thresholds: Literal['SCIENTIST_REVIEW_REQUIRED']='SCIENTIST_REVIEW_REQUIRED'
    persist_raw_or_harmonized: Literal[False]=False
    agent_inference_authorized: Literal[False]=False
    @model_validator(mode='after')
    def registered(self):
        if set(self.scope)!=set(SCOPES) or len(self.scope)!=len(SCOPES):raise ValueError('explicit full-lake scopes required')
        if self.horizons!=(1,3,7) or self.lengths!=(3,7,14,30):raise ValueError('fixed scientific support definitions')
        if not self.training_fractions or self.training_fractions[-1]!=1 or any(not 0<f<=1 for f in self.training_fractions) or tuple(sorted(set(self.training_fractions)))!=self.training_fractions:raise ValueError('whole eligible training cohort must be included')
        if not self.embedding_dimensions or any(d not in (4,8,16,32,64) for d in self.embedding_dimensions) or len(set(self.embedding_dimensions))!=len(self.embedding_dimensions):raise ValueError('registered embedding dimensions')
        if any(v is not None and (v<0 or not math.isfinite(v)) for v in self.minimum_effect_sizes.values()):raise ValueError('finite nonnegative expert effect sizes')
        return self
    @property
    def plan_digest(self):return digest(self)

class ScopeFinding(Contract):
    scope: str
    jurisdiction: str
    status: Literal['PASS','FAIL','NEEDS_EVIDENCE','NOT_APPLICABLE']
    evidence_ids: tuple[str,...]=Field(min_length=1)
    rationale: str=Field(min_length=1)
    @model_validator(mode='after')
    def registered(self):
        if self.scope not in SCOPES or self.jurisdiction not in JURISDICTIONS:raise ValueError('unknown scope/jurisdiction')
        return self

class LakeAuthorization(Contract):
    version: Literal['fire-full-lake-authorization-v1']='fire-full-lake-authorization-v1'
    plan_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    origin: Literal['DRAFT','EXTERNAL_HUMAN_REVIEW']='DRAFT'
    reviewer: str | None=None
    timestamp: datetime | None=None
    human_receipt_reference: str | None=None
    receipt_verified_by: str | None=None
    approved_scopes: tuple[str,...]=()
    findings: tuple[ScopeFinding,...]=()
    @model_validator(mode='after')
    def scoped(self):
        if not set(self.approved_scopes)<=set(SCOPES) or len(set(self.approved_scopes))!=len(self.approved_scopes):raise ValueError('unknown/duplicate scopes')
        if len({(f.scope,f.jurisdiction) for f in self.findings})!=len(self.findings):raise ValueError('duplicate jurisdiction')
        if self.origin=='DRAFT' and self.approved_scopes:raise ValueError('draft cannot authorize any phase')
        return self

class SourceBinding(Contract):
    version: Literal['fire-source-binding-v1']='fire-source-binding-v1'
    source_relative_path: str
    expected_sha256: str=Field(pattern=r'^[a-f0-9]{64}$')
    event_field: str
    date_field: str
    area_field: str
    native_area_unit: Literal['km2']='km2'
    meaning: Literal['reviewed_area_per_native_calendar_day_bin']='reviewed_area_per_native_calendar_day_bin'
    sorted_by_event_and_date: bool
    date_interpretation: Literal['native_iso_date','reviewed_midnight_date_bin']
    semantic_evidence: str=Field(min_length=1)
    uncertainty_evidence: str=Field(min_length=1)
    quality_fields: tuple[str,...]=()
    availability_field: str | None=None
    cumulative_field: str | None=None
    @property
    def binding_digest(self):return digest(self)
