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
