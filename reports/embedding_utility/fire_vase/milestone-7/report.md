# Milestone 7 report — metadata and offline infrastructure

Status: **PROTOTYPE; real scientific experiment pending authorization and implementation completion.**

## Measured metadata

The complete stat walk found **646 files / 40,318,194,810 bytes**. The historical
manifest reports 642 / 40,318,128,369. Four additional SQLite WAL/SHM runtime sidecars
and six size differences are retained in the inventory summary; no files are missing
from the historical inventory. Their provenance/content has not been inferred.
Current hashes have not been computed. Historical hashes are identified as historical.

All 330 NetCDF, 16 Parquet and two GeoPackage containers received metadata inspection;
298 other files have uninspected schemas. Coverage, rights, support and lineage are
unknown where metadata do not establish them. Footer rows across overlapping products
are not summed. Metadata contains no scientific eligibility counts: those fields
remain null. Real rows read: **0**. Array values read: **0**. Real models trained: **0**.

## Implemented and checked

Scoped, digest-bound external-review gates; complete-container byte verification;
projected Parquet streams; native-evidence preservation; one-fire streaming summaries;
37-day bounded task windows; independently checked future totals; incremental PCA/SVD;
compact supervised/SSL/multitask kernels; conventional model interfaces; same-fire
excluded exact neighbor search; whole-fire splits, nested learning fractions, clustered
comparisons, Holm adjustment and same-task Pareto/cost helpers.

The retained [v3 dry validation](dry-validation-v3/dry-validation.json) uses 12 explicitly
generated fires / 540 generated days / 4,152 supported generated examples. Only 24
windows exercise numerical kernels. These are software checks, **not scientific
benchmark results or primary-cohort subsampling**. All five embedding dimensions run
supervised and SSL updates. The first dry directory is an incomplete failed attempt,
preserved after a target-mask/temporal-mask collision; v2 records the corrected run; v3 repeats it after the acceleration diagnostic update.
Finite-difference tests cover gradients at all dimensions. Generated Parquet tests
exercise positive access gates, native evidence, missing/zero and stale identity.

## Remaining implementation and scientific work

The CLI performs explicitly selected generated validation or gated real **profiling**.
It does not yet execute an end-to-end all-task full-lake training study. Callable
kernels are not a completed experimental orchestrator. Out-of-core selection,
checkpoint/restart, all-model repeated fits, measured resource scheduling, workload
routing/index benchmarking and final plotting orchestration remain to be completed.
Reviewed classification, geometry/environment associations, full-history morphology
scaling and retrieval relevance criteria are unresolved. These are not implemented
by guessing scientific rules. No adapter silently substitutes generated data.

A metadata inventory and reproducible draft protocol are complete; reviewed recipes,
sample-size accounting, prediction/retrieval/transfer results, learning/scaling curves,
uncertainty, empirical Pareto frontiers and publication figures are **pending**, not
empty successes. The protocol lists precisely how those comparisons will be made.

## Manuscript-ready methods draft

We propose a retrospective, whole-fire grouped comparison of native observations,
interpretable developmental summaries, train-only classical coordinates and learned
temporal representations. Exact calendar support determines eligible depth–horizon
windows; missing intervals are not replaced by zero. Task-specific support masks
retain partially observed labels. All transformations retain source and reviewed
recipe identities. Training, model selection, calibration and held-out evaluation
are separated by whole fire and reviewed temporal/geographic blocks. Scientific
minimum effects and confirmatory comparison families are fixed before test inspection.
Full lifecycle costs are assessed against optimized native and cache baselines.

## Results draft — evidence pending

The package is locally present and metadata-indexed. There is currently no approved
real-fire estimate of representation skill, transfer, information preservation or
computational advantage. Therefore this study cannot yet answer whether embeddings
are necessary, helpful, unnecessary or harmful for these real populations. Earlier
synthetic results remain synthetic and are not pooled with this proposed study.

See [authorization amendment](authorization-amendment.md), [protocol](protocol.md),
[theory and failure hypotheses](theory.md), [unsupported claims](unsupported-claims.md),
and [evidence index](evidence-index.json).

## Validation record

Final full suite: **377 passed, 2 skipped**. Strict MkDocs build: **passed**.
The initial suite had 376 passes, two skips and one pinned-worker startup timeout;
the unchanged test passed individually, then the full suite passed on rerun.
All logs are retained under `validation/`. No timeout limit or scientific operation
was changed to obtain the pass. All 112 recorded frozen M1–5 output hashes and 15
M6 evidence hashes match; upstream remains clean. See `historical-integrity.json`.
