"""Backend-neutral cube metadata contracts; external arrays never serialize here."""
from typing import Literal, Protocol, Any
from pydantic import Field, model_validator
from .contracts import Contract, BackendOperation

CUBE_VERSION='0.1.0rc3'

class ResourceGuards(Contract):
    max_input_bytes: int = Field(default=16_777_216,ge=1,le=67_108_864)
    max_output_bytes: int = Field(default=4_194_304,ge=1,le=16_777_216)
    max_chunks: int = Field(default=256,ge=1,le=1024)
    max_tasks: int = Field(default=4096,ge=1,le=16384)
    max_axis: int = Field(default=512,ge=1,le=4096)
    max_time_seconds: int = Field(default=31_622_400,ge=1,le=31_622_400)

class CubeInput(Contract):
    resource_ids: tuple[str,...] = Field(min_length=1,max_length=16)
    variable_units: dict[str,str]
    crs: str
    spatial_resolution: tuple[float,float]
    spatial_support: str = Field(min_length=1)
    temporal_resolution_seconds: float | None = Field(default=None,gt=0)
    temporal_support: Literal['instantaneous','equal_intervals','unknown']
    interval_seconds: float | None = Field(default=None,gt=0)
    mask_definition: str | None = None
    stage: Literal['source','harmonized'] = 'harmonized'

    @model_validator(mode='after')
    def valid(self):
        if not self.variable_units or min(self.spatial_resolution)<=0:
            raise ValueError('PRECONDITION_FAILED: variable units and positive resolution required')
        if self.interval_seconds is not None and self.interval_seconds*1e9!=round(self.interval_seconds*1e9):
            raise ValueError('INVALID_PARAMETERS: interval precision finer than one nanosecond unsupported')
        if self.temporal_support=='equal_intervals' and self.interval_seconds is None:
            raise ValueError('NEEDS_EVIDENCE: interval duration required')
        return self

class CubeConfiguration(Contract):
    version: Literal['1']='1'
    inputs: dict[str,CubeInput]
    variable: str | None = None
    # Half-open positional time/y/x window, resolved from reviewed configuration.
    window: tuple[int,int,int,int,int,int] | None = None
    months: tuple[Literal[1,2,3,4,5,6,7,8,9,10,11,12],...] = ()
    allowed_quality_classes: tuple[int,...] = ()
    target_temporal_support: str | None = None
    target_temporal_resolution_seconds: float | None = Field(default=None,gt=0)
    target_spatial_support: str | None = None
    evidence: tuple[str,...] = Field(min_length=1)
    scientific_justification: str = Field(min_length=1)
    materialize: bool = False
    guards: ResourceGuards = ResourceGuards()

class TransformationChanges(Contract):
    values: bool
    units: bool=False
    crs: bool=False
    spatial_resolution: bool=False
    spatial_support: bool=False
    temporal_resolution: bool=False
    temporal_support: bool=False
    extent: bool=False
    biological_level: bool=False
    aggregation: bool=False

class TransformationResult(Contract):
    operation_id: str
    operation_version: str
    input_resource_ids: tuple[str,...]
    output_resource_id: str
    backend: Literal['cubedynamics']='cubedynamics'
    backend_version: str
    dependency_versions: dict[str,str]
    parameters: dict[str,str]
    resolved_parameters: dict
    input_metadata: dict
    output_metadata: dict
    changes: TransformationChanges
    lazy: bool
    materialized: bool
    status: Literal['LAZY_PLAN','EXECUTED']
    validation_results: tuple[str,...]
    provenance: dict

class TransformationBackend(Protocol):
    def capabilities(self) -> dict: ...
    def validate(self, recipe:Any, sources:tuple, configuration:CubeConfiguration, inputs:dict, human:Any) -> None: ...
    def execute(self, recipe:Any, sources:tuple, configuration:CubeConfiguration, inputs:dict, human:Any) -> Any: ...

class CubeOption(Contract):
    option_id: str
    step: BackendOperation

class CubeCapabilitySpace(Contract):
    context_digest: str
    base_recipe_digest: str
    options: tuple[CubeOption,...]

    @property
    def identity(self):
        from .contracts import digest
        return digest(self)
