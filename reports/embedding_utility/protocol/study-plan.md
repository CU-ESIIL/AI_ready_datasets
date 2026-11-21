# Supporting raster study plan v0.1

Status: **UNDER ANALYSIS**. Draft for review; no approved real cases. Generated exploratory diagnostics
are retained in [first results](../results/first-benchmarks.md).

This is the raster-prediction sub-study of the broader
[agent-versus-embedding question](agent-versus-embedding.md). It cannot by itself
establish whether embeddings add value over capable agents using source tools.

## Questions

- Prediction: do embeddings improve held-out outcomes over strong alternatives?
- Label efficiency: does the difference change with training-label count?
- Transfer: do gains survive held-out geography, time and, when justified, sensors?
- Information loss: which targets favor summaries or direct inputs?
- Operational utility: what are the accuracy, compute, storage and reuse tradeoffs?

Begin with raster prediction and existing MOSAIKS. Retrieval and LLM consumption
need separate protocols and relevance judgments. Vector proximity does not establish
scientific similarity, semantic equivalence or compatibility.

## Comparison arms

| Arm | Purpose |
| --- | --- |
| Training mean / class frequency | Trivial reference |
| Reviewed raster summaries + regularized linear head | Interpretable compression baseline |
| Same summaries + suitable nonlinear learner | Check learner-capacity effects |
| MOSAIKS + matched regularized linear head | Primary representation comparison |
| Summaries + MOSAIKS + matched head | Incremental information |
| Direct harmonized inputs + suitable learner, if feasible | Compression loss |
| Shuffled training labels | Leakage diagnostic, not a competitive baseline |

Summary definitions, nonlinear learners and budgets require case-specific review.
Use identical eligible observations, labels, support, splits and paired training
subsets, with comparable tuning budgets. Report matched-head and best-budgeted
pipeline comparisons separately. Missing competitive baselines limit conclusions.
All arms consume the same approved bounded windows. Direct-input methods must stay
bounded in memory; infeasibility is reported rather than writing raster snapshots.

## Cases and evidence

Start with generated diagnostic cases to test mechanics: proposed texture,
brightness-sensitive and null targets expose possible strengths and failure modes.
Their generators and expectations need reviewed deterministic tests. They are not
independent scientific evidence.

Next select one feasible independently labeled real task as a pilot. Broader claims
need multiple scientifically distinct tasks, regions/times and failure-oriented
cases. No datasets have been selected. Declare the task population, selection rule,
exclusions and unavailable cases so convenience sampling is visible.

Each real case needs source/version/rights, label method and independence, units,
actual spatial/temporal support, alignment evidence, uncertainty and expert review.
Keep derived diagnostics, proxies and independent labels separate. Do not invent
tower-to-pixel associations. Missing rights/support evidence blocks the case.

## Splits and fitting

Freeze independent units, geographic groups/buffers and temporal holdouts before
fitting. Nonoverlapping tiles can still be autocorrelated. Keep repeated observations
and overlapping footprints together; audit duplication and label leakage. Buffer
sizes need scientific justification.

Fit empirical filters, scaling and all learned preprocessing on training only.
Tune on validation only; freeze protocol and arm selection before test access.
Learning curves use paired nested training subsets with fixed validation/test units.
Distinguish label count from unlabeled filter-fitting exposure. Predeclare fixed
training-reference filters versus subset-specific refitting. Transfer experiments
state which encoder/head is frozen or refitted; no silent holdout adaptation.

## Analysis and interpretation

Before test access, select one primary metric per case, direction and scientifically
meaningful minimum benefit. Specify an equivalence margin separately if needed.
Group counts, repeated seeds and uncertainty methods remain undecided: choose them
from pilot variability and desired precision. Seeds are not independent geographic
replicates. Use paired differences and uncertainty at the independent group level.
Predeclare primary contrasts, secondary analyses and multiplicity handling.

A benefit needs uncertainty supporting the practical threshold against the strongest
eligible baseline. A disadvantage can be supported similarly. Practical equivalence
requires sufficient precision within its prespecified margin. Nonsignificance alone
means inconclusive, not no usefulness. Report per-case results before aggregates;
retain failures, exclusions, negative outcomes and all planned comparisons.
Date amendments; test-informed analyses are exploratory and require fresh holdout
confirmation. A finite portfolio cannot establish embeddings universally helpful
or useless.

Measure filter-fit, encoding and head-fit time, memory measurement method, feature
bytes, tuning budget and inference cost with hardware/software identities. Separate
one-time costs from repeated-task reuse, cold/warm runs and source acquisition.
Report accuracy-cost tradeoffs without inventing a universal utility score.

## Pipeline boundary

Reuse reviewed harmonization, MOSAIKS and provenance; do not copy core pipelines.
Preserve source/version/checksum scope, frozen recipe/review/human-decision identities,
encoder/preprocessing identity, splits, seeds, label origins and environment.
Scientific ambiguity and existing vetoes remain binding. No planning record grants
execution permission. Raw/harmonized real windows stream directly to consumers.

Existing `embedding_dataset.verify_dataset` provides integrity checks and a bounded
ridge/mean/shuffled-label diagnostic. It is not this comparative study runner.
Generated texture performance is not independent ecological validation.

## Sequence

1. Review this protocol and fill one case template, including primary comparison.
2. Build an offline synthetic harness with independent positive/invalid tests,
   leakage checks and deliberately uninformative cases.
3. Review real-pilot labels, rights, support, sampling, recipes and execution gates.
4. Freeze a versioned run plan; evaluate the held-out pilot once.
5. Expand to a predeclared portfolio and report positive, negative and inconclusive
   findings with costs and scoped limitations.
