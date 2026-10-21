---
hide:
  - navigation
---
# Make scientific preparation inspectable and reusable

The research goal is to reduce repeated data preparation while exposing the judgments
that shape a dataset. A useful system should help scientists understand a product’s
meaning, reproduce its transformations and know when it is unsuitable for their question.

## What success would look like

A researcher starts with a question, inspects source evidence and reviews an explicit
harmonization recipe. Once required decisions are complete, approved observations
stream into a representation dataset. Another researcher can trace each representation
back to observations, decisions, source versions and rights.

![Representation lineage connects harmonized observations, optional track recipes, core transformations, reviews, source assets and metadata versions and rights.](assets/figures/provenance.svg)

*Lineage is part of the product, including applicable human decisions.
[Figure source](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/scripts/generate_figures.py).*

## What the prototype establishes today

Offline tests exercise deterministic execution, review gates, immutable source reuse,
streaming boundaries and MOSAIKS verification. Live integrations have produced metadata
and actual model proposals. Rejected Sentinel reviews remain visible evidence of the
system’s limits. There is no approved real Sentinel MOSAIKS release or validated food
or water decision-support product from those runs.

## Questions we still need to answer

How can evidence curation become reliable at greater scale? Which independent tasks
and labels establish usefulness for each scientific community? What governance is
needed for sensitive or restricted observations? Which changes require a scientist
rather than a new automated rule?

These are research questions. The current architecture provides reviewable places
to record answers as evidence improves.

[Inspect current status](PROTOTYPE_STATUS.md) · [Read the case study](development/sentinel-review-refactor.md) ·
[Contribute through GitHub](https://github.com/CU-ESIIL/AI_ready_datasets)
