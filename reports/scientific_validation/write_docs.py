"""Generate scientist-facing validation findings from retained measured outputs."""
from pathlib import Path
import json
HERE=Path(__file__).parent;ROOT=HERE.parents[1];D=HERE/'data';DOC=ROOT/'docs/validation';DOC.mkdir(exist_ok=True)
load=lambda p:json.loads((D/p).read_text())
S=load('sentinel_review_gap_analysis.json');C=load('canonical_benchmark.json');N=load('neon_sentinel_case.json');V=load('model_experiment/summary.json');G=load('resource_depth.json');DS=load('dataset_benchmark.json')
repo='https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/'
def link(path,label='artifact'):return f'[{label}]({repo}{path})'
def write(name,s):(DOC/name).write_text(s.strip()+'\n')
write('index.md',f'''# Scientific validation: what can we justify?

Environmental data differ in their meaning as well as their file formats.
Existing semantic systems describe different parts of those meanings. Bounded AI
can help navigate the choices, while tested operations execute only reviewed plans.
We can now measure failures and identify decisions that still need scientists.

This 22 October 2026 pass measured three real vocabulary graphs, specified 25
canonical observations, investigated 18 candidate metadata records and their 153
pairs, and completed 100 live Verde calls. These objects have different evidence
scopes; their counts do not establish ecological validity.

- [Sentinel expert package](sentinel-real-case.md) retains ten issue records and every historical veto.
- [Semantic and dataset experiments](benchmarks.md) separate graph measurements from provisional scope assessments.
- [NEON + Sentinel case](neon-sentinel.md) proposes environmental context, not measurement equivalence.
- [Verde constraint experiment](verde-experiment.md) shows why valid JSON is not enough.

{link('output/pdf/AI_ready_scientific_validation_report.pdf','Read the separate 20-page scientific validation report')}
and {link('reports/scientific_validation/README.md','rebuild its 18 figures and evidence packages')}.
Repository links require publication of the local changes; no deployment is claimed.

No real scientific release was approved. No new raster or NEON observation files
were downloaded. Small public vocabulary graphs and product/site metadata were
retrieved explicitly and retain attribution, versions where declared, and hashes.
The older [pipeline-state report](../pipeline-state-report.md) remains a dated
historical snapshot; its unmeasured claims describe the earlier audit.
''')
rows=['| Issue | Jurisdiction | Current resolution path |','| --- | --- | --- |']
for g in S['blockers']:rows.append(f"| `{g['blocker_id']}` | {g['review_jurisdiction']} | {g['proposed_resolution']} |")
write('sentinel-real-case.md',f'''# Prepare the real Sentinel case for expert review

The retained case is `{S['case_id']}`. Historical QA requested revision; the
original report and model criticisms remain unchanged. This analysis cannot lift
a veto or create human approval.

## What software checked

Native raster CRS is EPSG:32613; geographic footprint coordinates use EPSG:4326.
The native band coefficients are scale 0.0001 and offset −0.1, and acquisition
support is instantaneous. The recipe's calibration and rename operations are
registered. These checks do not establish downstream scientific suitability.

## What the objections mean now

The native-CRS objection is technically supported and needs corrected proposal
wording. The [official Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice)
provides evidence for lawful distribution/modification and required notices, but an
expert still needs to bind terms and attribution to the intended product.

The demand for a whole-raster checksum is unsupported by this project's bounded
streaming contract: metadata and window hashes intentionally have narrower scopes.
That does not prove remote immutability. Preserve the criticism and adjudicate
residual integrity risk explicitly. Do not download an entire raster to satisfy an
unsupported interpretation of provenance requirements.

Historical evidence pointers are not valid under the later strict source-pointer
validator. Rebuild evidence and repeat reviews, rather than editing the historical
model outputs. Independent quality criteria and any inferential claim need expert
acceptance and appropriate independent data.

{chr(10).join(rows)}

## Expert decision package

{link('outputs/scientific_validation/sentinel_review_gap_analysis.json','Machine-readable issue ledger')}
retains original findings, cited/current evidence, classification, technical support,
software/documentation/expert requirements, execution necessity and proposed action.
The {link('outputs/scientific_validation/sentinel_proposed_recipe.json','version-2 draft recipe')}
adds a correction proposal while preserving old proposals and the original consensus veto. Its old content digest intentionally remains stale, so deterministic QA blocks execution until renewed review.

Use the {link('outputs/scientific_validation/expert_decision_template.json','per-issue decision form')}
to approve, reject, revise or request evidence. Every choice is initially null.
This form is **not** a runtime `HumanDecision`; execution still requires matching
fresh consensus, scoped evidence review, resolved vetoes and an explicit exact-recipe
human decision. Any scientific edit invalidates the corresponding approval.
''')
opt='; '.join(f"size {r['size']}: {r['coverage']:.1%} ({', '.join(r['resources'])})" for r in C['exact_best'])
graphrows='\n'.join(f"| {r['resource_id']} | {r['named_classes']} | {r['max_longest_root_depth']} | {r['median_shortest_root_depth']} | {r['restrictions']} |" for r in G)
write('benchmarks.md',f'''# Measured semantic-resource and dataset experiments

## Resource scope and canonical observations

The new analysis retains 2,408 evidence-linked assertions for 86 resources across
28 requested dimensions. Known legacy scope judgments map to an ordinal rubric;
new unsupported dimensions remain null. Zero means not-targeted in the assessed
scope, not proven absence of a concept. All scope scores remain PROJECT ASSESSMENT,
with provisional confidence and no fabricated expert review.

Twenty-five observations have explicit requirement IDs. Exact best-set enumeration
through size three yields {opt}. The objective counts repeated dimension
requirements with at least meaningful assessed scope. It does **not** measure
exact term expressibility, equivalence or ontology quality. Longer accumulation
curves are greedy witnesses; they do not prove minimal sets beyond size three.

Exact SOSA term presence is measured separately in `canonical_term_witnesses.json`.
Presence is a building-block witness, not an approved scientific mapping.
Subdomain accumulation, marginal gain, resource-pair overlap, unknown dimensions,
threshold failures and complete-case exploratory PCA are retained independently.
No missing values are imputed as zeros.

## Real graph structure

| Local snapshot | Named classes | Longest named-class depth | Median shortest root depth | Restrictions |
| --- | --- | --- | --- | --- |
{graphrows}

These are explicit local triples, not imported or inferred closures. SOSA/SSN
modeling patterns and external superclass references are not summarized by local
named-class depth. SSN's explicit SOSA import is verified; other inventory
relationships retain their weaker declaration provenance. Identifier resolvability,
I-ADOPT compatibility and semantic crosswalk correctness remain unmeasured.

## Candidate dataset diagnostics

The 18 records include product/network descriptions, a standard comparator and an
unselected climate counterpart. They are not 18 integrated datasets. Each source statement has primary evidence and scope; dimension and field-presence
coding are separately labeled PROJECT ASSESSMENT. Undocumented fields remain unknown.

Semantic diversity is a documented dimension lower bound, not variable count.
The ontology-potential diagnostic counts proposed resource relationships and is a
PROJECT ASSESSMENT. Formal ontology references are distinguished from standard use.
Eight separate review-prioritization rubrics and all 153 pair diagnostics are
available. Ties have no scientific standing; mixed documentation scope confounds
ranking. Pairwise added dimensions do not grant scientific compatibility.

{link('data/semantics/validation/dataset_inventory.json','Evidence inventory')} ·
{link('outputs/scientific_validation/canonical_benchmark.json','Canonical results')} ·
{link('outputs/scientific_validation/resource_depth.json','Graph measurements')} ·
{link('outputs/scientific_validation/dataset_benchmark.json','Dataset and pair diagnostics')}.
''')
write('neon-sentinel.md',f'''# NEON + Sentinel: retain the differences

The proposed bounded case uses NIWO air temperature (DP1.00002.001) in July 2023 as
environmental context for instantaneous Sentinel B08 NIR reflectance. Air temperature
is not reflectance, and tower support is not pixel support.

## Evidence supporting candidate selection

Public NEON product metadata confirms NIWO availability for July 2023; the retained
Sentinel scene footprint contains the public site coordinate. This is one eligible
metadata-backed candidate, not an optimized site ranking. Exact release/file
membership remains to be verified.

The historical Sentinel planning point is approximately
{N['coordinate_diagnostic']['old_planning_point_to_public_site_coordinate_m']/1000:.2f} km
from the published NEON site coordinate. Neither is a selected sensor coordinate.
A site centroid cannot establish tower height, air-sensor position, footprint or
spatial colocation. No NEON observation files were acquired; the process token is
absent and the legacy download method is not used by this streaming case.

## The proposed scientific relationship

NEON documents one-/thirty-minute averages of aspirated air-temperature observations
at multiple heights. Sentinel supplies instantaneous 10 m optical pixels. The review
must specify sensor, height, source units, interval convention, quality/uncertainty,
spatial relationship and intended ecological interpretation without equating them.

The registered Sentinel calibration/rename recipe fragment is preserved. The NEON
branch is unbound because source observations and sensor-aware normalization are
missing. A reviewed interval-to-instant contextual association is not registered;
`observation.join_exact` requires equal supports and is inappropriate here.
No model is asked to invent an operation, equation or matching rule.

**Stop at the data, method and expert gates.** The
{link('outputs/scientific_validation/neon_sentinel_case.json','complete proposed review package')}
records what/where/when/how, available operations, meaning lost if forced equal,
missing capabilities and decisions needed before implementation or execution.
''')
write('verde-experiment.md',f'''# Live Verde constraint experiment

The pilot completed {V['call_counts']['total']} calls over 25 tasks and two repeats
using the configured Verde `js2/gpt-oss-120b` model through isolated OpenClaw
2026.5.18. {V['call_counts']['returned']} responses returned; two failures remain
retained and were not repaired or replaced.

## Arms and interpretation

- A captures free natural-language content inside the JSON text envelope required
  by the installed plugin; it is not a fully unconstrained provider baseline.
- B requests the closed decision schema over offered operations/concept IDs.
- C deterministically validates the same B outputs using scenario preconditions
  and authoritative-parameter references; it is not an extra model sample.
- D adds a pending human gate; it cannot execute without actual approval.

All 50 B outputs passed their schema. Fourteen failed deterministic scenario checks,
and none of the 50 supplied an evidence-ID citation. Thirty-six passed scenario
checks, including abstention/review dispositions; this does not mean 36 validated
scientific transformations. The citation metric tests reference presence/membership,
not natural-language truth. Six of six operation-target examples selected the
expected operation, but this did not satisfy evidence requirements.

Strict agreement with the assistant-drafted reference was 37/50. **This is not
human-gold scientific accuracy.** A separate
{link('data/semantics/validation/expert_gold_template.json','blank expert gold form')}
is required. Prose correctness and unsafe-proposal rates need blinded human coding.
Zero scientific executions in every arm is an enforced design property, not evidence
of model competence. The weaker-model hypothesis and inter-model disagreement
remain untested by this single configured model.

Exact prompts, schemas, normalized outputs, failures, task IDs, repeat IDs, elapsed
latency and provider/model are retained. Token cost and weight digests are not
exposed by this plugin and remain unknown. Original `started_at` fields were recorded
after receipt in this runner version; elapsed durations are retained correctly.

{link('reports/scientific_validation/data/model_experiment/summary.json','Measured summary')} ·
{link('reports/scientific_validation/data/model_experiment/calls.jsonl','Exact inert call records')}.
No output is passed to eval, exec, shell, SQL, dynamic imports or scientific execution.
''')
print('Generated five evidence-linked validation pages')

# Website uses three measured figures from the same report definitions.
import shutil
for fig in ['04_depth','13_neon_sentinel_support','16_constraint_results']:
 target=ROOT/'docs/assets/figures'/('validation-'+fig+'.svg')
 shutil.copyfile(HERE/'figures'/(fig+'.svg'),target)
for page_name,figure,alt in [('benchmarks.md','04_depth','Named classes and explicit local hierarchy depth in three real vocabulary snapshots'),('neon-sentinel.md','13_neon_sentinel_support','Published site and historical planning coordinates; neither identifies the selected sensor'),('verde-experiment.md','16_constraint_results','Schema validity, scenario checks, evidence citation and draft reference agreement in the live pilot')]:
 p=DOC/page_name;s=p.read_text();first,rest=s.split('\n',1);p.write_text(first+'\n\n!['+alt+'](../assets/figures/validation-'+figure+'.svg){ .validation-figure }\n'+rest)
