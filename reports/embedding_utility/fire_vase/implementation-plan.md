# Implementing the Fire VASE study

## Current primary design — full observed population

The [full-population protocol](full-population-v1/protocol.md) supersedes the earlier
emphasis on long consecutive histories. All native fire IDs are primary, stratified
by1,2 and3+ observations; preservation, observable-property retrieval and optimized
access/reuse are the primary tasks. Long-run prediction is a separately labeled
selected-cohort extension. Earlier dated milestone plans below remain historical.
Real short-history diagnostics are executed; learned/classical comparisons and
full-gallery retrieval remain planned. Do not infer physical lifetime from record count.


Status: **WORKING** deterministic synthetic milestone; broader study **UNDER ANALYSIS**.
Plan v0.4, 20 November 2026. The user-authorized implementation adds no real-data
or model execution permission. [Upstream audit](upstream-audit.md) records
verified components; [references](references.md) distinguish supporting evidence.

## Main estimand

For task family t, metadata condition m, agent condition a and workload q, estimate
incremental utility of an embedding-enabled interface against capable direct access.
Report task correctness and cost separately before any case-specific value judgment:

```text
Delta(m,a,t,q) = success_embedding(m,a,t,q) − success_direct(m,a,t,q)
metadata interaction = Delta(rich,a,t,q) − Delta(basic,a,t,q)
capability interaction = Delta(m,stronger,t,q) − Delta(m,weaker,t,q)
```

A negative metadata interaction supports diminishing embedding advantage only if
uncertainty and predeclared practical thresholds support it. It is not enough that
rich metadata improves direct access. Report absolute success in every cell: two
failed systems can also have zero difference. Evaluate adaptive routing separately;
its improvements include the policy, not just the representation. Metadata richness
is a controlled treatment with independently checked correctness, not a scalar
quality score or a source of ground-truth answers.

## Separate representation from agent policy

| Data interface | Initial realization | Scientific boundary |
| --- | --- | --- |
| Direct histories | Dated reconstructed increments plus registered queries/operations | Source-native information is preserved; agent can compute approved features on demand |
| Interpretable features | Materialized 20-bin allocation profile and declared traits | This is a scientific representation already; do not attribute its entire value to learned embedding |
| Statistical embedding | Training-only standardized PCA at declared dimension | Distinguish reduction from profile construction; include Hellinger sensitivity |
| Adaptive | Access to all eligible interfaces with logged route/fallback | Fit routing only on development tasks; compare with simple fixed routing and an explicitly unattainable hindsight oracle |

Neural temporal embeddings come later, after PCA and direct baselines. Compare
raw-history→encoder and profile→encoder paths separately. Geometry/weather additions
must be offered to all applicable baselines; otherwise any gain could be extra
information rather than learning. No MOSAIKS substitution: fire histories are a
different modality. Distinguish full-history retrospective analysis from prefix-only
prediction in data contracts, labels and fitted artifacts.

Run two comparisons: (1) representation availability under a matched deterministic
consumer; (2) complete agent workflow performance with documented tool interfaces.
Embedding consumers must actually exist; an LLM is not expected to interpret naked
PC/neural coordinates. Exact tasks unavailable from compressed-only information
measure capability coverage/information loss, not failures on a shared task subset.
Report both the common-task subset and all-task coverage without hiding exclusions.

## Metadata conditions

M0 exposes field names, file types and minimum safe units/support/access constraints.
M1 adds source definitions, native identifiers, temporal/gap semantics and provenance.
M2 adds evidence-backed uncertainty/limitations and machine-readable eligible
operations, preconditions and input/output meanings. Freeze concrete evidence views,
not vague richer prose. Unknown uncertainty stays unknown; do not fabricate it to
complete M2. Add a length-matched prose/structure control where feasible.

Every metadata condition uses the same callable names/signatures, authorization and
budget within a given interface. M2 enriches evidence and operation meaning; it
does not secretly enable extra operations. Every condition uses the same source
cohort, source versions, permission checks,
canonical validator and retrieval backend. The executor always sees full safety and
scientific preconditions; the agent's experimental metadata view is separate.
Missing essential meaning must trigger abstention. Keep answer keys, target values,
held-out outcomes and recommended task answers out of metadata. Report direct-access
index/caching alternatives with identical warm/cold conditions.

## Agent conditions and current governance

Start with a fixed workflow reference and one agent selecting from reviewed
operations. Later compare model capability and structured multistep planning on
the same registered capability set, with matched budgets and exact provenance.
Model size alone is not an established capability ordering; validate development
performance and report model/quantization/context identities.

The proposal's code-constructing agent arm is **DEFERRED / outside current execution
policy**: AGENTS.md prohibits runtime model-authored scientific code, SQL and formulas.
Do not silently rename code generation as tool selection or claim it has been tested.
Composing registered operations is a permissible narrower experiment. Unrestricted
scientific programming would require a separate governance decision and study.

