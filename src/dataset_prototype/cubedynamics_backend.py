"""Bounded adapter to external ESIIL CubeDynamics; never accepts Python from a model."""
from dataclasses import dataclass
from hashlib import sha256
from datetime import timezone
from importlib.metadata import version, PackageNotFoundError
from math import prod
from typing import Any
from .contracts import BackendOperation, HarmonizationRecipe, HumanDecision, SourceResource, digest
from .cube_contracts import (CubeConfiguration, TransformationResult, TransformationChanges, CUBE_VERSION)
from .cube_specs import SPECS

class CubeError(ValueError):
    def __init__(self,code,message):
        self.code=code
        super().__init__(code+': '+message)

@dataclass(frozen=True)
class CubeProduct:
    value: Any
    transformations: tuple[TransformationResult,...]


def context_digest(configuration,sources):
    from .operations import execution_identity
    return digest({'configuration':configuration.model_dump(mode='json'),
        'sources':[s.model_dump(mode='json') for s in sorted(sources,key=lambda s:s.asset_id)],
        'execution_identity':execution_identity()})


def validate_step(step):
    step=BackendOperation.model_validate(step.model_dump(mode='json'))
    if step.operation_id not in SPECS:raise CubeError('UNSUPPORTED_OPERATION',step.operation_id)
    expected={key:entry['const'] for key,entry in SPECS[step.operation_id][2].items()}
    if step.parameters!=expected:raise CubeError('INVALID_PARAMETERS','operation parameters must be registered references/enums')
    return step


def _arrays(cube):
    import xarray as xr
    return list(cube.data_vars.values()) if isinstance(cube,xr.Dataset) else [cube]


def _lazy(cube):
    from dask.base import is_dask_collection
    return any(is_dask_collection(a.data) for a in _arrays(cube))


def _guard(cube,guards,*,output=False):
    arrays=_arrays(cube)
    size=sum(int(a.size)*int(a.dtype.itemsize) for a in arrays)
    limit=guards.max_output_bytes if output else guards.max_input_bytes
    if size>limit or any(n>guards.max_axis or n<1 for n in cube.sizes.values()):
        raise CubeError('RESOURCE_LIMIT','bounded cube shape/byte limit exceeded')
    count=0;tasks=0
    for a in arrays:
        if a.chunks is not None:
            count+=prod(len(c) for c in a.chunks)
            tasks+=len(a.data.__dask_graph__())
    if count>guards.max_chunks or tasks>guards.max_tasks:
        raise CubeError('RESOURCE_LIMIT','chunk/task graph limit exceeded')


def _metadata(cube):
    import numpy as np
    variables={str(a.name or 'value'):str(a.attrs.get('units','')) for a in _arrays(cube)}
    coordinates={k:{'size':int(c.size),'digest':digest(c.values.astype(str).tolist()),
                    'first':str(c.values[0]),'last':str(c.values[-1])} for k,c in cube.coords.items() if c.ndim==1 and c.size}
    resolution={d:float(abs(np.diff(cube[d].values.astype(float))[0])) if cube.sizes.get(d,0)>1 else (cube.attrs.get('native_spatial_resolution') or [None,None])[i] for i,d in enumerate(('x','y'))}
    return {'dimensions':dict(cube.sizes),'variables':variables,'coordinates':coordinates,
        'crs':str(cube.attrs.get('crs','')),'spatial_resolution':resolution,
        'spatial_support':cube.attrs.get('scientific_spatial_support'),
        'temporal_resolution':cube.attrs.get('temporal_resolution'),
        'temporal_support':{k:cube.attrs.get(k) for k in ('temporal_support_known','temporal_support_type','temporal_label_convention','temporal_reference_timezone','temporal_start_offset','temporal_end_offset')}}


