# Architectural decisions and repository audit

## 2026-10-26 — All-TACC storage and versioned backup planning

At user direction, inference spending and open-model runtime are front-loaded toward ontology/recipe development: 50%/one-third/one-sixth across Years 1/2/3. This changes annual demand allowances, not aggregate totals or scientific execution gates.

Storage tables report total retained capacity, not new annual ingest. The retention ledger carries earlier product releases forward without product deletion, distinguishes workspace closeout from protected backup history, and records the peak-capacity consequence of delayed closeout. Gross writes and real snapshot expiration remain unmeasured.

The backup audit uses current/prior-year mutable high-water capacity for ordinary version history, plus a full 6 TB governance closeout reserve in Year 3. This avoids shrinking backup capacity solely because active cohort workspaces close. It remains an unmeasured churn scenario, not a provider guarantee.

Target TACC for all persistent storage/distribution and additional recoverable backups; retain Jetstream2/ACCESS for inference and compute. This supersedes earlier OSN deployment planning without rewriting historical run records. Proposed 14 daily/12 weekly/12 monthly retention is sized by an explicit mutable-content churn model; neither scheduled backup nor provider service is implemented. No raw/harmonized persistence is added. See [budget and evidence](../resource-budget.md).

## 2026-10-23 — Local management composition

Use standard-library SQLite and content-addressed output files around the existing
independent scientific modules. This is not a replacement for MESA, OSN, a graph
database or authenticated governance. Imports recheck existing gates and bounded
MOSAIKS verification without changing input bundles. Controlled exports/backups
preserve metadata, blobs and dependency identities; recovery is actually tested.
The loopback UI creates only version-bound issues: no approval, execution or
publication authority. Planned products and unawarded requests stay explicit;
metadata index timing is not global encoder throughput. No scientific-track
configuration or raw/harmonized persistence changes are introduced.
See [workbench contracts and limits](../management-workbench.md).

## 2026-10-21 — V0 foundation

The initial checkout had README/AGENTS, MkDocs Material configuration and assets,
Pages deployment, manual template-sync and manual JupyterLab-image workflows.
There were no source, tests, data, packaging, environment, changelog, or dev-log
implementations in the committed template. Earlier provenance documentation and
an uncommitted changelog were retained and extended.

- Preserve MkDocs/Material, assets, and Pages deployment. Add a standard `src/`
  package and tests; keep website and package structure separate.
- Use Pydantic frozen typed contracts and JSON Schema at stage boundaries so
  discovery, harmonization, and representation can be tested independently.
- This is data infrastructure: discovery/access, recipes, execution, observations,
  representations, governance and lineage. A registry or STAC catalog alone cannot
  express the complete mechanism. STAC remains one discovery metadata component.
- Agents propose explicit recipes; deterministic allow-listed execution provides
  reproducible scientific transformations without generated code execution.
- Preserve provenance with every representation, including original values,
  metadata/rights snapshots, recipes, proposals, QA, optional human decisions, and
  parent core observations. JSON-LD is enough; no graph database is warranted.
- Distinguish modality from scale so different observation methods do not conceal
  different spatial/temporal support.
- Separate conservative core transformations from application-specific track rules.
  Shared data and caching do not force common scientific interpretation.
- JSON outputs make the small prototype reviewable and avoid introducing Parquet
  dependencies before their scale benefits are needed.
- Use project-authored synthetic fixtures rather than quietly ingesting external
  records or assuming provider redistribution rights. Native-schema adapters and
  real field/raster support harmonization remain explicit milestones.
- Keep MESA integration unavailable where tool signatures are unverified; its
  overview and source README differ in stated implementation status.
- Preserve the manually triggered template-sync and image-build workflows as
  historical template infrastructure. The image job still requires absent
  `containers/jupyterlab` files and template sync can overwrite project changes;
  neither is used by V0. Keep Pages and add an independent offline-test workflow.

## 2026-10-21 — First real-data and model boundary

- Add a small actual Sentinel STAC/COG vertical slice before assuming NEON access.
  The official NEON data route returned 403 without a token; its current license
  is CC BY 4.0. A token-aware native-file boundary exists without pretending sensor
  metadata normalization has been completed.
- Use an existing local Ollama model to exercise real role inference without new
  hosted credentials. OpenClaw remains a later runtime adapter, not a fabricated
  live integration. Preserve fixtures for deterministic offline regression tests.
- Retain raw DN, scale/offset, SCL and native pixel support rather than silently
  convert to reflectance or assert field equivalence. Permit explicit instantaneous
  timestamps and qualify extracted-window checksums.
- A real model rewrote a source identifier. Fail that call, retain its transcript,
  and narrow the judgment schema so code owns immutable identity/targets. This is
  a contract correction, not a hidden repair of the scientific decision.
