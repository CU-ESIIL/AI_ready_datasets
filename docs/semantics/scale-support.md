# Scale and support are first-class scientific properties

**Scale is not one dimension.** Biological organization, taxonomic rank, spatial
resolution, spatial extent, temporal cadence and averaging support must be described
separately. An ontology identifier for an organism does not determine where or for
how long a measurement applies.

## Spatial distinctions

| Property | Question | Example |
| --- | --- | --- |
| Location | Where is the referenced thing? | Pixel center coordinate |
| CRS | How are coordinates referenced? | Native EPSG:32613 versus geographic EPSG:4326 footprint |
| Resolution | What detail or spacing is declared? | 10 m pixel spacing |
| Footprint | What area/geometry is associated with the observation? | Native pixel bounds or sensor response area |
| Support | Over which domain/weighting does a value apply? | Plot average, sample area or sensor integration footprint |
| Extent | What total domain is covered? | Scene bounding box or study region |

A shared coordinate or overlapping polygon does not establish comparable support.
GeoSPARQL can help describe geometry and spatial relationships; it does not define
the biological or statistical justification for averaging values across those areas.

## Temporal distinctions

A timestamp might mark acquisition, processing, publication or an interval's center.
Reporting cadence differs from duration and averaging support. A daily series can
contain daily means, instantaneous samples or incomplete observations; the method
and metadata must distinguish them. Instantaneous records may have equal start/end
and never receive an invented duration to satisfy a schema.

OWL-Time offers temporal relations and structures. It does not alone decide whether
two values with matching timestamps have comparable temporal supports.

## Transformations require justification

Aggregation must specify membership, weighting, completeness, target support and
uncertainty behavior. Downscaling requires explicit modeling assumptions; smaller
output cells do not become independent observations. Cross-scale scientific claims
need source evidence, a versioned recipe, tests and human review when consequential
or uncertain. A provenance graph records the claim without proving it valid.

[Biological organization](biological-organization.md) · [Research gap](gaps.md) ·
[Glossary](glossary.md#scale-and-support) · [CF guidance](https://cfconventions.org/faq.html)
