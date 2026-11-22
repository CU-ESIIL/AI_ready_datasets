from pathlib import Path
import json,csv,math,sqlite3
b=Path('reports/embedding_utility/fire_vase/milestone-7-3-execution');c=json.loads((b/'census.json').read_text());s=json.loads((b/'population-summary.json').read_text());r=json.loads((b/'profiling-resource-report.json').read_text())
m=list(csv.DictReader((b/'depth-horizon-eligibility.csv').open()));depth=list(csv.DictReader((b/'temporal-depth.csv').open()));native=[x for x in m if x['source']=='native'];db=sqlite3.connect(b/'cohort-metadata.sqlite')
header='**CURRENT REAL OBSERVATIONS — internal-use outputs; no model training or publication performed.**\n\n'
text='# Real Fire VASE population census\n\n'+header
text+='''The complete relevant native daily/event GeoPackages and cached daily/trait Parquet
containers were freshly hash-verified and decoded without a pilot row cap. All four
full-container hashes match their historical identities. Climate raster arrays and
unrelated figures were not read: they are not needed to count the fire population.
No source file was modified. The investigator’s direct instruction superseded the
separate-receipt requirement for read-only internal profiling; no fictional receipt,
reviewer identity or domain PASS finding was created.

## Complete native/cache accounting

| Quantity | Native daily | Cached daily |
| --- | ---: | ---: |
'''
for label,key in [('Distinct fire IDs','fires'),('Daily records','rows'),('Supported valid date/area records','valid_supported_rows'),('Observed zero increments','observed_zero'),('Missing daily values','missing_area'),('Invalid/nonfinite/negative daily values','invalid_area'),('Missing/unsupported dates','missing_date'),('Duplicate event-date rows','duplicate_rows'),('Exact one-day intervals','exact_day_intervals'),('Longer inter-record gaps','gap_intervals'),('Unobserved calendar days inside gaps','unobserved_days')]:text+=f"| {label} | {c['counts']['native'][key]:,} | {c['counts']['cache'][key]:,} |\n"
text+='''
The event catalog contains **278,569 unique IDs**, with no missing or duplicate IDs.
Native daily observations contain **278,865 IDs**. The difference is 296 unmatched
native IDs, not a normalization collision or newly approved event merge. They remain
separate and retain unknown catalog year/region/size. Cached cumulative values are
finite/nonnegative in all 626,102 cached rows; this is a value check, not independent
validation of their scientific interpretation. Native `tot_ar_km2` is not differenced
or substituted as a daily increment.

## Local runs unlock substantially more usable histories

A supported run contains consecutive original calendar-day bins with valid
nonnegative native values and unique dates. Duplicate dates, missing/invalid values
and gaps break support. No gap filling, interpolation or cross-fire combination occurs.
“Strict history” describes the retained record, not full ignition-to-extinction coverage.

| Minimum run depth | Fires with a local run | Maximal qualifying runs | Within-run windows | Entire-history-consecutive fires |
| --- | ---: | ---: | ---: | ---: |
'''
for x in depth:text+=f"| {x['depth']} | {int(x['local_run_fires']):,} | {int(x['local_runs']):,} | {int(x['dependent_windows']):,} | {int(x['strict_whole_history_fires']):,} |\n"
text+='''
Native ≥3 local-run coverage is **34,911/278,865 = 12.52%**, compared with **10,260**
strict whole-consecutive ≥3 histories, a **3.40×** increase in fires. On the exact
historical cache population, the fresh result is **34,852 local-run fires** versus
**10,246 strict fires**, retaining the historical strict count while broadening
local-run coverage. The older 3.68% headline described strict histories, not local runs.

## Complete depth × horizon matrix

Cells below are eligible independent fire counts; dependent window/run counts,
median/max windows per eligible fire, cache comparisons and strata are in
`depth-horizon-eligibility.csv` and `eligibility-strata.csv`.

| Input days | Future 1 day | Future 3 days | Future 7 days |
| --- | ---: | ---: | ---: |
'''
for d in (3,5,7,10,14,21,30):
 vals=[next(x['eligible_fires'] for x in native if int(x['depth'])==d and int(x['horizon'])==h) for h in (1,3,7)]
 text+=f"| {d} | "+' | '.join(f'{int(v):,}' for v in vals)+' |\n'