- The later real model QA rejected a raw-DN proposal over calibration-context
  concerns. Preserve this result and enforce the veto; a successful model call
  is not evidence of correct science. Bind model review to content and retain
  mandatory human review regardless of model confidence.

## 2026-10-21 — OpenClaw and Verde

- Reuse the existing image and Verde credential rather than modifying working-group
  defaults or copying OpenClaw. Inspect the installed version and plugin source.
- Use the installed JSON-only `llm-task` HTTP bridge because it disables tools and
  preserves the bounded-role contracts; avoid unrestricted normal agent turns.
- Isolate gateway, state, workspace, credentials, port and model route. Expose only
  host loopback, disable channels and model heartbeat, and retain human review gates.
- Fully qualify slash-containing model IDs; disable tool-schema compatibility for
  Verde's no-tools tasks. Never add a dummy executable tool as a workaround.
- Label gateway-normalized JSON and unavailable provider usage/weight digest
  honestly. Keep runtime/configuration provenance separate from model identity.

## Metadata control plane and streaming data plane

Specialist dialogue uses only pinned metadata, fixed scientific targets and a bounded revision budget. Source access is delayed until unanimous consensus, deterministic QA and exact-recipe human approval. The first target is documented Sentinel B08 scale/offset reflectance. Existing executor buffering is constrained to one microbatch; joins/aggregation are rejected before source access. Persist embeddings and compact hash-based lineage, not raw or harmonized datasets. Full raw-data reconstruction is intentionally unavailable without reaccessing the source. Learned encoder integration remains open.

The installed OpenClaw compaction reserve is explicitly 8,192 tokens for bounded
one-shot tasks (4,096-token output cap, 32,768-token context). This corrects a
verified 20,000-token default-floor overflow without raising the advertised model
context or dropping peer evidence. Invalid calibration drafts and self-citing
reviews remain rejected; explicit recovery reuses only verified initial analyses
and, where present, the first valid unreviewed draft for fresh reviews.

## MOSAIKS consumes harmonization outputs

Use empirical MOSAIKS random convolutional features rather than a generic pretrained visual encoder or precomputed vectors with unrelated source provenance. Keep source access and reviewed scientific calibration upstream. Preserve canonical spatial raster structure; never reshape unrelated scalar records into images. Fit a bounded empirical filter bank on training outputs only; persist derived filters and vectors, not raw or harmonized raster arrays. Store labels separately and distinguish generated/derived diagnostics from independent scientific validation. Bind new raster extent and representation settings to fresh consensus.

## 2026-10-21 — ADR 1: Preserve three independently callable stages

Keep discovery/access, harmonization/review and representation in their existing
modules. The audit found review leakage and documentation debt, not a need for a
package rewrite. Add typed review contracts beside the legacy dialogue contracts;
keep orchestration thin. This preserves useful history and independently testable interfaces.

## 2026-10-21 — ADR 2: Scientific review statuses are not workflow votes

Use PASS, FAIL, NEEDS_EVIDENCE and NOT_APPLICABLE in the new evidence review.
Deterministic synthesis computes eligibility, missing-evidence review or revision.
Human approval is separate and mandatory for model proposals. Existing agent vetoes
remain binding; new metadata reports cannot authorize streaming.

## 2026-10-21 — ADR 3: Jurisdictions and evidence precede synthesis

Add integrity and quality jurisdictions to semantic, units, support and rights.
Provide each model only its curated evidence and the same frozen recipe. Stable
IDs and references avoid resubmitting the same finding; QA references existing IDs.
Enforce citation domains, recipe binding and ID syntax deterministically. Natural
language truth and semantic deduplication remain expert-review responsibilities.

## 2026-10-21 — ADR 4: Calibration and quality are distinct claims

Retain documented scale/offset and dimensionless unit 1. Negative reflectance alone
does not invalidate the calibration equation and is never implicitly clipped.
Document the independent SCL/nodata predicate and distinguish calibrated,
quality-filtered calibrated and use-specific analysis-ready products. Independent
scientific validity cannot be inferred from a derived texture diagnostic.

## 2026-10-21 — ADR 5: Evidence-based rights and checksum scope

Rights reviews address authoritative terms for an intended operation, not speculative
consequences of numeric values or a catalog label. Missing terms need evidence and
human interpretation. Integrity owns checksum scope: metadata, extracted windows
and full remote objects are different claims. No source-data reads occur in review.

## 2026-10-21 — ADR 6: Retain actual model failures

Preserve historical rejected Sentinel reviews and the scoped run’s invalid finding
identifier unchanged. Tighten role-specific deployed JSON Schemas before an explicit
fresh run. Never convert an error into approval, invent raw provider text/usage or
apply hidden output repair. Store accepted intermediate reviews and failure checkpoints.

## 2026-10-21 — ADR 7: Narrative entry, progressive technical depth

