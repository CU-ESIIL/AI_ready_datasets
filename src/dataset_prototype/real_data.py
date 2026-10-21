"""Actual STAC discovery/windowed Sentinel reads and auditable local snapshots.

No reflectance calibration, cloud interpolation, field/pixel join, or support
conversion is hidden in ingestion. Raw digital numbers remain digital numbers.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
from .contracts import Contract, ScientificRequest, SourceResource, RawObservation, Metadata, Variable, Rights, Support, digest
from .network import request_json

EARTH_SEARCH = "https://earth-search.aws.element84.com/v1"
SENTINEL_TERMS = "https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice"


class EvidenceFile(Contract):
    path: str
    sha256: str
    role: str


class Snapshot(Contract):
    resources: tuple[SourceResource, ...]
    records: tuple[RawObservation, ...]
    evidence: tuple[EvidenceFile, ...]
    content_digest: str
    acquisition: str


def save_snapshot(root, resources, records, evidence, acquisition):
    root = Path(root)
    fields = {"resources": [r.model_dump(mode="json") for r in resources], "records": [r.model_dump(mode="json") for r in records]}
    snapshot = Snapshot(resources=tuple(resources), records=tuple(records), evidence=tuple(evidence), content_digest=digest(fields), acquisition=acquisition)
    with (root / "snapshot.json").open("x") as handle:
        handle.write(snapshot.model_dump_json(indent=2) + "\n")
    return snapshot


class SnapshotClient:
    """Offline re-use of acquired real observations, not a MockMESA integration."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.snapshot = Snapshot.model_validate_json((self.root / "snapshot.json").read_text())
        self.resources = self.snapshot.resources
        fields = {"resources": [r.model_dump(mode="json") for r in self.resources], "records": [r.model_dump(mode="json") for r in self.snapshot.records]}
        if digest(fields) != self.snapshot.content_digest:
            raise ValueError("snapshot records or source metadata have changed")
        checksums = set()
        for evidence in self.snapshot.evidence:
            path = (self.root / evidence.path).resolve()
            if not path.is_relative_to(self.root) or sha256(path.read_bytes()).hexdigest() != evidence.sha256:
                raise ValueError("snapshot evidence missing, escaped root, or changed")
            checksums.add(evidence.sha256)
        if any(r.checksum not in checksums for r in self.resources):
            raise ValueError("source checksum has no verified evidence file")
        if any(row.asset_id not in {r.asset_id for r in self.resources} for row in self.snapshot.records):
            raise ValueError("snapshot contains unknown source records")

    def search(self, request):
        from .discovery import relevant
        return tuple(r for r in self.resources if relevant(request, r))

    def describe(self, asset_id):
        return next((r for r in self.resources if r.asset_id == asset_id), None) or self._missing(asset_id)

    def _missing(self, asset_id):
        raise LookupError(f"source unavailable: {asset_id}")

    def fetch(self, asset_id):
        self.describe(asset_id)
        return tuple(r for r in self.snapshot.records if r.asset_id == asset_id)


def _evidence(root, name, content, role):
    with (root / name).open("xb") as handle:
        handle.write(content)
    return EvidenceFile(path=name, sha256=sha256(content).hexdigest(), role=role)


