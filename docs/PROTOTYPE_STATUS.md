# Prototype status

## Metadata consensus and streaming

The new [streaming module](streaming-harmonization.md) separates metadata-only
OpenClaw specialist dialogue from lazy Sentinel native-window access. The first
target is B08 reflectance using documented scale/offset. Exact-plan consensus,
deterministic QA and human approval gate direct bounded-batch encoding. No raw or
harmonized data files are produced by this path. Current encoders remain reference
numeric features. Legacy fixture/snapshot paths still materialize data explicitly.

## Working now

Three independently callable typed modules compose into a complete offline run:
question/configuration → fixture discovery/access → semantic proposal → versioned
recipe → QA → approved deterministic execution → shared observations → track
products → modality-specific vectors → JSON-LD/source lineage → descriptive
synthetic downstream comparison. CLI, schema export, review artifacts, checksum
validation, immutable content-addressed storage, and separate track outputs work.

## Mocked

`MockMESAClient` searches local normalized fixture metadata and verifies local
asset checksums. The default fixture agent roles use deterministic curated rules; the separate
real workflow uses model-backed Ollama roles. Six records are synthetic field and satellite scalar measurements,
not provider records, native schemas, images, or actual observations.

## Real external integration

Live Earth Search STAC discovery and actual Sentinel-2 NIR/SCL COG pixel reads
were exercised on 2026-10-21. Three initial actual DN observations and an independent
one-pixel CLI acquisition preserve native metadata, calibration context, support,
quality and licensing. Four real local Ollama role calls completed with versioned
model transcripts. Ollama baseline QA rejected its proposed recipe; no scientist
approval or executed model-proposed transformation is claimed.

NEON public product metadata was retrieved; the data-file endpoint returned 403
without a token. Authenticated native CSV access code is implemented and unit-tested,
but token-backed acquisition/normalization has not yet been verified. Live MESA remains unimplemented. OpenClaw now has an isolated Verde-backed
JSON-only task adapter using the installed 2026.5.18 plugin. See [live evidence and limits](real-data-agents.md).

## Future MESA integration

Verify deployed MCP tool schemas/version, provide user-configured transport,
normalize real discovery metadata/rights/support to `SourceResource`, and implement
search/describe/fetch/history through verified capabilities. The current source
README's pre-alpha status differs from the tool families described in overview
docs. See [integration inspection](development/integrations.md).

## OpenClaw and Verde

An isolated gateway now uses the existing OpenClaw image and configured Verde
provider/model. No existing working-group/Slack routes are changed or mounted.
`OpenClawBackend` calls the actual JSON-only `llm-task` plugin over `/tools/invoke`.
The plugin disables inference tools and validates schemas. Route checks reject
provider/model substitution and there is no Ollama/mock fallback. Model weight
hash and usage are unavailable from the plugin and are explicitly unreported.

Live testing identified two compatibility requirements: fully qualify the model
as `verde/js2/gpt-oss-120b`, and set `compat.supportsTools: false` so Verde receives
no unsupported empty tools array. See [OpenClaw/Verde setup](openclaw-verde.md).
The live four-role OpenClaw → Verde run completed with schema-valid outputs from
`js2/gpt-oss-120b`. Model QA requested revision and deterministic QA blocked
execution. The isolated gateway is running; scientific acceptance remains pending.
Full working-group scheduling and authenticated human review remain future work.

## Scientific assumptions

In the default fixture demo, synthetic fields and satellite values have intentionally aligned coordinates,
daily intervals, and common support. Metadata matches curated identity targets.
Scalar/squared encoders illustrate reusable interfaces, not ecological feature
quality. The downstream correlation illustrates software composition only.
The real Sentinel path retains uncalibrated band-8 DN, actual 10 m pixel footprints,
instantaneous acquisition times and SCL. Scale/offset remain metadata, not a hidden
conversion to reflectance. No real field/pixel join has been asserted. No universal
ontology, universal latent space, food/water model, real cross-modality support
alignment, or scientifically validated prediction is claimed.

## Human decisions

Novel/low-confidence/disputed/ambiguous meaning, changed temporal/spatial support,
joins, and uncertain rights require exact-recipe review records. Unknown mappings
must be revised explicitly; QA rejection/known rights prohibitions block execution.
Default conservative fixture identity mappings pass deterministic QA. Real model
mappings always require human review; model QA vetoes cannot be bypassed by changing
approval state, and scientific edits invalidate the model review. Human
identity/signatures and tamper-resistant external audit are not implemented.

## Science tracks

Food and water run independently through shared modules using the same immutable
sources/core cache. Their only demonstrated scientific configuration is the common
synthetic comparison; encoders differ. Third track is disabled until scope is
specified; tests prove configuration-only extensibility with an enabled synthetic
copy. Default orchestration does not yet load arbitrary per-track recipe files.

## Testing status

Offline unit, contract/integration, CLI, deterministic repeatability and track
independence tests are implemented. On 2026-10-21, the expanded offline suite passed locally (94 tests after streaming harmonization),
the installed CLI ran both tracks, and the strict website build passed. Rendered
navigation/readability and local links/fragments were checked. [Testing](testing.md) describes coverage and
scientific gaps. CI also builds the existing MkDocs site strictly.

## Current limits

The legacy executor buffers inputs; the new streaming module limits each call to
a bounded microbatch. Large partitioned joins/aggregation remain unimplemented
and are refused by streaming preflight.
Source/core results use integrity-checked read-through caching and atomic
publication; distributed cache coordination remains future work. Linear unit/calibration uncertainty scaling is implemented; calibration-parameter
uncertainty, covariance and broader propagation remain incomplete. Only WGS84 identity coordinate
normalization is supported. Native Sentinel STAC/window access now exists; sensor-aware NEON normalization
and real field/satellite alignment remain pending.
Local JSON review is an auditable artifact, not an authenticated permissions system.

## Next milestone

Complete token-backed NEON CSV acquisition and verify sensor/variable metadata.
Review the actual model QA rejection and improve evidence/contracts without forcing
approval. Then specify and review a defensible real NEON + satellite support and
temporal alignment question. Then add a non-raster cross-network/trait vertical slice,
followed by ORNL DAAC context, before making generality claims.

## First live metadata consensus result

Real Earth Search metadata fed four specialist analyses, a schema-valid recipe,
and five actual OpenClaw/Verde peer reviews. The final run requested revision;
coefficient checks passed, while final QA enforced the model veto. No calibrated
real-data embeddings were emitted. Model claims and executor limitations remain
separate; see the [live evidence](streaming-harmonization.md#live-verification-2026-10-21).
