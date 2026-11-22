"""M6 preapproval scientific contracts. Records are not source access or approval."""
from datetime import date,datetime
from typing import Literal
from pydantic import Field,model_validator
from ..contracts import Contract,digest

Status=Literal['PASS','FAIL','NEEDS_EVIDENCE','NOT_APPLICABLE']
Domain=Literal['semantic','units','support','rights','integrity','quality','availability']
DOMAINS=tuple(Domain.__args__)

class RealSourceIdentity(Contract):
    source_id: str = Field(min_length=1)
    package_release: str = Field(min_length=1)
    package_relative_path: str
    local_path: str
    file_format: Literal['gpkg','parquet']
    expected_size_bytes: int = Field(gt=0)
    reported_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    checksum_evidence: str
    checksum_scope: Literal['historical_full_container_not_reverified']='historical_full_container_not_reverified'
    measurement_semantics: str
    native_fields: tuple[str,...] = Field(min_length=1)
    rights_status: Status='NEEDS_EVIDENCE'
    rights_evidence: tuple[str,...]=()
    @model_validator(mode='after')
    def relative(self):
        from pathlib import PurePosixPath
        path=PurePosixPath(self.package_relative_path)
        if path.is_absolute() or '..' in path.parts:raise ValueError('package path must be relative and contained')
        return self

class RecipeProposal(Contract):
    operation: Literal['native_increment_identity','calendar_support_validation','observed_prefix_only',
        'independent_future_targets','fire_grouped_holdouts']
    version: Literal['m6-review-v1']='m6-review-v1'
    status: Literal['PROPOSED_FOR_REVIEW']='PROPOSED_FOR_REVIEW'
    source_fields: tuple[str,...]
    intended_meaning: str
    preconditions: tuple[str,...] = Field(min_length=1)
    preserved_evidence: tuple[str,...] = Field(min_length=1)
    implementation_evidence: tuple[str,...]

class BoundedReadProposal(Contract):
    purpose: Literal['native_schema_value_alignment_audit']='native_schema_value_alignment_audit'
    max_total_decoded_rows: int = Field(default=512,ge=1,le=512)
    max_fires: int = Field(default=16,ge=1,le=16)
    batch_rows: int = Field(default=128,ge=1,le=128)
    read_geometries: Literal[False]=False
    full_source_scan: Literal[False]=False
    persist_raw_or_harmonized: Literal[False]=False
    train_models: Literal[False]=False
    redistribute_observations: Literal[False]=False
    @model_validator(mode='after')
    def bounded(self):
        if self.batch_rows>self.max_total_decoded_rows:raise ValueError('batch exceeds whole sample cap')
        return self

class RealStudyPacket(Contract):
    version: Literal['fire-real-review-packet-v1']='fire-real-review-packet-v1'
    purpose: str
    proposed_claim: Literal['retrospective_reconstructed','prospective_available_at_issue']
    sources: tuple[RealSourceIdentity,...] = Field(min_length=1)
    recipes: tuple[RecipeProposal,...] = Field(min_length=1)
    sample: BoundedReadProposal
    scientific_requirements: tuple[str,...] = Field(min_length=1)
    exclusions: tuple[str,...] = Field(min_length=1)
    unresolved: tuple[str,...]
    @model_validator(mode='after')
    def unique(self):
        if len({s.source_id for s in self.sources})!=len(self.sources):raise ValueError('duplicate source identity')
        if len({r.operation for r in self.recipes})!=len(self.recipes):raise ValueError('duplicate proposed operation')
        return self
    @property
    def packet_digest(self):return digest(self)

class ScientificReviewItem(Contract):
    domain: Domain
    status: Status
    evidence_ids: tuple[str,...] = Field(min_length=1)
    rationale: str = Field(min_length=1)

class RealStudyReview(Contract):
    """Externally supplied human review record; cannot authenticate its own authorship."""
    packet_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    origin: Literal['DRAFT_AGENT_PROPOSAL','HUMAN_REVIEW']='DRAFT_AGENT_PROPOSAL'
    reviewer: str | None = None
    reviewed_at: datetime | None = None
    decision: Literal['PENDING','APPROVE_BOUNDED_AUDIT','REJECT']='PENDING'
    findings: tuple[ScientificReviewItem,...]
    @model_validator(mode='after')
    def jurisdictions(self):
        if {f.domain for f in self.findings}!=set(DOMAINS) or len(self.findings)!=len(DOMAINS):raise ValueError('all distinct review jurisdictions required')
        if self.origin=='DRAFT_AGENT_PROPOSAL' and self.decision!='PENDING':raise ValueError('an agent draft cannot approve or reject a scientific human decision')
        if self.origin=='HUMAN_REVIEW' and (not self.reviewer or self.reviewed_at is None or self.reviewed_at.utcoffset() is None):raise ValueError('attributed timestamped external human review required')
        return self

class ContainerVerification(Contract):
    source_id: str
    checksum_sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    scope: Literal['complete_container_bytes']='complete_container_bytes'
    method: Literal['sha256_stream_without_decoding']='sha256_stream_without_decoding'
    verified_at: datetime
    @model_validator(mode='after')
    def timestamp(self):
        if self.verified_at.utcoffset() is None:raise ValueError('verification timestamp must be timezone aware')
        return self

class SupportCheckRow(Contract):
    """Generic generated validation input, not a real-source row adapter."""
    source_observation_id: str
    event_id: str
    native_date: date
    available: bool
    native_area_km2: float | None = Field(default=None,ge=0,allow_inf_nan=False)
    quality_flags: tuple[str,...]=()
    @model_validator(mode='after')
    def presence(self):
        if self.available!=(self.native_area_km2 is not None):raise ValueError('missing and observed zero are distinct')
        return self
