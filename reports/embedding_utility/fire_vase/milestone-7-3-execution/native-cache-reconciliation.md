# Native/cache reconciliation

**CURRENT REAL OBSERVATIONS — internal-use outputs; no model training or publication performed.**

Fresh complete-container hashes match all four recorded identities. Native daily
records: 627,033; cached daily: 626,102. Overlap: 626,102 unique event-date keys;
native-only: 931; cache-only: zero. Overlap native `dy_ar_km2` versus cache
`ring_area_km2`: zero exact numeric-value-hash mismatches, with no tolerance tuning.

**All 931 unmatched records belong to 296 native IDs absent from the native event
catalog.** No catalog fire loses a daily observation relative to this native source.
The native daily ID population is 278,865, while catalog/cache are 278,569. These
numbers reconcile rather than forcing all sources to use the catalog denominator.

Native integer IDs are converted to decimal strings only for the documented
upstream key crosswalk; native feature row IDs and cache row offsets are retained.
Source hashes fix the release identity. No equivalence of unrelated products is
inferred. The build code’s inner join on event ID explains the omission pattern;
it is implementation evidence, not approval to invent catalog metadata for the
296 IDs. `population-summary.json` retains omitted-record years and membership.

For cache comparisons, original historical results reproduce: 278,569 fires,
626,102 rows, 196,611 exact-day pairs, 150,922 longer gaps, strict ≥3/5/7 histories
10,246/2,887/1,171. Native all-ID results differ: 196,982 exact pairs, 151,186 longer
gaps and strict ≥3/5/7 histories 10,260/2,891/1,172. These scope differences are
reported explicitly. Missing/zero/duplicate/invalid records are zero in both decoded
streams, not assumed from historical reports. Absence of observation dates is not
zero growth; 263,312 unobserved days lie between native records.

The compact SQLite index contains hashes and source/date/key references, not daily
measurement values. Catalog totals and derived observed-sum area strata remain
distinct. Cached cumulative finite counts do not turn final totals into increments.
