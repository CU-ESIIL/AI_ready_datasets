# Architectural decisions and repository audit

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