def _support(cube,spec):
    result=cube.copy(deep=False);result.attrs=dict(cube.attrs)
    result.attrs['scientific_spatial_support']=spec.spatial_support
    result.attrs['native_spatial_resolution']=spec.spatial_resolution
    known=spec.temporal_support!='unknown'
    result.attrs.update({'temporal_support_known':int(known),
        'temporal_support_type':'instant' if spec.temporal_support=='instantaneous' else 'interval' if known else 'unknown',
        'temporal_label_convention':'instant' if spec.temporal_support=='instantaneous' else 'interval_start',
        'temporal_reference_timezone':'UTC','temporal_start_offset':'0s',
        'temporal_end_offset':str(int(round((spec.interval_seconds or 0)*1e9)))+'ns',
        'temporal_resolution':str(spec.temporal_resolution_seconds)+'s' if spec.temporal_resolution_seconds is not None else None,
        'temporal_support_evidence':'reviewed CubeConfiguration; source context digest retained'})
    return result


def _select(cube,*,variable):
    import xarray as xr
    if isinstance(cube,xr.Dataset):
        result=cube[variable].copy(deep=False);result.attrs={**cube.attrs,**result.attrs}
        return result
    if 'band' in cube.dims:return cube.sel(band=[variable])
    if str(cube.name)!=variable:raise CubeError('INVALID_PARAMETERS','requested variable absent')
    return cube


def _subset(cube,*,window):
    return cube.isel(time=slice(window[0],window[1]),y=slice(window[2],window[3]),x=slice(window[4],window[5]))


def _mask(cube,*,quality,classes):
    import xarray as xr
    if isinstance(quality,xr.Dataset):quality=quality[next(iter(quality.data_vars))]
    # Select coordinates exactly; never interpolate quality classes.
    quality=quality.sel({d:cube[d] for d in ('time','y','x')})
    return cube.where(quality.isin(classes))


