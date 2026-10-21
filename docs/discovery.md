# Discovery and Access

`discovery.run(request, client)` is independently callable. A request specifies a
question, WGS84 extent, timezone-aware interval, variables, modalities, and optional
track. Discovery filters by bounding-box intersection, overlapping intervals,
modality, and exact declared variable identifiers. It does not equate similar names.
The orchestrator additionally requires every configured variable to be present.

A `SourceResource` preserves dataset, source, asset/version, URI, checksum,
retrieval time, variable definitions/units/method/entity/ontology, spatial and
temporal support, modality, sensor/platform metadata, provenance, and rights.
Rights distinguish license, attribution, derivative permission, redistribution,
and access restrictions. No blanket license is inferred from a source name.

`MockMESAClient` reads `data/fixtures/catalog.json`, validates metadata, verifies
asset bytes before parsing, and exposes `search`, `describe`, `fetch`, and
`get_provenance`. Fixture paths cannot escape the fixture root. Registration is
intentionally unavailable for the immutable fixture catalog. Duplicate asset IDs,
conflicting results, missing metadata, unavailable assets, and checksum changes
fail explicitly. Empty searches return a warning.

```python
from pathlib import Path
from dataset_prototype.adapters import MockMESAClient
from dataset_prototype.contracts import ScientificRequest
from dataset_prototype.discovery import run

client = MockMESAClient(Path("data/fixtures"))
request = ScientificRequest.model_validate_json(Path("run/food_security/request.json").read_text())
result = run(request, client)
```

```bash
prototype discover run/food_security/request.json --output /tmp/discovery.json
```

MESA, local files, and STAC transports must normalize their results into
this same source contract. Discovery filtering establishes candidacy only; it
does not establish semantic compatibility or observational support equivalence.

The [real workflow](real-data-agents.md) adds actual Sentinel STAC/windowed COG
acquisition and a checksum-verifying `SnapshotClient`. `NEONClient` implements
authenticated native file discovery/download but normalization needs verified
sensor and variable metadata. The tested unauthenticated NEON data route returns
403; there is no fixture fallback.
