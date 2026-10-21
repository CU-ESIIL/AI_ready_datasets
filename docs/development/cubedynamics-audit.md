# CubeDynamics capability audit — 2026-10-21

Inspected the external local checkout at commit
`4c6afea9565b282d40e0de22254ebf2386cced08` (clean at inspection), package metadata,
public namespace, piping, custom/statistical/combining/biology verbs, temporal support,
Sentinel loader, dependency requirements, upstream tests and published website.
[Repository](https://github.com/CU-ESIIL/cubedynamics) ·
[Documentation](https://cu-esiil.github.io/cubedynamics/).

The current repository and package declare **0.1.0rc3**, while the website homepage
still advertises rc1. Treat this as a prerelease API and pin the tested distribution.
CubeDynamics remains an external ESIIL project; no upstream source is copied here.

## Inventory before adapter implementation

| Verified upstream surface | Behavior and integration decision |
| --- | --- |
| `pipe(value)`, `Pipe.unwrap()` | Builds an ordered pipeline and semantic trace; not itself a guarantee of lazy I/O |
| `verbs.apply(func, **kwargs)` | Public callable-stage wrapper; expose only fixed adapter functions, never a model-supplied callable/expression |
| `verbs.mean(dim='time', keep_dim=False, skipna=False)` | Lazy xarray/Dask reduction; unweighted arithmetic mean, not a general daily resampler; expose only with reviewed complete equal-duration interval evidence |
| `verbs.month_filter(months)` | Lazy calendar selection; adapter validates month integers/references before use |
| `verbs.align_time(other, mode='require_exact_support')` | Exact time labels and known identical interval support; no shifting, interpolation or resampling |
| `verbs.align_cube(like=..., spatial_method='nearest', temporal_method='nearest', tolerance='0s')` | xarray spatial interpolation and time reindex; not CRS reprojection; expose same-CRS nearest spatial sampling and exact time only |
| No dedicated public `select`, `clip`, `mask` or generic `resample` verb in this checkout | Fixed xarray select/isel/where stages through public `verbs.apply`; identify adapter glue explicitly, not invented upstream functions |
| `data.load_s2_cube(...)` | Cubo discovery/access, Dask chunks, collection/provenance attributes; do not call it here because Module 1 already owns source discovery and native-window access |
| stackstac / Cubo | Both remain declared dependencies; access behavior depends on the loader, not a universal streaming guarantee |
| `VirtualCube`, streaming internals | Advanced/internal surface with potentially materializing helpers; not exposed in this first adapter |
| Statistical/domain/plot/export/custom-code namespaces | Not exposed; no `run_python`, arbitrary attribute lookup, unrestricted apply, writers or plotting tools |

CubeDynamics uses xarray, Dask and established geospatial libraries for numerical
work. Its source metadata and semantic trace complement this project's source,
recipe, review, rights and representation lineage; they do not decide ontology
equivalence or scientific validity. Upstream `align_cube` does not enforce CRS or
scientific support compatibility itself, so the adapter must do so before calling it.

## Dependency boundary

The existing temporary test environment uses Python 3.14 / NumPy 2; CubeDynamics
requires NumPy <2. Test it separately under Python 3.12 and keep the integration
optional so core semantic review remains independently usable. Install the actual
external distribution, not a replacement implementation or fixture-only mock.