class CubeDynamicsBackend:
    def capabilities(self):
        from .operations import REGISTRY
        return {'backend':'cubedynamics','backend_version':CUBE_VERSION,
            'operations':[d for d in REGISTRY.manifest()['operations'] if d['backend']=='cubedynamics']}

    def validate(self,recipe,sources,configuration,inputs,human,*,raster_context=None):
        try:
            import numpy as np
            import xarray as xr
            from pyproj import CRS, Transformer
        except ImportError as error:raise CubeError('BACKEND_UNAVAILABLE','install the cubedynamics extra under Python 3.12') from error
        from .harmonization import authorize
        recipe=HarmonizationRecipe.model_validate(recipe.model_dump(mode='json'))
        configuration=CubeConfiguration.model_validate(configuration.model_dump(mode='json'))
        sources=tuple(SourceResource.model_validate(s.model_dump(mode='json')) for s in sources)
        human=HumanDecision.model_validate(human.model_dump(mode='json')) if human is not None else None
        if not recipe.backend_operations:raise CubeError('INVALID_PARAMETERS','no backend operations')
        for step in recipe.backend_operations:validate_step(step)
        if recipe.backend_context_digest!=context_digest(configuration,sources):
            raise CubeError('PRECONDITION_FAILED','source/configuration/implementation binding changed')
        if human is None or human.status!='approved' or human.recipe_digest!=digest(recipe):
            raise CubeError('NEEDS_HUMAN_REVIEW','exact-recipe human decision required')
        try:authorize(recipe,sources,human)
        except ValueError as error:raise CubeError('PRECONDITION_FAILED',str(error)) from error
        if not all(s.metadata.fixture for s in sources):
            if raster_context is None or raster_context.recipe!=recipe:
                raise CubeError('NEEDS_HUMAN_REVIEW','real data requires matching reviewed raster context')
            from .harmonized_rasters import authorize_context
            require_frozen_consensus(recipe,raster_context.plan,raster_context.consensus)
            authorize_context(raster_context)
        if set(inputs)!=set(configuration.inputs) or 'primary' not in inputs or set(inputs)-{'primary','quality','reference'}:
            raise CubeError('PRECONDITION_FAILED','exact declared input bindings required')
        by_id={s.asset_id:s for s in sources}
        try:total_bytes=sum(int(a.size)*int(a.dtype.itemsize) for cube in inputs.values() for a in _arrays(cube))
        except (AttributeError,TypeError):raise CubeError('PRECONDITION_FAILED','xarray arrays required')
        if total_bytes>configuration.guards.max_input_bytes:raise CubeError('RESOURCE_LIMIT','total input byte estimate exceeds guard')
        for name,cube in inputs.items():
            spec=configuration.inputs[name]
            if not isinstance(cube,(xr.DataArray,xr.Dataset)):
                raise CubeError('PRECONDITION_FAILED','xarray DataArray/Dataset required')
            _guard(cube,configuration.guards)
            if any(a.dtype.kind not in 'biuf' for a in _arrays(cube)):raise CubeError('PRECONDITION_FAILED','numeric/bool arrays required')
            if not {'time','y','x'}<=set(cube.dims) or set(cube.dims)-{'time','y','x','band'}:
                raise CubeError('PRECONDITION_FAILED','explicit time/y/x and optional band dimensions required')
            if not set(spec.resource_ids)<=set(by_id):raise CubeError('PRECONDITION_FAILED','unknown source resource')
            if not cube.attrs.get('crs') or not spec.crs:
                raise CubeError('PRECONDITION_FAILED','native CRS required')
            try:
                if CRS.from_user_input(cube.attrs['crs'])!=CRS.from_user_input(spec.crs):raise ValueError('CRS mismatch')
            except Exception as error:raise CubeError('PRECONDITION_FAILED','invalid or mismatched CRS') from error
            for d in ('x','y','time'):
                if d not in cube.coords or cube[d].dims!=(d,):raise CubeError('PRECONDITION_FAILED','one-dimensional native coordinates required')
                coord=cube[d].values
                if len(coord)<1:raise CubeError('PRECONDITION_FAILED','empty coordinate')
                if d=='time':
                    if coord.dtype.kind!='M' or np.isnat(coord).any():raise CubeError('PRECONDITION_FAILED','datetime coordinate required')
                    delta=np.diff(coord.astype('datetime64[ns]').astype('int64'))
                    if np.any(delta<=0):raise CubeError('PRECONDITION_FAILED','unique increasing time labels required')
                    span=float((coord[-1]-coord[0])/np.timedelta64(1,'s'))
                    if span>configuration.guards.max_time_seconds:raise CubeError('RESOURCE_LIMIT','time extent exceeds guard')
                    for resource_id in spec.resource_ids:
                        support=by_id[resource_id].support
                        start=np.datetime64(support.start.astimezone(timezone.utc).replace(tzinfo=None),'ns')
                        end=np.datetime64(support.end.astimezone(timezone.utc).replace(tzinfo=None),'ns')
                        if coord[0]<start or coord[-1]+np.timedelta64(int(round((spec.interval_seconds or 0)*1e9)),'ns')>end:raise CubeError('PRECONDITION_FAILED','time outside source support')
                else:
                    if coord.dtype.kind not in 'iuf' or not np.isfinite(coord).all():raise CubeError('PRECONDITION_FAILED','finite numeric spatial coordinates required')
                    delta=np.diff(coord.astype(float))
                    resolution=spec.spatial_resolution[0 if d=='x' else 1]
                    if len(delta) and (not (np.all(delta>0) or np.all(delta<0)) or not np.allclose(abs(delta),resolution)):
                        raise CubeError('PRECONDITION_FAILED','coordinate resolution differs from reviewed input')
            transform=Transformer.from_crs(spec.crs,'EPSG:4326',always_xy=True)
            rx,ry=spec.spatial_resolution
            xx=[float(cube.x.min())-rx/2,float(cube.x.max())+rx/2]
            yy=[float(cube.y.min())-ry/2,float(cube.y.max())+ry/2]
            lon,lat=transform.transform([xx[0],xx[0],xx[1],xx[1]],[yy[0],yy[1],yy[0],yy[1]])
            for resource_id in spec.resource_ids:
                bbox=by_id[resource_id].support.bbox
                if min(lon)<bbox[0] or max(lon)>bbox[2] or min(lat)<bbox[1] or max(lat)>bbox[3]:
                    raise CubeError('PRECONDITION_FAILED','native window lies outside source spatial coverage')
            actual={str(a.name or 'value'):str(a.attrs.get('units','')) for a in _arrays(cube)}
            if actual!=spec.variable_units:raise CubeError('PRECONDITION_FAILED','variable/unit metadata differs from reviewed input')
            allowed={}
            for resource_id in spec.resource_ids:
                if spec.stage=='source':allowed.update({v.name:v.unit for v in by_id[resource_id].variables})
                else:allowed.update({m.target.name:m.target.unit for m in recipe.mappings if m.source_asset==resource_id})
            if any(allowed.get(k)!=v for k,v in actual.items()):raise CubeError('PRECONDITION_FAILED','quantity/unit differs from declared scientific stage')
        ids={step.operation_id for step in recipe.backend_operations}
        primary=inputs['primary'];spec=configuration.inputs['primary']
        if 'cubedynamics.select' in ids and (configuration.variable is None or (configuration.variable not in spec.variable_units and configuration.variable not in primary.coords.get('band',[]))):
            raise CubeError('INVALID_PARAMETERS','requested variable absent from reviewed input')
        if 'cubedynamics.subset' in ids:
            w=configuration.window
            if w is None or any(not 0<=w[i]<w[i+1]<=primary.sizes[d] for i,d in zip((0,2,4),('time','y','x'))):
                raise CubeError('INVALID_PARAMETERS','half-open window outside source')
        if 'cubedynamics.month_filter' in ids and not configuration.months:raise CubeError('INVALID_PARAMETERS','explicit months required')
        if 'cubedynamics.quality_mask' in ids:
            if 'quality' not in inputs or not configuration.inputs['quality'].mask_definition or not configuration.allowed_quality_classes:
                raise CubeError('NEEDS_EVIDENCE','documented quality mask and class predicate required')
            if any(a.dtype.kind not in 'biu' for a in _arrays(inputs['quality'])):raise CubeError('PRECONDITION_FAILED','categorical integer/bool quality mask required')
            if configuration.inputs['quality'].crs!=spec.crs:raise CubeError('PRECONDITION_FAILED','quality CRS differs; no implicit resampling')
            if len(configuration.inputs['quality'].variable_units)!=1:raise CubeError('INVALID_PARAMETERS','one quality variable required')
        if ids & {'cubedynamics.align_time','cubedynamics.align_nearest'}:
            if 'reference' not in inputs:raise CubeError('NEEDS_EVIDENCE','explicit target reference required')
            reference=inputs['reference'];other=configuration.inputs['reference']
            if CRS.from_user_input(spec.crs)!=CRS.from_user_input(other.crs):raise CubeError('PRECONDITION_FAILED','alignment is not reprojection')
            if spec.variable_units!=other.variable_units:raise CubeError('PRECONDITION_FAILED','incompatible quantities/units')
            if not np.array_equal(primary.time.values,reference.time.values):raise CubeError('PRECONDITION_FAILED','exact time labels required; no temporal interpolation')
            if 'cubedynamics.align_nearest' in ids and not configuration.target_spatial_support:raise CubeError('NEEDS_EVIDENCE','explicit target support and justification required')
            for d in ('x','y'):
                if reference[d].min()<primary[d].min() or reference[d].max()>primary[d].max():raise CubeError('PRECONDITION_FAILED','target grid extends outside source centers')
        if 'cubedynamics.temporal_mean' in ids:
            if spec.temporal_support!='equal_intervals' or not configuration.target_temporal_support:
                raise CubeError('NEEDS_EVIDENCE','mean requires documented interval duration and target support')
            delta=np.diff(primary.time.values.astype('datetime64[ns]').astype('int64'))
            if len(delta)<1 or not np.all(delta==int(round(spec.interval_seconds*1e9))) or spec.temporal_resolution_seconds!=spec.interval_seconds:
                raise CubeError('PRECONDITION_FAILED','mean requires complete equal-duration nonoverlapping intervals')

    def execute(self,recipe,sources,configuration,inputs,human,*,raster_context=None):
        self.validate(recipe,sources,configuration,inputs,human,raster_context=raster_context)
        try:
            if version('cubedynamics')!=CUBE_VERSION:raise CubeError('PRECONDITION_FAILED','untested CubeDynamics version')
        except PackageNotFoundError as error:raise CubeError('BACKEND_UNAVAILABLE','install the cubedynamics extra') from error
        import cubedynamics as cd
        import numpy as np
        from .operations import execution_identity
        dependencies={name:version(name) for name in ('cubedynamics','xarray','dask','numpy','pandas','scipy','pyproj')}
        current=_support(inputs['primary'],configuration.inputs['primary']);results=[]
        for step in recipe.backend_operations:
            # Revalidate ordered-stage preconditions after earlier subsets/masks.
            if step.operation_id=='cubedynamics.temporal_mean':
                deltas=np.diff(current.time.values.astype('datetime64[ns]').astype('int64'))
                if len(deltas)<1 or not np.all(deltas==int(round(configuration.inputs['primary'].interval_seconds*1e9))):
                    raise CubeError('PRECONDITION_FAILED','earlier operations broke complete equal-interval support')
            if step.operation_id in {'cubedynamics.align_time','cubedynamics.align_nearest'}:
                reference=inputs['reference']
                if not np.array_equal(current.time.values,reference.time.values):
                    raise CubeError('PRECONDITION_FAILED','earlier operations changed exact temporal alignment')
                for axis in ('x','y'):
                    if reference[axis].min()<current[axis].min() or reference[axis].max()>current[axis].max():
                        raise CubeError('PRECONDITION_FAILED','target outside current subset')
            before=_metadata(current);api=SPECS[step.operation_id][1]
            # The dispatch is written here, never selected by attribute name or expression.
            if step.operation_id=='cubedynamics.select':
                verb=cd.verbs.apply(_select,variable=configuration.variable);resolved={'variable':configuration.variable}
            elif step.operation_id=='cubedynamics.subset':
                verb=cd.verbs.apply(_subset,window=configuration.window);resolved={'time_y_x_window':configuration.window}
            elif step.operation_id=='cubedynamics.month_filter':
                verb=cd.verbs.month_filter(configuration.months);resolved={'months':configuration.months}
            elif step.operation_id=='cubedynamics.quality_mask':
                verb=cd.verbs.apply(_mask,quality=inputs['quality'],classes=configuration.allowed_quality_classes)
                resolved={'quality_source':configuration.inputs['quality'].resource_ids,'classes':configuration.allowed_quality_classes,'definition':configuration.inputs['quality'].mask_definition}
            elif step.operation_id=='cubedynamics.temporal_mean':
                verb=cd.verbs.mean(dim='time',keep_dim=False,skipna=False)
                resolved={'dim':'time','keep_dim':False,'skipna':False,'statistic':'mean','source_interval_seconds':configuration.inputs['primary'].interval_seconds,'target_support':configuration.target_temporal_support}
            elif step.operation_id=='cubedynamics.align_time':
                verb=cd.verbs.align_time(_support(inputs['reference'],configuration.inputs['reference']),mode='require_exact_support')
                resolved={'target_resource_ids':configuration.inputs['reference'].resource_ids,'mode':'require_exact_support'}
            else:
                verb=cd.verbs.align_cube(like=inputs['reference'],spatial_method='nearest',temporal_method='nearest',tolerance='0s')
                resolved={'target_resource_ids':configuration.inputs['reference'].resource_ids,'spatial_method':'nearest','temporal_method':'nearest','tolerance':'0s','source_resolution':configuration.inputs['primary'].spatial_resolution,'target_resolution':configuration.inputs['reference'].spatial_resolution,'target_support':configuration.target_spatial_support}
            try:
                pipe=cd.pipe(current)|verb
                value=pipe.unwrap()
            except (ValueError,TypeError,KeyError) as error:raise CubeError('PRECONDITION_FAILED',str(error)) from error
            if step.operation_id=='cubedynamics.temporal_mean':
                value=value.expand_dims(time=[current.time.values[0]])
                value.attrs.update({'temporal_support_known':1,'temporal_support_type':'interval',
                    'temporal_start_offset':'0s','temporal_end_offset':str(int(round(len(current.time)*configuration.inputs['primary'].interval_seconds*1e9)))+'ns',
                    'temporal_resolution':str(configuration.target_temporal_resolution_seconds)+'s' if configuration.target_temporal_resolution_seconds is not None else None,
                    'scientific_temporal_support':configuration.target_temporal_support})
            if step.operation_id=='cubedynamics.align_nearest':
                value.attrs['scientific_spatial_support']=configuration.target_spatial_support
                value.attrs['native_spatial_resolution']=configuration.inputs['reference'].spatial_resolution
            _guard(value,configuration.guards,output=True)
            if _lazy(current) and not _lazy(value):raise CubeError('PRECONDITION_FAILED','operation unexpectedly materialized lazy values')
            after=_metadata(value)
            if before['crs']!=after['crs'] or sorted(before['variables'].values())!=sorted(after['variables'].values()):
                raise CubeError('PRECONDITION_FAILED','operation unexpectedly changed units/CRS')
            flags=SPECS[step.operation_id]
            changes=TransformationChanges(values=flags[3],spatial_support=before['spatial_support']!=after['spatial_support'],
                spatial_resolution=before['spatial_resolution']!=after['spatial_resolution'],
                temporal_support=before['temporal_support']!=after['temporal_support'],
                temporal_resolution=before['temporal_resolution']!=after['temporal_resolution'],aggregation=step.operation_id=='cubedynamics.temporal_mean',
                extent=any(before['coordinates'].get(axis)!=after['coordinates'].get(axis) for axis in ('time','x','y')))
            provenance={'recipe_digest':digest(recipe),'human_decision_digest':digest(human),
                'source_metadata_digests':[digest(s) for s in sources],'configuration_digest':digest(configuration),
                'execution_identity':execution_identity(),'upstream_api':api,
                'upstream_trace':[{'index':t.index,'verb':t.verb} for t in pipe.semantic_trace],
                'evidence':configuration.evidence,'scientific_justification':configuration.scientific_justification,
                'change_scope':'operation effects; metadata differences measured; lazy pixel differences not evaluated',
                'previous_transformations':tuple(r.output_resource_id for r in results)}
            if not _lazy(value):
                if any(np.isinf(a.values).any() for a in _arrays(value)):
                    raise CubeError('EXECUTION_FAILED','infinite output values are unsupported')
                provenance.update(window_evidence_hashes={str(a.name):sha256(np.asarray(a.values).tobytes()).hexdigest() for a in _arrays(value)},
                    checksum_scope='in-memory output window only; not complete remote asset')
            fields=dict(operation_id=step.operation_id,operation_version=step.operation_version,
                input_resource_ids=tuple(dict.fromkeys(a for spec in configuration.inputs.values() for a in spec.resource_ids)),
                backend_version=CUBE_VERSION,dependency_versions=dependencies,parameters=step.parameters,resolved_parameters=resolved,
                input_metadata=before,output_metadata=after,changes=changes.model_dump(mode='json'),lazy=_lazy(value),materialized=not _lazy(value),
                status='LAZY_PLAN' if _lazy(value) else 'EXECUTED',validation_results=('structural/scientific preflight passed','resource guards passed','laziness preserved'),provenance=provenance)
            results.append(TransformationResult(output_resource_id='cube:'+digest(fields),**fields));current=value
        if configuration.materialize:
            # Explicitly materialize only the bounded final graph, never the original full source.
            _guard(current,configuration.guards,output=True)
            current=current.compute(scheduler='single-threaded')
            if any(np.isinf(a.values).any() for a in _arrays(current)):raise CubeError('EXECUTION_FAILED','infinite output values are unsupported')
            hashes={str(a.name):sha256(np.asarray(a.values).tobytes()).hexdigest() for a in _arrays(current)}
            if results:
                last=results[-1];provenance={**last.provenance,'materialization':'explicit bounded final graph',
                    'window_evidence_hashes':hashes,'checksum_scope':'materialized final window only; not complete remote asset'}
                fields=last.model_dump(mode='json',exclude={'output_resource_id'});fields.update(lazy=False,materialized=True,status='EXECUTED',provenance=provenance)
                results[-1]=TransformationResult(output_resource_id='cube:'+digest(fields),**fields)
        return CubeProduct(current,tuple(results))


