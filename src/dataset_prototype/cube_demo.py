"""Generated Sentinel-like windows → reviewed harmonization → real CubeDynamics → MOSAIKS."""
from datetime import datetime,timezone
from pathlib import Path
import json
from .contracts import (SourceResource,Variable,SemanticMapping,HarmonizationRecipe,Operation,
    Proposal,HumanDecision,digest)
from .cube_contracts import CubeConfiguration,CubeInput
from .cube_ir import capabilities,selection_schema,compile_decision
from .decision_ir import RecipeDecision,SelectDecision,FixtureDecisionModel
from .stream_contracts import StreamPlan,StreamBinding
from .harmonized_rasters import RasterContext,harmonize_window


def context():
    root=Path(__file__).resolve().parents[2]
    template=SourceResource.model_validate_json((root/'data/fixtures/semantics/sentinel_source.json').read_text())
    source=template.model_copy(update={'source_id':'generated-cubedynamics-demo','asset_id':'generated-cube-nir',
        'uri':'generator://cubedynamics-sentinel-like','dataset':'Generated Sentinel-like calibration diagnostic',
        'support':template.support.model_copy(update={'bbox':(-106,39,-104,41)}),
        'checksum':digest('Generated metadata configuration, not raster bytes'),
        'provenance':(*template.provenance,'Generated extended cube layout; original illustrative STAC footprint is not the generated domain.')})
    target=Variable(name='nir_reflectance',definition='Calibrated generated NIR diagnostic; not observed Sentinel reflectance',
        unit='1',measurement_method='Documented scale/offset applied by the deterministic harmonizer')
    mapping=SemanticMapping(source_asset=source.asset_id,source_variable='B08_DN',target=target,relationship='convertible_to',
        evidence=('generated fixture calibration coefficients; no real scientific validation',),confidence=1,novel=True)
    base=HarmonizationRecipe(recipe_id='generated-cube-mosaiks',version='1',scope='core',mappings=(mapping,),
        operations=(Operation(source_asset=source.asset_id,operation='calibrate',source_variable='B08_DN',from_unit='DN',to_unit='1',scale=source.metadata.calibration_scale,offset=source.metadata.calibration_offset),
                    Operation(source_asset=source.asset_id,operation='map_variable',source_variable='B08_DN',target_variable=target.name)),
        proposals=(Proposal(role='harmonization',agent='fixture-decision-model',version='fixture-v1',rationale='Generated fixture selection only',evidence=('fixture',)),),author='generated-cube-demo')
    configuration=CubeConfiguration(inputs={'primary':CubeInput(resource_ids=(source.asset_id,),variable_units={target.name:'1'},
        crs='EPSG:32613',spatial_resolution=(10,10),spatial_support=source.support.spatial,temporal_support='instantaneous')},
        variable=target.name,window=(0,1,0,8,0,8),months=(7,),materialize=True,
        evidence=('generated fixture and approved native grid',),scientific_justification='Exercise real CubeDynamics over calibrated generated windows without altering pixel/acquisition support.')
    space=capabilities(base,(source,),configuration)
    offered={o.step.operation_id:o for o in space.options}
    selections=tuple(SelectDecision(operation_id=identifier,option_id=offered[identifier].option_id)
        for identifier in ('cubedynamics.select','cubedynamics.subset','cubedynamics.month_filter'))
    output=RecipeDecision(capability_digest=space.identity,status='PROPOSED',steps=selections,rationale='Select fixed canonical band, native window and documented July acquisition.')
    selected=FixtureDecisionModel(output.model_dump_json()).generate('harmonization','Select offered options only',space.model_dump(mode='json'),selection_schema(space))
    recipe=compile_decision(selected,space,base,(source,),configuration).model_copy(update={'status':'approved'})
    human=HumanDecision(recipe_digest=digest(recipe),status='approved',reviewer='generated-test-only',rationale='Synthetic governance example, no actual scientific approval',timestamp=datetime(2026,10,21,tzinfo=timezone.utc),fixture=True)
    plan=StreamPlan(question='Generated Sentinel-like CubeDynamics/MOSAIKS diagnostic; no real imagery',reader='test-generator',
        bindings=(StreamBinding(binding_id='generated-nir',source=source,source_variable='B08_DN',target=target,longitude=-105.585,latitude=40.035),))
    return RasterContext(plan=plan,recipe=recipe,human=human,cube_configuration=configuration),selected


