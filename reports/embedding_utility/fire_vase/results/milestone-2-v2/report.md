# Fire VASE controlled-agent milestone 2

Complete mock-provider protocol matrix; **no real-model evidence**.

The deterministic simulator ignores metadata and selects operations using public question phrases. Its scores test dispatch and grading, not language-model reasoning. Fixed and adaptive access are separate regimes. Questions are public synthetic development diagnostics, not a hidden generalization benchmark.

## Scientific correctness and abstention

| Condition | Metadata | Episodes | Correct answers | Correct abstentions | Incorrect | Failures |
| --- | --- | --- | --- | --- | --- | --- |
| adaptive | M0 | 87 | 69 | 18 | 0 | 0 |
| adaptive | M1 | 87 | 69 | 18 | 0 | 0 |
| adaptive | M2 | 87 | 69 | 18 | 0 | 0 |
| fixed_R0 | M0 | 87 | 69 | 18 | 0 | 0 |
| fixed_R0 | M1 | 87 | 69 | 18 | 0 | 0 |
| fixed_R0 | M2 | 87 | 69 | 18 | 0 | 0 |
| fixed_R1 | M0 | 87 | 33 | 54 | 0 | 0 |
| fixed_R1 | M1 | 87 | 33 | 54 | 0 | 0 |
| fixed_R1 | M2 | 87 | 33 | 54 | 0 | 0 |
| fixed_R2 | M0 | 87 | 6 | 78 | 3 | 0 |
| fixed_R2 | M1 | 87 | 6 | 78 | 3 | 0 |
| fixed_R2 | M2 | 87 | 6 | 78 | 3 | 0 |

## Selection errors and computational accounting

| Condition | Metadata | Wrong first operation selections | Insufficient selected view | Tool calls | Invalid calls | Input/output tokens |
| --- | --- | --- | --- | --- | --- | --- |
| adaptive | M0 | 0 | 18 | 87 | 0 | not applicable (mock) |
| adaptive | M1 | 0 | 18 | 87 | 0 | not applicable (mock) |
| adaptive | M2 | 0 | 18 | 87 | 0 | not applicable (mock) |
| fixed_R0 | M0 | 0 | 18 | 87 | 0 | not applicable (mock) |
| fixed_R0 | M1 | 0 | 18 | 87 | 0 | not applicable (mock) |
| fixed_R0 | M2 | 0 | 18 | 87 | 0 | not applicable (mock) |
| fixed_R1 | M0 | 0 | 54 | 87 | 0 | not applicable (mock) |
| fixed_R1 | M1 | 0 | 54 | 87 | 0 | not applicable (mock) |
| fixed_R1 | M2 | 0 | 54 | 87 | 0 | not applicable (mock) |
| fixed_R2 | M0 | 0 | 78 | 87 | 0 | not applicable (mock) |
| fixed_R2 | M1 | 0 | 78 | 87 | 0 | not applicable (mock) |
| fixed_R2 | M2 | 0 | 78 | 87 | 0 | not applicable (mock) |

## Abstention and avoidable representation errors

| Condition | Metadata | Appropriate abstention | Incorrect abstention | Avoidable adaptive view errors |
| --- | --- | --- | --- | --- |
| adaptive | M0 | 18 | 0 | 0 |
| adaptive | M1 | 18 | 0 | 0 |
| adaptive | M2 | 18 | 0 | 0 |
| fixed_R0 | M0 | 18 | 0 | 0 |
| fixed_R0 | M1 | 18 | 0 | 0 |
| fixed_R0 | M2 | 18 | 0 | 0 |
| fixed_R1 | M0 | 54 | 0 | 0 |
| fixed_R1 | M1 | 54 | 0 | 0 |
| fixed_R1 | M2 | 54 | 0 | 0 |
| fixed_R2 | M0 | 78 | 0 | 0 |
| fixed_R2 | M1 | 78 | 0 | 0 |
| fixed_R2 | M2 | 78 | 0 | 0 |

Insufficient assigned fixed views are not agent representation-selection errors. Adaptive errors require an authorized sufficient alternative. Source-wide unavailable evidence is not repairable by choosing another view.

## Measured orchestration costs

