# Scientific feasibility and candidate splits

**CURRENT REAL OBSERVATIONS — internal-use outputs; no model training or publication performed.**

No predictive model or held-out performance was evaluated. Split files are
**proposals**, not reviewed/approved scientific evaluation plans. Existing primary
metric definitions and unknown scientifically meaningful effects remain unchanged.

The compact split index assigns each source fire ID once using SHA256 seed20260828:
70% train, 15% validation, 15% test, using a split-specific hash namespace independent
of the learning-fraction hash. Every prefix/run from a fire inherits its group;
SQL uniqueness and independent tests verify split isolation. Candidate temporal
blocks are train≤2013, selection2014–2016, calibration2017–2018 and test2019–2021.
Unknown event years are excluded from year-based folds. Geographic group labels
support leave-one-reported-region-out candidates; no region was selected using
outcome performance. Region-specific completeness and small groups require review.

| Input/future days | Candidate train fires | Validation fires | Test fires |
| --- | ---: | ---: | ---: |
| 3/1 | 13,266 | 2,887 | 2,851 |
| 3/3 | 4,980 | 1,062 | 1,075 |
| 7/3 | 1,290 | 297 | 272 |
| 14/7 | 157 | 39 | 28 |
| 30/7 | 18 | 8 | 1 |

`learning-curve-sizes.csv` provides exact nested 1%,3%,10%,30%,100% candidate training
counts for every native/cache depth/horizon, with the same held-out IDs at every
fraction. Hash-based subsampling is a learning-curve sensitivity, not the primary
all-eligible training cohort. Actual final folds must preserve the protocol's
selection/calibration separation and be frozen before model evaluation.

Short-depth tasks offer substantial independent-fire replication. Depth14/horizon7
has only 28 candidate test fires; depth30/horizon7 has one. Those are sparse for
multi-region/year/size subgroup claims or capacity/tuning comparisons. No universal
minimum acceptable sample threshold is invented. Higher-level independent clusters
may be fewer still; prefixes and future outcomes remain correlated within fires.
Median/max windows per fire and geographic/year strata are measured in the CSVs.

## Preliminary power-planning inputs, not empirical power

We now have true fire/run/window counts and cluster sizes. Paired model-loss variance,
minimum scientifically meaningful effects, cluster dependence and training variability
remain unknown. Therefore empirical predictive power and a numerical minimum
detectable scientific effect are not reported. Under an explicitly hypothetical
independent-fire normal approximation, a standardized paired detectable difference
would scale as (z_(1-alpha/2)+z_power)/sqrt(n_test), not 1/sqrt(n_windows). That formula
requires a justified design, multiplicity family and variance before numerical use.

Task A uses depth3/horizon1. B/C/D use depth3/horizon3 as candidate mathematical
support. C compares supported future versus observed historical growth reference;
its scientific decision criterion needs to stay separate from mean successive
future differences. D can use future population SD. E proposes depth3/horizon7
future-pattern query/gallery support. Query/gallery fires must be disjoint; same-fire
candidates are forbidden. Relevance cannot be defined by embedding coordinates,
and future-pattern similarity is not validated ecological analog discovery.

The 296 unmatched native IDs permit source-native support analysis but lack catalog
strata. Report both all-native and catalog/cache-matched populations; do not silently
attach guessed metadata. Model labels, outcome evaluation and training remain off.
