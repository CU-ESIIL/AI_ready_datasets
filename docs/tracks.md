# Science tracks

One engine accepts `TrackConfig`; no food, water, or third-track pipeline is copied.
The default food and water configurations request the same synthetic canopy-height
and NIR-reflectance observations. Food uses a scalar encoder; water uses scalar
and square. This demonstrates configuration and output independence, **not** a
scientific food- or water-security indicator.

Each track declares question, variable requirements, modalities, spatial/temporal
requirements, encoder, and scientific assumption. A track recipe references its
core recipe; track observations retain parent canonical identifiers and parent
provenance. Track-specific artifacts carry track identity and never overwrite core
observations or another track's outputs.

Source records and shared canonical cache entries are immutable and shareable.
A shared source does not imply shared interpretation. Future food rules might
involve traits/productivity, and water rules might involve fluxes/soil/environment;
no such scientific model is encoded until supplied and reviewed.

## Add a track

1. Copy `tracks/third_track/config.json` to a new track folder or another JSON path.
2. Supply a scientific question, required variables/modalities, support, and explicit assumptions.
3. Define and review any nonconservative recipes and domain validation.
4. Enable the track and run `prototype run --config path/to/config.json --output run/new`.
5. Add configuration, scientific validation, provenance, and independence tests.

The third-track template is disabled because its scientific scope is undecided.
An integration test enables a synthetic copy to demonstrate configuration-only
extensibility without inventing a third scientific application. Custom domain
recipes can use the independent harmonization API; the default orchestrator currently
constructs only curated identity/selection recipes from declared metadata.
