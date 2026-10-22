# Scientific validation — 22 October 2026

This is separate from the historical pipeline-state report. It retains real public
vocabulary graphs and NEON product/site metadata, provisional semantic assessments,
blocked real-data review packages, and 100 live inert Verde calls.

The report does not approve scientific execution, lift model vetoes, equate datasets,
claim a human gold standard or claim the weaker-model hypothesis has been tested.

## Major artifacts

- `../../output/pdf/AI_ready_scientific_validation_report.pdf`: 20 pages, 18 figures.
- `report.json`, `report.md`, `build_report.py`: editable report content and figures.
- `data/sentinel_review_gap_analysis.json`: ten issues with original findings intact.
- `data/expert_decision_template.json`: blank issue decisions, not runtime approval.
- `data/neon_sentinel_case.json`: proposed context relationship and missing operation.
- `data/canonical_benchmark.json`: 25 observation specifications, exact sets through
  size three, greedy/subdomain accumulation, thresholds, pair overlap and gaps.
- `data/resource_depth.json`: three parsed local graphs, no import closure/reasoning.
- `data/dataset_benchmark.json`: 18 mixed-scope records, eight review rubrics, 153 pairs.
- `data/model_experiment/`: 100 exact calls, deterministic evaluations and summary.
- `data/run_manifest.json`: input/output, graph, model-call, build and figure hashes.

Formal observation roles verified in a graph are not exact scientific variable
mappings. Coverage is a dimension-level project assessment. Graph size/depth is not
quality. Dataset diversity is a documented lower bound; candidate resource count is
an explicit, unvalidated potential diagnostic. Unassessed fields stay unknown.

## Rebuild from the retained report snapshot

Use Python 3.12 and install repository extras `dev,cubedynamics,validation`. From root:

```sh
MPLCONFIGDIR=/tmp/ai-ready-validation-mpl python reports/scientific_validation/build_report.py
python reports/scientific_validation/write_docs.py
python reports/scientific_validation/verify.py
```

This rebuild does not acquire metadata, invoke models or access observations.
Figures are emitted as PNG and editable SVG; timestamps may change file hashes.
Visually inspect the rendered PDF after any change. Text-block overflow is rejected.

## Refresh analysis from original local inputs

`analyze.py` reads explicitly selected historical `run/` artifacts, canonical CSV,
retained graphs, and NEON metadata. Those ignored historical inputs are required
and are not silently synthesized if missing.

```sh
python reports/scientific_validation/analyze.py
python reports/scientific_validation/evaluate_retained_calls.py
python -m pytest -q --junitxml=reports/scientific_validation/data/tests.xml
python reports/scientific_validation/build_report.py
python reports/scientific_validation/write_docs.py
```

`acquire_graphs.py` is a separate explicit metadata acquisition step using the
allow-listed source plan; it never follows imports. Metadata licenses/attribution
are retained in `data/graphs/manifest.json` and the W3C notice. NEON metadata came
from public product/site endpoints; no observations or source raster datasets were
retrieved. Source-specific citation/DOI and permissions still need review.

## Live model experiment (explicit opt-in)

The original pilot used the existing isolated OpenClaw runtime and one configured
Verde model. Running a new experiment requires an operational verified runtime and
a fresh output directory:

```sh
python reports/scientific_validation/run_model_experiment.py --output run/new-validation-experiment --repeats 2 --limit 25
```

Update the explicit replay input path before refreshing the report. A captures prose
inside a mandatory transport JSON envelope; B is a closed decision schema; C/D are
paired deterministic re-evaluations of B. Failed calls remain failures. No model
content is executable. The original pilot's `started_at` was recorded after response;
its elapsed durations and exact trace timestamps are preserved with that caveat.
The runner has subsequently corrected the start timestamp; call schemas/prompts
remain in each original record. Semantic correctness of A is not automatically
inferred from keywords. Gold decisions remain blank until actual experts author them.

## Interpretation limits and next experiments

The single 120b provider model cannot establish the weaker-local-model hypothesis.
Additional models, expert gold/adjudication, blinded prose coding, independent
outcome labels, a pre-specified unsafe-proposal rubric and a larger repeated design
are required for scientific model comparisons. Zero execution is enforced, not a
model-safety score. New methods must remain registered, reviewed and deterministic.

The proposed NIWO case stops before source access: the site coordinate differs
from the old Sentinel planning point and is not a sensor location. Obtain bounded
sensor-aware NEON evidence and define a scientifically justified interval-to-instant
contextual association before implementing a new operation. Existing exact-support
joins and nearest sampling do not supply that scientific relationship.
