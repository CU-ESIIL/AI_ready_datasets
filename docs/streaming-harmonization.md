# Metadata consensus and streaming embeddings

The first target is **Sentinel-2 L2A B08 reflectance using the asset's documented
scale and offset**, preserving native pixel and acquisition support. This path
separates metadata planning from data access. It does not create raw snapshots or
persist harmonized observations. Existing `acquire-sentinel`, fixture runs, and
standalone `harmonize`/`encode` commands retain their historical materializing
behavior; use the commands below for the streaming workflow.

## Legacy specialist dialogue

`plan-stream` queries Earth Search collection and Item metadata only. Native STAC,
processing baseline, NIR/SCL access locations, calibration coefficients, source
rights/attribution, and a fixed scientific target enter a `StreamPlan`. Its checksum
scope is **metadata**, not raster bytes. The first demonstration samples one native
pixel per candidate scene at a caller-specified coordinate, with at most ten scenes.

Four separate OpenClaw/Verde specialists analyze semantics, units/calibration,
spatial/temporal support, and rights. A recipe builder reads their actual messages.
Every specialist and adversarial QA then reviews the same frozen recipe digest,
replying to its draft and at least one peer finding. Revisions must answer every
previous review. All five must agree without outstanding concerns, and deterministic
QA must pass. There is no majority override. Rejection, abstention, invalid output,
or exhaustion of the bounded revision rounds blocks execution.

Keep the consensus directory alongside embedding outputs: it holds the dialogue
and full model-task traces referenced by recipe evidence.

Dialogue, each round's recipe/votes, prompt/response traces, final consensus,
encoder specification, and an execution contract are persisted as metadata. Agent
messages are structured, sequential exchanges through a shared transcript; these
are separate tool-free model calls, not independent autonomous tool-using workers.
The gateway's response scope remains normalized plugin-validated JSON.

## Evidence-bound review before real execution

The newer [scoped review](review/index.md) is an additional required gate for real
Sentinel streaming. Its report binds the complete source set and scientific recipe,
contains the curated evidence and all six specialist findings, and records an
explicit QA synthesis decision. Execution recomputes evidence/status checks rather
than trusting a serialized eligibility label. Missing evidence, a specialist failure
or a QA veto blocks access. Existing legacy consensus and human gates remain in
force; this additive migration does not erase earlier vetoes.

Prepare a `ReviewBundle` with the exact recipe and `sources`, a `source_digest`
computed by `review.source_set_digest`, intended operation, evidence and fixture flag:

```sh
prototype review-metadata run/review-bundle.json --output run/scoped-review
```

The actual Sentinel example remains blocked. The required report cannot be produced
by inventing missing evidence or editing a failure into a pass.

## Access and embedding execution

After consensus, scoped evidence review and human review, `stream-embed` checks exact plan/recipe/encoder
binding **before opening the source iterator**. Rasterio reads one NIR window and
one SCL window per candidate; HTTP range access transfers the necessary compressed
COG blocks. This still transfers bytes over the network and uses bounded in-memory
caches; it does not mean zero-byte access. No full-scene download, local raster
cache, raw-value JSON snapshot, or harmonized-data file is part of this path.

SCL classes 4, 5, and 6 are accepted; DN nodata zero and other classes stop the run
explicitly. There is no interpolation or synthetic fallback. The allow-listed
`calibrate` operation computes `reflectance = DN * scale + offset`, with exact
coefficients checked against source metadata. Scalar uncertainty is multiplied by
`abs(scale)`; calibration-parameter uncertainty/covariance is not modeled. Output
is not clipped to [0,1], and this step does not claim field/pixel equivalence.

A synchronous microbatch (default 32, maximum 1024 records) passes through the
executor directly into the encoder and sink. The source is advanced only when the
previous batch has been written. Joins, temporal aggregation, and track transforms
are refused before data access because their bounded scientific streaming semantics
have not been defined here. Stream samples carry an increasing sequence per binding;
producers must provide stable record identities. No unbounded global duplicate-ID
index is kept. Memory scales with metadata, bounded dialogue, encoder, and batch
size, rather than total sample count.

`embeddings.jsonl` contains vectors and content identities. `lineage.jsonl` contains
source record/asset IDs, native indices/CRS and actual pixel footprint, time, quality flag and calibrated uncertainty,
metadata/version references, extracted-window evidence hashes, recipe, QA, human,
consensus, and encoder references. Neither file serializes raw/harmonized observation
objects. Source metadata and licenses remain in `data_access_plan.json`. The vector
is necessarily a derived data product; the reference identity encoder exposes the
calibrated scalar itself. An evidence hash does not permit recovery of discarded
raw values or prove complete remote-asset immutability.

