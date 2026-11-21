# Embedding utility study

Status: **UNDER ANALYSIS**. Draft v0.2, 20 November 2026. First generated diagnostics run; no agent or independent scientific evaluation.

**Core question: is a materialized embedding layer worth it when agents can already
work with source data through tools?** Agent effectiveness is a testable premise.
Compare the same agent with direct-data access, embedding consumers and both,
against deterministic references, accounting for correctness and the full lifecycle.

Start with the [agent-versus-embedding framework](protocol/agent-versus-embedding.md).
The [earlier raster comparison plan](protocol/study-plan.md) is a supporting
experiment, not the full study. MOSAIKS is a first case; broader modalities require
separate evidence. No finite study establishes universal usefulness.

This analysis is separate from pipeline design, historical validation reports and
science tracks. It changes no operation, source integration or scientific gate.

- [protocol/](protocol/study-plan.md): questions and draft analysis plan.
- [cases/](cases/TEMPLATE.md): unapproved task definitions and scientific decisions.
- [results/](results/README.md): generated diagnostic results and compact run evidence.

[Website overview](../../docs/analysis/embedding-utility.md).
Future reusable code belongs in `src/dataset_prototype/`, tests in `tests/`, tiny
synthetic fixtures in `data/fixtures/`. Transient runs belong in ignored
`run/embedding_utility/<run-id>/`. Never persist raw/harmonized raster datasets.
The offline `run_first_benchmarks.py` runner uses existing MOSAIKS and synthetic inputs.
No downloads or model inference occur.

[Benchmark mathematics and graph guide](protocol/benchmark-math.md) ·
[First generated findings](results/first-benchmarks.md).

## Primary proposed scientific case: Fire VASE

The [Fire VASE implementation plan](fire_vase/README.md) develops the user proposal
into metadata × representation × agent comparisons using a pinned upstream audit.
The original proposal, reference assessment and inert pilot inventory are retained.
No new fire-data ingestion, integration, agent inference or neural training has run.
The generated MOSAIKS benchmarks remain supporting harness diagnostics.
