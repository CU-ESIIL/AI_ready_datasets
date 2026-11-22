# Provisional representation utility framework

## Four mechanisms, four different experiments

| Mechanism | Established evidence | What is not established |
| --- | --- | --- |
| Information availability | Deterministic transforms cannot add per-case information to the same raw prefix; completed normalization can discard scale/dates | No claim that compressed coordinates are scientifically sufficient for unrestricted questions |
| Statistical learning | Supervised temporal embedding predicts independent held-out synthetic next-day observations; raw ridge and matched tabular predictor are strong rivals | No unique ecological relationship or learned advantage over every raw-data predictor |
| Computational reuse | Same encoder/head predictions agree after materialization; stored lookup avoids encoder work | No total lifecycle advantage over cached complete predictions or heterogeneous workloads |
| Agent selection | M1–3 deterministic/mock isolation and routing work; recorded requests fit the real adapter | No real-agent competence, metadata effect or learned-representation routing result |

For fixed training information and parameters theta, a deterministic embedding is
`Z = f_theta(X)`. It cannot add information beyond `(X, theta)`. Better prediction by
a restricted head can arise from inductive bias and training information learned in
theta, not additional observations in the test prefix. Compare train-only raw,
interpretable and PCA heads, learned frozen probes and capacity controls separately.
Do not confuse equal embedding dimension with equal statistical training objective:
PCA4 is unsupervised; the learned encoder uses training targets.

All eight methods request the **same next-calendar-day outcome**. Every prediction
is uncertain; none can establish the exact stochastic next day, ecological mechanism
or real operational skill. The raw prefix retains the supplied past information;
PCA/learned summaries are lossy. Calibration intervals are empirical diagnostics,
not expert-approved real-fire uncertainty. No ex ante real accuracy tolerance was
supplied, so report observed error/cost vectors rather than inventing a binary
scientific acceptance threshold after seeing the results.

At query count Q and refresh count R, a provisional cost ledger is

`C = training + source preparation + materialization + Q × query + R × refresh`.

With the encoder already trained, materialization versus repeated encoding has
break-even `Q > P / (c_encoder - c_lookup)` only when the denominator is positive.
This comparison cancels shared training, **not training versus a raw baseline**.
For identical fixed-head queries, cache the whole answer and compare
`c_first + (Q - 1) × c_cache`; storing an intermediate need not win. New heads,
source updates and model refresh change the reuse problem and need new measurements.

The current measurements are local resident CPU/interfaces. They exclude operational
rights/review labor, acquisition, durable storage pricing, monitoring, scientific
validation and empirically measured refresh frequency. The observed three-query
amortization against repeated encoding is scoped to this run, not a universal
boundary. Full-model training cost differs by orders of magnitude from ridge fitting;
include it when comparing different methods from scratch.

A meaningful deployment decision needs independently defined accuracy/uncertainty
requirements, reviewed source support and rights, a workload distribution, actual
refresh/maintenance assumptions and real evidence. Neither a coherent plot nor one
synthetic MSE difference provides those conditions.
