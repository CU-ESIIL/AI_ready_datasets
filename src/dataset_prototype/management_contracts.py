"""Operational metadata contracts; registration never grants scientific authority."""
from datetime import datetime, timezone
from typing import Literal
from pydantic import Field, model_validator
from .contracts import Contract, digest

ArtifactKind = Literal[
    'source', 'semantic_resource', 'semantic_assessment', 'semantic_profile',
    'mapping', 'recipe', 'review', 'human_decision', 'context', 'operation_registry',
    'run', 'encoder', 'verification', 'dataset', 'release', 'workspace',
    'service', 'allocation', 'usage', 'feedback', 'preservation', 'benchmark', 'product',
]
Track = Literal['forest_bioresources', 'cropland_food', 'watershed_water']


class BlobReference(Contract):
    sha256: str = Field(pattern=r'^[a-f0-9]{64}$')
    bytes: int = Field(ge=0)
    name: str = Field(pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,99}$')
    media_type: Literal['application/json', 'application/x-ndjson',
                        'application/x-npy', 'application/x-npz', 'text/markdown']


class ArtifactRecord(Contract):
    schema_version: Literal['1'] = '1'
    artifact_id: str = Field(pattern=r'^[a-f0-9]{64}$')
    kind: ArtifactKind
    title: str = Field(min_length=1, max_length=240)
    fixture: bool
    visibility: Literal['public', 'controlled'] = 'controlled'
    track: Track | None = None
    parents: tuple[str, ...] = Field(default=(), max_length=128)
    payload: dict
    blobs: tuple[BlobReference, ...] = ()
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode='after')
    def identity(self):
        if self.created_at.tzinfo is None:
            raise ValueError('timezone-aware creation time required')
        if len(self.parents) != len(set(self.parents)):
            raise ValueError('duplicate parent references')
        if len({b.name for b in self.blobs}) != len(self.blobs):
            raise ValueError('duplicate blob names')
        body = self.model_dump(mode='json', exclude={'artifact_id', 'created_at'})
        if digest(body) != self.artifact_id:
            raise ValueError('artifact identity/content mismatch')
        return self


class ProductDefinition(Contract):
    track: Track
    name: str
    state: Literal['planned'] = 'planned'
    observation_unit: str | None = None
    scientific_scope_status: Literal['requires_scientific_definition'] = 'requires_scientific_definition'


class ServiceDefinition(Contract):
    name: str
    boundary: str
    capability: Literal['WORKING', 'PROTOTYPE', 'MOCKED', 'PLANNED', 'UNDER ANALYSIS']
    host: str
    endpoint: str | None = None
    limitation: str


class AllocationPlan(Contract):
    provider: str
    resource: str
    unit: Literal['GB', 'CPU_SU', 'GPU_hour']
    requested: float = Field(gt=0)
    status: Literal['planning_estimate', 'requested', 'awarded'] = 'planning_estimate'
    period: str
    evidence_uri: str | None = None
    verified_at: str | None = None
    limitation: str

    @model_validator(mode='after')
    def award_evidence(self):
        if self.status == 'awarded' and not self.evidence_uri:
            raise ValueError('awarded capacity requires award evidence')
        return self


class WorkspaceDefinition(Contract):
    group_id: str = Field(pattern=r'^(governance-[1-3]|synthesis-[1-6])$')
    cohort: Literal['governance', 'synthesis']
    years: tuple[int, int]
    quota_bytes: int = Field(gt=0)
    quota_status: Literal['planning_estimate'] = 'planning_estimate'
    dataset_ids: tuple[str, ...] = ()
    retention: str

    @model_validator(mode='after')
    def cohort_identity(self):
        if not self.group_id.startswith(self.cohort + '-'):
            raise ValueError('group and cohort differ')
        if self.years != ((1, 2) if self.cohort == 'governance' else (2, 3)):
            raise ValueError('cohort years differ from project schedule')
        return self


class UsageMeasurement(Contract):
    activity: str
    metric: Literal['wall_seconds', 'process_cpu_seconds', 'bytes_read', 'bytes_written', 'records']
    value: float = Field(ge=0)
    scope: str
    evidence_kind: Literal['DERIVED_DETERMINISTICALLY'] = 'DERIVED_DETERMINISTICALLY'
    provider_billing: Literal[False] = False


class FeedbackIssue(Contract):
    target_id: str = Field(pattern=r'^[a-f0-9]{64}$')
    group_id: str = Field(pattern=r'^(governance-[1-3]|synthesis-[1-6])$')
    category: Literal['semantics', 'harmonization', 'representation', 'rights', 'interface']
    summary: str = Field(min_length=5, max_length=240)
    detail: str = Field(min_length=5, max_length=4000)
    state: Literal['open'] = 'open'
    permission: Literal['issue_only_no_execution_authority'] = 'issue_only_no_execution_authority'


class DatasetEntry(Contract):
    records: int = Field(ge=1)
    dimensions: int = Field(ge=1)
    dtype: Literal['float32'] = 'float32'
    encoder_identity: str
    context_digest: str
    fixture: bool
    manifest: dict
    scientific_validation: Literal['not_established'] = 'not_established'


class ReleaseEntry(Contract):
    dataset_id: str = Field(pattern=r'^[a-f0-9]{64}$')
    verification_id: str = Field(pattern=r'^[a-f0-9]{64}$')
    state: Literal['diagnostic', 'needs_scientific_release_review']
    scientific_approval: Literal[False] = False
    persistent_identifier: None = None
    limitation: str


class PreservationResult(Contract):
    snapshot_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    records: int = Field(ge=1)
    blobs: int = Field(ge=0)
    bytes: int = Field(ge=0)
    verification: Literal['fixity_checked'] = 'fixity_checked'
    retention_agreement: None = None
    remote_deposit: Literal[False] = False


class ScaleProbe(Contract):
    generated_records: int = Field(ge=1, le=100000)
    scope: Literal['generated_metadata_index_only'] = 'generated_metadata_index_only'
    write_seconds: float = Field(ge=0)
    page_query_seconds: float = Field(ge=0)
    database_bytes: int = Field(ge=0)
    limitation: str = 'Local index probe; not global raster throughput, scientific validity or an ACCESS allocation benchmark.'
