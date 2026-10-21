# Current-state audit

Audit date: 2026-10-21. This records the repository before the review-hardening and
narrative-site pass. Existing implementations and historical evidence are retained.

## Three scientific stages

| Stage | Implemented modules | Boundary | Actual status |
| --- | --- | --- | --- |
| Discovery & access | `discovery`, `adapters`, `real_data`, `stream_sources`, `stream_rasters`, `neon`, `network`, `storage` | `ScientificRequest` → `SourceResource` / bounded stream | Offline fixture transport and live Sentinel STAC/COG access; MESA explicitly unavailable; authenticated NEON normalization pending |
| Harmonization & review | `agents`, `model_agents`, `consensus`, `harmonization`, `harmonized_rasters` | Sources → mappings / recipe → canonical scalar or raster outputs | Allow-listed execution, metadata dialogue, deterministic QA, exact-recipe human gate; existing free-text specialist review leaks jurisdiction |
| Representation | `representations`, `mosaiks`, `embedding_dataset` | Validated harmonized outputs → vectors / lineage | Scalar reference encoders; empirical MOSAIKS with generated held-out diagnostics; real raster execution blocked upstream |

`orchestration`, `mosaiks_pipeline` and `cli` compose these stages. `science` provides
a descriptive synthetic comparison, not a food/water-security model. Contracts are
frozen Pydantic models, plus an in-memory raster dataclass whose content is hashed.

## Contracts, recipes and provenance

`contracts.py` defines source, request, discovery, mappings, recipes, observations,
representations, QA, human decisions and track configuration. `stream_contracts.py`
defines metadata plans, votes, messages, encoder configuration and consensus.
Recipes are versioned JSON, scoped to conservative core or an explicit track.
Source IDs and targets are code-owned; models cannot supply arbitrary executable code.

Scalar provenance nests source records, source metadata, recipe, executor, QA,
human decisions and core/track parents. Streaming output substitutes compact IDs,
window hashes and support for persisted raw/harmonized values. MOSAIKS stores frozen
filters, full training context, separate labels, numeric feature shards and checksums.
Metadata hashes are not raster-byte hashes. Discarded input windows cannot be
reconstructed solely from an output hash.

## Observed Sentinel failures

Inspected the complete available recipe, QA, consensus, dialogue and trace artifacts
in `run/sentinel-stream-consensus-bounded/` and `run/mosaiks-real-consensus/`.
The former completed five reviews and requested revision; final QA rejected execution.
Semantic, units, support and rights roles repeated negative-reflectance, licensing,
mask and checksum concerns. Rights asserted potential usage-policy breaches from
numeric values without supporting terms. Metadata-only checksums were repeatedly
conflated with raster integrity. Several claims contradicted declared executor behavior.
The MOSAIKS run retained a valid draft and three revision requests, then rejected a
rights self-citation. No approved real harmonized MOSAIKS dataset was produced.

The exact native B08 coefficients were scale 0.0001 and offset -0.1. Unit `1` is
valid dimensionless notation. Negative calibrated values were never automatically
clipped. Uncertainty scaling exists, while calibration-parameter covariance does not.
Human approval was never fabricated. OpenClaw traces expose normalized plugin JSON,
not raw provider text, token usage or model-weight digests.

## Concrete debt and minimal response

- Review findings are free text; topics and evidence provenance need typed boundaries.
- Integrity has no independent reviewer domain; checksum claims leak into other roles.
- `agree/revise/reject/abstain` conflates missing evidence with demonstrated failure.
- Repeated concerns need stable finding identities and references, not another vote.
- Quality selection is performed in source adapters, separately from recipe calibration,
  but historical output labels do not reliably distinguish calibrated and filtered data.
- Legacy snapshot/fixture paths materialize data; new streaming paths must remain distinct.
- Scalar and raster executors duplicate a small allowlist; parity tests are preferable
  to a speculative universal execution framework at this stage.
- The flat website mixes introductory narrative with implementation reference. Preserve
  MkDocs, Markdown URLs, Material overrides, search and Pages deployment; add a clear
  narrative/documentation split rather than another frontend.

## Tests, tracks and deployment

The audited suite has 110 offline tests covering contracts, discovery, calibration,
review gates, streaming, MOSAIKS, provenance, cache integrity and independent track
configuration. Food/water share immutable sources/core results; the third track is
disabled. No new source or track is warranted by these findings.

The existing Pages workflow builds MkDocs strictly. Template synchronization and
container publishing are separate manual historical workflows, not required for
site deployment. No configured linter/type checker exists; do not invent a claim
that one ran. Tests and strict documentation builds remain required checks.
