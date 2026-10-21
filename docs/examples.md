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
