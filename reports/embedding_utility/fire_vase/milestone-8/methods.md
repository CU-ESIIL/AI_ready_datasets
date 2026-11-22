# Manuscript methods

## Population, source and scientific support

We used every native ID in the verified Fire VASE daily GeoPackage: 278,865 fires
and 627,033 rows. The population contains 161,200 one-observation fires, 47,992
two-observation fires and 69,673 histories with at least three observations.
These are lengths of retained observed histories, not physical fire lifetimes.
The native population includes 296 IDs absent from the event catalog; they remain
in the primary analysis with unknown catalog attributes. Source containers and
selected source identities are bound by SHA-256, with fresh postflight hashes.
Native values, dates, row IDs and versions remain unchanged. No geometry,
environmental join or calibration was introduced. Measurement quality,
uncertainty and operational observation availability are unknown.

A deterministic native reader groups sorted native rows under a bounded per-fire
limit. Derived model matrices are subsequently held in memory. This is not a
fully streaming optimizer or a throughput benchmark of the complete raster lake.
No raw or harmonized observation arrays are persisted by this experiment.

## References and defined properties

Ten mathematical properties define the scientific state: retained-increment sum;
observation count; first and last retained increments; population standard
deviation; first-increment allocation; mean change over exact consecutive-day
pairs; strict interior maxima over exact consecutive triples; allocation in the
first floor(n/2) retained observations; and elapsed first-to-last observed span.
Sum/count/first/last/SD/span use log1p preprocessing, pair change uses asinh;
allocation and extrema use their declared direct values. Raw-unit references are
retained separately and independently recalculated from native rows. Native
sums are also checked with exact rational arithmetic in the feature recipe.

SD and allocation are undefined at n=1. Pair change is undefined without an
exact one-day pair, and maxima are undefined without a consecutive triple.
Missing days are never filled with zero growth. First-half allocation describes
observation index, not half a physical lifetime. A single record has observed
elapsed span zero; that does not imply instantaneous fire lifetime. The retained
increment cumulative series is not complete physical fire area. Mathematical
support masks are not sensor-quality flags. `property-eligibility.csv` gives
all eligible and undefined populations, including the fixed test population.

The scientific state discards absolute date origin and general longer sequence
ordering before neural encoding. Its ten scalar fields and support masks cannot
answer arbitrary sequence questions. The raw first/last/total fields *do* suffice
for retained cumulative sequences of length one or two. A six-point state
collision with different cumulative paths is independently unit-tested.

## Splits, preprocessing and capacity

A preserved whole-fire hash split assigns 194,980 training, 41,894 validation and
41,991 test IDs. Independent deterministic hash thresholds select 1%, 3%, 10%,
30% and 100% of training fires. Evaluation IDs remain fixed. All preprocessing,
PCA and downstream-head fitting use training fires only; no test fitting or
hyperparameter selection occurs. Existing public development data are not a
pristine prospective held-out sample.

Undefined *model input* fields use training-only medians plus ten actual support
bits; scientific labels retain undefined masks. The resulting model input has
20 columns. Native observations and missing source days are never imputed.
R0 performs independently validated native operations. R1 retains the raw-unit
interpretable scientific state; its model preprocessing view is distinct.

PCA is fitted on training covariance at requested dimensions 4/8/16/32/64,
capped to numerical rank. Neural encoders use a 20→16→d tanh architecture and a
linear objective head, with d=4/8/16/32/64, 12 epochs, batch size 1024, Adam
learning rate .003, clipping at 5 and seed 20260828. Count-supervised training
uses observation count alone; multitask uses total/count/SD with masked SD;
self-supervision autoencodes all 20 preprocessed state channels, including
support bits and input fillers. This is state autoencoding, not masked native
observation prediction. The three objectives have 1/3/20 output channels and
different supervision. Width is fixed, but capacity and objective computation
are not identical. Dimensions 32/64 are overcomplete relative to hidden width16.
`checkpoint-inventory.json` records encoder and objective-head parameter counts.

Seventy-five primary neural fits cover all fractions/dimensions/objectives.
Additional direct, blocked, forecast and lifecycle-update controls are separately
identified. Probes use standardized ridge or a fixed-seed 32-feature tanh map
with ridge. Same-label raw-state probes and direct all-target neural models are
controls. Nonlinear probes are finite-capacity diagnostics, not proofs of
recoverability by arbitrary nonlinear functions. All reported recovery is
model-dependent unless a native/deterministic inverse operation is specified.

