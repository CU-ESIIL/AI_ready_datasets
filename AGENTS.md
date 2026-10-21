# Scientific and software governance

## Operating contract

- Treat this repository as the source of truth and the website as its rendered view.
- Inspect existing structure before editing. Prefer small, additive, traceable changes;
  preserve useful infrastructure and history. Do not destructively rewrite without authorization.
- Keep package code in `src/`, tests in `tests/`, fixtures in `data/fixtures/`, track
  configuration in `tracks/`, and project-level website documentation in `docs/`.
- Keep README, website, examples, status, tests, and these instructions synchronized.
  Record meaningful scientific, structural, integration, and design decisions in the
  changelog and `docs/development/decisions.md`. Keep the website simple and readable.

## Scientific integrity

1. Agents propose. Deterministic code executes.
2. Never invent scientific equivalences or infer compatibility from source names.
3. Similar variable names do not establish semantic equivalence.
4. Preserve original source observations, identifiers, versions, and metadata.
5. Never silently change units, CRS, spatial support, temporal support, biological
   meaning, taxonomic identity, methods, or measurement definitions.
6. Every scientific transformation belongs in a validated, versioned recipe.
7. Every derived product retains source, recipe, transformation, agent, QA, and
   applicable human-decision provenance; representations retain observation lineage.
8. Distinguish source/observed data, harmonized data, derived data, and AI-generated
   representations. Scientific harmonization is separate from model preprocessing.
9. Abstain rather than infer unsupported meaning. Unknown mappings need explicit revision.
10. Human review is required for consequential/uncertain decisions, novel equivalence,
    low confidence, agent disagreement, support changes, ambiguous meaning and rights.
11. Public accessibility does not imply redistribution permission.
12. Preserve source-specific licenses, attribution, derivative/redistribution permissions,
    access restrictions, sensor and platform identity. Flag unclear rights for review.
13. Do not create a universal biological ontology or claim a universal latent space.
    Distinguish observation modality from spatial/temporal scale.

## Integration and execution

- Never invent MESA endpoints or tool signatures. Verify current official documentation
  and deployed tool schemas. Explicitly distinguish real, mocked, and planned integrations.
- Do not unnecessarily duplicate MESA discovery/access/metadata functionality.
- STAC is a spatiotemporal metadata/catalog standard, not the whole infrastructure.
  Do not call the entire discovery/harmonization/representation architecture a registry.
- Never execute arbitrary LLM-generated transformation code. Extend only allow-listed
  deterministic operations with explicit validation and positive/negative tests.
- Keep the orchestrator thin and the discovery, harmonization, and representation
  modules independently callable through validated typed contracts.
- Keep OpenClaw as an adapter/runtime boundary, not a copied framework.
- Do not claim a source is integrated because a fixture exists. Real integration
  requires actual retrieval and processing, with its limitations documented.

## Science tracks and shared data

- Do not duplicate core pipeline code for science tracks.
- Track-specific assumptions must not leak into core harmonization or other tracks.
  Promotion to shared scientific rules requires explicit scientific review.
- One track must never modify another track's configurations, recipes, cache entries,
  or products. Track-specific products carry track provenance.
- Shared source resources and canonical observations are immutable. Track operations
  produce new products; shared sources do not imply shared interpretation.
- Account for source/version/checksum, recipe, executor, and encoder/preprocessing
  identity in derived-product caching. Never reuse stale products under new identities.
- Food and water security use configuration and reviewed rules, not copied pipelines.
  Keep third-track assumptions undefined until a scientist supplies them.

## Data policy

- Prefer open and FAIR data and streaming/windowed/lazy access where feasible.
  Consider standards-based discovery and appropriate scientific geospatial tools.
- Do not silently ingest external data. Document source, access method, format,
  version, license, permissions, attribution, and citation before use.
- Consider copyright, privacy, Indigenous data sovereignty, and source restrictions.
- Never download or commit large source datasets or redistribute without permission.
  Prefer tiny deterministic, explicitly synthetic, redistributable fixtures for CI.

## Tests and documentation