Keep MkDocs Material, Markdown, existing technical URLs and Pages. Add a spacious
research narrative with Home, Approach, Data, Science and Impact; Documentation
organizes progressively deeper module, governance, operation and reference pages.
Use repository-generated SVGs and credited NASA educational imagery. Do not reuse
an unattributed hero or introduce a frontend framework or deployment change.

## 2026-10-21 — ADR 8: Generate reference from code

Generate JSON Schemas and Markdown source/module links from actual contracts and
Python definitions. Keep diagram specifications in a deterministic generator.
Generated outputs are committed for GitHub readability; regeneration and strict
build/link checks expose drift without requiring a JavaScript documentation stack.

The new report is an additional gate on real Sentinel streaming, not an alternate
route around legacy consensus or human review. Preflight reconstructs findings
from their persisted evidence ledger, checks the source-set and recipe digests,
and honors explicit QA synthesis vetoes. Generated/offline paths remain explicit.
The scoped live pilot still produced a questionable integrity inference; retain
it as evidence of the remaining limits of model judgment.

## 2026-10-21 — Semantic ADR S1: Compose community resources

Preserve the wide landscape of ontologies, vocabularies, classifications, standards,
frameworks and historical efforts. A project profile composes selected resources;
it does not declare a universal ontology or replace source community meanings.
Coverage and candidate roles are provisional project assessments with explicit evidence.

## 2026-10-21 — Semantic ADR S2: Discover evidence before interpretation

Module 1 discovers data, access metadata and semantic evidence. Typed concept
candidates have retrieval bases but no mapping or approval fields. Module 2 retains
scientific interpretation, mapping, recipes, QA and human gates; Module 3 consumes
harmonized outputs. Portal access remains behind explicit optional adapters.

## 2026-10-21 — Semantic ADR S3: Source-native semantics are provenance

Preserve identifiers, resource identity, definitions and locations in nested source
semantics. Bind evidence to the complete pre-enrichment source record. Omit absent
semantics from serialization to preserve historical source/plan identities; enriched
identities must not reuse stale derived products. Never overwrite source concepts.

## 2026-10-21 — Semantic ADR S4: Labels are insufficient

Separate source-annotated identifier retrieval, normalized identifiers, exact
vocabulary labels, lexical candidates and model hints. None establishes equivalence.
Model hints cannot be relabeled as source or deterministic evidence. Identifier
namespace recognition does not verify concept existence or a crosswalk.

## 2026-10-21 — Semantic ADR S5: Scale is multidimensional

Keep structural, ecological, taxonomic, spatial, temporal, observational and other
organizations separate. Do not present organism-to-species as a subclass relation,
or sample-to-dataset as one universal observational hierarchy. Explicit relations
and source community definitions govern the interpretation.

## 2026-10-21 — Semantic ADR S6: Support is scientific metadata

Record location, native CRS, footprint, resolution, extent and support distinctly.
Instantaneous source acquisitions keep equal start/end values. Metadata discovery
records documented calibration-output units without converting stored DN. Shared
coordinates, units or timestamps do not establish comparability.

## 2026-10-21 — Semantic ADR S7: Cross-support derivations need justification

Treat formal representation of scientific justification for cross-scale transformations
as a continued literature-review hypothesis. Do not claim no ontology addresses it.
Any actual transformation requires an explicit allow-listed recipe, tests, provenance
and review. A provenance relationship alone does not prove its scientific validity.

## 2026-10-21 — Semantic ADR S8: New concepts are a last resort

Search existing resources, compare definitions, attempt justified composition and
consider upstream extension before proposing a project concept. Record failed
alternatives, intended meaning, relations, reviewer/date and evidence. The reusable
human template is a non-executable review artifact, not automatic approval.

## 2026-10-21 — Semantic ADR S9: Benchmark metadata without overstating it

The user selected local inventory/source-metadata diagnostics for the first benchmark.
Write explicit-schema Parquet tables, including valid zero-row tables, with input/code
hashes and failure manifests. Coverage weights, pair overlap, documentation rankings
and greedy portfolio selection are transparent project heuristics, not measured term
alignment, ontology quality or scientific suitability. No data reader or model is invoked.

## 2026-10-21 — Semantic ADR S10: Dataset profiles precede selection

Explicit ontology use records declared semantic infrastructure. Ontology potential
asks whether definitions, methods and context support recoverable meaning. Semantic
diversity describes distinct dimensions, not ontology completeness. Ontology leverage
is an interpretable profile of richness, recoverability, connectivity, accessibility
and evidence quality. No scalar product or flagship selection is implemented by the
current documentation-presence rankings. Candidate pairs require independent review
of scientific comparability, rights and support transformations.

## 2026-10-21 — Documentation ADR: Narrative and evidence stay synchronized