## Information access and retrieval

A gives only coordinates (and explicitly declared trained decoders); B supplies
the same original date/source/support sidecar to every representation; C invokes
an explicit native fallback. Date-derived count/span are validated independently.
A stronger B sensitivity fits the same count/first-date/span/max-gap features
and masks alongside every representation. Source IDs are lineage keys, not hidden
native-value lookup features. C recovery is credited to native operations.

Five retrieval rubrics rank similarity in total, variability, first share,
consecutive change and elapsed span using independent scalar native references.
Relevance is the native kth-neighbor cutoff, including ties, with a 1e-8
normalized numerical comparison tolerance. It is not an ecological equivalence
rubric. Exact native precision is one; recall can be below one because the
relevant tie set may contain more than ten members. Whole-fire gallery/query
isolation and explicit same-ID exclusion are enforced.

The fixed test query sample has 4,096 IDs: 1,365/1,365/1,366 in the 1/2/3+
strata. Task eligibility further restricts queries and galleries. Galleries use
all eligible training fires, up to 194,980. Both the balanced-query estimate and
post-stratification to eligible native test-fire proportions are retained.
Coordinates, trained linear/nonlinear heads and deterministic PCA inverse are
distinct routes. Full-rank state preservation does not imply Euclidean metric
fidelity. Rank correlations use all eligible sampled queries against a fixed
independent-hash 1,024-fire diagnostic gallery, explicitly separate from full
gallery top-10 retrieval. Scaling measures area retrieval on galleries of
1,000/10,000/50,000/194,980 with 128/1,024/4,096 nested queries.

## Transfer, uncertainty and secondary prediction

Frozen downstream heads test different properties from encoder objectives;
trained heads are not zero-shot. Temporal refits train on source-reported years
through 2016, reserve 2017–18 and test 2019–21. Geographic refits withhold the
reported west region, training on other known regions. Unknown attributes remain
in primary results but cannot enter unsupported blocked strata. These coarse
source regions are not verified ecological support units. Fixed dimension16
blocked refits are a separately recorded extension after random-split results.

Equal-fire losses use supported labels only. The prespecified exploratory family
contains 50 self-supervised-versus-count-supervised linear comparisons: five
dimensions times ten properties. Paired 256-replicate fire bootstraps describe
conditional fixed-model uncertainty; six known-region group aggregates provide
region bootstrap and all 64 sign-flip configurations. Holm adjusts all 50
comparisons. One training seed does not estimate model-fitting variability.
No reviewed minimum scientifically meaningful effect or equivalence margin is
available. Per-year and source-region tables are descriptive strata, not refits.

Secondary retrospective prediction uses exact contiguous depth1/2 prefixes and
horizons1/3/7, grouped by whole fire. Target growth follows the input prefix;
prefix features never include future observations. All available training-fire
windows are used; losses average windows within fire before averaging fires.
Frozen primary encoders had access to complete *training-fire* states, while
direct prefix controls use prefix training data; this extra historical
pretraining information/computation is an explicit asymmetry, not test leakage.
Persistence, training mean, raw linear/nonlinear, PCA, all learned dimensions and
direct neural controls are retained. Forecast claims remain retrospective.

## Lifecycle and audit

The same 4,096-fire workload requests all defined transformed scalar properties
under common B metadata. Actual source preparation, fitting, full encoding,
materialization, storage, indexing, fallback and warm query stages are recorded.
Twenty repeated warm vectorized kernels measure batch execution, not request,
network or concurrent service latency. Reuse from one through one million fire
queries is a component-sum scenario, not an empirical million-query run.
Two update cycles per family and unchanged-source refresh/reencoding are measured;
true source updates and physical filesystem I/O bytes remain unknown. Shared
native source/date/provenance storage is retained by every method. Numeric-vector
bytes are not total lake storage; float32 learned vectors and float64 PCA/state
precision are explicitly distinguished.

An eligible-subset probe-centering defect was discovered and corrected. Invalid
initial outputs are retained privately; unchanged encoder weights were reused,
and every affected head/evaluation was rerun. An NA access-table defect was also
corrected. Serving encoding now skips an unused pretext head, with bit-identical
representation validation and a fresh lifecycle measurement. These corrections
are recorded in `probe-correction.json`; they are not scientific test selection.
