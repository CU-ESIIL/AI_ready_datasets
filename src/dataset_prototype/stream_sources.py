"""Metadata-only Sentinel planning and lazy native-pixel access without snapshots."""
from datetime import datetime, timezone
import json
from urllib.parse import urlsplit
from .contracts import SourceResource, Variable, Metadata, Rights, Support, RawObservation, digest
from .stream_contracts import StreamPlan, StreamBinding, StreamSample
from .real_data import EARTH_SEARCH, SENTINEL_TERMS, read_sentinel_pixel
from .network import request_json


def validate_assets(item):
    for key in ('nir','scl'):
        uri=urlsplit(item['assets'][key]['href'])
        if uri.scheme!='https' or uri.hostname!='sentinel-cogs.s3.us-west-2.amazonaws.com' or uri.username or uri.password or uri.port not in {None,443} or not uri.path.endswith('.tif'):
            raise ValueError('unexpected Sentinel COG access location')


def plan_sentinel(request,longitude,latitude,*,max_items=2,max_cloud=20,http=request_json):
    if not 1<=max_items<=10 or not 0<=max_cloud<=100:
        raise ValueError('bounded discovery requires 1..10 items and cloud threshold 0..100')
    x0,y0,x1,y1=request.support.bbox
    if not x0<=longitude<=x1 or not y0<=latitude<=y1:
        raise ValueError('sample point outside requested extent')
    collection=http(f'{EARTH_SEARCH}/collections/sentinel-2-l2a')
    query={'collections':['sentinel-2-l2a'],'intersects':{'type':'Point','coordinates':[longitude,latitude]},
           'datetime':f'{request.support.start.isoformat()}/{request.support.end.isoformat()}',
           'limit':max_items,'query':{'eo:cloud_cover':{'lte':max_cloud}}}
    response=http(f'{EARTH_SEARCH}/search',payload=query)
    bindings=[]
    for item in response.get('features',[])[:max_items]:
        validate_assets(item)
        p=item['properties']
        if p.get('platform') not in {'sentinel-2a','sentinel-2b','sentinel-2c'}:
            raise ValueError('unexpected satellite platform')
        if p.get('eo:cloud_cover',101)>max_cloud:continue
        band=item['assets']['nir'].get('raster:bands',[{}])[0]
        if band.get('scale') is None or band.get('offset') is None or band.get('nodata')!=0:
            raise ValueError('explicit scale, offset and supported nodata metadata required')
        when=datetime.fromisoformat(p['datetime'].replace('Z','+00:00'))
        license_id=item.get('license',collection.get('license','unknown'))
        known=license_id=='proprietary' and any(l.get('rel')=='license' and l.get('href') in {SENTINEL_TERMS,'https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice'} for l in collection.get('links',[]))
        permitted=known or license_id in {'CC-BY-4.0','CC0-1.0'}
        native={'item':item,'collection':collection,'query':query}
        source=SourceResource(source_id='Sentinel-2',dataset='Sentinel-2 L2A / Earth Search',asset_id=item['id']+':B08',
            version=f"{item['id']};processing_baseline={p.get('s2:processing_baseline','not supplied')}",uri=item['assets']['nir']['href'],modality='satellite',
            variables=(Variable(name='B08_DN',definition='Sentinel-2 L2A bottom-of-atmosphere NIR band 8 encoded digital number',unit='DN',measurement_method='MSI band 8 L2A native pixel; stored digital number'),),
            support=Support(bbox=tuple(item['bbox'][:4]),start=when,end=when,spatial='10 m native-CRS pixel; scene bounding extent, per-sample footprint in lineage',temporal='instantaneous'),
            metadata=Metadata(fixture=False,description='Metadata-only plan. Explicit calibration required; SCL codes 4/5/6 and nonzero DN required at read time.',platform=p['platform'],sensor=','.join(p.get('instruments',[])),stac_version=item['stac_version'],original_identifier=item['id'],native_metadata_json=json.dumps(native,sort_keys=True),calibration_scale=band['scale'],calibration_offset=band['offset']),
            rights=Rights(license='Copernicus Sentinel Data Legal Notice; STAC label=proprietary' if known else license_id,
                attribution=f'Contains modified Copernicus Sentinel data ({when.year}); accessed via Element 84 Earth Search.',derivative_use=True if permitted else None,redistribution=True if permitted else None),
            checksum=digest(native),checksum_scope='metadata',retrieved_at=datetime.now(timezone.utc),
            provenance=(EARTH_SEARCH,item['assets']['nir']['href'],item['assets']['scl']['href'],f'collection-license:{license_id}','Metadata checksum is not a checksum of remote raster bytes'))
        target=Variable(name='B08_reflectance',definition='Sentinel-2 L2A bottom-of-atmosphere NIR band 8 reflectance calculated using documented asset scale and offset',unit='1',measurement_method='MSI band 8 L2A native pixel; documented scale/offset calibration')
        bindings.append(StreamBinding(binding_id=item['id'],source=source,source_variable='B08_DN',target=target,longitude=longitude,latitude=latitude))
    if not bindings:raise ValueError('no matching metadata; no synthetic fallback')
    return StreamPlan(question='Calibrate Sentinel-2 B08 DN into reflectance using documented scale/offset, preserving native support; stream directly into reference features. '+request.question,reader='sentinel-pixel',bindings=tuple(bindings))



def validated_native(binding):
    source=binding.source
    native=json.loads(source.metadata.native_metadata_json)
    if source.checksum_scope!='metadata' or digest(native)!=source.checksum:
        raise ValueError('source metadata identity changed')
    item=native['item'];validate_assets(item)
    band=item['assets']['nir'].get('raster:bands',[{}])[0]
    when=datetime.fromisoformat(item['properties']['datetime'].replace('Z','+00:00'))
    if (source.uri!=item['assets']['nir']['href'] or source.asset_id!=item['id']+':B08'
        or source.metadata.original_identifier!=item['id']
        or source.metadata.calibration_scale!=band.get('scale')
        or source.metadata.calibration_offset!=band.get('offset')
        or band.get('nodata')!=0 or binding.source_variable!='B08_DN'
        or source.variables[0].unit!='DN' or source.support.start!=when or source.support.end!=when
        or source.support.bbox!=tuple(item['bbox'][:4])):
        raise ValueError('normalized source disagrees with native calibration, identity or support metadata')
    return item


def sentinel_samples(plan,*,reader=read_sentinel_pixel):
    """One bounded NIR/SCL window per binding; fail explicitly on rejected quality."""
    if plan.reader!='sentinel-pixel':raise ValueError('not a Sentinel plan')
    for binding in plan.bindings:
        source=binding.source
        item=validated_native(binding)
        result=reader(item,binding.longitude,binding.latitude)
        if result['scl'] not in {4,5,6} or result['dn']==0:
            raise ValueError('candidate rejected by SCL/nodata; no interpolation or synthetic fallback')
        yield StreamSample(binding_id=binding.binding_id,sequence=0,evidence_digest=digest(result),evidence_scope='extracted native DN/SCL window evidence JSON; not full remote asset',
            spatial_bbox=tuple(result['bbox']),native_crs=result['native_crs'],native_indices=(result['row'],result['col'],result['scl_row'],result['scl_col']),
            record=RawObservation(record_id=source.asset_id+f":{result['row']}:{result['col']}",asset_id=source.asset_id,variable=binding.source_variable,value=result['dn'],longitude=result['longitude'],latitude=result['latitude'],start=source.support.start,end=source.support.end,quality_flag=f"SCL={result['scl']};native_DN"))
