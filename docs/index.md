---
hide:
  - navigation
  - toc
---

<div class="research-hero" markdown>
<div class="hero-copy" markdown>
<p class="eyebrow">ESIIL · Research infrastructure prototype</p>

# From environmental observations to AI-ready science

Scientific data carry a history: where a measurement was made, what it means,
and how it can be used. That history should survive every transformation.

We are exploring how specialist agents and human judgment can turn a scientific
question into a traceable dataset—streaming approved observations directly into
machine representations.

[Explore the approach](approach.md){ .md-button .md-button--primary }
[Read the documentation](documentation/index.md){ .text-link }

</div>
<figure class="hero-earth">
<img src="assets/blue-marble-2002.jpg" alt="NASA composite of Earth’s western hemisphere, showing oceans, continents and cloud systems" width="800" height="800">
<figcaption>Blue Marble, 2002 · NASA’s Earth Observatory.<br><a href="image-credits/">Image source and usage</a></figcaption>
</figure>
</div>

<p class="eyebrow">The scientific problem</p>

## Data can be accessible and still be difficult to use together

A satellite pixel, a vegetation measurement and a water sample observe different
things at different scales. Similar names do not make them interchangeable.
Combining them requires evidence about units, methods, spatial support, timing
and rights. Those decisions are often hidden in a researcher’s preprocessing code.

Our research question is whether that work can become explicit, repeatable and
reviewable, while retaining the distinctions that make observations scientifically useful.

## One question. Three accountable stages.

![System architecture: a question enters discovery, then governed harmonization, then representation and downstream science. Human review precedes execution.](assets/figures/system.svg)

*Discovery identifies sources; harmonization establishes supported transformations;
representation produces machine features. [Figure source](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/scripts/generate_figures.py).*

**Discover.** Find candidate observations and preserve their native metadata, source
versions, access constraints and licenses. A catalog match is evidence to inspect.

**Harmonize.** Specialists assess a frozen recipe within defined scientific domains.
Deterministic checks and human review govern what can execute. Uncertainty or
disagreement stops the stream.

**Represent.** Read bounded windows only after approval. Apply the reviewed recipe
in memory, then feed harmonized raster outputs into MOSAIKS. Keep vectors and
compact lineage; avoid saving raw or harmonized raster datasets.

[Follow the full approach →](approach.md)

<div class="editorial-band" markdown>
<p class="eyebrow">Different observations, distinct meanings</p>

## Bring data into relation without erasing its context

The architecture accommodates field, sensor and remotely sensed observations.
The current real-data work concentrates on Sentinel-2 metadata and bounded access.
NEON metadata access is implemented; authenticated observation processing remains
unfinished. MESA is an adapter boundary awaiting verified integration.

[Explore data and integration status →](data.md)

</div>

## Discover what the source says its data mean

Sources may already reference an ontology, controlled vocabulary, standard name,
protocol, taxon identifier or unit system. The discovery layer preserves that
semantic evidence before harmonization begins. It composes scientific communities’
existing systems and keeps source identifiers and definitions intact.

Module 1 discovers evidence and candidate concepts. Module 2 interprets their
relationships; retrieval is never approval of scientific equivalence.

[Explore the semantic landscape and glossary →](semantics/index.md)

## Shared infrastructure, independent scientific questions

Food security and water security are configuration namespaces over a shared core.
Their scientific assumptions and products remain separate. A third track stays
undefined until scientists specify its question, evidence and reviewed rules.
These tracks are research scaffolding; we have not validated food or water outcomes.

[See how science tracks work →](science.md)

## A stopped run is a useful result

The Sentinel prototype produced real model-backed proposals and rejected reviews.
Specialists repeated concerns outside their domains, including unsupported claims
about negative reflectance and licensing. No approved real Sentinel MOSAIKS dataset
was produced by those runs.

That evidence motivates scoped reviews, explicit missing-evidence states and a
separate integrity reviewer. Generated MOSAIKS tests demonstrate numeric usability,
with held-out diagnostics and baselines; they do not establish ecological validity
or native language-model understanding.

[Read the Sentinel case study →](development/sentinel-review-refactor.md)

## Toward reusable, inspectable scientific datasets

The intended impact is less repeated data preparation and more visible scientific
judgment. Success means that another researcher can inspect a dataset, understand
its limits, and trace a vector through its harmonized observation, recipe and
review decisions back to the source asset and its rights.

[Research goals and limits](impact.md) · [What works today](PROTOTYPE_STATUS.md) ·
[Build and verify the prototype](documentation/index.md)
