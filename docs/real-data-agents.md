# Real data and model-backed agents

The first replacement of synthetic components is **live Sentinel-2 STAC discovery,
actual windowed COG pixel reads, and four model-backed roles using an existing local
Ollama installation**. Synthetic fixtures remain for offline tests. No live run
silently falls back to fixtures or deterministic agent responses.

## Verified live on 2026-10-21

- Earth Search returned actual Sentinel-2 L2A items near the example NIWO vicinity.
- NIR band 8 and scene-classification (SCL) pixels were read through rasterio/GDAL
  range requests. The initial three accepted pixels had DN values 1318, 1365, and
  1280, with SCL=4 (vegetation). These are actual source-native values, not reflectance.
- The public CLI independently acquired a one-pixel snapshot and called discovery,
  semantic, harmonization, and QA roles through Ollama's documented `/api/chat`.
- The installed `deepseek-r1:8b` model digest, complete prompt/output transcripts,
  schema constraints, prompt version, timestamps, and token counts were recorded.
  Proposal evidence links prompt/response content hashes to the saved transcripts.
- The latest model QA **rejected** the proposal over its interpretation of calibration
  context. Deterministic QA honors that veto. No scientist approval or transformed
  scientific product is claimed from this proposal. A model rejection is evidence
  to inspect, not a definitive scientific conclusion.

An earlier live call rewrote a source identifier and was rejected by validation.
The boundary now keeps identifiers/targets under deterministic code control and
asks the model only for its scientific judgment. Earlier failed transcripts remain
under ignored run outputs; no repair or fixture substitution is hidden.

## Acquire a small real sample

```bash
python -m pip install -e '.[dev,real]'
prototype acquire-sentinel examples/real/sentinel_request.json \
  --longitude -105.586 --latitude 40.0329 \
  --max-cloud 30 --max-items 3 --output run/my-sentinel
prototype propose run/my-sentinel --model deepseek-r1:8b \
  --output run/my-agent-proposal
```

Use a model already installed on your Ollama server. No model is downloaded and
no hosted API key is needed. The optional `--endpoint` defaults to loopback;
unencrypted remote endpoints are rejected. This is real model inference, not an
OpenClaw worker invocation. OpenClaw remains the intended later runtime adapter.

The example point is a site vicinity, **not a verified NEON sensor location**.
Request and date selection live in example configuration, not core architecture.
The public CLI caps candidates at ten, filters scene cloud percentage, then accepts
only SCL 4, 5, or 6 and nonzero NIR DN. A scene-level cloud threshold alone does not
prove a pixel is clear. SCL is a quality indicator, not a guarantee of suitability.
Failed/rejected candidates retain evidence and never become fabricated observations.
GDAL fetches the compressed blocks needed for individual pixels, not whole scenes.

## What remains unchanged scientifically

Ingestion preserves **raw digital numbers**. Native STAC scale/offset, platform,
sensor, processing baseline, acquisition timestamp, footprint, native CRS/indices,
SCL, and complete STAC Item metadata are retained. Physical reflectance calibration
is not applied behind the recipe engine. Field-to-pixel equivalence, temporal
aggregation, and ecological inference are not authorized by this example.

Instantaneous satellite timestamps are represented by equal start/end times;
no artificial one-second or daily interval is invented. Core validation accepts
zero duration only when source support explicitly says `instantaneous`.
The 10 m native-CRS pixel footprint is retained as a WGS84 bounding box; it is not
replaced with a site centroid or declared equal to field-observation support.

A source checksum with scope `extracted_window` covers the saved pixel-evidence
JSON, **not the full remote COG**. Snapshot content digests separately protect the
normalized resource and record descriptions. `SnapshotClient` verifies all evidence
files and supports offline reuse through the existing discovery/access contract.
Large native rasters and live outputs stay out of git.

## License evidence

Earth Search's Sentinel collection labels its license `proprietary` and links the
specific [Copernicus Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
The adapter recognizes only that verified notice link for this collection, retains
the original STAC label, records the legal-notice identity and attribution, and
preserves the native collection evidence. Unknown/custom licenses remain uncertain
and require review. Do not infer reuse permission from a satellite name alone.

## Agent boundary and human review

The four roles receive bounded scientific metadata and return typed JSON. They
have no tools, filesystem handles, shell, network tools, or data-write capability.
Full native STAC metadata stays in source evidence; model prompts contain the
normalized scientific subset, explicitly recorded in transcripts.

Model-generated mappings always require human review, regardless of confidence.
The model cannot rewrite source/target identity or mark a recipe approved. A model
QA rejection or revision request becomes a recipe veto enforced by deterministic
QA. Its content digest excludes only approval state and the review itself; editing
scientific content invalidates that model review. Approval-state edits alone cannot
bypass the veto. Malformed/truncated output fails and is retained for inspection.
Model calls can be nondeterministic even with seed/temperature settings; exact
transcripts are the evidence, not an inference-reproducibility guarantee.

Inspect `discovery_proposal.json`, `semantic_mappings.json`, `draft_recipe.json`,
`proposed_recipe.json`, `model_qa.json`, `qa_report.json`, `review.json`,
`agent_traces.json`, `sources.json`, and `records.json`. On failure, completed stages,
transcripts, and a failure report are retained. No scientific transformation runs
inside `prototype propose`.

Revise scientifically rejected/unknown proposals and obtain renewed model QA
before human approval. For a valid proposal, save the intended approved recipe,
record an explicit human decision with `prototype review`, then use the existing
`harmonize` and `encode` stage commands. See [the review workflow](harmonization.md).
An expert can disagree with model QA, but this prototype requires a recorded
revised proposal/review rather than a silent override.

## NEON: implemented access boundary, token required

The official [NEON API authentication documentation](https://data.neonscience.org/data-api/authentication/)
specifies the `X-API-Token` header. The tested NIWO July 2023 `/data` request returned
403 without a token. Public product metadata was retrieved successfully. The
current [API documentation](https://data.neonscience.org/data-api/) specifies
CC BY 4.0, not the old CC0 assumption.

Configure `NEON_API_TOKEN` in your process environment; do not paste it in chat,
commit it, or place it in an example file. The CLI reads it without logging it.

```bash
prototype neon-files --product DP1.00002.001 --site NIWO \
  --month 2023-07 --release RELEASE-2025 --output run/neon-files.json
# Select one exact small CSV name from the provider response, then:
prototype neon-files --product DP1.00002.001 --site NIWO \
  --month 2023-07 --release RELEASE-2025 \
  --filename EXACT_PROVIDER_FILENAME.csv --output run/neon-native
```

The adapter requires an explicit release and exact provider filename, checks the
file-size limit, retains native metadata/CSV/checksum and license/citation requirements,
and sends tokens only to the NEON host. It does not guess sensor coordinates or
height, normalize uncertain variable semantics, or claim live CSV acquisition
before a token-backed download has actually succeeded. Sensor positions, variable
metadata, quality flags, uncertainty, and interval definitions must be verified
before this native CSV becomes harmonized observations.

## Next scientific step

Complete authenticated NEON acquisition and sensor metadata normalization, then
have an expert specify a defensible field/sensor-to-pixel question and support
relationship. NIR digital numbers are not air temperature, vegetation height, or
food/water indicators. Keep that scientific decision distinct from making live
adapters and models run.