def patches(context):
    import numpy as np
    from pyproj import Transformer
    transform=(10.,0.,500000.,0.,-10.,4430000.)
    to_geo=Transformer.from_crs('EPSG:32613','EPSG:4326',always_xy=True)
    source=context.plan.resources[0];rng=np.random.default_rng(91)
    for i in range(32):
        # Disjoint native columns; leave buffers between train/validation/test groups.
        column=i if i<16 else i+2 if i<24 else i+4
        raw=np.round(rng.uniform(1500,6000)+rng.normal(0,rng.uniform(20,500),(8,8)))
        left=500000+column*80;bottom=4430000-80
        lo,la=to_geo.transform([left,left+80],[bottom,4430000])
        lineage={'bbox':[min(lo),min(la),max(lo),max(la)],'native_crs':'EPSG:32613','native_transform':transform,
            'native_window':[0,column*8,8,8],'source_assets':[source.asset_id],
            'datetime_start':source.support.start.isoformat(),'datetime_end':source.support.end.isoformat(),
            'quality_policy':'Generated nonzero DN and generated SCL=4; real SCL eligibility is not inferred',
            'quality_evidence_digest':digest({'generated_class':4,'window':i})}
        yield harmonize_window({(source.asset_id,'B08_DN'):raw},context=context,patch_id=f'generated-cube-{i}',lineage=lineage,
            split='train' if i<16 else 'validation' if i<24 else 'test',spatial_group=f'generated-column-{column}')


def run(output):
    from .mosaiks import MOSAIKSSpec
    from .mosaiks_pipeline import run as embed
    from .embedding_dataset import verify_dataset
    context_value,selected=context()
    output=Path(output)
    spec=MOSAIKSSpec(channels=('nir_reflectance',),units=('1',),features=32,calibration_tiles=8,input_scale=32)
    result=embed(patches(context_value),context_value,spec,output)
    report=verify_dataset(output,output/'verification.json')
    (output/'fixture-model-selection.json').write_text(selected.model_dump_json(indent=2)+'\n')
    (output/'cube-demo-status.json').write_text(json.dumps({'fixture':True,'live_source_read':False,'live_inference':False,
        'backend':'real external cubedynamics 0.1.0rc3','records':result['records'],
        'note':'Generated diagnostics only. No approved real Sentinel release or independent scientific validity.'},indent=2)+'\n')
    (output/'generated-alignment-example.json').write_text(json.dumps(alignment_example(),indent=2,sort_keys=True)+'\n')
    return result,report


def alignment_example():
    """Two generated source identities/structures; grid alignment is not equivalence."""
    import numpy as np
    import xarray as xr
    from .cube_specs import SPECS
    from .contracts import BackendOperation
    from .cubedynamics_backend import CubeDynamicsBackend,context_digest
    from .operations import execution_identity
    ctx,_=context();source=ctx.plan.resources[0]
    other=source.model_copy(update={'asset_id':'generated-reference-grid','source_id':'generated-second-provider',
        'dataset':'Independent generated target grid; not NEON data'})
    mapping=ctx.recipe.mappings[0].model_copy(update={'source_asset':other.asset_id})
    operations=tuple(o.model_copy(update={'source_asset':other.asset_id}) for o in ctx.recipe.operations)
    coords={'time':[np.datetime64(source.support.start.replace(tzinfo=None),'ns')],
        'y':[4430015.,4430005.],'x':[500005.,500015.,500025.]}
    primary=xr.DataArray(np.arange(6,dtype=float).reshape(1,2,3)/10,dims=('time','y','x'),coords=coords,
        name='nir_reflectance',attrs={'units':'1','crs':'EPSG:32613'})
    reference=primary.isel(x=[0,2]).to_dataset();reference.attrs={'crs':'EPSG:32613'}
    spec=ctx.cube_configuration.inputs['primary']
    reference_spec=spec.model_copy(update={'resource_ids':(other.asset_id,),'spatial_resolution':(20,10)})
    configuration=CubeConfiguration(inputs={'primary':spec,'reference':reference_spec},
        target_spatial_support='Nearest sampled canonical values on generated 20 m grid; not area-averaged observations',
        evidence=('generated source structures and explicit same-quantity mapping only',),
        scientific_justification='Generated alignment mechanism test; does not establish equivalence of field and satellite measurements.',materialize=True)
    identifier='cubedynamics.align_nearest'
    backend_step=BackendOperation(operation_id=identifier,parameters={k:v['const'] for k,v in SPECS[identifier][2].items()})
    recipe=ctx.recipe.model_copy(update={'mappings':(*ctx.recipe.mappings,mapping),'operations':(*ctx.recipe.operations,*operations),
        'backend_operations':(backend_step,),'backend_context_digest':context_digest(configuration,(source,other)),
        'execution_identity':execution_identity()})
    decision=ctx.human.model_copy(update={'recipe_digest':digest(recipe)})
    product=CubeDynamicsBackend().execute(recipe,(source,other),configuration,{'primary':primary,'reference':reference},decision)
    return {'fixture':True,'source_structures':['xarray.DataArray','xarray.Dataset'],
        'source_ids':[source.asset_id,other.asset_id],'scientific_comparability':'not established by alignment',
        'transformation':product.transformations[-1].model_dump(mode='json')}
