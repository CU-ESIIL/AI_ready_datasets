# Ontology and semantic-resource landscape

A growing landscape inventory of **86 resources**, not an exhaustive list or an adoption decision. Formal and application ontologies, standards, classifications, thesauri, frameworks and historical efforts serve different purposes.

The canonical CSV lives in `data/semantics/semantic_resources.csv`. This page and the [coverage matrix](comparison.md) are generated with `python scripts/generate_semantics.py`. [Download every inventory field](semantic_resources.csv), [auditable project assessments](assessments.jsonl) or [inspected registry fact evidence](verification_sources.json).

Resource identities, registry status and cited documentation are **resource facts** with a verification scope. Coverage, candidate roles, eras, limitations and influence are **provisional project assessments** by the coding assistant, not expert-reviewed ontology properties. Unknown release dates/rights stay unknown. A milestone below is not necessarily the first release; eras overlap.

!!! note "Do not collapse distinctions"
    [Organism, taxon, population and community](distinctions.md) describe different things. An ontology, vocabulary and exchange standard are also different kinds of resource. [Scale is not one dimension](scale-support.md).

## Master inventory

Browse the complete table without JavaScript, or filter it by a project assessment below. Biological-level filtering uses the inventory coverage dimensions, not a new hierarchy. Filters do not change the canonical inventory or approve resource selection.

<div id="semantic-filters" hidden></div>
<p id="semantic-count" role="status" aria-live="polite"></p>

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