def acquire_sentinel(request: ScientificRequest, longitude, latitude, output, *, max_cloud=20, max_items=5, http=request_json, reader=None):
    """Search a bounded interval and read one NIR/SCL pixel per candidate.

    Scene cloud percentage is only a prefilter; accepted SCL codes are 4
    (vegetation), 5 (not vegetated), and 6 (water). No substitution/interpolation.
    """
    if not (1 <= max_items <= 10 and 0 <= max_cloud <= 100):
        raise ValueError("limit candidates to 1..10 and scene cloud threshold to 0..100")
    if not (request.support.bbox[0] <= longitude <= request.support.bbox[2] and request.support.bbox[1] <= latitude <= request.support.bbox[3]):
        raise ValueError("sample point outside requested extent")
    if "satellite" not in request.modalities or "B08_DN" not in request.variables:
        raise ValueError("request must explicitly include satellite modality and B08_DN")
    query = {"collections": ["sentinel-2-l2a"], "bbox": list(request.support.bbox),
             "datetime": f"{request.support.start.isoformat()}/{request.support.end.isoformat()}",
             "limit": max_items, "query": {"eo:cloud_cover": {"lte": max_cloud}}}
    collection = http(f"{EARTH_SEARCH}/collections/sentinel-2-l2a")
    response = http(f"{EARTH_SEARCH}/search", payload=query)
    features = response.get("features", [])
    if not features:
        raise ValueError("no matching real Sentinel items; no synthetic fallback")
    root = Path(output)
    root.mkdir(parents=True, exist_ok=False)
    evidence = [_evidence(root, "request.json", request.model_dump_json(indent=2).encode(), "scientific request"),
                _evidence(root, "collection.json", json.dumps(collection, sort_keys=True).encode(), "native STAC collection and license evidence"),
                _evidence(root, "search.json", json.dumps({"query":query,"response":response},sort_keys=True).encode(), "native STAC query and response")]
    resources, records = [], []
    read = reader or read_sentinel_pixel
    rejections = []
    for i, item in enumerate(features[:max_items]):
        properties = item["properties"]
        if properties.get("eo:cloud_cover", 101) > max_cloud:
            continue
        if properties.get("platform") not in {"sentinel-2a", "sentinel-2b", "sentinel-2c"}:
            raise ValueError("unexpected satellite platform")
        from urllib.parse import urlsplit
        for key in ("nir", "scl"):
            parsed = urlsplit(item["assets"][key]["href"])
            if parsed.scheme != "https" or parsed.hostname != "sentinel-cogs.s3.us-west-2.amazonaws.com" or parsed.username or parsed.password or not parsed.path.endswith(".tif"):
                raise ValueError("unexpected Sentinel COG access location")
        result = read(item, longitude, latitude)
        if result["scl"] not in {4, 5, 6} or result["dn"] == 0:
            rejections.append({"item": item["id"], "reason": "SCL/nodata rejected", "scl":result["scl"]})
            continue
        payload = json.dumps(result, sort_keys=True, allow_nan=False).encode()
        window = _evidence(root, f"window-{i}.json", payload, "extracted pixel: native DN/SCL, indices, CRS, and footprint")
        evidence.append(window)
        when = datetime.fromisoformat(properties["datetime"].replace("Z", "+00:00"))
        band = item["assets"]["nir"].get("raster:bands", [{}])[0]
        asset_id = f"{item['id']}:B08:{result['row']}:{result['col']}"
        # Do not infer one universal license from the platform name. Keep the
        # collection license and its native link evidence alongside every sample.
        license_id = item.get("license", collection.get("license", "unknown"))
        known_terms = license_id == "proprietary" and any(link.get("href") in {"https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice", SENTINEL_TERMS} and link.get("rel") == "license" for link in collection.get("links", []))
        license_open = license_id in {"CC-BY-4.0", "CC0-1.0"} or known_terms
        rights = Rights(license=("Copernicus Sentinel Data Legal Notice; STAC label=proprietary" if known_terms else license_id), attribution=f"Contains modified Copernicus Sentinel data ({when.year}); accessed via Element 84 Earth Search. Extraction only; raw DN retained.",
                        derivative_use=True if license_open else None, redistribution=True if license_open else None)
        source = SourceResource(source_id="Sentinel-2", dataset="Sentinel-2 L2A / Earth Search", asset_id=asset_id,
            version=f"{item['id']};processing_baseline={properties.get('s2:processing_baseline','not supplied')};pixel-extractor-v1",
            uri=item["assets"]["nir"]["href"], modality="satellite",
            variables=(Variable(name="B08_DN", definition="Sentinel-2 L2A bottom-of-atmosphere NIR band 8 encoded digital number; physical reflectance requires the asset scale and offset", unit="DN", measurement_method="MSI band 8 L2A pixel; uncalibrated stored digital number"),),
            support=Support(bbox=result["bbox"],start=when,end=when,spatial="10 m native-CRS pixel footprint",temporal="instantaneous"),
            metadata=Metadata(fixture=False, description="Actual windowed COG read; SCL vegetation/nonvegetated/water only. Not field-equivalent support.",platform=properties["platform"],sensor=",".join(properties.get("instruments",[])),
                stac_version=item["stac_version"],original_identifier=item["id"],native_metadata_json=json.dumps(item,sort_keys=True),calibration_scale=band.get("scale"),calibration_offset=band.get("offset"),quality_mask_value=result["scl"]),
            rights=rights, checksum=window.sha256, checksum_scope="extracted_window", retrieved_at=datetime.now(timezone.utc),
            provenance=(EARTH_SEARCH, item["assets"]["nir"]["href"], item["assets"]["scl"]["href"], f"collection-license:{license_id}","rasterio transforms native pixel coordinate metadata to EPSG:4326; raster values are not resampled", "window checksum covers extracted evidence JSON, not entire remote COG"))
        resources.append(source)
        records.append(RawObservation(record_id=asset_id,asset_id=asset_id,variable="B08_DN",value=result["dn"],longitude=result["longitude"],latitude=result["latitude"],start=when,end=when,quality_flag=f"SCL={result['scl']};raw_DN;no_calibration"))
    evidence.append(_evidence(root,"rejections.json",json.dumps(rejections).encode(),"explicit rejected candidate evidence"))
    if not resources:
        raise ValueError(f"all candidate pixels rejected; evidence retained at {root}; no synthetic fallback")
    return save_snapshot(root,resources,records,evidence,"live Earth Search STAC + Sentinel COG range reads; extracted_window checksums")


def read_sentinel_pixel(item, longitude, latitude):
    import rasterio
    from rasterio.warp import transform, transform_bounds
    from rasterio.windows import Window, bounds
    # Disable directory scans and bound remote reads to COG TIFFs; GDAL reads the
    # compressed blocks necessary for these windows, not complete scenes.
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif", GDAL_HTTP_TIMEOUT=30, GDAL_HTTP_MAX_RETRY=1):
        with rasterio.open(item["assets"]["nir"]["href"]) as dataset:
            x,y=transform("EPSG:4326",dataset.crs,[longitude],[latitude])
            row,col=dataset.index(x[0],y[0])
            if not (0<=row<dataset.height and 0<=col<dataset.width):
                raise ValueError("requested point outside raster")
            window=Window(col,row,1,1)
            dn=int(dataset.read(1,window=window)[0,0])
            footprint=transform_bounds(dataset.crs,"EPSG:4326",*bounds(window,dataset.transform),densify_pts=21)
            cx,cy=dataset.xy(row,col)
            lon,lat=transform(dataset.crs,"EPSG:4326",[cx],[cy])
            native_crs=str(dataset.crs)
        with rasterio.open(item["assets"]["scl"]["href"]) as dataset:
            x,y=transform("EPSG:4326",dataset.crs,[longitude],[latitude])
            sr,sc=dataset.index(x[0],y[0])
            scl=int(dataset.read(1,window=Window(sc,sr,1,1))[0,0])
    return dict(dn=dn,scl=scl,row=row,col=col,scl_row=sr,scl_col=sc,bbox=list(footprint),longitude=lon[0],latitude=lat[0],native_crs=native_crs)
