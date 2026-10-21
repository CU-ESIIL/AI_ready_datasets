"""Bounded raster assembly from immutable harmonization outputs, never raw DN."""
from pydantic import model_serializer
from .review_contracts import ReviewReport
from .contracts import Contract, HarmonizedObservation, HarmonizationRecipe, HumanDecision, digest
from .stream_contracts import StreamPlan, ConsensusReport
from .streaming import preflight
from .operations import REGISTRY, convert, execution_identity


class RasterContext(Contract):
    plan: StreamPlan
    recipe: HarmonizationRecipe
    human: HumanDecision | None=None
    consensus: ConsensusReport | None=None
    evidence_review: ReviewReport | None=None

    @model_serializer(mode='wrap')
    def serialize(self, handler):
        data=handler(self)
        if self.evidence_review is None:data.pop('evidence_review',None)
        return data


def authorize_context(context):
    context=RasterContext.model_validate(context.model_dump(mode='json'))
    preflight(context.plan,context.recipe,context.human,context.consensus,context.evidence_review)
    return context


def assemble_patch(cells,*,context,patch_id,channels,units,height,width,lineage,split,spatial_group,verification_target=None,target_name=None,target_kind=None):
    """Consume explicit (row, column, HarmonizedObservation) cells, <=128²/band.

    No spatial interpolation, scientific conversion, implicit joins or reads.
    Input channel order comes from canonical variable names, not file order.
    """
    import numpy as np
    from .mosaiks import HarmonizedRasterPatch,array_digest
    context=authorize_context(context)
    if not 1<=height<=128 or not 1<=width<=128 or not 1<=len(channels)<=16 or len(channels)!=len(units) or len(set(channels))!=len(channels):
        raise ValueError('bounded, unique channel layout required')
    values=np.empty((len(channels),height,width),dtype=np.float32)
    seen=np.zeros(values.shape,dtype=bool);coordinates={};ids=[];when=None
    allowed={(m.source_asset,m.source_variable):m.target for m in context.recipe.mappings}
    expected_qa=preflight(context.plan,context.recipe,context.human,context.consensus,context.evidence_review)
    iterator=iter(cells)
    count=0
    try:
        for row,col,observation in iterator:
            count+=1
            if count>values.size:raise ValueError('too many harmonized cells')
            if not isinstance(observation,HarmonizedObservation):raise TypeError('raster assembly requires harmonized observations')
            o=HarmonizedObservation.model_validate(observation.model_dump(mode='json'))
            if o.observation_id!=digest(o.model_dump(mode='json',exclude={'observation_id'})) or o.provenance.recipe!=context.recipe or o.provenance.human!=context.human or o.provenance.qa!=expected_qa or o.provenance.context_sources!=context.plan.resources:
                raise ValueError('harmonized cell identity/review lineage mismatch')
            source=o.provenance.source
            if source not in context.plan.resources or allowed.get((source.asset_id,o.source_variable)) is None or o.track is not None:
                raise ValueError('cell source/track does not match reviewed raster context')
            if o.variable not in channels:raise ValueError('unexpected canonical channel')
            channel=channels.index(o.variable)
            if o.unit!=units[channel] or o.value is None or not 0<=row<height or not 0<=col<width or seen[channel,row,col]:
                raise ValueError('missing, duplicate, out-of-range or incompatible harmonized cell')
            location=(o.longitude,o.latitude)
            if (row,col) in coordinates and coordinates[row,col]!=location:raise ValueError('channels have different pixel coordinates')
            coordinates[row,col]=location
            acquisition=(o.datetime_start,o.datetime_end)
            if when is not None and when!=acquisition:raise ValueError('channels/time do not align')
            when=acquisition
            values[channel,row,col]=o.value;seen[channel,row,col]=True;ids.append(o.observation_id)
    finally:
        if hasattr(iterator,'close'):iterator.close()
    if not seen.all():raise ValueError('incomplete harmonized tile')
    lineage={**lineage,'harmonization_status':'approved','recipe_digest':digest(context.recipe),
        'context_digest':digest(context),'cell_observation_ids_digest':digest(ids),'cell_count':count,
        'datetime_start':when[0].isoformat(),'datetime_end':when[1].isoformat()}
    observation_digest=digest({'values':array_digest(values),'recipe_digest':digest(context.recipe),'lineage':lineage})
    return HarmonizedRasterPatch(values,patch_id,tuple(channels),tuple(units),digest(context.recipe),observation_digest,lineage,split,spatial_group,
        verification_target,target_name,target_kind)


