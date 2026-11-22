# Scientific and software governance

## Operating contract

- The local management workbench indexes scientific artifacts; registration and
  feedback never grant scientific approval, execute jobs or clear existing vetoes.
  Keep controlled exports/backups separate from the public catalog; resource plans
  are not awards, local recovery is not a remote deposit, and metadata scale probes
  are not global raster/encoder throughput. Preserve raw/harmonized streaming limits.

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

## VERDE model trust and deterministic execution

1. VERDE models are not trusted computational authorities. They interpret, select,
   parameterize, compare, rank, propose, explain and request review.
2. Runtime scientific code, mathematical formulas, algorithms, SQL, scripts,
   executable templates and scientific numerical results must never originate from
   model output. Never pass model content to eval, exec, shell execution, dynamic
   imports or equivalent expression/code evaluators.
3. Every executable scientific operation is pre-written, reviewed, tested, versioned
   and registered before runtime. Unknown operation IDs fail closed; never ask a
   runtime model to implement them.
4. Models select only registered, caller-offered capabilities and modify only
   schema-permitted parameters. Validate structures, identifiers, parameters,
   dependencies and scientific preconditions independently before execution.
5. Model-generated numbers are MODEL_JUDGMENT, never authoritative constants.
   Deterministic code owns conversion factors and formulas. Prefer source-metadata
   references to model transcription of coefficients; missing evidence is not guessed.
6. Keep SELECT, PARAMETERIZE and PROPOSE contracts separate. Semantic proposals
   preserve source meanings and supplied candidate IDs; they cannot approve themselves.
7. Keep structural validity separate from scientific validity. Scientific ambiguity,
   uncertain meaning/rights, novel concepts and cross-support changes need evidence
   and explicit human decisions. Existing model vetoes remain binding.
8. Consensus is deterministic aggregation of structured findings. QA may recommend
   registered checks or veto; it cannot calculate scientific results, rewrite
   validators, override findings or grant execution permission.
9. Approved recipes execute without an LLM. Offline fixture-model orchestration
   remains explicit and never substitutes silently for unavailable real services.
10. Record recipe/registry/operation/validator/constants identities, authoritative
    parameter sources, model/prompt provenance and exact-recipe human decisions.
    Distinguish MODEL_PROPOSED, DETERMINISTICALLY_VALIDATED and HUMAN_APPROVED evidence.
    A changed scientific implementation requires renewed review and fresh products.
11. Preserve bounded real-data streaming directly through harmonization into MOSAIKS.
    The fixture decision controller is not a replacement for real streaming gates.
12. Agents propose. Deterministic software executes. Humans remain responsible for
    scientific decisions that available evidence cannot safely resolve.

## CubeDynamics execution backend

- CubeDynamics is an external ESIIL scientific execution dependency, accessed through
  an adapter. Never vendor or copy its implementation into this repository.
- VERDE must not write CubeDynamics Python, call arbitrary functions, provide an
  apply callable or invoke a Python interpreter. Only registered capabilities and
  schema-permitted reference/enumeration parameters are available to runtime models.
- Inspect and pin the actual upstream package/API before adding capabilities.
  Every exposed operation requires independent offline tests with the real package.
- Computational feasibility does not establish scientific validity. Semantic mapping,
  ontology/taxon/trait equivalence, scientific comparability and rights stay in
  harmonization/review, not CubeDynamics.
- Resolution, support and extent are distinct. Aggregation changes support and must
  record source/target support, method, evidence and justification. Reprojection is
  not resampling; nearest sampling is not an area mean. Do not infer temporal cadence
  from the duration of one aggregate observation.
- Quality masking and calibration are distinct scientific operations. Preserve source
  identifiers, native metadata, coordinate support, quality evidence and units.
- Prefer lazy graphs and bounded upstream windows. Materialization intent, size/task
  guards and checksum scope must be explicit; never silently load or persist a full
  source dataset. Tests use generated in-memory arrays/iterators, not data downloads.
- Every backend stage emits typed transformation provenance including upstream
  version and relevant dependency versions. A plan is not an executed data read.
- Approved backend recipes execute with inference off. Preserve existing consensus,
  evidence-review, QA, human and MOSAIKS gates. New layouts/support changes require
  matching new scientific and encoder review; no automatic promotion into embeddings.
- Module 1 owns source discovery/access; do not repeat CubeDynamics loader discovery
  or duplicate MESA infrastructure inside the adapter. Core semantic/review functions
  must remain usable without the optional CubeDynamics dependency.

## Scientific validation experiments

- Keep benchmark scores, exact term presence, source facts, model judgments and
  expert gold decisions separate. Assistant-authored reference answers are drafts,
  never a human gold standard. Unknown fields must not become zero or absence.
- Resource combination coverage describes the declared requirement rubric, not
  scientific expressibility or equivalence. Class count/depth and metadata presence
  are not quality or compatibility scores. Record mixed candidate-inventory scopes.
- Model experiment arms remain inert. Preserve exact schemas/prompts, normalized
  responses, failures and evaluation identities; deterministic re-evaluations are
  not extra model samples. Enforced zero execution is not model competence.
- Preserve historical Sentinel vetoes and findings unchanged. Issue adjudication
  forms are not runtime HumanDecision objects or execution permission.
- Public site coordinates do not identify actual sensor support. Do not promote an
  exact-support join or grid alignment into a tower-to-pixel scientific association.
  A genuinely new association method needs expert definition before implementation.

