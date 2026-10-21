# Architectural decisions and repository audit

## 2026-10-21 — V0 foundation

The initial checkout had README/AGENTS, MkDocs Material configuration and assets,
Pages deployment, manual template-sync and manual JupyterLab-image workflows.
There were no source, tests, data, packaging, environment, changelog, or dev-log
implementations in the committed template. Earlier provenance documentation and
an uncommitted changelog were retained and extended.

- Preserve MkDocs/Material, assets, and Pages deployment. Add a standard `src/`
  package and tests; keep website and package structure separate.
- Use Pydantic frozen typed contracts and JSON Schema at stage boundaries so
  discovery, harmonization, and representation can be tested independently.
- This is data infrastructure: discovery/access, recipes, execution, observations,
  representations, governance and lineage. A registry or STAC catalog alone cannot
  express the complete mechanism. STAC remains one discovery metadata component.
- Agents propose explicit recipes; deterministic allow-listed execution provides
  reproducible scientific transformations without generated code execution.
- Preserve provenance with every representation, including original values,
  metadata/rights snapshots, recipes, proposals, QA, optional human decisions, and
  parent core observations. JSON-LD is enough; no graph database is warranted.
- Distinguish modality from scale so different observation methods do not conceal
  different spatial/temporal support.
- Separate conservative core transformations from application-specific track rules.
  Shared data and caching do not force common scientific interpretation.
- JSON outputs make the small prototype reviewable and avoid introducing Parquet
  dependencies before their scale benefits are needed.
- Use project-authored synthetic fixtures rather than quietly ingesting external
  records or assuming provider redistribution rights. Native-schema adapters and
  real field/raster support harmonization remain explicit milestones.
- Keep MESA integration unavailable where tool signatures are unverified; its
  overview and source README differ in stated implementation status.
- Preserve the manually triggered template-sync and image-build workflows as
  historical template infrastructure. The image job still requires absent
  `containers/jupyterlab` files and template sync can overwrite project changes;
  neither is used by V0. Keep Pages and add an independent offline-test workflow.

## 2026-10-21 — First real-data and model boundary

- Add a small actual Sentinel STAC/COG vertical slice before assuming NEON access.
  The official NEON data route returned 403 without a token; its current license
  is CC BY 4.0. A token-aware native-file boundary exists without pretending sensor
  metadata normalization has been completed.
- Use an existing local Ollama model to exercise real role inference without new
  hosted credentials. OpenClaw remains a later runtime adapter, not a fabricated
  live integration. Preserve fixtures for deterministic offline regression tests.
- Retain raw DN, scale/offset, SCL and native pixel support rather than silently
  convert to reflectance or assert field equivalence. Permit explicit instantaneous
  timestamps and qualify extracted-window checksums.
- A real model rewrote a source identifier. Fail that call, retain its transcript,
  and narrow the judgment schema so code owns immutable identity/targets. This is
  a contract correction, not a hidden repair of the scientific decision.
- The later real model QA rejected a raw-DN proposal over calibration-context
  concerns. Preserve this result and enforce the veto; a successful model call
  is not evidence of correct science. Bind model review to content and retain
  mandatory human review regardless of model confidence.
