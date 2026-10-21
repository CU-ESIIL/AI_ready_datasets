# MOSAIKS from harmonization outputs

The embedding module consumes **harmonized raster outputs**, not raw Sentinel
assets. It has no STAC client, raster reader, DN calibration, image download, or
generic pretrained vision encoder. The optional source-specific orchestrator
composes these separate stages:

```text
metadata + context → specialist consensus → deterministic QA + human decision
  → bounded source windows → approved raster harmonization
  → HarmonizedRasterPatch stream → frozen MOSAIKS filters → feature dataset
  → train/validation/test verification
```

## Raster output contract

The previous demonstration produced individual calibrated NIR values. Spatial
convolution requires a real spatial neighborhood. `HarmonizedRasterPatch` adds a
bounded C×H×W output with canonical channels/units, acquisition, actual footprint,
native window/CRS, quality policy, observation/content digest, and reviewed recipe
context. It is held in memory and discarded after encoding.

`assemble_patch` accepts explicit `(row, column, HarmonizedObservation)` cells. It
checks identities, recipe/human lineage, missing or duplicate cells, channel order,
units, coordinates and acquisition alignment. It does not turn unrelated scalars
into an image. `harmonize_window` is a vectorized deterministic raster counterpart
of the existing scalar executor; it accepts only the reviewed scalar operation
allowlist for the first single-band vectorized slice and emits this contract. Scientific calculations retain float64; conversion
to float32 and explicit input scaling belong to MOSAIKS preprocessing. Scientific
values are not clipped or resized.

`RasterContext` carries the full source plan, recipe, consensus and human decision.
Real Sentinel contexts additionally require `evidence_review`: a source/recipe-bound
report from all six scoped specialists with accepted QA synthesis. The preflight
recomputes evidence checks and preserves every earlier model veto.
The same preflight gates run before reference sampling, source access or encoding.
A new `sentinel-raster` plan binds its tile layout and MOSAIKS settings into the
consensus digest; an older single-pixel consensus cannot authorize the larger job.
Metadata cleanup/enrichment remains an upstream responsibility. Unknown meaning or
rights do not become resolved merely because a tile can be encoded.

## MOSAIKS implementation

