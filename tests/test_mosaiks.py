"""Real MOSAIKS math on generated harmonization outputs; no data downloads."""
import json
import numpy as np
import pytest
from dataset_prototype.mosaiks import MOSAIKSSpec,MOSAIKSEncoder,validate_patch,target_schema_digest
from dataset_prototype.harmonized_rasters import RasterContext,harmonize_window
from dataset_prototype.mosaiks_pipeline import demo
from dataset_prototype.embedding_dataset import write_dataset,verify_dataset
from dataset_prototype.contracts import digest


@pytest.fixture
def raster_context(tmp_path):
    root=tmp_path/'demo'
    manifest,report=demo(root)
    context=RasterContext.model_validate_json((root/'harmonization_context.json').read_text())
    return context,root,report


def patch(context,i=0,split='train'):
    source=context.plan.resources[0];variable=source.variables[0]
    array=np.random.default_rng(i).uniform(0,1,(8,8))
    lineage={'bbox':[-105+i*.001,40,-105+(i+1)*.001,40.0005], 'native_crs':'synthetic-grid','native_window':[i,0,8,8],
        'source_assets':[source.asset_id],'datetime_start':source.support.start.isoformat(),'datetime_end':source.support.end.isoformat(),'quality_policy':'generated finite values'}
    return harmonize_window({(source.asset_id,variable.name):array},context=context,patch_id=str(i),lineage=lineage,split=split,spatial_group=f'block-{i}')


def test_mosaiks_oracle_and_no_raw_inputs(raster_context):
    from dataclasses import replace
    context,_,_=raster_context
    p=patch(context)
    # Analytic constant filter: all valid 2x2 sums of 0..15 have mean 30.
    source=context.plan.resources[0]
    q=harmonize_window({(source.asset_id,source.variables[0].name):np.arange(16).reshape(4,4)},context=context,patch_id='oracle',lineage={**p.lineage,'native_window':[0,0,4,4]},split='train',spatial_group='oracle')
    spec=MOSAIKSSpec(channels=q.channels,units=q.units,features=16,kernel_size=2)
    model=MOSAIKSEncoder(spec,np.ones((8,1,2,2)),('diagnostic',),digest(context),target_schema_digest(context,spec))
    vector=model.encode(q,context)
    assert vector[:8]==pytest.approx([29]*8) and vector[8:]==pytest.approx([0]*8)
    with pytest.raises(TypeError,match='harmonized raster'):
        model.encode(q.values,context)
    with pytest.raises(ValueError,match='content/lineage'):
        model.encode(replace(q,values=q.values+1),context)
    with pytest.raises(ValueError,match='shape, channel'):
        model.encode(replace(q,units=('DN',)),context)


def test_train_only_fit_and_frozen_reload(raster_context,tmp_path):
    context,_,_=raster_context
    patches=[patch(context,i) for i in range(4)]
    spec=MOSAIKSSpec(channels=patches[0].channels,units=patches[0].units,features=32,calibration_tiles=4)
    a=MOSAIKSEncoder.fit(iter(patches),spec,context);b=MOSAIKSEncoder.fit(iter(patches),spec,context)
    assert a.identity==b.identity and np.array_equal(a.filters,b.filters)
    a.save(tmp_path/'encoder');loaded=MOSAIKSEncoder.load(tmp_path/'encoder')
    assert np.array_equal(a.encode(patches[0],context),loaded.encode(patches[0],context))
    with pytest.raises(ValueError,match='training split only'):
        MOSAIKSEncoder.fit(iter([patch(context,8,'test')]),spec,context)
    from dataset_prototype.mosaiks_pipeline import run as pipeline
    with pytest.raises(ValueError,match='training split only'):
        pipeline(iter([patch(context,8,'test')]),context,spec,tmp_path/'failed-calibration')
    failed=json.loads((tmp_path/'failed-calibration/manifest.json').read_text())
    assert failed['status']=='failed' and failed['stage']=='filter_calibration'
    filters=np.load(tmp_path/'encoder/filters.npy');filters[0,0,0,0]+=1;np.save(tmp_path/'encoder/filters.npy',filters)
    with pytest.raises(ValueError,match='integrity'):
        MOSAIKSEncoder.load(tmp_path/'encoder')