## Proposed execution flow

```text
Frozen task + selected source/version + full canonical scientific evidence
    ├── experimental metadata view → agent → structured operation proposal
    └── scientific preconditions ────────────┐
                                             ↓
                     schema/allowlist/scientific/human gates
                                             ↓
                  isolated pinned Fire VASE operation adapter
                                             ↓
                 typed values + units/support + evidence lineage
                                             ↓
                independent evaluator + costs + immutable traces
```

The agent never invokes an interpreter. Read-only source windows/rows and candidate
artifacts remain outside prompts unless explicitly included in the evidence view.
The deterministic synthetic portions are now implemented; the agent branch remains
planned. See the benchmark guide for exact implemented contracts.

## First task suite

| Family | Example | Ground truth / score |
| --- | --- | --- |
| Exact computation | Reconstructed sum, observed peak increment and peak date; detect a two-day gap | Reviewed upstream operation replay; value/unit/date tolerance and provenance |
| Representation construction | Construct the 20-bin allocation for an eligible consecutive history | Upstream mass-conserving implementation, nonnegativity and unit sum; invalid dates must block |
| Similarity retrieval | Find fires matching a stated early/late criterion or developmental relevance request | Explicit rule tasks have deterministic keys; open scientific similarity needs blinded expert relevance, not PCA neighbors as gold |
| Prefix prediction | Predict next observed-day increment from data available through t | Holdout future observation, exact-day pairing; naive persistence/AR and conventional-feature baselines |
| Out-of-objective questions | Recover absolute size, exact dates or observation-depth limitations from each interface | Information-preservation/capability coverage; do not invent inverse recovery from shape-only coordinates |

Do not train a head to recover an input statistic and call that independent science.
For similarity, separate distance approximation to a declared reference geometry
from independently judged scientific relevance. Score retrieval with recall/nDCG only
when a relevance set exists; otherwise report distance/neighborhood diagnostics.
Human labels are authored or adjudicated by actual experts; assistant drafts remain
drafts. Ground-truth operation results also need independent analytic synthetic
oracles to avoid an implementation grading its own errors.

## Forecast leakage controls

No final area, final duration, completed-history growth normalization, completed
morphospace coordinates, future geometry, later weather or whole-event summaries in
prefix inputs. Normalized progress through a completed fire requires knowing its
future endpoint and cannot be used as a prospective clock. Prefix-specific features
need their own reviewed definition. Forecasting is blocked until that definition is
supplied; do not automatically reuse the completed-history 20-bin recipe.

Group all prefixes of one fire together. Fit all scaling/PCA/encoders/heads on train
only; tune on validation tasks, then lock test. Existing global upstream PCA is a
retrospective descriptive reference, not a clean prediction artifact. Hold out event,
year and geography; test the >=3/5/7 depth strata explicitly. Withhold uncertain
observation-time cases or label the task retrospective reconstructed next-step
prediction. Dated records alone do not establish operational availability.

## Nulls and scientific fidelity

Reuse reviewed temporal-shuffle nulls that preserve the increment multiset, and
compare order-sensitive tasks before/after shuffling. Uniform scaling preserves
normalized shape but changes absolute size: task-conditioned invariance only.
Removing observations changes support and may invalidate primary eligibility;
measure abstention and degradation instead of demanding stability. Added spatial
geometry with equal temporal allocation is a new task requiring real geometry and
review, not something inferred from the profile. Separate null references from
observed events and geometry diagnostics from claims of distinct fire types.

## Pilot size and analysis

First audit the adapter on generated histories. Proposed feasibility pilot: 12 task
instances spanning exact/profile/similarity-rule families, 4 interfaces × 3 metadata
views × 2 agent repeats = 288 scheduled calls for one fixed model, plus deterministic
references. This is a proposed budget, not a power calculation or approved run.
Unavailable compressed-only tasks must be marked explicitly. Prefer a smaller dry
run to validate instrumentation before allocating these calls.

Freeze independent task IDs and paired order randomization. Separate development
and hidden test task templates/events. Repeated calls are not independent fires.
Choose confirmatory group counts from pilot variability and scientifically meaningful
precision; predeclare equivalence margins, primary contrasts and multiplicity.
Retain failures, invalid outputs, retries, vetoes, abstentions and exact call usage.
Execution eligibility, workflow success and scientific correctness remain distinct.

## Deliverables and phases

1. **Input/API audit:** Pin upstream commit/package environment; inspect the exact
   source schemas and rights; select bounded local inputs explicitly. No automatic
   FIRED/gridMET downloads or data-lake rebuild. Avoid a full Arrow/Parquet read just
   to discover columns; inspect schema metadata and bounded batches.
