"""Versioned scientific inputs, task definitions and fitted-artifact integrity."""
from datetime import date as CalendarDate, datetime
import math
from typing import Literal
from pydantic import Field, model_validator
from ..contracts import Contract, digest

PIN = '2e20e15a42610f77cdd0583bb5a43fcc6f6c8959'
UPSTREAM_SHA256 = '5b8fddd59c552fea22dc9a68fff911674a5a61c41399455e9fba1a9902c4ae9a'
FEATURE_ORDER = tuple(f'allocation_{i:02d}' for i in range(20))
OPERATIONS = ('cumulative', 'interval_growth', 'daily_growth', 'maximum_daily_growth',
              'peak_date', 'sequence_days', 'pulses', 'profile', 'front_fraction',
              'profile_distance', 'pca_distance', 'nearest_profile', 'scientific_analog')
Representation = Literal['R0', 'R1', 'R2']


class Source(Contract):
    source_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    uri: str = Field(min_length=1)
    license: str = Field(min_length=1)
    attribution: str = Field(min_length=1)
    method: str = Field(min_length=1)
    checksum: str = Field(pattern=r'^[a-f0-9]{64}$')
    checksum_scope: Literal['metadata', 'observations']
    synthetic: bool
    temporal_support: str = Field(min_length=1)
    spatial_support: str = Field(min_length=1)
    uncertainty: str = Field(min_length=1)


class Observation(Contract):
    observation_id: str = Field(min_length=1)
    date: CalendarDate
    available_at: datetime | None
    available: bool
    cumulative_area: float | None = Field(ge=0)
    daily_growth: float | None = Field(ge=0)
    days_since_previous: int | None = Field(ge=1)
    quality_flags: tuple[str, ...] = ()

    @model_validator(mode='after')
    def valid(self):
        if self.available != (self.cumulative_area is not None):
            raise ValueError('availability must match observed cumulative area; missing is not zero')
        if not self.available and (self.daily_growth is not None or self.available_at is not None):
            raise ValueError('a missing observation cannot have growth or an availability timestamp')
        if self.available_at is not None:
            if self.available_at.utcoffset() is None or self.available_at.date() < self.date:
                raise ValueError('availability must be timezone-aware and not predate observation')
        return self


class FireHistory(Contract):
    schema_version: Literal['fire-history-v1'] = 'fire-history-v1'
    fire_id: str = Field(min_length=1)
    split: Literal['train', 'evaluation']
    area_unit: Literal['km2']
    growth_unit: Literal['km2/day']
    source: Source
    baseline_date: CalendarDate | None
    baseline_area: float | None = Field(ge=0)
    baseline_evidence: str | None
    observations: tuple[Observation, ...] = Field(min_length=1, max_length=512)

    @model_validator(mode='after')
    def valid(self):
        if (self.baseline_date is None) != (self.baseline_area is None):
            raise ValueError('baseline date and area must both be supplied or both unknown')
        if self.baseline_date is not None and not self.baseline_evidence:
            raise ValueError('baseline requires explicit source evidence')
        dates = [o.date for o in self.observations]
        if dates != sorted(set(dates)):
            raise ValueError('observation dates must be unique and strictly ordered; no silent sorting')
        ids = [o.observation_id for o in self.observations]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate source observation identifiers')
        previous_date, previous_area = self.baseline_date, self.baseline_area
        if previous_date is not None and previous_date >= dates[0]:
            raise ValueError('baseline must precede observation sequence')
        for o in self.observations:
            expected_days = (o.date-previous_date).days if previous_date is not None else None
            if o.days_since_previous != expected_days:
                raise ValueError('temporal gap must refer to previous available observation or evidenced baseline')
            if o.available:
                if previous_area is not None and o.cumulative_area < previous_area:
                    raise ValueError('cumulative burned area decreased')
                expected = o.cumulative_area-previous_area if expected_days == 1 and previous_area is not None else None
                if expected is None:
                    if o.daily_growth is not None:
                        raise ValueError('growth across an unknown baseline or temporal gap is unknown, not daily')
                elif o.daily_growth is None or not math.isclose(o.daily_growth, expected, rel_tol=1e-10, abs_tol=1e-10):
                    raise ValueError('daily growth must equal evidenced one-day cumulative difference, including zero')
                previous_date, previous_area = o.date, o.cumulative_area
        if self.source.checksum_scope=='observations':
            packet={'observations':[o.model_dump(mode='json') for o in self.observations],
                'baseline_date':self.baseline_date.isoformat() if self.baseline_date else None,
                'baseline_area':self.baseline_area,'area_unit':self.area_unit,'growth_unit':self.growth_unit}
            if digest(packet)!=self.source.checksum:
                raise ValueError('canonical observation-packet checksum mismatch')
        return self

    @property
    def complete_sequence(self):
        return all(o.available and o.daily_growth is not None and o.days_since_previous == 1 for o in self.observations)

    @property
    def profile_eligible(self):
        return (len(self.observations) >= 3 and all(o.available and o.daily_growth is not None
                and o.days_since_previous == 1 for o in self.observations)
                and sum(o.daily_growth for o in self.observations) > 0)

    @property
    def growth(self):
        if not self.profile_eligible:
            raise ValueError('profile requires >=3 complete consecutive daily increments and positive total')
        return tuple(o.daily_growth for o in self.observations)