text+='''
![Actual eligibility](figures/eligible-fire-heatmap.png)

For depth3/horizon1, **19,004 fires**, **20,618 runs** and **61,342 overlapping
windows** are distinct sample sizes. For depth7/horizon3, the corresponding counts
are **1,859 / 1,896 / 10,570**. These same-support counts establish candidate task
feasibility, not predictive or ecological validity. All target days are supported;
original measurement QA, uncertainty and operational availability remain unknown.

## Reproducibility and resource evidence

The full successful replay decoded 1,253,135 daily records (native plus cache), took
73.55 seconds and used 313,917,440 bytes peak process memory. Exact source/cache
records are reconciled through compact key/value hashes and row references; no raw
or harmonized daily measurement dataset or prediction tensors were persisted.
Metadata products are approximately 0.7 GB, mostly the reconciliation key index.
Full-container verification covered 893,563,713 bytes; filesystem physical I/O bytes
are unmeasured and are not substituted with that logical total.

Independent replay gave identical census JSON, byte-identical run/profile Parquet
files and identical fire/run/window/gap metadata rows. The initial Arrow writer
failed when a later batch had all-null quality columns; the failure and partial
file were retained, the schema handling was corrected, and stage restart reused
completed source streams. A dedicated test now covers that batch-boundary defect.

See `replay-validation.json`, `profiling-resource-report.json`, source hashes and
validation logs. All nine requested figure families are generated in PDF/SVG/PNG.
They are internal scientific artifacts, not published or independently reviewed
scientific conclusions. Earlier M1–7 frozen evidence remains separate.

## What this means for the embedding experiment

We have enough supported short-depth fires for a substantial raw/features/PCA/neural
comparison. The critical scientific test is now representation utility under
whole-fire and geographic/temporal separation, rather than whether any sequences
exist. Longer-depth comparisons remain sharply constrained: depth30/horizon7 has
only **27 fires**, so 246 windows must not be presented as 246 independent trials.
Quality/uncertainty, support, source coverage and long-history selection must accompany
any later skill claim. No model has yet been trained on these real cohorts.

Companion reports: [reconciliation](native-cache-reconciliation.md),
[selection bias](selection-bias-report.md), [feasibility](scientific-feasibility.md),
[unsupported claims](unsupported-claims.md).
'''
(b/'real-population-census.md').write_text(text)
(b/'native-cache-reconciliation.md').write_text('# Native/cache reconciliation\n\n'+header+'''Fresh complete-container hashes match all four recorded identities. Native daily
records: 627,033; cached daily: 626,102. Overlap: 626,102 unique event-date keys;
native-only: 931; cache-only: zero. Overlap native `dy_ar_km2` versus cache
`ring_area_km2`: zero exact numeric-value-hash mismatches, with no tolerance tuning.

**All 931 unmatched records belong to 296 native IDs absent from the native event
catalog.** No catalog fire loses a daily observation relative to this native source.
The native daily ID population is 278,865, while catalog/cache are 278,569. These
numbers reconcile rather than forcing all sources to use the catalog denominator.

Native integer IDs are converted to decimal strings only for the documented
upstream key crosswalk; native feature row IDs and cache row offsets are retained.
Source hashes fix the release identity. No equivalence of unrelated products is
inferred. The build code’s inner join on event ID explains the omission pattern;
it is implementation evidence, not approval to invent catalog metadata for the
296 IDs. `population-summary.json` retains omitted-record years and membership.

For cache comparisons, original historical results reproduce: 278,569 fires,
626,102 rows, 196,611 exact-day pairs, 150,922 longer gaps, strict ≥3/5/7 histories
10,246/2,887/1,171. Native all-ID results differ: 196,982 exact pairs, 151,186 longer
gaps and strict ≥3/5/7 histories 10,260/2,891/1,172. These scope differences are
reported explicitly. Missing/zero/duplicate/invalid records are zero in both decoded
streams, not assumed from historical reports. Absence of observation dates is not
zero growth; 263,312 unobserved days lie between native records.

The compact SQLite index contains hashes and source/date/key references, not daily
measurement values. Catalog totals and derived observed-sum area strata remain
distinct. Cached cumulative finite counts do not turn final totals into increments.
''')
(b/'selection-bias-report.md').write_text('# Scientific selection bias\n\n'+header+'''The requested populations are measured in `population-summary.json` and their full
year/region/size/count/span/gap distributions in `selection-distributions.csv`:

| Population | Fires |
| --- | ---: |
'''+''.join(f'| {k} | {v:,} |\n' for k,v in s['populations'].items())+'''
A is the event catalog; B contains valid native daily IDs and therefore includes
296 additional unmatched IDs. These populations are not a sequential nested funnel.
G includes one-observation histories that are vacuously consecutive; morphology
comparisons must additionally require ≥3 observations. The strict ≥3 counts are
reported separately. Unknown attributes are retained rather than assigned to zero.

## Geography and temporal depth change the population

At local depth≥3, catalog-linked eligibility is Alaska 3,137/41,279 (7.60%), central
10,105/89,584 (11.28%), east 6,575/43,972 (14.95%), intermountain 8,866/58,896
(15.05%) and west 6,154/44,783 (13.74%). Hawaii is 15/55, a small denominator.
Another 59 local-run fires lack a catalog region. These are source-provided
`fire_traits.region` labels, not a newly calculated scientific spatial association.

For depth14/horizon7 the population contains 224 fires: its regional composition
is heavily shifted toward west/Alaska, unlike the catalog. Such contrasts concern
source support/observation selection; they do not establish ecological causes.
Year distributions use catalog ignition-year metadata; unmatched IDs retain unknown
event year even though their observation dates are preserved. Partial edge years
and source coverage must remain distinct from fire behavior.

## Fire size, gaps and environmental metadata

Measured source-catalog size selection is substantial: 205,970/278,569 catalog fires
(73.94%) are below1 km²; 25,128/34,911 local≥3 fires (71.98%) fall in1–<10 km²;
153/224 depth14/horizon7 fires (68.30%) fall in100–<1000 km². These compare cohort
composition using source-reported area classes, not causal ecological mechanisms.
A model comparison confined to these temporal cohorts cannot automatically generalize
to all catalog fires.

Figures compare source catalog-total size classes; CSVs additionally report classes
of summed retained native increments. The latter is a deterministic observed-area
summary, not a complete life-cycle reconstruction across gaps. Size bins are
<1, 1–<10, 10–<100, 100–<1000 and ≥1000 source-reported km², used as descriptive
strata rather than ecological equivalence or supervised labels. Observation count,
calendar span and gap distributions are retained for each selected cohort.

The cache flags 550,961/626,102 rows as `climate_available`, and 237,235 fires have
that flag for every cached row. This is source metadata, not verified environmental
alignment, native burn-area QA, physical uncertainty or operational availability.
Native sensor QA and measurement uncertainty are unknown for all counted support
windows. Missing QA is not evidence of high quality. Geometry was not decoded or
validated for scientific use; spatial/environment tasks remain independently scoped.

![Geographic composition](figures/geographic-selection.png)

![Size composition](figures/fire-size-selection.png)

All charts use actual current cohort metadata. Fractions show composition within a
cohort; they are not the probability of selection from the catalog. Unknown strata
and cohort denominators are retained in CSVs. No ecological-causal interpretation
or representative wildfire-population claim follows from observed-support coverage.
''')
train=list(csv.DictReader((b/'learning-curve-sizes.csv').open()))
feas='# Scientific feasibility and candidate splits\n\n'+header+'''No predictive model or held-out performance was evaluated. Split files are
**proposals**, not reviewed/approved scientific evaluation plans. Existing primary
metric definitions and unknown scientifically meaningful effects remain unchanged.

The compact split index assigns each source fire ID once using SHA256 seed20260828:
70% train, 15% validation, 15% test, using a split-specific hash namespace independent
of the learning-fraction hash. Every prefix/run from a fire inherits its group;
SQL uniqueness and independent tests verify split isolation. Candidate temporal
blocks are train≤2013, selection2014–2016, calibration2017–2018 and test2019–2021.
Unknown event years are excluded from year-based folds. Geographic group labels
support leave-one-reported-region-out candidates; no region was selected using
outcome performance. Region-specific completeness and small groups require review.

| Input/future days | Candidate train fires | Validation fires | Test fires |
| --- | ---: | ---: | ---: |
'''
for d,h in [(3,1),(3,3),(7,3),(14,7),(30,7)]:
 x=next(x for x in train if x['source']=='native' and x['training_fraction']=='1.0' and int(x['depth'])==d and int(x['horizon'])==h)
 feas+=f"| {d}/{h} | {int(x['candidate_training_fires']):,} | {int(x['candidate_validation_fires']):,} | {int(x['candidate_test_fires']):,} |\n"
