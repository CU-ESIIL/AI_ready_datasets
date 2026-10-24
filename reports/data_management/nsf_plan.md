# Data Management and Sharing Plan

AI-ready environmental datasets through governed discovery, harmonization, and MOSAIKS representation

Draft for Research.gov entry | 23 October 2026

## 1. Types of data and research products

The project will produce source-discovery records and semantic inventories; versioned harmonization recipes; specialist-agent proposals, QA findings, and human decisions; MOSAIKS feature datasets and fitted encoder artifacts; verification datasets and metrics; and software, documentation, and reproducibility manifests. The computational scope anticipates no new physical samples or human-subject data collection. Sentinel-2 imagery and NEON environmental observations are intended source families; live capabilities and incomplete integrations will be labeled separately from generated test fixtures.

Source observations will remain in provider repositories. New real-data processing will retrieve bounded windows into memory, apply approved deterministic harmonization, and pass harmonized raster patches directly into MOSAIKS. Neither raw windows nor harmonized rasters will be routinely written to disk, including during tests. Offline tests will use generated in-memory arrays and iterators. Existing historical snapshot workflows will remain explicitly identified and excluded from claims about the streaming design.

Durable outputs will include feature shards, row-level observation lineage, encoder filters and training context, dataset cards, verification labels, and complete/failed run manifests. Empirical MOSAIKS filters and normalization will use training data only. Validation and test tiles will be excluded from fitting. Verification will distinguish independent labels from derived diagnostics and proxy labels. Storage estimates will be refined through bounded pilots; float32 vectors require 4 x rows x dimensions bytes, excluding metadata, filters, and backups.

## 2. Standards for data and metadata

Discovery will preserve native STAC Items where available, source identifiers and versions, asset locations, sensor/platform identity, processing baseline, calibration and quality evidence, and source-specific rights and citations. Native CRS, pixel indices, spatial support, footprint, temporal support, and measurement definitions will remain explicit. Source digital numbers will be distinguished from calibrated reflectance; scientific calibration will occur only through validated recipes with authoritative metadata references.

Versioned typed JSON schemas will define module contracts and review records. JSON/JSONL, CSV, and Parquet will carry metadata and diagnostics; non-pickled NumPy arrays will carry numerical vectors and filters. Documentation will provide field definitions, units, channel order, missing-value conventions, split assignments, and format/schema versions. Community ontology identifiers and source definitions will be preserved without asserting equivalence from labels. Project-specific semantic extensions will require documented evidence and review.

Each representation will retain links to its source observation/window, core and applicable track recipe, transformation implementation, agent proposal, QA decision, and applicable human decision. Manifests will record software/backend and encoder identities and checksums with explicit scope. Metadata and extracted-window hashes will never be described as checksums of whole remote assets. Provenance exports will use a documented JSON-LD structure inspired by PROV; unsupported formal conformance will not be claimed.

## 3. Access, sharing, and protection

Data supporting NSF-funded publications will be made available at publication, with any necessary exceptions described and justified in this plan. Public release packages will contain the supporting vectors, permitted verification data, recipes, encoder artifacts, lineage, software versions, and reuse documentation. Dataset persistent identifiers and associated publication links will be included in NSF reporting through the applicable PAR workflow. Additional curated products will be released when their scientific and rights reviews are complete.

During development, durable products will reside in [institution-approved active storage], with access assigned by project role. Credentials will remain outside public repositories and release packages. Only institution-approved model services will receive reviewed, bounded metadata; provider retention, training-use, and access terms must be assessed before restricted material is transmitted. Models will have no execution tools. Scientific operations will be pre-written and registered; deterministic checks, specialist consensus, QA vetoes, and exact-recipe human approval will govern execution.

Release review will address source restrictions, sensitive ecological locations, privacy, intellectual property, and Indigenous data governance where applicable. Vectors and filters will be treated as source-derived products, not presumed anonymous or unrestricted. Necessary restrictions will be documented with access procedures and permissible public metadata; consequential changes or exceptions will follow NSF approval requirements. Public website content will be a curated view, not an automatic publication of working directories or model logs.

## 4. Reuse, redistribution, and derivatives

Each release will retain source-specific license evidence, attribution, citation instructions, and derivative/redistribution conditions. Public accessibility will not be treated as permission to redistribute source data or embeddings. Project-authored software will use [institution-approved open-source license]; project-authored data and metadata will use [approved reuse license], only where compatible with upstream rights. Third-party materials will retain their own terms. Unclear rights will block redistribution pending review.

Dataset cards will identify intended uses, canonical variable definitions and units, harmonization assumptions, encoder/preprocessing identities, spatial and temporal limits, and verification evidence. Scientific harmonization will remain separate from model preprocessing. Benchmark rankings and semantic coverage scores will be labeled project diagnostics; neither they nor generated-data tests establish scientific equivalence, independent ecological validity, or native language-model understanding. Reusers will be able to distinguish observed evidence, deterministic derivations, model judgments, and human decisions.

## 5. Archiving and preservation of access

The PI will be accountable for this plan and will designate a data steward to maintain inventories, access controls, release reviews, and preservation records. Approved releases will be deposited in [named discipline or institutional repository assigning persistent identifiers]. [Institution/unit] will provide active-storage backup and recovery under [documented schedule], and preservation will follow [specified retention period and repository policy]. These institutional commitments and associated costs must be confirmed before submission.

Preservation packages will include open-format metadata, vectors, filters, verification data, recipes and schemas, software/environment versions, rights statements, and checksummed manifests. The steward will check package completeness and fixity before deposit and test restoration from active-storage backups according to the confirmed schedule. Failed runs, malformed model responses, disagreements, and historical vetoes will be retained in controlled project records; publication packages will include the evidence necessary to assess reported results, subject to documented protections.

Reproducibility depends on access to the exact upstream observations. The project will prefer persistent provider versions and verify their availability when releasing supporting datasets. If provider retention cannot preserve required publication-supporting data, the PI will arrange an authorized preservation solution or an approved exception before relying on that release; metadata hashes alone will not substitute for unavailable observations. Any preservation change requiring raw-data retention will undergo explicit scientific, rights, and design review. The steward will maintain a repository landing page and update locations and identifiers when products migrate.
