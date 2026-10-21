"""Authenticated official NEON data-file access, without guessing sensor support.

This boundary retrieves native metadata/CSV bytes. Scientific normalization is
not inferred from filenames or site centroids; it needs verified variable and
sensor-position metadata before those records enter harmonization.
"""
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from hashlib import sha256
import os
import re
import json
from .network import request_json, request_bytes

BASE = "https://data.neonscience.org/api/v0"


class NEONClient:
    def __init__(self, *, token=None, http=request_json, download=request_bytes):
        self._token=token if token is not None else os.environ.get("NEON_API_TOKEN")
        if self._token is not None and (not self._token.strip() or any(c in self._token for c in "\r\n")):
            raise ValueError("NEON token has invalid header characters")
        self.http=http
        self.download=download

    def files(self, product, site, month, release):
        if not re.fullmatch(r"DP[1-4]\.\d{5}\.\d{3}",product) or not re.fullmatch(r"[A-Z]{4}",site) or not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])",month) or not re.fullmatch(r"RELEASE-\d{4}",release):
            raise ValueError("explicit valid product, site, month and release required")
        if not self._token:
            raise ValueError("NEON_API_TOKEN is required for NEON file discovery/download; never paste tokens into artifacts")
        url=f"{BASE}/data/{product}/{site}/{month}?{urlencode({'release':release})}"
        result=self.http(url,headers={"X-API-Token":self._token})
        if result.get("error") or not isinstance(result.get("data"),dict):
            raise ValueError("NEON returned an error or missing native data metadata")
        return result

    def acquire_file(self, product, site, month, release, filename, output, *, max_bytes=2_000_000):
        if not filename.endswith('.csv') or Path(filename).name!=filename:
            raise ValueError("select exactly one native CSV basename")
        metadata=self.files(product,site,month,release)
        candidates=[f for f in metadata['data'].get('files',[]) if f.get('name')==filename]
        if len(candidates)!=1:
            raise ValueError("filename must match exactly one provider metadata record")
        chosen=candidates[0]
        if int(chosen.get('size',max_bytes+1))>max_bytes:
            raise ValueError("NEON file exceeds configured byte limit or its size is unavailable")
        uri=chosen.get('url','')
        parsed=urlsplit(uri)
        if parsed.scheme!='https' or parsed.username or parsed.password:
            raise ValueError("NEON file reference must be HTTPS without embedded credentials")
        # Only the NEON API receives its token. Never forward it to a cloud host.
        headers={"X-API-Token":self._token} if parsed.hostname=='data.neonscience.org' else {}
        content=self.download(uri,headers=headers,max_bytes=max_bytes)
        if len(content) != int(chosen["size"]):
            raise ValueError("NEON download byte count disagrees with provider file size")
        root=Path(output);root.mkdir(parents=True,exist_ok=False)
        (root/filename).write_bytes(content)
        (root/'native_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
        report={"source":"NEON","product":product,"site":site,"month":month,"release":release,
            "file":filename,"sha256":sha256(content).hexdigest(),"bytes":len(content),
            "license":"CC-BY-4.0","license_evidence":"https://data.neonscience.org/data-api/",
            "attribution":f"NEON (National Ecological Observatory Network). {product}, {release}. Preserve provider citation and DOI from product/release metadata before scientific publication.",
            "status":"native CSV acquired; not yet normalized to scientific observations",
            "normalization_requirements":["variable definition/unit metadata","explicit selected sensor location/height and indices","quality flags and uncertainty","native interval definition"]}
        (root/'acquisition.json').write_text(json.dumps(report,indent=2)+'\n')
        return report