2. **Offline adapter:** Isolated Fire VASE worker and typed JSON evidence/results.
   Validate units, dates, per-fire IDs, support, checksums and operation allowlists.
   No arbitrary Python callable, dynamic model code or generic shell endpoint.
   Reuse upstream algorithms; core pipeline remains independent of this dependency.
3. **Generated harness:** Analytic answer keys, valid/invalid/gappy/duplicate cases,
   split and future-data leakage tests, deterministic request replay and cost logs.
   Record code/validator/upstream identities and exact metadata evidence views.
4. **Reviewed real pilot:** Rights-reviewed event cohort, expert relevance rubric,
   fresh split-bound artifacts and model/prompt/runtime verification. Then paired
   model calls with frozen protocol and budget. No silent fixture fallback.
5. **Extensions:** Neural sequence models, geometry/weather, adaptive selection and
   a second environmental case, each with separately reviewed capability additions.

Implemented files: `src/dataset_prototype/embedding_study/` for isolated adapter
contracts/evaluation, `tests/` for offline tests, `data/fixtures/embedding_utility/`
for tiny generated fixtures, this folder for protocol/case manifests and curated
compact outputs, ignored `run/embedding_utility/fire_vase/<run-id>/` for private run
artifacts. The synthetic capabilities are implemented; real-data and agent extensions remain
planned. This case
is not a third science track and does not change production scientific contracts.

## Main figures

- Metadata × representation interaction plot: success and paired embedding advantage,
  with per-task strata; separate panels by agent policy/model.
- Accuracy–cost frontier: first-use and repeated workloads, including metadata labor,
  training, indexing, caches, source reads, retries, storage and refresh.
- Label/query-budget learning curves; PCA dimensions vs held-out utility.
- Fidelity curves: neighbor overlap/rank stability vs dimension, seed, depth and
  perturbation. Geometry agreement is not independent scientific validity.
- Prefix skill vs observed history length, with naive baselines and time-safe inputs.
- Representation-choice phase diagram only after measured cells exist. Mark unsupported
  regions unknown; include routing overhead and direct cached computation as rivals.

## Milestone 1 implementation status

Completed under the user's implementation request: versioned history/task/artifact
contracts; synthetic train/evaluation fixtures; isolated pinned upstream worker;
R0/R1/R2 views; independent rational/SVD keys; M0/M1/M2 isolation; deterministic
cache-aware runner; per-query and preparation telemetry; integrity/replay tests;
structured synthetic results and a concise report. See
[implementation report](implementation-report.md) and
[next agent components](agent-experiment.md).

Corrections to initial planning: the first benchmark has 29 deterministic tasks,
three strict interfaces and no adaptive/model calls. The old 288-call model pilot
remains an inert proposal. A compatible complete upstream fitted artifact was not
assumed; a synthetic-only training fit is recorded and reused within each run.
R2 neighbor fidelity backprojects to original profile units to separate compression
from changing the comparison metric. Real cumulative-versus-ring definitions,
rights/support/availability and independent relevance remain unresolved before real
case execution. No forecasting, neural learning or unrestricted runtime code was added.

## Milestone 1 completion and deviations

The [implementation report](implementation-report.md) records 34 synthetic fires,
29 task definitions and 1,566 attempts across R0/R1/R2, M0/M1/M2, cache modes and
repeats. Canonical inputs, independent rational/SVD references, explicit abstention,
artifact integrity, metadata isolation and preparation/query accounting are working.
The full offline suite passed 262 tests with 2 skips; pinned-backend tests are explicit.

Phases 2–3 are implemented for synthetic data. Phase 1 confirmed code/API identity,
but real-input rights/support and source cumulative/ring equivalence are still open.
Phases 4–5, adaptive routing, neural encoders, expert scientific analog labels and
prefix prediction remain planned. The old 288-call agent proposal is unchanged and
unexecuted; the new deterministic config is separate and does not imply model approval.

No complete reusable upstream PCA artifact was loaded. Instead a fresh, declared
training-only synthetic fit is frozen once per run and reloaded; historical manuscript
fits are not substituted for held-out benchmark artifacts. Cold/warm means application
query caches, not cold source storage. Identical deterministic answers across metadata
views validate experimental isolation only. Exact information loss is tested separately
from an explicitly approximate PCA-neighbor diagnostic. No literature review, original
proposal, upstream scientific audit or upstream implementation was rewritten.

A final interface audit identified retained source-ID counts and validated primary
eligibility in provenance. R1/R2 now use that metadata for the declared consecutive
sequence-length query. The normalized payload omits length, but the full interface
does not; absolute size and native dates remain unavailable. This correction avoids
calling retained metadata an information-loss failure.

