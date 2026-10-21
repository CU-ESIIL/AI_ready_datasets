"""Actual external CubeDynamics API over generated lazy arrays; no live source access."""
from datetime import datetime, timezone
import json
import pytest
pytest.importorskip('cubedynamics', reason='optional real CubeDynamics integration extra')
import numpy as np
import xarray as xr
import dask.array as da
from dask import delayed
from dask.callbacks import Callback
from dataset_prototype.contracts import (BackendOperation, SourceResource,Variable,Support,Metadata,Rights,
    SemanticMapping,HarmonizationRecipe,Operation,Proposal,HumanDecision,digest)
from dataset_prototype.cube_contracts import CubeConfiguration,CubeInput,ResourceGuards
from dataset_prototype.cube_specs import SPECS
from dataset_prototype.cubedynamics_backend import CubeDynamicsBackend,CubeError,context_digest
from dataset_prototype.cube_ir import capabilities,selection_schema,compile_decision
from dataset_prototype.decision_ir import RecipeDecision,SelectDecision,FixtureDecisionModel
from dataset_prototype.operations import execution_identity


def step(identifier):
    return BackendOperation(operation_id=identifier,parameters={k:v['const'] for k,v in SPECS[identifier][2].items()})


def human(recipe):
    return HumanDecision(recipe_digest=digest(recipe),status='approved',reviewer='generated-only-reviewer',rationale='Synthetic scientific governance test only',timestamp=datetime(2026,10,21,tzinfo=timezone.utc),fixture=True)


@pytest.fixture
def cubes():
    times=np.array(['2023-01-01','2023-01-02','2023-01-03'],dtype='datetime64[ns]')
    coords={'time':times,'y':[4400015.,4400005.],'x':[500005.,500015.,500025.]}
    array=xr.DataArray(da.from_array(np.arange(18,dtype=float).reshape(3,2,3),chunks=(1,2,3)),dims=('time','y','x'),coords=coords,name='quantity',attrs={'units':'m','definition':'generated quantity'})
    array.attrs['crs']='EPSG:32613'
    variable=Variable(name='quantity',definition='generated quantity only',unit='m',measurement_method='generated fixture')
    source=SourceResource(checksum=digest('generated cube recipe; not a remote asset hash'),retrieved_at=datetime(2026,10,21,tzinfo=timezone.utc),provenance=('generated fixture, no real data',),source_id='generated',dataset='generated lazy cube',asset_id='cube-primary',version='1',uri='generator://cube',
        modality='satellite',variables=(variable,),support=Support(bbox=(-106,39,-104,41),start=datetime(2023,1,1,tzinfo=timezone.utc),end=datetime(2023,1,4,tzinfo=timezone.utc),spatial='native 10 m fixture cells',temporal='daily intervals'),
        metadata=Metadata(fixture=True,description='Generated cube; no provider observations',original_identifier='generated-cube'),rights=Rights(license='CC0-1.0',attribution='Generated project fixture',derivative_use=True,redistribution=True))
    mapping=SemanticMapping(source_asset=source.asset_id,source_variable=variable.name,target=variable,relationship='equivalent_to',evidence=('generated exact target',),confidence=1)
    recipe=HarmonizationRecipe(recipe_id='generated-cube-recipe',version='1',scope='core',mappings=(mapping,),operations=(Operation(operation='validate',source_variable=variable.name),),
        proposals=(Proposal(role='harmonization',rationale='Generated fixture',evidence=('fixture',)),),author='generated-test')
    spec=CubeInput(resource_ids=(source.asset_id,),variable_units={'quantity':'m'},crs='EPSG:32613',spatial_resolution=(10,10),spatial_support='native 10 m fixture cells',temporal_resolution_seconds=86400,temporal_support='equal_intervals',interval_seconds=86400)
    config=CubeConfiguration(inputs={'primary':spec},variable='quantity',window=(0,2,0,2,0,2),months=(1,),target_temporal_support='mean over three complete daily intervals',evidence=('generated definition/support',),scientific_justification='Synthetic operation test; no real scientific comparability claim')
    return source,recipe,array,config


