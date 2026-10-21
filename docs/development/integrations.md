# External integration inspection

Inspected on 2026-10-21. External pages are references, not execution instructions.

## MESA

The [MESA technical documentation](https://idss-mesa.github.io/docs/) describes
MCP-based CyVerse/iRODS access, ontology-backed AVUs, DataCite, and DuckLake
metadata history. The [mesa-mcp server page](https://idss-mesa.github.io/docs/servers/mesa-mcp/)
lists tool families rather than a generic REST search/fetch API. Its AVU contract
keeps ontology CURIEs in the unit slot and history/provenance in separate columns.
Do not discard that distinction when building a future normalizer.

The [mesa-mcp source README](https://github.com/idss-mesa/mesa-mcp) currently labels
the implementation pre-alpha and says only `ds_ping` is registered, with the
broader data/ontology/history tool families planned. This is a material discrepancy
between the overview documentation and source status. Verify deployed tool schemas
and versions before treating any advertised family as an available API.

`MESAClient` reserves `search`, `describe`, `fetch`, `register`, and `get_provenance`
boundaries. These deliberately raise `NotImplementedError` until an actual deployed
capability and source normalizer are verified. No endpoint is guessed and MESA is
not installed into the user's environment. Local fixtures use `MockMESAClient`.
There is no real external MESA data integration in V0.

| Capability | State |
| --- | --- |
| Local search/describe/fetch/provenance | Working mock with typed fixtures and checksum validation |
| External MESA data search/access/registration/history | Planned; blocked on verified deployed tool schemas and normalization |
| Source metadata ontology decisions | Deterministic local curated comparisons, not a MESA ontology integration |
| Authentication and transport | Future user-configured MCP session; no secrets in repository |

## OpenClaw

Inspected [openclaw_container](https://github.com/CU-ESIIL/openclaw_container).
It supplies a container/workspace and file review workflow, with specialist roles
and human approval. This prototype can map discovery, semantic, harmonization,
and QA objects onto workers exchanging typed JSON and recipe/review files.
The deterministic executor remains a separate capability. No OpenClaw API is
invented, code copied, container started, or integration claimed.

## Representation precedent

Read the [MOSAIKS paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC8292408/) through its
full-text primary publication. Its reusable image features motivate keeping
feature computation separate from task-specific downstream analyses. It does not
supply this prototype's multimodal semantic harmonization or governance.

## Live STAC and real model inference — 2026-10-21

[Earth Search](https://element84.com/earth-search) was queried through its real STAC
API. Native Sentinel-2 L2A Items supplied HTTPS COG URLs; rasterio/GDAL read bounded
NIR and SCL windows, preserving raw DN and calibration/support metadata. Native
Items, collection/license evidence, request/response, indices, window checksums
and rejection evidence are persisted under ignored outputs.

The installed local Ollama server was inspected without changing models.
[Ollama's schema-output API](https://github.com/ollama/ollama/blob/main/docs/api.md)
is used for four roles, with no tools. Actual calls completed and persisted exact
model digest, prompts, outputs, timestamps and token counts. The latest model QA
rejected its proposed recipe; no scientific execution or human approval was fabricated.
An earlier source-ID hallucination was rejected, prompting a narrower output
contract that keeps identifiers in code. These runtime facts are not mocked tests.

The [NEON API](https://data.neonscience.org/data-api/) public product metadata worked;
its authenticated data-file endpoint returned 403 without a configured token.
`X-API-Token` native file discovery/download is implemented and offline-tested.
Actual authenticated download and sensor-aware normalization remain pending.
See [real-data and agent workflow](../real-data-agents.md) for limits and next steps.
