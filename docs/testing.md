# Testing

Run `python -m pytest -q` from the checkout. Tests use project-authored synthetic
fixtures; no internet, MESA credentials, OpenClaw, or commercial LLM access is
required. Tests block socket connections to enforce this boundary. CI installs
dependencies, then runs tests and a strict MkDocs build. The expanded offline suite includes native-boundary and model-transport tests;
live verification is separate from CI and is described in the real-data guide.

Discovery tests cover spatial/temporal/modality/variable filtering, metadata,
source versions, rights, deterministic ordering, duplicate/conflicting sources,
missing/unavailable resources, checksum integrity, immutable contracts, and
unavailable external interfaces.

Harmonization tests cover exact and unknown meaning, abstention, positive and
negative conversions, variable mapping, missing values/filtering, validation,
recipe schema, QA approval/rejection, low confidence, novel/disputed mappings,
rights review, bound human decisions, core/track separation, original values,
daily coverage/overlap, spatial matching, joins, CRS bounds and lineage.

Representation tests cover batch and generator inputs, known fixture vectors,
dimensions, missing values, malformed inputs, encoder identities/versions,
preprocessing, multiple encoders, source lineage and JSON-LD export.

Integration/track tests cross all three contracts for both food and water,
assert modality-specific products, parent core lineage, licensing and nonempty
artifacts, verify shared cache identity, compare repeat-run bytes, preserve other
track outputs/configuration, exercise CLI/schema export, and add a synthetic third
track through configuration only.

Remaining gaps: authenticated NEON normalization, live MESA and full OpenClaw working-group scheduling, large input
streaming, authenticated reviewer identity, scientific uncertainty propagation,
real raster preprocessing/cloud masks, and scientifically validated domain models.
No test claims ecological validity or predictive performance from synthetic values.

Real-boundary tests mock HTTP and raster readers explicitly. They check native
STAC preservation, instantaneous timestamps, DN/calibration separation, cloud
rejection, checksummed snapshots, unsafe raster locations, NEON token handling
and file bounds, model JSON-schema requests, model identity/transcripts, malformed
and truncated outputs, missing-model failures, identifier protection, mandatory
human review, and model QA veto/staleness. They do not claim live integration
merely because a transport was mocked.

OpenClaw adapter tests run without Docker or provider credentials. They verify
version-matched policy configuration, credential-file parsing without shell
execution, loopback routing, actual `/tools/invoke` envelope/model qualification,
provider/model substitution failures, no-fallback errors, normalized-response
provenance and policy-drift rejection. Live runtime testing is separate from CI.

## Metadata consensus and direct streaming

The [streaming harmonization module](streaming-harmonization.md) adds metadata-only specialist
dialogue, digest-bound unanimous review, documented Sentinel-2 scale/offset
calibration, and bounded window-to-encoder execution without raw or harmonized
data files. The existing fixture/snapshot commands retain their historical
materialization behavior. Current streamed vectors are reference numeric features;
model consensus still requires an actual human decision before execution.

## MOSAIKS over harmonized outputs

The [MOSAIKS module](mosaiks-embeddings.md) consumes bounded harmonized raster tiles,
freezes train-only empirical convolution filters, writes dense feature datasets
with scientific lineage, and verifies held-out ridge-model consumption against
baselines. It does not encode raw source assets. Generated diagnostics exercise
the complete mechanism; independent scientific validation and real-data review
remain separate requirements.

## Scoped review and documentation checks

`tests/test_review.py` checks citation ownership, stale scientific recipe bindings,
missing evidence versus failure, duplicate findings, unknown QA references, and
same-recipe role calls. An offline fake transport exercises checkpointed failures;
it is explicitly a test fixture and never a live fallback. Generated DN values also
verify that documented negative reflectance survives calibration unchanged.

Regenerate source-derived reference and figures before checking documentation:

```sh
python scripts/generate_figures.py
python scripts/generate_reference.py
mkdocs build --strict
python scripts/check_site.py site
```

The site checker validates local HTML links, fragments, images and generated assets.
Browser checks additionally inspect desktop/mobile layout, navigation, focus and
reduced-motion behavior. No linter or type-checker configuration currently exists;
these checks do not imply that one was run.

## Semantic discovery and diagnostic benchmark

`test_semantic_discovery.py` covers complete/partial/invalid evidence, serialization,
source/model distinctions, multiple semantic systems, immutable original metadata,
stale bindings, candidate retrieval bases, explicit resolver failures and the
Module 1/Module 2 authority boundary. Generated Sentinel metadata verifies B08,
scale/offset, stored DN versus calibrated unit, native CRS and instantaneous support
without reading pixels or approving a recipe.

`test_semantic_benchmark.py` checks inventory breadth, typed coverage and assessment
records, deterministic diagnostics, bounds, namespace-reference limits, source
identities, genuine Parquet round trips and file hashes, including zero-row schemas.
Rankings and portfolio suggestions are never tests of biological equivalence.

```sh
python scripts/generate_semantics.py
python scripts/generate_reference.py
python scripts/generate_figures.py
pytest -q
mkdocs build --strict
python scripts/check_site.py site
```

## Model trust tests

`tests/test_operation_registry.py` exercises all ten registered dispatches with
generated in-memory inputs, output/lineage assertions and invalid parameters. It
also covers arbitrary code/languages, invented operations/constants, malformed JSON,
scientifically incompatible parameters, stale source/implementation identity,
unknown ontology candidates, safe abstention, mandatory human review, no-model
execution, fixture-model orchestration and timeout behavior without fallback.
The full suite passes 175 tests at this hardening checkpoint. Historical audit test
counts remain historical. [Audit](development/model-trust-audit.md).
