# Human review of semantic relationships

Review a concrete source concept and proposed target in the context of a scientific
question. A registry hit, broad coverage score or embedding similarity is not an
accepted mapping. Use the [comparison template](review-template.md); retain the
source identifier even if a target mapping is later approved.

## Comparison procedure

| Step | What to record and why |
| --- | --- |
| 1. Identify the source concept | Persistent identifier, resource and version; preserve the exact source value |
| 2. Read its definition | Quote only what rights permit; otherwise cite and paraphrase with a source location |
| 3. Identify its semantic resource | Distinguish a formal ontology, vocabulary, classification or exchange field |
| 4. Retrieve candidate targets | Record identifier, resource, version and match basis; a lexical/model candidate stays a candidate |
| 5. Compare definitions | Look for actual meaning and exclusions; labels and synonyms alone are insufficient |
| 6. Compare entity types | Distinguish organism, taxon, anatomical part, collection, material and process |
| 7. Compare biological organization | State which structural/ecological/taxonomic perspective is intended |
| 8. Compare spatial support | Inspect native CRS, resolution, footprint, membership, weighting and extent separately |
| 9. Compare temporal support | Separate acquisition instant, observation interval, cadence and total coverage |
| 10. Compare methods | Preserve protocol/version, instrument, sampling design, processing and known biases |
| 11. Compare units and quantities | Unit conversion may be possible without variable or biological equivalence |
| 12. Propose a relationship | Equivalent, narrower, broader, related, convertible, derived, incomparable or unknown; explain its direction |
| 13. Record evidence | Classify source documents, observed evidence, deterministic derivations, model judgments and human decisions |
| 14. Record uncertainty | Identify absent evidence and potential loss of meaning; confidence is not automatic permission |
| 15. Escalate unresolved decisions | Consequential/uncertain mappings, support changes, novel equivalence and disagreement need human review |
| 16. Preserve the source concept | Mapping creates a related assertion; it never silently replaces the source identifier or definition |

## Record a proposed relationship precisely

The template is a review artifact, not an executable recipe. Module 2 uses existing
`SemanticMapping` relation codes: `equivalent_to`, `narrower_than`, `broader_than`,
`associated_with`, `convertible_to`, `derived_from`, `not_comparable`, `unknown` or
`requires_human_review` where appropriate. Do not equate `part-of`, `member-of`,
`subclass` and SKOS `broader` while translating a review into a mapping.

Save source/target versions and source-evidence hashes. A scientist must evaluate
uncertainty, restrictions and method/support changes. A mapping alone does not
permit arbitrary transformation code. Supported operations use the allowlist and
versioned recipes; scientific edits invalidate bound reviews and human decisions.

Local records provide an audit trail, not authenticated identity or signatures.
Never fill in an expert name or approval merely to run a pipeline.

## Do we need a new concept?

1. **Does an established resource represent the intended meaning?** Inspect definitions,
   versions and scope. If supported, reuse its identifier without replacing source annotations.
2. **Can the meaning be composed from existing concepts?** Specify entities, property,
   matrix/context, constraints and relations. Validate the composition scientifically.
3. **Could an existing resource be extended appropriately?** Consider its governance,
   scope and an upstream contribution with maintainers. No messages are sent automatically.
4. **Only then consider a project-specific concept.** Record why existing concepts
   failed, alternatives considered, intended definition, relations, reviewer, date,
   evidence and limitations. Expert approval is separate from a coding proposal.

The project does not mint a universal biological ontology because a local query
returned no result. Continue the [cross-support literature review](gaps.md).

## Review the inventory itself

Coverage, candidate status, overlap, limitations and historical influence are project
assessments. Update the canonical CSV and append/version a `ResourceAssessment`
with the actual reviewer/date, evidence, confidence interpretation and notes.
`expert_reviewed` is false for the initial coding-assistant assessments; it can become
true only for an actual expert review. An unknown crosswalk field means not recorded,
not that none exists. Regenerate the website tables and rerun metadata diagnostics
under fresh input hashes after changes.