def test_verification_native_ml_and_baselines(raster_context):
    _,root,report=raster_context
    assert report['status']=='evaluated' and report['native_numeric_consumption']
    assert report['scientific_validation']=='not_established'
    assert report['target'][1]=='derived-diagnostic'
    assert report['test']['rmse']<report['mean_baseline']['rmse']
    assert report['test']['rmse']<report['shuffled_label_baseline']['rmse']
    assert report['counts']=={'train':16,'validation':8,'test':8}
    from dataset_prototype.embedding_dataset import predict_vectors
    vectors=np.load(root/'vectors-00000.npy',allow_pickle=False)
    predictions=predict_vectors(vectors,root/report['probe_file'],encoder_identity=report['encoder_identity'],expected_sha256=report['probe_sha256'])
    assert predictions.shape==(16,) and np.isfinite(predictions).all()
    with pytest.raises(ValueError,match='encoder identity'):
        predict_vectors(vectors,root/report['probe_file'],encoder_identity='wrong',expected_sha256=report['probe_sha256'])
    assert not any('raw' in p.name or 'harmonized_arrays' in p.name for p in root.rglob('*'))
    assert '"values"' not in (root/'records.jsonl').read_text()


@pytest.mark.parametrize('corruption',['group','geography','shard','row_identity'])
def test_reject_leakage_and_corruption(raster_context,tmp_path,corruption):
    _,root,_=raster_context
    path=root/'records.jsonl';rows=[json.loads(line) for line in path.read_text().splitlines()]
    train=next(r for r in rows if r['split']=='train');test=next(r for r in rows if r['split']=='test')
    if corruption=='group':test['spatial_group']=train['spatial_group']
    elif corruption=='geography':test['lineage']['bbox']=train['lineage']['bbox']
    elif corruption=='row_identity':test['observation_digest']='0'*64
    else:
        shard=root/rows[0]['vector_shard'];array=np.load(shard);array[0,0]+=1;np.save(shard,array)
    path.write_text('\n'.join(json.dumps(r) for r in rows)+'\n')
    if corruption!='shard':
        from dataset_prototype.mosaiks import file_digest
        manifest=json.loads((root/'manifest.json').read_text());manifest['records_sha256']=file_digest(path)
        (root/'manifest.json').write_text(json.dumps(manifest))
    with pytest.raises(ValueError):verify_dataset(root,tmp_path/'bad.json')


def test_review_gate_before_opening_stream(raster_context,tmp_path):
    context,_,_=raster_context
    bad=context.model_copy(update={'recipe':context.recipe.model_copy(update={'status':'needs_review'})})
    model=MOSAIKSEncoder.fit(iter([patch(context,i) for i in range(3)]),MOSAIKSSpec(channels=(context.recipe.mappings[0].target.name,),units=('1',),features=16,calibration_tiles=3),context)
    def forbidden():
        raise AssertionError('unapproved harmonized stream opened')
        yield
    with pytest.raises(ValueError,match='not approved'):write_dataset(forbidden(),model,bad,tmp_path/'blocked')
    assert not (tmp_path/'blocked').exists()


def test_backpressure_and_partial_failure(raster_context,tmp_path):
    context,_,_=raster_context
    ps=[patch(context,i) for i in range(6)]
    spec=MOSAIKSSpec(channels=ps[0].channels,units=ps[0].units,features=16,calibration_tiles=3)
    model=MOSAIKSEncoder.fit(iter(ps[:3]),spec,context)
    root=tmp_path/'stream'
    def source():
        for i,p in enumerate(ps):
            if i>=2:assert (root/'vectors-00000.npy').exists()
            yield p
        raise RuntimeError('interrupted harmonization stream')
    with pytest.raises(RuntimeError):write_dataset(source(),model,context,root,batch_size=2)
    assert json.loads((root/'manifest.json').read_text())['status']=='failed'
    assert (root/'records.jsonl.partial').exists() and not (root/'records.jsonl').exists()


def test_independent_labels_need_scientific_provenance(raster_context,tmp_path):
    from dataclasses import replace
    context,_,_=raster_context
    ps=[patch(context,i) for i in range(3)]
    spec=MOSAIKSSpec(channels=ps[0].channels,units=ps[0].units,features=16,calibration_tiles=3)
    model=MOSAIKSEncoder.fit(iter(ps),spec,context)
    independent=replace(ps[0],target_kind='independent-label')
    with pytest.raises(ValueError,match='alignment provenance'):
        write_dataset(iter([independent]),model,context,tmp_path/'no-label-evidence')


