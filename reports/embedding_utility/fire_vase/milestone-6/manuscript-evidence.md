# Manuscript-ready M6 provenance and evidence status

## Scientific provenance

A local Fire VASE v0.1 package was located within the Fire VASE working directory,
with native FIRED daily/event GeoPackages and derived lakehouse products present in
its `files/` tree. The package manifest records642 files,40,318,128,369 bytes and
historical full-container SHA-256 identities. Selected current sizes agree with the
inventory. Parquet footers and GeoPackage schema/catalog/CRS metadata were inspected
read-only. Current full data contents were not rehashed and no observation rows were
read. The package and current analysis code have distinct version identities.

Upstream transformation code copies native daily area into a ring-area field,
constructs cumulative sums and tests exact-day source/cache alignment. These are
source-documented implementation facts. They do not establish reviewed equivalence
for all similarly named fields, physical spread rates or different temporal support.
Native event dates, units, spatial support, quality, source uncertainty and actual
availability must survive any approved adapter. The initial review packet excludes
geometry, weather, completed morphospace, endpoints as predictors and public release.

## Cohort and experimental design

Real cohort construction is pending source-use/scientific review and bounded native
validation. Planned inclusion requires reviewed event identity, consecutive prefix
support and independent future observations. Prospective mode additionally requires
actual availability by issue time. Unknown availability is not replaced by synthetic
timestamps; retrospective reconstructed prediction requires an explicitly different
reviewed claim. All prefixes of a fire must share a fold; real validation, calibration,
chronological/geographic holdouts and observation-process strata precede model selection.

Historical upstream aggregates document severe observation-support selection, but
cannot substitute for this experiment's cohort counts, bias assessment or outcomes.
No real baseline, representation-transfer, retrieval or workload-computation result
is reported. Mean, persistence, raw/summary ridge, train-only PCA and existing small
TCN/matched-MLP comparisons remain planned after separately approved cohort/training.

## Evidence table

| Category | What can be stated | What cannot be stated |
| --- | --- | --- |
| Mathematical result | Deterministic representations cannot add per-case observations; exact support and source identity checks are defined | That a compressed representation is scientifically sufficient for an unrestricted real task |
| Synthetic experimental observation | Frozen M1–5 outcomes remain as reported, including mixed transfer/reuse tradeoffs | That those measured differences persist on real fires |
| Real scientific observation | **No new row-level M6 scientific observation** | Real predictive skill, cohort coverage, calibration, ecological retrieval or observational error distribution |
| Real-model agent observation | None collected | Agent competence, metadata benefit or approved inference |
| Theoretical prediction | Proposed task-conditioned information/cost tradeoffs and reviewable real design | An empirical winner, exact lifecycle crossover or operational forecasting validity |
| Unmeasured / pending | Source terms/mapping review, fresh full hashes, real cohort and model/cost evaluation | Treating pending quantities as zero, absence or success |

Real-source metadata (file presence, sizes, schemas, native CRS and historical
inventory/aggregate statements) is **SOURCE_DOCUMENTED / METADATA_INSPECTED** evidence,
not newly measured scientific observations or a validated real-data integration.

## Limitations and reproducibility

The dataset landing page could not be accessed to confirm source-specific terms;
code/article licenses do not fill that gap. Native uncertainty/QA and real processing
latency remain unresolved. Pure generated precondition tests do not establish source
value correctness or expert scientific compatibility. No production executor,
harmonization gate, public release decision or old model veto has been altered.

Packet, metadata/schema hashes, proposed recipes, review template and checker output
are retained under [review-v2](review-v2/manifest.json). Approval must bind exact packet
content. A future approved study must preserve source/recipe/review and execution
provenance, current identity verification, all exclusions/failures and held-out results.
