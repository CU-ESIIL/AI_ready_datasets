# Semantic comparison review template

Use this reusable record after identifying a concrete source and candidate target.
[Download the YAML template](semantic_review_template.yaml), fill actual evidence,
and follow the [review workflow](review-workflow.md). Unfilled values remain unknown;
no reviewer or approval is supplied by the template.

| Field group | Required scientific content |
| --- | --- |
| Source concept | Exact identifier, semantic resource, version, definition, source field, evidence location and source metadata digest |
| Scientific context | Question/domain, biological organization, entity, property, matrix/context, spatial/temporal support, native CRS, method/protocol, units and quantity kind |
| Candidate target | Exact identifier, resource/version, definition and retrieval basis |
| Proposed relationship | Explicit direction and Module 2 relationship code; unknown is permitted |
| Evidence | Type, source, location, statement and content digest, with scope |
| Differences and loss | Distinctions the proposed mapping might obscure or discard |
| Review | Actual reviewer/date, confidence with interpretation, decision, missing evidence and human notes |

The source group corresponds to `SemanticEvidence`; the candidate group corresponds
to `ConceptCandidate`. A reviewed proposal can inform Module 2's `SemanticMapping`
and recipe. The template is deliberately non-executable: it does not bypass
source rights, deterministic QA, model vetoes or exact-content human approval.
