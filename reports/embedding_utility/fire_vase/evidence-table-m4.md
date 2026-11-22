# Milestone 4 evidence table

Table 1. Descriptive held-out synthetic next-calendar-day prediction. 256 transitions from 64 fires; four dependent prefixes per fire. All methods receive the same observed past. Seeds selected by separate validation fires. No population significance or real-fire claim.

| Method | Log-growth MSE ↓ | MAE (km²/day) ↓ | Empirical 90% coverage | Mean interval width (km²/day) |
| --- | ---: | ---: | ---: | ---: |
| training_mean | 0.311009 | 2.8280 | 92.58% | 13.1297 |
| persistence | 0.093738 | 1.6025 | 85.55% | 5.8879 |
| raw_ridge | 0.060737 | 1.2901 | 92.58% | 5.8497 |
| interpretable_ridge | 0.074885 | 1.4574 | 91.80% | 5.9688 |
| pca4_ridge | 0.155574 | 2.1594 | 91.80% | 8.3921 |
| learned4_ridge | 0.060796 | 1.3241 | 92.58% | 5.6617 |
| tcn_end_to_end | 0.060604 | 1.3178 | 92.58% | 5.6658 |
| mlp_end_to_end | 0.060521 | 1.3305 | 94.14% | 5.9650 |

TCN has 177 parameters; tabular MLP has 168. Learned/PCA representations have four coordinates; raw tensor has 48 and explicit summaries nine. TCN/PCA objectives differ: predictive supervised versus unsupervised variance. The same ridge penalty and independent outcomes apply. All raw inputs precede their target; no completed-history normalization.

Table 2. Local warm scalar compute/reuse accounting. Prevalidated immutable query keys; excludes shared training and unknown maintenance/refresh frequency. Materialized/on-demand learned modes use identical weights and head.

| Path | Median per-query time (µs) | Evidence scope |
| --- | ---: | --- |
| On-demand TCN + frozen ridge | 37.500 | Local timing, 31 repetitions; no independent scientific samples |
| Stored learned vector + same ridge | 3.125 | Local timing, 31 repetitions; no independent scientific samples |
| Raw prefix + ridge | 10.458 | Local timing, 31 repetitions; no independent scientific samples |
| Direct prefix summaries + ridge | 13.125 | Local timing, 31 repetitions; no independent scientific samples |
| Cached complete learned prediction | 0.083 | Local timing, 31 repetitions; no independent scientific samples |
| Cached direct-feature prediction | 0.083 | Local timing, 31 repetitions; no independent scientific samples |

Embedding construction: 18.410 ms for 256 prefixes. JSON storage: 155,425 bytes (numeric coordinates alone 8,192). Write/read: 2.586/2.980 ms. Query identity construction: 21.750 µs, outside steady-state timing. Formula crossover against repeated encoding: 3 identical queries per prefix, not a lifecycle crossover against raw computation.

All three TCN initializations trained in 0.988 s wall; MLP 0.212 s. Raw ridge fit 0.236 ms. Train-only PCA preparation 1.594 ms. These are local scoped costs, not general throughput.

Evidence taxonomy: the tables are SYNTHETIC_OBSERVATION results, arithmetic identities are MATHEMATICAL, Track A is PENDING_REAL_MODEL, real-fire prediction is PENDING_RIGHTS_SUPPORT_AVAILABILITY, and operational lifecycle maintenance is UNMEASURED.

Sources: [frozen manifest](results/milestone-4-learning-v1/manifest.json), [evaluation](results/milestone-4-learning-v1/evaluation.json), [materialization](results/milestone-4-learning-v1/materialization.json), [protocol](learned-protocol-m4-v1.md).
