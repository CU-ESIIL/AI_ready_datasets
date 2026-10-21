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


## Discover semantic evidence alongside assets

`discovery.run(request, client, semantic_registry=None)` now returns sources with
optional typed `SourceSemantics`: evidence records, concept candidates, extractor
identity and a source-metadata binding. Existing source records remain immutable.
Source definitions, identifiers, methods and declared support survive in provenance.
Absent semantics is omitted from serialization for legacy identity compatibility.

Normalized adapter metadata is marked deterministically derived; native Sentinel
band metadata retains explicit locations and source-documented classification.
A `ConceptCandidate` has a retrieval basis, evidence and confidence but no approved
relationship. Labels are insufficient to establish equivalence. Module 2 retains
all mapping and harmonization authority; source access and MOSAIKS remain separate.

The local `SemanticResourceRegistry` indexes resource records and explicit fixture
concepts behind a portal-independent protocol. External ontology resolvers remain
planned/configurable adapters; no ontology graph or source observations are fetched
by semantic enrichment. See [pipeline contracts and Sentinel regression](semantics/pipeline.md),
[landscape](semantics/landscape.md) and [human review](semantics/review-workflow.md).

!!! note "Finding terms is not approving mappings"
    An [ontology](semantics/glossary.md#ontology), [vocabulary](semantics/glossary.md#vocabulary) and [standard](semantics/glossary.md#standard) serve different purposes. An ontology is also distinct from a [knowledge graph](semantics/glossary.md#knowledge-graph). Discovering an identifier does not establish equivalence.
