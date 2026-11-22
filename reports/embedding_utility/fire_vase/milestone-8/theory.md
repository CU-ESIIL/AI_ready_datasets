# What these experiments can establish mathematically

Let X be retained native observations, M the permitted sidecar, S=f(X) the
validated scientific state and Z=e(S) a fixed learned encoding. Let Y=q(X) be a
scientific query. Training data and fitted parameters are held fixed in these
statements. Different prediction training regimes remain separate comparisons.

## Information cannot be added by deterministic encoding

Every answer computed as h(Z,M) can also be computed from (X,M) by composing
h(e(f(X)),M). Thus the unrestricted answer class from native input contains the
embedding answer class. Learned features can still improve a *restricted* learner,
finite-data regularization, search metric or serving implementation. Better
linear-head prediction therefore does not imply that new information appeared.
The relevant comparison is accuracy and complete cost against a specified native
implementation, not a general assertion about what an agent could compute.

## Exact answerability is a fiber condition

For exact recovery by a decoder, q(x) must be constant for every pair x,x' with
the same supplied interface. Under A this requires e(f(x))=e(f(x')) to imply
q(x)=q(x'). Under B compare pairs with the same (Z,M), and under C include the
observations actually retrieved. A single counterexample disproves exact
answerability for that interface. Successful approximate probes cannot prove it.
The six-point state collision supplies a counterexample for general cumulative
paths. It does not disprove short one/two-point cumulative answerability.

## Normalized scale loss is an exact counterexample

For positive increments a, allocation a/sum(a) is invariant under a→c*a for
positive c, whereas observed total changes by c. A one-point allocation is always
[1]. No deterministic allocation-only decoder can recover arbitrary absolute
totals. Actual one/two-point payload collisions show that this is present in the
lake, not just a hypothetical construction. Original sidecars can distinguish
records, but source-value lookup must then be explicit and costed.

For squared error, the best unrestricted population decoder of a supplied
interface U is its conditional mean, with residual risk E[Var(Y|U)]. This is a
mathematical identity, not an estimated ecological Bayes-error curve in this run.
Identical allocation payloads with different totals force nonzero residual error
for those empirical cases when U supplies no distinguishing information.

## Invertibility is different from geometry

A full-rank linear change of coordinates may be invertible while changing
Euclidean distances. PCA coordinates plus a declared inverse can retain the
numerical state, yet coordinate nearest neighbors need not match a particular
native-property ranking. A trained scalar head changes both metric and label
access; its performance is not zero-shot coordinate geometry. Rank13 here is a
numerical covariance fact about engineered input, not a biological latent-space
dimension or the number of native measurements.

## A workload-specific break-even condition

For fixed preparation cost F and average serving cost c under a specified query
mixture, the component-sum lifecycle is C(Q)=F+Q*c. An embedding with larger fixed
cost beats a native implementation only if c_native>c_embedding and
Q>(F_embedding-F_native)/(c_native-c_embedding), subject to an acceptable error
constraint. If it also has larger serving cost, repeated queries alone do not
create a break-even. Refresh, index, fallback and model-update costs add terms;
a workload or accuracy change requires a new comparison.

For this measured scalar bundle the exact-native route is cheaper and exact,
so reuse does not rescue the tested learned routes. This does not extend to
unmeasured geometry/sequence queries or production workloads. Storage is another
axis: comparing different precision, retaining shared sources and supporting
short minimal raw representations all matter. No universal storage/economic
bound was estimated.

## First graphs to extend

The measured rank/recovery, dimension and learning curves, property-retrieval
curves, query/gallery scaling and cost–error frontier separate information loss,
metric mismatch and implementation cost. The next stronger theory test would
choose a scientifically reviewed query absent from S, then compare a raw-sequence
encoder with validated native operations and same-information nonlinear controls.
That would test a new representation hypothesis; this run must not be relabeled
as if it already tested it.
