# Sentinel review: learning from a stopped run

The current Sentinel example targets documented B08 bottom-of-atmosphere reflectance,
then an explicitly reviewed representation. We inspected actual retained model runs
before changing contracts. No reviewed real Sentinel MOSAIKS dataset was produced.
The generated MOSAIKS diagnostic is a different, explicitly offline execution.

## Before: observed cross-domain review leakage

The metadata-only run `sentinel-stream-consensus-bounded` completed four specialist
reviews and QA with revision/rejection. Semantic, units, support and rights roles
repeated concerns about negative reflectance, masks, missing checksums and licensing.
Rights speculated that numeric values might violate terms without citing terms.
Unit `1` was challenged despite its valid dimensionless meaning. Metadata and
full-raster checksum claims were conflated. These are recorded model judgments,
not scientific facts adopted by the executor.

The raster/MOSAIKS metadata run `mosaiks-real-consensus` retained a valid draft and
three revision requests, then failed on a rights reviewer’s self-citation. The
proposal also described native coordinates as EPSG:4326. The native raster metadata
specifies EPSG:32613; geographic footprints use EPSG:4326. This is a concrete
support/provenance concern that needs correction and fresh review.

## After: additive scoped contracts

| Observed old behavior | New contract / deterministic check | Remaining responsibility |
| --- | --- | --- |
| Any reviewer repeated any concern | Domain-owned evidence and role-specific JSON Schema | Expert assessment of prose accuracy |
| `revise` mixed unknowns and contradictions | PASS / FAIL / NEEDS_EVIDENCE / NOT_APPLICABLE | Curate authoritative evidence |
| Repeated concerns became more votes | Stable domain-prefixed IDs and references; duplicates rejected | Recognize paraphrased duplicates with different IDs |
| QA could introduce a new concern | QA finding IDs must already exist | Expert review of synthesis wording |
| A metadata hash was treated like raster integrity | Dedicated integrity scope and explicit evidence kinds | Inspect per-window evidence at execution |
| A catalog label invited speculative legal prohibitions | Intended operation and explicit missing-terms evidence | Review actual terms and source-specific permissions |
| Negative reflectance implied failure | Calibration separate from explicit quality selection; no clipping | Analysis-specific validity evidence |
| Workflow consensus sounded like approval | Eligibility, human approval and execution authority separate | Human decision and existing execution gates |

All six scoped specialists review the same frozen scientific recipe. Each receives
only its curated domain evidence and references to prior findings. Missing terms
are declared `MISSING_EVIDENCE`; they do not manufacture either permission or a ban.
The example ledger was explicitly assembled by the coding agent from retained
metadata and implementation behavior. It has not been expert-validated and is not
an automated metadata-cleanup stage.

## Actual re-review records

The first new OpenClaw/Verde run `scoped-sentinel-review` returned
`semantic_quantity_01`, violating the required `semantic.` prefix. The run was
rejected and retained unchanged. The next explicit run used a domain-specific
schema; it accepted semantic review, then rejected an unknown units evidence ID.
The schema was further narrowed to enumerate supplied evidence IDs and bind the
exact recipe digest. A fresh versioned run records its own results; no output is
repaired, and none of these reports authorizes execution.

The installed gateway is OpenClaw 2026.5.18, provider `verde`, model
`js2/gpt-oss-120b`. Traces contain exact task envelopes, schemas, plugin-normalized
JSON, timestamps and available runtime identity. The plugin does not expose raw
provider text, token usage or a model-weight digest. No raster was read for these
reviews. Historical recipe vetoes remain in force.

## Offline Sentinel regression

Offline tests use generated DN values with the documented equation
`reflectance = DN × 0.0001 − 0.1`. For DN 10, the retained result is −0.099 with
unit `1`; original DN remains unchanged. That verifies deterministic calibration
behavior. It does not claim that the generated observation was acquired by Sentinel
or that a negative value is suitable for any ecological analysis.

Additional tests reject stale recipe digests, cross-domain evidence, unknown QA
references, duplicates and opinion-only failures. They test missing evidence as a
review state, matching frozen recipes across specialist calls, and failure checkpoints.
All run offline with network access prohibited.

## What is still blocked

A scientist must correct the support description, attach appropriate rights and
use-specific quality evidence, and review a fresh frozen recipe and raster/encoder
plan. Required consensus, deterministic QA, historical model vetoes and an exact
human decision continue to gate any live streaming. Numeric verification of
MOSAIKS is available; independent scientific validation and a real approved dataset
remain unestablished.

### Completed scoped pilot (v3)

The versioned `scoped-sentinel-review-v3` completed all six actual Verde reviews
and QA. Deterministic synthesis returned `needs_revision`; no raster data was read.

| Specialist | Actual outcome | Interpretation |
| --- | --- | --- |
| Semantic | PASS | Accepted the stated dimensionless B08 reflectance definition |
| Units/calibration | PASS | Accepted scale 0.0001, offset −0.1 and unit `1` |
| Support | FAIL | Identified native EPSG:32613 versus footprint EPSG:4326 confusion |
| Rights | NEEDS_EVIDENCE | Requested authoritative terms for the intended derivative operation |
| Integrity | FAIL | Treated lack of whole-raster immutability proof as incomplete provenance |
| Quality | PASS and NEEDS_EVIDENCE | Accepted the explicit mask predicate; requested independent validity evidence |

The integrity rejection remains a **model judgment needing expert analysis**.
Correctly scoped metadata/window checksums do not promise a whole-object checksum;
that limitation alone does not demonstrate a violated requirement. Likewise,
passing an SCL predicate does not prove all selected pixels scientifically valid.
The new boundaries improve ownership and evidence visibility; they cannot prove
that natural-language inferences follow from their citations. We retain these
limitations rather than force approval.

The pilot predates the final complete-source-set binding, explicit QA-veto field
and real-stream report gate. Its report is retained as pilot evidence, not migrated
into an executable approval. The final versioned integration run uses those stricter
contracts; all historical vetoes remain visible and binding.

### Source-bound run (v4) and stricter provenance check

`scoped-sentinel-review-v4` completed seven real model calls with complete source-set
binding and an explicit QA `revise` veto. Semantic and calibration passed; support
failed; rights and quality needed evidence; integrity both passed recipe binding
and rejected metadata-only checksum scope. The result remained `needs_revision`,
with `source_data_read: false` and no execution permission.

A subsequent stricter revalidation rejected a finding’s source label because it
was not the exact source pointer attached to its cited evidence. That run predates
the exact-source-pointer constraint and is retained unchanged, not upgraded into a
current executable report. The deployed role schema now enumerates source pointers
as well as evidence IDs, role and recipe digest; offline contract tests exercise
this constraint. There is no fully approved real Sentinel result from this pass.