def prepared(cubes,identifier,*,configuration=None,inputs=None,sources=None):
    source,base,array,config=cubes
    config=configuration or config;sources=sources or (source,);inputs=inputs or {'primary':array}
    recipe=base.model_copy(update={'status':'approved','backend_operations':(step(identifier),),'backend_context_digest':context_digest(config,sources),'execution_identity':execution_identity()})
    return recipe,sources,config,inputs,human(recipe)


@pytest.mark.parametrize('identifier',['cubedynamics.select','cubedynamics.subset','cubedynamics.month_filter','cubedynamics.temporal_mean'])
def test_real_public_operations_lazy_output_and_provenance(cubes,identifier):
    calls=[]
    with Callback(pretask=lambda *a:calls.append(a)):
        product=CubeDynamicsBackend().execute(*prepared(cubes,identifier))
    assert not calls
    assert product.transformations[0].lazy and not product.transformations[0].materialized
    result=product.transformations[0]
    assert result.backend_version=='0.1.0rc3' and result.dependency_versions['xarray']
    assert result.provenance['upstream_trace'] and result.provenance['recipe_digest']
    assert cubes[2].attrs['definition']=='generated quantity' and 'selected_calendar_months' not in cubes[2].attrs
    expected=np.arange(18).reshape(3,2,3)
    if identifier.endswith('subset'):expected=expected[:2,:,:2]
    elif identifier.endswith('temporal_mean'):expected=expected.mean(axis=0)[None,:,:]
    np.testing.assert_allclose(product.value.compute(),expected)
    if identifier.endswith('temporal_mean'):
        assert result.changes.aggregation and result.changes.temporal_support
        assert product.value.attrs['temporal_end_offset']=='259200000000000ns'


def test_explicit_bounded_materialization_reads_selected_chunks_only(cubes):
    reads=[]
    def block(i):
        reads.append(i)
        return np.full((1,2,3),i,dtype=float)
    cube=cubes[2].copy(data=da.concatenate([da.from_delayed(delayed(block)(i),shape=(1,2,3),dtype=float) for i in range(3)]))
    config=cubes[3].model_copy(update={'window':(0,1,0,2,0,2),'materialize':True})
    product=CubeDynamicsBackend().execute(*prepared(cubes,'cubedynamics.subset',configuration=config,inputs={'primary':cube}))
    assert reads==[0] and product.value.shape==(1,2,2)
    result=product.transformations[-1]
    assert result.materialized and not result.lazy and result.provenance['window_evidence_hashes']
    assert result.provenance['checksum_scope'].startswith('materialized final window')


def test_mask_uses_documented_predicate_and_keeps_missing_values(cubes):
    source,recipe,array,config=cubes
    quality=array.copy(data=da.from_array(np.array([4,0,5]*6).reshape(3,2,3),chunks=(1,2,3))).rename('SCL')
    quality.attrs={**array.attrs,'units':'1'}
    qvar=source.variables[0].model_copy(update={'name':'SCL','unit':'1'})
    qsource=source.model_copy(update={'asset_id':'quality','variables':(qvar,)})
    qmapping=recipe.mappings[0].model_copy(update={'source_asset':'quality','source_variable':'SCL','target':qvar})
    recipe=recipe.model_copy(update={'mappings':(*recipe.mappings,qmapping),'operations':(*recipe.operations,Operation(operation='validate',source_variable='SCL'))})
    cubes=(source,recipe,array,config)
    qspec=config.inputs['primary'].model_copy(update={'resource_ids':('quality',),'variable_units':{'SCL':'1'},'mask_definition':'Generated SCL; retain classes 4 and 5'})
    config=config.model_copy(update={'inputs':{'primary':config.inputs['primary'],'quality':qspec},'allowed_quality_classes':(4,5)})
    product=CubeDynamicsBackend().execute(*prepared(cubes,'cubedynamics.quality_mask',configuration=config,inputs={'primary':array,'quality':quality},sources=(source,qsource)))
    assert product.transformations[0].lazy
    assert np.isnan(product.value.compute().values[:,:,1]).all()