def test_reviewed_raster_plan_changes_digest_and_settings_are_fixed(request_model):
    from dataset_prototype.stream_sources import plan_sentinel
    from dataset_prototype.stream_contracts import StreamPlan
    from dataset_prototype.mosaiks_pipeline import plan_rasters,RasterLayout
    x0,y0,x1,y1=request_model.support.bbox
    item={'id':'generated-stac','stac_version':'1.0.0','bbox':[x0,y0,x1,y1],
          'properties':{'datetime':request_model.support.start.isoformat(),'platform':'sentinel-2a','eo:cloud_cover':0},
          'assets':{k:{'href':'https://sentinel-cogs.s3.us-west-2.amazonaws.com/generated/'+k+'.tif',
                       'raster:bands':[{'scale':.0001,'offset':-.1,'nodata':0}]} for k in ('nir','scl')}}
    def http(url,**kwargs):return {'license':'CC-BY-4.0'} if url.endswith('sentinel-2-l2a') else {'features':[item]}
    plan=plan_sentinel(request_model,x0,y0,http=http)
    spec=MOSAIKSSpec(channels=('B08_reflectance',),units=('1',))
    old_json=plan.model_dump(mode='json')
    converted=plan_rasters(plan,spec,RasterLayout(side=8))
    assert digest(converted)!=digest(plan) and converted.reader=='sentinel-raster'
    assert converted.encoder.method=='mosaiks' and converted.raster_layout_json
    assert digest(StreamPlan.model_validate(old_json))==digest(old_json)
    with pytest.raises(ValueError,match='lengths'):
        MOSAIKSSpec(channels=('a','b'),units=('1',))


def test_raster_calibration_matches_scalar_executor_and_rejects_bad_coefficients(raster_context):
    from datetime import datetime,timezone
    from dataset_prototype.contracts import Variable,Operation,HumanDecision,RawObservation
    from dataset_prototype.harmonization import run as scalar
    context,_,_=raster_context
    source=context.plan.resources[0];target=context.recipe.mappings[0].target
    native=target.model_copy(update={'name':'encoded_DN','unit':'DN','definition':'Generated encoded diagnostic quantity'})
    source=source.model_copy(update={'variables':(native,),'metadata':source.metadata.model_copy(update={'calibration_scale':.0001,'calibration_offset':-.1})})
    mapping=context.recipe.mappings[0].model_copy(update={'source_variable':native.name,'relationship':'convertible_to','novel':True})
    operations=(Operation(operation='calibrate',source_variable=native.name,from_unit='DN',to_unit='1',scale=.0001,offset=-.1),Operation(operation='map_variable',source_variable=native.name,target_variable=target.name))
    recipe=context.recipe.model_copy(update={'mappings':(mapping,),'operations':operations})
    human=HumanDecision(recipe_digest=digest(recipe),status='approved',reviewer='offline-test-only',rationale='Generated numerical calibration diagnostic; no scientific approval claimed',timestamp=datetime.now(timezone.utc))
    binding=context.plan.bindings[0].model_copy(update={'source':source,'source_variable':native.name})
    plan=context.plan.model_copy(update={'bindings':(binding,)})
    reviewed=RasterContext(plan=plan,recipe=recipe,human=human)
    raw=np.arange(16,dtype=np.uint16).reshape(4,4)+2000
    lineage=patch(context).lineage.copy();lineage['native_window']=[0,0,4,4]
    tile=harmonize_window({(source.asset_id,native.name):raw},context=reviewed,patch_id='calibrated',lineage=lineage,split='train',spatial_group='test-calibration')
    records=[RawObservation(record_id=str(i),asset_id=source.asset_id,variable=native.name,value=int(v),longitude=-105,latitude=40,start=source.support.start,end=source.support.end,quality_flag='generated') for i,v in enumerate(raw.flat)]
    expected=[o.value for o in scalar((source,),recipe,iter(records),human)]
    assert tile.values.dtype==np.float64
    np.testing.assert_allclose(tile.values.ravel(),expected,rtol=0,atol=1e-14)
    wrong=recipe.model_copy(update={'operations':(operations[0].model_copy(update={'offset':0}),operations[1])})
    with pytest.raises(ValueError,match='calibration disagrees'):
        harmonize_window({(source.asset_id,native.name):raw},context=reviewed.model_copy(update={'recipe':wrong}),patch_id='bad',lineage=lineage,split='train',spatial_group='bad')


def test_matching_channel_names_do_not_override_scientific_definitions(raster_context):
    context,_,_=raster_context
    ps=[patch(context,i) for i in range(3)]
    spec=MOSAIKSSpec(channels=ps[0].channels,units=ps[0].units,features=16,calibration_tiles=3)
    model=MOSAIKSEncoder.fit(iter(ps),spec,context)
    newvar=context.plan.resources[0].variables[0].model_copy(update={'definition':'Different generated quantity; same spelling and units'})
    source=context.plan.resources[0].model_copy(update={'variables':(newvar,)})
    mapping=context.recipe.mappings[0].model_copy(update={'target':newvar})
    recipe=context.recipe.model_copy(update={'mappings':(mapping,)})
    binding=context.plan.bindings[0].model_copy(update={'source':source,'target':newvar})
    changed=RasterContext(plan=context.plan.model_copy(update={'bindings':(binding,)}),recipe=recipe)
    with pytest.raises(ValueError,match='scientific definitions'):
        model.encode(patch(changed,8),changed)


