"""Closed, versioned operation library. No model code, imports or expressions execute."""
from collections import defaultdict
from hashlib import sha256
from datetime import timedelta
from types import MappingProxyType
from pydantic import Field
from .contracts import Contract, Operation, digest

REGISTRY_VERSION = '1'
EXECUTOR_VERSION = 'registered-allowlist-v3'
VALIDATOR_VERSION = 'scientific-preconditions-v1'
CONSTANTS_VERSION = 'units-v1'
UNIT_CONVERSIONS = MappingProxyType({('degC','K'):(1,273.15), ('K','degC'):(1,-273.15),
                                    ('cm','m'):(.01,0), ('m','cm'):(100,0)})

class OperationDefinition(Contract):
    operation_id: str
    legacy_name: str
    name: str
    version: str = '1'
    description: str
    input_contract: str = 'validated row tuples with source/support lineage'
    output_contract: str = 'validated row tuples; HarmonizedObservation validation at executor boundary'
    parameter_schema: dict
    implementation_reference: str = 'dataset_prototype.operations._execute_rows'
    scientific_assumptions: tuple[str,...]
    preconditions: tuple[str,...]
    postconditions: tuple[str,...] = ('canonical output and provenance validated',)
    allowed_units: tuple[str,...] = ()
    allowed_quantity_kinds: tuple[str,...] = ('explicit reviewed mapping only; no inferred quantity kinds',)
    changes_spatial_support: bool = False
    changes_temporal_support: bool = False
    changes_biological_level: bool = False
    requires_human_approval: bool = False
    tests: tuple[str,...] = ('tests/test_harmonization.py', 'tests/test_operation_registry.py')
    provenance: str = 'registered implementation identity plus source/recipe/review lineage'

# Only implemented operations are listed. These are not plugin entry points.
_SPECS = (
 ('unit.convert','convert_units','Fixed unit conversion',('from_unit','to_unit'),('Four explicit unit pairs; no inferred equivalence',),False,False,False),
 ('calibration.scale_offset','calibrate','Documented DN calibration',('from_unit','to_unit','scale','offset'),('Exact source metadata coefficients; DN to unit 1 only',),False,False,True),
 ('semantic.rename','map_variable','Reviewed canonical variable name',('target_variable',),('Rename does not establish scientific equivalence',),False,False,False),
 ('quality.filter','filter','Inclusive reviewed bounds',('minimum','maximum'),('Track-only selection; no inferred plausibility limits',),False,False,False),
 ('quality.missing','missing','Explicit sentinel to missing',('sentinel',),('No imputation; downstream encoder rejects null',),False,False,False),
 ('temporal.aggregate.daily_mean','temporal_mean','Duration-weighted daily mean',('target_support',),('Complete nonoverlapping UTC-aligned 86400-second day; not local civil days',),False,True,True),
 ('spatial.match','spatial_match','Unique coordinate-tolerance match',('other_asset','tolerance','target_support'),('WGS84 degree tolerance and exact interval; not a distance/resampling algorithm',),True,False,True),
 ('spatial.validate_wgs84','normalize_coordinates','WGS84 identity validation',(),('Coordinates already WGS84; no reprojection',),False,False,False),
 ('observation.join_exact','join','Unique exact-support join',('other_asset',),('Exact coordinates/interval and equal support; permitted rights',),False,False,True),
 ('quality.validate_bounds','validate','Explicit numeric bounds',('minimum','maximum'),('No bounds means identity validation; no inferred clipping',),False,False,False),
)

def _definitions():
    schema=Operation.model_json_schema()
    return tuple(OperationDefinition(operation_id=identifier,legacy_name=legacy,name=name,description=name,
        parameter_schema={'type':'object','additionalProperties':False,'properties':{k:schema['properties'][k] for k in fields}},
        scientific_assumptions=assumptions,preconditions=('typed parameters','source/target semantics, units, rights and review gates checked'),
        changes_spatial_support=spatial,changes_temporal_support=temporal,requires_human_approval=human,
        allowed_units=('degC','K','cm','m') if legacy=='convert_units' else ('DN','1') if legacy=='calibrate' else ())
        for identifier,legacy,name,fields,assumptions,spatial,temporal,human in _SPECS)

