# Manuscript results

## Primary finding

For supported mathematical properties of the declared scientific state, learned
representations did not improve over independently validated cached native
operations. Native scalar answers were exact under the retained recipe, and
native property ranking achieved precision@10 of 1.0. Learned coordinates and
trained decoders introduced approximation. In the measured heterogeneous scalar
query bundle, an adaptive exact-native route dominated learned alternatives on
component-sum cost and error at every declared reuse count (Figure13; serving
kernels are separately shown in Figure9). Crosses in Figure13 denote cost/error-dominated methods under these components;
vector storage is a separate tradeoff axis. Near-identical native
cache routes differ at timer-noise scale; those differences do not establish a
production systems advantage.

This is a result about encoding an explicitly constructed scientific state.
It does not establish that raw sequences, imagery or arbitrary environmental
questions never benefit from representation learning.

## Population and information preservation

Short observed histories dominate: one observation comprises 57.81%, two 17.21%,
and three or more 24.98%. All native IDs enter supported primary tasks. SD and
allocation are undefined for 161,200 one-point histories; change is undefined
for 202,912 fires and extrema for 243,954. They were not scored as zeros.

The training-state numerical covariance rank is 13 globally, with ranks 1, 8 and
12 in one-, two- and longer-history strata. The two-point rank reflects nonlinear
engineered features, date gaps and masks, not eight independent observations.
PCA effective dimensions are 4/8/13/13/13. Full-rank inverse gives a numerical
state roundtrip without downstream labels; it does not restore upstream-discarded
dates or longer sequence order and is not a source-bit preservation claim.

| Full-training linear recovery | Observed-total standardized MSE |
|---|---:|
| Same-label raw-state ridge | 1.492e-9 |
| PCA, requested16/effective13 | 2.671e-11 |
| Count-supervised16 | 0.12401 |
| Self-supervised16 | 0.004427 |
| Multitask16 | 0.0003363 |

These are approximate trained-head errors on all 41,991 test fires, not exact
preservation. The count-only encoder retains area information it was not trained
to predict, but much less accurately than the raw-state control. Original-unit
MAE/RMSE, nonnegative-property violations, per-stratum performance, all dimensions,
all fractions and nonlinear probes are retained in the result tables. Predictions
are not clipped to manufacture physically plausible reconstruction.

Actual normalized positive one-point allocations collapse all 161,200 histories
to [1]. Among 47,992 two-point histories, only 414 distinct float64 allocation
payloads occur; 67 payload groups with different totals encompass 45,963 fires.
The learned scientific-state encoders preserve approximate scale because their
input includes scale. They do not recover scale from an information-destroying
normalized input. A controlled fixed-date reversal of all 47,992 two-point histories verifies that
total/count/SD/span are invariant while first/last/allocation change and
consecutive change reverses sign where supported. There are 23,679 unequal
increment pairs and 17,263 consecutive pairs. This is recipe order sensitivity,
not learned encoder equivariance. A retained ID can still support a separately charged native
lookup. Raw first/last/total fields reconstruct short cumulative sequences;
general longer cumulative paths are not uniquely determined by this state.

## Retrieval and access

Population-weighted total-area precision@10 is 1.000 for cached native ranking.
PCA13 coordinates give 0.8574 despite near-complete state recoverability; its
trained linear head gives 1.000. Coordinate/linear-head precision is respectively
0.8374/0.8260 for count-supervised16, 0.8539/0.8664 for self-supervised16 and
0.8982/0.9471 for multitask16. Nonlinear-head precision is 0.8284, 0.8839 and
0.9509 respectively. Thus information retention, Euclidean geometry and decoder
quality are different outcomes. All five task rubrics and length strata are
reported, with full galleries and separate rank-diagnostic scope.

B metadata restores original date/support information through explicit sidecar
operations and strengthens some trained heads. This is observed-support evidence,
not a test of semantic metadata efficacy or agent reasoning. C independently read
94,493 native rows for all 41,991 test fires and reproduced their defined state
numerically, returning 3,888,100 SQL-response bytes. Response bytes are not physical
disk bytes. C recovery belongs to the native source, not to the embedding.

## Transfer and uncertainty

Transfer depends on objective and target: count-supervised states retain some
area/shape information, and autoencoding improves many approximate recovery
errors, while multitask specialization can damage untrained properties. Larger
coordinates or more training cases do not imply uniform monotonic improvement.
Fixed16 temporal and west-region encoder refits, same-label raw heads and direct
all-target neural controls are in `blocked-generalization.csv`. Random-split
region/year stratification is separately retained.

All 50 Holm-adjusted coarse-region sign-flip p-values equal 1.0. These comparisons
do not establish confirmatory superiority or equivalence. Conditional paired
fire intervals can be much narrower than region sensitivities; they omit
training-seed variation and do not certify ecological generalization.

## Cost and secondary prediction

Native feature construction decoded all 627,033 rows in 7.601 seconds on this
machine. The exact cached-native 4,096-fire batch kernel took about 0.034 ms;
this is vectorized warm arithmetic, not per-request latency. Learned fitting,
encoding and serving added cost and nonzero error for this workload. Lower-width
float32 vectors trade accuracy for numeric-vector storage, but all methods retain
source/lineage. Bare native area numbers occupy 5,016,264 bytes globally; even
short raw histories can be cheaper than dense feature caches. No claim of unique
learned compression or total-lake storage reduction follows. Peak primary
training/probe process RSS was approximately 2.58 GB. Physical disk I/O and true
source-update costs were not measured.

The depth1/next-day extension evaluates 11,539 test fires. Fire-mean log1p-growth
MSE is 0.23798 for persistence, 0.18553 for raw linear, 0.18596 for raw nonlinear,
0.18204 for frozen self-supervised16 with a linear head, and 0.18253 for the
direct raw-state neural control. The self-supervised effect relative to raw linear
is -0.003491 (conditional paired fire-bootstrap interval approximately
[-0.004557, -0.002587]), about 1.9% lower error. Count-supervised and multitask16
are similar. This is a small task-specific predictive regularization/feature-map
benefit, with additional training-history pretraining information and single-seed
uncertainty; it is not newly created scientific information or operational skill.
All six depth/horizon cohorts and dimensions are retained, rather than selecting
the most favorable task.

## Decision boundary

For queries already exposed as cheap validated native operations, use those
operations and cache their interpretable answers. A learned representation is a
candidate when approximate loss is acceptable and a distinct downstream task
benefits from the learned feature map enough to pay fitting, serving, validation
and refresh costs. This run provides limited secondary predictive evidence for
that possibility, and no primary scalar-query economic advantage. Novel sequence,
geometry and external-label tasks remain necessary tests of broader utility.
