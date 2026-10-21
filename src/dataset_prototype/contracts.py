"""Immutable, validated inter-module contracts. JSON schemas are exportable."""
from datetime import datetime
from hashlib import sha256
import json
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


def digest(value) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


class Contract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", allow_inf_nan=False)


class Support(Contract):
    bbox: tuple[float, float, float, float]
    start: datetime
    end: datetime
    spatial: str = Field(min_length=1)
    temporal: str = Field(min_length=1)
    crs: str = "EPSG:4326"

    @model_validator(mode="after")
    def valid(self):
        x0, y0, x1, y1 = self.bbox
        if self.crs != "EPSG:4326" or not (-180 <= x0 <= x1 <= 180 and -90 <= y0 <= y1 <= 90):
            raise ValueError("V0 support requires valid EPSG:4326 bounds")
        if self.start.tzinfo is None or self.end.tzinfo is None or self.start > self.end:
            raise ValueError("ordered timezone-aware interval required")
        return self


class Rights(Contract):
    license: str = Field(min_length=1)
    attribution: str = Field(min_length=1)
    derivative_use: bool | None
    redistribution: bool | None
    access_restrictions: str = "none"


class Variable(Contract):
    name: str = Field(min_length=1)
    definition: str = Field(min_length=1)
    unit: str = Field(min_length=1)
    measurement_method: str = Field(min_length=1)
    biological_entity: str | None = None
    ontology_id: str | None = None


class Metadata(Contract):
    fixture: bool
    description: str
    platform: str | None = None
    sensor: str | None = None
    stac_version: str | None = None
    original_identifier: str
    native_metadata_json: str | None = None
    calibration_scale: float | None = None
    calibration_offset: float | None = None
    quality_mask_value: int | None = None


class ScientificRequest(Contract):
    question: str = Field(min_length=1)
    support: Support
    modalities: tuple[str, ...] = Field(min_length=1)
    variables: tuple[str, ...] = Field(min_length=1)
    track: str | None = None


class SourceResource(Contract):
    source_id: str
    dataset: str
    asset_id: str
    version: str = Field(min_length=1)
    uri: str = Field(min_length=1)
    modality: str
    variables: tuple[Variable, ...] = Field(min_length=1)
    support: Support
    metadata: Metadata
    rights: Rights
    checksum: str = Field(pattern=r"^[a-f0-9]{64}$")
    checksum_scope: Literal["asset", "extracted_window", "metadata"] = "asset"
    retrieved_at: datetime
    provenance: tuple[str, ...] = Field(min_length=1)


class DiscoveryCandidate(Contract):
    resource: SourceResource
    rationale: str


class DiscoveryResult(Contract):
    request: ScientificRequest
    candidates: tuple[DiscoveryCandidate, ...]
    warnings: tuple[str, ...] = ()


State = Literal["proposed", "needs_review", "approved", "rejected"]
Relation = Literal["equivalent_to", "convertible_to", "broader_than", "narrower_than", "derived_from", "measures", "associated_with", "not_comparable", "unknown", "requires_human_review"]


class SemanticMapping(Contract):
    source_asset: str
    source_variable: str
    target: Variable
    relationship: Relation
    evidence: tuple[str, ...] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    review_status: State = "proposed"
    novel: bool = False
    disagreement: bool = False


class Operation(Contract):
    source_asset: str | None = None
    operation: Literal["convert_units", "map_variable", "filter", "missing", "temporal_mean", "spatial_match", "normalize_coordinates", "join", "validate", "calibrate"]
    source_variable: str
    target_variable: str | None = None
    from_unit: str | None = None
    to_unit: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    sentinel: float | None = None
    target_support: str | None = None
    other_asset: str | None = None
    tolerance: float | None = None
    scale: float | None = None
    offset: float | None = None

    @model_validator(mode="after")
    def valid(self):
        if self.operation == "convert_units" and (self.from_unit, self.to_unit) not in {("degC", "K"), ("K", "degC"), ("cm", "m"), ("m", "cm")}:
            raise ValueError("unsupported unit conversion")
        if self.operation == "calibrate" and (self.scale is None or self.offset is None or self.scale == 0 or self.from_unit != "DN" or self.to_unit != "1"):
            raise ValueError("calibration requires explicit nonzero metadata scale/offset and DN to dimensionless units")
        if self.operation == "map_variable" and not self.target_variable:
            raise ValueError("target variable required")
        if self.operation == "temporal_mean" and self.target_support != "daily":
            raise ValueError("only daily temporal means supported")
        if self.operation in {"join", "spatial_match"} and not self.other_asset:
            raise ValueError("second asset required")
        if self.operation == "spatial_match" and (self.tolerance is None or self.tolerance < 0 or not self.target_support):
            raise ValueError("explicit tolerance and target support required")
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("invalid filter bounds")
        return self


class Proposal(Contract):
    role: Literal["discovery", "semantic", "units", "support", "rights", "harmonization", "qa"]
    agent: str = "deterministic-fixture-agent"
    version: str = "1"
    configuration: str = "curated rules; no LLM"
    rationale: str
    evidence: tuple[str, ...]


class AgentReview(Contract):
    recipe_content_digest: str
    outcome: Literal["approve", "reject", "request_revision", "require_human_review"]
    reasons: tuple[str, ...]
    reviewer: str


def recipe_content_digest(recipe):
    data = recipe.model_dump(mode="json", exclude={"status", "agent_review"})
    for mapping in data["mappings"]:
        mapping.pop("review_status", None)
    return digest(data)