This is a small NumPy implementation of the empirical random-convolution method
in [Rolf et al. (2021)](https://www.nature.com/articles/s41467-021-24638-z), checked
against the [authors' pinned featurization source](https://github.com/Global-Policy-Lab/mosaiks-paper/blob/7efb09ed455505562d6bb04c2aaa242ef59f0a82/code/mosaiks/featurization.py).
It samples small filters from **training harmonization outputs only**, performs
contrast normalization and regularized covariance normalization, freezes the filter
bank, and pools positive/negative thresholded convolution responses. It is a
MOSAIKS variant with global mean pooling, not a reproduction of the global API's
feature coordinates or a pretrained semantic neural network. No external model
weights are needed.

Default settings are 512 features, 3×3 filters, seed 42, bias 1, and at most 16
reference tiles. `input_scale` is explicit; it is not a unit conversion. The small
NIR example sets it to 32 to avoid suppressing low-amplitude texture responses.
One NIR channel is supported without inventing visible bands. Contrast-normalized
single-band filters need not retain absolute brightness: the first verification
target is within-tile variation, not an assertion that mean reflectance can be
recovered. A multichannel harmonization product can use explicit cell assembly and the
same MOSAIKS interface after
its channel meanings and alignment are reviewed.

A bounded prefix of training tiles stays in memory while filters are fitted; those
tiles are then encoded before the source advances. Filter calibration never sees
validation/test data. Filters, seed, parameters, full reference-training context and canonical
scientific-definition digests are recorded. Filters are derived model artifacts,
not archived raw image patches. A frozen encoder is reusable only with compatible
canonical definitions/units; matching variable names alone is insufficient.

## AI-ready output and verification sets

The dataset contains:

- `vectors-*.npy`: bounded dense float32 matrices, directly loadable by NumPy and ML libraries.
- `records.jsonl`: vector locations, observation IDs, source/recipe/context lineage, spatial groups and split membership.
- `encoder/`: frozen empirical filters and full encoder/preprocessing identity.
- `harmonization_context.json`: scientific metadata, source rights, recipe, QA/consensus and applicable human decision.
- `verification_labels.jsonl`: targets stored separately from features, with declared label origin.
- `manifest.json`: completion status, schema, dimensions, code/runtime identity and content checksums.
- `dataset_card.md`: human-readable input meaning, split counts and scientific limitations.

No raw or harmonized raster files are written. Failed runs retain partial metadata
and are not accepted by verification. Feature shards are bounded by batch size;
the verification command is deliberately limited to 2,048 examples by default.
There is no resumable distributed execution or vector database service yet.

`mosaiks-verify` checks shapes, finite values, encoder identities, file integrity,
vector collisions/zero vectors, duplicate observations, spatial-group separation,
and geographic overlap across splits. Its ridge probe fits normalization on train
only, selects regularization on validation only, and evaluates on test once. It
reports RMSE/R² beside mean-prediction and shuffled-training-label baselines. It
does not tune on test results. The fitted numeric consumer is saved as
`verification_probe.npz`, including train-only normalization, coefficients,
intercept and encoder identity; the report carries its checksum.
`predict_vectors` reloads it to consume compatible vectors without retraining. Declared group IDs still require a scientifically
defensible geographic/temporal sampling design.

Three target types are distinct: `derived-diagnostic`, `proxy-label`, and
`independent-label`. The latter two require source/version/license/method and
spatial/temporal alignment provenance. The initial texture target is calculated
from harmonized inputs and is **not independent scientific ground truth**. Strong
verification still needs reviewed independent labels, another area/time, and
scientific task-specific acceptance criteria. No ecological validation is claimed.

These vectors are native numerical inputs for a fitted ML model. An arbitrary LLM
does not inherently understand their dimensions; a trained downstream head or
retrieval system and its own verification are necessary.

## Commands

```sh
pip install -e '.[embeddings,real,dev]'
prototype mosaiks-demo --output run/mosaiks-diagnostic
prototype mosaiks-verify run/mosaiks-diagnostic --output run/mosaiks-diagnostic/verification.json
```

The demo sends **generated diagnostics through actual deterministic harmonization
and actual MOSAIKS computation**. It creates no synthetic human approval and does
not claim provider observations. Offline tests also use generated in-memory tiles;
no test imagery is downloaded.

For the real-data pipeline, create a `MOSAIKSSpec` JSON with channels
`["B08_reflectance"]`, units `["1"]`, features 512 and `input_scale: 32`, then:

```sh
prototype mosaiks-plan run/sentinel-stream-plan.json run/mosaiks-nir-spec.json \
  --side 8 --grid 8 --output run/mosaiks-real-plan.json
prototype consensus run/mosaiks-real-plan.json --output run/mosaiks-real-consensus
```

The source-specific example requests native 8×8-pixel tiles within an 8×8 grid
(about 640×640 m at 10 m resolution). A buffer column is unused; remaining columns
form train/validation/test spatial blocks. It reads one bounded NIR window and
native covering SCL cells at a time. Any nodata or unacceptable SCL stops the run
explicitly. It performs no spatial interpolation or temporal compositing.

After genuine consensus and review, create `RasterContext` JSON containing that
plan, the exact approved recipe, its matching actual human decision, and consensus.
The recipe/context files are metadata, not image datasets:

```sh
prototype mosaiks-run run/mosaiks-approved-context.json run/mosaiks-nir-spec.json \
  --side 8 --grid 8 --output run/mosaiks-real-dataset
prototype mosaiks-verify run/mosaiks-real-dataset --output run/mosaiks-real-dataset/verification.json
```

The independent Python interface is `write_dataset(harmonized_patch_iterator,
model, context, output)`. Any reviewed harmonization provider can supply the stream;
Sentinel access is confined to the upstream example adapter.

## Verification result — 2026-10-21

The generated run `run/mosaiks-verified-release/` produced 32 vectors with 128 features:
16 train, eight validation, eight test. A frozen-filter ridge probe recovered the
derived within-tile variation diagnostic with test R² approximately 0.996 and
RMSE 0.00119; mean and shuffled-label baseline RMSEs were 0.02065 and 0.02827.
These results verify numerical task consumption on generated harmonization
outputs, not ecological performance. All examples were generated in memory; no
imagery was downloaded for testing.

A real-metadata plan is saved as `run/mosaiks-real-plan.json`, using 512 features
and an approximately 640×640 m native NIR grid. Its live OpenClaw/Verde run produced
a schema-valid draft and three valid peer reviews, all requesting revision. The
rights response cited its own analysis instead of a peer and was rejected. The
run therefore did not reach consensus or read source rasters. The exact candidate
reviewed by the agents was preserved from the task envelope as
`run/mosaiks-real-consensus/candidate_recipe.json`, with failure traces and a
`run_summary.json`; it is not an approved scientific recipe. Future runs now
checkpoint a valid candidate and deterministic QA before starting peer reviews.

The real harmonized-data → MOSAIKS path is implemented and offline-tested, but
actual source execution remains gated on fresh valid consensus and a real human
decision. Independent labels and geographic/temporal transfer verification remain
open scientific work. Nearby blocks can still share spatial autocorrelation even
when they do not overlap.

## External CubeDynamics execution

The optional [CubeDynamics backend](cubedynamics.md) supplies seven registered,
reference-bound capabilities on trusted xarray/Dask inputs. Models select operations;
tested software performs them after scientific validation and exact-recipe human
review. Source access remains upstream. The direct MOSAIKS bridge preserves the
reviewed raster layout; support-changing aggregation/alignment needs explicit review
and does not automatically establish a new representation layout. Real Sentinel
vetoes and existing streaming gates remain binding.
