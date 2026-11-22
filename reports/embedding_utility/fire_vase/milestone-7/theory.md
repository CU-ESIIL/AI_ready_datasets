# What would make embeddings worth their cost?

This is an analytical framework, not a result measured on Fire VASE.

## Information cannot increase; practical usefulness can

Let X denote the complete supplied native interface, including provenance and support,
Z=f(X) a deterministic representation, and Y a separately defined scientific target.
For unrestricted predictors under the same distribution, every rule g(Z) can be
implemented as g(f(X)). Thus the best achievable native-input risk cannot exceed the
best achievable representation risk. A representation advantage must arise from
finite samples, restricted model classes, optimization, regularization, access cost
or reusable computation. It does not establish new information in Z.

A sufficient representation satisfies P(Y|X)=P(Y|Z) for the declared target and
population. Sufficiency for one task does not imply sufficiency for another. If
f(x1)=f(x2) but their independently defined target values differ, exact target
recovery is impossible from Z alone. Retained native-ID metadata must be included
when testing such a collision; discarding sidecars would test a different interface.
Floating-point storage and a finite evaluation sample cannot establish universal
sufficiency or an information-theoretic dimension bound.

For squared loss, with square-integrable targets, optimal risks differ by
E[(E[Y|X]-E[Y|Z])^2]. This nonnegative approximation penalty can be offset in finite
training data by a smaller estimation or optimization penalty. That decomposition
motivates learning curves, dimension curves and matched-capacity raw-data rivals.
An observed crossover is conditional on model class, supervision and tuning budget.
It is not a proof that raw-data agents could never implement the same computation.

## Task dependence and negative transfer

A shared encoder must retain task-relevant distinctions across multiple targets.
If one task needs absolute area while another rewards normalized allocation, an
invariance that helps the latter can erase the former. Compare task-specific and
shared objectives using identical training labels where the estimand requires it;
otherwise label-information gains cannot be assigned to architecture. Measure
rare-size and temporal-order failure strata, not only mean prediction loss.
A failed linear probe only rejects that probe family. Nonlinear recovery remains
possible, and strong recovery is not independent ecological validity.

## Economic threshold

For fixed source/model versions and an identical task acceptance requirement, let
F_r,F_z be complete fixed costs and c_r,c_z per-query costs. Embedding materialization
wins only if F_z+Q*c_z < F_r+Q*c_r. If c_r>c_z, the strict break-even condition is
Q>(F_z-F_r)/(c_r-c_z). If c_r<=c_z, increasing query reuse cannot rescue a larger
embedding fixed cost. Source refreshes and model refits add their actual costs.
Optimized raw/answer caches can sharply reduce c_r; heterogeneous tasks may favor
reusable representations while repeated identical answers favor answer caching.
Accuracy and support constraints must be checked before cost dominance is relevant.

## Power is a paired-cluster question

Let d_i be one paired loss difference per independent fire-level evaluation unit,
with variance s_d^2. Under an explicit independent-cluster normal approximation,
a two-sided detectable mean difference scales as
(z_(1-alpha/2)+z_(power))*s_d/sqrt(n).
This is a planning approximation, not an empirical confidence interval or a numerical
power claim. Correlated year/region conditions reduce the effective independent
information; unequal cluster sizes and repeated model fits need an appropriate
resampling/design analysis. We cannot substitute fire-day counts for n or select a
scientifically meaningful difference from held-out outcomes. Profiling and reviewed
thresholds must precede a numerical power calculation.

## Falsifiable outcomes

- Raw models dominate after matched labels, tuning and caching: embeddings add cost
  or bias for that task/workload, even if their geometric plots look attractive.
- PCA matches learned vectors: classical compression may suffice at the measured
  scientific tolerance and training population.
- Learned vectors help only small training cohorts: regularization may explain the
  benefit; do not claim intrinsic information superiority.
- Shared vectors help reuse but harm rare tasks: task-aware routing needs an
  independent validation set and a safe native path.
- Apparent gains vanish under whole-fire or regional holdouts: dependence, source
  shortcuts or population shift are candidate explanations, not encoder utility.
- Scale/support distinctions vanish while mean skill improves: report that scientific
  loss explicitly; aggregate loss is not a universal acceptance rule.