## Fire VASE representation-utility benchmark

- Keep the deterministic benchmark explicitly synthetic until real source rights,
  cumulative/ring semantics, support and availability are reviewed. Reuse the pinned,
  hash-verified external operation file through the isolated closed worker; never
  vendor it or expose arbitrary scientific code execution.
- Evaluate the complete supplied interface, including retained provenance metadata.
  A normalized payload can lose size/date information while its source-ID sidecar
  still supports a validated consecutive-sequence count. Keep answerability,
  correctness, geometric fidelity, scientific relevance and cost distinct.
- M0/M1/M2 may change evidence, never data, executable capabilities or budgets.
  Deterministic metadata invariance is an isolation test, not metadata efficacy.

- Controlled Fire VASE agent actions are inert JSON proposals. Only the synthetic
  deterministic controller may invoke the registered fixture operations. Keep
  task IDs, references, answerability and grading metadata out of model prompts;
  use condition-invariant sanitized feedback and evidence-referenced numerical
  answers. Preserve malformed proposals and recovery attempts without repairs.
- Mock/rule-provider results establish protocol behavior, never LLM capability or
  metadata efficacy. Real calls need verified runtime identity, access and cost
  bounds; unavailable usage stays unknown. Do not relabel public development cases
  as genuinely held out or overwrite historical benchmark/audit outputs.

- Expanded Fire VASE evaluation cases are frozen/model-unseen, not independently
  blinded to implementers. Keep draft evidence-claim rubrics separate from expert
  gold. Public timing hints use development cases only; evaluation sufficiency,
  numerical references and measured Pareto minima remain private to grading.
- Compare targeted and cached R0 against prepared R1/R2, charging preparation and
  routing explicitly. Backprojected PC geometry is not full-profile equality;
  coordinates alone cannot certify discarded residuals. Preserve historical runs.

- Fire VASE learned-prefix experiments stay isolated from completed-history VASE
  and production MOSAIKS. Fit preprocessing/encoders/PCA/heads on training fires
  only; group all prefixes of a fire and separate model selection from calibration.
  Future observations are outcomes, never encoder inputs. Synthetic predictive
  controls do not establish real-fire science or operational availability.
- Physical legacy data availability is separate from reviewed rights/support/access.
  Materialization compares the identical trained model/head against on-demand and
  cached complete/direct predictions, preserving source/preprocessing/checkpoint
  identities and unmeasured lifecycle costs. No runtime agent may train or author code.

- Fire VASE transfer studies must distinguish frozen A-only downstream heads from
  additional multitask/task-specific supervision. Preserve source/checkpoint and
  full prefix support/availability identities; all prefixes of a fire remain grouped.
  Future-outcome retrieval relevance is not ecological relevance and must exclude
  same-fire candidates. Failed linear probes do not prove information absence.
- Report every predeclared task, paired fire summaries and current/historical training
  separately. Heterogeneous head reuse is distinct from identical complete-bundle
  caching; source/model/head changes invalidate affected products. No universal
  scientific or lifecycle boundary from the synthetic convenience cohort.

- M6 real-source work must use the identified packaged Fire VASE lake rather than
  infer missing data from absent root cache paths. Metadata presence/sizes/reported
  hashes are not fresh data-byte verification or permission. No observation rows
  before required human review; paper/code licenses do not relicense datasets.
- Real-study review packets bind source/recipe/claim/scope digests. Pure precondition
  validation cannot authenticate human authorship, approve science or execute reads.
  Keep retrospective reconstruction distinct from operationally available prefixes;
  never fabricate real availability timestamps to satisfy synthetic contracts.

- M7 full-lake scope does not grant access. Keep current hashes, exact reviewed
  bindings and externally verified scope receipts separate; no real rows before
  authorization. Full-lake population has no 512-row cap after broader approval.
- Keep generated kernel checks separate from real sample sizes/results. Unknown
  geometry/environment criteria, scientific thresholds and task labels remain
  review inputs; callable kernels do not establish completed full-lake execution.

- Later direct investigator instructions authorize internal read-only native Fire VASE
  profiling without a separate external receipt. Preserve those exact instructions
  and historical review records; never fabricate external verification or PASS findings.
  Keep native support diagnostics separate from scientific equivalence, quality,
  operational forecasting, model execution and external redistribution. Compact
  source-linked census indexes remain internal and outside the public catalog.

- Current Fire VASE utility benchmark treats all native fire IDs as primary, with
  separate1,2 and3+ observation strata. Long-run prediction is a selected-cohort
  extension. Never infer physical lifetime/extinction from observed record count,
  turn one-observation shape into a flat history, or exclude gappy pairs from
  otherwise supported observed-property tasks. Preserve complete interface lineage
  and charge explicit source fallback; normalization loss is payload-specific.

## Fire VASE Milestone8 interpretation

- Milestone8 is an executed real observed-scientific-state experiment: ten scalar
  properties plus mathematical support masks, not a native sequence/polygon encoder.
- Preserve exact native/interpretable controls, numerical PCA inverse, approximate
  learned recovery, common sidecar evidence and charged native fallback as distinct.
- Do not mix archived invalid uncentered-probe outputs with corrected final tables.
  Undefined scientific labels remain NA even when model input is median-filled.
- Local warm-batch cost and conditional single-seed uncertainty do not establish
  production economics, ecological analogy or universal embedding utility.