class Dataset(Contract):
    version: Literal['synthetic-fire-vase-v1']
    source_note: str
    histories: tuple[FireHistory, ...] = Field(min_length=3, max_length=64)

    @model_validator(mode='after')
    def valid(self):
        ids = [h.fire_id for h in self.histories]
        if len(ids) != len(set(ids)):
            raise ValueError('fire identity duplicated or crossing splits')
        if not all(h.source.synthetic for h in self.histories):
            raise ValueError('this milestone accepts explicitly synthetic observations only')
        return self


class Task(Contract):
    task_id: str = Field(min_length=1)
    family: Literal['A', 'B', 'C']
    question: str = Field(min_length=1)
    fire_ids: tuple[str, ...] = Field(min_length=1)
    operation: str
    required_operations: tuple[str, ...]
    required_observation_ids: tuple[str, ...] = Field(min_length=1)
    date: CalendarDate | None = None
    start_date: CalendarDate | None = None
    candidates: tuple[str, ...] = ()
    answer_type: Literal['number', 'date', 'profile', 'ids', 'pulses']
    unit: str
    tolerance: float = Field(ge=0)
    permitted_representations: tuple[Representation, ...]
    answerable: dict[Representation, bool]
    approximation_allowed: bool = False
    ground_truth_method: str = Field(min_length=1)
    validity_constraints: tuple[str, ...] = Field(min_length=1)
    expected_provenance: tuple[str, ...] = Field(min_length=1)
    evidence_kind: Literal['exact', 'geometry_diagnostic', 'pending_external_validation']

    @model_validator(mode='after')
    def valid(self):
        if self.required_operations!=(self.operation,):
            raise ValueError('this milestone permits one declared registered query operation per task')
        if self.operation not in OPERATIONS:
            raise ValueError('unknown operation identifier; no dynamic scientific code')
        if self.date is not None and self.operation not in {'cumulative','daily_growth','interval_growth'}:
            raise ValueError('date not a parameter of this operation')
        if self.start_date is not None and self.operation!='interval_growth':
            raise ValueError('start_date not a parameter of this operation')
        if (self.candidates or self.approximation_allowed) and self.operation!='nearest_profile':
            raise ValueError('candidate/approximation parameters are exclusive to neighbor diagnostics')
        if self.operation not in {'profile_distance','pca_distance'} and len(self.fire_ids)!=1:
            raise ValueError('operation requires exactly one primary fire')

        if set(self.answerable) != {'R0','R1','R2'} or set(self.permitted_representations) != {'R0','R1','R2'}:
            raise ValueError('all representation attempts and their answerability must be declared')
        if self.operation in {'cumulative','daily_growth'} and self.date is None:
            raise ValueError('date query needs an explicit observation date')
        if self.operation == 'interval_growth' and (self.date is None or self.start_date is None or self.start_date >= self.date):
            raise ValueError('interval query requires ordered endpoints')
        if self.operation in {'profile_distance','pca_distance'} and len(self.fire_ids) != 2:
            raise ValueError('pair comparison requires two fire identifiers')
        if self.operation == 'nearest_profile' and (len(set(self.candidates))<2 or len(set(self.candidates))!=len(self.candidates) or self.fire_ids[0] in self.candidates or not self.approximation_allowed):
            raise ValueError('neighbor diagnostic must declare candidates and allow representation approximation')
        return self


