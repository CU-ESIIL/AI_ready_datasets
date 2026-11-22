# Milestone 4 — frozen synthetic learning protocol

21 November 2026. This protocol and configuration precede the retained run. Real
agent inference and real-fire learning are separate pending evidence tracks.

## Track A

Preserve M2/M3 protocols and existing smoke/pilot configurations. Read-only access
check: saved isolated OpenClaw 2026.5.18 policy valid; gateway connection denied from
this session (PermissionError); access/no-charge authorization unverified. No service,
Docker, Slack or credential change. No inference attempted. Serialization preflight
of 6,480 recorded M3 requests finds largest payload 37,810 bytes, below 48,000. The
adapter can transport those recorded requests without modification; this does not
verify live service identity, future recovery histories or model performance. Usage
and provider cost remain unknown with the installed plugin. Real smoke/pilot pending.

## Objective and real-data boundary

Select next-calendar-day observed growth prediction from dated prefixes. Of the
three proposed objectives, it needs neither fabricated analog labels nor new spatial
semantics. The primary supervised objective is subsequent log(1 + km2/day) growth,
not input reconstruction or PCA mimicry. Real source observation availability is
unresolved, so only synthetic scientific controls are executed. Synthetic future
observations are independent held-out *observations under a declared generator*,
not independent ecological evidence or physical fire mechanisms.

Real FIRED GeoPackages and lakehouse Parquet files exist in documented legacy
CubeDynamics roots. Footers/schema catalogs were inspected without feature rows.
Experiment-specific rights/attribution, ring-versus-cumulative support mapping,
source identity/checksum verification and operational availability require review.
No real source row is ingested or training sample silently substituted.

## Cohort, support and split

Configuration: `config/learned-synthetic-m4-v1.json`. Generator seed 20261121.
128 train / 48 validation / 64 test synthetic fires; 14 observed days each; prefixes
at 3, 5, 7 and 10 observations. All prefixes of a fire stay in one split. Train,
validation and test have separate synthetic years. Region A/B are generator labels,
not real spatial units or environmental transfer. Same generator across splits;
this is not a stress test of geographic/climate distribution shift.

Source-native synthetic daily increments, dates, observation IDs and availability
are explicit. Each day is available at the next midnight; forecast issue follows the
last observed day and precedes the target observation's availability. Targets are
exactly the next calendar day's canonical synthetic observation, cross-checked
against the separately retained history. Gaps, invalid availability, duplicate IDs
or negative/nonfinite growth fail closed. No missing-as-zero imputation.

Encoder receives only an observed prefix: last 12 slots (all selected depths fit),
left padding, log observed growth, log observed cumulative sum, mask, log prefix
length. Normalize continuous inputs on train valid observations only. No final fire
size, duration, full-history VASE normalization, future geometry/weather or IDs as
predictive inputs. Prefix descriptors are a new synthetic-only recipe, not an
approved prospective use of completed-history Fire VASE features.

## Methods and learning

Eight methods on identical past observations and identical future outcomes:

- Training-mean and persistence predictions.
- Ridge on the full raw prefix tensor (48 coordinates).
- Ridge on nine explicit observed-prefix summaries: last/mean/std log growth,
  log observed total, last log-growth difference, zero fraction, log prefix length,
  log first-half observed mass, mean last-three log growth.
- Training-only four-PC projection and ridge, dimension matched to learned embedding.
- Four-dimensional supervised temporal embedding with a train-only ridge probe.
- End-to-end temporal network, exposing the effect of its nonlinear prediction head.
- Conventional tabular MLP on the same flattened raw tensor, with similar parameter
  count, exposing the role of capacity versus temporal inductive structure.

TCN: static causal kernel3 Conv1D, 4 input to 8 hidden channels, tanh, masked mean
plus final state, tanh embedding4, linear head. 177 parameters. MLP: 48→3→4→1,
tanh hidden layers, 168 parameters (capacity approximate, not an exact architecture
match). No foundation-model dependency. NumPy backprop gradients are independently
finite-difference tested.

Training seeds 271/811/1729, 120 epochs, batch64, Adam lr .01, betas .9/.999,
epsilon 1e-8, global norm clip5, L2 1e-4. Standardize target on train only; fixed
ridge penalty1. Each architecture chooses a seed by validation-selection MSE,
never test outcomes. Split validation **by fire** into 24 seed-selection and 24
calibration fires. Calibration uses only the latter residuals for descriptive 90%
absolute-error intervals in log space. Synthetic shift/grouping means no claim of
general ecological coverage; repeated prefixes are dependent.

Save every checkpoint, parameter count, loss history, runtime, training CPU/wall,
input/preprocessing/checkpoint identities and selected seed. No hyperparameter or
architecture edits after retained test outcomes; subsequent changes need new version
and clearly labeled exploratory status.

## Evaluation and controls

Report log-space MSE, original-unit MAE, interval coverage/width and observation-depth
strata; show synthetic group labels separately without real-transfer claims. Report
all seed metrics descriptively; no independent-fire count from repeated initializations,
no population p-values, no cherry-picked best test seed.

Mathematical controls: temporal permutation and equal-total reversal need not preserve
an absolute next-day prediction; report sensitivity, not forced success. Uniform
scaling is also not irrelevant to absolute growth and is not required invariant.
Nominal-ID renaming must give identical embedding. Observation removal and changed
calendar resolution fail daily-support contracts instead of claiming interpolation
robustness. Spatial geometry is unavailable in this approved cohort; no invented
spatial control. Raw-vs-embedding neighborhood overlap is a fidelity diagnostic, not
ecological relevance. Input reconstruction is not the training objective and its
unmeasured error stays not applicable.

## Materialization and lifecycle

Use the same trained TCN and same frozen ridge head for on-demand and stored modes.
Record generation/write/read bytes/times, scalar warm encoder+head, stored vector+
head, direct prefix features+head, raw+head, cached whole-model predictions and cached
direct-feature predictions. Use immutable validated query identities consistently;
identity preparation is separate. Assert prediction equality after materialization.

At Q identical queries, illustrative accounting is `P + Q c_lookup` versus
`Q c_encoder`; break-even exists only when `c_encoder > c_lookup`. Include measured
per-prefix construction and allocated file write/read. Cached final predictions are
a stronger rival for identical fixed-head queries. Different future heads may reuse
embeddings but require a separate experiment. Changed source/prefix, recipe,
preprocessing, encoder or probe invalidates relevant caches. Training/refresh costs
are measured or stated, never assumed free; storage service fees, operational
refresh frequency, validation labor and maintenance remain unmeasured. No universal
break-even or lifecycle boundary follows from this small synthetic run.