This command retains **reference numeric features**, identity scalar or scalar
plus square. The separate [MOSAIKS raster path](mosaiks-embeddings.md) implements
empirical convolutional features over harmonized windows. Neither claims a
universal latent space; encoder settings and preprocessing remain explicit.

Output streams use `.partial` filenames until exhaustion. `manifest.json` marks
completion or failure; interrupted/failed runs retain partial evidence without
claiming a complete product. There is no resume/deduplication protocol yet.

## Commands

Install the existing `real` extra for rasterio. Use the already configured isolated
OpenClaw runtime described in [OpenClaw and Verde](openclaw-verde.md).

```sh
prototype plan-stream run/real-sentinel/request.json \
  --longitude -105.586 --latitude 40.0329 --max-items 1 \
  --output run/sentinel-stream-plan.json
prototype consensus run/sentinel-stream-plan.json \
  --max-rounds 2 --output run/sentinel-stream-consensus
```


If the first draft is malformed, it is rejected and retained rather than repaired.
An explicit retry may reuse its four verified metadata analyses for the exact same
plan and model. If a valid first draft exists but its first review failed, that
draft can also be reused while all five reviews run afresh. The failed response
is retained in the audit artifacts; new calls receive its failure reason rather
than treating rejected claims as peer findings. No failed response is repaired or
treated as an accepted proposal:

```sh
prototype consensus run/sentinel-stream-plan.json \
  --analysis-from run/sentinel-stream-consensus \
  --output run/sentinel-stream-consensus-retry
```

Inspect `review_summary.md`, `consensus.json`, `dialogue.jsonl`, `proposed_recipe.json`, and
`qa_report.json`. Consensus does not approve a scientific recipe. A scientist must
review the concrete proposal, set its recipe status to `approved` in a separate
file, and record a decision against that **exact approved file**. Do not edit the
mappings, operations, or proposal content after consensus; scientific edits need a
new consensus. Do not manufacture a reviewer identity or approval.

```sh
prototype review run/scientist-approved-recipe.json \
  --reviewer '<actual reviewer>' --rationale '<scientific review rationale>' \
  --decision approved --output run/scientist-decision.json
prototype stream-embed run/sentinel-stream-plan.json run/scientist-approved-recipe.json \
  --review run/scientist-decision.json \
  --consensus run/sentinel-stream-consensus/consensus.json \
  --evidence-review run/scoped-review/report.json \
  --output run/sentinel-stream-embeddings
```

Offline tests use generated iterators and tiny in-memory STAC responses, with
network access forbidden. They exercise calibration, invalid coefficients,
uncertainty, revision dialogue, bounded disagreement, stale consensus, pre-access
review gates, early sink writes, ordered sequences, failure manifests, and lazy
window access without downloading test datasets. These checks do not establish
ecological validity or scientific suitability of an encoder.

## Live verification — 2026-10-21

`run/sentinel-stream-plan.json` was built from real Earth Search metadata for
`S2B_13TDE_20230715_0_L2A` near the configured NIWO example coordinate. No raster
was opened. The documented coefficients were scale 0.0001 and offset -0.1.

The first draft omitted mandatory units and used an invalid operation source
reference; it was rejected and retained. A fresh draft passed validation. An
initial self-citing review was rejected, and a later context-budget failure was
diagnosed and corrected using the installed OpenClaw schema.

The completed run is `run/sentinel-stream-consensus-bounded/`. All five reviewers
returned actual Verde `js2/gpt-oss-120b` plugin-validated responses, replied to a
peer, and reviewed the same recipe digest. All requested revision. The pre-veto
deterministic assessment found no coefficient mismatch and required human review;
final deterministic QA enforced the model revision veto and rejected execution.
No model-proposed real-data harmonization or embedding was executed.

Several model claims conflict with supplied metadata or executor evidence,
including assertions that uncertainty scaling/masking are undefined and that
clipping is automatically required. Rights-related claims about the catalog's
proprietary label, and claims linking reflectance values to usage-policy breaches,
are model judgments, not verified legal or scientific conclusions. Failed-review
text had been included as retry context in this live run; future calls retain it
in audit files and pass only the failure reason, reducing repeated rejected-claim
anchoring. Scientific evaluation and renewed recipe/model review remain necessary;
this run demonstrates real dialogue and enforced gates, not scientific consensus.

That historical run was checked with the then-current 94-test suite. The
expanded suite is described in [testing](testing.md); current strict builds also pass. Direct calibrated streaming
is verified with generated offline streams; the real calibrated stream remains
unexecuted pending revision, consensus and an actual human decision. The active
isolated runtime is left available for subsequent work.
