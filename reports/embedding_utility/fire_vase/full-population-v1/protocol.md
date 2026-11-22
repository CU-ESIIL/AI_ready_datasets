# Fire VASE benchmark: full observed population is primary

**Current design amendment, 2026-11-21.** The investigator explicitly recentered the
study on the fact that most fires are short. Observed history length is measured;
physical lifetime/extinction is not independently established. This amendment changes
the study emphasis without rewriting the frozen M1–7 or census outputs. It is not
based on held-out predictive performance and does not approve new scientific labels.

## Primary population and weighting

All **278,865 native fire IDs** remain in scope: **161,200 one-observation** (57.81%),
**47,992 two-observation** (17.21%) and **69,673 three-or-more** (24.98%). One/two
histories comprise **75.02%**. The296 IDs absent from the event catalog retain unknown
catalog strata; they are not silently removed. `primary-population.csv` fixes the
measured reference weights.

Report every result separately for1,2 and3+ observations. For tasks supported in all
strata, report equal-fire aggregate loss as sum_s (n_s/N)*mean_loss_s, with uncertainty
at whole-fire and appropriate year/region cluster levels. Also show balanced-stratum
sensitivity to expose differences, explicitly labeled as a different weighting.
Do not weight by prefix/window count. For tasks lacking a meaningful target in a
stratum, report NOT_APPLICABLE and coverage; do not insert zero error or silently
change the denominator. Fire-frequency weights describe the scientific reference
population, not an empirically observed production-query mix.

## Primary tasks and interfaces

Primary tasks are observable-property preservation, source/support semantics,
declared-property retrieval, and computational reuse. They do not require an observed
future interval. Relative allocation/order applies to2+ retained observations; a
one-observation record cannot reveal developmental shape, extinction or a future
trajectory. Its observed absolute area, date and provenance remain useful data.
A gappy two-observation record supports a comparison of the two retained increments,
not a complete daily growth trajectory or gap-imputed acceleration label.

| Interface | Primary comparison | Scientific/cost boundary |
| --- | --- | --- |
| Compact native record + indexed access | One/two actual values, original dates and provenance | Optimized native access, not an inefficient full scan per query |
| Minimal interpretable state | First/second observed values, optional observed sum, same support | Retains every short-history source value; extra redundant fields may increase storage |
| Normalized observed allocation control | Relative shares plus exactly the same sidecar | One-value positive histories all map to[1]; scale requires explicit source fallback |
| Classical representation | Dimensions justified against1/2 input values | No PCA fit in this audit; rank/precision and fit/materialization costs must be explicit |
| Learned representation | Train/evaluate on the same information and populations | Not executed here; do not inherit the old minimum-three/consecutive TCN input restriction |
| Adaptive access | Direct/cached/representation route plus recorded fallback | Source lookup restores answerability at its measured cost; routing is not LLM reasoning evidence |

Preserve IDs, original dates, source row references and checksum for every interface.
Evaluate the whole interface: dates/counts survive normalization via the sidecar.
Do not call scale absolutely irrecoverable when the source can be dereferenced.
Report payload-only capability separately from payload+paid source access. Cached
native aggregates and whole-answer caches are strong baselines. A representation
must earn an advantage after those optimizations, with no extra geometry/weather
information offered only to the embedding arm.

## Executed native-value diagnostics

The audit streamed all **627,033 native rows**, independently reconciled population
counts against the census and checked all **209,192 one/two histories**. Native
values and dates/source references are preserved exactly by the short interpretable
state. No completed-fire normalization, final duration or future values were used.
No PCA, neural model, predictor or agent was fitted or called.

For all161,200 one-observation histories, normalized allocation is exactly[1], despite
observed areas ranging from0.2146586733 to37.7799265002 source-reported km². It conveys
no discrimination of absolute observed area by itself. Two-observation normalization
retains relative allocation but lacks its absolute scale. Actual date gaps remain
visible: **17,263 consecutive pairs and30,729 gappy pairs**, all retained in the
primary two-observation stratum. Missing dates were not replaced by zero.

This is an information/access diagnostic, not evidence that a trained embedding is
ineffective. A learned coordinate can still improve a restricted downstream learner
or reuse across tasks. It cannot be credited with extra input information, and
scale-dependent tasks must test that loss explicitly.

## Cost interpretation

The same serialized sidecar is included in native, summary and normalized JSON
byte measurements in `short-history-audit.json`. In this particular encoding the
explicit summary is larger because it duplicates values/sum and uses named fields;
that is not an inherent lower bound on summary encoding. Normalized payloads can
be smaller while requiring a source lookup for scale-dependent queries. Compare
complete preparation, indexes, precision, lookup/cache, refresh and serving costs.

At matching float64 precision, one/two native numerical values require8/16 bytes;
a4–64-coordinate vector requires32–512 numerical bytes before shared metadata or
model/index costs. These are analytical footprints, not trained-vector sizes or an
empirical cost frontier. Quantization and different precision change the comparison
and require their own error checks. An overcomplete vector may still have predictive
value; more coordinates do not establish compression or scientific utility.

128 fixed short-history source-reference lookups reconstructed native values exactly.
They use the existing `fid` primary key and a warm file after streaming. Timing is
retained as a narrow diagnostic, not representative latency, cold-cache performance
or a lifecycle cost claim. The first64 histories per stratum are not a random
population sample. An exact cached-native property-search diagnostic also searched194,980 candidate
training-gallery fires for48 hash-selected test queries across1,2,3+ strata. All48
matched an independent scalar-ranking oracle. This establishes the declared
observable-property lookup operation, not ecological relevance or learned-model
performance. The optimized native and interpretable-total interfaces expose the
same scalar information. Comparative learned retrieval and multi-query/refresh
economics remain unexecuted. Do not present them as measured successes.

## Short-prefix prediction eligibility also includes one/two input observations

The earlier encoder's minimum-three input is not a scientific population rule.
An additional native-run audit now counts depth1 and2 at horizons1/3/7 in
`short-prefix-eligibility.csv`. One input observation followed by one supported
future day is available for **75,953 fires /196,982 dependent windows**. This
includes consecutive pairs in otherwise gappy histories, and the window count
independently matches all native exact-day transitions. These are one-observation
*prefixes* from longer retained histories, not future labels for the161,200 fires
with only one observation in the entire supplied record. Absent future observations
are not zero growth or physical extinction. No predictive outcomes were evaluated.

## Prediction becomes a secondary selected-cohort study

Keep the measured depth×horizon matrix and earlier long-history plans intact, but
label every predictive result with its eligible-fire fraction, observation depth,
size/region/source-quality selection and dependent-window count. A depth3/horizon1
population of19,004 fires is not the all-fire population. Depth30/horizon7 has27.
Their performance cannot be promoted to usefulness for most fires. Separate observed
support from genuine physical duration and operational availability.

The next model experiment should first ask whether compact native data or a minimal
scientific state already suffices for common short-history tasks. Learned vectors
must then show an incremental benefit on the same task/data/cost basis. Strong
native performance, no advantage, or normalization-induced failure are substantive
outcomes rather than excluded cases.

## Status and limitations

WORKING: full-population counts; exact native/short-state preservation and support
checks; normalized-payload information diagnosis; complete JSON byte accounting;
small indexed-fallback check and exact full-gallery native property-search diagnostic.
PLANNED: learned/classical comparisons, comparative representation retrieval rankings,
independent ecological labels and full-workload cost frontiers.
Scientific uncertainty, native QA and availability remain unknown. No source was
modified or raw/harmonized daily measurement dataset persisted or published.
