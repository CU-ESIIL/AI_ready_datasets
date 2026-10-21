# Semantic landscape source data

This directory contains a growing curated resource inventory, not ontology graphs
or scientific observations. It includes formal ontologies, standards, classifications,
vocabularies, conceptual frameworks and unresolved historical leads. No claim of
exhaustiveness or universal ontology is made.

`semantic_resources.csv` is canonical. Resource facts (name, resource kind, reference
URLs, documented origin, rights and verification scope) are separated from explicit
project assessments (coverage, candidate role, overlap, limitations, historical
interpretation). `assessments.jsonl` records assessment, reviewer, date, evidence,
confidence and notes. The reviewer is the coding assistant, not a domain expert.
Provisional assessments require scientific review. Unknowns are recorded, not guessed.

The website master table and coverage matrix are generated from these files.
Coverage uses strong/partial/indirect/not_target; unknown is retained for unresolved
resource identities. Scores are metadata diagnostics, not measured ontology quality,
term alignment, biological equivalence or scientific compatibility.

Access during this pass: official documentation pages via web browsing and the OBO
Foundry registry metadata, streamed into bounded memory for factual verification.
No ontology graph or source dataset is downloaded. Registry metadata is not treated
as permission to redistribute ontology content. Resource licenses remain specific;
unknown licenses require review before reuse. Inventory text is original paraphrase;
reference URLs and factual metadata retain their source citations.
