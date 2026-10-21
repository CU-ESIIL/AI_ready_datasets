# Concepts

AI-ready data retain the scientific context needed to interpret and reuse values:
units, methods, biological entities, observational support, quality, source rights,
and a reproducible transformation history. A vector alone does not supply that context.

**Multimodal** describes different ways of observing a system, such as field
measurements, traits, sensors, fluxes, imagery, gridded products, or text.
**Multiscale** describes spatial and temporal support, such as organism, plot,
site, landscape, hourly, seasonal, or annual. Many datasets do not necessarily
constitute many modalities. Matching coordinates does not establish equal support.

Core harmonization contains conservative reusable operations: explicit unit
conversions, WGS84 coordinate validation, missing-value normalization, or verified
identifier mapping. Track harmonization contains application-specific selection,
aggregation, neighborhoods, metrics, and interpretation. The contract rejects
filtering, joins, and support-changing operations in core recipes. Promotion of a
track assumption requires a separately reviewed scientific decision and implementation;
there is no automatic promotion path.

Human-governed autonomy means that agents may abstain and propose decisions, QA may
reject them, and consequential uncertainty must reach a human. A human approval
cannot turn an unknown relationship into an explicit equivalence; revise the
mapping with evidence first.

Representations are machine products derived from validated observations. Model
preprocessing is recorded separately from scientific harmonization. Modality-specific
vectors stay separate; this prototype makes no universal embedding claim.
