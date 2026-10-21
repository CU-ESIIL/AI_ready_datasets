# Ontology and semantic-resource landscape

A growing landscape inventory of **86 resources**, not an exhaustive list or an adoption decision. Formal and application ontologies, standards, classifications, thesauri, frameworks and historical efforts serve different purposes.

The canonical CSV lives in `data/semantics/semantic_resources.csv`. This page and the [coverage matrix](comparison.md) are generated with `python scripts/generate_semantics.py`. [Download every inventory field](semantic_resources.csv), [auditable project assessments](assessments.jsonl) or [inspected registry fact evidence](verification_sources.json).

Resource identities, registry status and cited documentation are **resource facts** with a verification scope. Coverage, candidate roles, eras, limitations and influence are **provisional project assessments** by the coding assistant, not expert-reviewed ontology properties. Unknown release dates/rights stay unknown. A milestone below is not necessarily the first release; eras overlap.

!!! note "Do not collapse distinctions"
    [Organism, taxon, population and community](distinctions.md) describe different things. An ontology, vocabulary and exchange standard are also different kinds of resource. [Scale is not one dimension](scale-support.md).

## Master inventory

| Resource | Kind / domain | Era and origin/milestone | Contribution (project reading) | Project role | Verification |
| --- | --- | --- | --- | --- | --- |
| [Basic Formal Ontology](#bfo) | `upper_ontology` / foundations | unknown; First release not established in inspected registry metadata | Distinguishes broad categories of entities and processes | domain_overlay | registry_metadata |
| [Information Artifact Ontology](#iao) | `formal_ontology` / foundations | unknown; First release not established in inspected registry metadata | Describes information entities used in scientific records | domain_overlay | registry_metadata |
| [Relation Ontology](#ro) | `relation_ontology` / foundations | unknown; First release not established in inspected registry metadata | Provides explicitly defined relations used across OBO resources | provisional_core | registry_metadata |
| [NCBI organismal classification](#ncbitaxon) | `classification` / taxonomy | unknown; First release not established in inspected registry metadata | Provides organismal taxonomic identifiers in an ontology representation | provisional_core | registry_metadata |
| [Taxonomic Rank Vocabulary](#taxrank) | `controlled_vocabulary` / taxonomy | unknown; First release not established in inspected registry metadata | Names taxonomic ranks | domain_overlay | registry_metadata |
| [Population and Community Ontology](#pco) | `formal_ontology` / biology | unknown; First release not established in inspected registry metadata | Describes collections and interacting groups of organisms | provisional_core | registry_metadata |
| [Environment Ontology](#envo) | `formal_ontology` / environment | unknown; First release not established in inspected registry metadata | Distinguishes environmental systems features and materials | provisional_core | registry_metadata |
| [Biological Collections Ontology](#bco) | `formal_ontology` / observations | unknown; First release not established in inspected registry metadata | Models collecting sampling and biological material | domain_overlay | registry_metadata |
| [Ontology for Biomedical Investigations](#obi) | `formal_ontology` / observations | unknown; First release not established in inspected registry metadata | Describes investigations instruments protocols and assays | domain_overlay | registry_metadata |
| [Ontology of Biological Attributes](#oba) | `formal_ontology` / traits | unknown; First release not established in inspected registry metadata | Composes biological attributes for measurable characteristics | provisional_core | registry_metadata |
| [Phenotype And Trait Ontology](#pato) | `formal_ontology` / traits | unknown; First release not established in inspected registry metadata | Provides qualities for entity-quality descriptions | provisional_core | registry_metadata |
| [Plant Trait Ontology](#to) | `formal_ontology` / traits | unknown; First release not established in inspected registry metadata | Names plant traits | domain_overlay | registry_metadata |
| [Plant Ontology](#po) | `formal_ontology` / anatomy | unknown; First release not established in inspected registry metadata | Describes plant anatomy and development | provisional_core | registry_metadata |
| [Flora Phenotype Ontology](#flopo) | `application_ontology` / traits | unknown; First release not established in inspected registry metadata | Connects flora phenotype descriptions | domain_overlay | registry_metadata |
| [Vertebrate Trait Ontology](#vt) | `formal_ontology` / traits | unknown; First release not established in inspected registry metadata | Describes vertebrate traits | domain_overlay | registry_metadata |
| [Clinical Measurement Ontology](#cmo) | `formal_ontology` / traits | unknown; First release not established in inspected registry metadata | Describes clinical measurement types | domain_overlay | registry_metadata |
| [Uberon multispecies anatomy ontology](#uberon) | `formal_ontology` / anatomy | unknown; First release not established in inspected registry metadata | Connects anatomical structures across species | provisional_core | registry_metadata |
| [Cell Ontology](#cl) | `formal_ontology` / anatomy | unknown; First release not established in inspected registry metadata | Describes cell types | domain_overlay | registry_metadata |
| [Common Anatomy Reference Ontology](#caro) | `formal_ontology` / anatomy | unknown; First release not established in inspected registry metadata | Supplies shared anatomical categories | domain_overlay | registry_metadata |
| [Biological Spatial Ontology](#bspo) | `formal_ontology` / anatomy | unknown; First release not established in inspected registry metadata | Describes anatomical spatial organization | domain_overlay | registry_metadata |
| [Gene Ontology](#go) | `formal_ontology` / molecular | unknown; First release not established in inspected registry metadata | Describes molecular functions biological processes and cellular components | domain_overlay | registry_metadata |
| [Sequence Ontology](#so) | `formal_ontology` / molecular | unknown; First release not established in inspected registry metadata | Describes biological sequence features | domain_overlay | registry_metadata |
| [Protein Ontology](#pr) | `formal_ontology` / molecular | unknown; First release not established in inspected registry metadata | Represents protein forms and relationships | domain_overlay | registry_metadata |
| [Chemical Entities of Biological Interest](#chebi) | `formal_ontology` / molecular | unknown; First release not established in inspected registry metadata | Identifies chemical entities | domain_overlay | registry_metadata |
| [Neuro Behavior Ontology](#nbo) | `formal_ontology` / behavior | unknown; First release not established in inspected registry metadata | Describes behavioral processes and phenotypes | domain_overlay | registry_metadata |
| [Ontology of Microbial Phenotypes](#omp) | `formal_ontology` / microbiome | unknown; First release not established in inspected registry metadata | Describes microbial phenotypes | domain_overlay | registry_metadata |
| [MicrO: Prokaryotic Phenotypic and Metabolic Characters](#micro) | `formal_ontology` / microbiome | unknown; First release not established in inspected registry metadata | Describes prokaryotic phenotypic and metabolic characters | domain_overlay | registry_metadata |
| [Ontology of Host-Microbiome Interactions](#ohmi) | `formal_ontology` / microbiome | unknown; First release not established in inspected registry metadata | Connects hosts microbiomes and their interactions | domain_overlay | registry_metadata |
| [Agronomy Ontology](#agro) | `formal_ontology` / agriculture | unknown; First release not established in inspected registry metadata | Describes agronomic experiments and management | domain_overlay | registry_metadata |
| [Plant Experimental Conditions Ontology](#peco) | `formal_ontology` / agriculture | unknown; First release not established in inspected registry metadata | Names plant experimental conditions | domain_overlay | registry_metadata |
| [Food Ontology](#foodon) | `formal_ontology` / agriculture | unknown; First release not established in inspected registry metadata | Describes food products sources and processing | domain_overlay | registry_metadata |
| [Units of Measurement Ontology](#uo) | `formal_ontology` / quantities | unknown; First release not established in inspected registry metadata | Identifies measurement units | domain_overlay | registry_metadata |
| [DOLCE / DUL](#dolce) | `upper_ontology` / foundations | 2000s; 2002 DOLCE publication; DUL is a later lightweight variant | Descriptive foundational categories and a lightweight DUL vocabulary | domain_overlay | reference_only |
| [Simple Knowledge Organization System](#skos) | `semantic_framework` / foundations | 2000s; 2009 W3C Recommendation | Represents concept schemes labels and broader narrower mappings | interoperability | primary_documentation |
| [Taxonomic Concept Schema](#tcs) | `exchange_standard` / taxonomy | 2000s; 2005 TCS standard; subsequent TCS2 revision work | Separates taxon names from taxon concepts in exchange | interoperability | primary_documentation |
| [Darwin Core](#dwc) | `exchange_standard` / biodiversity | 2000s; 2009 TDWG ratification; work predates ratification | Provides community terms for biodiversity data exchange | interoperability | primary_documentation |
| [Darwin Core Conceptual Model](#dwc_cm) | `conceptual_model` / biodiversity | 2020s; Current conceptual-model documentation; earliest origin not established | Explains relationships among Darwin Core classes | domain_overlay | primary_documentation |
| [Darwin-SW](#darwin_sw) | `application_ontology` / biodiversity | 2010s; TDWG RDF work; exact first release not established | Models relationships complementing Darwin Core in RDF | domain_overlay | primary_documentation |
| [WoRMS / Aphia taxonomic resources](#worms) | `controlled_vocabulary` / marine | 2000s; Aphia/WoRMS database development; exact first release not established | Provides authoritative marine names and stable Aphia identifiers | domain_overlay | primary_documentation |
| [Humboldt Extension](#humboldt) | `exchange_standard` / biodiversity | 2010s; 2017 Humboldt Core paper; later TDWG vocabulary | Adds ecological inventory scope and effort metadata | interoperability | primary_documentation |
| [Extensible Observation Ontology](#oboe) | `formal_ontology` / observations | 2000s; 2007 ecological observation paper | Relates observations measurements entities characteristics standards and protocols | provisional_core | primary_documentation |
| [Sensor Observation Sample and Actuator](#sosa) | `formal_ontology` / observations | 2010s; 2017 W3C/OGC Recommendation | Lightweight core for observations sampling and sensing | provisional_core | primary_documentation |
| [Semantic Sensor Network Ontology](#ssn) | `formal_ontology` / observations | 2010s; 2017 Recommendation; earlier SSN work exists | Extends sensor and observation modeling around SOSA | domain_overlay | primary_documentation |
| [I-ADOPT Interoperability Framework](#iadopt) | `semantic_framework` / observations | 2020s; 2021 framework and recommendations | Decomposes variables into property object of interest matrix context and constraints | provisional_core | primary_documentation |
| [Ecological Trait-data Standard](#ets) | `exchange_standard` / traits | 2010s; 2018 rationale; 2019 v0.10 citation | Describes trait data with persistent vocabulary fields | interoperability | primary_documentation |
| [Minimum Information about any Sequence](#mixs) | `metadata_standard` / molecular | 2010s; 2011 MIxS publication; predecessor checklists are earlier | Describes sequence sample context through checklists and extensions | interoperability | primary_documentation |
| [Microbiome Ontology Core](#microbiome_core) | `formal_ontology` / microbiome | 2010s; Repository history includes 2018; release identity needs verification | Top-level microbiome ontology effort | domain_overlay | primary_documentation |
| [GloBI + RO](#globi) | `resource_network` / interactions | 2010s; Project origin and version history require resource-specific review | Links biotic-interaction records using community relations and source citations | domain_overlay | reference_only |
| [Soil Food Web Ontology](#sfwo) | `application_ontology` / interactions | 2020s; 2023 ontology paper | Describes trophic groups resources processes and dietary traits | domain_overlay | primary_documentation |
| [AGROVOC](#agrovoc) | `thesaurus` / agriculture | pre1990; 1980s thesaurus roots; precise origin not reverified | Multilingual agricultural concepts and relations for discovery | domain_overlay | primary_documentation |
| [Crop Ontology](#crop) | `controlled_vocabulary` / agriculture | 2010s; Exact first release not established | Connects crop traits measurement methods and scales | domain_overlay | reference_only |
| [Minimum Information About Plant Phenotyping Experiments](#miappe) | `metadata_standard` / agriculture | 2010s; Community standard; exact first release not established | Specifies experimental phenotyping metadata through checklist and data model | interoperability | primary_documentation |
| [Plant Phenotyping Experiment Ontology](#ppeo) | `application_ontology` / agriculture | 2010s; Implementation of MIAPPE; precise origin not established | Represents MIAPPE experimental metadata structure | domain_overlay | reference_only |
| [Plant Stress Ontology](#pso) | `formal_ontology` / agriculture | 2010s; Planteome development; first release not established | Describes biotic and abiotic plant stresses | domain_overlay | primary_documentation |
| [Animal Trait Ontology for Livestock](#atol) | `formal_ontology` / agriculture | unknown; Primary version and identifier pattern need verification | Describes livestock traits | domain_overlay | unresolved |
| [Environment Ontology for Livestock](#eol) | `formal_ontology` / agriculture | unknown; Identity retained as a review lead; official release not verified | Describes livestock farm environmental conditions | domain_overlay | unresolved |
| [Livestock Product Trait Ontology](#lpt) | `controlled_vocabulary` / agriculture | unknown; Primary ontology release and rights need verification | Describes traits of livestock products | domain_overlay | unresolved |
| [Semantic Web for Earth and Environmental Terminology](#sweet) | `resource_network` / environment | 2000s; NASA Earth-science semantic work; precise origin not established | Provides linked Earth-system terminology modules | domain_overlay | primary_documentation |
| [Ecosystems Ontology](#ecso) | `formal_ontology` / environment | 2010s; DataONE semantic provenance effort; first release not established | Describes ecosystem observation concepts in DataONE work | domain_overlay | primary_documentation |
| [CF Standard Names](#cf) | `controlled_vocabulary` / environment | 2000s; CF conventions development; specific table versions are separately versioned | Provides named physical quantities with canonical units | domain_overlay | primary_documentation |
| [GCMD Keywords](#gcmd) | `controlled_vocabulary` / environment | 1990s; GCMD catalog lineage; exact first keyword release not established | Supports Earth-science discovery using managed keyword hierarchies | domain_overlay | primary_documentation |
| [General Multilingual Environmental Thesaurus](#gemet) | `thesaurus` / environment | 1990s; Development since 1995 documented by EEA | Connects multilingual environmental indexing concepts | domain_overlay | primary_documentation |
| [IUCN Habitats Classification Scheme](#iucn_habitat) | `classification` / conservation | unknown; Version 3.1 documentation; origin not established | Names habitat classes for Red List assessments | domain_overlay | primary_documentation |
| [IUCN Threats Classification Scheme](#iucn_threat) | `classification` / conservation | unknown; Version 3.3 documentation; origin not established | Classifies direct threats in species assessments | domain_overlay | primary_documentation |
| [IUCN Red List Categories and Criteria](#iucn_redlist) | `classification` / conservation | 1990s; Modern criteria development; exact milestone requires review | Organizes extinction-risk assessment categories and criteria | domain_overlay | reference_only |
| [Essential Biodiversity Variables](#ebv) | `conceptual_model` / conservation | 2010s; 2013 EBV paper | Organizes biodiversity state variables across organization space and time | domain_overlay | primary_documentation |
| [EBV application-ontology / Bari Manifesto work](#bari) | `semantic_framework` / conservation | 2010s; 2018 Bari Manifesto | Proposes interoperability architecture for EBV production | domain_overlay | primary_documentation |
| [BON in a Box semantic work](#bon_box) | `semantic_framework` / conservation | 2010s; 2015 initiative brochure; semantic-artifact origin unresolved | Connects biodiversity monitoring workflow resources | domain_overlay | reference_only |
| [MarineTLO](#marine_tlo) | `upper_ontology` / marine | 2010s; 2013 marine integration work | Integrates marine facts with categorical and spatiotemporal context | domain_overlay | primary_documentation |
| [Marine Regions semantic resources](#marine_regions) | `controlled_vocabulary` / marine | unknown; Gazetteer and vocabulary versions require separate review | Provides marine geographic identifiers and spatial reference resources | domain_overlay | reference_only |
| [APHIA ontology network](#aphia_network) | `resource_network` / marine | 2020s; Network documentation inspected; exact first release not established | Provides linked vocabularies across Aphia information modules | domain_overlay | primary_documentation |
| [GeoSPARQL](#geosparql) | `formal_ontology` / space | 2010s; 2012 initial standard; subsequent revisions exist | Represents geospatial features geometry and spatial relations | provisional_core | primary_documentation |
| [OWL-Time](#owl_time) | `formal_ontology` / time | 2010s; 2017 Recommendation; earlier work and later drafts overlap | Represents temporal instants intervals and relations | provisional_core | primary_documentation |
| [Quantities Units Dimensions and Types](#qudt) | `formal_ontology` / quantities | 2000s; NASA NExIOM lineage; exact first release not established | Represents quantities quantity kinds dimensions and units | provisional_core | primary_documentation |
| [PROV-O](#prov) | `formal_ontology` / provenance | 2010s; 2013 W3C Recommendation | Represents entities activities agents and derivations | provisional_core | primary_documentation |
| [ProvONE](#provone) | `application_ontology` / provenance | 2010s; DataONE scientific workflow provenance | Extends provenance for scientific workflow structure and execution | domain_overlay | primary_documentation |
| [Data Catalog Vocabulary](#dcat) | `metadata_standard` / infrastructure | 2010s; 2014 first Recommendation; 2024 DCAT 3 | Describes datasets distributions and catalog services | interoperability | primary_documentation |
| [Dublin Core / DCTERMS](#dcterms) | `metadata_standard` / infrastructure | 1990s; 1995 workshop lineage | Provides general resource metadata terms | interoperability | primary_documentation |
| [DataCite Metadata Schema](#datacite) | `metadata_standard` / infrastructure | 2010s; Schema revisions are versioned; origin not established | Describes research outputs for identification citation and discovery | interoperability | primary_documentation |
| [SpatioTemporal Asset Catalog](#stac) | `metadata_standard` / infrastructure | 2010s; Community development before 1.0; precise origin not reverified | Describes spatiotemporal assets with extension metadata | interoperability | primary_documentation |
| [Ecological Metadata Language](#eml) | `metadata_standard` / ecology | 1990s; 1997 metadata work cited as precursor; EML releases followed | Documents ecological dataset entities methods attributes and access | interoperability | primary_documentation |
| [Ecolingua](#ecolingua) | `historical_effort` / ecology | 2000s; 2006 formal ontology paper | Formalizes ecological data for model synthesis | historical_comparison | primary_documentation |
| [SEEK semantic mediation](#seek) | `historical_effort` / ecology | 2000s; 2003 project notes and associated OBOE lineage | Explored semantic annotation and mediation of ecological datasets | historical_comparison | primary_documentation |
| [OBOE ecology extensions](#oboe_ecology) | `resource_network` / ecology | 2000s; OBOE 2007 lineage; individual extensions vary | Extends an observation model with ecological terms | domain_overlay | primary_documentation |
| [Historical biodiversity ontology efforts](#biodiversity_history) | `historical_effort` / biodiversity | 2000s; TDWG name concept and RDF efforts overlap across decades | Preserves prior TDWG semantic-model experiments for comparison | historical_comparison | unresolved |
| [AnaEE semantic resources](#anaee) | `resource_network` / ecology | 2020s; 2020 technical report; individual semantic resources need identification | Identifies an ecosystem-experiment semantic infrastructure review area | domain_overlay | unresolved |

## Resource details, limitations and evidence

An empty crosswalk/dependency field means **not recorded in this review**, not that none exists. Registry dependency metadata is not a parsed OWL-import graph. Resolvable identifiers mean the source declares persistent identifiers; live resolution of every term was not tested. Portal APIs are not assumed from a downloadable OWL file.

### Basic Formal Ontology { #bfo }

**Identity and status:** BFO; `upper_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Barry Smith.
**Original problem / contribution (project reading):** Project reading of documented scope: Distinguishes broad categories of entities and processes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Distinguishes broad categories of entities and processes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Upper categories do not identify biological variables or justify support changes.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bfo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bfo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bfo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Information Artifact Ontology { #iao }

**Identity and status:** IAO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jie Zheng.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes information entities used in scientific records.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes information entities used in scientific records.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** An information model does not establish the truth of an annotation.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/iao.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/iao.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `iao.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Relation Ontology { #ro }

**Identity and status:** RO; `relation_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides explicitly defined relations used across OBO resources.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides explicitly defined relations used across OBO resources.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A relation name alone does not validate its application to a pair of source concepts.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### NCBI organismal classification { #ncbitaxon }

**Identity and status:** NCBITaxon; `classification`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Frederic Bastian.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides organismal taxonomic identifiers in an ontology representation.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides organismal taxonomic identifiers in an ontology representation.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Taxonomic identity does not imply ecological or measurement equivalence.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ncbitaxon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ncbitaxon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ncbitaxon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Taxonomic Rank Vocabulary { #taxrank }

**Identity and status:** TAXRANK; `controlled_vocabulary`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jim Balhoff.
**Original problem / contribution (project reading):** Project reading of documented scope: Names taxonomic ranks.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names taxonomic ranks.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Ranks do not resolve competing taxon concepts or population membership.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/taxrank.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/taxrank.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `taxrank.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Population and Community Ontology { #pco }

**Identity and status:** PCO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Ramona Walls.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes collections and interacting groups of organisms.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes collections and interacting groups of organisms.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not by itself solve remote-sensing spatial support or population estimation.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, caro, envo, go, iao, ncbitaxon, pato, ro. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Environment Ontology { #envo }

**Identity and status:** ENVO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pier Luigi Buttigieg.
**Original problem / contribution (project reading):** Project reading of documented scope: Distinguishes environmental systems features and materials.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Distinguishes environmental systems features and materials.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Environmental annotations do not justify transferring measurements across supports.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** chebi, foodon, go, ncbitaxon, pco, po, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/envo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/envo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `envo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Biological Collections Ontology { #bco }

**Identity and status:** BCO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Ramona Walls.
**Original problem / contribution (project reading):** Project reading of documented scope: Models collecting sampling and biological material.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Models collecting sampling and biological material.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Collection metadata does not automatically establish taxon equivalence or sensor calibration.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ontology for Biomedical Investigations { #obi }

**Identity and status:** OBI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Bjoern Peters.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes investigations instruments protocols and assays.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes investigations instruments protocols and assays.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Investigation descriptions do not establish compatibility with every ecological protocol.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/obi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/obi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `obi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ontology of Biological Attributes { #oba }

**Identity and status:** OBA; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Composes biological attributes for measurable characteristics.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Composes biological attributes for measurable characteristics.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Attributes need observation methods units and support to interpret measurements.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/oba.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/oba.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `oba.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Phenotype And Trait Ontology { #pato }

**Identity and status:** PATO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides qualities for entity-quality descriptions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides qualities for entity-quality descriptions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A quality term alone is not a complete variable or measurement protocol.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pato.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pato.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pato.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Plant Trait Ontology { #to }

**Identity and status:** TO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Names plant traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names plant traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not replace taxon method unit or plot-support evidence.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/to.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/to.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `to.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Plant Ontology { #po }

**Identity and status:** PO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes plant anatomy and development.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes plant anatomy and development.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical containment is not ecological aggregation.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/po.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/po.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `po.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Flora Phenotype Ontology { #flopo }

**Identity and status:** FLOPO; `application_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Robert Hoehndorf.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects flora phenotype descriptions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects flora phenotype descriptions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Text-derived phenotype coverage is not universal trait measurement coverage.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/flopo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/flopo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `flopo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Vertebrate Trait Ontology { #vt }

**Identity and status:** VT; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Carissa Park.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes vertebrate traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes vertebrate traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Vertebrate scope cannot be silently applied to all organisms.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/vt.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/vt.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `vt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Clinical Measurement Ontology { #cmo }

**Identity and status:** CMO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jennifer Smith.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes clinical measurement types.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes clinical measurement types.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Clinical scope does not establish ecological measurement equivalence.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/cmo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/cmo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `cmo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Uberon multispecies anatomy ontology { #uberon }

**Identity and status:** UBERON; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects anatomical structures across species.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects anatomical structures across species.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical correspondence is not a rule for ecosystem or raster support.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, bspo, chebi, cl, envo, go, nbo, ncbitaxon, omo, pato, pr, ro. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/uberon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/uberon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `uberon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Cell Ontology { #cl }

**Identity and status:** CL; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: David Osumi-Sutherland.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes cell types.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes cell types.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Cell type is distinct from taxon organism and sampled cell abundance.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** go, ncbitaxon, omo, pato, pr, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/cl.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/cl.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `cl.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Common Anatomy Reference Ontology { #caro }

**Identity and status:** CARO; `formal_ontology`; inactive_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Melissa Haendel.
**Original problem / contribution (project reading):** Project reading of documented scope: Supplies shared anatomical categories.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Supplies shared anatomical categories.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Reference anatomy is not a complete organism-specific anatomical or ecological model.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/caro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `caro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Biological Spatial Ontology { #bspo }

**Identity and status:** BSPO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes anatomical spatial organization.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes anatomical spatial organization.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical spatial relations are not geospatial CRS or raster support.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bspo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bspo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bspo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Gene Ontology { #go }

**Identity and status:** GO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Suzi Aleksander.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes molecular functions biological processes and cellular components.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes molecular functions biological processes and cellular components.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Functional annotation does not directly define organism or community ecological traits.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** cl, go/extensions/go-bridge-to-nifstd.owl, ncbitaxon, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/go.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/go.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `go.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Sequence Ontology { #so }

**Identity and status:** SO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Karen Eilbeck.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes biological sequence features.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes biological sequence features.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Sequence features do not establish organismal abundance or habitat equivalence.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/so.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/so.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `so.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Protein Ontology { #pr }

**Identity and status:** PRO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Darren Natale.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents protein forms and relationships.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents protein forms and relationships.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Protein identity does not substitute for experimental context or ecological support.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pr.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pr.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pr.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Chemical Entities of Biological Interest { #chebi }

**Identity and status:** CHEBI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Adnan Malik.
**Original problem / contribution (project reading):** Project reading of documented scope: Identifies chemical entities.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Identifies chemical entities.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Chemical identity alone does not define concentration matrix or exposure.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/chebi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/chebi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `chebi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Neuro Behavior Ontology { #nbo }

**Identity and status:** NBO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes behavioral processes and phenotypes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes behavioral processes and phenotypes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Behavioral vocabulary does not supply a universal ecological behavior protocol.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/nbo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/nbo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `nbo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ontology of Microbial Phenotypes { #omp }

**Identity and status:** OMP; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: James C. Hu.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes microbial phenotypes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes microbial phenotypes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Phenotypes depend on strain and experimental conditions.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/omp.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/omp.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `omp.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### MicrO: Prokaryotic Phenotypic and Metabolic Characters { #micro }

**Identity and status:** MICRO; `formal_ontology`; inactive_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Carrine Blank.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes prokaryotic phenotypic and metabolic characters.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes prokaryotic phenotypic and metabolic characters.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Registry reports inactive; evaluate version and reuse before adoption.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 2.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/micro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/micro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `micro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ontology of Host-Microbiome Interactions { #ohmi }

**Identity and status:** OHMI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Yongqun Oliver He.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects hosts microbiomes and their interactions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects hosts microbiomes and their interactions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Host-microbiome scope does not solve all soil or marine sampling semantics.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ohmi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ohmi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ohmi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Agronomy Ontology { #agro }

**Identity and status:** AGRO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Marie-Angélique Laporte.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes agronomic experiments and management.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes agronomic experiments and management.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Agronomic terms do not by themselves define food-security outcomes.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, envo, foodon, go, iao, ncbitaxon, obi, pato, peco, po, ro, to, uo, xco. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/agro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/agro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `agro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Plant Experimental Conditions Ontology { #peco }

**Identity and status:** PECO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Names plant experimental conditions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names plant experimental conditions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A condition label does not encode complete experimental exposure or support.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/peco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/peco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `peco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Food Ontology { #foodon }

**Identity and status:** FOODON; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Damion Dooley.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes food products sources and processing.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes food products sources and processing.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Food descriptions are not a validated food-security model.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, chebi, envo, eo, ncbitaxon, obi, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/foodon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/foodon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `foodon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Units of Measurement Ontology { #uo }

**Identity and status:** UO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Identifies measurement units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Identifies measurement units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Same or convertible units do not establish variable equivalence.
**Access / format:** Registry-linked release files; not fetched; OWL/OBO products listed in registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/uo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/uo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `uo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### DOLCE / DUL { #dolce }

**Identity and status:** DOLCE; `upper_ontology`; documented.
**Milestone / era:** 2002 DOLCE publication; DUL is a later lightweight variant; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Descriptive foundational categories and a lightweight DUL vocabulary.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Descriptive foundational categories and a lightweight DUL vocabulary.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Do not equate DOLCE and DUL versions or their commitments with BFO.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.loa.istc.cnr.it/dolce/).
**Canonical resource link:** [resource](https://www.ontologydesignpatterns.org/ont/dul/DUL.owl).
**Verification:** reference_only; last verified not established. Assessment `dolce.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Simple Knowledge Organization System { #skos }

**Identity and status:** SKOS; `semantic_framework`; documented.
**Milestone / era:** 2009 W3C Recommendation; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents concept schemes labels and broader narrower mappings.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents concept schemes labels and broader narrower mappings.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** SKOS broader is not automatically OWL subclass.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/skos-reference/).
**Canonical resource link:** [resource](http://www.w3.org/2004/02/skos/core#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `skos.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Taxonomic Concept Schema { #tcs }

**Identity and status:** TCS; `exchange_standard`; documented.
**Milestone / era:** 2005 TCS standard; subsequent TCS2 revision work; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Separates taxon names from taxon concepts in exchange.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Separates taxon names from taxon concepts in exchange.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A taxon name alone cannot resolve concept circumscription.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.tdwg.org/community/tnc/tcs2/).
**Canonical resource link:** [resource](http://www.tdwg.org/standards/117).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `tcs.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Darwin Core { #dwc }

**Identity and status:** DWC; `exchange_standard`; documented.
**Milestone / era:** 2009 TDWG ratification; work predates ratification; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides community terms for biodiversity data exchange.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides community terms for biodiversity data exchange.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A populated field does not prove biological equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://dwc.tdwg.org/).
**Canonical resource link:** [resource](http://rs.tdwg.org/dwc/terms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dwc.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Darwin Core Conceptual Model { #dwc_cm }

**Identity and status:** DWC_CM; `conceptual_model`; documented.
**Milestone / era:** Current conceptual-model documentation; earliest origin not established; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Explains relationships among Darwin Core classes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Explains relationships among Darwin Core classes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Conceptual relationships are not all formal ontology predicates.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://dwc.tdwg.org/cm/).
**Canonical resource link:** [resource](https://dwc.tdwg.org/cm/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dwc_cm.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Darwin-SW { #darwin_sw }

**Identity and status:** DARWIN_SW; `application_ontology`; documented.
**Milestone / era:** TDWG RDF work; exact first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Models relationships complementing Darwin Core in RDF.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Models relationships complementing Darwin Core in RDF.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Complementary model does not automatically align all Darwin Core usage.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/tdwg/rdf/blob/master/BiodiversityOntologies.md).
**Canonical resource link:** [resource](https://github.com/darwin-sw/dsw).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `darwin_sw.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### WoRMS / Aphia taxonomic resources { #worms }

**Identity and status:** WORMS; `controlled_vocabulary`; documented.
**Milestone / era:** Aphia/WoRMS database development; exact first release not established; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides authoritative marine names and stable Aphia identifiers.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides authoritative marine names and stable Aphia identifiers.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Taxonomic authority and ontology-network semantics are distinct resources.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.marinespecies.org/about.php).
**Canonical resource link:** [resource](https://www.marinespecies.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `worms.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Humboldt Extension { #humboldt }

**Identity and status:** HUMBOLDT; `exchange_standard`; documented.
**Milestone / era:** 2017 Humboldt Core paper; later TDWG vocabulary; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Adds ecological inventory scope and effort metadata.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Adds ecological inventory scope and effort metadata.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Inventory effort does not prove absence or complete detection.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://rs.tdwg.org/eco.htm).
**Canonical resource link:** [resource](http://rs.tdwg.org/eco/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `humboldt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Extensible Observation Ontology { #oboe }

**Identity and status:** OBOE; `formal_ontology`; documented.
**Milestone / era:** 2007 ecological observation paper; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Relates observations measurements entities characteristics standards and protocols.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Relates observations measurements entities characteristics standards and protocols.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Observation structure does not independently justify scale transformations.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NCEAS/oboe).
**Canonical resource link:** [resource](http://ecoinformatics.org/oboe/oboe.1.2/oboe.owl).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `oboe.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Sensor Observation Sample and Actuator { #sosa }

**Identity and status:** SOSA; `formal_ontology`; documented.
**Milestone / era:** 2017 W3C/OGC Recommendation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Lightweight core for observations sampling and sensing.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Lightweight core for observations sampling and sensing.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Observation identity does not determine scientific comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-ssn/).
**Canonical resource link:** [resource](http://www.w3.org/ns/sosa/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `sosa.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Semantic Sensor Network Ontology { #ssn }

**Identity and status:** SSN; `formal_ontology`; documented.
**Milestone / era:** 2017 Recommendation; earlier SSN work exists; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Extends sensor and observation modeling around SOSA.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Extends sensor and observation modeling around SOSA.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Sensor modeling does not establish biological meanings or mappings.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** sosa. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-ssn/).
**Canonical resource link:** [resource](http://www.w3.org/ns/ssn/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ssn.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### I-ADOPT Interoperability Framework { #iadopt }

**Identity and status:** I-ADOPT; `semantic_framework`; documented.
**Milestone / era:** 2021 framework and recommendations; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Decomposes variables into property object of interest matrix context and constraints.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Decomposes variables into property object of interest matrix context and constraints.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not supply every domain concept or replace units methods or observational ontologies.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.rd-alliance.org/wp-content/uploads/2024/12/I_ADOPT_recommendations.pdf).
**Canonical resource link:** [resource](https://w3id.org/iadopt/ont/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `iadopt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ecological Trait-data Standard { #ets }

**Identity and status:** ETS; `exchange_standard`; documented.
**Milestone / era:** 2018 rationale; 2019 v0.10 citation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes trait data with persistent vocabulary fields.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes trait data with persistent vocabulary fields.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A trait-data standard does not guarantee method or support comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/EcologicalTraitData/ETS).
**Canonical resource link:** [resource](https://ecologicaltraitdata.github.io/ETS/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ets.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Minimum Information about any Sequence { #mixs }

**Identity and status:** MIXS; `metadata_standard`; documented.
**Milestone / era:** 2011 MIxS publication; predecessor checklists are earlier; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes sequence sample context through checklists and extensions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes sequence sample context through checklists and extensions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Metadata compliance is not sequence or taxon equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://genomicsstandardsconsortium.github.io/mixs/).
**Canonical resource link:** [resource](https://w3id.org/mixs).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `mixs.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Microbiome Ontology Core { #microbiome_core }

**Identity and status:** MICROBIOME_CORE; `formal_ontology`; documented.
**Milestone / era:** Repository history includes 2018; release identity needs verification; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Top-level microbiome ontology effort.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Top-level microbiome ontology effort.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Repository is not the Microbial Conditions Ontology MCO; current release and rights need review.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/OHMI-ontology).
**Canonical resource link:** [resource](https://github.com/OHMI-ontology/MicrobiomeOntologyCore).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `microbiome_core.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### GloBI + RO { #globi }

**Identity and status:** GLOBI; `resource_network`; documented.
**Milestone / era:** Project origin and version history require resource-specific review; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Links biotic-interaction records using community relations and source citations.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Links biotic-interaction records using community relations and source citations.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A source interaction assertion does not prove every taxon or interaction mapping.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** ro. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.globalbioticinteractions.org/).
**Canonical resource link:** [resource](https://www.globalbioticinteractions.org/).
**Verification:** reference_only; last verified not established. Assessment `globi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Soil Food Web Ontology { #sfwo }

**Identity and status:** SFWO; `application_ontology`; documented.
**Milestone / era:** 2023 ontology paper; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes trophic groups resources processes and dietary traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes trophic groups resources processes and dietary traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Soil trophic categories do not establish universal feeding or support rules.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://soilfoodwebontology.github.io/).
**Canonical resource link:** [resource](http://purl.org/sfwo.owl).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `sfwo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### AGROVOC { #agrovoc }

**Identity and status:** AGROVOC; `thesaurus`; documented.
**Milestone / era:** 1980s thesaurus roots; precise origin not reverified; pre1990.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Multilingual agricultural concepts and relations for discovery.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Multilingual agricultural concepts and relations for discovery.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Thesaurus links do not establish measurement equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.fao.org/agrovoc/).
**Canonical resource link:** [resource](http://aims.fao.org/aos/agrovoc/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `agrovoc.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Crop Ontology { #crop }

**Identity and status:** CROP; `controlled_vocabulary`; documented.
**Milestone / era:** Exact first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects crop traits measurement methods and scales.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects crop traits measurement methods and scales.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Crop-specific variables need identifiers and protocol-specific interpretation.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.cropontology.org/).
**Canonical resource link:** [resource](https://www.cropontology.org/).
**Verification:** reference_only; last verified not established. Assessment `crop.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Minimum Information About Plant Phenotyping Experiments { #miappe }

**Identity and status:** MIAPPE; `metadata_standard`; documented.
**Milestone / era:** Community standard; exact first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Specifies experimental phenotyping metadata through checklist and data model.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Specifies experimental phenotyping metadata through checklist and data model.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Checklist completeness is not trait or experimental equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.miappe.org/).
**Canonical resource link:** [resource](https://www.miappe.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `miappe.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Plant Phenotyping Experiment Ontology { #ppeo }

**Identity and status:** PPEO; `application_ontology`; documented.
**Milestone / era:** Implementation of MIAPPE; precise origin not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents MIAPPE experimental metadata structure.
**Relationship to prior work:** OWL representation of the MIAPPE checklist/data-model structure; not interchangeable with the checklist itself.
**Historical role:** Project assessment: Represents MIAPPE experimental metadata structure.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Experimental metadata structure does not supply all domain trait semantics.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/MIAPPE/MIAPPE-ontology).
**Canonical resource link:** [resource](https://github.com/MIAPPE/MIAPPE-ontology).
**Verification:** reference_only; last verified not established. Assessment `ppeo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Plant Stress Ontology { #pso }

**Identity and status:** PSO; `formal_ontology`; documented.
**Milestone / era:** Planteome development; first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes biotic and abiotic plant stresses.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes biotic and abiotic plant stresses.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Stress categories do not define complete exposure dose or response variables.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/Planteome/plant-stress-ontology).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pso.owl).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `pso.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Animal Trait Ontology for Livestock { #atol }

**Identity and status:** ATOL; `formal_ontology`; unresolved.
**Milestone / era:** Primary version and identifier pattern need verification; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes livestock traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes livestock traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Livestock trait names do not replace measurement-method evidence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.atol-ontology.com/).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** unresolved; last verified not established. Assessment `atol.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Environment Ontology for Livestock { #eol }

**Identity and status:** EOL; `formal_ontology`; unresolved.
**Milestone / era:** Identity retained as a review lead; official release not verified; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes livestock farm environmental conditions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes livestock farm environmental conditions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Do not confuse with Encyclopedia of Life; source terms and release need verification.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.atol-ontology.com/).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** unresolved; last verified not established. Assessment `eol.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Livestock Product Trait Ontology { #lpt }

**Identity and status:** LPT; `controlled_vocabulary`; unresolved.
**Milestone / era:** Primary ontology release and rights need verification; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes traits of livestock products.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes traits of livestock products.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Product traits are not animal traits or a food-security outcome.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.animalgenome.org/).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** unresolved; last verified not established. Assessment `lpt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Semantic Web for Earth and Environmental Terminology { #sweet }

**Identity and status:** SWEET; `resource_network`; documented.
**Milestone / era:** NASA Earth-science semantic work; precise origin not established; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides linked Earth-system terminology modules.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides linked Earth-system terminology modules.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Broad Earth-system terminology does not establish biological or support equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NASA-SWEET/sweet).
**Canonical resource link:** [resource](http://sweetontology.net/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `sweet.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ecosystems Ontology { #ecso }

**Identity and status:** ECSO; `formal_ontology`; documented.
**Milestone / era:** DataONE semantic provenance effort; first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes ecosystem observation concepts in DataONE work.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes ecosystem observation concepts in DataONE work.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Evaluate exact term scope and release; not every ecosystem quantity is covered.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/DataONEorg/sem-prov-ontologies).
**Canonical resource link:** [resource](https://github.com/DataONEorg/sem-prov-ontologies).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ecso.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### CF Standard Names { #cf }

**Identity and status:** CF; `controlled_vocabulary`; documented.
**Milestone / era:** CF conventions development; specific table versions are separately versioned; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides named physical quantities with canonical units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides named physical quantities with canonical units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Same canonical unit does not establish the same standard name or cell method.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://cfconventions.org/faq.html).
**Canonical resource link:** [resource](https://cfconventions.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `cf.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### GCMD Keywords { #gcmd }

**Identity and status:** GCMD; `controlled_vocabulary`; documented.
**Milestone / era:** GCMD catalog lineage; exact first keyword release not established; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Supports Earth-science discovery using managed keyword hierarchies.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Supports Earth-science discovery using managed keyword hierarchies.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Discovery keywords are not formal measurement definitions.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.earthdata.nasa.gov/sites/default/files/imported/KeywordsCommunityGuide_Baseline_v1_SIGNED_FINAL.pdf).
**Canonical resource link:** [resource](https://gcmd.earthdata.nasa.gov/kms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `gcmd.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### General Multilingual Environmental Thesaurus { #gemet }

**Identity and status:** GEMET; `thesaurus`; documented.
**Milestone / era:** Development since 1995 documented by EEA; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects multilingual environmental indexing concepts.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects multilingual environmental indexing concepts.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Broader and related thesaurus links are not biological equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.eionet.europa.eu/gemet/en/about/).
**Canonical resource link:** [resource](https://www.eionet.europa.eu/gemet/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `gemet.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### IUCN Habitats Classification Scheme { #iucn_habitat }

**Identity and status:** IUCN_HABITAT; `classification`; documented.
**Milestone / era:** Version 3.1 documentation; origin not established; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Names habitat classes for Red List assessments.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names habitat classes for Red List assessments.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Categories do not supply quantitative habitat support or sensor equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://nrl.iucnredlist.org/resources/habitat-classification-scheme).
**Canonical resource link:** [resource](https://nrl.iucnredlist.org/resources/habitat-classification-scheme).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `iucn_habitat.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### IUCN Threats Classification Scheme { #iucn_threat }

**Identity and status:** IUCN_THREAT; `classification`; documented.
**Milestone / era:** Version 3.3 documentation; origin not established; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Classifies direct threats in species assessments.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Classifies direct threats in species assessments.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Threat categories are distinct from measured pressures and causal attribution.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://nrl.iucnredlist.org/resources/threat-classification-scheme).
**Canonical resource link:** [resource](https://nrl.iucnredlist.org/resources/threat-classification-scheme).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `iucn_threat.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### IUCN Red List Categories and Criteria { #iucn_redlist }

**Identity and status:** IUCN_REDLIST; `classification`; documented.
**Milestone / era:** Modern criteria development; exact milestone requires review; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Organizes extinction-risk assessment categories and criteria.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Organizes extinction-risk assessment categories and criteria.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A risk category is not a raw population observation or taxonomic ontology.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.iucnredlist.org/resources/categories-and-criteria).
**Canonical resource link:** [resource](https://www.iucnredlist.org/resources/categories-and-criteria).
**Verification:** reference_only; last verified not established. Assessment `iucn_redlist.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Essential Biodiversity Variables { #ebv }

**Identity and status:** EBV; `conceptual_model`; documented.
**Milestone / era:** 2013 EBV paper; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Organizes biodiversity state variables across organization space and time.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Organizes biodiversity state variables across organization space and time.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A monitoring framework is not a complete formal ontology or aggregation justification.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://geobon.org/ebvs/what-are-ebvs/).
**Canonical resource link:** [resource](https://geobon.org/ebvs/what-are-ebvs/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ebv.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### EBV application-ontology / Bari Manifesto work { #bari }

**Identity and status:** BARI; `semantic_framework`; documented.
**Milestone / era:** 2018 Bari Manifesto; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Proposes interoperability architecture for EBV production.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Proposes interoperability architecture for EBV production.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A recommendation to develop an ontology is not proof of a deployed complete ontology.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.vliz.be/imisdocs/publications/322519.pdf).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `bari.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### BON in a Box semantic work { #bon_box }

**Identity and status:** BON_BOX; `semantic_framework`; documented.
**Milestone / era:** 2015 initiative brochure; semantic-artifact origin unresolved; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects biodiversity monitoring workflow resources.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects biodiversity monitoring workflow resources.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Specific semantic artifacts and versions require continued review.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://geobon.org/documents/biodiversity-monitoring/).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** reference_only; last verified not established. Assessment `bon_box.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### MarineTLO { #marine_tlo }

**Identity and status:** MARINE_TLO; `upper_ontology`; documented.
**Milestone / era:** 2013 marine integration work; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Integrates marine facts with categorical and spatiotemporal context.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Integrates marine facts with categorical and spatiotemporal context.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Marine integration abstractions do not independently justify sampling equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://projects.ics.forth.gr/isl/MarineTLO/).
**Canonical resource link:** [resource](http://www.ics.forth.gr/isl/ontology/MarineTLO/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `marine_tlo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Marine Regions semantic resources { #marine_regions }

**Identity and status:** MARINE_REGIONS; `controlled_vocabulary`; documented.
**Milestone / era:** Gazetteer and vocabulary versions require separate review; unknown.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides marine geographic identifiers and spatial reference resources.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides marine geographic identifiers and spatial reference resources.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Region identity does not define biological organization or pixel support.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.marineregions.org/).
**Canonical resource link:** [resource](https://www.marineregions.org/).
**Verification:** reference_only; last verified not established. Assessment `marine_regions.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### APHIA ontology network { #aphia_network }

**Identity and status:** APHIA_NETWORK; `resource_network`; documented.
**Milestone / era:** Network documentation inspected; exact first release not established; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides linked vocabularies across Aphia information modules.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides linked vocabularies across Aphia information modules.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Network artifacts are distinct from WoRMS taxonomic records.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://aphia.org/ns/).
**Canonical resource link:** [resource](https://aphia.org/ns/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `aphia_network.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### GeoSPARQL { #geosparql }

**Identity and status:** GEOSPARQL; `formal_ontology`; documented.
**Milestone / era:** 2012 initial standard; subsequent revisions exist; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents geospatial features geometry and spatial relations.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents geospatial features geometry and spatial relations.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Geometry and overlap do not define biological organization or comparable support.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.ogc.org/standard/geosparql/).
**Canonical resource link:** [resource](http://www.opengis.net/ont/geosparql#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `geosparql.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### OWL-Time { #owl_time }

**Identity and status:** OWL-Time; `formal_ontology`; documented.
**Milestone / era:** 2017 Recommendation; earlier work and later drafts overlap; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents temporal instants intervals and relations.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents temporal instants intervals and relations.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Time relations do not alone establish observation support or temporal comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/owl-time/).
**Canonical resource link:** [resource](http://www.w3.org/2006/time#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `owl_time.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Quantities Units Dimensions and Types { #qudt }

**Identity and status:** QUDT; `formal_ontology`; documented.
**Milestone / era:** NASA NExIOM lineage; exact first release not established; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents quantities quantity kinds dimensions and units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents quantities quantity kinds dimensions and units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Unit convertibility cannot establish biological or variable equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.qudt.org/).
**Canonical resource link:** [resource](http://qudt.org/schema/qudt/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `qudt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### PROV-O { #prov }

**Identity and status:** PROV-O; `formal_ontology`; documented.
**Milestone / era:** 2013 W3C Recommendation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents entities activities agents and derivations.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents entities activities agents and derivations.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A recorded derivation is not proof of scientific justification.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/prov-o/).
**Canonical resource link:** [resource](http://www.w3.org/ns/prov#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `prov.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### ProvONE { #provone }

**Identity and status:** PROVONE; `application_ontology`; documented.
**Milestone / era:** DataONE scientific workflow provenance; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Extends provenance for scientific workflow structure and execution.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Extends provenance for scientific workflow structure and execution.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Workflow provenance does not validate a scientific transformation.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/DataONEorg/sem-prov-ontologies).
**Canonical resource link:** [resource](https://github.com/DataONEorg/sem-prov-ontologies).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `provone.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Data Catalog Vocabulary { #dcat }

**Identity and status:** DCAT; `metadata_standard`; documented.
**Milestone / era:** 2014 first Recommendation; 2024 DCAT 3; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes datasets distributions and catalog services.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes datasets distributions and catalog services.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Catalog metadata does not establish observation meaning or equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-dcat-3/).
**Canonical resource link:** [resource](http://www.w3.org/ns/dcat#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dcat.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Dublin Core / DCTERMS { #dcterms }

**Identity and status:** DCTERMS; `metadata_standard`; documented.
**Milestone / era:** 1995 workshop lineage; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides general resource metadata terms.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides general resource metadata terms.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** General metadata terms do not supply domain measurement definitions.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/).
**Canonical resource link:** [resource](http://purl.org/dc/terms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dcterms.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### DataCite Metadata Schema { #datacite }

**Identity and status:** DATACITE; `metadata_standard`; documented.
**Milestone / era:** Schema revisions are versioned; origin not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes research outputs for identification citation and discovery.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes research outputs for identification citation and discovery.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Citation metadata is not scientific harmonization.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://schema.datacite.org/).
**Canonical resource link:** [resource](https://schema.datacite.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `datacite.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### SpatioTemporal Asset Catalog { #stac }

**Identity and status:** STAC; `metadata_standard`; documented.
**Milestone / era:** Community development before 1.0; precise origin not reverified; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes spatiotemporal assets with extension metadata.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes spatiotemporal assets with extension metadata.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A catalog standard is not the entire pipeline or an equivalence ontology.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/radiantearth/stac-spec).
**Canonical resource link:** [resource](https://stacspec.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `stac.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ecological Metadata Language { #eml }

**Identity and status:** EML; `metadata_standard`; documented.
**Milestone / era:** 1997 metadata work cited as precursor; EML releases followed; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Documents ecological dataset entities methods attributes and access.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Documents ecological dataset entities methods attributes and access.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Metadata completeness does not prove cross-dataset comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NCEAS/eml).
**Canonical resource link:** [resource](https://eml.ecoinformatics.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `eml.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Ecolingua { #ecolingua }

**Identity and status:** ECOLINGUA; `historical_effort`; historical.
**Milestone / era:** 2006 formal ontology paper; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Formalizes ecological data for model synthesis.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Formalizes ecological data for model synthesis.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Historical design and publication do not imply a maintained modern endpoint.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.scielo.br/j/jbcos/a/xbtCVcgqzPx8bKGb5WBDzNg/?lang=en).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ecolingua.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### SEEK semantic mediation { #seek }

**Identity and status:** SEEK; `historical_effort`; historical.
**Milestone / era:** 2003 project notes and associated OBOE lineage; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Explored semantic annotation and mediation of ecological datasets.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Explored semantic annotation and mediation of ecological datasets.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A historical program is not a current ontology service.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://cseweb.ucsd.edu/groups/tatami/seek/).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `seek.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### OBOE ecology extensions { #oboe_ecology }

**Identity and status:** OBOE_ECOLOGY; `resource_network`; documented.
**Milestone / era:** OBOE 2007 lineage; individual extensions vary; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Extends an observation model with ecological terms.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Extends an observation model with ecological terms.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Extension scope and versions must be inspected individually.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NCEAS/oboe).
**Canonical resource link:** [resource](https://github.com/NCEAS/oboe).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `oboe_ecology.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### Historical biodiversity ontology efforts { #biodiversity_history }

**Identity and status:** BIODIVERSITY_HISTORY; `historical_effort`; unresolved.
**Milestone / era:** TDWG name concept and RDF efforts overlap across decades; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Preserves prior TDWG semantic-model experiments for comparison.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Preserves prior TDWG semantic-model experiments for comparison.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** An umbrella review lead has no single canonical ontology identity.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/tdwg/rdf/blob/master/BiodiversityOntologies.md).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** unresolved; last verified not established. Assessment `biodiversity_history.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

### AnaEE semantic resources { #anaee }

**Identity and status:** ANAEE; `resource_network`; unresolved.
**Milestone / era:** 2020 technical report; individual semantic resources need identification; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Identifies an ecosystem-experiment semantic infrastructure review area.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Identifies an ecosystem-experiment semantic infrastructure review area.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Specific artifacts versions licenses and coverage remain to be verified.
**Access / format:** Documentation/resource link only; no live resolver integration; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.anaee.eu/sites/default/files/Mediatheque/Resources/reportsdocuments/std_-_v_7.1_-_appendix_8_-_16.10.2020.pdf).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** unresolved; last verified not established. Assessment `anaee.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.
