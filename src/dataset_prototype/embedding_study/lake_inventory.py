"""Complete stat/schema inventory with zero scientific array/observation reads."""
import csv,json,struct,math
from pathlib import Path
import sqlite3
from collections import Counter
from datetime import datetime,timezone
from ..contracts import digest


def safe(value):
    if isinstance(value,bytes):return value.decode('utf-8',errors='replace')
    if hasattr(value,'tolist'):return safe(value.tolist())
    if isinstance(value,(list,tuple)):return [safe(v) for v in value]
    if isinstance(value,float) and not math.isfinite(value):return {'nonfinite_metadata':str(value)}
    if isinstance(value,(str,int,float,bool)) or value is None:return value
    return str(value)


def nc3_header(path):
    """XDR header only. Never seek to variable data or read coordinate arrays."""
    with Path(path).open('rb') as f:
        magic=f.read(4)
        if magic not in (b'CDF\x01',b'CDF\x02'):raise ValueError('not supported NetCDF3 header')
        def read(n):
            if n<0 or f.tell()+n>2*1024*1024:raise ValueError('metadata header budget exceeded')
            data=f.read(n)
            if len(data)!=n:raise ValueError('truncated metadata')
            return data
        def u32():return struct.unpack('>I',read(4))[0]
        def name():
            n=u32();text=read(n).decode('utf-8',errors='replace');read((-n)%4);return text
        def listing(tag):
            got,count=u32(),u32()
            if got not in (0,tag) or count>10000 or (got==0 and count!=0):raise ValueError('invalid NetCDF metadata list')
            return count
        widths={1:1,2:1,3:2,4:4,5:4,6:8};formats={1:'b',3:'h',4:'i',5:'f',6:'d'}
        def attributes():
            out={}
            for _ in range(listing(12)):
                key=name();kind,n=u32(),u32()
                if kind not in widths:raise ValueError('unrecognized attribute type')
                data=read(n*widths[kind]);read((-len(data))%4)
                if kind==2:value=data.decode('utf-8',errors='replace').rstrip('\x00')
                else:
                    values=struct.unpack('>'+formats[kind]*n,data);value=values[0] if n==1 else list(values)
                out[key]=safe(value)
            return out
        records=u32();dims=[]
        for _ in range(listing(10)):
            key=name();length=u32();dims.append({'name':key,'length':records if length==0 else length,'unlimited':length==0})
        attrs=attributes();variables=[]
        for _ in range(listing(11)):
            key=name();nd=u32()
            if nd>32:raise ValueError('invalid variable rank')
            indices=[u32() for _ in range(nd)];va=attributes();kind=u32();size=u32();offset=struct.unpack('>Q' if magic[-1]==2 else '>I',read(8 if magic[-1]==2 else 4))[0]
            if any(i>=len(dims) for i in indices):raise ValueError('invalid dimension index')
            variables.append({'name':key,'dimensions':[dims[i]['name'] for i in indices],'shape':[dims[i]['length'] for i in indices],'native_type':kind,'attributes':va})
        return {'format':'NetCDF3','dimensions':dims,'variables':variables,'attributes':attrs,'header_bytes_read':f.tell(),'data_values_read':0}


def netcdf_metadata(path):
    with Path(path).open('rb') as f:signature=f.read(8)
    if signature.startswith(b'CDF'):return nc3_header(path)
    if signature==b'\x89HDF\r\n\x1a\n':
        import h5py
        result={'format':'NetCDF4/HDF5','variables':[],'data_values_read':0}
        with h5py.File(path,'r') as f:
            result['attributes']={str(k):safe(v) for k,v in f.attrs.items()}
            def visit(name,obj):
                if isinstance(obj,h5py.Dataset):result['variables'].append({'name':name,'shape':list(obj.shape),'native_type':str(obj.dtype),'attributes':{str(k):safe(v) for k,v in obj.attrs.items()}})
            f.visititems(visit)
        return result
    raise ValueError('unrecognized NetCDF container')


def schema_metadata(path):
    suffix=path.suffix.lower()
    if suffix=='.parquet':
        import pyarrow.parquet as pq
        f=pq.ParquetFile(path)
        return {'status':'METADATA_INSPECTED','scope':'footer only','rows_from_footer':f.metadata.num_rows,
          'row_groups':f.metadata.num_row_groups,'fields':[{'name':v.name,'type':str(v.type)} for v in f.schema_arrow],'schema':str(f.schema_arrow)}
    if suffix=='.gpkg':
        with sqlite3.connect(path.as_uri()+'?mode=ro&immutable=1',uri=True) as db:
            contents=db.execute('SELECT table_name,data_type,srs_id,min_x,min_y,max_x,max_y FROM gpkg_contents').fetchall()
            result=[]
            for name,kind,srs,*extent in contents:
                cols=db.execute('PRAGMA table_info("'+name.replace('"','""')+'")').fetchall()
                result.append({'table':name,'type':kind,'native_srs_id':srs,'extent_from_catalog':extent,
                  'fields':[{'name':c[1],'type':c[2]} for c in cols]})
            srs=db.execute('SELECT srs_id,organization,organization_coordsys_id,definition FROM gpkg_spatial_ref_sys').fetchall()
        return {'status':'METADATA_INSPECTED','scope':'GeoPackage schema/catalog/CRS only','tables':result,
          'crs':[{'native_srs_id':a,'organization':b,'code':c,'definition':d} for a,b,c,d in srs]}
    if suffix=='.nc':return {'status':'METADATA_INSPECTED','scope':'container header/attributes only',**netcdf_metadata(path)}
    # A CSV/JSON file may begin with an observation, so never guess that its first
    # record is a safe header or treat arbitrary JSON as metadata.
    return {'status':'NOT_INSPECTED','scope':'stat/inventory only','reason':'no safe approved metadata-only schema reader for this format'}


