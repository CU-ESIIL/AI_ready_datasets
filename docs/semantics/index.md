# Discover meaning before interpreting it

Finding environmental data is one discovery problem. Discovering what the source
says those data mean is another. Sources may identify a vocabulary, ontology term,
standard name, taxon, protocol, unit system or community data standard. Those
annotations should survive discovery before anyone proposes harmonization.

The project composes community semantics. It does not replace them with one
universal ontology, a universal biological hierarchy or a universal latent space.

## Start with a question

| If you need to… | Read… |
| --- | --- |
| Understand the scientific stakes | [Why semantics matter](why-semantics.md), [key distinctions](distinctions.md) |
| Explore the landscape | [86-resource inventory](landscape.md), [comparison matrix](comparison.md) |
| Understand terminology | [Glossary](glossary.md) |
| Describe biological organization | [Intersecting biological hierarchies](biological-organization.md) |
| Describe what was observed | [Observation and measurement](observation.md), [scale and support](scale-support.md) |
| Understand how this developed | [Historical evolution](history.md) |
| Examine unresolved science | [Semantic gaps](gaps.md), [proposed profile](profile.md) |
| Use the implementation | [Pipeline integration](pipeline.md), [benchmark diagnostics](benchmark.md) |
| Review a concept relationship | [Human workflow](review-workflow.md), [comparison template](review-template.md) |

## Three stages, different authorities

**Module 1 discovers data and semantic evidence.** It preserves source definitions,
identifiers, annotations and explicit hints. It can retrieve concept candidates.
It does not approve semantic equivalence or execute scientific calibration.

**Module 2 interprets and maps.** Evidence supports a proposed relationship, versioned
recipe, specialist review, deterministic QA and applicable human decision. Similar
labels, convertible units or coincident supports cannot substitute for that review.

**Module 3 represents.** Encoders consume approved harmonized outputs. Encoder
preprocessing and embedding verification remain separate from scientific meaning.

The inventory and matrix are source-maintained project resources. Coverage, candidate
roles and gaps are provisional assessments with reviewer/date/evidence records,
not authoritative claims about external ontologies. The benchmark runs offline over
this inventory and source metadata; it does not evaluate ontology graphs or approve
mappings. Current external ontology-portal integrations remain planned adapter work.

## Compare systems and datasets

[Ontology benchmarking](ontology-benchmarking.md) separates breadth, depth and
composability. [Dataset benchmarking](dataset-benchmarking.md) distinguishes explicit
use, potential, diversity and leverage. Their research frameworks extend beyond the
[working metadata diagnostics](benchmark.md); uncomputed analyses remain explicit.

![Complementary semantic families for biology, environment, observation, variable structure, relations, taxonomy, quantitative context and provenance.](../assets/figures/semantic-landscape.svg)

*Repository-authored conceptual diagram; [maintained source](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/scripts/generate_figures.py). Analytical hypotheses are not measured results.*
