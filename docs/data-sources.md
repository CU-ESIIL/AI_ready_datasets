# Target data sources

The prototype targets heterogeneity across modalities and scales, not arbitrary
generic tables. Real integration requires code that retrieves **and processes**
actual provider data. Current fixtures do not meet that definition. No provider
records are redistributed in this repository.

| Source | Contribution / modality | Spatial / temporal scale | Access boundary | Current status and rights considerations |
| --- | --- | --- | --- | --- |
| NEON | Field, organismal, sensors, airborne; vegetation/environment | Organism/plot/site/landscape; product-specific intervals | Future product metadata/API adapter | Synthetic field fixture plus live public product metadata; token CSV adapter implemented, authenticated acquisition/normalization pending; preserve CC BY 4.0 and product citation |
| LTER | Independently designed ecological observations | Plot/ecosystem; long-term series | Future dataset-specific catalog/repository adapter | Planned; schemas and licenses differ by dataset |
| NASA ORNL DAAC | Biomass, carbon, gridded Earth observations | Site/regional/global; product-specific | Future product-specific access adapter | Planned; preserve product/version, spatial support, citation and rights |
| AmeriFlux | Carbon/water/energy flux and meteorology | Tower/ecosystem; subdaily to long-term | Future network/product access adapter | Planned; cross-network definitions and licensing need verification |
| TRY | Organismal/species plant traits | Organism/species; observation-specific time | Future permitted-subset adapter | Planned; taxonomic identity, trait method, units and reuse permission require review |
| CartograPlant | Spatial botanical observations | Organism/geographic; record-specific time | Future contributing-resource adapter | Planned; preserve contributing source rights; no blanket reuse assumption |
| Landsat | Satellite imagery | Pixel/landscape/continental; sensor acquisitions | Future STAC discovery and windowed raster access | Planned; sensor, processing level, cloud masks and asset rights remain explicit |
| Sentinel-2 | Satellite imagery | Pixel/landscape/continental; sensor acquisitions | Earth Search STAC metadata and bounded COG windows; direct stream-to-encoder path | Live native STAC discovery and actual NIR/SCL pixel-window reads verified; DN/scale/offset/sensor/support retained; fixtures remain for CI |

Except for the verified Sentinel and documented NEON boundaries described in the
[live workflow](real-data-agents.md), these are target access mechanisms rather
than verified provider integrations. Before using real data, record the precise source URI, format, access
method, version, license, derivative/redistribution permissions, and citation.
Unclear rights require human review. Do not bulk-download archives into git.
Use the [metadata consensus and streaming path](streaming-harmonization.md) for
new Sentinel harmonization: documented scale/offset is applied in the reviewed
executor, with no raw or harmonized dataset files. Historical snapshots remain
explicit legacy examples.

## Vertical slices and scientific boundaries

1. NEON + Landsat or Sentinel: demonstrate actual field-to-raster spatial and
   temporal support alignment. Start with a few sites and a short available period;
   example sites/time belong in configuration, never in core code.
2. NEON + AmeriFlux or TRY: test cross-network quantity definitions or cross-scale
   biological context. Do not join traits to sites by species name alone.
3. NEON + ORNL DAAC: test site-to-regional context and spatial support, beyond a
   nearest-neighbor join.

Food and water tracks may select shared vegetation, traits, environmental, flux,
or satellite resources for different questions. Source identity remains separate
from scientific use. The third track's scope stays configurable. None of these
future scientific use cases is currently encoded as a validated domain model.

## Fixture policy

The six committed test records are project-authored synthetic normalized contracts, dedicated
to the public domain under CC0-1.0 as stated in fixture metadata. They do not claim
to reproduce native NEON or Sentinel schemas. Original identifiers, methods,
platform/sensor, support, and source-specific rights survive ingestion. Additional
native-schema-compatible fixtures for LTER, ORNL DAAC, AmeriFlux, TRY, CartograPlant,
and Landsat remain planned; do not create empty files or imply coverage.
