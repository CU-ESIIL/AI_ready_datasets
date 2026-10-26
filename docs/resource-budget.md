# Grant-period storage, backup and compute budget

**PLANNING ESTIMATE — 26 October 2026.** Three-year U.S.-and-territories infrastructure plan for three products and 150 participants across nine groups. All persistent storage, distribution and backup are intended for TACC; VERDE inference and compute use Jetstream2/ACCESS. No OSN request is included. No awards, backup service or provider agreement are implied.

## Storage by type and year

Decimal TB; annual provisioned capacities, not annual increments. The 80 TB final product allowance covers all three products together, including retained releases, feature shards, row lineage, encoders and verification artifacts. It assumes the provisional 1 PB global premise concerns all three products combined; it is not a measurement or approved scientific specification. No equal allocation among products is assumed.

| Type | Year 1 TB | Year 2 TB | Year 3 TB | Retention and basis |
| --- | ---: | ---: | ---: | --- |
| Three product collections, combined | 20 | 50 | 80 | Immutable identified releases; selected release versions already included in this allowance |
| Group workspaces | 6 | 36 | 30 | Three governance groups at 2 TB in Years 1–2; six synthesis groups at 5 TB in Years 2–3; closeout requires notice |
| Shared metadata/governance | 1 | 2 | 3 | Source/semantic metadata, recipes, reviews, model evidence and service state; avoids duplicating product-packaged lineage |
| Primary content subtotal | 27 | 88 | 113 | Products plus workspaces and shared metadata |
| Primary recovery/publication headroom | 6 | 18 | 23 | Provisioned temporary restore and replacement capacity; not another permanent copy |
| Backup: current full content copy | 27 | 88 | 113 | Separately recoverable product, workspace and metadata copy, beyond provider replication |
| Backup: historical changed/deleted mutable content | 7 | 35 | 41 | Rounded-up version-history model below; workspace plus shared metadata only |
| Backup allocation subtotal | 34 | 123 | 154 | Full current copy plus version history |
| **Total allocated storage** | **67** | **229** | **290** | Primary content + headroom + backup; excludes internal provider replication overhead |

## Retention and growth ledger

**Opening retained capacity + new capacity − retired capacity = closing retained capacity.** All figures below are planning allowances in decimal TB, not measured ingest or write volumes. Opening capacity equals the previous year's closing capacity. New capacity includes incremental retained releases; gross temporary output, overwrites and backup churn are not measured here. No product or governance-metadata deletion is assumed during the grant.

| Content/capacity type | Year | Opening retained TB | New TB | Retired TB | Closing retained TB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Three product collections | 1 | 0 | 20 | 0 | 20 |
| Three product collections | 2 | 20 | 30 | 0 | 50 |
| Three product collections | 3 | 50 | 30 | 0 | 80 |
| Group workspaces | 1 | 0 | 6 | 0 | 6 |
| Group workspaces | 2 | 6 | 30 | 0 | 36 |
| Group workspaces | 3 | 36 | 0 | 6 | 30 |
| Shared metadata/governance | 1 | 0 | 1 | 0 | 1 |
| Shared metadata/governance | 2 | 1 | 1 | 0 | 2 |
| Shared metadata/governance | 3 | 2 | 1 | 0 | 3 |
| Primary content subtotal | 1 | 0 | 27 | 0 | 27 |
| Primary content subtotal | 2 | 27 | 61 | 0 | 88 |
| Primary content subtotal | 3 | 88 | 31 | 6 | 113 |

The 20 / 50 / 80 TB product figures mean **20 TB retained in Year 1, another 30 TB in Year 2, and another 30 TB in Year 3**. All earlier retained releases remain within the closing total. They do not mean 20 + 50 + 80 TB of separate annual additions. The 80 TB limit still needs a product-by-product retained-file inventory; it is not validated by this bookkeeping.

The Year 3 workspace retirement is a proposed 6 TB governance closeout, subject to notice, rights and selection of research artifacts for retention. Selected outputs must fit within the product/shared-metadata allowances before active workspace retirement. The full current-copy backup moves deleted workspace content into protected history; it is not assumed to disappear from backups on closeout.

## Backup and headroom allocation ledger

These rows describe provisioned capacity, not actual snapshots created or expired. In particular, zero retired history allowance does not mean snapshots never expire: expired snapshots are replaced inside the reserved rolling-history capacity. Monthly-point expiration is not modeled as a guaranteed capacity saving.

| Content/capacity type | Year | Opening retained TB | New TB | Retired TB | Closing retained TB |
| --- | ---: | ---: | ---: | ---: | ---: |
| Backup current-copy allocation | 1 | 0 | 27 | 0 | 27 |
| Backup current-copy allocation | 2 | 27 | 61 | 0 | 88 |
| Backup current-copy allocation | 3 | 88 | 31 | 6 | 113 |
| Backup history allowance | 1 | 0 | 7 | 0 | 7 |
| Backup history allowance | 2 | 7 | 28 | 0 | 35 |
| Backup history allowance | 3 | 35 | 6 | 0 | 41 |
| Recovery/publication headroom | 1 | 0 | 6 | 0 | 6 |
| Recovery/publication headroom | 2 | 6 | 12 | 0 | 18 |
| Recovery/publication headroom | 3 | 18 | 5 | 0 | 23 |
| Total allocated storage | 1 | 0 | 67 | 0 | 67 |
| Total allocated storage | 2 | 67 | 162 | 0 | 229 |
| Total allocated storage | 3 | 229 | 73 | 12 | 290 |

