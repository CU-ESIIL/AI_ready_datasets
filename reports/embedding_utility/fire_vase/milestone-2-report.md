# Fire VASE milestone 2 — controlled agent infrastructure

Status: **WORKING** controlled harness and complete **MOCKED** protocol experiment,
20 November 2026. **Real-model evidence is pending.** H1–H4 remain untested for LLMs.
No neural embeddings, real wildfire observations, prospective forecasts or runtime
scientific code generation were introduced. Milestone-1 artifacts are unchanged.

## Implemented and executed

The modular extension adds JSON action/argument contracts, a deterministic metadata
renderer, fixed/adaptive authorization, scientific operation dispatch, provenance
receipts, finite budgets, provider abstraction, mock and explicit rule policies,
independent evaluation, behavioral diagnostics, paired summaries and offline report
regeneration. It reuses the original 29 questions, independent references, trained
PCA artifact and pinned external scientific worker. No copied upstream algorithm,
new model training or unreviewed numerical operation was needed.

The frozen v2 matrix has **348 cells × 3 deterministic repetitions = 1,044 mock
episodes** and **348 deterministic baseline episodes**. There were **2,088 mock
provider invocations and zero real-model requests**. Every scheduled cell is retained.
Fixed R0/R1/R2 and adaptive access are separate conditions; cache state begins cold
per episode rather than doubling the matrix. Representation payloads, scientific
operations, observations and budgets are constant across M0/M1/M2.

The model-facing environment contains no Task ID, required operation label, family,
answerability, reference value or scoring tolerance. Source/fire IDs are aliased.
General scientific operation contracts are legitimate M2 evidence; task-specific
instructions are excluded. Shared parsing includes representation formats, units,
null semantics and argument types. Errors are uniform across metadata conditions;
rich underlying scientific explanations remain private. Final numerical results
must reference actual deterministic tool results and their evidence receipts.
Unknown operations, invalid arguments, unauthorized representations, unoffered
identifiers and unsupported claims are rejected and recorded. Recovery uses new
proposals, not repaired output. Unexpected implementation failures are distinct from
invalid agent requests.

## Observed mock and rule behavior

Each row below collapses repetitions and metadata; it counts outcomes across the
same 29 public synthetic questions. These are not observed LLM capabilities.

| Simulated policy/interface | Correct answers | Correct abstentions | Approximate-fidelity misses |
| --- | --- | --- | --- |
| Mock fixed R0 | 23 | 6 | 0 |
| Mock fixed R1 | 11 | 18 | 0 |
| Mock fixed R2 | 2 | 26 | 1 |
| Mock adaptive (first allowed interface: R0) | 23 | 6 | 0 |
| Explicit operation-contract adaptive router | 23 | 6 | 0 |

The mock deliberately ignores metadata and chooses operations through a small
public-question phrase parser. Its outcomes are identical across M0/M1/M2. This
checks isolation and scoring; it does not show metadata has no value. The mock's
adaptive policy is not learned and offers no coverage gain over fixed R0 here.
The rule router uses scientific operation requirements and supplied preconditions,
not task IDs, references or benchmark answerability. Its hand-built language parser
is scoped to this public vocabulary, not general scientific language understanding.

R2's neighbor miss is the retained approximate two-neighbor diagnostic, not a
fabricated exact answer or independently wrong ecological analog. The source-ID
sidecar still supports sequence length. Independent scientific analog labels remain
unavailable, and appropriate abstention receives separate credit from numerical
correctness. Invalid-proposal recovery, wrong-unit/provenance/operation/argument,
wrong approximation claims and budget limits are exercised by tests, not silently
inserted as extra scientific cases in the frozen matrix.

## Evaluation and accounting

First proposed and final supported operation selections are separate. A wrong
operation or valid-but-wrong date cannot gain accidental numerical credit. Adaptive
abstention is incorrect when an authorized sufficient alternative exists. Insufficient
fixed assigned views are not avoidable routing errors. Temporal, normalization,
compression and citation diagnostics are independent behavioral criteria, not model
self-grading or claims to inspect internal reasoning. Free prose is retained but
not assumed true.

