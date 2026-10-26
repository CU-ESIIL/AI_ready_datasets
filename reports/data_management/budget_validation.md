# Grant resource budget audit — 26 October 2026

Scope: docs/resource-budget.md, docs/assets/data/grant-resource-budget.csv and docs/assets/data/grant-storage-lifecycle.csv. No source data, model inference, cloud provisioning or runtime science executed.

## Pass 1: independent accounting

Recomputed component sums, annual quantities × rates, full-year capacity charges, annual cash totals, total cash, CPU core-hours, GPU SU conversions and range endpoints. Compared numeric cells in the Markdown tables against CSV rows. CSV separates expense quantities from storage components and alternative range endpoints; summing all quantity rows is invalid.

## Pass 2: lifecycle and overlap

Found an underallowance in Year 3 history: current mutable storage declined to 33 TB while earlier monthly snapshots can retain the Year 2 38 TB mutable allocation and deleted governance spaces. Replaced 31 TB ordinary history with 35 TB based on current/prior-year mutable high-water storage plus an explicit 6 TB closeout reserve. Result: 41 TB history, 154 TB total backup, 290 TB combined Year 3 capacity. This is conservative within declared assumptions, not proof of a maximum under arbitrary churn. The six-TB deletion reserve can overlap ordinary history; no savings from overlap are claimed.

Corrected cash: Year 1 $19,020; Year 2 $43,740; Year 3 $57,400; total $120,160. Increase from the previous version: $600. Primary expense $16,500; backup expense $18,660; APIs $60,000; service allowance $25,000. History adds 83 TB-years ($4,980 at assumed $60) over a full-current-copy-only design.

Headroom is ceil(20% of primary content), not a simultaneous complete replacement clone. Recovery targets need provider capacity/throughput confirmation. Version retention can extend beyond grant closeout and is not prepaid here. Standard CPU service arithmetic assumes 365 days/year. Inference hours aggregate across instances; 9,000 hours in Year 3 requires overlap rather than one 24/7 instance.

## Pass 3: provider evidence

Official documents checked on 26 October 2026:

- Corral: https://docs.tacc.utexas.edu/hpc/corral/ publishes $60/TB/year, documented UT System access, included tape replica, annual renewal, 200,000 files/TB and requested S3 access for at least 25 TB. No confirmed AMBER eligibility, separate versioned backup product/price, or public hosting service agreement.
- Jetstream2: https://docs.jetstream-cloud.org/general/vmsizes/ publishes g5.xl at 128 SU/hour with 240 GB system RAM and 80 GB GPU memory. Access/availability and actual model fit remain conditional. CPU and GPU are separate allocation resources.
- ACCESS: https://allocations.access-ci.org/project-types lists Accelerate at 3 million credits for the project duration and Maximize resource awards lasting 12 months. Upper inference/development/service subtotal already exceeds Accelerate before scientific production.

The $60 backup rate is a budget assumption, not a verified separate service price. The $60,000 API and $25,000 hosting totals are spending allowances, not token/usage quotes. All annual storage charges assume the entire provisioned annual maximum is billed for the whole year; no free allocation or compression credit is deducted. No inflation is included.

## Pass 4: reproducibility and invalid cases

Run `python scripts/check_resource_budget.py --self-test`. It recalculates the model, checks CSV/Markdown numeric agreement and rejects deliberate corruptions of backup history, primary expense, inference SUs and Markdown total. Strict MkDocs build and git diff whitespace checks are also required. These validate accounting and documentation, not infrastructure performance or scientific sufficiency.

## Unresolved inputs and sensitivity

- Product storage 20/50/80 TB assumes the provisional global 1 PB is combined across the three products. The repo does not establish that premise or national observation counts/dimensions/releases. Workspace quota arithmetic is repo-backed; quotas are not measured consumption.
- Backup model requires incremental/deduplicated blocks; restore-point percentages are assumed retained changes, not measured daily churn. Verify deletion retention, security isolation, restore cost and history expiration with TACC.
- At twice the assumed backup rate ($120/TB/year), total cash would be $138,820 rather than $120,160, with all other inputs fixed.
- Production harmonization/MOSAIKS/verification remains TBD. No replacement commercial compute, personnel, indirect costs or Years 4–10 is included. Requested compute subtotal 2,864,240–3,114,240 SUs excludes production.
- Local publication and verification need production scaling; tiny-file counts can become a quota problem. Metadata benchmarks are not raster/encoder throughput.

Conclusion: corrected accounting and consistent planning tables, not a fully quoted/benchmarked grant budget. Do not label unverified rates or demand as confirmed costs or adequate capacity.

## Carry-forward ledger follow-up

Added 24 year/type lifecycle rows covering primary components, backup allocations, headroom and total storage. Each row satisfies opening + new - retired = closing, with opening equal to the preceding year's closing value. Product additions are 20/30/30 TB, with no product deletions: closing totals 20/50/80 TB retain earlier releases. Metadata adds 1 TB/year, reaching 3 TB. Workspace quota expands 6 to 36 TB then retires 6 TB governance space only under approved closeout. Backup history retains an additional closeout reserve; retirement of active quota does not mean deleting protected historical content.

The 290 TB Year 3 model assumes closeout precedes the final capacity additions. If workspace retirement is delayed, primary and current-copy backup need 12 TB extra, producing a 302 TB allocation. A full year of that additional capacity at the assumed $60 rate costs $720; alternative grant cash is $120,880. No automated deletion is authorized. Ledger rows model allowance movements, not actual gross writes or snapshot expiry.

Checker now verifies all 24 balances, previous-to-next-year carry-forward, component/subtotal agreement, closing values against the original budget CSV and exact lifecycle Markdown rows. Two additional invalid-input checks reject changed opening/retirement values. All six deliberately invalid cases are rejected. Base cash remains $120,160; capacity remains 67/229/290 TB. Strict documentation build passed.

## Front-loaded inference revision

At user direction, redistributed the same 18,000 H100 reference hours to 9,000/6,000/3,000 across Years 1/2/3, and the same $60,000 commercial API allowance to $30,000/$20,000/$10,000. This is a revised demand assumption rather than an empirical forecast. Current annual cash totals are $39,020 / $43,740 / $37,400; total remains $120,160. Storage and backup quantities/rates are unchanged. Earlier annual totals in this audit are historical findings, superseded by this paragraph. Delayed-closeout sensitivity is now $38,120 in Year 3, still $120,880 across the grant. The 9,000-hour concurrency caveat applies to Year 1 rather than Year 3. Checker and strict build rerun after revision.