Year 3's 12 TB retired allocation comprises 6 TB of active workspace plus 6 TB of its current-copy backup. The history allowance separately increases by 6 TB, preserving those deleted contents rather than treating closeout as immediate backup deletion. No new cost is added for the same history twice.

The annual billing model provisions closing capacity for the full year and assumes the approved workspace retirement precedes the final planned additions. If closeout is delayed, peak Year 3 current content and its full copy can require **12 TB extra**, taking combined allocation from **290 to 302 TB**. Reserving that extra capacity for the full year at the assumed rate would add **$720**, making Year 3 **$38,120** and the grant **$120,880**. This is a sensitivity, not included in the base total, and no deletion is executed or authorized by this document. Additional internal workspace churn still requires measurement.

Each year incurs costs for its entire provisioned capacity, including retained earlier data. Storage-year quantities and annual costs add across the grant; year-end capacities are not added to obtain a final footprint. The [lifecycle CSV](assets/data/grant-storage-lifecycle.csv) makes the carry-forward calculation explicit. Subtotal and total rows are alternative summaries, not additional stored objects.

## Proposed versioned backup policy

This is a proposed service policy, not implemented scheduled backup or a TACC guarantee. Retain 14 daily, 12 weekly and 12 monthly restore points using incremental/deduplicated storage. Assume each daily point retains changed/deleted bytes equal to 0.5% of current mutable content, each weekly point 2%, and each monthly point 5%. Do not assume deduplication across separately protected copies.

History coefficient = 14 × 0.005 + 12 × 0.02 + 12 × 0.05 = 0.91. Current mutable content is 7 / 38 / 33 TB. Size ordinary version history against the larger of the current and previous year's mutable allocation: 7 / 38 / 38 TB. This gives 6.37 / 34.58 / 34.58 TB, rounded up to 7 / 35 / 35 TB. Add a separate 6 TB Year 3 closeout reserve for potentially deleted governance workspaces (three groups × 2 TB), giving **7 / 35 / 41 TB of historical content**. This intentionally allows overlap between ordinary history and closeout retention rather than claiming deduplication savings. The closeout reserve is additional to the current full copy; it does not buy extra active workspace quota.

All restore-point cohorts are counted without deducting overlap. The percentages estimate distinct changed/deleted blocks retained per restore point, not cumulative daily change rates or extra full copies. They are capacity assumptions, not observed churn or guarantees for arbitrary overwrite patterns. Rolling twelve-month retention can span grant-year boundaries and service costs beyond grant closeout are not included. Higher churn, larger deleted datasets or additional release versions require recalculation; this allowance does not guarantee any possible backup workload.

Released scientific versions are immutable and counted in product storage and its full backup, rather than multiplied by daily snapshot count. Protect mutable metadata at least daily; proposed recovery point objective is 24 hours. Proposed targets, subject to provider agreement: restore essential metadata/services within two business days and complete dataset recovery within ten business days. These require transfer/restore benchmarks. The 20% primary headroom is not enough for a simultaneous full clone of primary content: complete recovery would replace unavailable storage or require temporary provider capacity. Quarterly sampled restores (12 over the grant) and an annual end-to-end recovery exercise (three over the grant) are proposed; transfer, staffing and any temporary capacity costs require agreement. All recovery evidence is retained. Separate credentials, protected retention/deletion policy and failure isolation must be specified with TACC. Two directories or Corral's built-in replica alone do not satisfy this requirement.

Backup history can preserve controlled/deleted content; apply source rights, visibility controls and authorized deletion requirements to backups too. Raw/harmonized raster arrays are not persisted or backed up. Restart cursors and permitted partial feature shards may be retained with explicit status. Post-grant Years 4–10 are excluded from this budget and require a separate agreement.

## Direct expenses by year

| Expense | Unit/rate and duration | Year 1 USD | Year 2 USD | Year 3 USD | Total USD | Evidence status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| TACC primary capacity, including headroom | 33 / 106 / 136 TB for a full year, at $60/TB/year | 1,980 | 6,360 | 8,160 | 16,500 | Published Corral reference rate; AMBER eligibility/quote unconfirmed |
| TACC additional versioned backup | 34 / 123 / 154 TB for a full year, assumed $60/TB/year | 2,040 | 7,380 | 9,240 | 18,660 | Planning rate only; backup service, retention and price unconfirmed |
| Commercial inference APIs | Annual spending caps; input/output/cache/reasoning usage metered where reported; Years 1–3 only | 30,000 | 20,000 | 10,000 | 60,000 | Proposed allowance, not a provider quote or token forecast |
| Hosting/distribution/access services | Annual non-compute service allowances; no project salaries or allocated VM costs included | 5,000 | 10,000 | 10,000 | 25,000 | Scope and provider pricing unconfirmed; avoid overlap with institutional staff |
| **Cash planning total** | Excludes personnel, indirect costs and post-grant retention | **39,020** | **43,740** | **37,400** | **120,160** | Arithmetic checked; not a fully quoted budget |

