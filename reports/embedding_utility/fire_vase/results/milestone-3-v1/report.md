# Milestone 3 expanded synthetic run

**MOCKED agent evidence; WORKING deterministic benchmark. Real-model evidence pending.**

120 questions across 24 templates; no power calculation or ecological validation.

| Provider / view / metadata | Correct | Appropriate abstention | Incorrect abstention | Incorrect answer | Failure |
| --- | ---: | ---: | ---: | ---: | ---: |
| mock/R0/M0 | 206 | 34 | 0 | 0 | 0 |
| mock/R0/M1 | 206 | 34 | 0 | 0 | 0 |
| mock/R0/M2 | 206 | 34 | 0 | 0 | 0 |
| mock/R1/M0 | 174 | 66 | 0 | 0 | 0 |
| mock/R1/M1 | 174 | 66 | 0 | 0 | 0 |
| mock/R1/M2 | 174 | 66 | 0 | 0 | 0 |
| mock/R2/M0 | 102 | 138 | 0 | 0 | 0 |
| mock/R2/M1 | 102 | 138 | 0 | 0 | 0 |
| mock/R2/M2 | 102 | 138 | 0 | 0 | 0 |
| mock/adaptive/M0 | 206 | 34 | 0 | 0 | 0 |
| mock/adaptive/M1 | 206 | 34 | 0 | 0 | 0 |
| mock/adaptive/M2 | 206 | 34 | 0 | 0 | 0 |
| rule/adaptive/M0 | 103 | 17 | 0 | 0 | 0 |
| rule/adaptive/M1 | 103 | 17 | 0 | 0 | 0 |
| rule/adaptive/M2 | 103 | 17 | 0 | 0 | 0 |

## Optimized direct rivals

Timings are median local resident-interface nanoseconds, include Python validation/cache key and worker IPC where used. Warm is exact-query cache. R0 scalar allocation uses a targeted integral, not all upstream traits.

| Operation | R0 cold / warm | R1 cold / warm | R2 cold / warm |
| --- | ---: | ---: | ---: |
| assess_claim | 7083 / 6334 | 7042 / 6333 | 7041 / 6292 |
| cumulative | 7084 / 6333 | unavailable | unavailable |
| daily_growth | 8146 / 6459 | unavailable | unavailable |
| front_fraction | 18854 / 6312 | 6688 / 6125 | unavailable |
| growth_compare | 8083 / 6834 | unavailable | unavailable |
| interval_growth | 7375 / 6500 | unavailable | unavailable |
| late_fraction | 18542 / 6416 | 6750 / 6125 | unavailable |
| neighbor_stability | 2952146 / 11625 | 66458 / 8500 | unavailable |
| pca_distance | 501500 / 8812 | 18396 / 7458 | 9375 / 6980 |
| profile | 266188 / 7770 | 8188 / 6625 | unavailable |
| profile_distance | 496062 / 8312 | 10208 / 7062 | unavailable |
| projected_distance | 512980 / 8292 | 25062 / 7354 | 16500 / 7104 |
| pulse_count | 71667 / 7250 | 6938 / 6250 | unavailable |
| reconstruction_error | 506104 / 8230 | 17562 / 6917 | unavailable |
| source_evidence | 6959 / 6250 | 6959 / 6209 | 6958 / 6208 |

Scientific correctness, receipt provenance, first-operation/argument selection, temporal/normalization/compression errors, sufficiency, routing, usage and task-specific valid-cost frontier are separate episode fields. Unknown usage/cost remains null.

The rule router uses public goal phrases and general operation preconditions plus measured timing inputs, never reference answers or task IDs. Its construction labor is unmeasured. Mock/rule results establish protocol behavior only. Cost calibration is visible in every metadata arm and carries no values, success flags or ideal-view labels.

Counterfactual costs include amortization of measured preparation and routing for repeated identical queries. Cached R0 is a strong rival. No universal speedup or adaptive advantage is assumed. Full traces retain failures, malformed responses and recovery. Synthetic semantic rubrics remain draft evidence-scope checks, not expert gold.
