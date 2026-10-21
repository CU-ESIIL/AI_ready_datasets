"""Network-free native-boundary tests. Invented responses are not live evidence."""
import json
from pathlib import Path
import pytest
from dataset_prototype.contracts import ScientificRequest, Support, Operation, AgentReview, recipe_content_digest
from dataset_prototype.real_data import acquire_sentinel, SnapshotClient
from dataset_prototype.harmonization import assess, run
from dataset_prototype.neon import NEONClient
from dataset_prototype.network import AccessError


@pytest.fixture
def sentinel_request():
    return ScientificRequest.model_validate_json(Path('examples/real/sentinel_request.json').read_text())


def fake_stac():
    href='https://sentinel-cogs.s3.us-west-2.amazonaws.com/test/'
    return {'license':'proprietary','links':[{'rel':'license','href':'https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice'}]}, {
        'id':'invented-native-stac-item','stac_version':'1.0.0','properties':{'datetime':'2023-07-10T18:00:00Z','platform':'sentinel-2a','instruments':['msi'],'eo:cloud_cover':5,'s2:processing_baseline':'05.09'},
        'assets':{'nir':{'href':href+'B08.tif','raster:bands':[{'scale':.0001,'offset':-.1}]},'scl':{'href':href+'SCL.tif'}}}


def fake_pixel(*args):
    return dict(dn=1234,scl=4,row=1,col=1,scl_row=0,scl_col=0,bbox=[-105.5861,40.0328,-105.5859,40.033],longitude=-105.586,latitude=40.0329,native_crs='EPSG:32613')


def test_stac_query_raw_dn_metadata_and_snapshot(sentinel_request,tmp_path):
    collection,item=fake_stac(); calls=[]
    def http(url,**kwargs):
        calls.append((url,kwargs));return collection if 'collections/' in url else {'features':[item]}
    out=tmp_path/'snapshot'
    snapshot=acquire_sentinel(sentinel_request,-105.586,40.0329,out,http=http,reader=fake_pixel)
    assert calls[1][1]['payload']['query']['eo:cloud_cover']['lte']==20
    source=snapshot.resources[0]; row=snapshot.records[0]
    assert not source.metadata.fixture and source.metadata.calibration_offset==-.1
    assert row.value==1234 and source.variables[0].unit=='DN' # no hidden calibration
    assert row.start==row.end and source.support.temporal=='instantaneous'
    assert source.checksum_scope=='extracted_window'
    assert 'Legal Notice' in source.rights.license
    assert source.metadata.original_identifier==item['id']
    client=SnapshotClient(out)
    assert client.fetch(source.asset_id)==snapshot.records
    assert client.search(sentinel_request)==snapshot.resources
    with pytest.raises(LookupError): client.fetch('nonexistent')
    (out/'window-0.json').write_text('{}')
    with pytest.raises(ValueError,match='evidence'): SnapshotClient(out)


def test_unknown_license_never_assumed_open(sentinel_request,tmp_path):
    collection,item=fake_stac();collection['links']=[]
    def http(url,**kwargs): return collection if 'collections/' in url else {'features':[item]}
    snapshot=acquire_sentinel(sentinel_request,-105.586,40.0329,tmp_path/'unknown',http=http,reader=fake_pixel)
    assert snapshot.resources[0].rights.redistribution is None


def test_cloud_rejection_and_no_fallback(sentinel_request,tmp_path):
    collection,item=fake_stac()
    def http(url,**kwargs): return collection if 'collections/' in url else {'features':[item]}
    def cloudy(*args): return {**fake_pixel(),'scl':9}
    with pytest.raises(ValueError,match='all candidate pixels rejected'):
        acquire_sentinel(sentinel_request,-105.586,40.0329,tmp_path/'cloudy',http=http,reader=cloudy)
    assert (tmp_path/'cloudy/rejections.json').exists()
    assert not (tmp_path/'cloudy/snapshot.json').exists()


def test_empty_search_and_unsafe_href(sentinel_request,tmp_path):
    collection,item=fake_stac()
    def empty(url,**kwargs): return collection if 'collections/' in url else {'features':[]}
    with pytest.raises(ValueError,match='no matching real'):
        acquire_sentinel(sentinel_request,-105.586,40.0329,tmp_path/'empty',http=empty,reader=fake_pixel)
    item['assets']['nir']['href']='file:///etc/passwd'
    def unsafe(url,**kwargs): return collection if 'collections/' in url else {'features':[item]}
    with pytest.raises(ValueError,match='access location'):
        acquire_sentinel(sentinel_request,-105.586,40.0329,tmp_path/'unsafe',http=unsafe,reader=fake_pixel)


def test_instantaneous_harmonization(sentinel_request,tmp_path):
    from dataset_prototype.agents import SemanticAgent,HarmonizationAgent
    collection,item=fake_stac()
    def http(url,**kwargs): return collection if 'collections/' in url else {'features':[item]}
    snapshot=acquire_sentinel(sentinel_request,-105.586,40.0329,tmp_path/'instant',http=http,reader=fake_pixel)
    r=snapshot.resources[0];v=r.variables[0]
    mapping=SemanticAgent().propose(r,v.name,v)
    recipe=HarmonizationAgent().propose((mapping,),(Operation(operation='validate',source_variable=v.name),)).model_copy(update={'status':'approved'})
    result=tuple(run((r,),recipe,snapshot.records))
    assert result[0].datetime_start==result[0].datetime_end
    assert result[0].value==1234