<div id="semantic-filter-data" hidden data-resources="[{&quot;id&quot;: &quot;bfo&quot;, &quot;name&quot;: &quot;Basic Formal Ontology&quot;, &quot;acronym&quot;: &quot;BFO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;foundations&quot;, &quot;kind&quot;: &quot;upper_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;population&quot;, &quot;community&quot;, &quot;observation&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;population&quot;, &quot;community&quot;]}, {&quot;id&quot;: &quot;iao&quot;, &quot;name&quot;: &quot;Information Artifact Ontology&quot;, &quot;acronym&quot;: &quot;IAO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;foundations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;method&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;ro&quot;, &quot;name&quot;: &quot;Relation Ontology&quot;, &quot;acronym&quot;: &quot;RO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;foundations&quot;, &quot;kind&quot;: &quot;relation_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;population&quot;, &quot;community&quot;, &quot;interaction&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;population&quot;, &quot;community&quot;]}, {&quot;id&quot;: &quot;ncbitaxon&quot;, &quot;name&quot;: &quot;NCBI organismal classification&quot;, &quot;acronym&quot;: &quot;NCBITaxon&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;taxonomy&quot;, &quot;kind&quot;: &quot;classification&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;taxrank&quot;, &quot;name&quot;: &quot;Taxonomic Rank Vocabulary&quot;, &quot;acronym&quot;: &quot;TAXRANK&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;taxonomy&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;], &quot;level&quot;: [&quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;pco&quot;, &quot;name&quot;: &quot;Population and Community Ontology&quot;, &quot;acronym&quot;: &quot;PCO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;biology&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;population&quot;, &quot;community&quot;, &quot;interaction&quot;, &quot;ecosystem&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;population&quot;, &quot;community&quot;, &quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;envo&quot;, &quot;name&quot;: &quot;Environment Ontology&quot;, &quot;acronym&quot;: &quot;ENVO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;community&quot;, &quot;ecosystem&quot;, &quot;habitat&quot;, &quot;environment&quot;, &quot;space&quot;], &quot;level&quot;: [&quot;community&quot;, &quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;bco&quot;, &quot;name&quot;: &quot;Biological Collections Ontology&quot;, &quot;acronym&quot;: &quot;BCO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;obi&quot;, &quot;name&quot;: &quot;Ontology for Biomedical Investigations&quot;, &quot;acronym&quot;: &quot;OBI&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;units&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;oba&quot;, &quot;name&quot;: &quot;Ontology of Biological Attributes&quot;, &quot;acronym&quot;: &quot;OBA&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;pato&quot;, &quot;name&quot;: &quot;Phenotype And Trait Ontology&quot;, &quot;acronym&quot;: &quot;PATO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;to&quot;, &quot;name&quot;: &quot;Plant Trait Ontology&quot;, &quot;acronym&quot;: &quot;TO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;po&quot;, &quot;name&quot;: &quot;Plant Ontology&quot;, &quot;acronym&quot;: &quot;PO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;anatomy&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;, &quot;organism&quot;], &quot;level&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;flopo&quot;, &quot;name&quot;: &quot;Flora Phenotype Ontology&quot;, &quot;acronym&quot;: &quot;FLOPO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;application_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;organism&quot;, &quot;taxonomy&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;vt&quot;, &quot;name&quot;: &quot;Vertebrate Trait Ontology&quot;, &quot;acronym&quot;: &quot;VT&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;cmo&quot;, &quot;name&quot;: &quot;Clinical Measurement Ontology&quot;, &quot;acronym&quot;: &quot;CMO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;observation&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;uberon&quot;, &quot;name&quot;: &quot;Uberon multispecies anatomy ontology&quot;, &quot;acronym&quot;: &quot;UBERON&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;anatomy&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;, &quot;organism&quot;], &quot;level&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;cl&quot;, &quot;name&quot;: &quot;Cell Ontology&quot;, &quot;acronym&quot;: &quot;CL&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;anatomy&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;], &quot;level&quot;: [&quot;cellular&quot;, &quot;anatomy&quot;]}, {&quot;id&quot;: &quot;caro&quot;, &quot;name&quot;: &quot;Common Anatomy Reference Ontology&quot;, &quot;acronym&quot;: &quot;CARO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;anatomy&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;inactive_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;organism&quot;], &quot;level&quot;: [&quot;anatomy&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;bspo&quot;, &quot;name&quot;: &quot;Biological Spatial Ontology&quot;, &quot;acronym&quot;: &quot;BSPO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;anatomy&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;anatomy&quot;, &quot;space&quot;], &quot;level&quot;: [&quot;anatomy&quot;]}, {&quot;id&quot;: &quot;go&quot;, &quot;name&quot;: &quot;Gene Ontology&quot;, &quot;acronym&quot;: &quot;GO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;molecular&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;molecular&quot;, &quot;cellular&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;molecular&quot;, &quot;cellular&quot;]}, {&quot;id&quot;: &quot;so&quot;, &quot;name&quot;: &quot;Sequence Ontology&quot;, &quot;acronym&quot;: &quot;SO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;molecular&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;molecular&quot;], &quot;level&quot;: [&quot;molecular&quot;]}, {&quot;id&quot;: &quot;pr&quot;, &quot;name&quot;: &quot;Protein Ontology&quot;, &quot;acronym&quot;: &quot;PRO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;molecular&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;molecular&quot;], &quot;level&quot;: [&quot;molecular&quot;]}, {&quot;id&quot;: &quot;chebi&quot;, &quot;name&quot;: &quot;Chemical Entities of Biological Interest&quot;, &quot;acronym&quot;: &quot;CHEBI&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;molecular&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;molecular&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;molecular&quot;]}, {&quot;id&quot;: &quot;nbo&quot;, &quot;name&quot;: &quot;Neuro Behavior Ontology&quot;, &quot;acronym&quot;: &quot;NBO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;behavior&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;behavior&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;omp&quot;, &quot;name&quot;: &quot;Ontology of Microbial Phenotypes&quot;, &quot;acronym&quot;: &quot;OMP&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;microbiome&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;micro&quot;, &quot;name&quot;: &quot;MicrO: Prokaryotic Phenotypic and Metabolic Characters&quot;, &quot;acronym&quot;: &quot;MICRO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;microbiome&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;inactive_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;ohmi&quot;, &quot;name&quot;: &quot;Ontology of Host-Microbiome Interactions&quot;, &quot;acronym&quot;: &quot;OHMI&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;microbiome&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;community&quot;, &quot;interaction&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;community&quot;]}, {&quot;id&quot;: &quot;agro&quot;, &quot;name&quot;: &quot;Agronomy Ontology&quot;, &quot;acronym&quot;: &quot;AGRO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;observation&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;peco&quot;, &quot;name&quot;: &quot;Plant Experimental Conditions Ontology&quot;, &quot;acronym&quot;: &quot;PECO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;foodon&quot;, &quot;name&quot;: &quot;Food Ontology&quot;, &quot;acronym&quot;: &quot;FOODON&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;molecular&quot;, &quot;organism&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;molecular&quot;, &quot;organism&quot;]}, {&quot;id&quot;: &quot;uo&quot;, &quot;name&quot;: &quot;Units of Measurement Ontology&quot;, &quot;acronym&quot;: &quot;UO&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;quantities&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;active_registry&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;units&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;dolce&quot;, &quot;name&quot;: &quot;DOLCE / DUL&quot;, &quot;acronym&quot;: &quot;DOLCE&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;foundations&quot;, &quot;kind&quot;: &quot;upper_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;skos&quot;, &quot;name&quot;: &quot;Simple Knowledge Organization System&quot;, &quot;acronym&quot;: &quot;SKOS&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;foundations&quot;, &quot;kind&quot;: &quot;semantic_framework&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;], &quot;level&quot;: [&quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;tcs&quot;, &quot;name&quot;: &quot;Taxonomic Concept Schema&quot;, &quot;acronym&quot;: &quot;TCS&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;taxonomy&quot;, &quot;kind&quot;: &quot;exchange_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;dwc&quot;, &quot;name&quot;: &quot;Darwin Core&quot;, &quot;acronym&quot;: &quot;DWC&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;biodiversity&quot;, &quot;kind&quot;: &quot;exchange_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;dwc_cm&quot;, &quot;name&quot;: &quot;Darwin Core Conceptual Model&quot;, &quot;acronym&quot;: &quot;DWC_CM&quot;, &quot;era&quot;: &quot;2020s&quot;, &quot;domain&quot;: &quot;biodiversity&quot;, &quot;kind&quot;: &quot;conceptual_model&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;observation&quot;, &quot;sampling&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;darwin_sw&quot;, &quot;name&quot;: &quot;Darwin-SW&quot;, &quot;acronym&quot;: &quot;DARWIN_SW&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;biodiversity&quot;, &quot;kind&quot;: &quot;application_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;, &quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;worms&quot;, &quot;name&quot;: &quot;WoRMS / Aphia taxonomic resources&quot;, &quot;acronym&quot;: &quot;WORMS&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;marine&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;humboldt&quot;, &quot;name&quot;: &quot;Humboldt Extension&quot;, &quot;acronym&quot;: &quot;HUMBOLDT&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;biodiversity&quot;, &quot;kind&quot;: &quot;exchange_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;population&quot;, &quot;community&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;scale_support&quot;], &quot;level&quot;: [&quot;population&quot;, &quot;community&quot;]}, {&quot;id&quot;: &quot;oboe&quot;, &quot;name&quot;: &quot;Extensible Observation Ontology&quot;, &quot;acronym&quot;: &quot;OBOE&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;, &quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;units&quot;, &quot;scale_support&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;sosa&quot;, &quot;name&quot;: &quot;Sensor Observation Sample and Actuator&quot;, &quot;acronym&quot;: &quot;SOSA&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;ssn&quot;, &quot;name&quot;: &quot;Semantic Sensor Network Ontology&quot;, &quot;acronym&quot;: &quot;SSN&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;scale_support&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;iadopt&quot;, &quot;name&quot;: &quot;I-ADOPT Interoperability Framework&quot;, &quot;acronym&quot;: &quot;I-ADOPT&quot;, &quot;era&quot;: &quot;2020s&quot;, &quot;domain&quot;: &quot;observations&quot;, &quot;kind&quot;: &quot;semantic_framework&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;observation&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;ets&quot;, &quot;name&quot;: &quot;Ecological Trait-data Standard&quot;, &quot;acronym&quot;: &quot;ETS&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;traits&quot;, &quot;kind&quot;: &quot;exchange_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;observation&quot;, &quot;method&quot;, &quot;units&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;mixs&quot;, &quot;name&quot;: &quot;Minimum Information about any Sequence&quot;, &quot;acronym&quot;: &quot;MIXS&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;molecular&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;molecular&quot;, &quot;environment&quot;, &quot;sampling&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;molecular&quot;]}, {&quot;id&quot;: &quot;microbiome_core&quot;, &quot;name&quot;: &quot;Microbiome Ontology Core&quot;, &quot;acronym&quot;: &quot;MICROBIOME_CORE&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;microbiome&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;community&quot;, &quot;interaction&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;community&quot;]}, {&quot;id&quot;: &quot;globi&quot;, &quot;name&quot;: &quot;GloBI + RO&quot;, &quot;acronym&quot;: &quot;GLOBI&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;interactions&quot;, &quot;kind&quot;: &quot;resource_network&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;interaction&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;sfwo&quot;, &quot;name&quot;: &quot;Soil Food Web Ontology&quot;, &quot;acronym&quot;: &quot;SFWO&quot;, &quot;era&quot;: &quot;2020s&quot;, &quot;domain&quot;: &quot;interactions&quot;, &quot;kind&quot;: &quot;application_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;community&quot;, &quot;interaction&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;community&quot;]}, {&quot;id&quot;: &quot;agrovoc&quot;, &quot;name&quot;: &quot;AGROVOC&quot;, &quot;acronym&quot;: &quot;AGROVOC&quot;, &quot;era&quot;: &quot;pre1990&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;thesaurus&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;environment&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;crop&quot;, &quot;name&quot;: &quot;Crop Ontology&quot;, &quot;acronym&quot;: &quot;CROP&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;, &quot;observation&quot;, &quot;method&quot;, &quot;units&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;miappe&quot;, &quot;name&quot;: &quot;Minimum Information About Plant Phenotyping Experiments&quot;, &quot;acronym&quot;: &quot;MIAPPE&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;scale_support&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;ppeo&quot;, &quot;name&quot;: &quot;Plant Phenotyping Experiment Ontology&quot;, &quot;acronym&quot;: &quot;PPEO&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;application_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;pso&quot;, &quot;name&quot;: &quot;Plant Stress Ontology&quot;, &quot;acronym&quot;: &quot;PSO&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;environment&quot;, &quot;method&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;atol&quot;, &quot;name&quot;: &quot;Animal Trait Ontology for Livestock&quot;, &quot;acronym&quot;: &quot;ATOL&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;unresolved&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;eol&quot;, &quot;name&quot;: &quot;Environment Ontology for Livestock&quot;, &quot;acronym&quot;: &quot;EOL&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;unresolved&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;environment&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;lpt&quot;, &quot;name&quot;: &quot;Livestock Product Trait Ontology&quot;, &quot;acronym&quot;: &quot;LPT&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;agriculture&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;unresolved&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;trait&quot;], &quot;level&quot;: [&quot;organism&quot;]}, {&quot;id&quot;: &quot;sweet&quot;, &quot;name&quot;: &quot;Semantic Web for Earth and Environmental Terminology&quot;, &quot;acronym&quot;: &quot;SWEET&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;resource_network&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;ecosystem&quot;, &quot;environment&quot;, &quot;space&quot;, &quot;time&quot;, &quot;units&quot;], &quot;level&quot;: [&quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;ecso&quot;, &quot;name&quot;: &quot;Ecosystems Ontology&quot;, &quot;acronym&quot;: &quot;ECSO&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;ecosystem&quot;, &quot;environment&quot;, &quot;observation&quot;, &quot;units&quot;], &quot;level&quot;: [&quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;cf&quot;, &quot;name&quot;: &quot;CF Standard Names&quot;, &quot;acronym&quot;: &quot;CF&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;environment&quot;, &quot;observation&quot;, &quot;method&quot;, &quot;units&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;gcmd&quot;, &quot;name&quot;: &quot;GCMD Keywords&quot;, &quot;acronym&quot;: &quot;GCMD&quot;, &quot;era&quot;: &quot;1990s&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;environment&quot;, &quot;space&quot;, &quot;time&quot;, &quot;observation&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;gemet&quot;, &quot;name&quot;: &quot;General Multilingual Environmental Thesaurus&quot;, &quot;acronym&quot;: &quot;GEMET&quot;, &quot;era&quot;: &quot;1990s&quot;, &quot;domain&quot;: &quot;environment&quot;, &quot;kind&quot;: &quot;thesaurus&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;habitat&quot;, &quot;environment&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;iucn_habitat&quot;, &quot;name&quot;: &quot;IUCN Habitats Classification Scheme&quot;, &quot;acronym&quot;: &quot;IUCN_HABITAT&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;classification&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;, &quot;habitat&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;iucn_threat&quot;, &quot;name&quot;: &quot;IUCN Threats Classification Scheme&quot;, &quot;acronym&quot;: &quot;IUCN_THREAT&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;classification&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;, &quot;interaction&quot;, &quot;environment&quot;], &quot;level&quot;: [&quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;iucn_redlist&quot;, &quot;name&quot;: &quot;IUCN Red List Categories and Criteria&quot;, &quot;acronym&quot;: &quot;IUCN_REDLIST&quot;, &quot;era&quot;: &quot;1990s&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;classification&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;, &quot;population&quot;], &quot;level&quot;: [&quot;taxonomy&quot;, &quot;population&quot;]}, {&quot;id&quot;: &quot;ebv&quot;, &quot;name&quot;: &quot;Essential Biodiversity Variables&quot;, &quot;acronym&quot;: &quot;EBV&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;conceptual_model&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;taxonomy&quot;, &quot;trait&quot;, &quot;population&quot;, &quot;community&quot;, &quot;ecosystem&quot;, &quot;space&quot;, &quot;time&quot;, &quot;scale_support&quot;], &quot;level&quot;: [&quot;taxonomy&quot;, &quot;population&quot;, &quot;community&quot;, &quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;bari&quot;, &quot;name&quot;: &quot;EBV application-ontology / Bari Manifesto work&quot;, &quot;acronym&quot;: &quot;BARI&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;semantic_framework&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;, &quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;ecosystem&quot;, &quot;observation&quot;, &quot;scale_support&quot;, &quot;provenance&quot;], &quot;level&quot;: [&quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;bon_box&quot;, &quot;name&quot;: &quot;BON in a Box semantic work&quot;, &quot;acronym&quot;: &quot;BON_BOX&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;conservation&quot;, &quot;kind&quot;: &quot;semantic_framework&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;observation&quot;, &quot;method&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;marine_tlo&quot;, &quot;name&quot;: &quot;MarineTLO&quot;, &quot;acronym&quot;: &quot;MARINE_TLO&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;marine&quot;, &quot;kind&quot;: &quot;upper_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;environment&quot;, &quot;space&quot;, &quot;time&quot;, &quot;observation&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;marine_regions&quot;, &quot;name&quot;: &quot;Marine Regions semantic resources&quot;, &quot;acronym&quot;: &quot;MARINE_REGIONS&quot;, &quot;era&quot;: &quot;unknown&quot;, &quot;domain&quot;: &quot;marine&quot;, &quot;kind&quot;: &quot;controlled_vocabulary&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;habitat&quot;, &quot;environment&quot;, &quot;space&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;aphia_network&quot;, &quot;name&quot;: &quot;APHIA ontology network&quot;, &quot;acronym&quot;: &quot;APHIA_NETWORK&quot;, &quot;era&quot;: &quot;2020s&quot;, &quot;domain&quot;: &quot;marine&quot;, &quot;kind&quot;: &quot;resource_network&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;, &quot;interaction&quot;, &quot;space&quot;], &quot;level&quot;: [&quot;organism&quot;, &quot;taxonomy&quot;]}, {&quot;id&quot;: &quot;geosparql&quot;, &quot;name&quot;: &quot;GeoSPARQL&quot;, &quot;acronym&quot;: &quot;GEOSPARQL&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;space&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;scale_support&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;owl_time&quot;, &quot;name&quot;: &quot;OWL-Time&quot;, &quot;acronym&quot;: &quot;OWL-Time&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;time&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;time&quot;, &quot;scale_support&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;qudt&quot;, &quot;name&quot;: &quot;Quantities Units Dimensions and Types&quot;, &quot;acronym&quot;: &quot;QUDT&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;quantities&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;units&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;prov&quot;, &quot;name&quot;: &quot;PROV-O&quot;, &quot;acronym&quot;: &quot;PROV-O&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;provenance&quot;, &quot;kind&quot;: &quot;formal_ontology&quot;, &quot;role&quot;: &quot;provisional_core&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Core candidate&quot;], &quot;dimension&quot;: [&quot;observation&quot;, &quot;method&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;provone&quot;, &quot;name&quot;: &quot;ProvONE&quot;, &quot;acronym&quot;: &quot;PROVONE&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;provenance&quot;, &quot;kind&quot;: &quot;application_ontology&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;method&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;dcat&quot;, &quot;name&quot;: &quot;Data Catalog Vocabulary&quot;, &quot;acronym&quot;: &quot;DCAT&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;infrastructure&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;dcterms&quot;, &quot;name&quot;: &quot;Dublin Core / DCTERMS&quot;, &quot;acronym&quot;: &quot;DCTERMS&quot;, &quot;era&quot;: &quot;1990s&quot;, &quot;domain&quot;: &quot;infrastructure&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;datacite&quot;, &quot;name&quot;: &quot;DataCite Metadata Schema&quot;, &quot;acronym&quot;: &quot;DATACITE&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;infrastructure&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;stac&quot;, &quot;name&quot;: &quot;SpatioTemporal Asset Catalog&quot;, &quot;acronym&quot;: &quot;STAC&quot;, &quot;era&quot;: &quot;2010s&quot;, &quot;domain&quot;: &quot;infrastructure&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;scale_support&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;eml&quot;, &quot;name&quot;: &quot;Ecological Metadata Language&quot;, &quot;acronym&quot;: &quot;EML&quot;, &quot;era&quot;: &quot;1990s&quot;, &quot;domain&quot;: &quot;ecology&quot;, &quot;kind&quot;: &quot;metadata_standard&quot;, &quot;role&quot;: &quot;interoperability&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Interoperability&quot;, &quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;space&quot;, &quot;time&quot;, &quot;observation&quot;, &quot;sampling&quot;, &quot;method&quot;, &quot;units&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;ecolingua&quot;, &quot;name&quot;: &quot;Ecolingua&quot;, &quot;acronym&quot;: &quot;ECOLINGUA&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;ecology&quot;, &quot;kind&quot;: &quot;historical_effort&quot;, &quot;role&quot;: &quot;historical_comparison&quot;, &quot;status&quot;: &quot;historical&quot;, &quot;category&quot;: [&quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;ecosystem&quot;, &quot;observation&quot;, &quot;method&quot;], &quot;level&quot;: [&quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;seek&quot;, &quot;name&quot;: &quot;SEEK semantic mediation&quot;, &quot;acronym&quot;: &quot;SEEK&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;ecology&quot;, &quot;kind&quot;: &quot;historical_effort&quot;, &quot;role&quot;: &quot;historical_comparison&quot;, &quot;status&quot;: &quot;historical&quot;, &quot;category&quot;: [&quot;Historical precedent&quot;], &quot;dimension&quot;: [&quot;observation&quot;, &quot;method&quot;, &quot;provenance&quot;], &quot;level&quot;: []}, {&quot;id&quot;: &quot;oboe_ecology&quot;, &quot;name&quot;: &quot;OBOE ecology extensions&quot;, &quot;acronym&quot;: &quot;OBOE_ECOLOGY&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;ecology&quot;, &quot;kind&quot;: &quot;resource_network&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;documented&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [&quot;trait&quot;, &quot;ecosystem&quot;, &quot;observation&quot;], &quot;level&quot;: [&quot;ecosystem&quot;]}, {&quot;id&quot;: &quot;biodiversity_history&quot;, &quot;name&quot;: &quot;Historical biodiversity ontology efforts&quot;, &quot;acronym&quot;: &quot;BIODIVERSITY_HISTORY&quot;, &quot;era&quot;: &quot;2000s&quot;, &quot;domain&quot;: &quot;biodiversity&quot;, &quot;kind&quot;: &quot;historical_effort&quot;, &quot;role&quot;: &quot;historical_comparison&quot;, &quot;status&quot;: &quot;unresolved&quot;, &quot;category&quot;: [&quot;Historical precedent&quot;], &quot;dimension&quot;: [], &quot;level&quot;: []}, {&quot;id&quot;: &quot;anaee&quot;, &quot;name&quot;: &quot;AnaEE semantic resources&quot;, &quot;acronym&quot;: &quot;ANAEE&quot;, &quot;era&quot;: &quot;2020s&quot;, &quot;domain&quot;: &quot;ecology&quot;, &quot;kind&quot;: &quot;resource_network&quot;, &quot;role&quot;: &quot;domain_overlay&quot;, &quot;status&quot;: &quot;unresolved&quot;, &quot;category&quot;: [&quot;Domain candidate&quot;], &quot;dimension&quot;: [], &quot;level&quot;: []}]"></div>


