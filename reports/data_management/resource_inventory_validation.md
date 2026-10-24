# AMBER technical resource inventory validation

Reviewed: 23 October 2026.

Source: `/Users/tuff/Downloads/AMBER_master_technical_resource_inventory.xlsx`.
SHA-256: `79c3a635d0d4e68c6114866c428e68c93dffc32e1078c2cc686d0072caca593f`.

## Conclusion

The workbook is a usable requirements inventory and preliminary scenario register.
It is not yet a validated global storage estimate, ACCESS resource request, or
financial budget. The original workbook was not changed. All five sheets and
48 resource rows were inspected. The audit compared formulas and cached results,
independently checked arithmetic, reviewed project/repository constraints, and
verified allocation policies against official documentation. Excel recalculation
and native application behavior were not tested.

There are 14 formulas, no cached Excel error cells, no external workbook links,
and no defined names. The XLSX archive passed its member-integrity check.
The 48 resource statuses are: 2 Specified, 35 Estimated, 7 Proposed, 4 Undecided.
These are workbook classifications, not independently verified implementation states.

## Findings and required changes

| Priority | Location | Finding | Required change |
| --- | --- | --- | --- |
| Critical | Master inventory H01-H05, H08 (rows 15-19, 22); D01-D03 (rows 23-25) | Raw extracts, harmonized observations, alignment arrays and checkpoints are budgeted as disk products. Examples include worker memory/scratch with hours-to-days retention, Parquet source extracts, 5-30 TB active harmonized observations, and Zarr/Parquet restart checkpoints. This conflicts with the current streaming design. | Separate aggregate worker RAM from disk. Stream bounded raw and harmonized arrays directly into encoders. Persist restart cursors, immutable identities, manifests and permitted partial feature shards; do not persist raw/harmonized arrays. Any proposed scientific raster release needs explicit separate design and rights review. |
| Critical | Budget and assumptions B10:B19; Three product calculator rows 2-4 | Production and preservation capacities are typed assumptions, not results of the product calculator. Scientific domain, observation count, dimensions, temporal scope and retained versions remain blank. | Identify forest bioresource, cropland food and watershed water products. Define observation support, geographic coverage and gaps, dates, N, D, precision, version policy and shared-source reuse. Link capacity scenarios to these builds. |
| High | Budget and assumptions B2:B4; Master S01-S03; Decisions and gaps rows 2-3 | Five foundational sources plus 5-10 additional sources are labeled confirmed/specified, but no supporting source list is supplied. The project PDF names multiple groups and products; these counts were not established as fixed requirements by this audit. | Treat counts as provisional scope until a dated scientific source register establishes the counting unit and approved IDs. Distinguish source family, dataset, product, asset and observation. |
| High | Three product calculator M2:M4 | N x D x bytes x retained versions / 10^12 is correct for equal-size uncompressed vector generations in decimal TB. | Label its assumptions. Vary counts/dimensions by release or modality where necessary. This is logical vector payload, not physical storage. |
| High | Three product calculator P2:P4; Read me row 11 | SUM includes blank lineage/other costs as zero. The instructions call these optional, so this is not an Excel arithmetic error, but an incomplete estimate can look like a complete product total. | Show a vector-only subtotal or an explicit completeness warning until lineage, labels, encoder artifacts and index costs are either quantified or intentionally excluded. Preserve unknown versus zero. |
| High | Three product calculator R2:R4, T2:T4 | Compute formulas calculate one pass over N observations; they do not account for builds, scientific revisions, training searches, validation passes, failures or retries. | Add distinct execution-pass and experiment assumptions. Retained versions are not automatically equal to full rebuild count. Record hardware, allocated cores/GPUs, wall time, peak RAM and measured throughput. |
| High | Master I02-I06 (rows 32-36); Budget B7:B8 | Five services sum to 14-56 continuous vCPUs if separately provisioned. At 8,760 hours/year for three years this is 367,920-1,471,680 CPU SUs on standard Jetstream2 CPU instances, before notebooks or production. | Reconcile continuous service demand with the 350,000-600,000 SU envelope. Identify co-hosted services, existing OASIS contributions, duty cycles and service start dates. Do not simply add the entire inventory. |
| High | Master W01 (row 40) | Notebook allowance is 100,000-250,000 CPU-hours, described as included in the development envelope. Combined with the above independently provisioned continuous services, demand is 467,920-1,721,680 SUs before other computation. | Build an explicit non-overlapping compute schedule. Separate elapsed worker-hours, CPU core-hours, CPU SUs, GPU-instance SUs and large-memory charges. |
| High | Master D04; Budget B20:B21 | 3,100-31,000 GPU-hours have no model, hardware, experiment or throughput basis. | Keep as unvalidated scenarios. For illustration only, the documented single-A100 Jetstream2 g3.xl flavor costs 64 SUs/hour: 198,400-1,984,000 SUs for that duration. This is not a universal GPU conversion. Budget fitting, encoding, verification and any locally hosted model inference separately. |
| High | Budget B9; Master D01-D03, P02 | Fifty TB is a valid standard OSN ceiling, not a confirmed award or a pathway to 300-500 TB. Larger storage destinations remain uncommitted. | Request/justify pilot storage; obtain a separate larger OSN/pod or partner agreement. Do not assume one allocation per product or working group. |
| High | Budget B14:B15; Master W02 | A shared 20-40 TB workspace is plausible as a request, not a guaranteed quota. Nine groups at 0.5-5 TB each could need 4.5-45 TB if all are active simultaneously. | Model cohort overlap, concurrency and shared-data reads. Jetstream2 generally permits 20 TB for Accelerate and 40 TB for Maximize; allocation tier and provider approval matter. |
| High | Budget B16:B23; Master P01-P04 | Several alternative archive capacities are not reconciled: 300-500 TB protected copy; 12-183 TB curated archive; P02 10-150 TB plus other archive classes. | Build one explicit retained-file inventory per scenario, with source category, version count, copy count and host. A curated subset is not equivalent to a complete release copy. |
| High | Master N column; Read me row 5; Budget B18:B19 | The label Physical storage scenario is unsupported: most figures are logical content, workspace or copy allowances. Physical replication/erasure-coding overhead is unknown. | Rename to logical size/quota allowance and specify occupied logical bytes, provisioned quota, protected copies, physical overhead and duration separately. |
| High | Master P01-P04; Budget B16:B17 | Separate preservation is correctly recognized, but provider, term and recovery commitments are missing. | Obtain agreements specifying retention, responsible operator, fixity, recovery tests, RPO/RTO and migration. OSN is documented as not backed up; never-purged is not a perpetual preservation agreement. |
| Medium | Master S03-G07 and H07 | Metadata/review storage and CPU ranges lack a record-count or throughput basis. Ten to fifteen registrations cannot justify 10-100 GB by themselves; asset-level evidence could change that substantially. | Use assets x average metadata bytes x retained versions; recipes x review rounds x reviewers x transcript/evidence bytes; graph nodes/edges x measured index/export sizes. |
| Medium | Master G04-G07 | Review, model-inference and human labor accounting are incomplete. Operational logs do not necessarily preserve scientific model evidence. | Preserve frozen recipe/evidence IDs, exact prompts and schemas, normalized outputs, provider/model identities, timestamps, findings, vetoes and human decisions. Record transcript scope and only available usage. Separate model tokens/GPU inference from expert person-hours. |
| Medium | Master W01-W06; Budget and assumptions | Nine groups are represented, but 150 participants, 3/6 cohort split, overlapping Years 1-2 and 2-3, and Year 2 Q2 summit concurrency are not modeled as demand drivers. | Add group sizes, active notebook concurrency, CPU/GPU hours per project, summit peak sessions, and workspace retention. Account for publications and consent/rights for recorded media. |
| Medium | Master I02, D06; resource accounting | Public query/transfer demand is not quantified; vector-index cost has no implementation basis. | Specify reads by project, expected bytes/second, concurrent readers, request counts, shard layout, index build RAM/disk and versioning. Obtain provider terms instead of assuming commercial egress charges or unlimited free distribution. |
| Medium | Entire workbook | Resource claims lack verification dates and source URLs; many quantities are text ranges. | Add evidence source, checked date, quantity basis, unit, accounting period, host/allocation, and included-in identifiers. Keep lower/upper quantities numeric in a future calculation build. |
| Medium | Master dependency fields and product context | G08 outputs I07 (containers) without a stated reason; W03 points to operational backup P04 instead of an explicit publication/research archive. Reused source products and track-specific scientific interpretations are not distinguished. | Review dependency references; preserve immutable shared resources with separately identified track products. Complete lineage through observation, applicable track/core recipe, execution, agents, QA/human decisions, source/version/rights. |

