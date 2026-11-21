# Fire VASE deterministic synthetic benchmark

Synthetic mechanics only. No agent calls, observed wildfire findings, independent scientific analog labels or metadata-effect estimates.

| Representation | Answerable correct / attempts | Correct abstentions | Cold query median (µs) | Warm query median (µs) |
| --- | --- | --- | --- | --- |
| R0 | 414 / 414 | 108 | 37.50 | 16.04 |
| R1 | 198 / 198 | 324 | 66.00 | 16.00 |
| R2 | 36 / 54 | 468 | 32.75 | 15.96 |

Counts include metadata/cache/repeat cells, not independent scientific samples. All-task coverage and accuracy conditional on answerability must be read separately.

Metadata answer invariance: True. Views are recorded, not interpreted by this deterministic consumer.

Cold means application query-cache cold; materialized R1/R2 artifacts are resident. OS caches are uncontrolled. Warm prefill costs are retained in preparation.json. Timings include Python instrumentation and worker IPC when used.

Preparation (not free or folded silently into per-query latency):

| Phase | Wall time (ms) |
| --- | --- |
| load_observations | 2.144 |
| metadata_views | 8.852 |
| independent_reference_preparation | 29.306 |
| worker_startup_and_import | 1118.453 |
| compute_vase_features | 11.213 |
| fit_training_only_pca | 4.621 |
| write_pca_artifact | 0.752 |
| load_pca_artifact | 4.411 |
| compute_pca_coordinates | 0.221 |
| publish_feature_artifact | 2.333 |
| publish_coordinate_artifact | 0.680 |
| load_existing_pca_coordinates | 3.179 |

Example of matched correct queries: first-half allocation fraction. R0 on-demand feature calls include worker IPC; R1 resident lookup does not, so the difference is not pure algorithm time.

| Interface | Cold median (µs) | Warm median (µs) |
| --- | --- | --- |
| R0 | 351.92 | 15.54 |
| R1 | 67.54 | 16.54 |

No universal cost winner or empirical break-even is claimed: supported tasks differ and this tiny local run includes preparation shared by several interfaces. Compare measured task-specific cumulative costs at equal correctness, including warmup, artifact refresh and direct caching.

Direct data retain area/date information; normalized profiles intentionally discard those values; truncated PCA cannot exactly invert the profile. Exact compressed-only queries abstain. Neighbor outputs are explicitly approximate geometric diagnostics. Scientific analog evidence remains pending.

Real-data contract validation remains pending selected-input rights/support and availability review. No archive was downloaded or ingested. Numerical outputs/config/artifact identities reproduce; runtime/memory and serialized output hashes vary by environment.
