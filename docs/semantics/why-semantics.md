# Why semantics matter

A column named `height` can describe an individual plant, a plot statistic, a canopy
surface or an instrument's encoded measurement. Converting centimetres to metres
solves a numeric problem. It does not tell us which height was measured, how it was
obtained or whether another observation represents the same quantity.

## Sources already carry useful meaning

A source might supply a persistent concept identifier, a definition, a controlled
standard name, a sampling protocol, a taxon identifier or an instrument identity.
Discovery should retain these as evidence with their location and semantic resource.
A missing ontology annotation is allowed; a missing definition is an explicit gap,
not permission to invent one.

For Sentinel B08, the stored DN, documented scale/offset, band description, sensor,
platform, native CRS and pixel resolution matter together. The calibrated unit `1`
does not mean the stored DN is already reflectance. Discovery records the native
calibration metadata; the harmonization module decides and executes the recipe.

## Preserve useful variety

Taxonomy, anatomy, traits, observations, environment, quantities and provenance need
different semantic systems. [PCO](landscape.md#pco) helps describe organism groups;
[GeoSPARQL](landscape.md#geosparql) addresses spatial relationships;
[QUDT](landscape.md#qudt) addresses quantity/unit structure;
[PROV-O](landscape.md#prov) records derivation. None alone establishes a scientifically
justified transition from leaf measurements to a landscape representation.

## What a successful mapping must explain

Which source concept and version were used? What entity, property, method and support
does it describe? Which relationship is proposed to the target? What meaning could
be lost? Which evidence supports that relationship, and who reviewed it?

The answer can be narrower, broader, related, convertible, derived, incomparable or
unknown. Harmonization is allowed to preserve a difference or abstain. An approved
mapping must never erase its source concept.

[Key distinctions](distinctions.md) · [Glossary](glossary.md) · [Review workflow](review-workflow.md)
