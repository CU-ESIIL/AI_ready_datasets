# Mathematics and first benchmark graphs

Status: **UNDER ANALYSIS**. Analysis v0.2, 20 November 2026.
The [first results](../results/first-benchmarks.md) are generated diagnostics,
not a test of agent competence or independent scientific outcomes.

## 1. Cumulative cost and break-even

For one fixed workload horizon, let P be embedding preparation, R total refresh
cost, d direct cost per question and e embedding cost per question. In a single
consistent unit:

```text
C_direct(Q) = Q d
C_embedding(Q) = P + R + Q e
Embedding is cheaper when Q(d − e) > P + R.
If d > e: first strictly cheaper integer Q = floor((P + R)/(d − e)) + 1.
If d ≤ e: no strictly cheaper Q under these nonnegative fixed-cost assumptions.
```

For assumed P=120, d=3 and e=1, costs tie at 60 questions; embedding first wins
at 61. Add R=60 and it first wins at 91. These are arithmetic scenarios, not
measured prices, agent timings or expected project usage.

For real runs, sum observed question-specific costs and refresh events rather
than assuming constant marginal cost. Count source scans, filters, head training,
inference, retries, cache/index construction, storage and human effort. Compare
systems at a declared minimum correctness; cheaper wrong answers are not a win.
Use the same caching policy. A direct-data system can also amortize work.

## 2. Compression and lost information

With one fixed encoder Z=f(X), squared-error optimal prediction uses conditional
means m_X=E[Y|X] and m_Z=E[Y|Z]. For finite second moments:

```text
optimal MSE using Z − optimal MSE using X = E[(m_X − m_Z)²] ≥ 0.
```

To see this, expand Y−m_Z=(Y−m_X)+(m_X−m_Z); the cross term has zero expectation
conditional on X. Thus deterministic compression alone cannot improve the best
possible predictor with unlimited capacity and the same information. It can improve
a limited learner's efficiency or inductive bias. A pretrained encoder's external
training information must be accounted for separately. This is a theoretical bound,
not a prediction that today's agent achieves the direct-data optimum. The
[information bottleneck](https://arxiv.org/abs/physics/0004057) frames which target
information a compressed representation retains.

In the ideal mean-centered MOSAIKS filter w, sum(w)=0, so a constant brightness
shift c gives w·(x+c)=w·x. Pooling cannot reconstruct that removed offset. Finite
precision and implementation details qualify exact invariance; the generated
brightness experiment measures the effect in the actual repository encoder.

Float32 payload ratio = embedding dimensions / (channels × height × width).
For our 1×12×12 windows, 128 features occupy 512 bytes versus 576 input bytes
(about 0.89×); 512 features would occupy 2,048 bytes (about 3.56×).
Metadata, filter banks and storage compression are excluded. Embedding does not
necessarily mean smaller storage.

## 3. Classic graphs and how to test them

| Graph | Axes and comparison | Test design / current status |
| --- | --- | --- |
| Learning curve | Held-out error or task success vs labeled training examples | Same nested subsets; training-only preprocessing; paired groups. Generated ridge curves run here. |
| Accuracy–cost Pareto frontier | Correctness vs total cost or latency at multiple budgets | Same tasks for direct/embedding/hybrid, include failures and setup; dominated systems lose on both axes. Agent frontier not yet measured. |
| Amortization curve | Cumulative cost vs questions/reuse | Measure first query and repeats, direct caches and refreshes. Assumed-cost algebra plotted here. |
| Representation-size / rate–distortion curve | Task error vs dimensions or retained bytes | Freeze each train-fitted encoder; count filters too. Three MOSAIKS dimensions tested; this is task distortion, not a theoretical rate–distortion bound. |
| Transfer/degradation curve | Task success vs held-out region/time or defined shift severity | Frozen encoder/head policy, independent labels and groups; no geographic transfer evidence from generated iid tiles. Planned. |
| Scaling curve | Time/memory/read volume vs data or workload size | Same resources, bounded access, cold/warm runs and repeated measurements. Local encoding timing only; scaling not yet measured. |
| Risk–coverage curve | Error among answered questions vs fraction answered | Same tasks, abstention rule and frozen confidence threshold; keep abstentions and failures. Planned for real agent runs. |

[Scikit-learn's learning/validation-curve documentation](https://scikit-learn.org/stable/modules/learning_curve.html)
describes sample-size and parameter diagnostics. [AI Agents That Matter](https://arxiv.org/abs/2407.01502)
motivates joint accuracy/cost evaluation and careful holdouts. The
[MOSAIKS paper](https://doi.org/10.1038/s41467-021-24638-z) is a reference for
reusable raster features, not proof they beat agent source access.

ROC/precision–recall curves are useful for an actual detection task, not a generic
answer to embedding utility. Likewise a visually attractive t-SNE/UMAP cluster plot
cannot establish task benefit or scientific semantic equivalence.

## 4. First agent benchmark to build

Use the same agent/model and deterministic tool permissions with direct, embedding
and hybrid interfaces. Include a deterministic reference. Predefine tasks that
require exact details, pattern prediction and changed questions; keep unit/support
and provenance correctness visible. Source data are synthetic initially, with
independent generators and deterministic answer keys. All numerical computation
remains in pre-written tested functions; models select permitted operations only.

The current study predicts simple statistics with ridge heads. It has no model
calls, tool-choice decisions or agent-success scores. Its strong summaries include
the exact mean/std target by design: they represent an easy tool a competent agent
could select. This is a useful sanity check, not an independently labeled prediction
benchmark and not evidence that a particular agent will select that tool correctly.
