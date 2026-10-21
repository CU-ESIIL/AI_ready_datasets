# Website audit and reader review

## Before redesign

The initial [current-state audit](../architecture/current-state.md) found a flat
Material navigation mixing concepts, operational commands, integration history and
scientific governance. The homepage explained a prototype but did not give a
complete research narrative or a clear path from overview to reference. There was
no distinct Approach/Data/Science/Impact layer, source-generated schema reference
or coherent diagram set. The existing hero image had unverified attribution.

The site already had MkDocs Material, an ESIIL logo override, search and a strict
Pages workflow. Those were useful infrastructure to preserve. Inspection during
rendered verification additionally found a nested logo anchor and an unnecessary
asynchronous latest-release request that returned 404; the small template fixes
retain the logo and repository link without that request.

## Non-specialist: the first thirty seconds

The homepage opens with the scientific problem and the aim of preserving meaning
and history through AI-ready dataset creation. Its next sections explain why
heterogeneous observations are hard to combine and introduce three accountable
stages. Discovery is presented as finding candidates; transformation decisions and
representation generation require more than a catalog. The stopped Sentinel run
and explicit limits give readers evidence to assess trust without opening a schema.

## Scientist: the next five minutes

Approach explains explicit scientific recipes, native support, specialist evidence,
deterministic operations and human decisions. Data separates modality from scale
and distinguishes real, synthetic and planned integrations. Science makes food and
water independence explicit and leaves the third track undefined. Impact and the
Sentinel case distinguish numerical diagnostics from independent validation.
Provenance gives the complete representation-to-source inspection chain.

## Engineer: as much depth as needed

Documentation offers paths for foundations, architecture, running, scientific review,
extension and verification. Existing Markdown technical URLs are retained. The
source-generated module map and JSON Schemas identify actual contracts and entry
points; streaming, MOSAIKS, governance and extension pages describe their limits.
The extension guide covers source readers, allow-listed operations, representation
interfaces and track isolation without copying core pipelines.

## Rendered verification

- Strict MkDocs build and a local checker validate rendered links, fragments,
  images and generated schema assets without network access.
- Browser inspection at 1440px and 1200px verifies the research hero and desktop/
  intermediate navigation; 390px and 320px show no document-wide horizontal overflow.
- Mobile menu opens with the primary destinations; documentation tables and
  architecture figures scroll locally when needed, retaining legible diagram labels.
- Images load and retain alt text. NASA credit and usage evidence are documented.
- Keyboard Tab reaches Material’s skip-to-content link. Focus outlines remain
  visible, and reduced-motion emulation yields zero-duration transitions.
- Generated figures/reference reproduce identical content on regeneration.

These are concrete prototype checks, not a full accessibility certification or
proof that every future source/integration works. No site deployment was performed.

## Semantic synchronization verification — 2026-10-21

The earlier sections describe the initial editorial redesign. The subsequent
[documentation synchronization audit](documentation-sync-audit.md) expands the
semantic narrative while preserving Material, Pages and the two reader layers.

- All **135 offline tests passed**. No linter is configured in `pyproject.toml`;
  `git diff --check` and Python compilation check changed generators.
- Strict MkDocs build passed; the repository checker passed **53 rendered HTML
  pages**, including local links, fragments, image alt text and schema assets.
- Sixteen generated SVGs share maintained specifications. Conceptual ontology
  depth, accumulation, potential/diversity and quadrant figures contain no fabricated
  measurements or dataset positions.
- Browser checks matched all eight filter result counts against canonical generated
  metadata; name search returned ENVO alone and reset restored all 86 rows.
- Keyboard Tab moved from name search to the era selector; a direct ENVO hash link
  expanded its evidence. Labels and a live result count accompany native controls.
- With JavaScript disabled at 390px, all 86 table records and 86 evidence details
  remained available, controls stayed hidden, and there was no page-wide overflow.
- Desktop and mobile inspections preserve readable narrative, local figure/table
  scrolling and the existing environmental imagery. Screenshots remain ignored in
  `run/website/` as local verification artifacts.

No source rasters, ontology graphs, remote services or model inference were invoked
for this documentation pass. Pipeline behavior was not changed. Existing contract
and inventory edits present before the pass were preserved. No deployment was made.