class HarmonizationRecipe(Contract):
    recipe_id: str
    version: str
    scope: Literal["core", "track"]
    track: str | None = None
    core_recipe: str | None = None
    mappings: tuple[SemanticMapping, ...] = Field(min_length=1)
    operations: tuple[Operation, ...] = Field(min_length=1)
    proposals: tuple[Proposal, ...] = Field(min_length=1)
    status: State = "proposed"
    author: str = Field(min_length=1)
    agent_review: AgentReview | None = None

    @model_validator(mode="after")
    def scope_valid(self):
        if self.scope == "core" and (self.track or self.core_recipe):
            raise ValueError("core recipe cannot carry track assumptions")
        if self.scope == "track" and (not self.track or not self.core_recipe):
            raise ValueError("track recipe requires track and core recipe")
        if self.scope == "core" and any(o.operation in {"temporal_mean", "spatial_match", "join", "filter"} for o in self.operations):
            raise ValueError("application-specific selection/support operations require track scope")
        keys = [(m.source_asset, m.source_variable) for m in self.mappings]
        if len(set(keys)) != len(keys):
            raise ValueError("duplicate semantic mapping")
        return self


class QAReport(Contract):
    recipe_digest: str
    outcome: Literal["approve", "reject", "request_revision", "require_human_review"]
    reasons: tuple[str, ...]
    reviewer: str = "deterministic-adversarial-qa-v1"


class HumanDecision(Contract):
    recipe_digest: str
    status: Literal["approved", "rejected"]
    reviewer: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    timestamp: datetime
    fixture: bool = False


class RawObservation(Contract):
    record_id: str
    asset_id: str
    variable: str
    value: float | None
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    start: datetime
    end: datetime
    quality_flag: str = "synthetic"
    uncertainty: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def ordered(self):
        if self.start.tzinfo is None or self.end.tzinfo is None or self.start > self.end:
            raise ValueError("ordered timezone-aware observation interval required")
        return self


class ProvenanceRecord(Contract):
    source: SourceResource
    source_records: tuple[RawObservation, ...] = Field(min_length=1)
    recipe: HarmonizationRecipe
    qa: QAReport
    human: HumanDecision | None = None
    parent_observations: tuple[str, ...] = ()
    parent_lineage: tuple["ProvenanceRecord", ...] = ()
    context_sources: tuple[SourceResource, ...] = ()
    related_sources: tuple[SourceResource, ...] = ()
    related_records: tuple[RawObservation, ...] = ()
    executor: str = "allowlist-v2"


class HarmonizedObservation(Contract):
    observation_id: str
    variable: str
    value: float | None
    unit: str
    biological_entity: str | None
    measurement_method: str
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    spatial_support: str
    crs: str = "EPSG:4326"
    datetime_start: datetime
    datetime_end: datetime
    temporal_support: str
    dataset: str
    source: str
    source_variable: str
    source_version: str
    modality: str
    uncertainty: float | None
    quality_flag: str
    ontology_id: str | None
    semantic_relationships: tuple[SemanticMapping, ...]
    track: str | None = None
    provenance: ProvenanceRecord


    @model_validator(mode="after")
    def scientific_lineage(self):
        p = self.provenance
        if p.recipe.status != "approved" or p.qa.recipe_digest != digest(p.recipe):
            raise ValueError("observation requires exact approved recipe and QA lineage")
        if p.qa.outcome not in {"approve", "require_human_review"}:
            raise ValueError("observation QA is not executable")
        if p.qa.outcome == "require_human_review" and (p.human is None or p.human.status != "approved" or p.human.recipe_digest != digest(p.recipe)):
            raise ValueError("observation lacks required bound human review")
        if self.track != p.recipe.track or self.source != p.source.source_id or self.source_version != p.source.version or self.dataset != p.source.dataset or self.modality != p.source.modality:
            raise ValueError("observation context disagrees with lineage")
        if self.crs != "EPSG:4326" or self.datetime_start > self.datetime_end:
            raise ValueError("invalid observation support")
        mapping = next((m for m in p.recipe.mappings if m.source_asset == p.source.asset_id and m.source_variable == self.source_variable), None)
        if mapping is None or (self.variable, self.unit, self.measurement_method, self.biological_entity, self.ontology_id) != (mapping.target.name, mapping.target.unit, mapping.target.measurement_method, mapping.target.biological_entity, mapping.target.ontology_id):
            raise ValueError("observation scientific meaning disagrees with recipe")
        if self.track and (not p.parent_observations or len(p.parent_observations) != len(p.parent_lineage)):
            raise ValueError("track observation requires complete core lineage")
        return self


class Representation(Contract):
    representation_id: str
    observation_ids: tuple[str, ...] = Field(min_length=1)
    modality: str
    vector: tuple[float, ...]
    encoder: str
    encoder_version: str
    preprocessing: str
    dimensionality: int = Field(gt=0)
    track: str | None
    provenance: tuple[ProvenanceRecord, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def dimensions(self):
        if self.dimensionality != len(self.vector) or len(self.observation_ids) != len(self.provenance):
            raise ValueError("vector dimensions or lineage cardinality mismatch")
        if any(p.recipe.track != self.track or p.source.modality != self.modality for p in self.provenance):
            raise ValueError("representation modality/track disagrees with lineage")
        return self


class TrackConfig(Contract):
    track: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    question: str
    variables: tuple[str, ...] = Field(min_length=1)
    modalities: tuple[str, ...] = Field(min_length=1)
    support: Support
    enabled: bool = True
    assumption: str
    encoder: Literal["scalar", "squared"] = "scalar"
