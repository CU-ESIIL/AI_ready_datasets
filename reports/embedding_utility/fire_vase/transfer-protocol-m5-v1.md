# Milestone 5 frozen transfer protocol

21 November 2026. Freeze before retained B–E evaluation. **Synthetic only. No real
fire, ecological analog or real-agent evidence.** Preserve M1–4 and upstream unchanged.

## Audit and source boundary

M4 raw prefix tensor retains supplied observed increments (log/cumulative/mask/depth),
not future observations. Its four-dimensional supervised encoder uses A-only training
labels. The training head predicts next day; a newly fitted linear head may recover
other properties, but this neither proves exact preservation nor scientific generality.
M4 geometric sensitivities and approximate prediction do not identify everything
lost. A failed linear probe cannot prove information absence.

Reuse the exact M4 source cohort, train-only preprocessing/PCA and selected A-only
TCN checkpoint. Verify every retained artifact hash, regenerated canonical source
digest, preprocessing and parameter digest before running. Source model bytes remain
unchanged; no refitting of the original A representation. The cohort has 128 train,
48 validation and 64 test fires, four prefixes (3/5/7/10) each. **A performance was
already observed in M4; this is a new task protocol, not a new blinded cohort.**
B–E results were not used to choose the protocol. All prefixes of a fire stay together.
Use existing 24 validation-selection / 24 calibration fires separately. Test labels
never fit encoders/heads/PCA, select seeds or normalize future relevance.

## Targets independently defined from canonical future observations

Future horizon: exactly three calendar days after the observed prefix, within the
frozen 14-day history. Unavailable support fails, never imputes future values.

| Task | Definition | Primary metric |
| --- | --- | --- |
| A | Next daily increment, log(1+km2/day) | MSE |
| B | Sum of next three increments, log(1+km2) | MSE |
| C | Mean of next three exceeds mean of last three observed increments, strictly; equality false | Brier score; log loss/accuracy/reliability secondary |
| D | Population standard deviation (ddof=0) of next three increments, log(1+km2/day) | MSE |
| E | Similarity of next-three log-increment vectors, standardized on training outcomes | Precision/recall@10 and distance-rank Spearman |

B–D are verified against separate Fraction/pairwise identities. Targets are independently
specified, **not statistically independent**: they share three future observations.
C is a relative future/past mean comparison, not a physical second derivative or a
threshold tuned on test outcomes. E relevance is top-ten nearest full future vectors,
not ecological analog relevance. All same-fire prefixes are excluded from gallery.

## Strategies and supervision

1. Raw-prefix ridge (A/B/D) or regularized logistic (C).
2. Nine explicit observed-prefix summaries with the same heads.
3. Frozen train-only PCA4 and heads.
4. **Frozen A-only encoder** and new task heads; B–E measure downstream transfer.
5. **Shared A–D TCN**, trained jointly, then frozen with independent per-task heads.
6. **Task-specific TCNs** for B/C/D and E's future-vector target; reuse A's original
   encoder for aligned A. Keep all cross-specific heads available rather than selecting
   favorable task/encoder combinations after outcomes.
7. Similar-capacity direct per-task MLP predictors. Also train shared A–D MLP as a
   supervision/capacity control and report shared TCN training-head predictions separately.

Primary representations all have four coordinates except raw48 and summaries9.
Original trunk172 parameters + one task head5 =177; shared four-head TCN192;
future-vector TCN187. Tabular MLP trunk163 + one head5 =168, four-head183,
three-output178. Independent lightweight heads add deployment parameters and training.
No claim of exactly matched architectures. Multitask/E-specific encoders receive
additional training objectives; their gains are **not** A-only frozen transfer.
PCA is unsupervised; frozen A already uses training labels.

Fixed seeds 271/811/1729, 120 epochs, batch64, Adam .01/.9/.999/1e-8, global norm clip5,
weight L2 1e-4. Train-only per-target standardization for regression; C binary
cross-entropy logits are unstandardized. Shared objective is equal mean per-head
MSE/BCE. Selection uses the matching mean normalized validation loss on selection
fires only. Regularized downstream heads use penalty1; no test tuning.
Save every seed's checkpoint, loss curve, parameter count, timing and validation score.

