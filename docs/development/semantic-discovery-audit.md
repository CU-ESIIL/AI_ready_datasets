# Semantic discovery audit

Inspected 2026-10-21 before this pass: README, AGENTS, Material navigation and
technical/narrative pages; frozen contracts and generated schemas; discovery,
fixture/MESA transport, Sentinel STAC planning and legacy acquisition; provenance,
streaming gates, MOSAIKS, tests, examples, fixtures, tracks and decision history.
The working tree contains earlier uncommitted review/MOSAIKS/website work; retain it.

## Existing boundaries and concrete gap

`discovery.run` accepts a request and metadata-search client. It filters space,
time, modality and declared variable identifiers, returns candidate sources, and
does not approve equivalence. `SourceResource` already has identity, access, version,
rights, support and nested `Metadata`/`Variable` contracts. Variables carry definition,
unit, method, entity and one optional ontology ID. Native Sentinel metadata survives
as JSON with checksum scope, but semantic annotations have no typed extraction or
candidate-resource interface. MESA is explicitly unavailable; no API is guessed.

`stream_sources.plan_sentinel` reads STAC metadata only and proposes a fixed target;
calibration executes later in harmonization. Existing review/human gates must remain.
`real_data` snapshot acquisition is historical. `provenance.export` serializes full
source contracts; additive source semantics can therefore survive to representations.
Module 2 owns `SemanticMapping`; Module 3 consumes harmonized outputs only.

## Focused response

Add optional nested source semantics with serialization preserving old identities
when absent. Deterministically extract only declared metadata, distinguishing stored
DN from documented calibration-output units. Return candidates without mapping or
approval fields. Provide a local semantic-resource index and adapter protocol rather
than downloading ontology graphs or binding core code to one portal.

Add a source-maintained landscape inventory, separately auditable project assessments,
generated master table/matrix, glossary and review workflow. Retain all requested
resource categories, including ambiguous historical leads with explicit unresolved
identity/status/rights. Neither coverage scores nor lexical overlap proves scientific
compatibility. The requested Parquet benchmark is a metadata diagnostic unless a
separate scientifically reviewed evaluation protocol is supplied; no raw data reads.

## Verification baseline

122 existing offline tests and a strict Material build passed before this pass.
Existing fixture source checksums and old serialized plan/context identities need
backward-compatibility tests. New tests cover partial/invalid contracts, annotation
preservation, candidate provenance, Sentinel extraction and the discovery/mapping
boundary. Full offline tests, generated reference, strict build and rendered links
remain final requirements. No linter/type-checker is configured.
