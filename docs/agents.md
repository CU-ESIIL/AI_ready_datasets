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

The isolated OpenClaw/Verde `llm-task` adapter is implemented as a tool-free JSON
inference transport. Full working-group worker scheduling, Slack integration and
authenticated human review remain unimplemented in this prototype.
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

## Evidence-bound review roles

The newer [scoped review workflow](review/index.md) adds explicit integrity and
quality reviewers, domain-owned evidence citations and typed scientific statuses.
Its six specialists and QA are independently bounded tool-free model calls over a
single frozen recipe. Role-specific JSON Schemas constrain ownership and finding-ID
syntax. Prior findings can be referenced by ID. Deterministic synthesis and human
approval remain separate. The legacy free-text consensus workflow above retains
its original four-specialist contract and historical vetoes.

## Semantic reasoning permissions

Agents may propose semantic resources and mappings, compare supplied definitions,
identify conflicts or missing evidence, suggest crosswalks and prepare review packets.
Candidate retrieval is currently local or explicitly adapter-backed; model roles
have no tools for autonomous web retrieval. Their permitted output is a judgment
or allow-listed plan, not a write to source data.

They must never invent ontology IDs, overwrite source meanings, treat lexical
similarity as equivalence, promote model judgment to source evidence, convert missing
evidence into failure, or alter unusual scientific values merely because they look
implausible. Scoped reviewers stay in their jurisdictions; QA synthesizes their
existing finding IDs rather than inventing specialist claims.

Agents reason and propose. Deterministic software executes approved recipes.
[Evidence distinctions](semantics/glossary.md#evidence) and the
[human workflow](semantics/review-workflow.md) apply throughout.

## Runtime role authority

Bounded model roles read evidence and produce schema-constrained proposals for
deterministic software to validate. VERDE is not a programmer or arithmetic engine.
The [trust-boundary guide](architecture/model-trust.md) specifies the executable IR,
operation library, parameter references, failure states and no-model execution.

| Role | Inputs → allowed output / schema | Operations, evidence and escalation |
| --- | --- | --- |
| Discovery | Request + fixed source candidates → `CandidateChoice` | Select supplied IDs and explain relevance; no mapping or source mutation; insufficient evidence can yield empty selection |
| Semantic | Source definitions + fixed target → `SemanticJudgment`; standalone candidate workflow uses `SemanticMappingProposal` | Compare/rank supplied concepts, never invent IDs/definitions or execute; novel/uncertain meaning needs review |
| Calibration / units | Authoritative unit/calibration metadata → `SpecialistFinding`, `ReviewVote` or scoped `SpecialistReview` | Compare evidence or recommend `unit.convert` / `calibration.scale_offset`; never calculate factors, ranges or coefficients; missing metadata requires evidence |
| Support | Native space/time/support evidence → scoped finding or vote | Compare support; only explicitly reviewed registered operations; no invented resampling/upscaling; support changes escalate |
| Rights | Source-specific legal evidence → scoped finding or vote | Classify documented rights, request evidence/review; never infer permission from calibration or other domains |
| Integrity | Source/version/hash-scope evidence and deterministic check results → scoped finding | Inspect computed identities; never invent or calculate hashes; incomplete scope needs evidence |
| Quality | Documented quality predicates and deterministic checks → scoped finding | Distinguish calibration, filtering and fitness; no model-computed statistics or invented bounds |
| Harmonization | Fixed mappings + `CapabilitySpace` → bounded `RecipeDecision` / `DecisionRecipeDraft` | SELECT or PARAMETERIZE offered options; no executable code, formulas, source IDs or numerical constants; explicit abstention allowed |
| QA | Frozen recipe + deterministic checks + existing findings → `Critique` / `QASynthesis` | Recommend registered checks, challenge evidence or veto; no new specialist claims, arithmetic, validator changes or execution permission |

All roles have no tools, shell, SQL, code-writing or data-write permissions. Mandatory
scientific checks cannot be disabled by a model. Scoped role schemas enforce evidence
IDs, jurisdiction, source pointers and frozen recipe identity. Exact schemas are
[generated from code](reference/contracts.md); deployed capability schemas additionally
constrain operation/option IDs. Unknown scientific meaning, insufficient evidence,
conflicting support, uncertain rights and consequential assumptions escalate.
