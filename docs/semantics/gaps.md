# Semantic gaps and open research

The central hypothesis is a need for more explicit scientific justification of
**cross-scale and cross-support transformations**. This is a project research area,
not a claim that no ontology or literature already addresses it.

## Describe a thing versus justify a transformation

Existing resources offer substantial capabilities for entities, properties,
observations, environments, geography, time, units and provenance. The difficult
question is how to record why a specific scientific transformation is justified:

```text
individual leaf measurements
  → species trait distribution
  → community trait distribution
  → plot-scale property
  → 30 m remotely sensed observation
  → landscape representation
```

Each arrow can introduce sampling, membership, statistical, physical or modeling
assumptions. A list of entity labels and part-of relations does not supply those
assumptions. A plot and a pixel can overlap while observing different quantities
with different response functions.

## What must be compared

For each transformation, inspect source/target entity definitions, population or
community membership, methods, sampling design, spatial/temporal weighting,
completeness, uncertainty, transfer assumptions and validation evidence. Distinguish
a proposed derivation from observed data. Record the exact reviewed recipe and
human decision where required.

PCO, GeoSPARQL, OWL-Time, QUDT and PROV-O can each contribute useful descriptions.
None alone proves a cross-support derivation scientifically justified. The
[inventory's limitations](landscape.md#resource-details-limitations-and-evidence)
are provisional scope assessments, not declarations that those resources cannot
be extended or composed.

## Continued literature review

Investigate existing observation-support models, statistical aggregation semantics,
remote-sensing response models, ecological sampling models, scientific workflow
provenance and evidence/argumentation frameworks. Compare actual axioms and worked
examples before proposing a project concept. The [Bari Manifesto](https://www.vliz.be/imisdocs/publications/322519.pdf)
and [OBOE](https://github.com/NCEAS/oboe) are relevant precedents, not an exhaustive review.

The benchmark's `semantic_gaps.parquet` counts assessed inventory coverage and records
this hypothesis as **not measured**. It cannot establish the absence of an external
ontology or rank the scientific validity of transformations.

[Conservative new-concept decision process](review-workflow.md#do-we-need-a-new-concept) ·
[Proposed semantic profile](profile.md)