def test_neon_authentication_and_native_acquisition(tmp_path,monkeypatch):
    monkeypatch.delenv('NEON_API_TOKEN',raising=False)
    with pytest.raises(ValueError,match='NEON_API_TOKEN'): NEONClient().files('DP1.00002.001','NIWO','2023-07','RELEASE-2025')
    calls=[]
    def http(url,**kwargs):
        calls.append((url,kwargs));return {'data':{'files':[{'name':'native.csv','size':16,'url':'https://storage.googleapis.com/example/native.csv'}]}}
    def download(url,**kwargs):
        assert 'X-API-Token' not in kwargs['headers'];return b'field,value\nx,1\n'
    client=NEONClient(token='test-only-secret',http=http,download=download)
    report=client.acquire_file('DP1.00002.001','NIWO','2023-07','RELEASE-2025','native.csv',tmp_path/'neon')
    assert calls[0][1]['headers']=={'X-API-Token':'test-only-secret'}
    assert 'release=RELEASE-2025' in calls[0][0]
    assert report['license']=='CC-BY-4.0' and report['status'].startswith('native CSV')
    assert all('test-only-secret' not in p.read_text() for p in (tmp_path/'neon').iterdir())
    with pytest.raises(ValueError,match='exactly one'): client.acquire_file('DP1.00002.001','NIWO','2023-07','RELEASE-2025','missing.csv',tmp_path/'absent')


def test_neon_rejects_unknown_sizes_errors_and_paths(tmp_path):
    with pytest.raises(ValueError): NEONClient(token='test').files('bad','NIWO','2023-07','RELEASE-2025')
    client=NEONClient(token='test',http=lambda *a,**k:{'data':{'files':[{'name':'file.csv','url':'https://example.org/file.csv'}]}})
    with pytest.raises(ValueError,match='size'): client.acquire_file('DP1.00002.001','NIWO','2023-07','RELEASE-2025','file.csv',tmp_path/'out')
    with pytest.raises(ValueError,match='basename'): client.acquire_file('DP1.00002.001','NIWO','2023-07','RELEASE-2025','../file.csv',tmp_path/'out')


def test_model_qa_veto_and_staleness(bundle):
    resource,mapping,recipe,raw=bundle
    reviewed=recipe.model_copy(update={'agent_review':AgentReview(recipe_content_digest=recipe_content_digest(recipe),outcome='reject',reasons=('unsupported science',),reviewer='model:test')})
    assert assess(reviewed,(resource,)).outcome=='reject'
    with pytest.raises(ValueError,match='QA rejected'): tuple(run((resource,),reviewed,raw))
    edited=reviewed.model_copy(update={'version':'2'})
    assert any('stale' in r for r in assess(edited,(resource,)).reasons)


def test_complete_model_workflow_is_review_only(sentinel_request,tmp_path):
    from dataset_prototype.model_agents import (propose_snapshot,CandidateChoice,SemanticJudgment,RecipePlan,Critique)
    from dataset_prototype.contracts import HarmonizationRecipe
    collection,item=fake_stac()
    def http(url,**kwargs): return collection if 'collections/' in url else {'features':[item]}
    root=tmp_path/'snapshot'
    snapshot=acquire_sentinel(sentinel_request,-105.586,40.0329,root,http=http,reader=fake_pixel)
    original={p:p.read_bytes() for p in root.iterdir()}
    asset=snapshot.resources[0].asset_id
    class Backend:
        model='test-model';_model_digest='model-version';traces=[]
        def generate(self,role,instruction,evidence,schema):
            if schema is CandidateChoice: return CandidateChoice(asset_ids=(asset,),rationale='Actual candidate metadata matches')
            if schema is SemanticJudgment: return SemanticJudgment(relationship='equivalent_to',evidence=('Exact raw-DN definition matches',),confidence=1)
            if role=='harmonization':
                cap=evidence['available_operations']
                return schema.model_validate({'capability_digest':cap['capability_digest'],'status':'PROPOSED','rationale':'Preserve source-native values','steps':[{'authority':'SELECT','operation_id':o['operation_id'],'option_id':o['option_id']} for o in cap['options']]})
            return Critique(outcome='require_human_review',reasons=('Expert must review the scientific use',))
    output=propose_snapshot(root,tmp_path/'proposals',Backend())
    recipe=HarmonizationRecipe.model_validate_json((output/'proposed_recipe.json').read_text())
    assert recipe.agent_review.outcome=='require_human_review'
    assert assess(recipe,snapshot.resources).outcome=='require_human_review'
    assert json.loads((output/'review.json').read_text())['status']=='needs_review'
    assert all(p.read_bytes()==content for p,content in original.items())
    assert not (output/'harmonized.json').exists()
    with pytest.raises(ValueError,match='not approved'): tuple(run(snapshot.resources,recipe,snapshot.records))
    approved=recipe.model_copy(update={'status':'approved'})
    with pytest.raises(ValueError,match='human review'): tuple(run(snapshot.resources,approved,snapshot.records))


def test_instantaneous_semantics_are_explicit(bundle):
    resource,mapping,recipe,raw=bundle
    instant=raw[0].model_copy(update={'end':raw[0].start})
    with pytest.raises(ValueError,match='instantaneous source support'): tuple(run((resource,),recipe,(instant,)))
