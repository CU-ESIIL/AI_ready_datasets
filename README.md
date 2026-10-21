# AI-ready biological and environmental datasets

A research prototype for autonomous, human-governed creation of reusable datasets.
It tests whether a scientific question can drive discovery, auditable scientific
harmonization, deterministic execution, and machine representations while preserving
meaning, uncertainty, decisions, and source rights.

**Agents reason and propose. Deterministic code transforms data.**

```text
Scientific question + track configuration
                 ↓
Discovery and Access → SourceResource
                 ↓
Semantic proposal → recipe → QA → human review when required
                 ↓
Deterministic Harmonization → immutable canonical observations
                 ↓
Track view → Representation → vectors + source/decision provenance
                 ↓
Downstream science
```

Three independently callable modules live in `src/dataset_prototype/`:
`discovery`, `harmonization`, and `representations`. Pydantic contracts connect
them; orchestration composes them. JSON recipes select allow-listed operations.
Uncertain mappings, rights, joins, and support changes require explicit review.
There is no generated-code execution.

Food and water security use the same engine and immutable source/core cache.
Their current configurations demonstrate independent scientific use with synthetic
field and satellite observations; **neither implements a food/water-security model**.
A third track stays disabled until its scientific scope is defined.

MESA is the intended discovery/access infrastructure; its adapter is currently an
explicit unavailable boundary, with a fully functional local `MockMESAClient`.
A live STAC adapter now discovers Sentinel-2 and reads actual NIR/SCL pixel windows.
Four model-backed roles can run through an existing local Ollama server, producing
reviewable proposals without execution permissions. Model QA vetoes and human review
remain enforced. OpenClaw is a future runtime adapter. NEON product metadata is
reachable; token-authenticated native CSV access is implemented but not yet verified
with a configured token. No live MESA or OpenClaw integration is claimed.
The lightweight scalar encoders preserve modality-specific vectors and record model
preprocessing separately from scientific harmonization. They are not MOSAIKS or a
universal latent space.

## Real data and agents

```bash
python -m pip install -e '.[dev,real]'
prototype acquire-sentinel examples/real/sentinel_request.json \
  --longitude -105.586 --latitude 40.0329 --max-cloud 30 \
  --max-items 3 --output run/my-sentinel
prototype propose run/my-sentinel --model deepseek-r1:8b --output run/my-proposal
```

The model must already be installed in Ollama; no automatic model download or mock
fallback occurs. Raw satellite digital numbers and their calibration metadata stay
explicit. NEON requires `NEON_API_TOKEN`; see the workflow guide for native-file access.

## Install and run the offline fixture demonstration

From this repository checkout, with Python 3.11+:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
prototype run --track food_security
prototype run --track water_security
# Use a fresh output directory when repeating a run:
prototype run --all-tracks --output run/repeat
python -m pytest -q
mkdocs build --strict
mkdocs serve
```

Each run writes nonempty JSON artifacts under `<output>/<track>/`, including the
request, sources, proposed/approved recipes, QA, review, harmonized observations,
representations, JSON-LD provenance, downstream comparison, and reproducibility
manifest. Existing run directories cannot be overwritten. Cache entries are
content-addressed. JSON keeps this small prototype inspectable without Parquet
or distributed infrastructure.

Target sources: **NEON, LTER, NASA ORNL DAAC, AmeriFlux, TRY, CartograPlant,
Landsat, Sentinel-2**. The default demo/CI retains synthetic fixtures. The optional
[real-data and model-agent workflow](docs/real-data-agents.md) has been exercised on
actual Sentinel data and local model inference. The latest real model proposal was
rejected by QA and remains unexecuted; model output is not scientific approval.

See the [documentation](docs/index.md), [data-source matrix](docs/data-sources.md),
[prototype status and limitations](docs/PROTOTYPE_STATUS.md),
[review workflow](docs/harmonization.md), and [development decisions](docs/development/decisions.md).
The existing MkDocs Material/GitHub Pages infrastructure is retained; the published
site is configured at [CU-ESIIL/AI_ready_datasets](https://cu-esiil.github.io/AI_ready_datasets/).
Tests and CI run offline after dependency installation.