## Milestone 2 completion — controlled synthetic agent infrastructure

Implemented fixed R0/R1/R2 and adaptive regimes, evidence-only M0/M1/M2 rendering,
typed proposals, per-source/representation authorization, uniform sanitized feedback,
receipt-backed answers, budgets, mock and optional verified-provider transports,
explicit contract routing, independent selection/reasoning diagnostics and accounting.
The frozen protocol executed all 348 cells with three mock repetitions (1,044
episodes) and 348 separate deterministic baseline episodes. Scientific answerability
and previous reference keys/artifacts are unchanged. See
[milestone 2 report](milestone-2-report.md) and [protocol](agent-protocol-v2.md).

The full offline suite passed 290 tests with 2 skips. The source/alias/gold boundaries,
rejections/recovery, budgets, provenance, full matrix replay and report regeneration
are tested. Actual model evidence remains absent: the gateway was not reachable from
this session and live access/cost authorization was not established. The adapter and
predeclared small smoke configuration are ready but disabled; no fallback substitutes
mock data for a failed live call. Held-out-pending inputs remain explicitly unavailable.

H1–H4 stay hypotheses. Identical mock metadata outcomes are an isolation check; the
mock ignores metadata. The mock adaptive policy matches fixed R0 and the explicit
router in this controlled suite. These are not LLM comparisons or ecological results.
The original code-writing, real-data, forecast and neural extensions remain deferred.

## Milestone 3 — expanded synthetic utility, real inference pending

The [M3 report](milestone-3-report.md) and [frozen protocol](agent-protocol-m3-v1.md)
add 120 evaluation questions with separate training/development/evaluation histories,
independent numeric references, targeted/cached R0 rivals, explicit projected versus
full-profile queries and development-only public cost calibration. The full matrix
contains 2,880 mock episodes plus 360 rule-router episodes. Task-specific sufficiency,
correctness, selection, scientific cost and routing remain separate.

The original R0-first equality is not evidence against representation efficiency;
it follows from a simple mock and information dominance. Nor does a faster lookup
prove lower total cost. Real metadata/agent effects remain unmeasured because this
session has no verified reachable authorized inference. The disabled real pilot
configuration binds new frozen inputs and requires smoke/access/no-charge checks.
M1/M2 history and the original proposal/audits remain unchanged. Neural, real-source,
forecast and expert analog extensions are still deferred.

## Milestone 4 — explicit learning extension, real evidence still pending

The user's new milestone authorizes a minimal neural experiment, superseding the
previous deferred-neural scope for this isolated study only. The
[M4 report](milestone-4-report.md) records completed prefix-only synthetic prediction,
strong raw/PCA/summary/capacity baselines, held-out evaluation and materialization.
Production MOSAIKS and scientific review gates are unchanged. Real source data exist
in documented legacy paths but require experiment-specific rights/support/availability
review; no source rows were ingested. Real agent smoke/pilot remain unexecuted under
the unchanged frozen protocols. See the new evidence table and unsupported claims.

## Milestone 5 — cross-task transfer and heterogeneous reuse

The [M5 report](milestone-5-report.md) records frozen A-only transfer, new lightweight
heads, joint AD and task-specific training, predictive-outcome retrieval, observed-
property probes and multihead reuse. B/C/D/E targets are independently defined from
future observations but correlated. Full task matrices and fire-paired summaries
retain losing as well as winning comparisons. Same-fire retrieval is excluded.
This is a new frozen task protocol on the existing synthetic M4 cohort, not a new
blind cohort or ecological evidence. Original source, encoder and M1–4 artifacts
remain immutable. Real-agent and real-source scientific evidence remain pending.

## Milestone 6 — packaged real-source review, stop before rows

The user identified the local Fire VASE lake; selected artifacts under its packaged
`files/` root are present and need no upload/download. The [M6 report](milestone-6/report.md)
records metadata-only source inspection, proposed native/support/prefix/target/fold
recipes, rights/attribution assessment, review packet, pure validation and conditional
cohort/model/cost design. No observation rows, adapter, real cohort or training ran.
Actual source availability is no longer the claimed blocker; human meanings/rights,
current identity and prospective availability remain explicit review requirements.
The user requires stopping at that boundary. M1–5 remain immutable.

## M7 full-lake extension

Metadata inventory and offline streams/model/statistical kernels are implemented.
All-row authorization supersedes the proposed 512-row cap only after external review.
Real training orchestration, scientific classification/geometry/environment definitions
and empirical evaluation remain pending. See [M7 report](milestone-7/report.md).

## Milestone8 execution status

**WORKING:** real full-population observed-scientific-state utility experiment
completed. See [methods, measured findings and retained artifacts](milestone-8/README.md).
This extension does not relabel earlier planned/raw-sequence work as executed.
