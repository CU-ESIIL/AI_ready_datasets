# Documentation

Start with the system’s scientific boundaries, run a small example, then inspect
contracts and implementation. This documentation is maintained as Markdown in the
same repository as the code. The public site renders that source.

## Choose a path

| Your goal | Start here | Continue with |
| --- | --- | --- |
| Understand the project | [Approach](../approach.md) | [Core concepts](../concepts.md), [current status](../PROTOTYPE_STATUS.md) |
| Understand the architecture | [System architecture](../architecture.md) | [Current-state audit](../architecture/current-state.md), [typed contracts](../reference/contracts.md) |
| Build and run | [Complete offline example](../examples.md) | [Streaming](../streaming-harmonization.md), [OpenClaw / Verde](../openclaw-verde.md) |
| Assess the science | [Harmonization](../harmonization.md) | [Evidence review](../review/index.md), [provenance](../provenance.md), [science tracks](../tracks.md) |
| Extend the implementation | [Extension guide](../reference/extending.md) | [Module map](../reference/modules.md), [contracts](../reference/contracts.md), [design decisions](../development/decisions.md) |
| Verify a dataset or change | [Tests and builds](../testing.md) | [MOSAIKS integrity and held-out diagnostics](../mosaiks-embeddings.md), [Sentinel review case](../development/sentinel-review-refactor.md) |

## Semantics: a major project resource

Explore the [ontology landscape](../semantics/landscape.md),
[glossary](../semantics/glossary.md), [coverage matrix](../semantics/comparison.md)
and [human comparison workflow](../semantics/review-workflow.md). The inventory
informs discovery without letting Module 1 approve mappings. The
[benchmark](../semantics/benchmark.md) produces auditable metadata diagnostics.

## The three module boundaries

**Discovery & access** accepts a scientific request and produces candidate source
resources with native metadata and access evidence. It does not establish semantic
compatibility. [Discovery](../discovery.md) · [Data sources](../data-sources.md)

**Harmonization & review** turns evidence into versioned allow-listed recipes,
review decisions and canonical observations. Model judgments never grant execution
permission. [Harmonization](../harmonization.md) · [Scoped review](../review/index.md)

**Representation** accepts harmonized outputs and produces vectors with model,
preprocessing and observation lineage. [Reference encoders](../representations.md) ·
[MOSAIKS](../mosaiks-embeddings.md)

## Execution modes

Offline generated examples are the reproducible default. Live discovery and model
inference are explicit commands; unavailable services never silently become mocks.
New real raster paths stream bounded windows. Historical snapshot commands remain
separate. Read [real-data status](../real-data-agents.md) before using a live workflow.

## Choose your route

Scientists can start with [biological organization](../semantics/biological-organization.md)
and [support](../semantics/scale-support.md). Semantic-data experts can inspect the
[filterable landscape](../semantics/landscape.md), [ontology research framework](../semantics/ontology-benchmarking.md)
and [dataset framework](../semantics/dataset-benchmarking.md). Engineers can follow
[typed contracts](../reference/contracts.md), [module APIs](../reference/modules.md)
and [verification](../testing.md). All routes connect to the
[human review workflow](../semantics/review-workflow.md).
