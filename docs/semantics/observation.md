# Observation and measurement

An interpretable observation needs more than a number: what entity or feature was
studied, what property was targeted, how the result was obtained, and which support
and context it represents. Different community models organize those elements differently.

## Compare models without declaring them equivalent

[OBOE](https://github.com/NCEAS/oboe) organizes observations, measurements, entities,
characteristics, standards and protocols. [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/)
models observations, sensing, sampling, procedures, results and features of interest.
These are useful structures with different commitments. A field called observation
in two systems does not automatically denote the same class or event structure.

[BCO](landscape.md#bco) addresses biological collection and sampling activity;
[OBI](landscape.md#obi) describes investigations and experimental procedures.
[Darwin Core and Humboldt](landscape.md#humboldt) supply exchange terms and inventory
context. Exchange compliance and ontology-model compatibility remain separate questions.

## Compose a variable's meaning

[I-ADOPT](https://www.rd-alliance.org/wp-content/uploads/2024/12/I_ADOPT_recommendations.pdf)
provides a way to describe a property, object of interest, matrix, context and
constraints. A concentration in water needs a different matrix description from
concentration in tissue. Domain resources can identify the chemical, material and
biological context. The framework does not replace all units, instruments, methods
or geographical metadata; those need complementary resources.

## Preserve the source model

Module 1 records declared concepts and source paths, with explicit evidence kinds.
The `SemanticEvidence` contract permits partial records. Missing methods or ontology
identifiers stay missing. Parser-derived normalized metadata is classified separately
from a direct native annotation. Model-proposed hints remain `MODEL_JUDGMENT`.

Module 2 compares definitions, entity types, methods, units and support, then proposes
a reviewed relationship. Module 3 sees the resulting harmonized observation contract,
not an assumption that all observation models are interchangeable.

[Glossary](glossary.md#observation-and-measurement) · [Pipeline implementation](pipeline.md)

!!! note "An observation is not necessarily a measurement"
    A measurement quantifies a property under a method. Observation models may also represent categorical observations and sampling context. [Read the distinctions](distinctions.md).