Retain the existing Material/Pages infrastructure and editorial design. Public pages
explain why scientific semantic variety matters; linked technical pages expose typed
contracts, operations, evidence and status. Keep the 86-resource inventory canonical;
generate the table, filter metadata and downloadable mirrors from it. Local accessible
JavaScript enhances filtering; the full table and expandable evidence remain usable
without it. Diagrams distinguish architecture from uncomputed research frameworks.
A contract, semantic relationship, evidence model, transformation or module-boundary
change updates documentation and its architecture diagram in the same change.

## 2026-10-21 — Trust ADR T1: Runtime models are not computational authorities

VERDE and other runtime models interpret, compare and propose within caller-defined
capabilities. They do not write executable science, derive formulas or author numerical
results. Scientific operations are designed and reviewed before runtime; development
models assist that process without replacing scientific responsibility.

## 2026-10-21 — Trust ADR T2: Closed operations, declarative IR

Maintain the existing scientific recipe and introduce distinct SELECT, PARAMETERIZE
and semantic PROPOSE contracts. A closed registry maps versioned IDs to pre-written
implementations. Offered option IDs bind complete source metadata, fixed mappings,
parameter references and registry identity. Calibration resolves authoritative
metadata, never model coefficients. No executable code or expression language is accepted.

## 2026-10-21 — Trust ADR T3: Structure precedes science, neither grants approval

Parse exact schemas, validate operation/option and source identities, then apply
scientific preconditions, QA and exact-recipe human review. Missing evidence and
human review are valid outcomes. Unknown operations and invalid parameters fail
closed. A model's recommendation cannot remove mandatory checks or override a veto.
Deterministic consensus consumes structured findings; model QA can only constrain it.

## 2026-10-21 — Trust ADR T4: Approved science has no inference dependency

Approved recipes execute through the registry without a model/backend. Keep the
explicit fixture model for offline orchestration and adversarial testing. Preserve
the bounded real-data streaming APIs; the new fixture controller is capped at 1024
records and cannot bypass real-data review gates or persist raw/harmonized rasters.

## 2026-10-21 — Trust ADR T5: Proposal, validation and approval are distinct evidence

Model statements remain MODEL_JUDGMENT. Deterministic computations and validations
retain their code/registry/constants identities. Human decisions bind the exact
recipe. New recipe, scalar provenance, raster/stream lineage and cache identities
record the execution backbone; legacy artifacts remain historical without invented
new metadata. Scientific code changes invalidate new bound recipes and require review.

## 2026-10-21 — CubeDynamics ADR C1: External primary environmental backend

Use ESIIL CubeDynamics as the intended primary environmental manipulation backend,
behind a small replaceable adapter. Keep it external, optional and pinned to the
inspected prerelease 0.1.0rc3. Core semantics, review and existing operations remain
independently callable. The source/public API and installed distribution are inspected
before registering capabilities; no upstream code is copied.

## 2026-10-21 — CubeDynamics ADR C2: Registered references, not runtime Python

Extend the existing scientific recipe with backend operation records and a digest
of reviewed configuration/source/implementation context. Runtime models select only
closed capability IDs and schema-constrained references. The adapter uses explicit
pre-written dispatch, including fixed select/isel/where stages through upstream's
public apply API. Arbitrary apply, function names, expressions and imports are never
model permissions. Exact-recipe human decisions and prior model vetoes remain binding.

## 2026-10-21 — CubeDynamics ADR C3: Stream and plan before materialization

Reuse Module 1's native readers rather than duplicate CubeDynamics/Cubo discovery.
Accept bounded trusted xarray/Dask inputs; preserve lazy values while inspecting only
bounded coordinates. Guard input/output size and task graphs. Materialization is an
explicit reviewed configuration change and computes only the bounded final graph.
No raw or harmonized arrays are persisted; final-window hashes state their scope.

## 2026-10-21 — CubeDynamics ADR C4: Computation does not justify support changes

Require evidence and human review for aggregation/alignment. Preserve resolution,
support, extent, CRS, units and biological meaning separately. Expose only complete
equal-duration whole-window means and same-CRS nearest spatial sampling with exact
time labels in this first backend. A mean's interval duration does not determine a
new temporal sampling cadence. Reprojection and general resampling remain unexposed.

## 2026-10-21 — CubeDynamics ADR C5: Explicit result and representation boundaries

Typed TransformationResult records connect source evidence and recipes to external
backend operations and resulting metadata, changes and package versions. A lazy plan
is not a completed data read. The initial MOSAIKS bridge permits only layout-preserving
one-band selection/subset/calendar operations on already calibrated bounded windows.
General support-changing products need a separately reviewed representation bridge.

## 2026-10-21 — Evidence-led pipeline state report

