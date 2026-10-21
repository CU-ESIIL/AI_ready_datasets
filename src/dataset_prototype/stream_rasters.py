"""Upstream native raster access → reviewed harmonization output stream.

The MOSAIKS embedding module has no dependency on this source-specific adapter.
"""
from contextlib import ExitStack
import math
from .harmonized_rasters import authorize_context,harmonize_window
from .stream_sources import validated_native


def sentinel_harmonized_tiles(context,*,side=16,grid=8):
    context=authorize_context(context)
    if context.plan.reader!='sentinel-raster' or len(context.plan.bindings)!=1:
        raise ValueError('first bounded raster source supports one reviewed native NIR binding')
    from .mosaiks_pipeline import RasterLayout
    layout=RasterLayout.model_validate_json(context.plan.raster_layout_json)
    if (side,grid)!=(layout.side,layout.grid):raise ValueError('window layout differs from reviewed raster plan')
    if not 4<=side<=32 or not 6<=grid<=8:raise ValueError('small-area example requires side 4..32 and grid 6..8')
    from .mosaiks import array_digest
    import numpy as np
    import rasterio
    from rasterio.windows import Window,bounds,from_bounds
    from rasterio.warp import transform,transform_bounds
    binding=context.plan.bindings[0];item=validated_native(binding);source=binding.source
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',GDAL_CACHEMAX=8*1024*1024,CPL_VSIL_CURL_CACHE_SIZE=1048576,VSI_CACHE=False,GDAL_HTTP_TIMEOUT=30):
        with ExitStack() as stack:
            band=stack.enter_context(rasterio.open(source.uri));mask=stack.enter_context(rasterio.open(item['assets']['scl']['href']))
            if not band.crs.is_projected or not np.allclose(band.res,(10,10)):raise ValueError('reviewed example requires native 10 m pixels in a projected CRS')
            x,y=transform('EPSG:4326',band.crs,[binding.longitude],[binding.latitude])
            row,col=band.index(x[0],y[0]);r0=row-grid*side//2;c0=col-grid*side//2
            if min(r0,c0)<0 or r0+grid*side>band.height or c0+grid*side>band.width:raise ValueError('small AOI crosses source raster boundary')
            # Spatial blocks with an unused one-column buffer. Calibration sees train only.
            layouts=[]
            for c in range(grid):
                if c==grid//2:continue
                split='train' if c<grid//2 else 'validation' if c==grid//2+1 else 'test'
                for r in range(grid):layouts.append((split,r,c))
            layouts.sort(key=lambda x:{'train':0,'validation':1,'test':2}[x[0]])
            for split,r,c in layouts:
                window=Window(c0+c*side,r0+r*side,side,side)
                native_bounds=bounds(window,band.transform)
                mb=transform_bounds(band.crs,mask.crs,*native_bounds)
                mw=from_bounds(*mb,transform=mask.transform)
                left=math.floor(mw.col_off);top=math.floor(mw.row_off)
                right=math.ceil(mw.col_off+mw.width);bottom=math.ceil(mw.row_off+mw.height)
                if min(left,top)<0 or right>mask.width or bottom>mask.height:raise ValueError('quality coverage unavailable')
                quality=mask.read(1,window=Window(left,top,right-left,bottom-top))
                if not np.isin(quality,[4,5,6]).all():raise ValueError(f'quality rejected tile {r},{c}; no silent filtering')
                raw=band.read(1,window=window)
                if np.any(raw==0):raise ValueError('nodata in tile; no imputation')
                bbox=transform_bounds(band.crs,'EPSG:4326',*native_bounds)
                lineage={'native_transform':list(band.transform)[:6],'bbox':bbox,'native_crs':str(band.crs),'native_window':[int(window.row_off),int(window.col_off),side,side],
                    'source_assets':[source.asset_id],'datetime_start':source.support.start.isoformat(),'datetime_end':source.support.end.isoformat(),
                    'quality_policy':'All native SCL cells covering this NIR window must be 4/5/6; no mask resampling',
                    'quality_classes':sorted(int(q) for q in np.unique(quality)),'quality_evidence_digest':array_digest(quality),
                    'quality_native_window':[top,left,bottom-top,right-left],'quality_native_crs':str(mask.crs)}
                yield harmonize_window({(source.asset_id,binding.source_variable):raw},context=context,patch_id=f'{source.asset_id}:{r}:{c}',
                    lineage=lineage,split=split,spatial_group=f'native-grid-column:{c}')
