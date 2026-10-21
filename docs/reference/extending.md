# Extend the prototype without changing the science silently

An extension begins with a scientific definition and a verified interface. The
existing three modules stay independently callable. This guide describes extension
points; it does not claim that unimplemented sources or scientific operations work.

## Add a source

**Problem and input.** Identify the measurements, methods, native support, source
versions and intended use. Verify official service documentation and deployed
schemas. Check whether MESA already provides discovery/access/metadata before
adding a transport. Do not guess endpoints or implement a second catalog needlessly.

**Metadata output.** Normalize candidates into `SourceResource`: stable asset and
dataset identity, version, URI, variables with quantity definitions/units/methods,
support, native metadata, provenance and source-specific rights. Preserve native
STAC or equivalent evidence. State checksum scope; a metadata digest cannot be
presented as a whole-data checksum. Unknown meaning or rights stays unknown.

**Discovery interface.** `discovery.run(request, client)` calls `client.search`
and validates `SourceResource` candidates. The historical `AccessClient` protocol
also declares `describe` and a materializing `fetch`; do not implement a new real
stream by accumulating an entire asset to satisfy that legacy return type.
`MESAClient` remains unavailable until its actual interface is verified.

**Streaming interface.** Follow the separation in `stream_sources.py` and
`stream_rasters.py`: metadata planning first, authorization before iterator access,
then bounded native windows and compact evidence. A new reader requires an explicit
`StreamPlan.reader` contract extension and source-specific validation in preflight.
Keep calibration in the harmonizer. Do not persist raw or harmonized source arrays,
including test downloads. Close readers on completion and failure, and let the
consumer control advancement. Declared support changes need reviewed operations.

**Validation.** Use generated native metadata and in-memory window readers for CI.
Test malformed metadata, missing rights, original DN survival, calibration exclusion
from adapters, bounded reads, mask behavior, hash scope, native indices, pre-access
gates, close-on-error and provenance. Keep live acquisition an explicit opt-in
integration check. A fixture is not evidence of real integration.

[Source contracts](contracts.md) · [Discovery implementation](../discovery.md) ·
[Streaming gates](../streaming-harmonization.md)

## Add a deterministic scientific operation

Specify its scientific meaning, units, support effects, uncertainty behavior and
rights implications before implementation. Extend the `Operation` allowlist and
`harmonization.assess` / execution together. Never execute model-generated code.
Add positive and deliberately invalid tests, exact recipe/QA/human binding tests,
and original-value/lineage checks. If a raster implementation is needed, maintain
scalar/raster parity and reject unsupported layouts or unbounded operations.
New scientific equivalence requires expert review, not matching names.

## Add a representation

Keep source access and scientific calibration upstream. An encoder accepts validated
harmonized outputs, records canonical definitions/units, and separates numerical
preprocessing from scientific transformations. Preserve encoder/filter/preprocessing
identity in model and dataset hashes. Training reference selection and normalization
must exclude validation/test data. Add integrity, geographic/split leakage and
held-out downstream tests with baselines. Generic encoders must not be substituted
for a reviewed MOSAIKS plan. Source/layout/encoder changes need fresh consensus.

[Actual MOSAIKS input and dataset contracts](../mosaiks-embeddings.md)

## Add a science track

Use the [track configuration procedure](../tracks.md#add-a-track). Supply the question,
variables, support, assumptions and reviewed rules in a new configuration. Reuse
core discovery and harmonization code. Add tests proving the new track cannot
mutate shared source/core resources or another track’s configuration and products.
Do not enable the undefined third track without a scientist-defined scope.

## Keep the reference synchronized

Regenerate figures and schemas after interface changes; update source status,
examples, README, changelog and design decisions. Run the full relevant offline
suite, strict MkDocs build and rendered-link checker. Inspect desktop/mobile
navigation and accessibility after visual changes. Existing Pages and Material
remain the deployment mechanism; local validation does not publish a site.