def test_heterogeneous_exact_support_alignment_and_nearest_grid(cubes):
    source,recipe,array,config=cubes
    # Dataset and DataArray differ structurally; coordinate compatibility is not equivalence.
    reference=array.to_dataset().isel(x=[0,2])
    reference.attrs=dict(array.attrs)
    config=config.model_copy(update={'inputs':{'primary':config.inputs['primary'],
        'reference':config.inputs['primary'].model_copy(update={'spatial_resolution':(20,10)})},'target_spatial_support':'nearest sampled values on 20 m target grid; not area means'})
    inputs={'primary':array,'reference':reference}
    for identifier in ('cubedynamics.align_time','cubedynamics.align_nearest'):
        product=CubeDynamicsBackend().execute(*prepared(cubes,identifier,configuration=config,inputs=inputs))
        assert product.transformations[0].lazy
        if identifier.endswith('align_nearest'):
            np.testing.assert_allclose(product.value.compute(),array.isel(x=[0,2]).compute())
            assert product.transformations[0].changes.spatial_support and product.transformations[0].changes.spatial_resolution
        else:np.testing.assert_allclose(product.value.compute(),array.compute())


@pytest.mark.parametrize('change,code',[
 ('missing_crs','PRECONDITION_FAILED'),('invalid_statistic','INVALID_PARAMETERS'),
 ('unknown_operation','UNSUPPORTED_OPERATION'),('missing_support','NEEDS_EVIDENCE'),
 ('wrong_units','PRECONDITION_FAILED'),('source_changed','PRECONDITION_FAILED'),
 ('review_missing','NEEDS_HUMAN_REVIEW'),('memory','RESOURCE_LIMIT'),
 ('window','INVALID_PARAMETERS'),('unknown_variable','INVALID_PARAMETERS'),
])
def test_failures_before_computation(cubes,change,code):
    identifier='cubedynamics.temporal_mean' if change=='missing_support' else 'cubedynamics.subset'
    recipe,sources,config,inputs,decision=prepared(cubes,identifier)
    if change=='missing_crs':inputs={'primary':inputs['primary'].copy()};inputs['primary'].attrs.pop('crs')
    elif change=='invalid_statistic':recipe=recipe.model_copy(update={'backend_operations':(step('cubedynamics.temporal_mean').model_copy(update={'parameters':{'statistic':'median'}}),)})
    elif change=='unknown_operation':recipe=recipe.model_copy(update={'backend_operations':(BackendOperation(operation_id='cubedynamics.execute_python',parameters={}),)})
    elif change=='missing_support':config=config.model_copy(update={'inputs':{'primary':config.inputs['primary'].model_copy(update={'temporal_support':'unknown'})}})
    elif change=='wrong_units':inputs={'primary':inputs['primary'].copy()};inputs['primary'].attrs['units']='K'
    elif change=='source_changed':sources=(sources[0].model_copy(update={'version':'2'}),)
    elif change=='review_missing':decision=None
    elif change=='memory':config=config.model_copy(update={'guards':ResourceGuards(max_input_bytes=1)})
    elif change=='window':config=config.model_copy(update={'window':(0,100,0,1,0,1)})
    elif change=='unknown_variable':identifier='cubedynamics.select';config=config.model_copy(update={'variable':'invented'});recipe=recipe.model_copy(update={'backend_operations':(step(identifier),)})
    if change in ('missing_support','memory','window','unknown_variable'):
        recipe=recipe.model_copy(update={'backend_context_digest':context_digest(config,sources)});decision=human(recipe)
    called=[]
    with Callback(pretask=lambda *a:called.append(a)):
        with pytest.raises(ValueError,match=code):CubeDynamicsBackend().execute(recipe,sources,config,inputs,decision)
    assert not called