Keep a portable local evidence snapshot, machine-readable component inventory and
programmatic ReportLab/Matplotlib report under `reports/pipeline_state`, with the
final PDF under `output/pdf`. Link the report from the website; the repository is
the source of truth. Distinguish retained real source evidence from generated
CubeDynamics/MOSAIKS diagnostics. Missing ontology depth, dataset potential/diversity,
independent validity and throughput remain unmeasured. No new source acquisition,
model inference, approval or website deployment is part of report generation.

## 2026-10-22 — Validate science without widening model authority

Add analysis-only modules and explicit evidence snapshots; leave the scientific
operation registry and executor unchanged. Measure graph structure and live model
behavior separately from inherited scope assessments. Exact combinations through
size three optimize a declared dimension rubric; longer curves are greedy witnesses.
Candidate dataset diversity/potential are scoped review diagnostics, not compatibility.

Keep the historical Sentinel review immutable and prepare a new unapproved draft.
The whole-raster hash objection is documented as unsupported by the bounded-stream
contract, without removing its veto. NIWO metadata supports a candidate site/month
but not a sensor location. A contextual interval-to-instant association needs a new
scientifically defined deterministic method; existing exact joins do not substitute.

The first Verde pilot uses one configured 120b model. Natural-language content is
wrapped in the installed plugin's mandatory JSON envelope; C/D re-evaluate B rather
than adding samples. Human gold and weaker-model competence are not established.
Retain this protocol limitation, exact model responses and negative findings.

## 2026-10-23 — Describe the data lifecycle before making storage commitments

Document source/provider ownership, transient raw/harmonized windows and retained
feature/encoder/decision evidence separately. Treat ignored local paths, a
OneDrive-located checkout and Git history as insufficient evidence of managed backup
or access controls. Keep retention, preservation destination and model-processing
terms as explicit decisions for the data management plan; do not imply MESA or an
institutional storage service is already deployed. The report adds no execution path.

## 2026-11-20 — Separate embedding utility analysis from pipeline design

Keep study planning under `reports/embedding_utility/` in protocol/cases/results
subfolders, with a website overview. Future code/tests/fixtures retain their normal
repository locations. This is analysis, not a new track or runtime interface.
Start with existing MOSAIKS and matched-input alternatives; other representation
families need separate protocols. Preserve independent-label, leakage, practical-effect
and cost questions. No universal utility claim, execution permission or cleared
veto follows. Architecture and generated contracts are unchanged.

## 2026-11-20 — Test embeddings against agents using source tools

The primary intervention is a materialized embedding interface, not replacing an
agent with a vector. Compare the same agent with direct, embedding and hybrid
interfaces; retain deterministic references and account for caching, tool quality,
external training exposure and lifecycle costs. Raster prediction is subordinate
to this broader question. “Raw” does not bypass scientific preprocessing. Preserve
registered-operation execution; conclusions apply to that agent capability boundary.
The premise that agents already work well with these data remains unmeasured.

## 2026-11-20 — Measure representation diagnostics before agent claims

Use existing MOSAIKS on generated identity-harmonized windows, compare summary and
pixel ridge consumers with identical splits and validation-only tuning, and retain
all seeds/settings as exploratory evidence. Summary targets intentionally expose
easy exact operations; they are not independent prediction labels. Keep arithmetic
cost scenarios separate from measured local encoding time. Reusable helpers live
in src with offline tests; report generation stays in the analysis workspace.
No new operation registry, scientific contract or architecture boundary is introduced.
Do not translate these curves into agent competence, ecological validity or a
production throughput claim. Snapshot source/output hashes and retain negative
findings. New real cases still need existing scientific gates.

## 2026-11-20 — Use Fire VASE as a proposed scientific utility case

Pin upstream inspection to 2e20e15a42610f77cdd0583bb5a43fcc6f6c8959 and retain
read-only code/schema/summary hashes. Keep the original proposal and literature
scope assessment in the analysis workspace. Separate source histories, scientific
profiles, statistical embeddings and agent routing; use fixed-data metadata views
to avoid retrieval-corpus confounding. Forecasting must not reuse completed-fire
normalization, and globally fitted manuscript PCA is not a clean holdout artifact.
Upstream currently shares the cubedynamics namespace; plan isolation rather than
vendoring or modifying either implementation. No runtime interface is added yet.
Code-constructing agents remain deferred under existing model-execution policy.
No fire-data integration, source access, training, agent run or scientific approval
is implied by the inert pilot inventory. Real inputs need reviewed rights/support.

## 2026-11-20 — Implement synthetic Fire VASE utility without widening authority

The analysis-only embedding_study package owns explicit history/task/artifact
contracts, strict representation payloads, metadata views, independent answer keys
and measured execution. Keep source-native observations separate from shape-only
features and coordinates. Evidence-backed one-day increments, missing versus zero,
interval growth and unknown baseline are distinct. Real ring/cumulative equivalence
is unresolved and must not be inferred from column names.