class TaskSet(Contract):
    version: Literal['fire-vase-tasks-v1']
    tasks: tuple[Task, ...] = Field(min_length=1,max_length=128)

    @model_validator(mode='after')
    def unique(self):
        if len({t.task_id for t in self.tasks}) != len(self.tasks):
            raise ValueError('duplicate task identifiers')
        return self


class BenchmarkConfig(Contract):
    version: Literal['fire-vase-benchmark-v1']
    fixture: str
    tasks: str
    metadata: str
    components: int = Field(ge=1, le=10)
    repeats: int = Field(ge=1, le=10)
    order_seed: int = Field(ge=0)
    query_cache_modes: tuple[Literal['cold','warm'], ...] = Field(min_length=1,max_length=2)
    synthetic_only: Literal[True]

    @model_validator(mode='after')
    def cache_modes_unique(self):
        if len(set(self.query_cache_modes))!=len(self.query_cache_modes):
            raise ValueError('duplicate cache modes')
        return self


class PCAArtifact(Contract):
    version: Literal['fire-vase-pca-v1']
    source_commit: Literal['2e20e15a42610f77cdd0583bb5a43fcc6f6c8959']
    upstream_sha256: str
    backend_versions: dict[str, str]
    feature_order: tuple[str, ...]
    training_ids: tuple[str, ...]
    training_history_digests: tuple[str, ...]
    training_feature_digest: str
    mean: tuple[float, ...]
    scale: tuple[float, ...]
    components: tuple[tuple[float, ...], ...]
    explained_variance: tuple[float, ...]
    artifact_digest: str

    @model_validator(mode='after')
    def valid(self):
        if (self.upstream_sha256 != UPSTREAM_SHA256 or self.feature_order != FEATURE_ORDER
            or len(self.training_ids) != len(set(self.training_ids))
            or len(self.training_ids) != len(self.training_history_digests)
            or len(self.mean) != 20 or len(self.scale) != 20 or any(s<=0 for s in self.scale)
            or not 1 <= len(self.components) <= min(10,len(self.training_ids)-1)
            or any(len(c)!=20 for c in self.components)
            or len(self.explained_variance) != len(self.components)
            or any(v<0 for v in self.explained_variance) or sum(self.explained_variance)>1+1e-10):
            raise ValueError('inconsistent PCA shape, training or scientific identity')
        import numpy as np
        w = np.array(self.components)
        if not np.allclose(w@w.T, np.eye(len(w)),rtol=0,atol=1e-8):
            raise ValueError('PCA components must be orthonormal')
        if digest(self.model_dump(mode='json',exclude={'artifact_digest'})) != self.artifact_digest:
            raise ValueError('PCA artifact integrity digest mismatch')
        return self


class DevelopmentalFeatures(Contract):
    version: Literal['fire-vase-features-v1'] = 'fire-vase-features-v1'
    history_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    source_commit: Literal['2e20e15a42610f77cdd0583bb5a43fcc6f6c8959'] = PIN
    profile: tuple[float, ...] = Field(min_length=20,max_length=20)
    traits: dict[str, float]

    @model_validator(mode='after')
    def valid_features(self):
        if any(v<0 for v in self.profile) or not math.isclose(sum(self.profile),1,abs_tol=1e-10):
            raise ValueError('profile must conserve nonnegative normalized growth mass')
        required={'front_loaded_fraction','late_growth_fraction','peak_timing','terminal_taper_fraction',
            'pulse_count','reactivation_count','normalized_first_difference','normalized_second_difference','normalized_entropy'}
        if set(self.traits)!=required or any(not math.isfinite(v) for v in self.traits.values()):
            raise ValueError('unexpected or missing interpreted feature definitions')
        return self


class CoordinateArtifact(Contract):
    version: Literal['fire-vase-coordinates-v1']
    artifact_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    dataset_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    dimensions: int = Field(ge=1,le=10)
    coordinates: dict[str, tuple[float,...] | None]

    @model_validator(mode='after')
    def valid_coordinates(self):
        if any(v is not None and len(v)!=self.dimensions for v in self.coordinates.values()):
            raise ValueError('coordinate dimension differs from frozen PCA layout')
        return self