def test_reference_bound_model_choice_and_model_off_execution(cubes):
    source,base,array,configuration=cubes
    space=capabilities(base,(source,),configuration)
    option=next(o for o in space.options if o.step.operation_id=='cubedynamics.subset')
    output=RecipeDecision(capability_digest=space.identity,status='PROPOSED',rationale='Choose reviewed window',steps=(SelectDecision(operation_id=option.step.operation_id,option_id=option.option_id),))
    backend=FixtureDecisionModel(output.model_dump_json())
    selected=backend.generate('harmonization','Choose offered option only',space.model_dump(mode='json'),selection_schema(space))
    proposed=compile_decision(selected,space,base,(source,),configuration)
    approved=proposed.model_copy(update={'status':'approved'})
    # No model/backend is accepted by the scientific execution interface.
    product=CubeDynamicsBackend().execute(approved,(source,),configuration,{'primary':array},human(approved))
    assert product.value.shape==(2,2,2)
    payload=output.model_dump(mode='json');payload['steps'][0]['python']='cube.compute()'
    with pytest.raises(ValueError):selection_schema(space).model_validate(payload)
    payload['steps'][0].pop('python');payload['steps'][0]['operation_id']='cubedynamics.any_function'
    with pytest.raises(ValueError):selection_schema(space).model_validate(payload)
    with pytest.raises(ValueError,match='UNSUPPORTED_OPERATION'):compile_decision(RecipeDecision.model_validate(payload),space,base,(source,),configuration)


def test_multiband_selection_preserves_native_attributes(cubes):
    source,base,array,config=cubes
    cube=array.expand_dims(band=['B04','B08'])
    config=config.model_copy(update={'variable':'B08'})
    result=CubeDynamicsBackend().execute(*prepared(cubes,'cubedynamics.select',configuration=config,inputs={'primary':cube}))
    assert result.value.band.values.tolist()==['B08'] and result.value.attrs['crs']=='EPSG:32613'


def test_ordered_subsets_cannot_invalidate_aggregation_silently(cubes):
    recipe,sources,config,inputs,_=prepared(cubes,'cubedynamics.subset')
    config=config.model_copy(update={'window':(0,1,0,2,0,2)})
    recipe=recipe.model_copy(update={'backend_operations':(step('cubedynamics.subset'),step('cubedynamics.temporal_mean')),
        'backend_context_digest':context_digest(config,sources)})
    with pytest.raises(ValueError,match='earlier operations broke'):
        CubeDynamicsBackend().execute(recipe,sources,config,inputs,human(recipe))


def test_no_scalar_bypass_and_required_review_for_changed_configuration(cubes):
    from dataset_prototype.harmonization import run
    recipe,sources,config,inputs,decision=prepared(cubes,'cubedynamics.subset')
    with pytest.raises(ValueError,match='CubeDynamics controller'):tuple(run(sources,recipe,iter(()),decision))
    changed=config.model_copy(update={'materialize':True})
    with pytest.raises(ValueError,match='binding changed'):
        CubeDynamicsBackend().execute(recipe,sources,changed,inputs,decision)


def test_real_sources_cannot_bypass_existing_streaming_review(cubes):
    recipe,sources,config,inputs,_=prepared(cubes,'cubedynamics.subset')
    source=sources[0].model_copy(update={'metadata':sources[0].metadata.model_copy(update={'fixture':False})})
    recipe=recipe.model_copy(update={'backend_context_digest':context_digest(config,(source,))})
    with pytest.raises(ValueError,match='matching reviewed raster context'):
        CubeDynamicsBackend().execute(recipe,(source,),config,inputs,human(recipe))


def test_generated_sentinel_harmonized_window_bridge_and_no_raw_persistence(tmp_path):
    from dataset_prototype.cube_demo import context,patches,run
    ctx,_=context();iterator=patches(ctx)
    patch=next(iterator);iterator.close()
    assert patch.channels==('nir_reflectance',) and patch.units==('1',)
    assert patch.lineage['cubedynamics_version']=='0.1.0rc3'
    assert len(patch.lineage['backend_transformations'])==3
    assert patch.lineage['backend_transformations'][-1]['materialized']
    manifest,report=run(tmp_path/'demo')
    assert manifest['records']==32
    assert (tmp_path/'demo/fixture-model-selection.json').exists()
    status=json.loads((tmp_path/'demo/cube-demo-status.json').read_text())
    assert not status['live_source_read'] and not status['live_inference']
    assert not list((tmp_path/'demo').rglob('*.tif')) and not list((tmp_path/'demo').rglob('*.nc'))