class OperationRegistry:
    """Read-only registry. Runtime input cannot register or replace implementations."""
    def __init__(self):
        self._entries=MappingProxyType({d.operation_id:d for d in _definitions()})
        self._legacy=MappingProxyType({d.legacy_name:d.operation_id for d in self._entries.values()})
    def get(self, operation_id):
        if operation_id not in self._entries: raise ValueError('UNSUPPORTED_OPERATION: '+str(operation_id))
        # Reparse nested metadata so callers never receive mutable registry-owned state.
        return OperationDefinition.model_validate(self._entries[operation_id].model_dump())
    def validate(self, operation):
        op=Operation.model_validate(operation.model_dump(mode='json'))
        if op.operation not in self._legacy:raise ValueError('UNSUPPORTED_OPERATION')
        definition=self.get(self._legacy[op.operation])
        allowed={'source_asset','source_variable','operation',*definition.parameter_schema['properties']}
        if any(value is not None and key not in allowed for key,value in op.model_dump().items()):
            raise ValueError('INVALID_PARAMETERS: fields not permitted for operation')
        if op.operation=='missing' and op.sentinel is None:
            raise ValueError('INVALID_PARAMETERS: explicit missing sentinel required')
        return op
    def manifest(self):
        entries=[self.get(k).model_dump(mode='json') for k in self._entries]
        from pathlib import Path
        identity=digest({'definitions':entries,'code':{name:sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
            for name in ('operations.py','contracts.py','harmonization.py','harmonized_rasters.py','decision_ir.py')}})
        return {'registry_version':REGISTRY_VERSION,'registry_digest':identity,'executor_version':EXECUTOR_VERSION,
                'validator_version':VALIDATOR_VERSION,'constants_version':CONSTANTS_VERSION,'operations':entries}
    def execute_rows(self, operation, rows, records, sources):
        op=self.validate(operation)
        return _execute_rows(op,rows,records,sources)

REGISTRY = OperationRegistry()

def execution_identity():
    manifest=REGISTRY.manifest()
    return {k:v for k,v in manifest.items() if k!='operations'}

def convert(value, from_unit, to_unit):
    scale,offset=UNIT_CONVERSIONS[from_unit,to_unit]
    return value*scale+offset

def _execute_rows(op, rows, records, by_id):
    if op.operation == "temporal_mean":
        groups = defaultdict(list)
        for row in rows:
            r = row[0]
            day = r.start.replace(hour=0, minute=0, second=0, microsecond=0)
            if r.end > day + timedelta(days=1):
                raise ValueError("cannot aggregate an interval crossing a day boundary")
            groups[(r.longitude, r.latitude, day)].append(row)
        aggregated = []
        for (_, _, day), group in sorted(groups.items()):
            ordered = sorted(group, key=lambda x: x[0].start)
            if any(a[0].end > b[0].start for a, b in zip(ordered, ordered[1:])):
                raise ValueError("overlapping observations cannot form a daily mean")
            if any(x[1] is None for x in group):
                raise ValueError("explicitly handle missing values before aggregation")
            durations = [(x[0].end - x[0].start).total_seconds() for x in group]
            if sum(durations) != 86400 or ordered[0][0].start != day or ordered[-1][0].end != day + timedelta(days=1):
                raise ValueError("daily mean requires complete nonoverlapping daily coverage")
            mean = sum(x[1] * duration for x, duration in zip(group, durations)) / 86400
            raw = group[0][0].model_copy(update={"start": day, "end": day + timedelta(days=1), "uncertainty": None, "quality_flag": "derived_daily_mean"})
            originals = tuple(r for x in group for r in x[4])
            aggregated.append((raw, mean, "daily", group[0][3], originals, (), ()))
        return aggregated
    updated = []
    for raw, value, temporal, spatial, originals, related_sources, related_records in rows:
        if op.operation == "convert_units" and value is not None:
            scale, offset = UNIT_CONVERSIONS[(op.from_unit, op.to_unit)]
            value = value * scale + offset
        elif op.operation == "calibrate" and value is not None:
            value = value * op.scale + op.offset
        elif op.operation == "missing" and value == op.sentinel:
            value = None
        elif op.operation == "filter":
            if value is None or (op.minimum is not None and value < op.minimum) or (op.maximum is not None and value > op.maximum):
                continue
        elif op.operation == "validate" and value is not None:
            if (op.minimum is not None and value < op.minimum) or (op.maximum is not None and value > op.maximum):
                raise ValueError("value failed recipe validation")
        elif op.operation in {"join", "spatial_match"}:
            candidates = [r for r in records if r.asset_id == op.other_asset and r.start == raw.start and r.end == raw.end]
            tolerance = 0 if op.operation == "join" else op.tolerance
            matches = [r for r in candidates if abs(r.longitude - raw.longitude) <= tolerance and abs(r.latitude - raw.latitude) <= tolerance]
            if len(matches) != 1:
                raise ValueError("join/match requires exactly one aligned record; ambiguous or unmatched input")
            other = by_id[op.other_asset]
            if other.support.spatial != spatial and op.operation == "join":
                raise ValueError("exact join requires equal observational support")
            if other.rights.derivative_use is not True or other.rights.redistribution is not True:
                raise ValueError("joined source rights do not permit export")
            related_sources += (other,)
            related_records += tuple(matches)
            if op.operation == "spatial_match":
                spatial = op.target_support
        # Coordinate normalization is explicit identity for already valid WGS84 inputs.
        updated.append((raw, value, temporal, spatial, originals, related_sources, related_records))
    return updated
