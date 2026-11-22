# Current implementation status

## Embedding utility study — 20 November 2026

[Separate analysis planning](analysis/embedding-utility.md) is **UNDER ANALYSIS**.
The scaffold centers the same agent using direct source tools, embedding consumers
or both, with verified task outcomes and full lifecycle costs. Raster prediction
is a supporting study; agent competence remains a hypothesis. No runner or new results exist.
The [Fire VASE deterministic benchmark](analysis/fire-vase-benchmark.md) is **WORKING**
with 29 synthetic questions, strict R0/R1/R2 views, three evidence-only metadata
conditions, independent keys and cost-aware replay. Real-data integration, expert
similarity and agent/model experiments remain planned; no ecological findings are claimed.
Pipeline contracts, source access, tracks and historical vetoes are unchanged.


## Resource planning — 26 October 2026

The [grant-period budget](resource-budget.md) targets all-TACC persistent storage and versioned backup, with VERDE/Jetstream2 compute. Its retention ledger explicitly carries earlier releases forward and separates capacity growth, authorized closeout assumptions and backup history. Rates, churn and scientific production remain conditional; no remote backup is implemented. Historical OSN plans remain explicit older prototype records.

## Local operational prototype — 23 October 2026

The [data management workbench](management-workbench.md) connects generated
harmonization/MOSAIKS output to immutable typed records, SQLite lineage lookup,
deduplicated files, portable JSONL/schema exports, nine workspace plans, three
planned products, resource plans, measured usage, feedback and actual local
snapshot/restore. The loopback UI supports filtering, pagination, evidence
traversal and checked range downloads. No scientific approval or arbitrary
execution API exists. Scale probes measure metadata indexing only. Remote
MESA/iRODS/OSN/NDP/TACC services, awards and global scientific products are not
claimed. The undefined third executable track is unchanged.

The [documentation synchronization audit](development/documentation-sync-audit.md)
separates implemented metadata diagnostics from planned ontology depth, composition,
accumulation, dataset potential/diversity and flagship analysis. See the
[ontology](semantics/ontology-benchmarking.md) and [dataset](semantics/dataset-benchmarking.md)
frameworks. No approved real Sentinel MOSAIKS release is claimed.


## Semantic discovery and landscape

Module 1 now preserves typed source semantic evidence and optional concept candidates.
Normalized metadata and native annotations retain distinct evidence kinds; source
identifiers/definitions survive and stale bindings are rejected. Mapping and approval
remain Module 2 responsibilities. MESA and external ontology-portal integration
status has not changed; no universal ontology or new data source is claimed.

The [Semantics resource](semantics/index.md) includes the canonical 86-resource
inventory, auditable provisional assessments, generated coverage comparison and
linked glossary. The [benchmark](semantics/benchmark.md) produces metadata-only
Parquet diagnostics and review-only portfolio suggestions. Default runs use generated
source metadata; explicit runs can inspect retained real source metadata without
reading observations. Neither establishes scientific compatibility or approval.

## Evidence-bound review and website

The new `review-metadata` command validates domain-scoped evidence and frozen-recipe
findings from six specialists, then requests QA synthesis referencing existing IDs.
Reports separate missing evidence, failure, eligibility and mandatory human review.
They never authorize execution or bypass historical model vetoes. A matching
report with accepted QA and no unresolved findings is now an additional required
gate for real Sentinel streams, checked before source access. The legacy
`consensus` command retains its original dialogue/vote contract. See the
[review guide](review/index.md), [audit](architecture/current-state.md) and
[Sentinel comparison](development/sentinel-review-refactor.md).

The website now separates narrative research pages from technical documentation,
with generated contract reference and source-maintained architecture and conceptual figures.
The existing Material/Pages configuration remains the deployment mechanism.

## Metadata consensus and streaming

The new [streaming module](streaming-harmonization.md) separates metadata-only
OpenClaw specialist dialogue from lazy Sentinel native-window access. The first
target is B08 reflectance using documented scale/offset. Exact-plan consensus,
deterministic QA and human approval gate direct bounded-batch encoding. No raw or
harmonized data files are produced by this path. Scalar reference encoders remain available; the independent MOSAIKS raster path is implemented below. Legacy fixture/snapshot paths still materialize data explicitly.

