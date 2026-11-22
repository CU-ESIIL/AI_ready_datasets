# Full-lake scientific protocol — proposed, not scientifically approved

## Estimand and representation hypothesis

Estimate paired held-out whole-fire loss differences for R3 learned representations
against R0 native-supported windows, R1 interpretable features and R2 classical
coordinates. Representation utility depends on the task, supervision, support,
training population and query workload. A geometric resemblance is not ecological
relevance. Exact information availability, prediction accuracy, scientific relevance
and resource cost are separate outcomes.

No sample size or statistical power is claimed before approved profiling. All
primary analyses use all eligible fires. Prefixes are repeated measures; task-specific
eligibility does not require every unrelated outcome to be present. Report exclusions,
overlaps, unique fires, windows, intervals and supported transitions separately.

## Canonical observation recipe proposal v1

A reviewed SourceBinding fixes native event/date/area fields, whole-container SHA256,
km2 meaning, exact date interpretation, grouping/order, quality and uncertainty
evidence, and optional availability/cumulative fields. Native ID types, values, date
text, quality, checksum and uncertainty remain attached in the in-memory stream.
No calibration, ring-to-cumulative equivalence, imputation, differencing of unrelated
cumulative products, or cross-product join is inferred. Negative/nonfinite areas,
duplicate dates or out-of-order events fail closed. Missing area stays missing;
observed zero remains zero. Gaps break supported windows. Summed observed-window
area is explicitly derived and is not an independently observed final event total.

Parquet reading projects reviewed columns in bounded batches; no raw or harmonized
rows are persisted. Completed event keys and summary counts may be stored privately
in SQLite. Source-order review is required: the implementation refuses reappearing
fire IDs rather than materializing an external raw-data sort. Other source formats
need reviewed streaming adapters before row access. Logical batch bounds do not
prove physical Parquet-page or encoder peak memory; measure those after approval.

## Cohorts and task accounting

| Cohort | Proposed eligibility | Unresolved scientific scope |
| --- | --- | --- |
| A | At least one supported area observation for basic summaries | Full-history descriptive eligibility requires review |
| B | Consecutive run supporting a depth plus future horizon | Report each depth/horizon separately |
| C | Long consecutive histories; prototype flag uses 14 days | Full developmental stages and complete-life boundaries undefined |
| D | Reviewed native geometry and support | Geometry, CRS and scientific association not approved |
| E | Reviewed covariates with time/space support | Alignment and availability not approved |

These flags are operational proposals, not validated fire-life definitions. A
complete observed run does not prove complete ignition-to-extinction observation.
D/E stay unknown, not false. Cohort overlaps must be counted from approved event
identities. Full profiles above the historical closed-worker capacity need upstream
scaling review; do not silently exclude long fires or reuse the 512 audit cap.

## Task families

1. Future increments: exact next day, next 3/7-day sums, mean successive future
   differences and population SD over the supported future interval. Independent
   Fraction summation checks totals. Input depths are 3/7/14/30, horizons 1/3/7.
   All are retrospective reconstructed targets, not operational forecasts.
2. Developmental classification: independently reviewed allocation, pulse, stage,
   acceleration and fragmentation criteria are required. Existing synthetic labels
   cannot become real scientific gold. This family remains scientifically undefined.
3. Retrieval: future observed trajectory relevance, same-fire exclusion and a strong
   supervised raw rival. Freeze gallery/query independence and relevance thresholds
   before held-out evaluation. Exact bounded-memory search is available; no ecological
   analog claim or full-scale retrieval result exists.
4. Information preservation: separately test exact support/identity survival and
   train-only approximate probes of scale, ordering, allocation, variability and
   pulses. Failed probes do not establish information-theoretic absence.
5. Transfer: whole-fire temporal/geographic holdouts and size, depth, source-quality,
   stage/environment strata where supported. Region evidence is required; unknown
   regions do not receive guessed labels. Report long-history selection bias.
6. Computational utility: optimized native queries, native/answer caches, summaries,
   classical coordinates, on-demand encoders and materialized vectors. Adaptive
   routing requires independent validation; deterministic routing is not agent skill.

