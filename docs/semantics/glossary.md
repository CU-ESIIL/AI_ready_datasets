# Glossary

Working explanations for scientists entering semantic engineering. Definitions are contextual; individual communities and standards can draw boundaries differently. These notes are not new ontology axioms or approved concept mappings. See [key distinctions](distinctions.md), [resource landscape](landscape.md) and [human review workflow](review-workflow.md).

Source orientation: [SKOS](https://www.w3.org/TR/skos-reference/), [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [OBOE](https://github.com/NCEAS/oboe), [I-ADOPT recommendations](https://www.rd-alliance.org/wp-content/uploads/2024/12/I_ADOPT_recommendations.pdf), [Darwin Core](https://dwc.tdwg.org/), [PROV-O](https://www.w3.org/TR/prov-o/), [QUDT](https://www.qudt.org/) and [CF conventions](https://cfconventions.org/faq.html). The prose below is project explanation; consult the cited resource for normative definitions.

## Find a term

**Semantic infrastructure:** [ontology](#ontology), [vocabulary](#vocabulary), [controlled vocabulary](#controlled-vocabulary), [thesaurus](#thesaurus), [classification](#classification), [taxonomy](#taxonomy), [knowledge graph](#knowledge-graph), [semantic model](#semantic-model), [conceptual model](#conceptual-model), [schema](#schema), [standard](#standard), [concept](#concept), [class](#class), [instance](#instance), [identifier](#identifier), [URI / IRI](#uri-iri), [label](#label), [synonym](#synonym), [definition](#definition), [axiom](#axiom), [relation](#relation), [subclass / is-a](#subclass-is-a), [part-of](#part-of), [member-of](#member-of), [broader / narrower](#broader-narrower), [equivalent](#equivalent), [alignment](#alignment), [mapping](#mapping), [crosswalk](#crosswalk), [semantic interoperability](#semantic-interoperability), [upper ontology](#upper-ontology), [domain ontology](#domain-ontology), [application ontology](#application-ontology), [ontology import](#ontology-import), [ontology profile](#ontology-profile), [semantic composition](#semantic-composition), [entity-quality model](#entity-quality-model), [I-ADOPT decomposition](#i-adopt-decomposition), [SKOS](#skos).

**Biological organization:** [biological entity](#biological-entity), [organism](#organism), [taxon](#taxon), [taxon name](#taxon-name), [taxon concept](#taxon-concept), [taxonomic rank](#taxonomic-rank), [population](#population), [community](#community), [assemblage](#assemblage), [guild](#guild), [functional group](#functional-group), [ecosystem](#ecosystem), [biome](#biome), [habitat](#habitat), [environmental system](#environmental-system), [environmental feature](#environmental-feature), [environmental material](#environmental-material).

**Biological characteristics:** [trait](#trait), [attribute](#attribute), [phenotype](#phenotype), [quality](#quality), [behavior](#behavior), [biotic interaction](#biotic-interaction), [trophic interaction](#trophic-interaction), [property hint](#property-hint).

**Observation and measurement:** [observation](#observation), [measurement](#measurement), [observed property](#observed-property), [feature of interest](#feature-of-interest), [object of interest](#object-of-interest), [matrix](#matrix), [context object](#context-object), [sample](#sample), [specimen](#specimen), [occurrence](#occurrence), [event](#event), [inventory](#inventory), [survey](#survey), [sampling](#sampling), [protocol](#protocol), [method](#method), [sensor](#sensor), [platform](#platform).

**Scale and support:** [spatial extent](#spatial-extent), [spatial resolution](#spatial-resolution), [spatial support](#spatial-support), [footprint](#footprint), [CRS](#crs), [location](#location), [temporal extent](#temporal-extent), [temporal resolution](#temporal-resolution), [temporal support](#temporal-support), [timestamp](#timestamp), [instant](#instant), [interval](#interval), [scale](#scale), [biological scale](#biological-scale), [ecological organizational level](#ecological-organizational-level), [grain](#grain), [extent](#extent), [support](#support), [aggregation](#aggregation), [upscaling](#upscaling), [downscaling](#downscaling), [cross-scale transformation](#cross-scale-transformation).

**Quantitative semantics:** [variable](#variable), [quantity](#quantity), [quantity kind](#quantity-kind), [unit](#unit), [dimensionless](#dimensionless), [calibration](#calibration), [quality control](#quality-control), [missing value](#missing-value), [uncertainty](#uncertainty), [confidence](#confidence).

**Provenance and harmonization:** [provenance](#provenance), [lineage](#lineage), [entity/activity/agent](#entity-activity-agent), [derivation](#derivation), [transformation](#transformation), [harmonization](#harmonization), [standardization](#standardization), [normalization](#normalization), [semantic equivalence](#semantic-equivalence), [numeric convertibility](#numeric-convertibility), [scientific comparability](#scientific-comparability), [AI-ready data](#ai-ready-data), [representation](#representation), [embedding](#embedding), [core harmonization](#core-harmonization), [track-specific harmonization](#track-specific-harmonization), [evidence](#evidence), [source-documented evidence](#source-documented-evidence), [observed evidence](#observed-evidence), [deterministically derived evidence](#deterministically-derived-evidence), [model judgment](#model-judgment), [human decision](#human-decision), [needs evidence](#needs-evidence), [semantic gap](#semantic-gap).

## Semantic infrastructure

### ontology { #ontology }

A formally structured account of entities, relations and constraints in a domain.

**Why it matters:** Its commitments can support logical inference; a list of labels alone cannot.

**Related:** [controlled vocabulary](#controlled-vocabulary), [knowledge graph](#knowledge-graph).

### vocabulary { #vocabulary }

A set of terms used to describe something.

**Why it matters:** A vocabulary may supply identifiers and definitions without formal axioms.

**Related:** [controlled vocabulary](#controlled-vocabulary), [ontology](#ontology).

### controlled vocabulary { #controlled-vocabulary }

A managed set of permitted terms with documented meanings.

**Why it matters:** Controlled labels reduce variation but do not prove that measurements are comparable.

**Related:** [thesaurus](#thesaurus), [standard](#standard).

### thesaurus { #thesaurus }

A managed vocabulary with broader, narrower and associative links, often multilingual.

**Why it matters:** Thesaurus broader is not automatically logical subclass.

**Related:** [broader / narrower](#broader-narrower), [SKOS](#skos).

### classification { #classification }

A scheme assigning things to named categories.

**Why it matters:** Categories can serve a reporting purpose without describing every entity relation.

**Related:** [taxonomy](#taxonomy), [ontology](#ontology).

### taxonomy { #taxonomy }

A system for classifying organisms, or more generally a classification hierarchy.

**Why it matters:** Biological taxonomies are versioned scientific opinions, not one immutable organism ladder.

**Related:** [taxon](#taxon), [taxon concept](#taxon-concept).

### knowledge graph { #knowledge-graph }

An interconnected set of assertions about identified things.

**Why it matters:** A graph can use an ontology, but instance assertions and ontology definitions are different products.

**Related:** [ontology](#ontology), [instance](#instance).

### semantic model { #semantic-model }

A structured description of meanings and relationships used by an application or community.

**Why it matters:** It may be conceptual rather than an executable formal ontology.

**Related:** [conceptual model](#conceptual-model), [schema](#schema).

### conceptual model { #conceptual-model }

A high-level account of important entities and how they relate.

**Why it matters:** A diagram does not necessarily supply formal predicates or inferencing rules.

**Related:** [semantic model](#semantic-model), [axiom](#axiom).

### schema { #schema }

A structural contract for fields, types and constraints in a data format.

**Why it matters:** Passing a schema validates structure, not the scientific truth of a record.

**Related:** [standard](#standard), [semantic model](#semantic-model).

### standard { #standard }

A community-agreed specification, such as an exchange format, checklist or terminology.

**Why it matters:** A standard need not be an ontology and compliance need not imply harmonization.

**Related:** [ontology](#ontology), [standardization](#standardization).

### concept { #concept }

An identified meaning used to organize or describe knowledge.

**Why it matters:** One label can express different concepts and one concept can have several labels.

**Related:** [identifier](#identifier), [label](#label).

### class { #class }

A category whose instances satisfy a specified meaning or definition.

**Why it matters:** A class of organisms is distinct from a particular observed organism.

**Related:** [instance](#instance), [subclass / is-a](#subclass-is-a).

### instance { #instance }

A particular thing represented as belonging to a class.

**Why it matters:** A particular tree is not the class tree or a taxon name.

**Related:** [class](#class), [organism](#organism).

### identifier { #identifier }

A persistent reference used to distinguish an entity or concept.

**Why it matters:** Stable identity survives label changes; version and authority still matter.

**Related:** [URI / IRI](#uri-iri), [label](#label).

### URI / IRI { #uri-iri }

A globally structured identifier; IRIs permit a wider character repertoire than URIs.

**Why it matters:** An HTTP identifier may resolve to documentation, but resolution alone does not establish semantic correctness.

**Related:** [identifier](#identifier), [definition](#definition).

### label { #label }

Human-readable text associated with an identifier.

**Why it matters:** Identical labels do not establish equivalence; different labels do not establish difference.

**Related:** [synonym](#synonym), [concept](#concept).

### synonym { #synonym }

An alternative designation associated with a term under a stated synonym policy.

**Why it matters:** Exact, related and historical synonyms have different implications.

**Related:** [label](#label), [mapping](#mapping).

### definition { #definition }

A statement specifying what a concept means.

**Why it matters:** Compare definitions, entity types, methods and support rather than matching labels alone.

**Related:** [axiom](#axiom), [semantic equivalence](#semantic-equivalence).

### axiom { #axiom }

A formal assertion or constraint used in an ontology's logical model.

**Why it matters:** Reasoner conclusions depend on these commitments and their consistent application.

**Related:** [relation](#relation), [subclass / is-a](#subclass-is-a).

### relation { #relation }

A specifically defined connection between identified things.

**Why it matters:** Part-of, member-of, subclass and broader are different relations.

**Related:** [part-of](#part-of), [member-of](#member-of).

### subclass / is-a { #subclass-is-a }

A class-inclusion relation: every instance of the narrower class is an instance of the broader class.

**Why it matters:** This is not physical containment or population membership.

**Related:** [part-of](#part-of), [broader / narrower](#broader-narrower).

### part-of { #part-of }

A relation between a whole and a constituent, under a specified mereological definition.

**Why it matters:** A leaf can be part of a plant; that does not make leaf a subclass of plant.

**Related:** [member-of](#member-of), [relation](#relation).

### member-of { #member-of }

A relation linking an individual to a collection or group.

**Why it matters:** An organism can belong to a population without being a physical anatomical part of it.

**Related:** [population](#population), [part-of](#part-of).

### broader / narrower { #broader-narrower }

Concept-scheme links expressing more general and more specific meanings.

**Why it matters:** In SKOS these links do not by themselves assert OWL class inclusion.

**Related:** [subclass / is-a](#subclass-is-a), [SKOS](#skos).

### equivalent { #equivalent }

The same relevant meaning under an explicit semantic regime and scientific context.

**Why it matters:** A strong equivalence claim requires evidence, versioning and appropriate review.

**Related:** [semantic equivalence](#semantic-equivalence), [numeric convertibility](#numeric-convertibility).

### alignment { #alignment }

A documented set of proposed relationships between semantic systems.

**Why it matters:** Alignment can include broader, narrower or related links, not just equivalence.

**Related:** [mapping](#mapping), [crosswalk](#crosswalk).

### mapping { #mapping }

An evidenced assertion relating a source concept to a target concept.

**Why it matters:** It must preserve the source identity and state relationship, uncertainty and review status.

**Related:** [alignment](#alignment), [harmonization](#harmonization).

### crosswalk { #crosswalk }

A maintained collection of mappings between schemas, vocabularies or classifications.

**Why it matters:** A crosswalk may be lossy, contextual and version-specific.

**Related:** [mapping](#mapping), [provenance](#provenance).

### semantic interoperability { #semantic-interoperability }

The ability to exchange and interpret information while retaining relevant meaning.

**Why it matters:** Readable files or matching field names are insufficient.

**Related:** [harmonization](#harmonization), [schema](#schema).

### upper ontology { #upper-ontology }

A model of very broad categories such as objects, processes and qualities.

**Why it matters:** It provides foundational commitments rather than all domain terms.

**Related:** [domain ontology](#domain-ontology), [application ontology](#application-ontology).

### domain ontology { #domain-ontology }

An ontology describing a scientific or practical subject area.

**Why it matters:** Its intended scope is a strength and a boundary, not a universal failure.

**Related:** [upper ontology](#upper-ontology), [semantic composition](#semantic-composition).

### application ontology { #application-ontology }

An ontology assembled or specialized for a defined task or application.

**Why it matters:** Its useful assumptions may be inappropriate elsewhere.

**Related:** [domain ontology](#domain-ontology), [ontology profile](#ontology-profile).

### ontology import { #ontology-import }

An explicit mechanism for incorporating another ontology's axioms or modules.

**Why it matters:** A citation or similar coverage is not evidence of an actual import.

**Related:** [axiom](#axiom), [semantic composition](#semantic-composition).

### ontology profile { #ontology-profile }

A documented selection of semantic resources, patterns and constraints for a purpose.

**Why it matters:** A profile composes community work without replacing every source ontology.

**Related:** [semantic composition](#semantic-composition), [mapping](#mapping).

### semantic composition { #semantic-composition }

Building a meaning from explicitly related concepts and constraints supplied by several resources.

**Why it matters:** Composition requires compatible relations and evidence; juxtaposed labels are insufficient.

**Related:** [entity-quality model](#entity-quality-model), [I-ADOPT decomposition](#i-adopt-decomposition).

### entity-quality model { #entity-quality-model }

A pattern expressing a quality of a specified entity, potentially with further context.

**Why it matters:** A quality alone cannot specify which entity, method or support was measured.

**Related:** [quality](#quality), [phenotype](#phenotype).

### I-ADOPT decomposition { #i-adopt-decomposition }

A variable description using property, object of interest, optional matrix/context and constraints.

**Why it matters:** The framework does not supply every domain concept, unit, method or observation model.

**Related:** [object of interest](#object-of-interest), [matrix](#matrix).

### SKOS { #skos }

A W3C framework for representing concept schemes, labels and semantic links.

**Why it matters:** It can represent a thesaurus without imposing all the axioms of a domain ontology.

**Related:** [thesaurus](#thesaurus), [broader / narrower](#broader-narrower).

## Biological organization

### biological entity { #biological-entity }

A biological thing or collection identified under a stated scientific model.

**Why it matters:** An organism, taxon concept, population and anatomical part are not interchangeable entities.

**Related:** [organism](#organism), [taxon](#taxon).

### organism { #organism }

An individual living entity identified at an appropriate level for the study.

**Why it matters:** A tree observation concerns an individual, not automatically its species or the plot community.

**Related:** [taxon](#taxon), [population](#population).

### taxon { #taxon }

A taxonomic grouping recognized under a classification or taxon concept.

**Why it matters:** A taxon is distinct from its name and from an ecological population.

**Related:** [taxon name](#taxon-name), [taxon concept](#taxon-concept).

### taxon name { #taxon-name }

A nomenclatural designation applied under a naming code.

**Why it matters:** The same name can have different circumscriptions in different taxonomic treatments.

**Related:** [taxon concept](#taxon-concept), [identifier](#identifier).

### taxon concept { #taxon-concept }

A taxon's circumscription according to an identified treatment, authority or version.

**Why it matters:** A name match without the treatment may hide scientific differences.

**Related:** [taxon name](#taxon-name), [mapping](#mapping).

### taxonomic rank { #taxonomic-rank }

A category such as species, genus or family in a taxonomic system.

**Why it matters:** Rank is not an organism's size, ecological level or observation support.

**Related:** [taxonomy](#taxonomy), [biological scale](#biological-scale).

### population { #population }

A scientifically specified group of organisms, often sharing taxon, place and time criteria.

**Why it matters:** Population membership and boundaries must be stated; they cannot be inferred from a raster footprint.

**Related:** [community](#community), [member-of](#member-of).

### community { #community }

A study-defined set of populations or organisms considered together in an ecological context.

**Why it matters:** Composition depends on inclusion criteria, location, time and detection methods.

**Related:** [population](#population), [assemblage](#assemblage).

### assemblage { #assemblage }

A set of organisms grouped for a study, often within a selected taxonomic group.

**Why it matters:** Usage differs across communities; state the operational definition.

**Related:** [community](#community), [guild](#guild).

### guild { #guild }

A grouping based on comparable resource use, under a stated ecological definition.

**Why it matters:** Resource-use categories are not necessarily taxonomic or phylogenetic groups.

**Related:** [functional group](#functional-group), [trophic interaction](#trophic-interaction).

### functional group { #functional-group }

Organisms grouped by selected ecological functions or traits.

**Why it matters:** Grouping depends on the chosen function and cannot replace source taxa silently.

**Related:** [guild](#guild), [trait](#trait).

### ecosystem { #ecosystem }

A specified ecological system involving organisms and their physical environment and interactions.

**Why it matters:** Its boundaries and measured properties need explicit study definitions.

**Related:** [community](#community), [environmental system](#environmental-system).

### biome { #biome }

A broad ecological regional grouping characterized by major environmental and biological patterns.

**Why it matters:** Biome classifications differ and are not a universal spatial support scale.

**Related:** [ecosystem](#ecosystem), [classification](#classification).

### habitat { #habitat }

The environmental setting used by an organism or group under a stated definition.

**Why it matters:** A habitat category is not the same as a measured environmental material or a polygon boundary.

**Related:** [environmental system](#environmental-system), [environmental feature](#environmental-feature).

### environmental system { #environmental-system }

An environmental whole described as a system under a particular semantic model.

**Why it matters:** System identity and boundaries must be distinguished from a sampled material.

**Related:** [environmental feature](#environmental-feature), [environmental material](#environmental-material).

### environmental feature { #environmental-feature }

An identifiable environmental feature, such as a landform, in a resource's terminology.

**Why it matters:** A feature may contextualize an observation without being its sampled matrix.

**Related:** [environmental system](#environmental-system), [matrix](#matrix).

### environmental material { #environmental-material }

A substance or material in the environment, such as soil or water.

**Why it matters:** The material containing a measured chemical differs from the surrounding ecosystem.

**Related:** [matrix](#matrix), [context object](#context-object).

## Biological characteristics

### trait { #trait }

A characteristic of a biological entity under a specified trait definition.

**Why it matters:** A trait is not the stored variable name or the value of one measurement.

**Related:** [variable](#variable), [measurement](#measurement).

### attribute { #attribute }

A characteristic used to describe an entity or record.

**Why it matters:** Data-field attributes and biological attributes can have different meanings.

**Related:** [trait](#trait), [property hint](#property-hint).

### phenotype { #phenotype }

An observable characteristic or set of characteristics of an organism in a stated context.

**Why it matters:** Phenotype descriptions depend on entity and conditions; they are not simply genotype labels.

**Related:** [quality](#quality), [entity-quality model](#entity-quality-model).

### quality { #quality }

A characteristic associated with an entity, as defined by the semantic resource in use.

**Why it matters:** Ontology quality differs from data-quality acceptance or uncertainty.

**Related:** [trait](#trait), [quality control](#quality-control).

### behavior { #behavior }

An action or process involving an organism under an explicit behavioral definition.

**Why it matters:** Behavioral categories do not automatically imply ecological interactions or comparable observation protocols.

**Related:** [biotic interaction](#biotic-interaction), [phenotype](#phenotype).

### biotic interaction { #biotic-interaction }

A specified relationship or process involving living entities.

**Why it matters:** Direction, participants, context and source evidence matter.

**Related:** [trophic interaction](#trophic-interaction), [relation](#relation).

### trophic interaction { #trophic-interaction }

An interaction concerning consumption or resource transfer under a stated model.

**Why it matters:** Trophic category assignments may vary with life stage, context and evidence.

**Related:** [guild](#guild), [biotic interaction](#biotic-interaction).

### property hint { #property-hint }

A recorded clue about which property a source describes.

**Why it matters:** A hint is not an accepted canonical property or approved mapping.

**Related:** [observed property](#observed-property), [model judgment](#model-judgment).

## Observation and measurement

### observation { #observation }

An act or record of determining something about a feature or entity.

**Why it matters:** SOSA and OBOE organize observations and measurements differently; preserve the source model.

**Related:** [measurement](#measurement), [feature of interest](#feature-of-interest).

### measurement { #measurement }

A determination of a property's value using a stated procedure and context.

**Why it matters:** A number without entity, property, unit, method and support is not a fully interpretable measurement.

**Related:** [variable](#variable), [uncertainty](#uncertainty).

### observed property { #observed-property }

The characteristic targeted by an observation.

**Why it matters:** Two sensors at the same location may observe different properties.

**Related:** [feature of interest](#feature-of-interest), [quantity kind](#quantity-kind).

### feature of interest { #feature-of-interest }

The entity or feature about which an observation determines a property.

**Why it matters:** In an observation model it can differ from the sample used to access it.

**Related:** [object of interest](#object-of-interest), [sample](#sample).

### object of interest { #object-of-interest }

The entity whose property defines a variable in I-ADOPT.

**Why it matters:** Its semantic role is variable-specific, not a fixed label for an entire dataset.

**Related:** [matrix](#matrix), [I-ADOPT decomposition](#i-adopt-decomposition).

### matrix { #matrix }

The entity or material in which the object of interest is situated for a variable description.

**Why it matters:** A chemical concentration in water is not the same variable as concentration in soil.

**Related:** [environmental material](#environmental-material), [object of interest](#object-of-interest).

### context object { #context-object }

An additional entity supplying context to a variable description.

**Why it matters:** Context helps distinguish otherwise similar variables without replacing the object of interest.

**Related:** [matrix](#matrix), [I-ADOPT decomposition](#i-adopt-decomposition).

### sample { #sample }

A selected entity, portion or proxy used to learn about a feature of interest.

**Why it matters:** A material sample and an observation's spatial sampling support need separate descriptions.

**Related:** [specimen](#specimen), [spatial support](#spatial-support).

### specimen { #specimen }

A particular collected or preserved biological entity or material under a collection model.

**Why it matters:** A specimen can support many observations; it is not the observation event itself.

**Related:** [sample](#sample), [observation](#observation).

### occurrence { #occurrence }

Evidence of an organism or taxon at a place and time under a recording convention.

**Why it matters:** An occurrence record does not necessarily estimate abundance or sampling completeness.

**Related:** [event](#event), [taxon](#taxon).

### event { #event }

A contextual occurrence or activity grouping observations under a specified data model.

**Why it matters:** Event identity does not by itself define survey design or detection probability.

**Related:** [survey](#survey), [inventory](#inventory).

### inventory { #inventory }

A survey-derived account of entities observed within an explicit scope.

**Why it matters:** Inventory completeness requires effort and detection context, not just a species list.

**Related:** [survey](#survey), [community](#community).

### survey { #survey }

A planned observation effort using a sampling design and scope.

**Why it matters:** Different survey designs can make similar-looking results incomparable.

**Related:** [protocol](#protocol), [sampling](#sampling).

### sampling { #sampling }

The selection or creation of samples according to a design.

**Why it matters:** Sampling design links observations to inference targets and must survive harmonization.

**Related:** [sample](#sample), [protocol](#protocol).

### protocol { #protocol }

A specified procedure for carrying out an observation or experiment.

**Why it matters:** Protocol identity and version can alter measurement meaning even when units match.

**Related:** [method](#method), [measurement](#measurement).

### method { #method }

The documented approach used to obtain or derive a result.

**Why it matters:** A method label may be less specific than a reproducible protocol.

**Related:** [protocol](#protocol), [calibration](#calibration).

### sensor { #sensor }

An instrument or system used to determine a property.

**Why it matters:** A sensor is distinct from the platform carrying it and the property it measures.

**Related:** [platform](#platform), [observed property](#observed-property).

### platform { #platform }

A host or carrier for sensing equipment, such as a satellite.

**Why it matters:** The satellite identity is not the same as instrument or processing level.

**Related:** [sensor](#sensor), [provenance](#provenance).

## Scale and support

### spatial extent { #spatial-extent }

The geographic domain covered by a dataset or study.

**Why it matters:** A scene boundary does not specify the support of each pixel value.

**Related:** [spatial support](#spatial-support), [footprint](#footprint).

### spatial resolution { #spatial-resolution }

A stated measure of spatial detail or sampling spacing under a source convention.

**Why it matters:** Pixel spacing can differ from the effective sensor footprint or averaging support.

**Related:** [spatial support](#spatial-support), [grain](#grain).

### spatial support { #spatial-support }

The spatial domain or weighting over which a reported value applies.

**Why it matters:** A plot average and a satellite pixel are not equivalent because their centers overlap.

**Related:** [footprint](#footprint), [aggregation](#aggregation).

### footprint { #footprint }

The spatial area associated with an observation, sensor response or extracted window.

**Why it matters:** A bounding box may approximate the footprint without defining the full response function.

**Related:** [spatial support](#spatial-support), [spatial extent](#spatial-extent).

### CRS { #crs }

A coordinate reference system defining how coordinates relate to Earth or another reference frame.

**Why it matters:** Native raster CRS differs from the CRS used to publish geographic footprints.

**Related:** [location](#location), [footprint](#footprint).

### location { #location }

A position or geometry associated with a thing or observation.

**Why it matters:** A coordinate alone does not establish resolution, extent or support.

**Related:** [CRS](#crs), [spatial support](#spatial-support).

### temporal extent { #temporal-extent }

The overall period covered by a dataset or study.

**Why it matters:** A year's coverage does not mean each value represents a yearly average.

**Related:** [temporal support](#temporal-support), [interval](#interval).

### temporal resolution { #temporal-resolution }

The time detail, spacing or cadence stated by a source.

**Why it matters:** Daily reporting does not prove daily averaging or complete daily coverage.

**Related:** [temporal support](#temporal-support), [timestamp](#timestamp).

### temporal support { #temporal-support }

The instant, interval or temporal weighting represented by a value.

**Why it matters:** An instantaneous acquisition and a daily mean differ even on the same date.

**Related:** [instant](#instant), [temporal extent](#temporal-extent).

### timestamp { #timestamp }

A recorded time marking an event or record under a stated convention.

**Why it matters:** One timestamp may indicate acquisition, publication or interval midpoint; inspect its role.

**Related:** [temporal resolution](#temporal-resolution), [temporal support](#temporal-support).

### instant { #instant }

A zero-duration temporal position under an explicit observation model.

**Why it matters:** Equal start/end acquisition times must not be turned into invented durations.

**Related:** [interval](#interval), [temporal support](#temporal-support).

### interval { #interval }

A period with temporal boundaries.

**Why it matters:** An interval's boundaries do not automatically tell whether observations are averaged or sampled within it.

**Related:** [instant](#instant), [aggregation](#aggregation).

### scale { #scale }

A family of distinct properties describing organization, support, resolution, extent or analysis.

**Why it matters:** Scale is not one universal ladder and its meaning must be specified.

**Related:** [biological scale](#biological-scale), [support](#support).

### biological scale { #biological-scale }

A study-specific description of biological organization or processes.

**Why it matters:** Molecular, anatomical, taxonomic and ecological organization intersect rather than forming one ranking.

**Related:** [ecological organizational level](#ecological-organizational-level), [scale](#scale).

### ecological organizational level { #ecological-organizational-level }

A category such as organism, population, community or ecosystem under an ecological model.

**Why it matters:** It is not automatically a spatial grain or taxonomic rank.

**Related:** [population](#population), [spatial resolution](#spatial-resolution).

### grain { #grain }

The size or detail of sampling or analysis units under an explicit usage.

**Why it matters:** Different disciplines use grain differently; document whether it means support, spacing or another property.

**Related:** [spatial resolution](#spatial-resolution), [support](#support).

### extent { #extent }

The overall domain considered in space, time or another specified dimension.

**Why it matters:** Always state the dimension rather than using extent as a synonym for resolution.

**Related:** [spatial extent](#spatial-extent), [temporal extent](#temporal-extent).

### support { #support }

The domain, membership or weighting represented by an observation or statistic.

**Why it matters:** A support transformation is a scientific decision, not merely file-format conversion.

**Related:** [spatial support](#spatial-support), [temporal support](#temporal-support).

### aggregation { #aggregation }

Combining observations using a specified grouping, weighting and statistical rule.

**Why it matters:** A mean can change support and uncertainty; provenance must retain that change.

**Related:** [upscaling](#upscaling), [transformation](#transformation).

### upscaling { #upscaling }

A stated transformation from one support or resolution to a coarser or broader one.

**Why it matters:** The statistical and scientific assumptions must be justified for the target use.

**Related:** [aggregation](#aggregation), [cross-scale transformation](#cross-scale-transformation).

### downscaling { #downscaling }

A stated transformation to finer support or resolution, often requiring a model.

**Why it matters:** Finer output cells do not create new independent observations.

**Related:** [upscaling](#upscaling), [model judgment](#model-judgment).

### cross-scale transformation { #cross-scale-transformation }

A transformation connecting distinct organizational levels, supports or analysis scales.

**Why it matters:** A leaf-to-pixel relationship needs explicit scientific justification, not a chain of labels.

**Related:** [support](#support), [derivation](#derivation).

## Quantitative semantics

### variable { #variable }

A specified characteristic represented in data, ideally with entity, property and context.

**Why it matters:** The same column name can represent different quantities and methods.

**Related:** [trait](#trait), [measurement](#measurement).

### quantity { #quantity }

A property that can be expressed by magnitude under a measurement system.

**Why it matters:** The quantity being measured is distinct from a numeric value and its chosen unit.

**Related:** [quantity kind](#quantity-kind), [unit](#unit).

### quantity kind { #quantity-kind }

A category of comparable quantities under a stated quantity system.

**Why it matters:** Equal dimensions alone do not make all quantities the same kind.

**Related:** [unit](#unit), [variable](#variable).

### unit { #unit }

An agreed reference used to express a quantity value.

**Why it matters:** Convertible units do not establish biological meaning or variable equivalence.

**Related:** [dimensionless](#dimensionless), [numeric convertibility](#numeric-convertibility).

### dimensionless { #dimensionless }

Having no physical dimension in the stated quantity system; often expressed with unit 1.

**Why it matters:** Different dimensionless quantities can have entirely different meanings.

**Related:** [unit](#unit), [quantity kind](#quantity-kind).

### calibration { #calibration }

A documented relationship used to relate an instrument's encoded or indicated values to a target quantity.

**Why it matters:** Scale and offset must come from source evidence; applying them does not prove ecological validity.

**Related:** [quality control](#quality-control), [transformation](#transformation).

### quality control { #quality-control }

Explicit checks and selection rules used to assess or filter data for a purpose.

**Why it matters:** A passed mask predicate is not universal proof of scientific suitability.

**Related:** [calibration](#calibration), [uncertainty](#uncertainty).

### missing value { #missing-value }

An explicit absence or unavailability of a value, including documented sentinels.

**Why it matters:** Zero can be a valid value or nodata depending on source evidence.

**Related:** [quality control](#quality-control), [needs evidence](#needs-evidence).

### uncertainty { #uncertainty }

A documented characterization of limited knowledge about a result or decision.

**Why it matters:** Measurement uncertainty, model confidence and missing evidence are different things.

**Related:** [confidence](#confidence), [measurement](#measurement).

### confidence { #confidence }

A stated assessment of certainty under an explicit interpretation.

**Why it matters:** An agent or curator score is not automatically a calibrated probability or measurement uncertainty.

**Related:** [uncertainty](#uncertainty), [model judgment](#model-judgment).

## Provenance and harmonization

### provenance { #provenance }

Information about the entities, activities and agents involved in producing a result.

**Why it matters:** Recorded history enables inspection but does not prove the activity was scientifically justified.

**Related:** [lineage](#lineage), [derivation](#derivation).

### lineage { #lineage }

The chain of input identities and transformations leading to a product.

**Why it matters:** Streaming hashes preserve evidence identity without reconstructing discarded observations.

**Related:** [provenance](#provenance), [transformation](#transformation).

### entity/activity/agent { #entity-activity-agent }

PROV categories for things, production/use activities and responsible actors.

**Why it matters:** A scientific concept, its measurement and the software producing a result play different roles.

**Related:** [provenance](#provenance), [instance](#instance).

### derivation { #derivation }

A relationship recording that a product depends on another entity or result.

**Why it matters:** A recorded derivation does not validate the scientific assumptions used.

**Related:** [transformation](#transformation), [provenance](#provenance).

### transformation { #transformation }

A specified operation producing a new result from inputs.

**Why it matters:** Scientific changes require versioned recipes and review; preprocessing has a separate identity.

**Related:** [derivation](#derivation), [normalization](#normalization).

### harmonization { #harmonization }

An evidenced process making data suitable for a stated joint interpretation while preserving source meaning and differences.

**Why it matters:** It can require conversion, explicit noncomparability or abstention; it is not automatic universal equivalence.

**Related:** [standardization](#standardization), [scientific comparability](#scientific-comparability).

### standardization { #standardization }

Conformance to a specified naming, structure, unit or procedural standard.

**Why it matters:** Standardized fields can still encode different scientific meanings.

**Related:** [harmonization](#harmonization), [standard](#standard).

### normalization { #normalization }

A context-dependent adjustment such as numerical scaling or structural normalization.

**Why it matters:** State whether it changes scientific meaning or is model preprocessing; the word alone is ambiguous.

**Related:** [transformation](#transformation), [embedding](#embedding).

### semantic equivalence { #semantic-equivalence }

An evidenced claim of the same relevant meaning under stated resources, versions and context.

**Why it matters:** Label similarity, shared units and spatial overlap are insufficient.

**Related:** [equivalent](#equivalent), [scientific comparability](#scientific-comparability).

### numeric convertibility { #numeric-convertibility }

The existence of a supported mathematical conversion between numeric expressions, such as units.

**Why it matters:** A valid conversion does not establish that two variables measure the same thing.

**Related:** [semantic equivalence](#semantic-equivalence), [calibration](#calibration).

### scientific comparability { #scientific-comparability }

Suitability of observations for a specified scientific comparison under reviewed assumptions.

**Why it matters:** Meaning, methods, support, time, uncertainty and rights can all matter.

**Related:** [semantic equivalence](#semantic-equivalence), [support](#support).

### AI-ready data { #ai-ready-data }

Data with explicit structure, meanings, rights, provenance and interfaces suitable for a stated computational use.

**Why it matters:** A numeric vector alone does not guarantee scientific suitability or universal model understanding.

**Related:** [representation](#representation), [embedding](#embedding).

### representation { #representation }

A machine-usable encoding of harmonized observations under an identified method.

**Why it matters:** Representation preprocessing is distinct from scientific harmonization.

**Related:** [embedding](#embedding), [provenance](#provenance).

### embedding { #embedding }

A numeric representation generated by a specified encoder and preprocessing contract.

**Why it matters:** Shared vector dimensions do not imply a universal latent space or native LLM interpretation.

**Related:** [representation](#representation), [AI-ready data](#ai-ready-data).

### core harmonization { #core-harmonization }

Reviewed transformations whose assumptions are explicitly shared across applicable tracks.

**Why it matters:** Promotion to the core requires scientific review; one track cannot impose its interpretation on others.

**Related:** [track-specific harmonization](#track-specific-harmonization), [harmonization](#harmonization).

### track-specific harmonization { #track-specific-harmonization }

Reviewed transformations scoped to a particular scientific question or track.

**Why it matters:** Shared sources do not make track-specific rules universally valid.

**Related:** [core harmonization](#core-harmonization), [scientific comparability](#scientific-comparability).

### evidence { #evidence }

An identified source, observation, deterministic derivation or explicitly classified judgment supporting a claim.

**Why it matters:** Evidence identity and scope matter more than a model's confident wording.

**Related:** [source-documented evidence](#source-documented-evidence), [model judgment](#model-judgment).

### source-documented evidence { #source-documented-evidence }

A statement or annotation explicitly supplied by a source, retained with its location and resource identity.

**Why it matters:** An adapter's inferred description must not silently become a source statement.

**Related:** [observed evidence](#observed-evidence), [evidence](#evidence).

### observed evidence { #observed-evidence }

Evidence actually encountered in data, with a declared observation or window scope.

**Why it matters:** An extracted window hash does not cover the entire remote asset.

**Related:** [source-documented evidence](#source-documented-evidence), [lineage](#lineage).

### deterministically derived evidence { #deterministically-derived-evidence }

Evidence produced by a specified reproducible rule from identified inputs.

**Why it matters:** A parser-derived fact remains distinct from a direct source annotation.

**Related:** [evidence](#evidence), [transformation](#transformation).

### model judgment { #model-judgment }

An interpretation proposed by a model and recorded with model/prompt/output provenance.

**Why it matters:** It can be wrong and must not be promoted to source metadata or automatic approval.

**Related:** [human decision](#human-decision), [confidence](#confidence).

### human decision { #human-decision }

A recorded person's explicit review outcome tied to exact scientific content.

**Why it matters:** A pending review is not an approval; local records do not authenticate identity by themselves.

**Related:** [model judgment](#model-judgment), [provenance](#provenance).

### needs evidence { #needs-evidence }

A state indicating that a required claim lacks adequate evidence.

**Why it matters:** Missing information is not automatically a demonstrated scientific failure.

**Related:** [evidence](#evidence), [semantic gap](#semantic-gap).

### semantic gap { #semantic-gap }

A documented unmet meaning, relation or representation need in a defined comparison.

**Why it matters:** A local gap is a research question, not proof that no ontology anywhere addresses it.

**Related:** [semantic composition](#semantic-composition), [cross-scale transformation](#cross-scale-transformation).
