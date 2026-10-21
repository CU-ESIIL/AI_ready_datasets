"""Discovery knows requirements and source contracts, never encoders."""
from .contracts import ScientificRequest, SourceResource, DiscoveryCandidate, DiscoveryResult


def relevant(request: ScientificRequest, resource: SourceResource) -> bool:
    a, b = request.support, resource.support
    spatial = a.bbox[0] <= b.bbox[2] and b.bbox[0] <= a.bbox[2] and a.bbox[1] <= b.bbox[3] and b.bbox[1] <= a.bbox[3]
    temporal = (a.start <= b.start <= a.end) if b.start == b.end else (a.start <= b.end and b.start <= a.end) if a.start == a.end else (a.start < b.end and b.start < a.end)
    return spatial and temporal and resource.modality in request.modalities and bool(set(request.variables) & {v.name for v in resource.variables})


def run(request: ScientificRequest, client) -> DiscoveryResult:
    resources = client.search(request)
    unique = {}
    for r in resources:
        if not isinstance(r, SourceResource):
            raise TypeError("discovery adapter must return SourceResource")
        key = (r.asset_id, r.version)
        if key in unique and unique[key] != r:
            raise ValueError("conflicting duplicate source metadata")
        if relevant(request, r):
            unique[key] = r
    candidates = tuple(DiscoveryCandidate(resource=r, rationale="Metadata intersects requested location/time and declares requested variable/modality; scientific comparability remains unapproved.") for _, r in sorted(unique.items()))
    return DiscoveryResult(request=request, candidates=candidates, warnings=() if candidates else ("No matching resources",))