feas+='''
`learning-curve-sizes.csv` provides exact nested 1%,3%,10%,30%,100% candidate training
counts for every native/cache depth/horizon, with the same held-out IDs at every
fraction. Hash-based subsampling is a learning-curve sensitivity, not the primary
all-eligible training cohort. Actual final folds must preserve the protocol's
selection/calibration separation and be frozen before model evaluation.

Short-depth tasks offer substantial independent-fire replication. Depth14/horizon7
has only 28 candidate test fires; depth30/horizon7 has one. Those are sparse for
multi-region/year/size subgroup claims or capacity/tuning comparisons. No universal
minimum acceptable sample threshold is invented. Higher-level independent clusters
may be fewer still; prefixes and future outcomes remain correlated within fires.
Median/max windows per fire and geographic/year strata are measured in the CSVs.

## Preliminary power-planning inputs, not empirical power

We now have true fire/run/window counts and cluster sizes. Paired model-loss variance,
minimum scientifically meaningful effects, cluster dependence and training variability
remain unknown. Therefore empirical predictive power and a numerical minimum
detectable scientific effect are not reported. Under an explicitly hypothetical
independent-fire normal approximation, a standardized paired detectable difference
would scale as (z_(1-alpha/2)+z_power)/sqrt(n_test), not 1/sqrt(n_windows). That formula
requires a justified design, multiplicity family and variance before numerical use.

Task A uses depth3/horizon1. B/C/D use depth3/horizon3 as candidate mathematical
support. C compares supported future versus observed historical growth reference;
its scientific decision criterion needs to stay separate from mean successive
future differences. D can use future population SD. E proposes depth3/horizon7
future-pattern query/gallery support. Query/gallery fires must be disjoint; same-fire
candidates are forbidden. Relevance cannot be defined by embedding coordinates,
and future-pattern similarity is not validated ecological analog discovery.

The 296 unmatched native IDs permit source-native support analysis but lack catalog
strata. Report both all-native and catalog/cache-matched populations; do not silently
attach guessed metadata. Model labels, outcome evaluation and training remain off.
'''
(b/'scientific-feasibility.md').write_text(feas)
(b/'unsupported-claims.md').write_text('''# Unsupported claims after real profiling

- Learned embedding, PCA, supervised/SSL/multitask predictive benefit or agent competence: no models trained.
- Empirical predictive power, paired loss variance, calibrated uncertainty or a scientifically meaningful effect size.
- Operational forecasting: source date bins are retrospective and true availability is unknown.
- Complete ignition-to-extinction records, or zero growth on absent dates.
- Native sensor QA, known error magnitudes, high quality inferred from missing flags, or causal interpretation of selection bias.
- Scientific equivalence of similarly named area/cumulative fields or unrelated products.
- Verified ecological regions, native CRS transformations, valid geometry/environment associations or ecological analog retrieval.
- Catalog metadata for the 296 unmatched native IDs, or claims that all sources share one fire denominator.
- Independently verified external approval receipts: execution used explicit direct user approval instead.
- Public release/redistribution, newly granted third-party rights or source relicensing.
- Global 40GB raster/encoder throughput: measured census used four relevant containers, not climate arrays.
- Filesystem physical I/O bytes: checksum byte scope and logical records are reported separately.
- Reviewed final experimental splits: delivered folds are explicit candidates.

Supported claims are source-identity-verified native/cache census and exact-calendar
mathematical support counts, with replicated deterministic metadata outputs. These
are not independent ecological/scientific validation of every downstream target.
''')
# Bind named native fields to observed identity evidence, without fabricating findings.
provenance={'authorization':json.loads((b/'direct-execution-authorization.json').read_text()),'sources':c['source_identity'],'binding_version':'native-profiling-v1','native_event_key':'integer id preserved; decimal-string crosswalk follows upstream documented builder','native_observation_date':'native date field retained; only exact calendar dates or midnight bins supported','native_daily_value':'dy_ar_km2 retained unchanged; no calibration or missing-value imputation','cache_fields':{'fire_id':'documented decimal string of native id','timestamp':'native date comparison only, not operational availability','ring_area_km2':'exact numeric hashes match native daily field on every overlap','cumulative_area_km2':'finite/nonnegative count only; no scientific interchangeability with native catalog totals'},'native_order':'read-only SQLite ORDER BY id,date,fid, temp_store MEMORY with256MiB SQLite heap cap','cache_order':'streamed grouped fire IDs, within-fire date sort; reappearing IDs fail on unique fire metadata key','source_refs':'native fid or cache row offset; full-container checksum in census provenance; per-fire/run evidence hashes','duplicates':'all copies of duplicate native dates excluded from supported runs; duplicates remain counted','missingness':'no gap filling, interpolation or zero substitution','source_value_storage':'daily values only in bounded memory; derived persistent products contain cohort metadata, source references and hashes','quality':'unknown native measurement QA and uncertainty','availability':'unknown, retrospective claims only','external_publication':False,'model_training':False}
(b/'real-data-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
# Confirm source identities still have their verified size/mtime after both executions.
lake=Path('../fire_vase/data_lake/fire-vase-data-lake-v0.1')
for rel,v in c['source_identity'].items():
 st=(lake/rel).stat();assert (st.st_size,st.st_mtime_ns)==(v['bytes'],v['mtime_ns'])
(b/'source-postflight.json').write_text(json.dumps({'all_source_stats_match_verified_identities':True,'files':4,'source_modifications':0},indent=2)+'\n')
print('Wrote census, reconciliation, selection, feasibility, provenance and unsupported claims.')
