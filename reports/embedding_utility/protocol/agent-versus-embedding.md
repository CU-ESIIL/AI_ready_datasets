# Is embedding worth it when an agent can work with source data?

Status: **UNDER ANALYSIS**. Draft v0.2, 20 November 2026. No measured agent conclusions. Generated representation diagnostics
are retained in [first results](../results/first-benchmarks.md).

## Central question

Does materializing an embedding layer provide enough additional scientific task
success, speed, cost savings or reuse to justify its preparation, information loss,
maintenance and governance, compared with an agent using source data through tools?
The claim that agents already do this well is a hypothesis to measure, not a baseline
score to assume. An agent and an embedding are not interchangeable components:
an agent can choose to use either source operations or embedding consumers.

“Raw” means source-native access without an embedding layer, not permission to skip
calibration, quality checks, harmonization or scientific review. Distinguish native
observations, reviewed harmonized values, summaries and vectors in every trace.
Tool-mediated queries and bounded computations count as direct-data access; do not
handicap this arm by pasting entire rasters into the model context.

## Working theory

For an encoder fixed independently of the held-out target, a representation made
only from the available input cannot create new target information. It can make
information easier to exploit under limited compute, labels, context or learner
capacity. Conversely, discarded detail can matter for a new question. This is the
information-bottleneck framing, not a proof of either system's practical superiority.
Pretrained encoders introduce external training information and must declare it;
compare that exposure explicitly rather than treating them as pure compression.
See [Tishby et al., information bottleneck](https://arxiv.org/abs/physics/0004057).

Our hypotheses: embedding may pay off for repeated similar tasks, expensive source
reads and useful shared spatial features; direct access may win for one-off exact
queries, rare details, changing questions and meanings needing native evidence.
A hybrid may be preferable when vectors narrow a search and source tools verify
it. None of these are established findings. An agent's transient internal model
representations are outside this comparison: the intervention is a separately
computed and retained embedding product.

## Primary controlled experiment

Hold the agent/model version, prompts, task evidence, scientific permissions,
source eligibility, budgets and evaluator constant. Vary the data interface:

| Arm | Available interface |
| --- | --- |
| A: direct | Source metadata plus registered bounded source operations and exact queries; no materialized embeddings |
| B: embedding | Same metadata plus frozen vectors and declared trained heads/retrieval tools; no source-value fallback |
| C: hybrid | Both interfaces, with every fallback and its cost recorded |
| D: deterministic reference | Predefined task-specific workflow without agent decisions |

B must have a real consumer: arbitrary vector coordinates are not interpretable
LLM evidence. If no appropriate trained consumer exists, record the arm as unavailable,
not a model failure or evidence against all embeddings. Include simple summaries,
indexes, caches and conventional models as alternatives: savings from reuse alone
must not be attributed uniquely to embeddings. Match caching policy, tool maturity
and task-specific engineering effort. An embedding arm's additional tools are part
of the system intervention; ablations separate representation from tool effects.

This study keeps the repo's trust boundary: model roles receive evidence envelopes
and return registered operation selections/parameters; deterministic software owns
access and computation. No generated Python, SQL, formulas or arbitrary shell runs.
This tests agents within that boundary. Claims about unrestricted code-writing agents
would need a separate explicitly governed study and must not be inferred here.

## Task portfolio and stress tests

Evaluate complete scientific questions, not convincing prose. Proposed families:
exact value/threshold queries; aggregates and trends; spatial-pattern prediction;
similarity search with expert relevance judgments; anomaly/detail recovery; and
new questions on a previously encoded cohort. Each needs its own case protocol,
independent answers and support/rights review. These are task candidates, not new
registered capabilities. MOSAIKS is an initial raster case, not the scope limit.
Text, table and time-series embeddings require distinct encoders and case evidence.

Vary data volume, query repetition, question novelty, missingness, spatial/temporal
shift, model capacity and budget. Include queries designed to require information
an encoder discards. Freeze a pilot subset before expanding; do not build the whole
factorial at once. Exact synthetic answers test mechanics; scientific real-case
answers need independent deterministic evidence or actual expert adjudication.
Assistant-authored references are drafts, never expert gold.

## What counts as worth it?

Primary outcome: independently verified task success within a declared time/cost
budget, including scientific correctness, units/support, provenance and abstention.
Keep factual correctness, unsupported claims and scientific gate compliance separate;
enforced non-execution is not demonstrated model competence. Record all attempted
tasks, failures, timeouts, retries and human interventions, not only successful calls.

Also measure end-to-end latency, source bytes/windows read, inference usage,
CPU/GPU time, peak memory, retained storage, label/expert effort and maintenance.
Count embedding preparation, source scans, head training and refresh after source,
recipe or encoder changes. Report first-question and repeated-workload costs;
separate valid pre-existing reusable artifacts from experiment-created ones.

At comparable correctness, look for the workload where measured cumulative savings
exceed preparation and refresh costs. If direct access is already cheaper per task,
no cost break-even is demonstrated for that workload. Do not assume constant marginal
cost or invent a universal conversion between accuracy, money and scientific risk.
Show tradeoffs and let case-specific thresholds determine practical value.

Pair tasks across arms, randomize order, isolate caches/state and repeat model seeds
as needed. Independent tasks/sites, not repeated calls alone, support generalization.
Freeze graders, thresholds, budgets, sample-size/precision rationale and held-out
cases before testing. Use blind adjudication where feasible and report paired
uncertainty. Distinguish benefit, disadvantage, practical equivalence and inconclusive
results as in the [study plan](study-plan.md).

## Phases and stopping decisions

1. Audit which direct operations and embedding consumers exist versus need work.
2. Freeze a small generated task suite spanning exact lookup, pattern prediction
   and intentional representation loss; verify the harness offline.
3. Review one real case and run A/B/C/D with complete cost accounting.
4. Expand across modalities and workloads only after pilot feasibility; preregister
   confirmatory cases and retain negative findings.
5. Produce an empirical decision map: direct, embedding, hybrid or insufficient
   evidence by task/workload. A finding that embeddings are unnecessary is a useful
   result and does not require redesigning the production pipeline automatically.

## Evidence leads and limits

[MOSAIKS (Rolf et al., 2021)](https://doi.org/10.1038/s41467-021-24638-z)
provides a reusable-feature approach for satellite prediction; it does not settle
agent-versus-source utility. [Spider 2.0](https://arxiv.org/abs/2411.07763) studies
complex database agent workflows; its reported systems and tasks are not evidence
that today's agents succeed on this scientific pipeline. These are starting points,
not a completed literature review or transferable benchmark scores.