- New modules require independent unit tests. New transformations require positive
  and deliberately invalid tests. Interface changes require contract/integration tests.
- Test review gates, scientific metadata survival, original values, lineage, rights,
  determinism, shared-data reuse, and track independence. Tests must work offline.
- Do not invent domain-specific expected behavior when the science is unclear;
  document gaps instead of claiming coverage or ecological validity.
- Scientific behavior changes require documentation/status updates. Run the full
  relevant test suite and strict MkDocs build; fix broken links, warnings and stale claims.
- Preserve the existing Material/Pages setup. Inspect changes to manual template-sync
  workflows carefully: they can overwrite project-specific work.

## Live data and model-backed roles

- Keep offline fixture runs and live acquisition/inference explicit. Never silently
  fall back from unavailable real services or invalid model output to mocks.
- Preserve native STAC Items, collection/license evidence, sensor/platform identity,
  processing baseline, native CRS/pixel indices, quality masks, and calibration metadata.
  Raw digital numbers are not calibrated reflectance. Do not apply scaling in an adapter.
- Instantaneous acquisitions may have equal start/end times; never invent a duration
  to satisfy a schema. Zero-duration source records require explicit instantaneous support.
- State checksum scope. Extracted-window evidence checksums do not cover complete remote rasters.
- Tokens come from process environment and must never be logged or committed. Do not
  forward NEON credentials to cloud download hosts. Current NEON downloads require
  authentication; preserve current source-specific CC BY 4.0 attribution requirements.
- Model roles have no tools or execution permissions. Deterministic code fixes source
  identifiers and targets; models return scientific judgments and allow-listed plans.
- Preserve exact prompts, schemas/version, model digest, outputs, timestamps and usage.
  Reject malformed/truncated output; never silently repair or fabricate a response.
- Model proposals always need human review. Honor model QA rejection/revision as a
  veto, bind it to scientific recipe content, and invalidate it after scientific edits.
- A model's rejection may be scientifically mistaken. Preserve it for expert analysis;
  do not force an approval or claim a rejected proposal produced validated science.

## OpenClaw and Verde runtime

- Inspect installed OpenClaw version/plugin contracts before changes. The current
  adapter deliberately targets 2026.5.18; do not assume latest documentation matches.
- Keep the prototype gateway isolated from working-group roles and Slack. Allow
  only JSON-only task inference, with no model tools, fallback models or heartbeat.
- For slash-containing Verde model IDs, use a fully provider-qualified route and
  verify the actual returned provider/model. Reject substitutions.
- The task plugin normalizes JSON and may remove code fences. Record response scope
  accurately; do not label it raw provider text or invent token counts/weight hashes.
- Never print Docker environment/configuration secrets. Preserve runtime policy
  digests/history and keep generated credential state under ignored private outputs.

## Streaming harmonization

- New real-data harmonization paths must stream bounded windows directly into encoders; do not persist raw/harmonized datasets, including test downloads. Use offline generated iterators for tests.
- Keep metadata consensus separate from source access. All four specialists and QA must review the same frozen recipe; disagreement blocks streaming. Human review remains mandatory for model proposals.
- Metadata checksums are not data checksums. Preserve per-window evidence hashes and native support in compact lineage without serializing raw observations.
- Legacy snapshot/fixture paths remain explicit historical workflows, not the streaming implementation.

## MOSAIKS representations

- MOSAIKS accepts harmonized raster outputs only; keep source reads and calibration upstream. Do not substitute generic encoders or unrelated precomputed MOSAIKS vectors.
- Fit empirical filters on a bounded training-only reference stream; never use validation/test tiles for filters or normalization.
- Preserve canonical definitions/units and source/recipe/review lineage in model and dataset identities. Raster layout and encoder settings need matching fresh consensus.
- Verification must check integrity, geographic/split leakage and held-out downstream performance with baselines. Label derived diagnostics honestly; they do not establish independent scientific validity or native LLM understanding.

## Review jurisdictions and documentation synchronization

- Keep semantic, units/calibration, support, rights, integrity and quality review
  jurisdictions explicit. QA synthesizes existing finding IDs and cannot add new
  specialist claims. Evidence citations must stay within their owning domain.
