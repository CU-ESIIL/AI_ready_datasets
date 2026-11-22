# Track B — real-data audit and objective selection

**Physical source availability verified; approved experiment-specific use unresolved.**
See [inspection metadata and evidence hashes](data-access-audit-m4-v1.json).

The release manifest's `included: true` does not prove current checkout availability.
The expected Fire VASE local cache/table roots are absent. Its documented legacy
CubeDynamics roots contain ~257 MB event and ~575 MB daily GeoPackages plus
`vase_slices.parquet`, `fire_traits.parquet` and developmental features. Parquet footer
and GeoPackage schema/catalog metadata were inspected; no feature/observation rows.
No archive download, full raster/table read or source-file copying occurred.

Schemas expose event/fire IDs, timestamps, slice indices, ring/cumulative area,
cache/source versions, geometry CRS and quality/climate availability fields. Upstream
metadata reports reconstructed dates and gaps, but does not establish when values
became operationally available. Historical manifest checksums are pointers, not
fresh full-file verification. Existing manuscript folds and fitted products cannot
serve automatically as fresh experiment splits.

Repository MIT code licensing does not establish FIRED/gridMET data rights. An
experiment-specific source/access/license/attribution manifest, reviewed native
ring/cumulative/daily support mapping, source/checksum verification, quality handling
and availability evidence remain missing. No real training or ecological claim is
made. The typed `RealPrefixApproval` is a record interface, not a source adapter or
scientific permission.

Selected objective: predict the next calendar-day observed growth from a dated,
available prefix. It offers independently held-out outcomes without inventing analog
relevance or new geometry semantics. Operational real prediction needs stronger
availability evidence; retrospective reconstructed prediction must be labeled
separately. Until review, the implementation executes explicitly synthetic future-
observation controls only. Spatial/environmental objectives and expert analog
retrieval remain unsupported; no synthetic relevance labels replace them.