## Resource details, limitations and evidence

An empty crosswalk/dependency field means **not recorded in this review**, not that none exists. Registry dependency metadata is not a parsed OWL-import graph. Resolvable identifiers mean the source declares persistent identifiers; live resolution of every term was not tested. Portal APIs are not assumed from a downloadable OWL file.

<details id="bfo" markdown>
<summary>Basic Formal Ontology — BFO</summary>

### Basic Formal Ontology

**Domain / assessed scope / role:** foundations; ; domain_overlay.
**Identity and status:** BFO; `upper_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Barry Smith.
**Original problem / contribution (project reading):** Project reading of documented scope: Distinguishes broad categories of entities and processes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Distinguishes broad categories of entities and processes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Upper categories do not identify biological variables or justify support changes.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bfo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bfo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bfo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="iao" markdown>
<summary>Information Artifact Ontology — IAO</summary>

### Information Artifact Ontology

**Domain / assessed scope / role:** foundations; method, provenance; domain_overlay.
**Identity and status:** IAO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jie Zheng.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes information entities used in scientific records.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes information entities used in scientific records.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** An information model does not establish the truth of an annotation.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/iao.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/iao.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `iao.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ro" markdown>
<summary>Relation Ontology — RO</summary>

### Relation Ontology

**Domain / assessed scope / role:** foundations; anatomy, population, community, interaction; provisional_core.
**Identity and status:** RO; `relation_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides explicitly defined relations used across OBO resources.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides explicitly defined relations used across OBO resources.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A relation name alone does not validate its application to a pair of source concepts.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ncbitaxon" markdown>
<summary>NCBI organismal classification — NCBITaxon</summary>

### NCBI organismal classification

**Domain / assessed scope / role:** taxonomy; organism, taxonomy; provisional_core.
**Identity and status:** NCBITaxon; `classification`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Frederic Bastian.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides organismal taxonomic identifiers in an ontology representation.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides organismal taxonomic identifiers in an ontology representation.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Taxonomic identity does not imply ecological or measurement equivalence.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ncbitaxon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ncbitaxon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ncbitaxon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="taxrank" markdown>
<summary>Taxonomic Rank Vocabulary — TAXRANK</summary>

### Taxonomic Rank Vocabulary

**Domain / assessed scope / role:** taxonomy; taxonomy; domain_overlay.
**Identity and status:** TAXRANK; `controlled_vocabulary`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jim Balhoff.
**Original problem / contribution (project reading):** Project reading of documented scope: Names taxonomic ranks.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names taxonomic ranks.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Ranks do not resolve competing taxon concepts or population membership.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/taxrank.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/taxrank.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `taxrank.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="pco" markdown>
<summary>Population and Community Ontology — PCO</summary>

