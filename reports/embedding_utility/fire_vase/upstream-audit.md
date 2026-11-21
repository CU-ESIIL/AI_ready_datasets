# Fire VASE upstream audit

Inspection: 20 November 2026. GitHub commit and local HEAD:
`2e20e15a42610f77cdd0583bb5a43fcc6f6c8959`. Local checkout was clean. No upstream
files were changed and no observational tables were loaded into this project.
The inspection manifest hashes the exact local files read.

## What is available

| Component | Evidence at pinned commit | Consequence |
| --- | --- | --- |
| Dated history primitives | `src/cubedynamics/analysis_v2.py`: `growth_summary`, `allocation_profile`, `shape_traits`, `pulse_counts` | Reuse upstream through a version-pinned adapter; do not copy algorithms |
| Temporal state controls | Same module: `exact_transitions`, `validate_exposure` | Existing gap/duplicate/future-geometry guards are useful, but do not prove observation availability at issue time |
| Statistical representation | Same module: `fit_pca`, `PCA.transform` | Standardized PCA exists; fresh benchmark splits need fresh training-only fits |
| Raw/derived table schema | `schemas/vase_slices.schema.json`: `fire_id`, `timestamp`, `ring_area_km2`, cache/version fields | Table-level adapter needs actual-table validation; schema does not fully define observation intervals, uncertainty or availability |
| Cohort and validation | `analysis/scientific_validation/population_audit.json`, `validated_summary.json`, `final_report.md` | Preserve declared populations and qualified claims |
| Geometry sensitivity | `analysis/scientific_validation/compositional_sensitivity/` | Baseline vs Hellinger comparisons already exist; use them to define diagnostics, not new test-set performance |
| Null/depth tests | `analysis/scientific_validation/final_adversarial_pass/` | Ordering and compression have distinct interpretations |
| Reproduction/storage | `config/data_release.yml`, `docs/reproduce-data-lake.md`, README | Data-lake access is separate from code access; no automatic source rebuild |

Links use this [pinned repository tree](https://github.com/CU-ESIIL/fire_vase/tree/2e20e15a42610f77cdd0583bb5a43fcc6f6c8959).

## Verified distinctions

The retained population audit reports 278,569 events, 10,246 primary eligible
histories and 9,212 primary histories with complete weather. Primary eligibility
requires at least three consecutive dated observations. Only about 3.68% of catalog
events qualify; this is not representative coverage of every fire. One/two-slice
and gappy histories need explicit strata, not silent deletion or imputation.

The compositional sensitivity reports 20 allocation bins and five standardized-PCA
axes explaining 0.894435897825 of baseline variance. Its Hellinger variant explains
0.882819004277. Fifteen-neighbor overlap is about 0.701 and extreme-tail overlap
about 0.430, despite high broad-distance correspondence. These are retained upstream
results, not rerun measurements in this study. Explained variance is not prediction,
retrieval relevance or scientific truth.

`allocation_profile` interpolates cumulative allocated mass over equal-width
observed-day intervals and differences the interpolated CDF. It is mass-conserving;
it is not simply interpolated growth rate at 20 points. Gappy data are explicitly
an observation-time sensitivity, not the primary calendar-time profile.

`growth_summary` distinguishes reconstructed sum from catalog area and observed
peak increment from total/duration. Preserve km², observation count and recorded
dates; do not call every adjacent observed pair a one-day transition.

The population audit reports actual cached dates 2000-11-02 through 2021-05-01;
filenames and older descriptions give a different apparent range. Use audited
coverage and per-record evidence. The `validated_summary.json` records an earlier
analysis SHA, distinct from the repository HEAD inspected here; retain both.

Upstream nulls show considerable compression even under constrained reference
histories. Observed ordering is additional evidence, not proof of biological
mechanism. Weather associations and predictive increments are qualified by response,
cohort and blocking; do not generalize them to all environmental information.

## Integration risks and open evidence

- The distribution is named `fire-vase`, but its transitional import namespace is
  `cubedynamics`. This project separately targets an external CubeDynamics package.
  Installing both into one environment risks namespace/version collisions. Prefer
  a pinned isolated worker with narrow JSON/Arrow contracts, after API tests.
- Real case data/version/checksums, FIRED/gridMET terms, attribution, derivative
  permissions, uncertainty and event-level support need an explicit input manifest.
  Code licensing does not establish source-data redistribution rights.
- Do not use already globally fitted PCA or existing manuscript weather results as
  leakage-free held-out benchmark artifacts. Refit inside training folds.
- Dated records are reconstructed observations, not necessarily information available
  operationally that day. Forecast claims need data-availability evidence.
- Temporal neural embeddings, geometry/fragmentation capabilities, adaptive routing
  and agent benchmark APIs are proposed here, not verified existing integrations.
- Missingness perturbations may make a history ineligible. The correct outcome can
  be abstention; removing observations is not necessarily a harmless transformation.
