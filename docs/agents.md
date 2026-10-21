# Bounded agents

The default offline demo uses deterministic fixture roles. All four roles also have
real model-backed implementations through local Ollama, exercised with actual
Sentinel metadata. See the [live workflow](real-data-agents.md) for commands,
transcripts, review gates, and the latest rejected proposal. Neither mode requires
OpenClaw or commercial LLM credentials; no automatic fallback crosses modes.

| Role | Permission | Output |
| --- | --- | --- |
| Discovery Agent | Read discovery/access metadata | Candidate resources with relevance rationale |
| Semantic Agent | Compare explicit scientific metadata | Relationship, evidence, confidence, source, review state; abstains on ambiguity |
| Harmonization Agent | Propose allow-listed recipe operations | Attributable versioned recipe; cannot execute it |
| QA Agent | Independently assess recipe and evidence | Approval, rejection, revision, or human-review contract |

Agents never mutate observations, choose arbitrary code to execute, infer
compatibility from similar names, or silently repair a scientific disagreement.
The executor rechecks QA and gates human decisions independently.

The [OpenClaw container](https://github.com/CU-ESIIL/openclaw_container) provides a
future file-based worker/review environment. Each role can later receive a validated
request and emit its current structured artifact in a mounted workspace. Human
review can map to the existing PI Liaison/review packet workflow. Worker scheduling,
The isolated OpenClaw/Verde `llm-task` transport is now implemented; full working-group
worker scheduling and authenticated human review remain unimplemented.
Local model calls and schema-validated transcripts are implemented. Model QA
rejection/revision blocks execution; model proposals always need human review.

[OpenClaw and Verde](openclaw-verde.md) documents the installed-version adapter,
no-model-tools policy, strict route checks and normalized-response evidence limits.

## Metadata consensus and direct streaming

The [streaming harmonization module](streaming-harmonization.md) adds metadata-only specialist
dialogue, digest-bound unanimous review, documented Sentinel-2 scale/offset
calibration, and bounded window-to-encoder execution without raw or harmonized
data files. The existing fixture/snapshot commands retain their historical
materialization behavior. Current streamed vectors are reference numeric features;
model consensus still requires an actual human decision before execution.
