# Fire VASE representation utility — Milestone 8

**WORKING: executed real full-population observed-scientific-state experiment.**
This experiment includes 278,865 native fire IDs and 627,033 daily observations.
It evaluates learned encoding of a validated scientific feature state, rather than
an end-to-end encoder of native polygons or complete observation sequences.

The primary result is negative for the declared scalar-property workload:
validated cached native operations are exact and dominate learned alternatives on
measured cost and error. Learned states retain useful approximate information,
but that information was already available in the input. A small secondary
prediction benefit over linear raw-state heads is similar to a direct neural
control and does not establish operational forecasting skill.

- [Mathematical interpretation](theory.md)
- [Manuscript methods](methods.md)
- [Measured results](results.md)
- [Scientific uncertainty](uncertainty.md)
- [Unsupported claims](unsupported-claims.md)
- [Reproduction and retained artifacts](reproducibility.md)
- [Authorization and provenance](provenance.md)
- [Design recorded before score inspection](preregistered-design.json)
- [Statistical plan](statistical-analysis-plan.json)
- [Checkpoint inventory](checkpoint-inventory.json)
- [Execution manifest](execution-manifest.json)
- [Implementation postflight](validation/postflight.json)

Historical milestones and upstream source data are preserved. Checkpoints,
lineage and working matrices remain under ignored `private/`; this is an internal
analysis, not a redistribution or scientific approval record.