Reuse the external Fire VASE operation file at the audited commit and SHA in an
isolated worker; permit only fixed features/pulses/PCA dispatch. Do not import its
transitional cubedynamics namespace into the core environment or copy upstream
code. Fits use declared synthetic training IDs only; all queries reuse the artifact.
PCA neighbor fidelity compares backprojections in original profile units, with
approximation explicit; it does not equate metric changes with compression.

Reference integration uses rational interval arithmetic and independent SVD, not
backend answers. The deterministic matrix tests metadata isolation, not metadata
benefit or agent competence. Score justified insufficiency separately from errors
and penalize unsupported numeric answers. Preserve costs for both direct caches
and materialized views, including warm prefill and preparation. Cold application
caches do not imply cold OS caches, and parent traced allocation is not worker RSS.

Retain compact generated evidence and source/output hashes. Document actual local
replay and configured (not yet executed remotely) CI separately. Production tracks,
streaming gates, human decisions, original proposal/audit and historical vetoes are
unchanged. No real-data integration, code-writing agent, forecast recipe or neural
training is part of this milestone.

Count source-ID provenance as available information: a validated primary consecutive
profile retains one ID per evidenced day. R1/R2 may answer the declared sequence
length from that metadata; do not overstate what normalization removed from the
complete interface. Exact absolute-size/date queries still demonstrate information
loss without source fallback.

## 2026-11-20 — Control the agent information boundary before model inference

Use explicit public projections rather than serializing the milestone-1 Task. Alias
native fire/observation IDs and keep expected operations, answerability, references,
tolerance and family labels private. General scientific contracts are legitimate
metadata; their item-specific application belongs to the agent/evaluator separately.
Keep operation implementations, data, payloads and budgets fixed across metadata.
Sanitize tool failures uniformly so M0 cannot receive M2 through errors. Preserve
exact rejected proposals and new recovery attempts without repairs.

Models return inert JSON. A deterministic synthetic controller checks authorization,
registered operation/argument contracts, budgets and source receipts. Numerical
final answers resolve existing validated values; a coincidentally right unsupported
number is not scientific success. Distinguish forced insufficiency, avoidable adaptive
selection, wrong operations/arguments, approximate geometry and provenance. Record
first and final selections and evaluate behavioral criteria independently of prose.

Use the complete 348-cell synthetic matrix and explicit non-LLM baselines; do not
manufacture a metadata effect with a simulator. Collapse repeats within task, and
withhold population intervals for the selected overlapping synthetic cases. Reuse
frozen PCA/source artifacts with their original preparation costs; query caches
reset per episode. Unknown provider usage/pricing/snapshots remain null. A manual
contract router has unmeasured construction/maintenance costs, not zero costs.

The live OpenClaw adapter keeps verified 2026.5.18 schemas/routes and no native tools
or fallback. JSON-object transport allows invalid structured proposals to reach the
strict deterministic validator and recovery boundary. Unique session keys isolate
calls; normalized output is not raw provider text. No live call is made without
verified access and cost bounds. This session could not establish reachable authorized
inference, so only explicit mock evidence is retained. No runtime/channel/credential
state or historical veto was changed. Early development runs with premature phase
labels are audited separately, not silently relabeled as frozen scientific evidence.

## 2026-11-21 — Expanded representation utility, strong raw-data rivals

Keep M1/M2 artifacts immutable and add separate V3 contracts/fixtures/runner. Share
the existing proposal controller and source-authorization dispatcher through optional
statically supplied contract/serialization hooks; defaults preserve M2 behavior.
Runtime models cannot choose contracts or executable implementations. The external
Fire VASE pin and worker remain unchanged.

R0 informationally dominates its deterministic representations, so adaptive access
cannot be assigned an accuracy advantage by construction. Measure legitimate reuse
cost tradeoffs with targeted direct CDF integrals and indexed native lookup, matched
query-result caches, preparation attribution and routing overhead. Distinguish the
PC metric, backprojected-profile metric and full-profile metric. Coordinates alone
cannot establish discarded residuals; mathematical neighbors are not ecological gold.

Freeze 120 evaluation questions on 20 new histories and separate development/training
cohorts. Evaluation narratives are visible to implementers and the hand-authored
phrase baseline; label this model-unseen, not independently blinded. Numeric keys
use independent rational/SVD/prominence oracles. General source-evidence claim rubrics
remain assistant-authored drafts pending expert adjudication. They test operation
selection/evidence use, not unobservable intrinsic scientific understanding.

Expose only development-calibrated timings in every metadata arm, never per-evaluation
task sufficiency/cost outcomes as routing hints. Private measured cost minimum is
computed only among scientifically sufficient views at the declared target. Report
counterfactual identical-query amortization separately from actual measurements;
common resident process startup, physical source IO and heterogeneous-query
intermediate memoization are outside that frontier. Unknown tokens/cost stay null.