| Condition | Metadata | Provider latency mean (ms) | Tool mean (ms) | Episode mean (ms) | Reported cost |
| --- | --- | --- | --- | --- | --- |
| adaptive | M0 | 0.076 | 0.202 | 2.639 | unavailable / not applicable |
| adaptive | M1 | 0.078 | 0.214 | 2.681 | unavailable / not applicable |
| adaptive | M2 | 0.085 | 0.213 | 2.699 | unavailable / not applicable |
| fixed_R0 | M0 | 0.064 | 0.212 | 2.684 | unavailable / not applicable |
| fixed_R0 | M1 | 0.063 | 0.201 | 2.599 | unavailable / not applicable |
| fixed_R0 | M2 | 0.070 | 0.207 | 2.658 | unavailable / not applicable |
| fixed_R1 | M0 | 0.063 | 0.049 | 2.436 | unavailable / not applicable |
| fixed_R1 | M1 | 0.064 | 0.050 | 2.446 | unavailable / not applicable |
| fixed_R1 | M2 | 0.071 | 0.050 | 2.500 | unavailable / not applicable |
| fixed_R2 | M0 | 0.054 | 0.041 | 2.402 | unavailable / not applicable |
| fixed_R2 | M1 | 0.056 | 0.041 | 2.481 | unavailable / not applicable |
| fixed_R2 | M2 | 0.062 | 0.040 | 2.439 | unavailable / not applicable |

For simulated providers, provider latency is local policy CPU time, not LLM inference. Missing usage and cost remain null. Source preparation, artifact reuse and rule construction/maintenance are separate in preparation_accounting.json.

## Deterministic fixed and contract-routing baselines

| Baseline | Metadata | Correct | Correct abstention | Other |
| --- | --- | --- | --- | --- |
| rule_adaptive | M0 | 23 | 6 | 0 |
| rule_adaptive | M1 | 23 | 6 | 0 |
| rule_adaptive | M2 | 23 | 6 | 0 |
| rule_fixed_R0 | M0 | 23 | 6 | 0 |
| rule_fixed_R0 | M1 | 23 | 6 | 0 |
| rule_fixed_R0 | M2 | 23 | 6 | 0 |
| rule_fixed_R1 | M0 | 11 | 18 | 0 |
| rule_fixed_R1 | M1 | 11 | 18 | 0 |
| rule_fixed_R1 | M2 | 11 | 18 | 0 |
| rule_fixed_R2 | M0 | 2 | 26 | 1 |
| rule_fixed_R2 | M1 | 2 | 26 | 1 |
| rule_fixed_R2 | M2 | 2 | 26 | 1 |

## Failure cases and diagnostics

| Case | Condition | Status | Independent diagnostic |
| --- | --- | --- | --- |
| `neighbor-fidelity` | fixed_R2 | incorrect |  |

Behavioral diagnostics separately identify temporal gaps/zero observations, normalized-size limitations, approximate geometry and evidence support. They use independent keys, never a model grading itself.

Paired M1−M0 and M2−M0 contrasts are retained in summary.json after averaging repetitions within each task. No confidence interval or significance claim is made for this selected synthetic task set. Runtime variation in a deterministic simulator is not a metadata mechanism.

## Reproduction and limits

Regenerate this report with `python -m dataset_prototype.embedding_study.agent_runner --report RUN_DIRECTORY`; this makes no model calls.
Exact prompts, schemas, proposal outputs, sanitized tool responses, rejected actions, private evaluation traces and usage availability are retained in compressed JSONL. Preparation is separately recorded. Application query caches start cold for each episode; no second cache factorial is added.
The explicit router is handcrafted from scientific operation requirements and a small public-question parser, not task IDs or reference answers. Construction/maintenance labor is unmeasured, not free. The mock adaptive policy uses the first offered interface; it is not learned routing.
Provider usage/cost fields absent from a transport stay null. Mock calls have no language-model token consumption measurement; live billing is not inferred. Parent orchestration/tool time and shared upstream preparation are separate from inference latency.
Real-model access, genuinely held-out events/templates and operational/general ecological conclusions remain pending. No scientific authority, real-data approval, neural embedding or unrestricted code execution is added.