- Use PASS, FAIL, NEEDS_EVIDENCE and NOT_APPLICABLE for scientific review; keep
  workflow eligibility and human approval separate. Missing evidence is not failure.
- Bind every review to the frozen scientific recipe digest. A new report cannot
  erase an existing model veto or authorize execution. Preserve malformed model
  responses and failed runs; do not silently repair findings or fall back to mocks.
- Distinguish calibrated, quality-filtered calibrated and analysis-ready product
  claims. Dimensionless unit 1 is valid. Never infer clipping or rejection solely
  from an unusual calibrated reflectance value.
- Keep evidence curation explicit. Statement digests and domain ownership do not
  prove natural-language truth, legal interpretation or independent scientific validity.
- Maintain the narrative Home/Approach/Data/Science/Impact pages and technical
  Documentation hierarchy in MkDocs Material. Regenerate figures and reference with
  scripts/generate_figures.py and scripts/generate_reference.py after relevant edits.
  Document image rights/credits; preserve Pages deployment and readable Markdown.

## Semantic discovery and mapping governance

1. Identical labels do not establish equivalent concepts; different labels do not establish different concepts.
2. Prefer persistent ontology identifiers over text matching, and preserve source-native identifiers and definitions.
3. Preserve the semantic resource/version and evidence location supplying each concept. Never silently replace a source ontology with a preferred one.
4. Mapping is not replacement. Crosswalks must preserve source identifiers and document direction, uncertainty and potential loss.
5. Unit equivalence does not establish variable equivalence. Taxonomic equivalence does not establish ecological equivalence.
6. Spatial overlap does not establish comparable spatial support. Matching timestamps do not establish comparable temporal support.
7. Broader, subclass, part-of and member-of are not interchangeable relations.
8. Organism, taxon, population and community are distinct. Trait, variable and measurement are distinct. Observation and measurement are distinct.
9. Location, resolution, support, footprint and extent are distinct. Biological organization is not one universal spatial or taxonomic scale.
10. Module 1 discovers source semantic evidence and optional candidates; it must never approve equivalence. Module 2 proposes mappings and harmonization.
11. Keep source-documented, observed, deterministically derived, model-judgment, human-decision and missing evidence distinct. Never promote a model hint into source metadata.
12. Human review governs consequential/uncertain mappings, novel equivalence, disagreement and support changes. Candidate confidence is not execution permission.
13. Reuse or compose existing community resources where appropriate. Project-specific concepts are a last resort and require documented alternatives, evidence, reviewer and date.
14. Every new semantic mapping requires tests; every semantic transformation remains traceable to source evidence and a validated versioned recipe.
15. Maintain the canonical landscape inventory and separately auditable project assessments. Unknown dates, rights, identity, crosswalks and coverage must remain explicit.
16. Coverage, overlap, rankings and portfolio recommendations are project metadata diagnostics, not external ontology facts or scientific compatibility evidence. No benchmark output can authorize mapping or execution.
17. Keep ontology-service access behind explicit adapters. Do not download ontology graphs or data silently; preserve offline generated tests and streaming constraints.
18. Regenerate semantics tables with scripts/generate_semantics.py and synchronize schemas, diagrams, README, website, status and decisions after semantic interface changes.

## Documentation and benchmark interpretation

- Any architectural change affecting a contract, semantic relationship, evidence
  model, transformation, or module boundary must update the relevant documentation
  and architecture diagram in the same change.
- Preserve two reader layers: a scientific public narrative and linked Markdown-first
  technical proof. Keep capability labels WORKING, PROTOTYPE, MOCKED, PLANNED and
  UNDER ANALYSIS consistent across both.
- Explicit ontology use, ontology potential and semantic diversity are different
  assessment dimensions. Ontology leverage is a multidimensional profile until an
  evidence-reviewed scoring model exists. Metadata presence is not semantic completeness.
- Conceptual figures and proposed observation/pair benchmarks must not be presented
  as measured results, selected flagship datasets or approved scientific mappings.