def test_assemble_actual_harmonized_observations_without_implicit_reshaping(raster_context):
    from dataset_prototype.harmonized_rasters import assemble_patch
    from dataset_prototype.harmonization import run as harmonize
    from dataset_prototype.contracts import RawObservation
    context,_,_=raster_context
    source=context.plan.resources[0];target=context.recipe.mappings[0].target
    records=[RawObservation(record_id=str(i),asset_id=source.asset_id,variable=target.name,value=i/10,longitude=-105+(i%4)*.0001,latitude=40+(i//4)*.0001,start=source.support.start,end=source.support.end,quality_flag='generated') for i in range(16)]
    observations=list(harmonize(context.plan.resources,context.recipe,iter(records)))
    cells=[(i//4,i%4,o) for i,o in enumerate(observations)]
    args=dict(context=context,patch_id='assembled',channels=(target.name,),units=('1',),height=4,width=4,
        lineage=patch(context).lineage,split='train',spatial_group='assembled')
    result=assemble_patch(iter(cells),**args)
    np.testing.assert_allclose(result.values.ravel(),[r.value for r in records])
    with pytest.raises(ValueError,match='incomplete'):assemble_patch(iter(cells[:-1]),**args)
    with pytest.raises(TypeError,match='harmonized observations'):assemble_patch(iter([(0,0,records[0])]),**args)


@pytest.mark.parametrize('accepted',[True,False])
def test_source_adapter_emits_harmonization_outputs_with_bounded_windows(raster_context,monkeypatch,accepted,evidence_review_factory):
    import sys
    from types import ModuleType,SimpleNamespace
    from contextlib import nullcontext
    from dataset_prototype.mosaiks_pipeline import plan_rasters,RasterLayout
    from dataset_prototype.stream_rasters import sentinel_harmonized_tiles
    import dataset_prototype.stream_rasters as access
    import dataset_prototype.stream_sources as metadata
    context,_,_=raster_context
    spec=MOSAIKSSpec(channels=(context.recipe.mappings[0].target.name,),units=('1',),features=16)
    plan=plan_rasters(context.plan.model_copy(update={'reader':'sentinel-pixel'}),spec,RasterLayout(side=4,grid=6))
    context=context.model_copy(update={'plan':plan,'evidence_review':evidence_review_factory(plan,context.recipe)})
    def native(binding):return {'assets':{'scl':{'href':'generated-mask'}}}
    monkeypatch.setattr(metadata,'validated_native',native);monkeypatch.setattr(access,'validated_native',native)
    reads=[];closed=[]
    class CRS:
        is_projected=True
        def __str__(self):return 'EPSG:32613'
    class Dataset:
        width=100;height=100;crs=CRS();res=(10,10);transform='generated-grid'
        def __init__(self,uri):self.uri=uri
        def __enter__(self):return self
        def __exit__(self,*args):closed.append(self.uri)
        def index(self,x,y):return 50,50
        def read(self,band,*,window):
            reads.append((self.uri,window.width,window.height))
            value=(4 if accepted else 9) if self.uri=='generated-mask' else .2
            return np.full((int(window.height),int(window.width)),value)
    rasterio=ModuleType('rasterio');rasterio.Env=lambda **kwargs:nullcontext();rasterio.open=Dataset
    windows=ModuleType('rasterio.windows')
    windows.Window=lambda col,row,width,height:SimpleNamespace(col_off=col,row_off=row,width=width,height=height)
    windows.bounds=lambda w,t:(-105+w.col_off*.00001,40+w.row_off*.00001,-105+(w.col_off+w.width)*.00001,40+(w.row_off+w.height)*.00001)
    windows.from_bounds=lambda *args,**kwargs:windows.Window(0,0,2,2)
    warp=ModuleType('rasterio.warp');warp.transform=lambda src,dst,x,y:(x,y);warp.transform_bounds=lambda src,dst,*bounds:bounds
    for name,module in [('rasterio',rasterio),('rasterio.windows',windows),('rasterio.warp',warp)]:monkeypatch.setitem(sys.modules,name,module)
    iterator=sentinel_harmonized_tiles(context,side=4,grid=6)
    assert not reads
    if accepted:
        result=next(iterator)
        assert result.values.shape==(1,4,4) and result.lineage['harmonization_status']=='approved'
        assert result.lineage['quality_evidence_digest']
        assert reads[-1][1:]==(4,4)
        iterator.close()
    else:
        with pytest.raises(ValueError,match='quality rejected'):next(iterator)
        assert all(uri=='generated-mask' for uri,_,_ in reads)
    assert len(closed)==2
