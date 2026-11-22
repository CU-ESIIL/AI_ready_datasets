# Reproducibility

Run from the repository root using the existing real lake and frozen census.
Do not download a substitute dataset or copy source observations into this repo.
The executed runtime and package versions are bound in the execution manifest.
The implementation uses NumPy/SciPy/Matplotlib; the original census also needs
PyArrow and the repository's base Pydantic dependency. `fire-vase-utility` declares
the new optional numerical dependencies. Existing lake dependencies remain
separate. Reproduction is CPU-only; no torch, API keys or inference services.

Retain the plans from this directory before fitting in a **fresh versioned output**
with a `private/` child. Preserve old outputs; archive an existing result directory
before any deliberate rerun. The primary runner rejects changed source/recipe or
training identities when reusing checkpoints. Do not reuse downstream heads after
changing scientific inputs or implementation. Final checkpoint files are NPZ,
loaded without pickle. Metadata/source state is private local evidence, not an
export package. Hash verification is read-only and does not grant approval.

```sh
export PYTHONPATH=src
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MPLCONFIGDIR=/tmp/fire-vase-m8-matplotlib
lake=../fire_vase/data_lake/fire-vase-data-lake-v0.1
census=reports/embedding_utility/fire_vase/milestone-7-3-execution
out=reports/embedding_utility/fire_vase/milestone-8
py=../spectralbridge/.venv/bin/python
"$py" scripts/run_fire_vase_milestone8.py --output "$out" --census "$census" --lake "$lake"
"$py" scripts/evaluate_fire_vase_milestone8.py --output "$out" --lake "$lake"
"$py" scripts/extend_fire_vase_milestone8.py --output "$out" 
"$py" scripts/predict_fire_vase_milestone8.py --output "$out" --lake "$lake"
"$py" scripts/reference_fire_vase_milestone8.py --output "$out" --lake "$lake"
"$py" scripts/audit_fire_vase_m8_access.py --output "$out" --lake "$lake"
"$py" scripts/statistics_fire_vase_milestone8.py --output "$out" 
"$py" scripts/lifecycle_fire_vase_milestone8.py --output "$out" 
"$py" scripts/scale_fire_vase_milestone8.py --output "$out" 
"$py" scripts/rank_fire_vase_milestone8.py --output "$out" 
"$py" scripts/access_retrieval_fire_vase_m8.py --output "$out" 
"$py" scripts/metadata_fire_vase_milestone8.py --output "$out" 
"$py" scripts/order_fire_vase_m8.py --output "$out"
"$py" scripts/normalization_fire_vase_m8.py --output "$out" 
"$py" scripts/cumulative_fire_vase_m8.py --output "$out" 
"$py" scripts/retain_fire_vase_m8_blocked_heads.py --output "$out" 
"$py" scripts/inverse_fire_vase_m8.py --output "$out" 
"$py" scripts/report_fire_vase_milestone8.py --output "$out" 
"$py" scripts/validate_fire_vase_milestone8.py --output "$out" --census "$census" --lake "$lake"
# After successful tests, strict docs and figure QA:
"$py" scripts/manifest_fire_vase_milestone8.py --output "$out"
```

These are execution commands and ordering, not a claim that rerunning into a
frozen directory is safe. For a fresh output copy the primary/statistical,
generalization and prediction plans first. The historical correction archive is
retained from the actual run; it is not required to reproduce corrected code.
`rank_fire_vase_milestone8.py` deliberately supersedes the older convenience rank
column. `retain_fire_vase_m8_blocked_heads.py` verifies retained heads reproduce
blocked scores. `inverse_fire_vase_m8.py` reproduces unsupervised PCA inverse
recovery without downstream labels. Physical timings vary by machine/cache.

```sh
FIRE_VASE_ROOT=../fire_vase FIRE_VASE_PYTHON=../fire_vase/.venv/bin/python \
  PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  ../spectralbridge/.venv/bin/python -m pytest -q
PYTHONPATH=src ../spectralbridge/.venv/bin/python scripts/generate_reference.py
../spectralbridge/.venv/bin/python -m mkdocs build --strict
```

The recorded suite passed 410 tests with two skips. Validation logs are retained
under `validation/`. Figure files include PDF/SVG/220dpi PNG, thirteen measured
figure families. The information-status figure is a recipe-derived exactness
classification; recovery/retrieval/cost panels use actual numerical results.

## Artifact map

| Evidence | Files |
|---|---|
| Cohorts/splits/eligibility | `feature-construction.json`, `property-eligibility.csv`, private `observed-state.npz` with source-row/date lineage and whole-fire folds |
| Training | design JSON, `training-complete.json`, `training-cache-identity.json`, private per-fit training JSON and encoder/PCA/preprocessing checkpoints |
| Capacity | `checkpoint-inventory.json` separates encoder/head parameters for 96 neural checkpoints; 75 primary, 21 control/update fits |
| Independent references | `independent-reference-validation.json`, private original-unit property references, native source hashes |
| Exact/approximate information | `exactness-register.json`, `information-preservation.csv`, `original-unit-reconstruction.csv`, `pca-inverse-recovery.csv`, `short-cumulative-recovery.csv`, normalization controls/collisions |
| A/B/C access | `access-condition-results.csv`, `metadataB-recovery.csv`, `metadataB-retrieval.csv`, `access-independent-validation.json` |
| Retrieval | results/population-weighted/uncertainty/rank/scaling CSVs, PCA inverse and access-condition CSVs, runtime/index traces and private gallery/query/reference indices |
| Transfer | property table by objective/dimension/fraction, `blocked-generalization.csv` and retained blocked preprocessors/heads |
| Inference diagnostics | `paired-statistical-comparisons.csv`, `geographic-temporal-strata.csv`, plans and rank diagnostics |
| Lifecycle | workload/reuse/Pareto CSVs; refresh/model-update/index/fallback timing traces; shared-source and physical-I/O limitations |
| Secondary prediction | prediction CSVs/runtime/paired intervals; all six exact support cohorts; private prefix model state and retained evaluation arrays |
| Corrections | `probe-correction.json`, private invalid-initial archive, bit-identical optimized encoder test |
| Integrity | `execution-manifest.json`, `validation/postflight.json`, full source rehash and offline tests |

No raw daily source values are serialized as a new observation dataset. Derived
property references and bounded prefix model inputs are distinct scientific
products with source lineage. Numeric storage counts exclude shared source/date
metadata; materialized vectors use the declared dtype. Hashes bind bytes and
identity; they do not establish scientific truth or third-party rights.
