# Fire VASE benchmark: deterministic milestone 1

Status: **WORKING** synthetic benchmark, 20 November 2026. The broader scientific
utility hypothesis remains **UNDER ANALYSIS**. No LLM, neural training, wildfire
observations, expert relevance labels or real-data integration were used.

## Implemented

The modular `src/dataset_prototype/embedding_study/` package separates canonical
observations, R0/R1/R2 data views, evidence-only metadata, task/reference generation,
registered operations, evaluation and accounting. The worker executes the actual
external operation source at the audited Git commit and verified file hash; it
imports neither the full upstream package nor model-generated code. Upstream remains
unchanged. Versioned config, metadata and machine-readable questions are retained.

The contract preserves original dates, cumulative observations, source units,
availability, gaps, quality and provenance. Inconsistent data fail explicitly.
A source-supported one-day difference can be zero; a multi-day difference cannot
be labeled daily growth. The explicitly evidenced synthetic baseline is distinct
from assuming zero before an unknown first observation.

R1 stores upstream 20-bin normalized profiles and shape traits without absolute
size or native dates. R2 stores three PCA coordinates with complete train-only
preprocessing/artifact identities. No complete reusable upstream fitted artifact
was assumed: a synthetic artifact was fitted once to the 24 declared training
fires, reloaded with checks, and reused for every query on 10 separate evaluation
fires. Profiles, coordinates, means/scales/loadings and exact source versions are
retained in the run snapshot. No fit uses evaluation observations.

Independent references difference original cumulative values, integrate rational
interval overlaps, use analytic pulse cases and an independent SVD construction.
They do not invoke the scientific worker or reuse its returned answers.

## Full initial matrix

29 questions × 3 representations × 3 metadata conditions × 2 application-cache
modes × 3 repeats = **1,566 attempts**. These are repeated experimental cells,
not 1,566 independent fires. Families A/B/C have 16/9/4 questions.

| View | Correct task types | Correctly abstained task types | Approximate fidelity misses |
| --- | --- | --- | --- |
| R0 direct | 23 | 6 | 0 |
| R1 shape | 11 | 18 | 0 |
| R2 three-PC | 2 | 26 | 1 |

Counts above collapse metadata/cache/repeats. The single R2 fidelity miss is the
explicit two-neighbor approximation: top-two overlap with the full-profile reference
is 0.5. That is a valid approximation diagnostic that fails its exact-fidelity
threshold, not a fabricated exact answer or independently wrong ecological analog.
Its backprojection is compared in original profile units; a separate PC-distance
question agrees with independent SVD geometry. No representation fabricates missing
area/date information. All insufficient-information cells abstain correctly.

The equal-shape/different-size pair is encoded identically in R1/R2 while original
final cumulative areas are 30 and 300 synthetic km2. Direct access answers both;
normalized features and coordinates cannot uniquely recover those sizes. Equal-total
front/back histories have different developmental profiles. Unknown daily growth
across gaps remains unknown; interval growth can still be known from endpoints.

The provenance sidecar retains source observation IDs and validated consecutive
profile eligibility. R1/R2 therefore answer the declared sequence-length query by
counting those IDs. The normalized numerical payload alone omits length; the full
interface must receive credit for its retained metadata. This was corrected during
review rather than overstating information loss. Absolute size/date loss remains.

Metadata conditions yield identical deterministic answers with invariant data,
operations and resources. This establishes isolation, not a finding about metadata
benefit or an agent's ability to use it.

## Preliminary costs

For the same correct first-half-allocation question, cold application-cache medians
were approximately **352 µs R0** and **68 µs R1**. Both were approximately **16 µs**
when the query result was cached. R0 on-demand features include worker IPC while
R1 is a resident lookup; this is measured interface cost, not pure algorithm time.
The R0 scalar query currently reuses the complete upstream feature calculation,
not an optimized single-statistic kernel. Future confirmatory cost comparisons need
validated targeted direct operations as well as these reuse baselines.
Those tiny local timings are not general throughput or statistically established
speed ratios.

One-time feature construction took about 11.2 ms, train-only PCA fitting 4.6 ms
and worker startup/import about 1.12 s. Raw loading, metadata rendering, artifact
publication/reload, coordinate construction/reload and every warm prefill are also
recorded. Evaluator/reference costs are separately attributed. OS caches were not
cleared. Parent Python traced allocation and worker cumulative peak RSS have distinct
scopes. Input bytes are serialized/logical bytes, not measured physical disk bandwidth.

No universal winner or break-even query count is asserted. The snapshot provides
per-task correct-query timings and preparation attribution for explicit workload
calculations. Direct query caching can remove much of the measured repeated-query
advantage. Metadata-authoring labor, remote access, tokens, operational refresh and
independent scientific outcomes remain unmeasured.

## Evidence and reproduction

- [Generated run report](results/milestone-1-v1/report.md)
- [Full structured results](results/milestone-1-v1/results.jsonl.gz)
- [Manifest and hashes](results/milestone-1-v1/manifest.json)
- [Summary](results/milestone-1-v1/summary.json)
- [Preparation/caching costs](results/milestone-1-v1/preparation.json)
- [PCA artifact](results/milestone-1-v1/pca_artifact.json)
- [Reproduction/architecture guide](../../../docs/analysis/fire-vase-benchmark.md)

The run records parent NumPy 2.5.2/Pydantic 2.13.4 and an isolated Python 3.11.11,
NumPy 1.26.4, pandas 2.3.3, SciPy 1.17.1 worker. The optional dependency extra and
minimal worker requirements document clean installation. A new sparse-source CI
job is configured; no remote CI completion is claimed. Only trusted operation code
is required from upstream, not its observation archive or package installation.

Verification: **262 passed, 2 skipped** in the full local offline suite with the
explicit pinned worker; **22 benchmark tests passed**. Integration tests replay two
runs and compare scientific-result digests separately from variable timings/memory.
Fixture and output hashes are verified. Strict documentation build and generated
reference/architecture synchronization are part of delivery checks.

## Remaining scope and next milestone

The canonical contract's real-source applicability still requires selected-input
rights, support, uncertainty and cumulative-versus-ring equivalence evidence. No
approved observation-access manifest was established, so no real sample was read
and no missing fitted upstream artifact was fabricated. Real validation remains
pending; this does not block the synthetic milestone.

[The next controlled agent milestone](agent-experiment.md) specifies a typed
selection/abstention envelope, permitted data renderer, budgeted dispatcher, exact
model/prompt/usage tracing and independent final-answer evaluation. It will reuse
these operations, not enable unrestricted scientific programming. Future forecasting
needs a reviewed prefix-only recipe, and scientific similarity needs actual expert
relevance evidence. Original proposal, upstream audit and historical vetoes remain
intact.