def harmonize_window(arrays,*,context,patch_id,lineage,split,spatial_group):
    """Deterministic raster counterpart of the scalar harmonizer.

    Source adapter supplies arrays keyed by (asset_id, variable). Only approved
    scalar operations are vectorized; shape/support must already match exactly.
    """
    import numpy as np
    from .mosaiks import HarmonizedRasterPatch,array_digest
    context=authorize_context(context)
    if len(arrays)!=1:raise NotImplementedError('first vectorized raster slice supports one canonical band; use reviewed cell assembly for aligned multichannel outputs')
    operations=context.recipe.operations
    allowed={'validate','missing','map_variable','calibrate','convert_units','normalize_coordinates'}
    for operation in operations: REGISTRY.validate(operation)
    if any(o.operation not in allowed for o in operations):raise ValueError('unsupported raster harmonization operation')
    if set(arrays)!={(m.source_asset,m.source_variable) for m in context.recipe.mappings}:raise ValueError('raster inputs differ from reviewed mappings')
    channels=[];units=[];outputs=[];raw_hashes=[]
    for mapping in context.recipe.mappings:
        raw=np.asarray(arrays[mapping.source_asset,mapping.source_variable])
        if raw.ndim!=2 or not 1<=min(raw.shape) or max(raw.shape)>128 or not np.isfinite(raw).all():raise ValueError('invalid bounded source raster')
        raw_hashes.append(array_digest(raw))
        value=raw.astype(np.float64)
        for op in operations:
            if op.source_variable!=mapping.source_variable or op.source_asset not in {None,mapping.source_asset}:continue
            if op.operation=='calibrate':value=value*op.scale+op.offset
            elif op.operation=='convert_units':
                value=convert(value,op.from_unit,op.to_unit)
            elif op.operation=='missing' and np.any(value==op.sentinel):raise ValueError('missing raster cells require an explicit supported policy')
            elif op.operation=='validate':
                if (op.minimum is not None and np.any(value<op.minimum)) or (op.maximum is not None and np.any(value>op.maximum)):raise ValueError('raster failed reviewed bounds')
        channels.append(mapping.target.name);units.append(mapping.target.unit);outputs.append(value)
    if len(set(channels))!=len(channels) or len({x.shape for x in outputs})!=1:raise ValueError('channels are duplicate or spatially unaligned')
    for key in ('bbox','native_crs','native_window','source_assets','datetime_start','datetime_end','quality_policy'):
        if key not in lineage:raise ValueError('raster support/quality lineage missing: '+key)
    from datetime import datetime
    bbox=lineage['bbox'];window=lineage['native_window']
    if len(bbox)!=4 or not (-180<=bbox[0]<bbox[2]<=180 and -90<=bbox[1]<bbox[3]<=90):raise ValueError('valid geographic raster bounds required')
    if len(window)!=4 or min(window)<0 or tuple(window[2:])!=outputs[0].shape:raise ValueError('native window differs from harmonized shape')
    for source in context.plan.resources:
        extent=source.support.bbox
        if not (extent[0]<=bbox[0]<bbox[2]<=extent[2] and extent[1]<=bbox[1]<bbox[3]<=extent[3]):raise ValueError('raster outside reviewed source coverage')
        if (datetime.fromisoformat(lineage['datetime_start']),datetime.fromisoformat(lineage['datetime_end']))!=(source.support.start,source.support.end):raise ValueError('raster time differs from reviewed acquisition')
    if set(lineage['source_assets'])!={m.source_asset for m in context.recipe.mappings}:raise ValueError('raster source lineage mismatch')
    values=np.stack(outputs)
    lineage={**lineage,'harmonization_status':'approved','recipe_digest':digest(context.recipe),'context_digest':digest(context),
        'source_window_evidence_digest':digest({'channels':raw_hashes,'quality':lineage.get('quality_evidence_digest')}),'raster_executor':'registered-raster-v2','execution_identity':execution_identity(),'resampling':'none for scientific values'}
    observation_digest=digest({'values':array_digest(values),'recipe_digest':digest(context.recipe),'lineage':lineage})
    # Quantity-retention diagnostic, explicitly not independent ground truth.
    return HarmonizedRasterPatch(values,patch_id,tuple(channels),tuple(units),digest(context.recipe),observation_digest,lineage,split,spatial_group,
        float(values[0].std()),'std_first_harmonized_channel','derived-diagnostic')
