# Representation generation

`representations.run(observations, encoder="scalar")` accepts a batch or iterator
of validated `HarmonizedObservation` contracts and yields immutable representations.
`batches(observations, size=64)` supplies a bounded batching interface. Discovery
and MESA are absent from this module.

Two deterministic local encoders demonstrate substitutability:

| Config name | Encoder identity | Features | Model preprocessing |
| --- | --- | --- | --- |
| `scalar` | `identity-scalar`, version 1 | `[value]` | None; scientific units retained |
| `squared` | `scalar-and-square`, version 1 | `[value, value²]` | Append square, no scaling |

Every vector records observation identifiers, modality, encoder/version,
preprocessing, dimensionality, track, and complete source/recipe/review lineage.
Missing values, unknown encoders, malformed contracts, nonfinite vectors, and
inconsistent dimensionality fail. Field and satellite vectors remain separate.
The encoders do not change scientific units or perform concealed harmonization.

[Rolf et al. (2021), MOSAIKS](https://pmc.ncbi.nlm.nih.gov/articles/PMC8292408/)
provides the precedent of computing reusable image features once for many tasks.
The current scalar demo does not implement MOSAIKS or reproduce its results.
Future encoder adapters may support random image features, remote-sensing foundation
models, traits, tabular data, or text; scientific preprocessing still belongs in
recipes and encoder preprocessing must remain explicit.
