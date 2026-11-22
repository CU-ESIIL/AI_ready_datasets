# Complete offline example

Question: how does synthetic satellite reflectance covary with synthetic
field-observed vegetation height? This is an architectural demonstration inspired
by the intended NEON + satellite vertical slice.

`data/fixtures/` contains three project-authored field records and three satellite
records. Coordinates, daily intervals, and support are deliberately aligned.
Values are invented, not actual NEON measurements or Sentinel pixels. The satellite
fixture preserves platform/sensor identity and a STAC metadata version but is not
a complete STAC Item or raster.

```bash
prototype run --all-tracks --output run/demo
```

1. Track configuration becomes a typed scientific request.
2. Discovery finds fixture assets by extent, interval, modality, and variable.
3. Access verifies checksums and returns original immutable records.
4. The semantic role compares each variable to its explicit curated target.
5. The harmonization role proposes core validation operations.
6. QA approves supported identity mappings; no human review is fabricated.
7. Deterministic code emits shared canonical observations.
8. Track selection recipes retain canonical parents in separate track products.
9. Encoders yield separate field and satellite vectors.
10. JSON-LD and run manifests preserve source, license, recipe, proposal, and decisions.
11. A descriptive Pearson correlation compares exactly coincident synthetic pairs.

The last step is a downstream software smoke demonstration, not evidence that
reflectance predicts canopy height or any food/water outcome. No predictive model
is evaluated. Actual field-to-pixel support alignment, cloud masks, seasonal
matching, access rights, and source metadata require real-data scientific review.

Each track directory contains `request.json`, `sources.json`,
`proposed_recipe.json`, `qa_report.json`, `review.json`, `approved_recipe.json`,
`harmonized.json`, `representations.json`, `provenance.jsonld`, `downstream.json`,
and `run_manifest.json`. Recipe files contain `core` and `track` artifacts; extract
one standalone object for the `qa` or `review` commands. The manifest stores the
full track configuration, source/recipe-aware cache keys, executor/prototype
versions, and content digests for every result artifact. Retain the source
checkout and dependency environment to reproduce results.

Inspect the three modules independently using the APIs on the discovery,
harmonization, and representation pages. CI uses only these local fixtures.

For actual observations and real model calls, use the separate
[real-data and agents workflow](real-data-agents.md). The commands above remain
an offline deterministic regression example.

## Bounded model decisions, without live inference

```sh
prototype operation-demo --output run/operation-trust-example
prototype operation-capabilities --output run/operation-capabilities.json
```

The explicit fixture model selects a registered metres-to-centimetres conversion.
Deterministic code converts a generated 2 m value to 200 cm. A synthetic human
decision exercises the gate; it is not real scientific approval. No source records
are fetched and raw/harmonized datasets are not persisted. The output includes a
rejected `spectral.magic_correction` selection and an ambiguous concept proposal
returning `NEEDS_HUMAN_REVIEW`. See the [complete trust-boundary example](architecture/model-trust.md#execute-with-verde-off).

## Real CubeDynamics, generated data

```sh
# Python 3.12; real external dependency, generated data and fixture review only.
python -m pip install -e '.[dev,cubedynamics]'
prototype cubedynamics-demo --output run/cubedynamics-example
```

Generated Sentinel-like DN → reviewed scale/offset harmonization → CubeDynamics
selection/subset/calendar operations → training-only MOSAIKS → vectors and lineage.
`fixture-model-selection.json` records what the fixture model selected. Backend
transformation records describe what deterministic software executed. The additional
generated alignment example uses two source identities and DataArray/Dataset inputs;
it records nearest sampling and support changes, not scientific equivalence.
No real raster or raw/harmonized dataset is downloaded or persisted.
[Details and limitations](cubedynamics.md).

## Scientific validation example

See the [NIWO air-temperature and Sentinel context proposal](validation/neon-sentinel.md)
for an evidence-backed but blocked cross-source case. Rebuild its diagnostics with
`python reports/scientific_validation/analyze.py` using the documented retained
inputs, then rebuild the separate report. This example does not acquire observations,
create equivalence, implement a new operation or bypass review.

## Fire VASE representation utility

The separate [synthetic benchmark example](analysis/fire-vase-benchmark.md) compares
R0/R1/R2 against independent answers and measures preparation/query/cache costs.
It uses an explicitly pinned external operation file in an isolated worker. No real
fire archive, runtime model calls or production execution permissions are involved.

The [controlled-agent mock example](analysis/fire-vase-agents.md) executes the full
348-cell experiment without credentials. Use its frozen config and a fresh run
directory; real-provider selection requires separately verified access and cost
permission and never falls back silently to a mock.

The [expanded Fire VASE pilot](analysis/fire-vase-pilot.md) documents the V3 synthetic
command, frozen cases, optimized/cached rivals and disabled live branch. Use a new
output directory; existing milestone results must not be overwritten.

The [prefix learning example](analysis/fire-vase-learning.md#reproduce) runs the
frozen synthetic future-observation objective without an LLM or real data. It saves
checkpoints, held-out predictions and matched materialization/caching costs to a new
output directory. Real-source approval and Track A inference remain separate.

The [task-transfer example](analysis/fire-vase-transfer.md#reproduce) freezes the M4
checkpoint and evaluates new scientific outcome heads, multitask/specific training,
future-pattern retrieval and heterogeneous task reuse. Use a new output directory;
training and table/figure regeneration are separate commands.

The [real-source review guide](analysis/fire-vase-real-data.md) links the metadata-only
inventory, proposed scientific contract and bounded human-review packet. It intentionally
provides no observation-ingestion/model command before approval. Metadata regeneration
uses `scripts/prepare_fire_vase_real_review.py` with a new output directory.

## Explicit full-lake offline validation

Install the `fire-vase-lake` extra for optional metadata/model dependencies. Use a
fresh private output directory:

```sh
PYTHONPATH=src python -m dataset_prototype.embedding_study.lake_experiment --dry-validate --output /tmp/fire-lake-generated-check
```

This generates software fixtures only; it is never a fallback for failed real
execution. The real CLI currently profiles approved streams, not a complete training
study. See [full-lake protocol/status](analysis/fire-vase-full-lake.md).

## Native census after direct investigator authorization

The dedicated native profiling entrypoint is
`python -m dataset_prototype.embedding_study.population_profile --lake CANONICAL_LAKE --output PRIVATE_OUTPUT`.
It requires the real direct-instruction record and current source verification
records in that output directory; tests cannot supply scientific/publication approval.
Use `scripts/report_fire_vase_population.py --results PRIVATE_OUTPUT` to derive cohort
matrices, candidate whole-fire splits and nine figure families from measured metadata.
See [scope and provenance](analysis/fire-vase-population.md).

## Full-population short-history audit

Use a fresh internal output directory. With the existing native source verification
and census, run `scripts/audit_fire_vase_short_histories.py --census CENSUS_OUTPUT
--lake CANONICAL_LAKE --output FRESH_PRIVATE_OUTPUT` under `PYTHONPATH=src`.
The script streams source values but persists aggregate diagnostics only. It fits
no models. Its fixed first64-per-stratum access sample is not a latency survey.
See [current benchmark scope](analysis/fire-vase-full-population.md).

## Reproduce measured Fire VASE utility

The executed command sequence is retained in
`reports/embedding_utility/fire_vase/milestone-8/reproducibility.md`. It uses the
existing local lake and frozen census, without downloading observations. Use a
fresh versioned output after copying the design plans; preserve historical
outputs. [Findings and limitations](analysis/fire-vase-utility.md).