Saved runtime policy is valid, but the session cannot reach the gateway and access/
cost authorization is unverified. No inference or service/credential change. Keep
real configs disabled; require input hashes, checked frozen smoke evidence and
explicit verified no-charge access before pilot invocation. Positive paid caps are
unsupported when this transport supplies no usage/cost accounting. Preserve draft
fixtures and failed integration runs in ignored outputs with an explicit ledger.

## 2026-11-21 — Prefix learning and materialization are independent mechanisms

Implement Track B independently of real-agent access. Select next-calendar-day
observed growth from available prefixes because no approved analog relevance or
new geometry objective exists. Do not use completed-history VASE normalization in
prediction. Keep this new recipe synthetic-only; physically present legacy FIRED
files do not establish rights, scientific support mapping or operational availability.
Inspect footers/catalog schemas only; no real source rows or large archive ingestion.
`RealPrefixApproval` records required evidence but does not approve or read a source.

Use a static auditable NumPy causal convolution (177 parameters), dimension-matched
PCA4 and learned4 probes, raw/explicit prefix ridge, persistence and a similar-size
MLP (168 parameters). Model output never authors executable scientific code. Fit
preprocessing/encoder/PCA/heads only on training fires; seed selection and calibration
use separate validation fires. All prefixes of each fire remain together. Preserve
all checkpoints and test outcomes; neither source/license ambiguity nor unavailable
inference permits a silent mock substitute.

The synthetic learned probe improves on tested PCA/summaries but not raw ridge;
near-matched neural errors do not isolate a unique embedding mechanism. Treat
statistical fitting, information preservation, computational reuse and agent selection
separately. Precompute the identical trained encoder/head for a materialization test,
then compare cached complete predictions as a stronger repeated-query rival. Include
training/construct/read/write identities and costs; unknown lifecycle labor/refresh
rates remain unmeasured. Nominal identifier invariance is required; scale/order
sensitivity is not ecological validation. Changed temporal support must abstain.

Real Track A remains pending under unchanged frozen protocols/configs. Read-only
checks cannot reach the gateway from this session, and no verified no-charge access
exists. Recorded transport payloads fit the adapter limit; live identity, parsing,
usage and actual model behavior still need the authorized smoke. No infrastructure,
credential, Docker or Slack state was changed.

## 2026-11-21 — Freeze the representation, separate added supervision and reuse

M5 reuses the exact M4 synthetic cohort, preprocessing/PCA and A-only encoder. Verify
canonical histories, full prefix availability/support fingerprints and checkpoint
identities; publish row-level source lineage. A test performance was previously
observed, so label new B–E task evaluation on existing histories rather than a new
independently hidden cohort. Separate validation selection/calibration by fire.

Define B as next-three total, C as strict next-three versus last-three mean comparison,
D as population SD of next-three increments and E as future-vector geometric relevance.
Independently check target identities; disclose correlated outcomes. Freeze targets,
metrics and all task comparisons before retained evaluation. New lightweight heads
are supervised downstream transfer, not zero shot. Shared AD and specific encoders
receive additional objectives; no A-only transfer credit for that supervision.

Preserve M4 code/artifacts and implement statically registered multihead MSE/BCE
training that reuses its encoder forward computation. Compare raw/summary/PCA,
frozen/shared/specific views, direct matched-capacity MLP and shared-MLP controls.
Linear and higher-capacity nonlinear source-property probes test approximate recovery,
not exact absence or causal meaning. Invalid support is source rejection, not a model
competence result. Retrieval excludes every same-fire prefix and uses future outcomes
only in grader relevance or explicitly train-only E-supervised heads.

Average paired prefix losses within fires, then use conditional descriptive empirical
fire resampling; no wildfire population or multiplicity claim. Keep the full task
matrix, including negative transfer. Shared encoding reduces separate-neural work
but need not beat direct heads, stored vectors or whole-bundle caches. Record current
and historical training, construction/storage/query identities and unknown refresh/
maintenance costs separately. A metadata-only release hardening replay preserved the
exact predictive evaluation digest; no scientific settings or outcomes were changed.

## 2026-11-21 — Local lake discovery and explicit real-data approval boundary

The user clarified that the lake lives inside Fire VASE. Inspect the actual packaged
`data_lake/fire-vase-data-lake-v0.1/files/` tree, not only expected root cache paths or
legacy CubeDynamics pointers. Selected native/derived files are physically present
with inventory-matching sizes; no upload, download, restore or copy is needed. Keep
historical full-container checksums separate from fresh metadata hashes and current
unverified file identity. The package's historical manifest mode does not override
current presence of materialized files.

Complete all authorized M6 source-document, schema/CRS and review-material work while
stopping before observation rows as the user explicitly required. Code documents a
native daily-area copy and reconstructed cumulative sum, but another product uses a
same-named field from catalog totals. No universal semantic equivalence follows.
Native feature SRS is custom100000, not a coexisting4326 metadata entry. Climate flags
are not source burn-date QA, and reconstructed dates are not availability evidence.
Dataset-specific rights remain unresolved; paper/code licenses are not dataset licenses.

