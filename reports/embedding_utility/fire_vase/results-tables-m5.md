# Milestone 5 manuscript results tables

Synthetic convenience cohort; 256 held-out prefixes / 64 fires. B–E independently defined but correlated; A already observed in M4. All per-fire intervals are descriptive, conditional on fitted models, not wildfire population inference.

| Strategy | A log MSE ↓ | B log MSE ↓ | C Brier ↓ | D log MSE ↓ |
| --- | ---: | ---: | ---: | ---: |
| raw | 0.060737 | 0.114779 | 0.160051 | 0.124811 |
| interpretable | 0.074885 | 0.125463 | 0.162906 | 0.132788 |
| PCA4 | 0.155574 | 0.186318 | 0.207585 | 0.135305 |
| frozen_A | 0.060796 | 0.118626 | 0.204011 | 0.136228 |
| shared_AD | 0.072711 | 0.122286 | 0.155780 | 0.129519 |
| task_specific | 0.060796 | 0.118836 | 0.169666 | 0.147380 |
| direct_MLP | 0.061918 | 0.129121 | 0.166828 | 0.131453 |
| shared_AD_end_to_end | 0.073206 | 0.123191 | 0.155117 | 0.132185 |
| shared_mlp_end_to_end | 0.071768 | 0.140834 | 0.160699 | 0.128712 |

Frozen A uses the exact M4 checkpoint. Shared AD is jointly supervised on all four tasks, so its gains are not A-only transfer. Aligned specific uses the A checkpoint for A and separately trained B/C/D encoders. Direct/shared MLPs are capacity/supervision controls.

| Task | Strategy | Raw minus method paired loss | Descriptive 95% fire interval |
| --- | --- | ---: | --- |
| B | frozen_A | -0.003847 | [-0.013570, 0.006452] |
| B | shared_AD | -0.007508 | [-0.017083, 0.003293] |
| B | task_specific | -0.004057 | [-0.014547, 0.007868] |
| B | direct_MLP | -0.014342 | [-0.026846, -0.002249] |
| C | frozen_A | -0.043960 | [-0.064448, -0.023051] |
| C | shared_AD | 0.004271 | [-0.014352, 0.023531] |
| C | task_specific | -0.009615 | [-0.028945, 0.008726] |
| C | direct_MLP | -0.006776 | [-0.019343, 0.005651] |
| D | frozen_A | -0.011417 | [-0.028284, 0.006323] |
| D | shared_AD | -0.004709 | [-0.018611, 0.007838] |
| D | task_specific | -0.022569 | [-0.040656, -0.004487] |
| D | direct_MLP | -0.006642 | [-0.019729, 0.005667] |

Positive raw-minus-method values favor the method on the corresponding predeclared task loss. No task selection, population p-values or multiplicity-adjusted confirmatory claim. Regression intervals and C reliability/calibration/depth/stratum results remain in full evaluation JSON.

| View | Direct representation P@10 ↑ | E-supervised head P@10 ↑ | Direct rank correlation |
| --- | ---: | ---: | ---: |
| raw | 0.0832 | 0.1273 | 0.1766 |
| interpretable | 0.0965 | 0.1156 | 0.3378 |
| PCA4 | 0.0703 | 0.0766 | 0.2065 |
| frozen_A | 0.1023 | 0.1125 | 0.4241 |
| shared_AD | 0.1082 | 0.1070 | 0.3343 |
| specific_B | 0.0953 | 0.1012 | 0.3538 |
| specific_C | 0.0602 | 0.0695 | 0.0477 |
| specific_D | 0.0641 | 0.0668 | 0.1842 |
| specific_E | 0.1082 | 0.1160 | 0.5070 |

Direct E MLP supervised-output P@10: 0.1336. Chance reference k/gallery: 0.0397.
Relevance is held-out future-pattern geometry, not ecology. Same-fire candidates excluded. Precision equals recall because both selected/relevant sets have k=10. E-supervised heads use extra training labels and are not zero-shot distances.

| View | Training (all current seeds, s) | AD bundle on demand (µs) | AD heads on stored vector (µs) | Vector file bytes |
| --- | ---: | ---: | ---: | ---: |
| raw | head fits separate | 18.125 | 9.708 | 98572 |
| interpretable | head fits separate | 20.458 | 9.541 | 18700 |
| PCA4 | head fits separate | 19.458 | 9.708 | 8460 |
| frozen_A | historical 0.988 | 45.500 | 10.541 | 8460 |
| shared_AD | 0.978 | 45.875 | 9.791 | 8460 |

Separate task-specific AD encoder bundle: 144.708 µs. Current network training all strategies: 6.159 s. All training/head fit costs and materialization break-even bundles are recorded separately.
File sizes exclude common lineage/checkpoints; not complete-interface storage. Raw/summary/PCA head fitting and original PCA construction are separate baselines. Cached complete bundles are stronger rivals for identical requests. Refresh/maintenance frequency and labor remain unmeasured.
