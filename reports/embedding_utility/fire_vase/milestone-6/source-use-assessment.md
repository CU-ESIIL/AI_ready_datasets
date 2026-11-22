# Source-use, identity and attribution assessment

Status: **NEEDS_EVIDENCE; not a legal determination or scientific approval.**

## Package identity and locality

The user's local lake is present, including the selected native/derived source files.
The package manifest reports release `fire-vase-data-lake-v0.1`, created2026-08-12,
642 inventory files and40,318,128,369 bytes. These are package-reported totals, not a
new byte scan of the entire archive. Historical package mode says `manifest`, but
the selected `files/` artifacts are physically present now. Current file sizes match
the recorded inventory. No upload or rebuild is required.

The [metadata inventory](review-v2/metadata-evidence.json) records exact paths,
reported full-container SHA values, current sizes, Parquet footers and GeoPackage
schema/CRS metadata. Reported checksums agree with the earlier inspected source
evidence; **current complete file contents were not rehashed**. Metadata-file hashes
are not data-file hashes. The package builder commit, current upstream code identity
and historical v2/validation analysis commits are distinct provenance scopes.

| Source | Intended use | Current rights/identity finding |
| --- | --- | --- |
| Native daily GeoPackage | Verify `id/date/dy_ar_km2` and native event-day semantics | File present; inventory SHA reported; original dataset terms/field definitions/current full hash need review |
| Native event GeoPackage | Reconcile event IDs/boundaries, catalog denominators and evaluation-only strata | File present; not an increment source or an operational forecast field |
| Cached `vase_slices.parquet` | Check exact source/cache identity and native-value survival | Footer626,102 rows, one row group; cannot treat one row group as a safe read bound |
| Cached `fire_traits.parquet` | Source reconciliation and later evaluation-only strata | Footer278,569 rows, one row group; endpoint/legacy peak fields cannot be predictors |
| gridMET / completed developmental products | Not needed for the initial audit | Explicitly excluded from this review scope; no inherited permission or scientific compatibility |

Fresh schemas alone do not prove value equivalence, uncertainty or rights. Stage1
must verify actual source bytes and bounded key/value checks only after appropriate
review. No row-level validation is claimed from this metadata inspection.

## Authoritative online evidence

- Dataset landing page configured by upstream:
  [CU Scholar FIRED record](https://scholar.colorado.edu/concern/datasets/d504rm74m).
  Access returned HTTP403 during this review; no dataset-specific license or terms
  were verified from that page and no archive was downloaded.
- Method/citation context:
  [Balch et al. (2020), FIRED, Remote Sensing12,3498](https://doi.org/10.3390/rs12213498).
  The publisher identifies this **article** as CC BY4.0. That is not evidence that
  the inspected cached dataset/version has the same license. The article describes
  an earlier CONUS product; do not silently equate it with this later CONUS/AK cache.
- Local package README and upstream release config explicitly retain FIRED/gridMET
  source-specific access, citation and reuse obligations. The MIT software license
  does not relicense source observations.

Proposed citation string, pending dataset-release confirmation: Balch, J.K.; St. Denis,
L.A.; Mahood, A.L.; Mietkiewicz, N.P.; Williams, T.M.; McGlinchy, J.; Cook, M.C. (2020).
*FIRED (Fire Events Delineation): An Open, Flexible Algorithm and Database of US Fire
Events Derived from the MODIS Burned Area Product (2001–2019).* Remote Sensing12,3498.
DOI10.3390/rs12213498. Also cite the **actual dataset release/accession**, creators and
required source-product acknowledgments once confirmed; the article alone is not a
complete dataset attribution decision.

## Required human evidence

Confirm internal research use, permitted processing/derivatives, attribution text,
restrictions on model/embedding/checkpoint release, publication of aggregate diagnostics
and any observation redistribution. No observations, embeddings or trained real models
will be publicly committed without a separate release review. Public accessibility,
local possession and software/article licenses do not resolve dataset-specific rights.

Known source uncertainty includes retrospective event delineation, estimated burn
dates/areas, unresolved observation availability and unknown original pixel-QA/error
survival. Review whether native daily-bin assignments support the intended target
and how to label retrospective results. No new weather or geometry equivalence is
proposed in this stage. Metadata/current identity checks and scientific permission
remain separate from a human's actual review decision.