def test_unregistered_function_and_invalid_refs_never_dispatch(cubes):
    from dataset_prototype.cube_ir import capabilities,compile_decision
    source,base,array,config=cubes
    space=capabilities(base,(source,),config)
    bad=RecipeDecision(capability_digest=space.identity,status='PROPOSED',rationale='adversarial',steps=(SelectDecision(operation_id='cubedynamics.apply',option_id=space.options[0].option_id),))
    with pytest.raises(ValueError,match='UNSUPPORTED_OPERATION'):compile_decision(bad,space,base,(source,),config)
    recipe,sources,config,inputs,_=prepared(cubes,'cubedynamics.subset')
    recipe=recipe.model_copy(update={'backend_operations':(step('cubedynamics.subset').model_copy(update={'parameters':{'window_ref':'__import__("os")'}}),)})
    with pytest.raises(ValueError,match='INVALID_PARAMETERS'):CubeDynamicsBackend().execute(recipe,sources,config,inputs,human(recipe))


def test_singleton_subset_does_not_change_pixel_resolution(cubes):
    config=cubes[3].model_copy(update={'window':(0,1,0,1,0,1)})
    product=CubeDynamicsBackend().execute(*prepared(cubes,'cubedynamics.subset',configuration=config))
    result=product.transformations[0]
    assert result.changes.extent and not result.changes.spatial_resolution and not result.changes.spatial_support


def test_aggregate_support_does_not_invent_sampling_resolution(cubes):
    product=CubeDynamicsBackend().execute(*prepared(cubes,'cubedynamics.temporal_mean'))
    assert product.value.attrs['temporal_resolution'] is None
    assert product.value.attrs['temporal_end_offset']=='259200000000000ns'


def test_model_harmonization_role_selects_backend_without_python(cubes):
    from dataset_prototype.model_agents import ModelHarmonizationAgent
    source,base,_,config=cubes
    space=capabilities(base,(source,),config)
    offered=next(o for o in space.options if o.step.operation_id=='cubedynamics.subset')
    decision=RecipeDecision(capability_digest=space.identity,status='PROPOSED',rationale='Review fixed window',
        steps=(SelectDecision(operation_id=offered.step.operation_id,option_id=offered.option_id),))
    recipe=ModelHarmonizationAgent(FixtureDecisionModel(decision.model_dump_json())).propose_backend(base,(source,),config)
    assert recipe.backend_operations[0].parameters=={'window_ref':'request.window'}
    assert recipe.status=='needs_review' and 'MODEL_JUDGMENT' in recipe.proposals[-1].configuration


def test_all_specialists_and_qa_review_exact_frozen_backend_recipe(tmp_path):
    from dataset_prototype.cube_demo import context
    from dataset_prototype.consensus import negotiate
    from dataset_prototype.stream_contracts import SpecialistFinding,ReviewVote
    from dataset_prototype.contracts import recipe_content_digest
    ctx,_=context()
    class Reviewers:
        model='generated-reviewers';_model_digest='fixture';traces=()
        def __init__(self):self.reviewed=[]
        def generate(self,role,instruction,evidence,schema):
            refs=tuple(m['metadata_ref'] for m in evidence['metadata'])
            if schema is SpecialistFinding:
                return SpecialistFinding(assessment='Generated review only',constraints=('Keep frozen recipe',),concerns=(),evidence_refs=refs)
            assert schema is ReviewVote
            self.reviewed.append(evidence['recipe_content_digest'])
            peer=next(m['message_id'] for m in evidence['dialogue'] if m['sender']!=role and m['kind']=='analysis')
            return ReviewVote(decision='agree',rationale='Generated test review',concerns=(),responds_to=(evidence['draft_message_id'],peer),evidence_refs=refs)
    backend=Reviewers()
    report=negotiate(ctx.plan,backend,tmp_path/'frozen',frozen_recipe=ctx.recipe,cube_configuration=ctx.cube_configuration)
    assert report.status=='consensus' and len(backend.reviewed)==5
    assert set(backend.reviewed)=={recipe_content_digest(ctx.recipe)}
    reviewed=HarmonizationRecipe.model_validate_json((tmp_path/'frozen/proposed_recipe.json').read_text())
    assert reviewed.backend_operations==ctx.recipe.backend_operations
    assert reviewed.backend_context_digest==ctx.recipe.backend_context_digest
    assert reviewed.status=='needs_review'  # Review is not a human approval.
