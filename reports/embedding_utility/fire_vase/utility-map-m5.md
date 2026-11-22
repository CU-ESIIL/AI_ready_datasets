# Task-dependent representation utility map

**Conditional synthetic evidence, not a universal phase diagram.** All predictive
outcomes are stochastic and unobserved at issue time; no representation is exactly
sufficient to determine them. “Useful” below means measured predictive/ranking
performance at a fixed declared target, not scientific approval or exact preservation.
No independently approved real-fire accuracy tolerance was supplied.

| Task | Required information / target | Retained observations | Approximate result | Failure / reuse implication |
| --- | --- | --- | --- | --- |
| A next day | Available prefix; next single day log growth | Raw tensor retains full supplied past; frozen A trained for this target | Raw ridge 0.060737 MSE; frozen A 0.060796; joint AD 0.072711 | Joint supervision produces negative transfer on A in this run; shared encoding does not ensure better prediction |
| B 3-day total | Independent next three increments; absolute units retained | Prefix summaries compress sequence; learned/PCA are lossy | Raw 0.114779; frozen A 0.118626; joint AD 0.122286 | A-trained signal transfers imperfectly; no demonstrated learned advantage over raw on this target |
| C relative future acceleration | Next-three mean versus last-three observed mean; binary, not physical second derivative | Past level/trajectory matters in addition to next-day signal | Raw Brier 0.160051; frozen A 0.204011; joint AD 0.155780 | Strong A performance does not imply support for this decision. Added C supervision helps; conditional interval for joint-vs-raw includes zero |
| D future variability | Population SD of three future increments | Past variability/ordering may help, but future variation remains uncertain | Raw 0.124811; frozen A 0.136228; joint AD 0.129519; specific D 0.147380 | Task-specific retraining is not guaranteed to help; cannot call it necessary from one winning or losing trial |
| E future-pattern retrieval | Distances between independently held-out future log-increment vectors | Geometry of past input need not align with future relevance | Direct-distance P@10 raw 0.0832, frozen A 0.1023, joint AD 0.1082 | Learned distances align better with this declared relevance than raw distances. This is not ecological analog discovery |
| E with a new trained head | Three train-only future-vector outputs; same held-out relevance | Supervised raw head can learn an outcome-oriented metric | P@10 raw head 0.1273, frozen-A head 0.1125, joint-AD head 0.1070; direct E MLP 0.1336 | Strong outcome-trained raw/capacity controls reverse the direct-distance ordering. Head training must not be mistaken for unsupervised retrieval |

Losses and paired descriptive intervals are in [complete results tables](results-tables-m5.md).
C uses Brier; A/B/D use log-transformed MSE, so do not average them as a single
scientific utility number. E precision equals recall for equal-size top-ten sets.
Every method has the same query/cohort/target support; original A-only transfer,
added AD supervision and E-specific supervision remain separately labeled.

## Preservation is task and interface dependent

The raw tensor can recover supplied observed increments/masks within floating
precision. Interpretable summaries explicitly retain observed size and recent rate,
but do not establish a full sequence inverse. PCA4/frozen4/shared4 are not generally
invertible. Source lineage/IDs/dates remain available in the experiment's full
interface and are not declared lost just because they are absent from numeric vectors.

Linear probes show approximate recoverability of source scale, order centroid,
recency, acceleration, local maxima and variability. Nonlinear kernel probes often
recover additional information (with more capacity). Failed linear probes therefore
do not establish absence. Success is predictive, not exactness or causal understanding.
Completeness is constant among validated inputs, and invalid schedules abstain;
no learned completeness-competence result is claimed.

## Reuse conditions observed here

A four-task shared AD encoder bundle costs about 45.9 µs on demand versus 144.7 µs
for separate aligned encoders. Raw preprocessing plus four heads costs 18.1 µs.
Stored shared-vector heads cost about 9.8 µs; cached complete bundles about 0.17 µs.
These are local warm CPU/interface measurements, not matched-accuracy deployment
winners. Training, vector construction, file I/O and refresh cannot be ignored.
The full economy artifact retains each K=1/2/3/4 task bundle and preparation crossover.

For N bundles and K distinct heads,

`C_shared = T_shared + P_shared + N (E_shared + H_K)`;

`C_separate = Σ T_task + Σ P_task + N Σ (E_task + H_task)`.

Stored vectors replace repeated E with one materialization M only when its cost can
be repaid. Identical complete bundle caching is a different regime from selecting
new/heterogeneous task heads. Original A acquisition and current training are separate;
common costs cancel only when truly shared. Source/model/head changes invalidate
relevant products, and the number of maintained checkpoints differs. Actual refresh
frequency, storage-service costs and human maintenance/review labor remain unknown.

No condition here establishes that task-specific models are necessary, that a shared
representation wins complete lifecycle cost, or that raw dominates every possible
scientific workload. The data show mixed task tradeoffs, a restricted retrieval gain,
and scoped reuse savings relative to separate neural encoders, with strong raw-data
rivals throughout.
