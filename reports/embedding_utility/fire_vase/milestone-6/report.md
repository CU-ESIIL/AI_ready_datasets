# Milestone 6 — real-source contract and approval boundary

**Completed authorized preapproval work. Real-row evaluation PENDING HUMAN REVIEW.**
21 November 2026. Historical M1–5 artifacts and upstream Fire VASE are unchanged.

## Local data found

The user's lake is present at `fire_vase/data_lake/fire-vase-data-lake-v0.1/files/`.
The selected daily/event GeoPackages and cached slices/traits Parquet files physically
exist, with current sizes matching the package inventory. There is no data-availability
or GitHub-upload requirement. Earlier audits established legacy-path presence and
expected-root absence; the user's correction identified this packaged canonical root.

Read the lake README, manifest, file inventory and reported checksums, plus fresh
Parquet footers and GeoPackage schema/catalog/CRS metadata. The package reports642
files/~40.3 GB; this is a historical inventory total, not a new full-archive scan.
**No observation rows were read, copied or decoded; no data archive was downloaded.**
Current complete data bytes were not rehashed. Exact paths, current sizes, historical
SHA values, schema/CRS evidence and metadata/document digests are retained in
[metadata-evidence.json](review-v2/metadata-evidence.json).

## Scientific findings from documentation/code inspection

- Upstream `normalize_daily` copies `dy_ar_km2` to `ring_area_km2` and constructs
  cumulative sums. Another product uses a same-named cumulative field sourced from
  catalog totals. Source names/units cannot establish universal equivalence.
- Corrected v2 validates exact calendar-day adjacency and duplicate ambiguity,
  preserving missingness rather than zero-filling. Historical source/cache alignment
  checks were performed upstream; they are not fresh verification of these bytes.
- Native feature tables use custom SRS100000, not the coexisting EPSG4326 metadata
  entry. No geometry read, reprojection or spatial-support change is proposed.
- Source date/area uncertainty and pixel-QA survival remain unresolved; cached climate
  availability flags do not establish burned-area quality.
- Upstream documentation identifies retrospective end-of-day reconstruction, not
  demonstrated operational availability. Real dates cannot be given synthetic
  midnight availability to make existing prefix contracts run.
- The public dataset landing page returned403. The article's CC BY license and code
  MIT license do not resolve this dataset release's processing/redistribution terms.
  See the [source-use assessment](source-use-assessment.md) and
  [public evidence record](public-source-evidence.json).

## Concrete review packet and validation work

The [approval packet](approval-packet.md) binds exact datasets, reported identities,
intended analysis, proposed versioned recipes, uncertainties, rights/attribution,
validation and publication implications. Packet digest:
`8be26eec72f9fb711569994cbb5cb8e2c3339b5c156037e8779a597b0570135a`.

It proposes only a **retrospective native-value alignment audit**: at most512 total
decoded source rows,16 fires, batches≤128; no geometry/full scan, raw/harmonized
persistence, training or redistribution. Row caps are logical/application scope;
future reader design must also account for page/batch memory and physical I/O.
Both inspected Parquet tables have one row group, so reading one group is not a
bounded sample. Incomplete fragments must not be treated as complete event prefixes.

New typed contracts distinguish source identity, proposed recipe, claim mode,
scientific review jurisdictions, actual container verification and a human decision.
Pure validators test support, missing versus observed zero, source/event identity,
review invalidation and known/unknown availability. They contain **no source-row
reader, real adapter or training entrypoint**. A technical evidence result is not
execution permission and cannot authenticate a human record.

All seven draft review jurisdictions remain **NEEDS_EVIDENCE**, not FAIL or PASS.
No human decision has been fabricated. The [review template](review-v2/review-template.json)
is bound to the packet digest; [preconditions](review-v2/preconditions.json) remain
incomplete. Current full-container verification must match the expected reviewed
identity before any decoded row. Neither this packet nor the old RealPrefixApproval
is a runtime HumanDecision or scientific execution authorization.

## Conditional real study and manuscript

The [scientific contract](scientific-contract.md) distinguishes daily-bin area,
physical rate, cumulative/catalog totals, calendar gaps, missing/zero, event identity,
native support, uncertainty, QA, rights and availability. Proposed recipes are
`m6-review-v1`, PROPOSED_FOR_REVIEW; no scientific transformation was executed.

The [cohort/evaluation plan](cohort-and-evaluation-plan.md) retains mean/persistence,
optimized raw/summary ridge, train-only PCA, the existing small TCN and matched MLP,
real validation/calibration and whole-fire/year/region/support/size/stage holdouts.
Only supported future A–E tasks would run. No completed-fire normalization, future
weather or test-fitted preprocessing. Actual observational error remains distinct
from predictive calibration, and future cost measurements must include real loading,
construction, storage, training, caching and heterogeneous reuse.

Historical upstream aggregates show severe long-history selection (about3.68% of
its catalog has ≥3 consecutive observations); they are not new M6 cohort counts.
Current cohort size, selection differences, predictive error, transfer, retrieval
and real workload costs remain **unmeasured**, not zero. A prospective cohort remains
blocked by missing availability evidence unless that evidence is supplied; a later
retrospective study needs an explicit reviewed scope change.

[Manuscript-ready provenance/design sections](manuscript-evidence.md) keep mathematical,
synthetic, real scientific, real-agent, theoretical and pending evidence distinct.
[Unsupported claims](unsupported-claims.md) explicitly withhold all unexecuted empirical
results. No model architecture grew and no synthetic benchmark was expanded; generated
unit cases only validate the real-source integration preconditions.

## Verification and next boundary

20 new offline tests cover digest binding, human versus agent review, domain vetoes,
current checksum requirements, bounded scope, support/missing/zero/quality survival,
unknown availability, and validation with source file access disabled. Full relevant
suite: **359 passed, two skipped**; strict documentation build passed. Earlier frozen
output hashes and the clean upstream checkout are checked separately.

The first metadata-only audit wrote its evidence but failed while recording relative
code paths; it is preserved under `review-v1` as an incomplete development artifact.
The corrected metadata audit is [review-v2/manifest.json](review-v2/manifest.json).
Neither attempt read observation rows or constitutes a scientific sample.

**Next step is human review of the concrete packet**, not automatic source ingestion.
The Milestone 6 request explicitly says “Do not read observation rows until the required
approval is established.” [AGENTS.md](../../../../AGENTS.md) separately requires human
review of uncertain meanings and rights. The local lake location resolves access to
files, not those scientific-use decisions. After review, any adapter/sample, cohort/
training and public release must stay within its separately authorized scope.
