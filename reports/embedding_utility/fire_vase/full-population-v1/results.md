# Full-population benchmark: first real diagnostics

The primary population is now **all278,865 native fire IDs**, not fires passing a
long-history filter. Primary tasks concern observed properties, original support,
retrieval and access/reuse. Prediction is a separately reported selected-cohort
extension. No learned/PCA/predictive models or agents were fitted/evaluated here.

| Primary stratum | Fire IDs | Population weight |
| --- | ---: | ---: |
| One observation | 161,200 | 57.81% |
| Two observations | 47,992 | 17.21% |
| Three or more | 69,673 | 24.98% |

**75.02% have one/two observations.** Short histories remain central. Gappy pairs
are retained for supported observed-property tasks:17,263 consecutive and30,729
gappy two-observation histories. Physical lifetime/extinction and missing-day growth
are not inferred from these records.

## Information preservation and access

All209,192 short histories passed exact native-value and original date/source-ref
preservation through the minimal short scientific state. The audit decoded all
627,033 native daily records and reconciled stratum counts with the prior census.
For every one-observation fire, positive normalized allocation was[1], despite
substantial absolute-area variation. Two-observation normalization also removes
scale from the payload. All representations retain the same provenance/date
sidecar; source fallback can recover native information and is explicitly charged.
128 indexed-source checks recovered values exactly. Their warm-file timing is a
small fixed-sample diagnostic, not representative workload performance.

Explicit redundant summaries increased JSON size in this encoding; neither that
result nor numerical payload-size arithmetic is an inherent encoding lower bound
or proof of learned-model inefficiency. Matched precision and complete preparation,
index, serving and refresh costs remain necessary comparisons.

## Observable-property retrieval

An optimized cached-native observed-area baseline searched194,980 candidate training
fires for48 disjoint test queries,16 from each history-length stratum. All48 matched
an independently implemented scalar-ranking oracle. This validates exact retrieval
for the declared observed-total-area metric. It does not validate ecological analogs,
learned representations or out-of-sample prediction. Query receipts are retained.
The earlier short-only development diagnostic is separately preserved.

## Short-prefix prediction extension

| Input depth | Future horizon | Eligible fires | Dependent windows |
| --- | --- | ---: | ---: |
| 1 | 1 | 75,953 | 196,982 |
| 1 | 3 | 19,004 | 61,342 |
| 1 | 7 | 3,386 | 16,547 |
| 2 | 1 | 34,911 | 101,035 |
| 2 | 3 | 11,195 | 40,724 |
| 2 | 7 | 2,452 | 13,072 |

Counts are independently checked against per-fire/run aggregates and enumerated
legal cutoffs. Depth1/horizon1 matches the native exact-day transition count.
A short prefix with observed future support is different from a completed
one-observation record. No unobserved future was labeled zero. No model skill or
empirical predictive power was estimated.

## Validation and remaining work

Full suite: **397 passed, 2 skipped**; strict MkDocs build passed. Eight new unit
checks cover short-state values/support, normalization collisions, zero/undefined
shape and invalid/duplicate rejection. The initial suite had one existing pinned-
worker startup timeout; the unchanged worker test passed individually and the full
rerun passed. Both logs are retained. Previous census and frozen results remain
unchanged, as does upstream Fire VASE.

Learned/classical representation comparisons, independent ecological relevance,
comparative retrieval scores and representative full-workload cost frontiers remain
unexecuted. The current evidence establishes strong compact-native baselines and
specific normalized-payload limitations; it does not establish a universal embedding
verdict. See [current protocol](protocol.md) and the machine-readable task manifest.
