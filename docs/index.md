# AI-ready biological and environmental datasets

Can a scientific question drive discovery of heterogeneous observations, bounded
agent proposals, governed harmonization, and reusable machine representations
without losing scientific meaning or provenance?

This repository tests that hypothesis with a small local prototype. Agents propose;
allow-listed deterministic software executes approved recipes. Three independent
modules provide discovery/access, harmonization, and representation generation.

The working demonstration uses **synthetic** field vegetation height and satellite
reflectance at deliberately coincident locations and times. Food and water security
are configuration namespaces, not validated scientific models. No external data is
downloaded by that default fixture demo. An optional [real-data workflow](real-data-agents.md)
now retrieves actual Sentinel pixels and runs four model-backed proposal roles
through local Ollama. Proposals remain subject to QA and human review; the first
current real proposal was rejected and has not transformed data.

Start with the [complete example](examples.md), read the [architecture](architecture.md),
and check [what is working, mocked, and planned](PROTOTYPE_STATUS.md).

```text
Question → Discovery → Source resources
                              ↓
             Semantic proposals → Recipes → QA / review
                              ↓
                 Deterministic harmonization
                              ↓
              Immutable shared observations
                              ↓
                   Independent track views
                              ↓
               Modality-specific representations
                              ↓
                  Downstream science + provenance
```
