"""Metadata control plane and bounded streaming data plane contracts."""
from typing import Literal
from pydantic import Field, model_validator, model_serializer
from .contracts import Contract, SourceResource, Variable, RawObservation, digest

SPECIALISTS = ('semantic', 'units', 'support', 'rights')
REVIEWERS = (*SPECIALISTS, 'qa')


class StreamBinding(Contract):
    binding_id: str
    source: SourceResource
    source_variable: str
    target: Variable
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)

    @model_validator(mode='after')
    def valid(self):
        if self.source_variable not in {v.name for v in self.source.variables}:
            raise ValueError('binding variable missing from metadata')
        return self


class EncoderSpec(Contract):
    method: Literal['scalar', 'squared', 'mosaiks'] = 'scalar'
    encoder: str = 'identity-scalar'
    version: str = '1'
    dimensionality: int = 1
    preprocessing: str = 'none; input quantity and units are defined by the recipe'
    purpose: str = 'Reference numeric features; not a learned or universal embedding'
    configuration_json: str | None = None

    @model_serializer(mode='wrap')
    def serialize(self,handler):
        data=handler(self)
        if self.configuration_json is None:data.pop('configuration_json',None)
        return data

    @model_validator(mode='after')
    def valid(self):
        if self.method=='mosaiks':
            from .mosaiks import MOSAIKSSpec
            from .mosaiks_pipeline import encoder_contract
            spec=MOSAIKSSpec.model_validate_json(self.configuration_json or '{}')
            if (self.encoder,self.version,self.dimensionality,self.preprocessing,self.purpose)!=encoder_contract(spec):
                raise ValueError('MOSAIKS encoder contract mismatch')
            return self
        if self.configuration_json is not None or self.purpose!='Reference numeric features; not a learned or universal embedding':
            raise ValueError('reference encoder metadata mismatch')
        expected = ('identity-scalar',1) if self.method=='scalar' else ('scalar-and-square',2)
        preprocessing = 'none; input quantity and units are defined by the recipe' if self.method=='scalar' else 'append square; no scaling'
        if (self.encoder,self.dimensionality)!=expected or self.version!='1' or self.preprocessing!=preprocessing:
            raise ValueError('encoder identity/version/dimensions disagree with implementation')
        return self


class StreamPlan(Contract):
    version: str = '1'
    question: str = Field(min_length=1)
    reader: Literal['sentinel-pixel','sentinel-raster','test-generator']
    bindings: tuple[StreamBinding,...] = Field(min_length=1,max_length=16)
    encoder: EncoderSpec = EncoderSpec()
    batch_size: int = Field(default=32,ge=1,le=1024)
    persist_raw_data: Literal[False] = False
    persist_harmonized_data: Literal[False] = False
    raster_layout_json: str | None = None

    @model_serializer(mode='wrap')
    def serialize(self,handler):
        data=handler(self)
        if self.raster_layout_json is None:data.pop('raster_layout_json',None)
        return data

    access_policy: str = 'bounded window/range reads; no full-asset download or disk data cache'

    @model_validator(mode='after')
    def valid(self):
        if self.reader=='sentinel-raster':
            from .mosaiks_pipeline import RasterLayout
            RasterLayout.model_validate_json(self.raster_layout_json or '{}')
            if self.encoder.method!='mosaiks':raise ValueError('reviewed raster plan requires MOSAIKS specification')
        elif self.raster_layout_json is not None:raise ValueError('raster layout requires raster reader')
        ids=[b.binding_id for b in self.bindings]
        pairs=[(b.source.asset_id,b.source_variable) for b in self.bindings]
        if len(set(ids))!=len(ids) or len(set(pairs))!=len(pairs):
            raise ValueError('duplicate stream bindings')
        return self

    @property
    def resources(self):
        return tuple({b.source.asset_id:b.source for b in self.bindings}.values())


class StreamSample(Contract):
    record: RawObservation
    sequence: int = Field(ge=0)
    evidence_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    evidence_scope: str
    spatial_bbox: tuple[float,float,float,float]
    native_crs: str
    native_indices: tuple[int,...]
    binding_id: str


    @model_validator(mode='after')
    def valid(self):
        x0,y0,x1,y1=self.spatial_bbox
        if not (-180<=x0<=x1<=180 and -90<=y0<=y1<=90):
            raise ValueError('stream footprint requires valid EPSG:4326 bounds')
        if any(i<0 for i in self.native_indices) or not self.native_indices or not self.native_crs:
            raise ValueError('native window indices and CRS required')
        return self


class AgentMessage(Contract):
    message_id: str
    round: int = Field(ge=0)
    sender: str
    kind: Literal['analysis','draft','review']
    reply_to: tuple[str,...]
    recipe_content_digest: str | None = None
    payload_json: str
    prompt_digest: str | None = None
    response_digest: str | None = None


class SpecialistFinding(Contract):
    assessment: str = Field(min_length=1,max_length=2500)
    constraints: tuple[str,...] = Field(max_length=8)
    concerns: tuple[str,...] = Field(max_length=8)
    evidence_refs: tuple[str,...] = Field(min_length=1,max_length=16)


class ReviewVote(Contract):
    decision: Literal['agree','revise','reject','abstain']
    rationale: str = Field(min_length=1,max_length=2500)
    concerns: tuple[str,...] = Field(max_length=8)
    responds_to: tuple[str,...] = Field(min_length=1,max_length=24)
    evidence_refs: tuple[str,...] = Field(min_length=1,max_length=16)


class RecipeBindingProposal(Contract):
    binding_id: str
    relationship: Literal['equivalent_to','convertible_to','not_comparable','unknown','requires_human_review']
    evidence: tuple[str,...] = Field(min_length=1,max_length=8)
    confidence: float = Field(ge=0,le=1)
    # Canonical target identity and scientific goal are fixed by StreamPlan.
    operations: tuple['Operation',...] = Field(min_length=1,max_length=8)


from .contracts import Operation
RecipeBindingProposal.model_rebuild()


class RecipeDraft(Contract):
    bindings: tuple[RecipeBindingProposal,...] = Field(min_length=1,max_length=16)
    rationale: str = Field(min_length=1,max_length=2500)
    responds_to: tuple[str,...] = Field(min_length=1,max_length=32)


class ConsensusReport(Contract):
    status: Literal['consensus','needs_revision','rejected','abstained']
    plan_digest: str
    recipe_content_digest: str
    rounds: int
    votes: tuple[tuple[str,ReviewVote],...]
    unresolved: tuple[str,...]
    human_review_required: Literal[True] = True
    data_read_during_planning: Literal[False] = False