### Population and Community Ontology

**Domain / assessed scope / role:** biology; organism, population, community, interaction, ecosystem; provisional_core.
**Identity and status:** PCO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Ramona Walls.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes collections and interacting groups of organisms.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes collections and interacting groups of organisms.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not by itself solve remote-sensing spatial support or population estimation.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, caro, envo, go, iao, ncbitaxon, pato, ro. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="envo" markdown>
<summary>Environment Ontology — ENVO</summary>

### Environment Ontology

**Domain / assessed scope / role:** environment; community, ecosystem, habitat, environment, space; provisional_core.
**Identity and status:** ENVO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pier Luigi Buttigieg.
**Original problem / contribution (project reading):** Project reading of documented scope: Distinguishes environmental systems features and materials.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Distinguishes environmental systems features and materials.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Environmental annotations do not justify transferring measurements across supports.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** chebi, foodon, go, ncbitaxon, pco, po, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/envo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/envo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `envo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="bco" markdown>
<summary>Biological Collections Ontology — BCO</summary>

### Biological Collections Ontology

**Domain / assessed scope / role:** observations; organism, taxonomy, observation, sampling, method; domain_overlay.
**Identity and status:** BCO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Ramona Walls.
**Original problem / contribution (project reading):** Project reading of documented scope: Models collecting sampling and biological material.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Models collecting sampling and biological material.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Collection metadata does not automatically establish taxon equivalence or sensor calibration.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="obi" markdown>
<summary>Ontology for Biomedical Investigations — OBI</summary>

### Ontology for Biomedical Investigations

**Domain / assessed scope / role:** observations; observation, sampling, method, units, provenance; domain_overlay.
**Identity and status:** OBI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Bjoern Peters.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes investigations instruments protocols and assays.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes investigations instruments protocols and assays.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Investigation descriptions do not establish compatibility with every ecological protocol.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/obi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/obi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `obi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="oba" markdown>
<summary>Ontology of Biological Attributes — OBA</summary>

### Ontology of Biological Attributes

**Domain / assessed scope / role:** traits; anatomy, organism, trait; provisional_core.
**Identity and status:** OBA; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Composes biological attributes for measurable characteristics.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Composes biological attributes for measurable characteristics.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Attributes need observation methods units and support to interpret measurements.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/oba.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/oba.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `oba.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="pato" markdown>
<summary>Phenotype And Trait Ontology — PATO</summary>

### Phenotype And Trait Ontology

**Domain / assessed scope / role:** traits; anatomy, organism, trait; provisional_core.
**Identity and status:** PATO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides qualities for entity-quality descriptions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides qualities for entity-quality descriptions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A quality term alone is not a complete variable or measurement protocol.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pato.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pato.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pato.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="to" markdown>
<summary>Plant Trait Ontology — TO</summary>

### Plant Trait Ontology

**Domain / assessed scope / role:** traits; organism, trait; domain_overlay.
**Identity and status:** TO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Names plant traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names plant traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not replace taxon method unit or plot-support evidence.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/to.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/to.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `to.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="po" markdown>
<summary>Plant Ontology — PO</summary>

### Plant Ontology

**Domain / assessed scope / role:** anatomy; cellular, anatomy, organism; provisional_core.
**Identity and status:** PO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes plant anatomy and development.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes plant anatomy and development.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical containment is not ecological aggregation.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/po.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/po.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `po.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="flopo" markdown>
<summary>Flora Phenotype Ontology — FLOPO</summary>

### Flora Phenotype Ontology

**Domain / assessed scope / role:** traits; anatomy, organism, taxonomy, trait; domain_overlay.
**Identity and status:** FLOPO; `application_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Robert Hoehndorf.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects flora phenotype descriptions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects flora phenotype descriptions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Text-derived phenotype coverage is not universal trait measurement coverage.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/flopo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/flopo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `flopo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="vt" markdown>
<summary>Vertebrate Trait Ontology — VT</summary>

### Vertebrate Trait Ontology

**Domain / assessed scope / role:** traits; anatomy, organism, trait; domain_overlay.
**Identity and status:** VT; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Carissa Park.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes vertebrate traits.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes vertebrate traits.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Vertebrate scope cannot be silently applied to all organisms.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/vt.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/vt.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `vt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="cmo" markdown>
<summary>Clinical Measurement Ontology — CMO</summary>

### Clinical Measurement Ontology

**Domain / assessed scope / role:** traits; trait, observation, method; domain_overlay.
**Identity and status:** CMO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Jennifer Smith.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes clinical measurement types.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes clinical measurement types.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Clinical scope does not establish ecological measurement equivalence.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC0 1.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/cmo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/cmo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `cmo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="uberon" markdown>
<summary>Uberon multispecies anatomy ontology — UBERON</summary>

### Uberon multispecies anatomy ontology

**Domain / assessed scope / role:** anatomy; cellular, anatomy, organism; provisional_core.
**Identity and status:** UBERON; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects anatomical structures across species.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects anatomical structures across species.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical correspondence is not a rule for ecosystem or raster support.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, bspo, chebi, cl, envo, go, nbo, ncbitaxon, omo, pato, pr, ro. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/uberon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/uberon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `uberon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="cl" markdown>
<summary>Cell Ontology — CL</summary>

### Cell Ontology

