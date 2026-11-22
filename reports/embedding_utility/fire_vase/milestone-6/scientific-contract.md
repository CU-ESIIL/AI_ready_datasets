# Real-data scientific contract — proposed for human review

**UNDER ANALYSIS / PROPOSED. No row adapter or cohort has executed.**
Canonical local source is the user's packaged lake at
`fire_vase/data_lake/fire-vase-data-lake-v0.1/files/`. The package inventory and
checksums identify source artifacts; physical presence is confirmed. No GitHub
upload, source copy or restore is needed.

## Native semantics and required distinctions

| Topic | Evidence inspected | Required treatment / unresolved review |
| --- | --- | --- |
| Daily area | FIRED field `dy_ar_km2`; upstream `normalize_daily` directly copies it to `ring_area_km2` | Native estimated area assigned to a burn-date bin, not automatically a calibrated instantaneous physical spread rate. Verify original unit/date-bin definitions before a km²/day convention |
| Cached ring area | Upstream v2 one-to-one ID/date comparison against native `dy_ar_km2`, historical tolerance1e-9 km² | Same values were historically checked for the audited files; code/report is not fresh identity verification or authority to infer arbitrary ring-to-day equivalence |
| Cumulative area | Climate-table builder constructs `groupby(fire_id).cumsum(ring_area_km2)` | Derived sum of retained observed increments. Across gaps it is not evidence of a complete daily history. Do not difference catalog final totals or treat observed-prefix mass as an evidenced full-event baseline |
| Other same-named fields | Perimeter builder sets a `cumulative_area_km2` field from native `tot_ar_km2` | Same labels across products do not establish the same definition. Exclude perimeter products until independently reviewed; never join by label alone |
| Calendar transitions | Corrected `exact_transitions` requires next-current date gap exactly1 and unique current/next IDs/dates | Multi-day adjacent records are not daily growth. A horizon3 target needs three supported future calendar days, not merely three following rows |
| Missing vs zero | Corrected builder rejects missing/nonfinite/negative area; upstream aggregate reports zero observed zero-growth rows | Unknown/missing stays unknown. An explicitly observed zero remains zero. Absence of recorded daily rows never creates zero-growth days |
| Event identity | Native `id`; cached `fire_id`; historical outer join enumerates unmatched rows | Preserve original value/type, source release, observation key and event boundaries. Do not merge releases or redefine fires from similar names/overlap |
| Native support / CRS | GeoPackage catalog associates both native feature tables with custom SRS100000 (`organization=NONE`), with definition recorded | Preserve native definition/support; presence of an EPSG4326 SRS entry is not the feature CRS. No reprojection, geometry reads or support changes in initial audit |
| Quality | Source schemas and cached climate availability flags | Climate completeness is not burn-date/area quality. Preserve native flags if present; missing original sensor QA and uncertainty remain explicit |
| Availability | Upstream v2 calls its predictors retrospective end-of-day reconstructions | Native date is not observation availability. Never insert synthetic midnight timestamps into real records. Operational prospective claims require release/processing latency evidence |
| Normalization | Full-history `normalized_vase_width` uses completed total | Forbidden predictor: final normalized width, complete-fire PCA/features, final area/duration, future weather and derived endpoint labels |
| Rights | Package README retains FIRED/gridMET terms; dataset landing page is currently inaccessible | Code MIT and article CC BY do not establish this cached release's dataset reuse/derivative/redistribution terms. Human assessment required |

The original M4 `RealPrefixApproval` is an inert string-based evidence record. It does
not establish source interpretation or availability and is not an execution gate.
M6 adds explicit source/container identities, versioned proposed recipes, domain review,
claim mode and bounded scope. A precondition checker cannot authenticate human
review or issue production permission.

## Proposed recipes and scientific preconditions

Each recipe is version `m6-review-v1`, status **PROPOSED_FOR_REVIEW** in
[packet.json](review-v2/packet.json). No model-generated formula, dynamic SQL or
arbitrary transformation is exposed.

1. `native_increment_identity`: preserve native raw values/units/IDs/dates; compare
   source/cache by exact keys, with no imputation or generic cumulative differencing.
2. `calendar_support_validation`: retain original order and duplicate evidence;
   validate one-day adjacency/event boundaries, missingness and observed zeros.
   Sorting is an explicit reviewed step, never a way to erase duplicates.
3. `observed_prefix_only`: only observed past, source uncertainty/flags and cutoff;
   define prefix origin as event-origin or observation-window before implementation.
   A bounded audit fragment cannot establish a full event prefix. No completed totals.
4. `independent_future_targets`: A next day; B next-three sum; C future/past mean
   comparison; D next-three population SD; E independent future-pattern relevance.
   Unsupported horizons abstain; future values never become predictor inputs.
5. `fire_grouped_holdouts`: immutable whole-fire grouping, training-only preprocessing,
   separate selection/calibration/test and year/region blocks; endpoint strata used
   for evaluation only, never predictors.

Implementation references are inspected upstream code and already tested synthetic
algorithms. Those references are not a reviewed real-source adapter or permission.
Tests here validate generic generated calendar/approval evidence, not empirical
FIRED equivalence. Native mapping and rights still require human findings.

## Prospective versus retrospective mode

The milestone's prospective scientific objective is **not achieved** by relabeling
retrospective observations. For the initial native-value audit, propose an explicitly
retrospective claim only. A subsequent real representation experiment needs either
actual availability evidence and a valid issue-time protocol, or a separately reviewed
retrospective-only protocol whose conclusions remain reconstructed prediction.

The existing `PrefixInput` requires known timezone-aware availability. Do not populate
it with invented real timestamps to make old model code run. A future approved adapter
must preserve unknown availability in a distinct retrospective evidence contract;
that interface change needs review, tests, recipe and diagram updates before execution.

## Holdouts, selection and uncertainty — required before training

Define complete-prefix origin, daily support and future support separately. Reject
ambiguous event keys, date collisions, unsupported gaps or unknown target values;
never exclude only because a numerical value is unusual. Preserve all exclusion
counts and separate source catalog/event/window denominators. Freeze train/validation/
calibration/test at fire level before fitting. Select temporal blocks and independently
reviewed geographic regions using catalog metadata after approved reads; do not reuse
upstream globally fitted morphospace or folds as fresh held-out evidence.

At depth3/5/7/10, A needs one following supported day; B–E need three. Catalog final
size and retrospectively defined stage can stratify evaluation but cannot enter
prospective inputs; stage measured relative to completed duration is unavailable at
issue. Native region labels, geographic footprint and region-holdout support require
review; ecological region labels are not interchangeable with arbitrary longitude bins.

Predictive intervals/calibration do not measure remote-sensing error. Report model
error separately from unquantified area/date uncertainty, date-bin/time-zone ambiguity,
source QA loss and observational selection. No observational error distribution,
time-shift tolerance or imputation rule is assumed without evidence.

Initial audit cap: **512 total decoded rows across sources, at most16 fires,
batches≤128**, no full scan/geometry, no raw/harmonized persistence, no model training,
no redistribution. This is an implementation/integrity audit, not a representative
scientific cohort or approved training sample. A budget exhaustion may mean incomplete
examples; abort/abstain rather than backfill beyond the approved bound.
