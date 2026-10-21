# Architecture

The existing template contained MkDocs Material, static assets, styling, and Pages
workflows. It had no `src/`, `tests/`, or `data/` implementation. The prototype adds
one standard Python package under `src/dataset_prototype/`, without repurposing
website sources as package files.

## Module boundaries

| Module | Inputs | Outputs | Exclusions |
| --- | --- | --- | --- |
| Discovery and Access | `ScientificRequest`, access client | `DiscoveryResult` with `SourceResource` candidates | No encoders or scientific equivalence decisions |
| Harmonization | Resources, recipe, records, optional review/core parents | Iterator of `HarmonizedObservation` | No MESA dependency or generated-code execution |
| Representation | Validated observation iterator, encoder name | Iterator of `Representation` | No discovery or hidden scientific harmonization |

`contracts.py` defines immutable Pydantic models, rejects extra fields, and exports
JSON Schema. `agents.py` contains deterministic fixture roles; `model_agents.py` supplies four
bounded real inference roles using Ollama without tools or data-write capabilities.
`orchestration.py` composes the stages and writes inspectable JSON artifacts.
`provenance.py` exports PROV-inspired JSON-LD without a graph database.

## Infrastructure boundaries

[MESA](https://idss-mesa.github.io/docs/) is intended to supply distributed data
access, iRODS tools, ontology metadata, and metadata history. It is infrastructure,
not the harmonization recipe or the representation module. See the verified
[integration notes](development/integrations.md).

STAC is a spatiotemporal catalog/metadata standard, one part of discovery. `real_data.py` now
implements bounded live Sentinel STAC search and raster-window access, retains
native Items/collection/license evidence, and supplies verified offline snapshots.
Raw DN, calibration metadata, pixel support and instantaneous time stay explicit.

[OpenClaw container](https://github.com/CU-ESIIL/openclaw_container) is the future
agent runtime. Local role objects exchange structured contracts; later workers
can return the same proposal artifacts. No runtime is copied or required.

## Storage and streaming

Source descriptions, raw records, and observations are frozen models containing
immutable nested contracts and tuples. Source checksum verification detects fixture
changes. Content-addressed cache entries include source/version/metadata/rights,
raw records, recipes, executor version, and resulting canonical observations.
A source or recipe change produces a different key; obsolete entries are retained,
not served under a new identity. Corrupted existing entries fail validation.

Food and water outputs have separate directories and track-bearing identifiers.
Existing output directories fail rather than overwrite. Source and canonical entries use an integrity-checked read-through cache, so
a second track reuses inputs and core products without fetching or executing again.
Entries are published atomically without overwriting existing keys. Filesystem
permissions are not an access-control or adversarial security boundary in V0.

Representation and batch interfaces consume iterators. Harmonization currently
buffers the small input fixture; joins and daily aggregation need grouped inputs.
A production-scale partitioned/streaming executor is a documented gap. No Kafka,
graph database, or distributed scheduler is introduced.