def transform_raster_window(values,*,context,lineage):
    """Bridge calibrated bounded windows into CD and back to the harmonized raster contract.

    First representation path preserves every pixel, band, acquisition and layout.
    Changed support/extent requires a separate reviewed raster-layout implementation.
    """
    import numpy as np
    import xarray as xr
    configuration=context.cube_configuration
    permitted={'cubedynamics.select','cubedynamics.subset','cubedynamics.month_filter'}
    if configuration is None or set(configuration.inputs)!={'primary'} or any(s.operation_id not in permitted for s in context.recipe.backend_operations):
        raise CubeError('PRECONDITION_FAILED','raster bridge permits reviewed one-input selection/subset/calendar operations only')
    if values.shape[0]!=1:raise CubeError('PRECONDITION_FAILED','first CubeDynamics raster bridge requires one canonical band')
    _,height,width=values.shape
    if configuration.window not in (None,(0,1,0,height,0,width)):
        raise CubeError('PRECONDITION_FAILED','changed raster extent needs new layout/support bridge')
    if configuration.variable not in (None,context.recipe.mappings[0].target.name):
        raise CubeError('PRECONDITION_FAILED','canonical band cannot change in representation bridge')
    if not configuration.materialize:raise CubeError('PRECONDITION_FAILED','bounded encoder handoff requires explicit materialization intent')
    transform=lineage.get('native_transform')
    if transform is None or len(transform)!=6 or transform[1]!=0 or transform[3]!=0:
        raise CubeError('PRECONDITION_FAILED','explicit unrotated native affine transform required')
    a,b,c,d,e,f=transform;row,col,_,_=lineage['native_window']
    x=c+a*(col+np.arange(width)+.5);y=f+e*(row+np.arange(height)+.5)
    when=np.datetime64(lineage['datetime_start'].replace('+00:00',''),'ns')
    target=context.recipe.mappings[0].target
    cube=xr.Dataset({target.name:xr.DataArray(values[0][None,:,:],dims=('time','y','x'),
        coords={'time':[when],'y':y,'x':x},attrs={'units':target.unit})},attrs={'crs':lineage['native_crs']})
    product=CubeDynamicsBackend().execute(context.recipe,context.plan.resources,configuration,{'primary':cube},context.human,raster_context=context)
    result=product.value
    if isinstance(result,xr.Dataset):result=result[target.name]
    result=result.transpose('time','y','x')
    if result.shape!=(1,height,width) or not np.array_equal(result.x,x) or not np.array_equal(result.y,y) or not np.array_equal(result.time,[when]):
        raise CubeError('PRECONDITION_FAILED','CubeDynamics changed reviewed raster layout/support')
    return result.values[0][None,:,:],tuple(t.model_dump(mode='json') for t in product.transformations)


def require_frozen_consensus(recipe,plan,report):
    """Metadata-only gate, callable before any native reader opens."""
    from .contracts import recipe_content_digest
    from .stream_contracts import REVIEWERS
    if plan.reader!='sentinel-raster':raise CubeError('PRECONDITION_FAILED','real CubeDynamics streaming currently requires the verified Sentinel raster path')
    if report is None or report.status!='consensus' or report.plan_digest!=digest(plan) or report.recipe_content_digest!=recipe_content_digest(recipe) or report.unresolved:
        raise CubeError('NEEDS_HUMAN_REVIEW','matching frozen four-specialist/QA consensus required')
    if len(report.votes)!=len(REVIEWERS) or {role for role,_ in report.votes}!=set(REVIEWERS) or any(v.decision!='agree' or v.concerns for _,v in report.votes):
        raise CubeError('NEEDS_HUMAN_REVIEW','all four specialists and QA must agree on the frozen backend recipe')
