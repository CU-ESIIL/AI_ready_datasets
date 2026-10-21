"""Local mock transport and an honest, unavailable external MESA boundary."""
from pathlib import Path
from hashlib import sha256
from typing import Protocol
from .contracts import SourceResource, RawObservation, ScientificRequest


class AccessClient(Protocol):
    def search(self, request: ScientificRequest) -> tuple[SourceResource, ...]: ...
    def describe(self, asset_id: str) -> SourceResource: ...
    def fetch(self, asset_id: str) -> tuple[RawObservation, ...]: ...


class MESAClient:
    """No verified MESA API is available to this prototype. Never guesses URLs."""
    def _unavailable(self, *args, **kwargs):
        raise NotImplementedError("MESA interface unverified; configure a documented transport before enabling real access")

    search = describe = fetch = register = get_provenance = _unavailable


class MockMESAClient:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        import json
        self.resources = tuple(SourceResource.model_validate(r) for r in json.loads((self.root / "catalog.json").read_text()))
        ids = [r.asset_id for r in self.resources]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate asset identifiers")

    def search(self, request):
        from .discovery import relevant
        return tuple(r for r in self.resources if relevant(request, r))

    def describe(self, asset_id):
        for resource in self.resources:
            if resource.asset_id == asset_id:
                return resource
        raise LookupError(f"unavailable resource: {asset_id}")

    def fetch(self, asset_id):
        import json
        resource = self.describe(asset_id)
        path = (self.root / resource.uri).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("fixture URI escapes fixture directory")
        content = path.read_bytes()
        if sha256(content).hexdigest() != resource.checksum:
            raise ValueError("source checksum mismatch")
        records = tuple(RawObservation.model_validate(x) for x in json.loads(content))
        if any(r.asset_id != asset_id or r.variable not in {v.name for v in resource.variables} for r in records):
            raise ValueError("asset contents violate source metadata")
        if len({r.record_id for r in records}) != len(records):
            raise ValueError("duplicate source record identifiers")
        return records

    def register(self, resource):
        raise NotImplementedError("immutable fixture catalog; registration is a planned external capability")

    def get_provenance(self, asset_id):
        return self.describe(asset_id).provenance