**Domain / assessed scope / role:** anatomy; cellular, anatomy; domain_overlay.
**Identity and status:** CL; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: David Osumi-Sutherland.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes cell types.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes cell types.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Cell type is distinct from taxon organism and sampled cell abundance.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** go, ncbitaxon, omo, pato, pr, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/cl.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/cl.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `cl.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="caro" markdown>
<summary>Common Anatomy Reference Ontology — CARO</summary>

### Common Anatomy Reference Ontology

**Domain / assessed scope / role:** anatomy; anatomy, organism; domain_overlay.
**Identity and status:** CARO; `formal_ontology`; inactive_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Melissa Haendel.
**Original problem / contribution (project reading):** Project reading of documented scope: Supplies shared anatomical categories.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Supplies shared anatomical categories.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Reference anatomy is not a complete organism-specific anatomical or ecological model.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/caro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `caro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="bspo" markdown>
<summary>Biological Spatial Ontology — BSPO</summary>

### Biological Spatial Ontology

**Domain / assessed scope / role:** anatomy; anatomy, space; domain_overlay.
**Identity and status:** BSPO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Chris Mungall.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes anatomical spatial organization.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes anatomical spatial organization.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Anatomical spatial relations are not geospatial CRS or raster support.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/bspo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/bspo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `bspo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="go" markdown>
<summary>Gene Ontology — GO</summary>

### Gene Ontology

**Domain / assessed scope / role:** molecular; molecular, cellular, trait; domain_overlay.
**Identity and status:** GO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Suzi Aleksander.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes molecular functions biological processes and cellular components.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes molecular functions biological processes and cellular components.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Functional annotation does not directly define organism or community ecological traits.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** cl, go/extensions/go-bridge-to-nifstd.owl, ncbitaxon, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/go.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/go.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `go.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="so" markdown>
<summary>Sequence Ontology — SO</summary>

### Sequence Ontology

**Domain / assessed scope / role:** molecular; molecular; domain_overlay.
**Identity and status:** SO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Karen Eilbeck.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes biological sequence features.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes biological sequence features.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Sequence features do not establish organismal abundance or habitat equivalence.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/so.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/so.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `so.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="pr" markdown>
<summary>Protein Ontology — PRO</summary>

### Protein Ontology

**Domain / assessed scope / role:** molecular; molecular; domain_overlay.
**Identity and status:** PRO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Darren Natale.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents protein forms and relationships.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents protein forms and relationships.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Protein identity does not substitute for experimental context or ecological support.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/pr.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pr.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `pr.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="chebi" markdown>
<summary>Chemical Entities of Biological Interest — CHEBI</summary>

### Chemical Entities of Biological Interest

**Domain / assessed scope / role:** molecular; molecular, environment; domain_overlay.
**Identity and status:** CHEBI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Adnan Malik.
**Original problem / contribution (project reading):** Project reading of documented scope: Identifies chemical entities.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Identifies chemical entities.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Chemical identity alone does not define concentration matrix or exposure.
**Access / format:** Registry-linked release files; not fetched; GZ; JSON; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/chebi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/chebi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `chebi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="nbo" markdown>
<summary>Neuro Behavior Ontology — NBO</summary>

### Neuro Behavior Ontology

**Domain / assessed scope / role:** behavior; organism, trait, behavior; domain_overlay.
**Identity and status:** NBO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes behavioral processes and phenotypes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes behavioral processes and phenotypes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Behavioral vocabulary does not supply a universal ecological behavior protocol.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/nbo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/nbo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `nbo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="omp" markdown>
<summary>Ontology of Microbial Phenotypes — OMP</summary>

### Ontology of Microbial Phenotypes

**Domain / assessed scope / role:** microbiome; organism, trait, method; domain_overlay.
**Identity and status:** OMP; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: James C. Hu.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes microbial phenotypes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes microbial phenotypes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Phenotypes depend on strain and experimental conditions.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 3.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/omp.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/omp.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `omp.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="micro" markdown>
<summary>MicrO: Prokaryotic Phenotypic and Metabolic Characters — MICRO</summary>

### MicrO: Prokaryotic Phenotypic and Metabolic Characters

**Domain / assessed scope / role:** microbiome; organism, trait, method; domain_overlay.
**Identity and status:** MICRO; `formal_ontology`; inactive_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Carrine Blank.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes prokaryotic phenotypic and metabolic characters.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes prokaryotic phenotypic and metabolic characters.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Registry reports inactive; evaluate version and reuse before adoption.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 2.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/micro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/micro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `micro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ohmi" markdown>
<summary>Ontology of Host-Microbiome Interactions — OHMI</summary>

### Ontology of Host-Microbiome Interactions

**Domain / assessed scope / role:** microbiome; organism, community, interaction, environment; domain_overlay.
**Identity and status:** OHMI; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Yongqun Oliver He.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects hosts microbiomes and their interactions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects hosts microbiomes and their interactions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Host-microbiome scope does not solve all soil or marine sampling semantics.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/ohmi.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/ohmi.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `ohmi.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="agro" markdown>
<summary>Agronomy Ontology — AGRO</summary>

### Agronomy Ontology

**Domain / assessed scope / role:** agriculture; trait, environment, observation, method; domain_overlay.
**Identity and status:** AGRO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Marie-Angélique Laporte.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes agronomic experiments and management.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes agronomic experiments and management.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Agronomic terms do not by themselves define food-security outcomes.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, envo, foodon, go, iao, ncbitaxon, obi, pato, peco, po, ro, to, uo, xco. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/agro.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/agro.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `agro.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="peco" markdown>
<summary>Plant Experimental Conditions Ontology — PECO</summary>

### Plant Experimental Conditions Ontology

**Domain / assessed scope / role:** agriculture; trait, environment, method; domain_overlay.
**Identity and status:** PECO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Pankaj Jaiswal.
**Original problem / contribution (project reading):** Project reading of documented scope: Names plant experimental conditions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Names plant experimental conditions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A condition label does not encode complete experimental exposure or support.
**Access / format:** Registry-linked release files; not fetched; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/peco.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/peco.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `peco.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="foodon" markdown>
<summary>Food Ontology — FOODON</summary>

### Food Ontology

**Domain / assessed scope / role:** agriculture; molecular, organism, environment; domain_overlay.
**Identity and status:** FOODON; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: Damion Dooley.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes food products sources and processing.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes food products sources and processing.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Food descriptions are not a validated food-security model.
**Access / format:** Registry-linked release files; not fetched; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** bfo, chebi, envo, eo, ncbitaxon, obi, ro, uberon. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/foodon.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/foodon.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `foodon.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="uo" markdown>
<summary>Units of Measurement Ontology — UO</summary>

### Units of Measurement Ontology

**Domain / assessed scope / role:** quantities; units; domain_overlay.
**Identity and status:** UO; `formal_ontology`; active_registry.
**Milestone / era:** First release not established in inspected registry metadata; unknown.
**Maintainer evidence:** Registry contact: George Gkoutos.
**Original problem / contribution (project reading):** Project reading of documented scope: Identifies measurement units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Identifies measurement units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Same or convertible units do not establish variable equivalence.
**Access / format:** Registry-linked release files; not fetched; JSON; OBO; OWL products declared by registry.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://obofoundry.org/ontology/uo.html), [source 2](https://purl.obolibrary.org/meta/ontologies.jsonld).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/uo.owl).
**Verification:** registry_metadata; last verified 2026-10-21. Assessment `uo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="dolce" markdown>
<summary>DOLCE / DUL — DOLCE</summary>

### DOLCE / DUL

**Domain / assessed scope / role:** foundations; ; domain_overlay.
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

</details>

<details id="skos" markdown>
<summary>Simple Knowledge Organization System — SKOS</summary>

### Simple Knowledge Organization System

**Domain / assessed scope / role:** foundations; ; interoperability.
**Identity and status:** SKOS; `semantic_framework`; documented.
**Milestone / era:** 2009 W3C Recommendation; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents concept schemes labels and broader narrower mappings.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents concept schemes labels and broader narrower mappings.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** SKOS broader is not automatically OWL subclass.
**Access / format:** Documentation/resource link only; no live resolver integration; RDF vocabulary and normative concept-scheme specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/skos-reference/).
**Canonical resource link:** [resource](http://www.w3.org/2004/02/skos/core#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `skos.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="tcs" markdown>
<summary>Taxonomic Concept Schema — TCS</summary>

### Taxonomic Concept Schema