## Methods and leakage controls

Raw ridge/logistic and optional histogram trees are callable. Interpretable prefix
summaries are distinct from reviewed full VASE morphology. Incremental centered,
unscaled covariance PCA and uncentered SVD fit training data only; these are not
historical standardized PCA without matching preprocessing. TCN kernels are fixed
prewritten code, with dimensions 4/8/16/32/64 and supervised, task-specific, shared
multitask or masked-observation objectives. Missing task labels use per-head support
masks rather than global complete-case filtering.

The masked reconstruction objective removes cumulative channels at both training and
inference to prevent a trivial difference shortcut. Its artificial mask is not native
missingness and its scientific value remains a hypothesis. No augmentation invariance
is assumed. The mean/last pooled trunk has dimension 16: 32/64 outputs are overcomplete,
not additional compression. Count actual parameters and control supervision, tuning,
head capacity and training cost before interpreting comparisons. No capacity-matched
full-lake experiment has been executed.

## Prespecified comparisons and uncertainty

Compare learned versus raw/features/PCA, shared versus task-specific, supervised
versus self-supervised, and materialized versus on-demand. Proposed metrics are
fire-mean log-MSE, Brier score for reviewed binary criteria, future-relevance
precision@10 and scoped lifecycle cost. Scientist-selected meaningful differences
are **unknown** and block training/evaluation in the draft gate. Classification and
relevance metrics cannot run until independent target criteria exist.

Choose disjoint training, selection, calibration and test year blocks and held-out
regions before test evaluation. Use nested deterministic whole-fire fractions
1%, 3%, 10%, 30%, 100% with identical untouched test sets. Freeze training-only
normalization, empirical filters, PCA and all hyperparameter selection. No seed,
region or cutoff is selected using test outcomes. Separate train-size curves from
compute-budget curves and document infeasibility rather than arbitrary downsampling.

Aggregate paired differences within fires first; examine higher-level year/region
clusters and model refits for training uncertainty. Empirical cluster bootstrap is
implemented but does not automatically justify population confidence intervals.
Power depends on independent clusters and paired variance, not fire-day count.
After reviewed profiling, estimate detectable effects using training/calibration
clusters; freeze a primary family before Holm correction of justified p-values.
Calibration curves, rare-fire strata and sensitivity bounds are required outputs,
not measured findings yet.

## Stress tests and classic graphs to generate after approval

| Graph | Controlled comparison | Interpretation limit |
| --- | --- | --- |
| Learning curve | Paired fire loss versus training fires, fixed test | Includes tuning/training budget |
| Dimension curve | Loss/probe recovery versus dimension | Parameter count changes; 32/64 overcomplete |
| Transfer matrix | Training objective by held-out task/region | Same information and split rules |
| Calibration/reliability | Predicted versus observed held-out outcomes | Independent bins/uncertainty |
| Retrieval precision–recall | Independent future relevance | Mathematical relevance only |
| Stress response | Loss versus missingness/aggregation/noise/order/scale | Artificial versus natural perturbations separate |
| Cost–accuracy frontier | Complete measured cost versus same-task loss | Unknown components excluded |
| Amortization curve | Total cost versus query count/refreshes | Cache/refresh regime explicit |

Use predeclared perturbations of copied model inputs, never mutate source observations
or rebrand altered support as native. Review uncertainty magnitudes and aggregation
before use. Natural quality strata and artificially corrupted inputs are different
estimands. Report rare large fires and excluded long histories prominently.

## Computational economics

For each same-task workload, C(Q,R)=loading+harmonization+features+training+
materialization+Q*query+R*refresh. Measure storage/index construction, inference,
cache warm/cold behavior, throughput, memory, dependency/runtime identity and query
mix separately. Unknown costs remain unknown. Break-even between methods a,b is
Q*=(fixed_b-fixed_a)/(query_a-query_b) only for identical refresh assumptions and a
positive denominator; otherwise no amortization advantage is implied. Source/model/
recipe changes invalidate affected cache products. A Pareto point requires the same
scientific acceptance requirements. No empirical scaling graph exists yet.