Token, reasoning, cache-token, snapshot and provider-cost fields unavailable from a
provider stay null. Mock CPU time is not LLM inference latency; actual model calls
are separately zero. Tools, query-cache hits, logical payload bytes, worker compute
and IPC have distinct measurements. Preparation references the original fitting/
materialization costs and measures current reuse/loading. Router construction and
maintenance labor are unmeasured rather than treated as free.

Paired metadata summaries first collapse repetitions within task and retain known
measurement denominators. The selected synthetic case set has overlapping events
and no population sampling design, so no significance claim or population confidence
interval is justified. Small latency differences in a deterministic simulator are
not evidence of semantic metadata effects or a general cost frontier.

## Evidence and reproducibility

- [Frozen protocol](agent-protocol-v2.md) and [configuration](config/agent-mock-frozen-v2.json).
- [Full generated tables/report](results/milestone-2-v2/report.md).
- [Episodes](results/milestone-2-v2/episodes.jsonl.gz), [exact decision/tool traces](results/milestone-2-v2/traces.jsonl.gz), [baselines](results/milestone-2-v2/baselines.jsonl.gz).
- [Manifest and hashes](results/milestone-2-v2/manifest.json), [paired summaries](results/milestone-2-v2/summary.json), [preparation accounting](results/milestone-2-v2/preparation_accounting.json).
- [Technical/reproduction guide](../../../docs/analysis/fire-vase-agents.md).

The source pin, dataset/question/artifact identities, environment, parameters,
schemas, prompts, outputs and timestamps are recorded. Prompt hashes and typed
proposals can be replayed without credentials. Reports regenerate without provider
calls. Test replay runs compare deterministic scientific/selection digests separately
from variable timings and memory. CI's pinned-source job now includes agent tests;
no new remote CI completion is claimed.

**Verification: 290 local offline tests passed, 2 skipped**, including **28 agent
benchmark tests**, using the explicit pinned scientific worker. The complete frozen
mock matrix completed without execution failures. Local source/artifact/output
hashes, documentation links and strict MkDocs generation are verified for delivery.

## Real-model and held-out scope

The read-only [access check](model-access-check-v1.json) found a valid saved
OpenClaw 2026.5.18 policy and declared Verde model, but gateway TCP access returned
PermissionError in this session and Docker state was not accessible. Credentials
were not present in the process environment, and no live cost/access authorization
was established. This does not prove a service is absent elsewhere; it means no
usable authorized inference was verified here. No real inference or external model
cost was incurred. No runtime, Slack, working-group or credential state was changed.

An optional real adapter implements the existing verified task protocol, fully
provider-qualified routes, returned model/provider checks, distinct isolated
session keys and normalized-JSON response scope. Plugin usage/weight identities are
not invented. Its transport contract is offline-tested with a test HTTP adapter;
that is not real-model testing. A permissive JSON-object transport allows structured
invalid actions to reach deterministic rejection/recovery; scientific execution
still requires the full strict action validator.

[The frozen smoke configuration](config/agent-live-smoke-v1.json) remains disabled
pending verified access and no-external-charge authorization. It fixes two indices
before execution, R0/M2, one repetition and six provider requests maximum; it is
connectivity smoke, not a reduced confirmatory experiment. A separate
[held-out-pending configuration](config/agent-held-out-pending-v1.json) cannot execute
until genuinely new reviewed inputs exist. The existing public cases are not
relabeled as unseen data. Real-model evidence is a separate completion criterion.

## Development history and remaining work

[The development ledger](agent-development-log-v2.json) preserves the initial unit-
property implementation failure and subsequent wiring run. Their initial config
phase field said frozen_pilot prematurely; they are explicitly excluded as debugging
runs without modifying their original manifests or responses. V2 fixes the public
boundary and controls before the retained freeze. No reference answers or original
scientific audit were changed to improve observed results.

Next: verify actual runtime/cost access, run the predeclared smoke, then design a
properly sized paired real-model pilot with new event/template holdouts and reviewed
scientific evidence. Targeted direct-statistic implementations and router maintenance
costs remain important before confirmatory computational comparisons. None of these
remaining scientific/model claims is filled in with mock outcomes.