**Domain / assessed scope / role:** taxonomy; organism, taxonomy; interoperability.
**Identity and status:** TCS; `exchange_standard`; documented.
**Milestone / era:** 2005 TCS standard; subsequent TCS2 revision work; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Separates taxon names from taxon concepts in exchange.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Separates taxon names from taxon concepts in exchange.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A taxon name alone cannot resolve concept circumscription.
**Access / format:** Documentation/resource link only; no live resolver integration; Taxonomic exchange schema; historical XML model and revision work.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.tdwg.org/community/tnc/tcs2/).
**Canonical resource link:** [resource](http://www.tdwg.org/standards/117).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `tcs.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="dwc" markdown>
<summary>Darwin Core — DWC</summary>

### Darwin Core

**Domain / assessed scope / role:** biodiversity; organism, taxonomy, space, time, observation, sampling, method; interoperability.
**Identity and status:** DWC; `exchange_standard`; documented.
**Milestone / era:** 2009 TDWG ratification; work predates ratification; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides community terms for biodiversity data exchange.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides community terms for biodiversity data exchange.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A populated field does not prove biological equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Term vocabulary; documented text/archive and other exchange encodings.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://dwc.tdwg.org/).
**Canonical resource link:** [resource](http://rs.tdwg.org/dwc/terms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dwc.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="dwc_cm" markdown>
<summary>Darwin Core Conceptual Model — DWC_CM</summary>

### Darwin Core Conceptual Model

**Domain / assessed scope / role:** biodiversity; organism, taxonomy, observation, sampling; domain_overlay.
**Identity and status:** DWC_CM; `conceptual_model`; documented.
**Milestone / era:** Current conceptual-model documentation; earliest origin not established; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Explains relationships among Darwin Core classes.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Explains relationships among Darwin Core classes.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Conceptual relationships are not all formal ontology predicates.
**Access / format:** Documentation/resource link only; no live resolver integration; Conceptual documentation; not itself a complete formal predicate ontology.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://dwc.tdwg.org/cm/).
**Canonical resource link:** [resource](https://dwc.tdwg.org/cm/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dwc_cm.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="darwin_sw" markdown>
<summary>Darwin-SW — DARWIN_SW</summary>

### Darwin-SW

**Domain / assessed scope / role:** biodiversity; organism, taxonomy, space, time, observation, sampling; domain_overlay.
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

</details>

<details id="worms" markdown>
<summary>WoRMS / Aphia taxonomic resources — WORMS</summary>

### WoRMS / Aphia taxonomic resources

**Domain / assessed scope / role:** marine; organism, taxonomy; domain_overlay.
**Identity and status:** WORMS; `controlled_vocabulary`; documented.
**Milestone / era:** Aphia/WoRMS database development; exact first release not established; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides authoritative marine names and stable Aphia identifiers.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides authoritative marine names and stable Aphia identifiers.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Taxonomic authority and ontology-network semantics are distinct resources.
**Access / format:** Official REST service documented; not integrated or probed; Resource-specific; consult cited specification.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.marinespecies.org/about.php), [source 2](https://www.marinespecies.org/rest/).
**Canonical resource link:** [resource](https://www.marinespecies.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `worms.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="humboldt" markdown>
<summary>Humboldt Extension — HUMBOLDT</summary>

### Humboldt Extension

**Domain / assessed scope / role:** biodiversity; population, community, observation, sampling, method, scale_support; interoperability.
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

</details>

<details id="oboe" markdown>
<summary>Extensible Observation Ontology — OBOE</summary>

### Extensible Observation Ontology

**Domain / assessed scope / role:** observations; space, time, observation, sampling, method, units, scale_support; provisional_core.
**Identity and status:** OBOE; `formal_ontology`; documented.
**Milestone / era:** 2007 ecological observation paper; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Relates observations measurements entities characteristics standards and protocols.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Relates observations measurements entities characteristics standards and protocols.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Observation structure does not independently justify scale transformations.
**Access / format:** Documentation/resource link only; no live resolver integration; OWL ontology.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NCEAS/oboe).
**Canonical resource link:** [resource](http://ecoinformatics.org/oboe/oboe.1.2/oboe.owl).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `oboe.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="sosa" markdown>
<summary>Sensor Observation Sample and Actuator — SOSA</summary>

### Sensor Observation Sample and Actuator

**Domain / assessed scope / role:** observations; space, time, observation, sampling, method; provisional_core.
**Identity and status:** SOSA; `formal_ontology`; documented.
**Milestone / era:** 2017 W3C/OGC Recommendation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Lightweight core for observations sampling and sensing.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Lightweight core for observations sampling and sensing.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Observation identity does not determine scientific comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; RDF/OWL ontology.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-ssn/).
**Canonical resource link:** [resource](http://www.w3.org/ns/sosa/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `sosa.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ssn" markdown>
<summary>Semantic Sensor Network Ontology — SSN</summary>

### Semantic Sensor Network Ontology

**Domain / assessed scope / role:** observations; space, time, observation, sampling, method, scale_support; domain_overlay.
**Identity and status:** SSN; `formal_ontology`; documented.
**Milestone / era:** 2017 Recommendation; earlier SSN work exists; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Extends sensor and observation modeling around SOSA.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Extends sensor and observation modeling around SOSA.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Sensor modeling does not establish biological meanings or mappings.
**Access / format:** Documentation/resource link only; no live resolver integration; RDF/OWL ontology.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** sosa. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-ssn/).
**Canonical resource link:** [resource](http://www.w3.org/ns/ssn/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ssn.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="iadopt" markdown>
<summary>I-ADOPT Interoperability Framework — I-ADOPT</summary>

### I-ADOPT Interoperability Framework

**Domain / assessed scope / role:** observations; trait, environment, observation; provisional_core.
**Identity and status:** I-ADOPT; `semantic_framework`; documented.
**Milestone / era:** 2021 framework and recommendations; 2020s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Decomposes variables into property object of interest matrix context and constraints.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Decomposes variables into property object of interest matrix context and constraints.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Does not supply every domain concept or replace units methods or observational ontologies.
**Access / format:** Documentation/resource link only; no live resolver integration; Ontology and variable-composition framework.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.rd-alliance.org/wp-content/uploads/2024/12/I_ADOPT_recommendations.pdf).
**Canonical resource link:** [resource](https://w3id.org/iadopt/ont/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `iadopt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ets" markdown>
<summary>Ecological Trait-data Standard — ETS</summary>

### Ecological Trait-data Standard

**Domain / assessed scope / role:** traits; organism, trait, observation, method, units; interoperability.
**Identity and status:** ETS; `exchange_standard`; documented.
**Milestone / era:** 2018 rationale; 2019 v0.10 citation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes trait data with persistent vocabulary fields.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes trait data with persistent vocabulary fields.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A trait-data standard does not guarantee method or support comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; CSV vocabulary source and OWL distribution.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/EcologicalTraitData/ETS).
**Canonical resource link:** [resource](https://ecologicaltraitdata.github.io/ETS/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `ets.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="mixs" markdown>
<summary>Minimum Information about any Sequence — MIXS</summary>

### Minimum Information about any Sequence

**Domain / assessed scope / role:** molecular; molecular, environment, sampling, method; interoperability.
**Identity and status:** MIXS; `metadata_standard`; documented.
**Milestone / era:** 2011 MIxS publication; predecessor checklists are earlier; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes sequence sample context through checklists and extensions.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes sequence sample context through checklists and extensions.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Metadata compliance is not sequence or taxon equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; LinkML schemas, checklists and environmental extensions.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://genomicsstandardsconsortium.github.io/mixs/).
**Canonical resource link:** [resource](https://w3id.org/mixs).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `mixs.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="microbiome_core" markdown>
<summary>Microbiome Ontology Core — MICROBIOME_CORE</summary>

### Microbiome Ontology Core

**Domain / assessed scope / role:** microbiome; organism, community, interaction; domain_overlay.
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

</details>

<details id="globi" markdown>
<summary>GloBI + RO — GLOBI</summary>

### GloBI + RO

**Domain / assessed scope / role:** interactions; organism, taxonomy, interaction; domain_overlay.
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

</details>

<details id="sfwo" markdown>
<summary>Soil Food Web Ontology — SFWO</summary>

### Soil Food Web Ontology

**Domain / assessed scope / role:** interactions; trait, community, interaction, environment; domain_overlay.
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

</details>

<details id="agrovoc" markdown>
<summary>AGROVOC — AGROVOC</summary>

### AGROVOC

**Domain / assessed scope / role:** agriculture; organism, trait, environment, method; domain_overlay.
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

</details>

<details id="crop" markdown>
<summary>Crop Ontology — CROP</summary>

### Crop Ontology

**Domain / assessed scope / role:** agriculture; organism, trait, observation, method, units; domain_overlay.
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

</details>

<details id="miappe" markdown>
<summary>Minimum Information About Plant Phenotyping Experiments — MIAPPE</summary>

### Minimum Information About Plant Phenotyping Experiments

**Domain / assessed scope / role:** agriculture; trait, environment, observation, sampling, method, scale_support; interoperability.
**Identity and status:** MIAPPE; `metadata_standard`; documented.
**Milestone / era:** Community standard; exact first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Specifies experimental phenotyping metadata through checklist and data model.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Specifies experimental phenotyping metadata through checklist and data model.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Checklist completeness is not trait or experimental equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; Metadata checklist/data model and tabular templates.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.miappe.org/).
**Canonical resource link:** [resource](https://www.miappe.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `miappe.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ppeo" markdown>
<summary>Plant Phenotyping Experiment Ontology — PPEO</summary>

### Plant Phenotyping Experiment Ontology

**Domain / assessed scope / role:** agriculture; trait, environment, observation, sampling, method; domain_overlay.
**Identity and status:** PPEO; `application_ontology`; documented.
**Milestone / era:** Implementation of MIAPPE; precise origin not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents MIAPPE experimental metadata structure.
**Relationship to prior work:** OWL representation of the MIAPPE checklist/data-model structure; not interchangeable with the checklist itself.
**Historical role:** Project assessment: Represents MIAPPE experimental metadata structure.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Experimental metadata structure does not supply all domain trait semantics.
**Access / format:** Documentation/resource link only; no live resolver integration; OWL ontology representation of MIAPPE.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/MIAPPE/MIAPPE-ontology).
**Canonical resource link:** [resource](https://github.com/MIAPPE/MIAPPE-ontology).
**Verification:** reference_only; last verified not established. Assessment `ppeo.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="pso" markdown>
<summary>Plant Stress Ontology — PSO</summary>

### Plant Stress Ontology

**Domain / assessed scope / role:** agriculture; trait, environment, method; domain_overlay.
**Identity and status:** PSO; `formal_ontology`; documented.
**Milestone / era:** Planteome development; first release not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes biotic and abiotic plant stresses.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes biotic and abiotic plant stresses.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Stress categories do not define complete exposure dose or response variables.
**Access / format:** Documentation/resource link only; no live resolver integration; OWL/OBO distributions.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/Planteome/plant-stress-ontology).
**Canonical resource link:** [resource](http://purl.obolibrary.org/obo/pso.owl).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `pso.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="atol" markdown>
<summary>Animal Trait Ontology for Livestock — ATOL</summary>

### Animal Trait Ontology for Livestock

**Domain / assessed scope / role:** agriculture; organism, trait; domain_overlay.
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

</details>

<details id="eol" markdown>
<summary>Environment Ontology for Livestock — EOL</summary>

### Environment Ontology for Livestock

**Domain / assessed scope / role:** agriculture; organism, environment, method; domain_overlay.
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

</details>

<details id="lpt" markdown>
<summary>Livestock Product Trait Ontology — LPT</summary>

### Livestock Product Trait Ontology

**Domain / assessed scope / role:** agriculture; organism, trait; domain_overlay.
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

</details>

<details id="sweet" markdown>
<summary>Semantic Web for Earth and Environmental Terminology — SWEET</summary>

### Semantic Web for Earth and Environmental Terminology

**Domain / assessed scope / role:** environment; ecosystem, environment, space, time, units; domain_overlay.
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

</details>

<details id="ecso" markdown>
<summary>Ecosystems Ontology — ECSO</summary>

### Ecosystems Ontology

**Domain / assessed scope / role:** environment; ecosystem, environment, observation, units; domain_overlay.
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

</details>

<details id="cf" markdown>
<summary>CF Standard Names — CF</summary>

### CF Standard Names

**Domain / assessed scope / role:** environment; environment, observation, method, units; domain_overlay.
**Identity and status:** CF; `controlled_vocabulary`; documented.
**Milestone / era:** CF conventions development; specific table versions are separately versioned; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides named physical quantities with canonical units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides named physical quantities with canonical units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Same canonical unit does not establish the same standard name or cell method.
**Access / format:** Documentation/resource link only; no live resolver integration; Standard-name table and canonical-unit metadata.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://cfconventions.org/faq.html).
**Canonical resource link:** [resource](https://cfconventions.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `cf.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="gcmd" markdown>
<summary>GCMD Keywords — GCMD</summary>

### GCMD Keywords

**Domain / assessed scope / role:** environment; environment, space, time, observation; domain_overlay.
**Identity and status:** GCMD; `controlled_vocabulary`; documented.
**Milestone / era:** GCMD catalog lineage; exact first keyword release not established; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Supports Earth-science discovery using managed keyword hierarchies.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Supports Earth-science discovery using managed keyword hierarchies.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Discovery keywords are not formal measurement definitions.
**Access / format:** Documentation/resource link only; no live resolver integration; Managed keyword vocabulary and KMS documentation.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.earthdata.nasa.gov/sites/default/files/imported/KeywordsCommunityGuide_Baseline_v1_SIGNED_FINAL.pdf).
**Canonical resource link:** [resource](https://gcmd.earthdata.nasa.gov/kms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `gcmd.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="gemet" markdown>
<summary>General Multilingual Environmental Thesaurus — GEMET</summary>

### General Multilingual Environmental Thesaurus

**Domain / assessed scope / role:** environment; habitat, environment; domain_overlay.
**Identity and status:** GEMET; `thesaurus`; documented.
**Milestone / era:** Development since 1995 documented by EEA; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Connects multilingual environmental indexing concepts.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Connects multilingual environmental indexing concepts.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Broader and related thesaurus links are not biological equivalence.
**Access / format:** Official HTTP/XML-RPC API documented; not integrated or probed; RDF/SKOS, XML and documented JSON service results.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.eionet.europa.eu/gemet/en/about/), [source 2](https://www.eionet.europa.eu/gemet/en/webservices/).
**Canonical resource link:** [resource](https://www.eionet.europa.eu/gemet/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `gemet.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="iucn_habitat" markdown>
<summary>IUCN Habitats Classification Scheme — IUCN_HABITAT</summary>

### IUCN Habitats Classification Scheme

**Domain / assessed scope / role:** conservation; taxonomy, habitat, environment; domain_overlay.
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

</details>

<details id="iucn_threat" markdown>
<summary>IUCN Threats Classification Scheme — IUCN_THREAT</summary>

### IUCN Threats Classification Scheme

**Domain / assessed scope / role:** conservation; taxonomy, interaction, environment; domain_overlay.
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

</details>

<details id="iucn_redlist" markdown>
<summary>IUCN Red List Categories and Criteria — IUCN_REDLIST</summary>

### IUCN Red List Categories and Criteria

**Domain / assessed scope / role:** conservation; taxonomy, population; domain_overlay.
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

</details>

<details id="ebv" markdown>
<summary>Essential Biodiversity Variables — EBV</summary>

### Essential Biodiversity Variables

**Domain / assessed scope / role:** conservation; taxonomy, trait, population, community, ecosystem, space, time, scale_support; domain_overlay.
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

</details>

<details id="bari" markdown>
<summary>EBV application-ontology / Bari Manifesto work — BARI</summary>

### EBV application-ontology / Bari Manifesto work

**Domain / assessed scope / role:** conservation; ecosystem, observation, scale_support, provenance; domain_overlay.
**Identity and status:** BARI; `semantic_framework`; documented.
**Milestone / era:** 2018 Bari Manifesto; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Proposes interoperability architecture for EBV production.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Proposes interoperability architecture for EBV production.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A recommendation to develop an ontology is not proof of a deployed complete ontology.
**Access / format:** Documentation/resource link only; no live resolver integration; Scientific paper and interoperability recommendations.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.vliz.be/imisdocs/publications/322519.pdf).
**Canonical resource link:** Unresolved; no URI invented.
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `bari.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="bon_box" markdown>
<summary>BON in a Box semantic work — BON_BOX</summary>

### BON in a Box semantic work

**Domain / assessed scope / role:** conservation; observation, method, provenance; domain_overlay.
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

</details>

<details id="marine_tlo" markdown>
<summary>MarineTLO — MARINE_TLO</summary>

### MarineTLO

**Domain / assessed scope / role:** marine; organism, taxonomy, environment, space, time, observation; domain_overlay.
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

</details>

<details id="marine_regions" markdown>
<summary>Marine Regions semantic resources — MARINE_REGIONS</summary>

### Marine Regions semantic resources

**Domain / assessed scope / role:** marine; habitat, environment, space; domain_overlay.
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

</details>

<details id="aphia_network" markdown>
<summary>APHIA ontology network — APHIA_NETWORK</summary>

### APHIA ontology network

**Domain / assessed scope / role:** marine; organism, taxonomy, interaction, space; domain_overlay.
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

</details>

<details id="geosparql" markdown>
<summary>GeoSPARQL — GEOSPARQL</summary>

### GeoSPARQL

**Domain / assessed scope / role:** space; space, scale_support; provisional_core.
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

</details>

<details id="owl_time" markdown>
<summary>OWL-Time — OWL-Time</summary>

### OWL-Time

**Domain / assessed scope / role:** time; time, scale_support; provisional_core.
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

</details>

<details id="qudt" markdown>
<summary>Quantities Units Dimensions and Types — QUDT</summary>

### Quantities Units Dimensions and Types

**Domain / assessed scope / role:** quantities; units; provisional_core.
**Identity and status:** QUDT; `formal_ontology`; documented.
**Milestone / era:** NASA NExIOM lineage; exact first release not established; 2000s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents quantities quantity kinds dimensions and units.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents quantities quantity kinds dimensions and units.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Unit convertibility cannot establish biological or variable equivalence.
**Access / format:** Official RDF vocabulary resources and SPARQL endpoint documented; not integrated or probed; RDF/SHACL models and vocabularies.
**License:** CC BY 4.0. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.qudt.org/).
**Canonical resource link:** [resource](http://qudt.org/schema/qudt/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `qudt.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="prov" markdown>
<summary>PROV-O — PROV-O</summary>

### PROV-O

**Domain / assessed scope / role:** provenance; provenance; provisional_core.
**Identity and status:** PROV-O; `formal_ontology`; documented.
**Milestone / era:** 2013 W3C Recommendation; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Represents entities activities agents and derivations.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Represents entities activities agents and derivations.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A recorded derivation is not proof of scientific justification.
**Access / format:** Documentation/resource link only; no live resolver integration; OWL ontology / RDF.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/prov-o/).
**Canonical resource link:** [resource](http://www.w3.org/ns/prov#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `prov.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="provone" markdown>
<summary>ProvONE — PROVONE</summary>

### ProvONE

**Domain / assessed scope / role:** provenance; method, provenance; domain_overlay.
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

</details>

<details id="dcat" markdown>
<summary>Data Catalog Vocabulary — DCAT</summary>

### Data Catalog Vocabulary

**Domain / assessed scope / role:** infrastructure; space, time, provenance; interoperability.
**Identity and status:** DCAT; `metadata_standard`; documented.
**Milestone / era:** 2014 first Recommendation; 2024 DCAT 3; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes datasets distributions and catalog services.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes datasets distributions and catalog services.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Catalog metadata does not establish observation meaning or equivalence.
**Access / format:** Documentation/resource link only; no live resolver integration; RDF vocabulary.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.w3.org/TR/vocab-dcat-3/).
**Canonical resource link:** [resource](http://www.w3.org/ns/dcat#).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dcat.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="dcterms" markdown>
<summary>Dublin Core / DCTERMS — DCTERMS</summary>

### Dublin Core / DCTERMS

**Domain / assessed scope / role:** infrastructure; space, time, provenance; interoperability.
**Identity and status:** DCTERMS; `metadata_standard`; documented.
**Milestone / era:** 1995 workshop lineage; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Provides general resource metadata terms.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Provides general resource metadata terms.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** General metadata terms do not supply domain measurement definitions.
**Access / format:** Documentation/resource link only; no live resolver integration; RDF vocabulary and metadata term documentation.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/).
**Canonical resource link:** [resource](http://purl.org/dc/terms/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `dcterms.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="datacite" markdown>
<summary>DataCite Metadata Schema — DATACITE</summary>

### DataCite Metadata Schema

**Domain / assessed scope / role:** infrastructure; space, time, provenance; interoperability.
**Identity and status:** DATACITE; `metadata_standard`; documented.
**Milestone / era:** Schema revisions are versioned; origin not established; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes research outputs for identification citation and discovery.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes research outputs for identification citation and discovery.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Citation metadata is not scientific harmonization.
**Access / format:** Documentation/resource link only; no live resolver integration; Versioned XML schema and documentation.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://schema.datacite.org/).
**Canonical resource link:** [resource](https://schema.datacite.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `datacite.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="stac" markdown>
<summary>SpatioTemporal Asset Catalog — STAC</summary>

### SpatioTemporal Asset Catalog

**Domain / assessed scope / role:** infrastructure; space, time, observation, scale_support, provenance; interoperability.
**Identity and status:** STAC; `metadata_standard`; documented.
**Milestone / era:** Community development before 1.0; precise origin not reverified; 2010s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Describes spatiotemporal assets with extension metadata.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Describes spatiotemporal assets with extension metadata.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** A catalog standard is not the entire pipeline or an equivalence ontology.
**Access / format:** Documentation/resource link only; no live resolver integration; JSON metadata and JSON Schema.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/radiantearth/stac-spec).
**Canonical resource link:** [resource](https://stacspec.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `stac.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="eml" markdown>
<summary>Ecological Metadata Language — EML</summary>

### Ecological Metadata Language

**Domain / assessed scope / role:** ecology; space, time, observation, sampling, method, units, provenance; interoperability.
**Identity and status:** EML; `metadata_standard`; documented.
**Milestone / era:** 1997 metadata work cited as precursor; EML releases followed; 1990s.
**Maintainer evidence:** See cited resource documentation; not independently established.
**Original problem / contribution (project reading):** Project reading of documented scope: Documents ecological dataset entities methods attributes and access.
**Relationship to prior work:** Compose with other domain resources; no equivalence or import inferred from similar scope.
**Historical role:** Project assessment: Documents ecological dataset entities methods attributes and access.
**Current relevance:** Candidate for evidence discovery/comparison; adoption and exact version need review.
**Does not establish:** Metadata completeness does not prove cross-dataset comparability.
**Access / format:** Documentation/resource link only; no live resolver integration; XML metadata schema.
**License:** Not established. This record is not a blanket redistribution permission.
**Dependencies recorded:** Not recorded. **Crosswalks recorded:** Not recorded.
**Evidence:** [source 1](https://github.com/NCEAS/eml).
**Canonical resource link:** [resource](https://eml.ecoinformatics.org/).
**Verification:** primary_documentation; last verified 2026-10-21. Assessment `eml.landscape-v1`, coding-assistant, 2026-10-21; expert review pending.

</details>

<details id="ecolingua" markdown>
<summary>Ecolingua — ECOLINGUA</summary>

### Ecolingua

**Domain / assessed scope / role:** ecology; ecosystem, observation, method; historical_comparison.
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

</details>

<details id="seek" markdown>
<summary>SEEK semantic mediation — SEEK</summary>

### SEEK semantic mediation

**Domain / assessed scope / role:** ecology; observation, method, provenance; historical_comparison.
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

</details>

<details id="oboe_ecology" markdown>
<summary>OBOE ecology extensions — OBOE_ECOLOGY</summary>

### OBOE ecology extensions

**Domain / assessed scope / role:** ecology; trait, ecosystem, observation; domain_overlay.
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

</details>

<details id="biodiversity_history" markdown>
<summary>Historical biodiversity ontology efforts — BIODIVERSITY_HISTORY</summary>

### Historical biodiversity ontology efforts

**Domain / assessed scope / role:** biodiversity; ; historical_comparison.
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

</details>

<details id="anaee" markdown>
<summary>AnaEE semantic resources — ANAEE</summary>

### AnaEE semantic resources

**Domain / assessed scope / role:** ecology; ; domain_overlay.
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

</details>
