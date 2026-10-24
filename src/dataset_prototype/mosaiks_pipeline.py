"""Thin composition: approved harmonization stream → MOSAIKS → dataset."""
from itertools import islice,chain
from .harmonized_rasters import authorize_context
from .mosaiks import MOSAIKSEncoder
from .embedding_dataset import write_dataset,verify_dataset


from typing import Literal
from pydantic import Field
from .contracts import Contract


class RasterLayout(Contract):
    side: int=Field(default=16,ge=4,le=32)
    grid: int=Field(default=8,ge=6,le=8)
    split_policy: Literal['native columns; one unused buffer column; train/validation/test spatial blocks']='native columns; one unused buffer column; train/validation/test spatial blocks'


def encoder_contract(spec):
    return ('mosaiks-empirical-rcf-v1','1',spec.features,
        'train-only empirical patches; ZCA; valid convolution; symmetric threshold; global mean pooling; no clipping or resizing',
        'MOSAIKS empirical random convolutional features; scientific validity requires held-out verification')


def plan_rasters(plan,spec,layout):
    from .stream_contracts import StreamPlan,EncoderSpec
    if plan.reader!='sentinel-pixel' or len(plan.bindings)!=1:raise ValueError('one native source binding required for the first raster example')
    encoder,version,dimensions,preprocessing,purpose=encoder_contract(spec)
    encoded=EncoderSpec(method='mosaiks',encoder=encoder,version=version,dimensionality=dimensions,preprocessing=preprocessing,purpose=purpose,configuration_json=spec.model_dump_json())
    result=plan.model_copy(update={'reader':'sentinel-raster','encoder':encoded,'raster_layout_json':layout.model_dump_json(),
        'question':'MOSAIKS vectors of reviewed harmonized native raster windows; no scientific resampling or clipping. '+plan.question})
    return StreamPlan.model_validate(result.model_dump(mode='json'))


def run(patches,context,spec,output):
    context=authorize_context(context)
    if context.plan.reader=='sentinel-raster':
        from .mosaiks import MOSAIKSSpec
        if MOSAIKSSpec.model_validate_json(context.plan.encoder.configuration_json)!=spec:raise ValueError('MOSAIKS settings differ from reviewed plan')
        layout=RasterLayout.model_validate_json(context.plan.raster_layout_json)
        if spec.calibration_tiles>(layout.grid//2)*layout.grid or spec.kernel_size>layout.side:raise ValueError('training reference or kernel exceeds reviewed spatial layout')
    from pathlib import Path
    import json
    root=Path(output)
    if root.exists():raise FileExistsError('embedding output already exists')
    iterator=iter(patches)
    try:
        # A bounded training prefix is retained only in memory until filters freeze.
        prefix=list(islice(iterator,spec.calibration_tiles))
        model=MOSAIKSEncoder.fit(iter(prefix),spec,context)
        return write_dataset(chain(prefix,iterator),model,context,output)
    except BaseException as error:
        if not root.exists():
            root.mkdir(parents=True)
            (root/'harmonization_context.json').write_text(context.model_dump_json(indent=2)+'\n')
            (root/'manifest.json').write_text(json.dumps({'status':'failed','stage':'filter_calibration','records':0,'error_type':type(error).__name__,'raw_data_persisted':False,'harmonized_arrays_persisted':False},indent=2)+'\n')
        raise
    finally:
        if hasattr(iterator,'close'):iterator.close()


def demo(output, *, records=32, features=128):
    """Generated diagnostics through the real harmonizer and MOSAIKS algorithm."""
    if not 32 <= records <= 1024 or records % 4:
        raise ValueError('generated demo requires 32..1024 windows in multiples of four')
    from datetime import datetime,timezone
    import numpy as np
    from .contracts import SourceResource,Variable,Support,Metadata,Rights,SemanticMapping,HarmonizationRecipe,Operation,Proposal,digest
    from .stream_contracts import StreamPlan,StreamBinding
    from .harmonized_rasters import RasterContext,harmonize_window
    from .mosaiks import MOSAIKSSpec
    when=datetime(2023,7,1,tzinfo=timezone.utc)
    variable=Variable(name='synthetic_reflectance',definition='Generated scalar diagnostic, not a provider observation',unit='1',measurement_method='seeded diagnostic generator')
    source=SourceResource(source_id='synthetic-diagnostic',dataset='generated MOSAIKS verification only',asset_id='generated-raster',version='1',uri='generator://mosaiks-demo-v1',modality='satellite',variables=(variable,),
        support=Support(bbox=(-106,39,-104,41),start=when,end=when,spatial='synthetic regular grid',temporal='instantaneous'),
        metadata=Metadata(fixture=True,description='No real scientific observations or provider data',original_identifier='generated-raster'),
        rights=Rights(license='CC0-1.0',attribution='Project-authored generated diagnostics',derivative_use=True,redistribution=True),checksum=digest({'generator':'mosaiks-demo-v1','records':records}),checksum_scope='metadata',retrieved_at=when,provenance=('generated-diagnostic-v1',))
    mapping=SemanticMapping(source_asset=source.asset_id,source_variable=variable.name,target=variable,relationship='equivalent_to',evidence=('Generated identity diagnostic',),confidence=1,review_status='approved')
    recipe=HarmonizationRecipe(recipe_id='generated-diagnostic-identity',version='1',scope='core',status='approved',author='deterministic-diagnostic',mappings=(mapping,),
        operations=(Operation(operation='map_variable',source_variable=variable.name,target_variable=variable.name),),proposals=(Proposal(role='harmonization',rationale='Identity only on generated data',evidence=('diagnostic',)),))
    plan=StreamPlan(question='Diagnostic pipeline, no scientific validation',reader='test-generator',bindings=(StreamBinding(binding_id='synthetic',source=source,source_variable=variable.name,target=variable,longitude=-105,latitude=40),))
    context=RasterContext(plan=plan,recipe=recipe)
    spec=MOSAIKSSpec(channels=(variable.name,),units=('1',),features=features,calibration_tiles=8,input_scale=32)
    def outputs():
        rng=np.random.default_rng(91)
        step=min(.001,.9/records)
        for i in range(records):
            split='train' if i<records//2 else 'validation' if i<3*records//4 else 'test'
            value=rng.uniform(.05,.6)+rng.normal(0,rng.uniform(.01,.08),(16,16))
            lineage={'bbox':[-105+i*step,40,-105+(i+1)*step,40.0005],'native_crs':'synthetic-grid',
                'native_window':[0,i*16,16,16],'source_assets':[source.asset_id],
                'datetime_start':when.isoformat(),'datetime_end':when.isoformat(),'quality_policy':'generated finite diagnostics; no satellite mask'}
            yield harmonize_window({(source.asset_id,variable.name):value},context=context,patch_id=f'generated-{i}',lineage=lineage,split=split,spatial_group=f'generated-block-{i}')
    manifest=run(outputs(),context,spec,output)
    from pathlib import Path
    report=verify_dataset(output,Path(output)/'verification.json')
    return manifest,report