## Independent evaluation

Use identical held-out prefixes/outcomes for every method. Regressions: log MSE,
original-unit MAE, 90% calibration-residual intervals. C: Brier, log loss, fixed .5
accuracy, ten fixed-bin reliability/ECE. Report depth and generator stratum (original
source index modulo3) without ecological transfer claims. No calibration guarantee
for dependent prefixes or real fires.

Primary comparisons: frozen A versus raw on B/C/D; shared versus frozen A and aligned
specific models on all A–D. Publish full matrix, not only winning tasks. Average
paired loss differences within each fire, then resample the 64 empirical test fires
1,000 times (seed880031) for descriptive 95% intervals conditional on selected fitted
models. Do not use prefixes or initializations as independent fires, refit-free
intervals as training uncertainty, or intervals as wildfire population significance.
No multiplicity-adjusted confirmatory inference is claimed.

## Retrieval and information probes

For each raw/summary/PCA/frozen/shared/specific view: train-only standardized
representation distance without E supervision, and a separate explicitly E-supervised
three-output lightweight head. Compare relevance against training-standardized
held-out future vectors. Direct E MLP is an additional supervised control. Candidate
and relevant sets each contain ten: precision@10 equals recall@10 by construction.
Resolve exact ties by frozen row order; Spearman uses averaged tied ranks. Report
fire-averaged metrics, paired descriptive retrieval intervals and chance k/gallery.
Held-out future labels are grader-only; no gallery fitting or same-fire retrieval.

Probes target observed total scale, temporal mass centroid, recent rate, recent
acceleration, strict interior-local-maximum count (not upstream prominence), and
observed variability. Compare train-only linear regression and fixed RBF kernel
ridge (bandwidth dimension, penalty1, all training samples) to expose nonlinear
recoverability with greater probe capacity. These are **input-property diagnostics**,
not independent future science. Completeness is constant true among validated daily
prefixes; invalid schedules fail contracts, not a fabricated competence score.
Raw input is mathematically invertible for the supplied growth/mask under floating
precision; no other method is awarded exactness from a successful learned probe.

## Perturbations and reuse economics

Apply permutation (seed451), fourfold scale, equal-total reversal and nominal-ID
rename across all held-out prefixes/views/task heads. Do not require scale/order
invariance universally: absolute A/B/D outcomes scale under jointly scaled observed
and future increments; C's relative criterion is invariant to joint positive scale.
Prefix-only perturbations with unchanged future labels are sensitivity tests, not
observed ecological counterfactuals. Observation removal and changed temporal
resolution fail support contracts; no missingness-accuracy claim. E ranking changes
are diagnostic; no universal scale/order relevance invariance. Spatial evidence absent.

Measure heterogeneous bundles of the first K distinct heads, K=1,2,3,4. Shared
representations encode once per prefix/bundle; separate encoders run per task. Compare
raw/summary/PCA/frozen/shared/specific preparation, scalar inference, training, vector
construction, file read/write and cached full bundles. Materialized and on-demand
modes use **identical models/heads** and must agree. Record coordinate/file bytes;
full lineage/service storage is outside those byte counts.

For N bundles with K task heads, `C = train + prepare + N × (encode + heads_K)` or
`train + materialize + N × heads_K`. Break-even against repeated encoding requires
positive savings. Different representations' training cannot be canceled. Identical
bundle caching is a separate stronger rival; unseen/new heads are heterogeneous
workloads and need their own training. Record current and historical A acquisition
cost separately. Source/recipe/preprocessing/encoder changes invalidate affected
vectors/predictions; changed heads invalidate predictions. Refresh frequency and
maintenance labor remain unknown. No universal cost or task-necessity claim.

## Interpretation boundary

No real-fire scientific accuracy threshold is supplied. Publish paired task loss,
calibration and scoped cost vectors, not a post hoc acceptance threshold or universal
phase boundary. Reuse may improve CPU work without predictive gain; statistical
learning may improve a restricted head without adding per-case information. Preserve
development failures in a ledger; no task deletion or protocol edits after retained
outcomes to manufacture an embedding win.