Version history adds 83 TB-years and $4,980 at the assumed rate to the previous $115,180 estimate. No unassigned contingency is included. No free first-5-TB concession or awarded storage is deducted. Using $60 for backup is not a claim that Corral provides versioned backup at that price. Service charges and inflation require a quote; the reference-rate calculation assumes constant prices for three years.

## Requested compute and memory: separate from cash

Inference is front-loaded: 50% in Year 1, one-third in Year 2 and one-sixth in Year 3. Both open-model hours and commercial API allowances prioritize ontology development, specialist-role evaluation and recipe iteration early, followed by synthesis/refinement and final verification. These fractions are planning choices, not measured demand. Approved deterministic recipes execute without inference; total hours and spending caps are unchanged.

| Resource/type | Year 1 | Year 2 | Year 3 | Three-year total | Basis/status |
| --- | ---: | ---: | ---: | ---: | --- |
| VERDE inference, H100 reference instance-hours | 9,000 | 6,000 | 3,000 | 18,000 | Proposed serving envelope, not measured demand; no inference after Year 3 |
| Same inference expressed as Jetstream2 SUs | 1,152,000 | 768,000 | 384,000 | 2,304,000 | 128 SU/hour; do not add to instance-hours as another resource |
| Development/cohort standard CPU SUs | 100,000–150,000 | 100,000–200,000 | 150,000–250,000 | 350,000–600,000 | Planning range; cohort demand unbenchmarked |
| Persistent standard CPU service SUs | 70,080 | 70,080 | 70,080 | 210,240 | 8 vCPUs × 8,760 hours/year; cohosting/in-kind contributions unresolved |
| Inference/development/service subtotal SUs | 1,322,080–1,372,080 | 938,080–1,038,080 | 604,080–704,080 | 2,864,240–3,114,240 | CPU/GPU requested separately; production excluded |
| Scientific production: harmonization, MOSAIKS, validation | Pilot within development | TBD | TBD | TBD | Benchmark actual CPU implementation; no invented GPU throughput |
| Reference inference memory per instance | 240 GB system / 80 GB GPU | Same | Same | Included in selected instance | g5.xl reference, not proof selected model fits; more/larger instances change SUs |
| Other worker RAM | TBD | TBD | TBD | Included in selected compute flavors | Peak concurrency and worker memory must be measured |

Awarded ACCESS resources carry no direct usage charge. This is conditional on approval and capacity; no commercial replacement compute is funded. The upper subtotal exceeds Accelerate's 3-million-credit ceiling before production. Provider consultation/Maximize strategy is required. These are resource needs, not awarded funds or an assessed in-kind valuation. Inference hours are aggregate across instances; 9,000 Year 1 hours exceeds one instance running for a 365-day year and requires overlap or larger configurations. CPU service arithmetic uses a standard 365-day planning year; dated allocations must account for actual calendar duration. RAM is per instance, not an aggregate project pool.

## Evidence and remaining validation

Checked official documentation on 26 October 2026:

- [TACC Corral](https://docs.tacc.utexas.edu/hpc/corral/): $60/TB/year reference rate; documented UT System access, annual renewal, online plus tape replica, 200,000 files/TB and requested S3 service at allocations of at least 25 TB. Public distribution and AMBER eligibility require agreement.
- [TACC Ranch](https://docs.tacc.utexas.edu/hpc/ranch/): allocation-based single-copy archive; no published $60 backup rate; unsuitable for operational system backups. Not assumed as the versioned backup service.
- [Jetstream2 flavors](https://docs.jetstream-cloud.org/general/vmsizes/): H100 g5.xl 128 SU/hour, 240 GB system RAM and 80 GB GPU memory; access and availability conditional.
- [ACCESS](https://allocations.access-ci.org/) and [project types](https://allocations.access-ci.org/project-types): no direct charge for allocated resources; resource awards and renewal are not guaranteed.

Repo evidence: [workbench](management-workbench.md), [MOSAIKS](mosaiks-embeddings.md), and [architecture](architecture.md). Source product definitions remain planned; N × D × precision × retained releases must be completed separately for each product. Float32 is implemented; 4,096 dimensions is an allowed setting, not a mandatory dataset specification. Existing tiny-shard publication and bounded verification/import paths need production engineering before national scale.

This document supersedes conversational budget arithmetic, not historical run evidence. Existing seeded OSN/Jetstream2 workspace plans remain historical prototype records and do not implement the new all-TACC target. Run `python scripts/check_resource_budget.py --self-test` for independent CSV arithmetic, Markdown table consistency and deliberately invalid-input checks. The [audit record](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/reports/data_management/budget_validation.md) records the findings. No cloud changes, allocations, scheduled backups or inference were executed. [Machine-readable expense/capacity rows](assets/data/grant-resource-budget.csv) preserve units, rates, years and evidence status. Subtotals must not be summed with component rows.