Add digest-bound source/recipe/scope/review records and pure validators, not a source
adapter or row reader before approval. Missing scientific evidence is NEEDS_EVIDENCE;
a human decision and current container verification remain distinct from structural
validity and confer no runtime permission in this checker. Scope the initial proposed
audit to512 total logical decoded rows/16 fires/batch128, without geometry, full scan,
training, raw/harmonized persistence or redistribution. Whole-table Parquet row groups
are not a bounded sample. Physical page/I/O constraints require later adapter review.

Prospective claims still require actual issue-time availability. Never assign real
rows synthetic midnight availability or silently relabel retrospective reconstruction
as operational forecasting. Propose only a retrospective native-value audit now;
subsequent scientific cohort/training and public release are separate decisions.
Keep historical aggregate selection findings distinct from new cohort measurements.
No empirical real outcome, new synthetic benchmark or larger model was produced.

## 2026-11-21 — Full-lake scope without implicit real-data permission

M7 uses all task-eligible fires with bounded batches/windows rather than importing
the M6 preliminary 512-row audit cap. Metadata inventory, scoped digest-bound review
and generated numerical validation are separate artifacts. Native evidence survives
projected streaming; missing labels use per-head support rather than global exclusion.
Scientific effect sizes and binding/geometry/environment definitions remain external
review inputs. The CLI profiles approved streams; offline kernels are not a claim of
a finished full-lake training runner. Historical M1–6 evidence remains unchanged.

## 2026-11-21 — M7.2 intent and historical population arithmetic

Recorded the supplied investigator intent without fabricating an authenticated
receipt or passing unresolved rights/binding reviews. Publication and model-training
thresholds are not requirements for internal native profiling. The prescribed
review mechanism remains unresolved. Completed independent stat/document checks
and historical aggregate reanalysis. Historical 3.68% eligibility requires the
entire retained history to be consecutive; it does not estimate occurrence of
local runs in gappy histories. Existing aggregate histograms permit subset window
arithmetic, explicitly separated from current-source profiling and independent
fire counts. No upstream or frozen M1–7 artifact was modified.

## 2026-11-21 — Execute native census using direct investigator authorization

The user explicitly instructed execution after granting project approvals. This
supersedes the separate external-receipt requirement for internal read-only native
profiling; it does not fabricate domain PASS findings, source rights or external
review identities. Existing M1–7 contracts/artifacts remain historical and unchanged.
Added a separately named native census operation with fresh source verification,
SQLite in-memory source sorting, bounded streams/per-fire buffers, compact metadata
indexes, stage restart and independent replay. Source daily IDs outside the event
catalog remain distinct with unknown strata. Local-run and strict-history populations
are separate; overlapping windows are not independent fires. Candidate splits use
a split-specific hash namespace separate from nested training-fraction hashes.
Arrow schema survival across all-null batches has a regression check. Raw daily
values/tensors are not persisted, internal source-linked indexes are ignored by Git,
and no models or external release are part of this execution.

## 2026-11-21 — Full observed population is the primary benchmark

The investigator corrected the study emphasis: most fires have short observed
histories. The benchmark now includes all native IDs in1,2,3+ strata, using
observable-property preservation, retrieval and access/reuse as primary tasks.
Long-run prediction remains a selected-cohort extension rather than the sampling
gate. New short-state code preserves original values/dates/gaps without changing
the historical TCN architecture or claiming learned-model results. One-point
allocation shape is not applicable; normalized positive payloads are constant[1].
Keep source-ID/date/checksum sidecars and explicit paid fallback when evaluating
answerability. Equal-fire weighting and per-stratum coverage replace window-based
population claims; query workload weights remain a separate empirical question.
Frozen milestones/census and source files remain unchanged.

Short-prefix depth1/2 eligibility is now counted independently from native runs;
depth1/horizon1 windows match all native exact-day transitions. The earlier
minimum-three TCN is an implementation restriction, not a scientific eligibility
rule; no encoder was changed or trained.

## 2026-11-21 — Execute full-population scientific-state utility

Use all native IDs with task-specific support, and encode validated fixed
observed-property state rather than silently presenting it as raw-sequence
learning. Keep native exact operations as the primary reference. Separate
coordinate geometry, trained-head recovery, common metadata and paid fallback.
Retain scalar-target overlap as an explicit scope limitation; do not equate
state autoencoding with scientific discovery. Report negative scalar-query
economics and modest secondary prediction equally. Preserve corrected invalid
probe outputs privately, refit all affected heads and retain unchanged encoder
weights under verified identities. Scientific/source rights uncertainty remains
separate from direct investigator authorization for internal execution.
