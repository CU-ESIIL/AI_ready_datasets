# Source access, egress and scale audit

Checked 26 October 2026. Read-only inspection of repository and public provider documentation; no dataset acquisition, paid request, authentication change, bulk benchmark or new integration. Repo source list: docs/data-sources.md; src/dataset_prototype/real_data.py and stream_sources.py; data/semantics/validation/dataset_inventory.json. Three AMBER output products are not three source providers. Exact production assets and national source-read volumes remain unspecified.

| Source / route | Repo state | Financial finding | Scale/operational finding |
| --- | --- | --- | --- |
| Sentinel-2 Earth Search and sentinel-cogs HTTPS | Actual tiny historical reads and bounded adapter; real scientifically approved embedding run not established | Current AWS registry lists sentinel-cogs and e84-earth-search-sentinel-data as no-account-required access, rather than Requester Pays. No requester egress charge identified for configured anonymous route | Earth Search public API is free best effort without service guarantee. Repo only accepts legacy sentinel-cogs hostname; newer bucket requires separately reviewed adapter work. Neither free route implies unlimited throughput |
| NEON authenticated HTTPS | Public metadata and token boundary; normalized live acquisition pending | Provider says free to users; egress costs described as costs to NEON, not a user tariff | Token required for downloads, rate limiting applies; API documents expiring Google Cloud URLs. Package formats may require substantial archive transfer even when processed in bounded memory |
| Landsat direct usgs-landsat S3 | Planned | Verified Requester Pays, requests and external egress can bill requesting AWS account | Jetstream2 is not AWS us-west-2; cannot assume same-region access. EarthExplorer is a free alternative, not automatically equivalent to streaming COG access |
| NASA ORNL DAAC | Candidate, no exact product/access route selected | NASA EOSDIS guidance says user downloads free, egress supported by EOSDIS; no ORNL-specific production route verified | Authenticate as required, direct S3 can have region restrictions and HTTPS can throttle. ORNL landing access returned 403 in research tool; do not infer service outage or permission status |
| AmeriFlux | Candidate, no product adapter | Provider explicitly describes datasets as free | Account and site/product licensing apply; Legacy and CC BY products differ. No nationwide streaming throughput commitment established |
| LTER / EDI | Candidate, no individual package selected | No per-GB download tariff identified in reviewed access docs; not a blanket guarantee for every LTER host | EDI announces required REST API authentication from July 30, 2026. EDI large-volume deposit/curation cost sharing is not a download charge |
| TRY | Candidate, no permitted subset adapter | No egress price established from reviewed policies; unknown is not zero | Request-based release, embargo permissions and package-specific rights. Updated 2023 guidelines describe public CC BY and restricted embargoed records; older web policy has broader redistribution language, requiring exact request/license review |
| CartograPlant | Under evaluation, no selected endpoint | Unresolved: no verified access/egress tariff or national service agreement | Provider research paper describes registered user downloads/workspaces. Website fetch returned 502 in research tool; no paid plan inferred and not confused with unrelated Cartographer service |

## Budget consequence

No evidence supports a blanket $25,000 source access/endpoint charge. Preserve current budget CSV unchanged pending a decision and named provider quote; do not label that allowance validated. Landsat direct Requester Pays is a specific possible billable expense, which should be estimated from selected asset route, billable transferred bytes, requests, billing region and current AWS tariff. No paid AWS account or route was used here. Do not automatically opt in to Requester Pays or claim free EarthExplorer access satisfies raw-data streaming constraints.

No documented per-GB TACC outgoing tariff or Jetstream2-to-TACC transfer quote was established by this source-provider audit; both remain questions for providers, not evidence of zero or a fixed charge. Dataset delivery, portal metadata and source acquisition are distinct routes.

Streaming avoids source disk persistence but still transfers bytes. Measure actual compressed COG blocks/archives and HTTP requests, not just selected pixel values. Account for repeat scientific builds, failed/retried reads, mask/metadata accesses and references used for fitting. Do not infer input transfer from final feature size. Retain bounded in-memory worker caches and restart/lineage metadata within policy; no raw/harmonized disk cache is authorized. Public endpoint throttles and authentication can extend compute wall time even without a transfer invoice.

## Official evidence

- Sentinel buckets, including legacy: https://registry.opendata.aws/sentinel-2-l2a-cogs/
- Earth Search service and asset billing distinction: https://github.com/Element84/earth-search/blob/main/README.md
- NEON free access and provider-paid egress context: https://www.neonscience.org/about/user-accounts
- NEON API and authentication: https://data.neonscience.org/data-api/ ; file/URL details: https://data.neonscience.org/data-api/endpoints/data/
- Landsat direct Requester Pays: https://www.usgs.gov/software/introduction-landsat-cloud-access-direct-requester-pays
- USGS route/cost comparison: https://www.usgs.gov/faqs/when-do-i-need-amazon-web-services-aws-account-access-landsat-data-cloud-there-a-cost
- NASA download/egress sponsorship context: https://www.earthdata.nasa.gov/s3fs-public/imported/02_Understanding_and_Managing_Costs_in_the_AWS_Cloud.pdf
- NASA route-specific example (PO.DAAC, not an ORNL verification): https://podaac.jpl.nasa.gov/cloud-datasets/faq
- AmeriFlux free dataset access: https://ameriflux.lbl.gov/data/aboutdata/ ; licenses: https://ameriflux.lbl.gov/data/data-policy/
- EDI access: https://www.edirepository.org/resources/accessing-data ; authentication announcement: https://edirepository.org/ ; deposit versus acquisition: https://www.edirepository.org/support/frequently-asked-questions
- TRY updated guidelines: https://www.try-db.org/TryWeb/TRY_Intellectual_Property_Guidelines.pdf ; older web policy: https://www.try-db.org/TryWeb/DataUsePolicy.php
- CartograPlant provider-authored paper: https://academic.oup.com/genetics/article/232/4/iyag060/8509013

Remaining: source product/version/asset list for each output collection; exact fee-bearing endpoints; product-specific request/rate policy; read-volume and concurrency measurements; TACC/Jetstream2 transfer and backup terms. No source-wide financial guarantee from small successful reads is claimed.
