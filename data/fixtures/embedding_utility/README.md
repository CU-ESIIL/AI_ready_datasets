# Synthetic Fire VASE utility fixtures

Project-authored CC0-1.0 synthetic numbers; no real fires, coordinates, provider
observations or scientific validation claims. `scripts/generate_embedding_fixture.py`
rebuilds `histories.json` and `tasks.json` deterministically without network access.

There are 24 explicitly training fires and 10 evaluation edge cases. Original ISO
dates and km2/km2/day units are preserved. Explicit missing rows and omitted calendar
dates both create unknown daily increments; observed zero increments remain zero.
The zero baseline is evidenced only when explicitly supplied. Unknown availability
timestamps do not establish operational forecast support. Source checksums cover
metadata; per-history and fixture hashes provide separate canonical-content evidence.

`tasks.json` contains 29 versioned task specifications, not expert scientific gold.
Exact/profile references are independently computed; analog relevance is unavailable.
PCA artifacts are fitted during each run on training fires only and are never refit
per question. See the website's Fire VASE benchmark documentation for boundaries.

`milestone-3-v3/` is the separate expanded synthetic cohort: 32 training, eight
development and 20 evaluation histories, 30 development and 120 evaluation questions.
Seed/source/license and checksum scope are explicit. Model-unseen evaluation cases
are visible to developers; general scientific claim rubrics remain drafts, not expert
gold. M1 files above are unchanged. See the expanded pilot protocol in
`reports/embedding_utility/fire_vase/agent-protocol-m3-v1.md`.
