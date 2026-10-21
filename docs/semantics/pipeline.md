# Semantic evidence in the pipeline

The implemented boundary is **discover data + discover semantic evidence →
interpret/map/harmonize → represent**. Discovery preserves what the source says;
Module 2 decides which scientific relationships are supported.

![Data discovery and semantic evidence discovery jointly produce SourceResource metadata for Module 2; ontology and vocabulary resources support retrieval without supplying approved mappings.](../assets/figures/discovery.svg)

*Detailed Module 1 boundary. No raster data is read by semantic discovery.
[Figure source](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/scripts/generate_figures.py).*

## Input and output

`discovery.run(request, client, semantic_registry=None)` retains the existing
metadata-search interface. It filters candidate sources, rejects conflicting
metadata, and returns new source records enriched with `SourceSemantics`. The
client's immutable resources remain unchanged. A catalog match or a retrieved
concept is not an approved `SemanticMapping`.

The existing `SourceResource` identity/access/version/integrity fields remain,
alongside typed `Rights`, `Support`, `Metadata` and `Variable` records. Its new
optional `semantics` field contains:

- `SemanticEvidence`: optional source definitions, identifiers, vocabulary, units,
  quantity/entity/property/matrix/context hints, taxa, methods, protocols, sensor,
  platform and spatial/temporal metadata, plus type/location/documentation/confidence.
- `ConceptCandidate`: identifier, label, resource, optional definition, retrieval
  basis, evidence and confidence. There is no approval or equivalence field.
- Extractor identity and a digest of the complete source record before enrichment.

Absent semantics is omitted from serialized output, preserving old source and
plan identities. Enriched sources get a different identity and cannot silently
reuse products under old identities. Existing annotations are preserved and stale
source/evidence bindings are rejected. Full source records already survive in
provenance; streaming products retain metadata and compact observation/window lineage.

## Evidence types and candidate bases

The shared vocabulary is `SOURCE_DOCUMENTED`, `OBSERVED_IN_DATA`,
`DERIVED_DETERMINISTICALLY`, `MODEL_JUDGMENT`, `HUMAN_DECISION`, `MISSING_EVIDENCE`.
Discovery currently parses metadata without model calls. Normalized adapter fields
are marked deterministic, because their prose may not be a literal native statement.
Native STAC fields have explicit source locations. Model hints, if supplied by an
adapter, remain model judgments and cannot be relabeled as deterministic matches.

Candidate bases distinguish an exact source annotation, a normalized metadata
identifier, exact vocabulary-label retrieval, lexical retrieval and model inference.
Even an exact identifier retrieval is only a candidate for Module 2's intended
scientific relationship. No label match establishes equivalence.

## Semantic-resource access

`SemanticResourceRegistry` indexes the local inventory and declared concept records.
It implements `search`, `lookup`, `describe`, `relationships` and `source`, plus
resource-level search. Configured resolver adapters follow `SemanticResolver`.
No external portal is silently contacted and no ontology graph is downloaded.
Failures propagate; there is no live-to-fixture fallback.

The shipped concept records use explicitly synthetic URNs. OBO Foundry, OLS,
BioPortal, EcoPortal, AgroPortal and TDWG are potential adapter providers, not newly
implemented live services. The small namespace index identifies declared resource
references; it does not establish concept existence, crosswalks or equivalence.

## Sentinel regression

`data/fixtures/semantics/sentinel_source.json` is an explicitly **generated metadata
fixture**, using the historical item `S2B_13TDE_20230715_0_L2A` for context. Its native
metadata supplies platform `sentinel-2b`, instrument `msi`, band `B08`, common name
`nir`, scale 0.0001, offset −0.1, documented unit `1`, 10 m resolution, native
EPSG:32613, processing type `S2MSI2A`, baseline `05.09`, SCL asset metadata and a
license link. Access URIs are intentionally nonresolving. No pixels were retrieved.

The stored variable stays `B08_DN` with unit `DN`. The documented band unit belongs
to the calibrated quantity; extraction never applies the coefficients. STAC common
name `nir` is not invented into a CF standard name. The fixture's license does not
license real Sentinel data. Missing temporal resolution remains missing; the source
acquisition stays instantaneous.

```sh
prototype discover-semantics data/fixtures/semantics/sentinel_source.json \
  --output run/sentinel-semantic-evidence.json
```

The actual Sentinel planning path now enriches metadata in the same way, without
changing the scientific target, deterministic calibration, model vetoes or human
gates. MESA remains an unverified adapter boundary. Legacy snapshots remain historical.

## Module 2 and Module 3 remain separate

Human/scientific comparison produces a proposed relationship and supporting evidence.
Approved scientific transformations belong in versioned recipes, with deterministic
QA and human decisions as required. The discovery layer does not create those
approvals. MOSAIKS still consumes harmonized raster outputs only and preserves
canonical meaning, encoder identity and source/recipe/review lineage.

[Contract schemas](../reference/contracts.md) · [Discovery module](../discovery.md) ·
[Review workflow](review-workflow.md) · [Tests](../testing.md)

## Deterministic backbone and model trust

VERDE interprets, selects, parameterizes, compares and proposes. It does not author
scientific computation. New model plans select closed, source-bound capabilities;
metadata coefficients and mathematical operations are resolved by tested code.
Schema validation, scientific checks, existing vetoes and human decisions remain
separate gates. Approved recipes execute without a model. See
[deterministic execution and model trust](../architecture/model-trust.md) for the registry, IR contracts,
examples, provenance and current limits.
