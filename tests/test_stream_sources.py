import json
import pytest
from dataset_prototype.contracts import digest
from dataset_prototype.stream_sources import plan_sentinel, sentinel_samples


def metadata(request):
    return {'id':'S2-test','stac_version':'1.0.0','bbox':list(request.support.bbox),
        'properties':{'datetime':request.support.start.isoformat(),'platform':'sentinel-2a','eo:cloud_cover':0,'instruments':['msi']},
        'assets':{'nir':{'href':'https://sentinel-cogs.s3.us-west-2.amazonaws.com/test/B08.tif','raster:bands':[{'scale':.0001,'offset':-.1,'nodata':0}]},
                  'scl':{'href':'https://sentinel-cogs.s3.us-west-2.amazonaws.com/test/SCL.tif'}}}


def test_metadata_plan_then_lazy_window_without_files(request_model,tmp_path):
    item=metadata(request_model);calls=[]
    def http(url,**kwargs):
        calls.append(url)
        return {'license':'CC-BY-4.0'} if url.endswith('sentinel-2-l2a') else {'features':[item]}
    x0,y0,x1,y1=request_model.support.bbox
    lon=(x0+x1)/2;lat=(y0+y1)/2
    plan=plan_sentinel(request_model,lon,lat,http=http)
    assert len(calls)==2 and plan.resources[0].checksum_scope=='metadata'
    assert not list(tmp_path.iterdir())
    reads=[]
    def reader(item,longitude,latitude):
        reads.append(item['id'])
        return dict(dn=2000,scl=4,row=1,col=2,scl_row=0,scl_col=1,bbox=[lon,lat,lon+.00001,lat+.00001],longitude=lon,latitude=lat,native_crs='EPSG:32613')
    stream=sentinel_samples(plan,reader=reader)
    assert not reads
    sample=next(stream)
    assert sample.record.value==2000 and sample.native_indices==(1,2,0,1)
    assert reads==['S2-test'] and not list(tmp_path.iterdir())
    assert json.loads(plan.resources[0].metadata.native_metadata_json)['item']==item


def test_metadata_missing_calibration_and_unsafe_uri_fail(request_model):
    item=metadata(request_model)
    x0,y0,x1,y1=request_model.support.bbox
    def http(url,**kwargs):return {'license':'unknown'} if url.endswith('sentinel-2-l2a') else {'features':[item]}
    del item['assets']['nir']['raster:bands'][0]['offset']
    with pytest.raises(ValueError,match='explicit scale'):
        plan_sentinel(request_model,x0,y0,http=http)
    item['assets']['nir']['href']='https://unknown.example/B08.tif'
    with pytest.raises(ValueError,match='COG access'):
        plan_sentinel(request_model,x0,y0,http=http)


def test_raster_access_reads_only_one_by_one_windows(monkeypatch,request_model):
    """Exercise the real reader against an in-memory rasterio protocol double."""
    import sys
    from types import ModuleType,SimpleNamespace
    from contextlib import nullcontext
    from dataset_prototype.real_data import read_sentinel_pixel
    reads=[];env=[]
    class Array:
        def __init__(self,value):self.value=value
        def __getitem__(self,index):assert index==(0,0);return self.value
    class Dataset:
        width=10;height=10;crs='EPSG:4326';transform='test-transform'
        def __init__(self,uri):self.uri=uri
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def index(self,x,y):return 1,2
        def xy(self,row,col):return 0,0
        def read(self,band,*,window):
            assert band==1 and window.width==window.height==1
            reads.append((self.uri,window))
            return Array(4 if self.uri.endswith('SCL.tif') else 2000)
    rasterio=ModuleType('rasterio')
    rasterio.open=Dataset
    rasterio.Env=lambda **kwargs: (env.append(kwargs) or nullcontext())
    warp=ModuleType('rasterio.warp');warp.transform=lambda src,dst,x,y:(x,y)
    warp.transform_bounds=lambda src,dst,*bounds,**kwargs:bounds
    windows=ModuleType('rasterio.windows')
    windows.Window=lambda col,row,width,height:SimpleNamespace(col_off=col,row_off=row,width=width,height=height)
    windows.bounds=lambda window,transform:(0,0,.0001,.0001)
    for name,module in [('rasterio',rasterio),('rasterio.warp',warp),('rasterio.windows',windows)]:
        monkeypatch.setitem(sys.modules,name,module)
    result=read_sentinel_pixel(metadata(request_model),0,0)
    assert result['dn']==2000 and result['scl']==4 and len(reads)==2
    assert env[0]['GDAL_DISABLE_READDIR_ON_OPEN']=='EMPTY_DIR'


def test_normalized_calibration_cannot_disagree_with_native_metadata(request_model):
    from dataset_prototype.stream_sources import validated_native
    item=metadata(request_model)
    def http(url,**kwargs):return {'license':'CC-BY-4.0'} if url.endswith('sentinel-2-l2a') else {'features':[item]}
    x0,y0,_,_=request_model.support.bbox
    plan=plan_sentinel(request_model,x0,y0,http=http)
    binding=plan.bindings[0]
    source=binding.source.model_copy(update={'metadata':binding.source.metadata.model_copy(update={'calibration_offset':0})})
    binding=binding.model_copy(update={'source':source})
    with pytest.raises(ValueError,match='normalized source disagrees'):
        validated_native(binding)
