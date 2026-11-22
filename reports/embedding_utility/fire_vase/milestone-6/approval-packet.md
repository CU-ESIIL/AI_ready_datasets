# Human-review packet — bounded real-source audit

**Decision requested: review evidence for a bounded native-value audit only. No approval exists yet.**

The data are locally available in the Fire VASE lake. No GitHub upload or acquisition is requested. This packet does not ask to waive source uncertainty, rights, scientific review or prospective availability.

Packet digest: `8be26eec72f9fb711569994cbb5cb8e2c3339b5c156037e8779a597b0570135a`. A changed source, scientific recipe, claim mode or budget invalidates this review.

## 1. Exact datasets and identity

Release: `fire-vase-data-lake-v0.1`, packaged local `files/` root. Selected artifacts are present with sizes matching inventory. Reported full-container hashes are historical and need current verification before decoding.

| Source ID | Package path | Bytes | Historical SHA-256 |
| --- | --- | ---: | --- |
| fired_daily | `files/artifacts/fire-vase-gridmet-real/fired-cache/fired_conus-ak_daily_nov2001-march2021.gpkg` | 575,012,864 | `added786e5741f835c4277b38478f446c1bb7269596998ad2ddda482cb59bf62` |
| fired_events | `files/artifacts/fire-vase-gridmet-real/fired-cache/fired_conus-ak_events_nov2001-march2021.gpkg` | 256,565,248 | `a77f06f9344bc1c2f6fbabf630948f4e263bc14bf341577bf32a39ad884d570d` |
| cached_slices | `files/scratch/fire_vase_run_full/tables/vase_slices.parquet` | 38,403,514 | `40ccca537301e408d74b072e9079edc8fb97b47c6e27a11e579786d52406f066` |
| cached_traits | `files/scratch/fire_vase_run_full/tables/fire_traits.parquet` | 23,582,087 | `7ed36a65e775048b54fc49d7b8c63f72085c2b097fc09d73df3727f650108f23` |

Exact absolute paths, native columns and metadata evidence are in [packet.json](review-v2/packet.json) and [metadata inventory](review-v2/metadata-evidence.json). Do not substitute a similarly named release/table.

## 2. Intended analysis and bounded scope

First verify source identities and, only after review conditions are complete, inspect at most **512 total decoded rows across these sources**, at most **16 native event IDs**, batches at most **128**. Inspect native ID/date/value alignment and support; no geometry reads, full-table scan, model training, raw/harmonized persistence, source copies, downloads or redistribution. This sample is for adapter verification only and cannot establish population skill.

A proposed deterministic sample is the first bounded source-row window, grouping only explicitly matching native event keys; if it yields incomplete events, duplicates or unsupported windows, record exclusion and stop. Do not extend the scan to obtain attractive/longer fires. Actual event IDs are unknown until approved inspection; the packet binds the selection procedure and total bound, not invented IDs. A future approved adapter must enforce the shared budget across source/cache lookups.

The requested scientific claim for this audit is **retrospective reconstructed** native-value alignment. It is not permission for a prospective performance claim. Operational availability needs its own evidence. Later full cohort/training, scientific mapping or public model/data release requires a separate reviewed plan and approval.

## 3. Required transformations / definitions

Review the [scientific contract](scientific-contract.md). The five versioned recipes in packet.json are proposed, not approved executable recipes: native-increment identity, exact calendar support, observed-prefix isolation, independent future outcomes and whole-fire holdouts.

Confirm `dy_ar_km2` source definition and the cached copy relationship; distinguish reconstructed sum from catalog total and differently generated same-named cumulative fields. Preserve original IDs/types, source/native observation dates, units, support, flags, uncertainty and transformation lineage. No implicit calibration, geometry reprojection, gap filling or source-zero assumptions.

## 4. Known uncertainty and missing evidence

Native area/date estimates, pixel QA survival, source uncertainty model, timezone/daily-bin definitions, event boundary/version identity, unsupported gaps, source/cached exclusions and actual availability at issue time. Current full byte identity is not reverified. Rights for this exact source release, derivatives, embeddings/checkpoints and publication require confirmation. None becomes zero or FAIL merely because evidence is missing.

## 5. Use/attribution and publication

Confirm original dataset creators/release/accession, permitted internal research/processing, required FIRED/MODIS attribution and any restrictions on derived representations/models. The repository MIT and article CC BY licenses do not establish dataset rights. Initial audit authorizes no observation publication; later aggregate/embedding/checkpoint release requires explicit rights review. [Assessment](source-use-assessment.md) separates verified evidence from unknowns.

## 6. Proposed validation tests

- Verify full container identity against exact reviewed expected checksums without decoding, then record current verification evidence. A mismatch blocks row reads.
- Check native ID/date uniqueness, original value/type survival, source/cache one-to-one alignment and unmatched categories; no permissive join or silent repair.
- Independently verify exact-day versus gappy support, missing versus observed zero, event boundaries and prefix origin; retain original quality flags.
- Reject fabricated availability; keep a retrospective contract separate when timestamps are unknown.
- Independently compare a bounded approved row subset with analytical date/area examples, once native semantics are reviewed. Current generated precondition tests are not real equivalence validation.
- Preserve source/recipe/evidence/checker identities and all failures; do not treat code tests as scientific or legal approval.

## 7. Review decisions and responsibilities

Use [review-template.json](review-v2/review-template.json), bound to the packet digest. All seven jurisdictions currently read NEEDS_EVIDENCE: semantic, units, support, rights, integrity, quality, availability. An attributed human reviewer must supply evidence references and rationale. Quality review may acknowledge unquantified source uncertainty with explicit limits; it may not invent an error distribution. Availability may be NOT_APPLICABLE only for the explicitly retrospective audit, never for a prospective claim.

An APPROVE_BOUNDED_AUDIT record is not approval of scientific equivalence, model training or public release. Fresh container verification must still match expected identities before any decoding; the pure checker cannot authenticate authorship or grant execution. A rejection or missing evidence remains binding.

### Reviewer response requested

1. Supply or confirm dataset-specific rights/accession/attribution evidence.
2. Review native daily-area/date-bin semantics, event identity and source uncertainty.
3. Decide whether to approve the limited retrospective **native-value audit** above, with conditions or revisions; leave subsequent cohort/training/publication unapproved.
4. For a genuinely prospective study, identify actual observation-release/processing availability evidence. If unavailable, explicitly choose a later retrospective-only study scope or keep prospective evaluation pending.

Approval boundary: the Milestone 6 brief says **“Do not read observation rows until the required approval is established.”** [AGENTS.md](../../../../AGENTS.md) also requires human review for uncertain meaning/rights. Local data possession supplies location, not those missing scientific decisions.
