# Track B — data access and selected objective

**Real source files exist; no approved real training cohort was established.**
The [machine-readable audit](data-access-audit-m4-v1.json) records exact paths,
inspection hashes and metadata scopes. No observation/feature rows were read.

The pinned Fire VASE release config says `included: true` for external inputs, but
its current checkout lacks those expected cache/table roots. Documented legacy
CubeDynamics roots contain the event GeoPackage (~257 MB), daily GeoPackage
(~575 MB), source lakehouse Parquet and developmental products. This is physical
availability, not experiment approval. No large archive is loaded or copied.

Inspected Parquet footers and GeoPackage catalog/schema metadata only. Relevant
identifiers include fire/event ID, slice index, timestamp, ring/cumulative area,
source/cache version, geometry CRS and climate/quality availability fields.
The schemas/manifests preserve source provenance but do not by themselves establish
ring-to-day support, source-specific reuse permissions or operational availability.
Reported historical hashes are evidence pointers, not fresh verification of entire
large local files. Cached date coverage must not be inferred from filenames.

The MIT repository code license does not relicense FIRED/gridMET inputs. Upstream
release guidance explicitly retains their citation/reuse obligations. A new
experiment-specific source/version/checksum, rights/attribution and support mapping
manifest is still required. Availability at model issue time is unresolved: upstream
v2 state is explicitly retrospective end-of-day reconstruction, not demonstrated
operational access. Existing global PCA, published folds, cohorts and manuscript
results are not reused as new held-out outcomes or training artifacts.

Repository governance requires: “Human review is required for consequential/uncertain
decisions, novel equivalence, low confidence, agent disagreement, support changes,
ambiguous meaning and rights.” See [AGENTS.md](../../../AGENTS.md). No assistant-issued
approval or inferred cumulative/ring equivalence replaces that evidence.

## Objective choice

| Option | Feasible evidence now | Decision |
| --- | --- | --- |
| Next observed-day growth from prefixes | Typed dated histories and independent subsequent synthetic observations; real availability unresolved | Implement and execute synthetic controls; real prospective validation pending |
| Ecological analog retrieval | No independently reviewed relevance/future-outcome labels for this experiment | Do not invent ecological labels |
| Timing plus geometry prediction | Geometry exists in unapproved source products; new support/association definitions needed | Defer spatial learning; no invented spatial robustness |

Select the first option because it gives a falsifiable outcome independent of the
encoder's input summary/PCA objective. Learning predicts an actual subsequent
synthetic observation under a declared generator; it does not reconstruct an input
profile or mimic PCA. Those outcomes are **mathematical controls**, not independent
wildfire or ecological evidence.

`PrefixInput`, `PrefixOutcome`, `RealPrefixApproval` and the closed synthetic training
config provide the preprocessing/training/evaluation boundary. The real approval
contract is an inert evidence record, not a data reader or scientific permission.
No automatic Parquet ingestion or synthetic fallback is added. Real ingestion
requires a reviewed bounded/streaming adapter and explicit prospective or
retrospective-only claim appropriate to actual availability evidence.