## Arithmetic that checks out

- Budget B18: 300 + 20 + 300 = **620 TB**.
- Budget B19: 500 + 40 + 500 = **1,040 TB**, or 1.04 decimal PB.
- These are arithmetically correct assumption sums. They do not validate the underlying production requirement or physical disk capacity.
- Vector formula: 1 billion observations x 4,096 dimensions x 4 bytes x 1 version = **16.384 TB per product**. Three equal products = **49.152 TB before lineage, other artifacts or protection copies**.
- CPU/GPU per-million-observation formulas are correct for the stated single-pass interpretation.
- Blank product outputs are expected from the missing sizing inputs; they are not evidence of a calculated zero requirement.

## Official resource-policy checks

Verified from official documentation on the review date:

1. OSN: standard 10-50 TB project allocation, shared bucket quota, 1 credit per GB, no backup. Above 50 TB requires provider discussion. <https://support.access-ci.org/documentation/resources/osn>
2. OSN provider guidance directs larger requests to discuss hosting/purchase of a pod. <https://www.openstoragenetwork.org/get-involved/get-an-allocation/>
3. Jetstream2 standard CPU: 1 SU per vCPU-hour; 1 ACCESS Credit per Jetstream2 SU. Large-memory/GPU resources and instance-specific costs must be requested separately. <https://docs.jetstream-cloud.org/general/access/>
4. Jetstream2 g3.xl: one A100, 64 SU per elapsed instance-hour. <https://docs.jetstream-cloud.org/general/vmsizes/>
5. Jetstream2 storage: default 1 TB; general limits Explore 5 TB, Discover 5-10 TB, Accelerate 20 TB, Maximize 40 TB. Limits are not awards. <https://docs.jetstream-cloud.org/general/quotas/>
6. ACCESS generally expects one coordinated project per supporting grant. Credit limits are not annual entitlements; Maximize normally uses annual resource-specific awards. <https://allocations.access-ci.org/allocations-policy>
7. Explore/Discover/Accelerate limits are 400,000/1,500,000/3,000,000 credits. <https://allocations.access-ci.org/project-types>

## Recommended order of revision

1. Remove routine raw/harmonized disk persistence from the streaming plan.
2. Name the three products and approved source register, without inventing a fixed source count.
3. Complete product sizing and measured per-resource computational benchmarks.
4. Reconcile active service runtime, notebooks and global builds without overlap.
5. Select a consistent retained-release/copy scenario and identify logical versus physical capacity.
6. Obtain production-storage and preservation commitments; request suitable ACCESS resources.
7. Add network demand, model inference, expert review and cohort concurrency.

No grant-dollar total can be validated from this workbook: there are no monetary
rate schedules, awarded-resource records or signed host commitments. ACCESS resource
quantities and grant-funded operations should remain separate accounting views.
