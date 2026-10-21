# Testing

Run `python -m pytest -q` from the checkout. Tests use project-authored synthetic
fixtures; no internet, MESA credentials, OpenClaw, or commercial LLM access is
required. Tests block socket connections to enforce this boundary. CI installs
dependencies, then runs tests and a strict MkDocs build. The expanded offline suite includes native-boundary and model-transport tests;
live verification is separate from CI and is described in the real-data guide.

Discovery tests cover spatial/temporal/modality/variable filtering, metadata,
source versions, rights, deterministic ordering, duplicate/conflicting sources,
missing/unavailable resources, checksum integrity, immutable contracts, and
unavailable external interfaces.

Harmonization tests cover exact and unknown meaning, abstention, positive and
negative conversions, variable mapping, missing values/filtering, validation,
recipe schema, QA approval/rejection, low confidence, novel/disputed mappings,
rights review, bound human decisions, core/track separation, original values,
daily coverage/overlap, spatial matching, joins, CRS bounds and lineage.

Representation tests cover batch and generator inputs, known fixture vectors,
dimensions, missing values, malformed inputs, encoder identities/versions,
preprocessing, multiple encoders, source lineage and JSON-LD export.

Integration/track tests cross all three contracts for both food and water,
assert modality-specific products, parent core lineage, licensing and nonempty
artifacts, verify shared cache identity, compare repeat-run bytes, preserve other
track outputs/configuration, exercise CLI/schema export, and add a synthetic third
track through configuration only.

Remaining gaps: authenticated NEON normalization, live MESA/OpenClaw, large input
streaming, authenticated reviewer identity, scientific uncertainty propagation,
real raster preprocessing/cloud masks, and scientifically validated domain models.
No test claims ecological validity or predictive performance from synthetic values.

Real-boundary tests mock HTTP and raster readers explicitly. They check native
STAC preservation, instantaneous timestamps, DN/calibration separation, cloud
rejection, checksummed snapshots, unsafe raster locations, NEON token handling
and file bounds, model JSON-schema requests, model identity/transcripts, malformed
and truncated outputs, missing-model failures, identifier protection, mandatory
human review, and model QA veto/staleness. They do not claim live integration
merely because a transport was mocked.
