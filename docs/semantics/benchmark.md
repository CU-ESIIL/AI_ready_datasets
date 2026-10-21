# Semantic benchmark: project metadata diagnostics

This first benchmark uses the local landscape inventory and source metadata. It
does not load ontology graphs, determine term equivalence, infer biological
compatibility or measure held-out scientific performance. The filenames retain
`ontology_*` for the requested interface, but the inventory also contains standards,
thesauri, classifications and frameworks.

## Run offline

```sh
python -m pip install -e '.[semantics]'
prototype semantic-benchmark --output outputs/semantic_benchmark
```

The default inputs are 86 inventory records, the two existing generated source
metadata records and the generated Sentinel semantic fixture. No source observations,
COG blocks, external portals or models are accessed. To use other **already available
source metadata**, pass one or more `--sources` JSON paths containing validated
`SourceResource` records. Live acquisition remains an explicit separate workflow.
Existing output directories are refused; preserve prior runs and choose a fresh path.

## Exact output contracts

| File | Grain and interpretation |
| --- | --- |
| `ontology_metrics.parquet` | One resource; assessed coverage, known/unknown dimensions, candidate flag, verification scope; term count stays null |
| `ontology_pairs.parquet` | One unordered resource pair; weighted assessed-scope overlap, not concept/axiom equivalence |
| `benchmark_coverage.parquet` | Resource × dimension, enum rating, diagnostic weight and assessment ID |
| `semantic_gaps.parquet` | Dimension coverage counts plus an explicitly unmeasured cross-support research hypothesis |
| `dataset_metrics.parquet` | One complete versioned source-resource record, including fixture flag, metadata evidence kinds and field presence |
| `dataset_ontology_edges.parquet` | Declared annotation namespace references with evidence type/location; concept existence and equivalence are not evaluated |
| `dataset_pairs.parquet` | Source-record pair; metadata-field presence overlap and shared declared resource references, with comparability not evaluated |
| `dataset_rankings.parquet` | Deterministic ordering by metadata field presence, then asset ID and full source identity |
| `recommended_portfolio.json` | Greedy assessed-coverage suggestion for human review, with budget, marginal gains and unresolved claims |
| `run_manifest.json` | Status, schema/config/code identity, input/output hashes, timestamp, source metadata identities, counts and limitations |

All eight Parquet tables have explicit schemas, including zero-row edge/pair tables.
Each is reopened and compared after writing. Failures retain a failed manifest and
partial files; they cannot be described as a completed benchmark. No raw/harmonized
observations are persisted.

## Scoring formulas

Inventory ratings use **strong = 1**, **partial = 0.5**, **indirect = 0.25**,
**not target = 0**. Unknown stays null in the coverage table and contributes no
assessed gain. Resource coverage score is the sum divided by all 21 dimensions;
known and unknown counts remain separate. The weights are project choices, not
empirically measured ontology quality.

Resource-pair overlap is `sum(min(left, right)) / sum(max(left, right))` over
mutually known dimensions. A zero denominator yields null, not perfect similarity.
This compares assessed coverage profiles, not shared classes, axioms or compatibility.

Source documentation score is the fraction of 27 declared semantic-metadata fields
present anywhere in the source record's factual/deterministically parsed evidence.
Model judgments, human decisions and missing-evidence placeholders do not boost
that score. The score does not validate correctness, representativeness, rights or
scientific suitability. The row grain is a source asset/version metadata record,
not necessarily an entire provider collection.

Dataset pairs use set Jaccard on field presence; two empty sets yield null. Shared
namespace references stay distinct from accepted mappings. Units are never guessed
into QUDT links and variable names never become ontology links through lexical resemblance.

The portfolio greedily maximizes additional assessed coverage with equal dimension
weights, within `--budget` (default eight). Core-candidate status then resource ID
break ties. Unresolved/historical/inactive-registry records and unverified reference
leads are excluded from this heuristic. Selection is not scientific adoption and
cannot authorize harmonization. Domain priorities may require a different reviewed
objective; this initial diagnostic does not infer them.

## Reproducibility and limits

Input and code digests bind each run. Dates and file hashes identify a concrete run;
logical metrics are deterministic for the same validated inputs. Bounds are 256
resources and 128 source records to keep pairwise metadata comparisons small.
JSON/CSV input files are capped at 8 MiB and total planned metadata at 16 MiB.
The source reader is never opened. No claim is made about large-scale graph reasoning,
ontology completeness, semantic alignment accuracy or native AI understanding.

See the [comparison matrix](comparison.md), [inventory assessment records](assessments.jsonl),
[semantic gap](gaps.md) and [implementation schemas](../reference/contracts.md).

## Retained-source run from this development pass

The delivered `outputs/semantic_benchmark/` was run with two existing synthetic
source metadata records and one **real Sentinel source metadata record retained from
the earlier EarthSearch plan**. This is different from the generated-only default.
The initial generated-only run was preserved under `run/semantic-benchmark-initial/`.
No new external data request or raster read was made.

The delivered run contains 86 resource rows, 3,655 resource pairs, 1,806 resource ×
dimension assessments, 22 gap/hypothesis records, three source records, one declared
STAC namespace association, three source pairs and three documentation rankings.
Two source records carry `fixture: true`; the retained Sentinel record does not.
The manifest identifies the exact input files, full hashes and diagnostic scope.
This run does not change the earlier blocked Sentinel harmonization decision.

## Read the diagnostics in context

The [ontology research framework](ontology-benchmarking.md) describes breadth,
depth, composability and accumulation tests. The [dataset research framework](dataset-benchmarking.md)
describes explicit use, potential, diversity, leverage and candidate pairs. Those
profiles have not been computed by these outputs. Rankings remain documentation
presence diagnostics, not a universal best-dataset leaderboard.