def inventory(lake):
    lake=Path(lake).resolve();files=lake/'files';package=json.loads((lake/'manifest.json').read_text())
    with (lake/'file_manifest.csv').open() as f:declared={r['path']:r for r in csv.DictReader(f)}
    catalog=[];errors=[]
    for path in sorted(files.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(lake).as_posix();record=declared.get(relative,{})
        entry={'relative_path':relative,'file_type':path.suffix.lower().lstrip('.'),'size_bytes':path.stat().st_size,
          'source_inventory_role':record.get('role'),'source_dataset':None,'source_version':None,
          'package_release':package['release_id'],'reported_sha256':record.get('sha256'),
          'current_complete_checksum':None,'checksum_status':'HISTORICAL_REPORTED_NOT_CURRENTLY_VERIFIED',
          'inventory_size_matches':int(record['size_bytes'])==path.stat().st_size if record else None,
          'schema':None,'temporal_coverage':None,'spatial_coverage':None,'event_identifier_candidates':[],
          'observation_support':'NEEDS_REVIEW','quality_field_candidates':[],
          'license_evidence':'package README retains source-specific terms; not reviewed permission',
          'processing_lineage':'historical role/source path in file_manifest.csv; scientific mapping not inferred',
          'source_path_from_manifest':record.get('source_path'),'derived_product':record.get('role') in ('repository-product','derived-lakehouse','lakehouse')}
        if not path.resolve().is_relative_to(lake):
            entry['metadata']={'status':'BLOCKED','reason':'symlink escapes canonical lake'}
        else:
            try:entry['metadata']=schema_metadata(path)
            except Exception as exc:
                entry['metadata']={'status':'METADATA_ERROR','error_type':type(exc).__name__};errors.append(relative)
        meta=entry['metadata'];fields=meta.get('fields',[])
        for table in meta.get('tables',[]):fields+=table.get('fields',[])
        if fields:
            entry['schema']=fields;names=[f['name'] for f in fields]
            entry['event_identifier_candidates']=[n for n in names if n in ('id','event_id','fire_id')]
            entry['quality_field_candidates']=[n for n in names if any(k in n.lower() for k in ('quality','flag','available','failure','qa'))]
        attrs=meta.get('attributes',{});entry['temporal_coverage']={k:attrs[k] for k in ('time_coverage_start','time_coverage_end') if k in attrs} or None
        entry['spatial_coverage']={k:v for k,v in attrs.items() if k.startswith('geospatial_')} or ([t.get('extent_from_catalog') for t in meta.get('tables',[])] or None)
        if '/fired-cache/' in relative:entry['source_dataset']='FIRED (release-specific identity/terms unresolved)'
        elif '/gridmet-cache/' in relative:entry['source_dataset']='gridMET (native variable/version/support require review)'
        elif record.get('role')=='repository-product':entry['source_dataset']='repository derived/document product; not an independent source'
        catalog.append(entry)
    actual={r['relative_path'] for r in catalog};historical=set(declared)
    summary={'version':'fire-full-lake-inventory-v1','timestamp':datetime.now(timezone.utc).isoformat(),
      'canonical_lake':str(lake),'historical_files':package['file_count'],'historical_bytes':package['total_size_bytes'],
      'current_files_stat':len(catalog),'current_total_bytes_stat':sum(r['size_bytes'] for r in catalog),
      'missing_inventory_files':sorted(historical-actual),'uninventoried_files':sorted(actual-historical),
      'size_mismatches':[r['relative_path'] for r in catalog if r['inventory_size_matches'] is False],
      'formats':dict(Counter(r['file_type'] for r in catalog)),'schema_status':dict(Counter(r['metadata']['status'] for r in catalog)),
      'metadata_errors':errors,'observation_rows_read':0,'data_array_values_read':0,
      'eligibility_counts':{k:None for k in ('unique_fires','fire_days','event_histories','intervals','consecutive_transitions','three_day_sequences','seven_day_sequences','fourteen_day_sequences','thirty_day_sequences','complete_histories','spatially_supported_fires','environmentally_supported_fires')},
      'counts_scope':'Row-derived counts not measured before full-lake authorization. Footer counts are per-artifact metadata and must not be summed across overlapping products.'}
    return catalog,summary
