---
hide:
  - navigation
---
# Observations retain their identity

The [local management workbench](management-workbench.md) makes source/semantic
metadata, recipes, dataset artifacts, resource plans and recovery inspectable
together. It indexes generated MOSAIKS outputs without persisting raw/harmonized
windows. Planned products and quotas remain distinct from diagnostic artifacts.

Environmental research connects observations collected with different instruments,
methods and purposes. We preserve those differences through discovery, harmonization
and representation. Modality describes how an observation was made; scale describes
its spatial or temporal support. Neither establishes equivalence.

## Sources in the prototype

| Source or path | Evidence and current status | Important limit |
| --- | --- | --- |
| Generated field and satellite fixtures | WORKING offline pipeline and tests | Explicitly synthetic; no ecological validation |
| Sentinel-2 L2A via EarthSearch STAC / COG | PROTOTYPE live metadata, historical tiny pixel reads, bounded streaming reader | Actual model reviews blocked approved real MOSAIKS execution |
| NEON | PROTOTYPE public metadata / authenticated file-access boundary | Normalized live observation processing pending; token required |
| MESA | PLANNED verified service integration | Adapter stub, not a deployed discovery service |
| Other biological and environmental sources | PLANNED architecture scope | No integrated source claimed from a fixture |

[Source-specific details and licenses](data-sources.md) · [Live versus fixture workflows](real-data-agents.md)

## Stream the observation; keep the evidence

The new harmonization path uses bounded native windows and direct encoder consumption.
It does not save raw or harmonized raster datasets. Tests use generated iterators.
Legacy snapshot demonstrations remain explicitly historical workflows.

A metadata checksum identifies the metadata record. Per-window hashes identify the
extracted evidence read during execution. Neither establishes a checksum for the
entire remote raster. Native CRS, pixel indices, masks and calibration metadata
remain attached to lineage.

## Accessible does not mean unrestricted

Review records source-specific terms, attribution, versions and intended operations.
Unknown permissions require evidence and human review. Copyright, privacy,
Indigenous data sovereignty and access restrictions remain source-specific questions.
A catalog’s license label cannot substitute for the authoritative terms.

[Rights and provenance](provenance.md) · [Streaming implementation](streaming-harmonization.md)

## Data management planning

The [data-location report](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/output/pdf/AI_ready_data_management_report.pdf)
and [editable inventory](https://github.com/CU-ESIIL/AI_ready_datasets/tree/main/reports/data_management)
map retained artifacts and transient processing separately. The report identifies
backup, retention, archive, access and model-processing decisions that the project
still needs to assign. It does not establish new storage infrastructure. Repository
links become available when the local report changes are published.