## MOSAIKS representation module

The [MOSAIKS module](mosaiks-embeddings.md) accepts harmonized raster outputs,
fits empirical random convolutional filters on training tiles only, and writes
dense feature matrices with lineage and separate verification labels. Generated
diagnostics run through actual harmonization and MOSAIKS computation; held-out
ridge evaluation includes mean/shuffled-label baselines and spatial leakage checks.
This is numerical pipeline verification, not independent ecological validation.
Fresh raster-layout consensus and an actual human decision gate real execution.

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
independence tests are implemented. An earlier MOSAIKS integration checkpoint passed 110 tests; current verification is
recorded in the [website review](development/website-review.md),
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

## MOSAIKS verification result

The generated harmonization → MOSAIKS → held-out ridge workflow produced 32 vectors
and passed numerical verification, alongside 110 offline tests. A real-metadata
640×640 m raster plan was reviewed through Verde, but the run stopped on an invalid
rights peer citation after three valid revision requests. No real calibrated
raster/vector dataset was emitted. See the [MOSAIKS result](mosaiks-embeddings.md#verification-result-2026-10-21)
for diagnostic metrics, the concrete candidate and remaining scientific gaps.

## Model trust hardening

WORKING: a ten-operation closed registry, declarative decision IR, constrained
capabilities, deterministic parameter resolution, scientific validation, explicit
review/failure states and no-model approved execution. The fixture demonstration is
MOCKED, including its human decision. OpenClaw/VERDE and model scientific roles remain
PROTOTYPE; no new live call or approved real Sentinel product is claimed. General
support algorithms, ontology composition and authenticated human approval remain
PLANNED. [Detailed status and limits](architecture/model-trust.md#current-status).

## CubeDynamics backend

WORKING in generated offline tests: external CubeDynamics 0.1.0rc3, seven registered
capabilities, source-bound JSON backend plans, lazy xarray/Dask validation, explicit
bounded materialization and typed transformation lineage. The generated Sentinel-like
window → CubeDynamics → MOSAIKS example is PROTOTYPE; its model/reviewer are MOCKED.
No new live source/inference run or approved real Sentinel product is claimed.
General support-changing representation bridges and reprojection are not exposed.
[Integration](cubedynamics.md) · [API audit](development/cubedynamics-audit.md).

## Visual evidence report

The [pipeline state report](pipeline-state-report.md) provides an auditable visual
snapshot, including measured local test/registry/inventory counts and explicit
scientific limitations. Source, figures, machine inventory and rebuild scripts are
retained in the repository. This communication artifact does not change scientific
approval or external integration status.

## Scientific validation update — 22 October 2026

The [new scientific validation findings](validation/index.md) retain real graph
measurements, canonical requirement diagnostics, scoped dataset/pair assessments
and live model results. Earlier unmeasured/planned statements describe the prior
architecture snapshot: depth is now measured for three local graphs, while exact
scientific mappings, independent ecological validity and the weaker-model
hypothesis remain unvalidated. The real Sentinel and NEON–Sentinel cases still
require explicit expert decisions; no scientific execution is approved.

## Controlled Fire VASE agent milestone — 20 November 2026

The [agent benchmark](analysis/fire-vase-agents.md) is **WORKING** with a complete
**MOCKED** provider matrix: 348 fixed/adaptive cells, three repetitions and a
separate deterministic contract-routing baseline. Typed proposals, authorization,
uniform metadata/error boundaries, independent grading and usage availability are
tested. The saved runtime policy is valid, but reachable authorized real inference
was not established. Real-model smoke, genuinely held-out inputs and H1–H4 model
evidence remain **PLANNED**. No real wildfire data or native model execution tools.

## Fire VASE expanded pilot — 21 November 2026

**WORKING:** 120 evaluation questions / 24 templates on 20 new synthetic histories,
30 development questions on eight separate histories, 32 training-only PCA histories,
independent arithmetic/geometry references, optimized direct allocation and lookup,
query caches, private evaluation-cost frontiers and public development calibration.
**MOCKED:** fixed/adaptive M0/M1/M2 proposal experiments and explicit cost router.
**PLANNED:** verified real-model pilot, metadata efficacy and expert adjudication of
draft scientific evidence-claim rubrics. No real data, neural training or ecological
analog gold. See the [expanded pilot](analysis/fire-vase-pilot.md).

## Fire VASE learned representations — 21 November 2026

**WORKING synthetic controls:** train-only prefix preprocessing/PCA, a 177-parameter
causal temporal network, similar-size tabular MLP, linear probes, held-out next-day
observations, calibration by separate fires, perturbation and materialization/cache
comparisons. **PENDING:** actual real-agent smoke/pilot and approved real-fire learning.
Real files physically exist in documented legacy roots, but only metadata was read;
rights/support/availability review is incomplete. The learned probe does not beat
raw-prefix ridge in the frozen synthetic run. See the
[learning guide](analysis/fire-vase-learning.md) and its linked evidence table.

## Fire VASE task transfer — 21 November 2026

**WORKING synthetic only:** frozen A-only transfer to three new predictive tasks,
joint A–D/task-specific encoders, strong conventional/capacity controls, future-pattern
retrieval excluding same-fire candidates, linear/nonlinear input-property probes,
paired fire summaries and heterogeneous task reuse. Frozen A loses to raw heads on
B/C/D; joint training improves C but worsens A. Learned distances improve future
retrieval over raw distances, while supervised raw retrieval heads remain stronger.
No real-fire, ecological-analog, real-agent or full-lifecycle advantage claim. See
[task transfer](analysis/fire-vase-transfer.md).

## Fire VASE real-source contract — 21 November 2026

**WORKING:** packaged local-lake metadata/schema/CRS inventory, digest-bound proposed
recipes/review packet, and pure precondition/support/availability validators.
**PENDING HUMAN REVIEW:** observation-row reads, validated real adapter, prospective
cohort, real baselines/transfer/retrieval/costs. The source files physically exist
inside Fire VASE; local possession does not approve meanings, rights or operational
availability. No source rows read, copied or trained on. See
[real-source review](analysis/fire-vase-real-data.md).

## Fire VASE Milestone 7 — PROTOTYPE / UNDER ANALYSIS

Full-lake metadata indexed: 646 files / 40,318,194,810 bytes. Real rows and model
training: zero. Offline bounded streams, dimension-grid kernels and gates tested.
The full scientific runner is incomplete; see [precise status](analysis/fire-vase-full-lake.md).

### Milestone 7.2 — partial historical assessment

Investigator intent is recorded. Existing aggregate reports have been reanalyzed
with provenance and temporal/region selection figures; these are not freshly
profiled observations. The real-profile preflight still rejects the unapproved
review. No new source observations or model training; source/binding/receipt
evidence remains unresolved. Internal figures have no publication clearance.

## Fire VASE M7.3 execution — WORKING real census

Direct investigator authorization superseded the separate-receipt requirement for
read-only internal profiling. Relevant sources were freshly hash-verified, native and
cached records fully streamed, and local-run eligibility/reconciliation measured.
A full independent replay produced identical cohort artifacts. Model training and
publication remain unperformed. Source-linked internal indexes are not public catalog
entries. See [implementation and scope](analysis/fire-vase-population.md).

## Full-population Fire VASE design — current emphasis

Primary analysis includes1,2 and3+ observations; long supported-run prediction is
secondary. Deterministic short-state preservation, normalized-payload loss, byte
accounting and indexed fallback checks ran on real native values. No PCA/neural
model or agent evaluation was performed. Full retrieval/workload and learned
comparisons remain planned. See [full-population scope](analysis/fire-vase-full-population.md).

## Milestone8 — executed scientific-state utility

**WORKING:** all 278,865 fires; 75 primary neural fits plus 21 controls/updates;
PCA, exact native and interpretable controls, A/B/C access, full-gallery retrieval,
blocked refits, lifecycle measurement and six secondary prefix cohorts.
Native scalar caches dominate the measured primary workload. Learned states are
approximate; a modest secondary predictive gain is similar to a direct neural
control. Scope: fixed observed-property state, not native sequence/geometry or
operational forecasting. [Measured findings](analysis/fire-vase-utility.md).
