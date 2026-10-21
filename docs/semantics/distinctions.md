# Distinctions that protect scientific meaning

These contrasts are deliberately prominent. They guide review; they are not a new
universal ontology. Consult each source community's definitions and versions.

!!! important "Organism ≠ taxon ≠ population ≠ community"
    An individual tree, a taxonomic grouping, a study-defined population and a
    community composition describe different entities or collections. A taxon name
    is another distinct thing. [Definitions](glossary.md#organism).

!!! important "Trait ≠ variable ≠ measurement"
    A trait describes a characteristic. A variable specifies what a dataset records.
    A measurement determines a value in a method/support context. For example,
    leaf area, a column describing leaf area and one measured area are related,
    but not interchangeable. [Definitions](glossary.md#trait).

!!! important "Location ≠ resolution ≠ support ≠ extent"
    A coordinate locates an observation. Pixel spacing describes one aspect of
    resolution. Support describes the domain represented by a value. Extent describes
    total coverage. A scene bounding box cannot supply every pixel's true support.
    [Scale and support](scale-support.md).

!!! important "Timestamp ≠ temporal resolution ≠ temporal support ≠ temporal extent"
    Acquisition time, reporting cadence, averaging interval and a dataset's overall
    period answer different questions. Instantaneous observations can have equal
    start/end times; no duration is invented. [Definitions](glossary.md#timestamp).

!!! important "Same unit ≠ same variable"
    Unit `1` can describe many unrelated dimensionless quantities. Length in metres
    does not establish that plant height, leaf length and water depth are the same
    variable. [Quantitative semantics](glossary.md#unit).

!!! important "Standardized ≠ harmonized"
    A standard can make field names or formats consistent while methods, meanings
    and supports remain different. Joint scientific interpretation needs evidence.
    [Definitions](glossary.md#harmonization).

!!! important "Ontology ≠ knowledge graph"
    An ontology describes categories, relations and constraints. A knowledge graph
    can contain instance assertions using that ontology. A graph assertion is not
    automatically a valid scientific conclusion. [Definitions](glossary.md#ontology).

!!! important "Ontology ≠ vocabulary ≠ standard"
    A managed term list, an axiomatized domain model and an exchange specification
    provide different capabilities. The [landscape](landscape.md) deliberately
    includes all these kinds of resource.

!!! important "Scale is not one dimension"
    Structural, taxonomic, ecological, spatial, temporal and observational organization
    intersect. Their links have different meanings. [Biological organization](biological-organization.md).

!!! note "Relations also need their own meanings"
    `subclass`, `part-of`, `member-of` and SKOS `broader` are not synonyms. A leaf
    can be part of an organism; an organism can be a member of a population; a
    species can occupy a rank within a taxonomic classification. These are
    different assertions. [Relation glossary](glossary.md#relation).
