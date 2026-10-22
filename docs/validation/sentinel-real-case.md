# Prepare the real Sentinel case for expert review

The retained case is `S2B_13TDE_20230715_0_L2A:B08`. Historical QA requested revision; the
original report and model criticisms remain unchanged. This analysis cannot lift
a veto or create human approval.

## What software checked

Native raster CRS is EPSG:32613; geographic footprint coordinates use EPSG:4326.
The native band coefficients are scale 0.0001 and offset −0.1, and acquisition
support is instantaneous. The recipe's calibration and rename operations are
registered. These checks do not establish downstream scientific suitability.

## What the objections mean now

The native-CRS objection is technically supported and needs corrected proposal
wording. The [official Sentinel legal notice](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice)
provides evidence for lawful distribution/modification and required notices, but an
expert still needs to bind terms and attribution to the intended product.

The demand for a whole-raster checksum is unsupported by this project's bounded
streaming contract: metadata and window hashes intentionally have narrower scopes.
That does not prove remote immutability. Preserve the criticism and adjudicate
residual integrity risk explicitly. Do not download an entire raster to satisfy an
unsupported interpretation of provenance requirements.

Historical evidence pointers are not valid under the later strict source-pointer
validator. Rebuild evidence and repeat reviews, rather than editing the historical
model outputs. Independent quality criteria and any inferential claim need expert
acceptance and appropriate independent data.

| Issue | Jurisdiction | Current resolution path |
| --- | --- | --- |
| `semantic.b08_reflectance_quantity` | semantic | Prior review PASS preserved; no promotion to human approval. |
| `units.b08_reflectance_calibration` | units | Native asset coefficients match recipe; verify processing-baseline/offset convention at source. Do not apply a second global offset. |
| `support.native_epsg_mismatch` | support | A new proposal must distinguish native raster EPSG:32613 from footprint EPSG:4326; preserve historical prose unchanged. |
| `rights.terms_missing` | rights | Official Sentinel legal notice now inspected: lawful reproduction, distribution and modification permitted with required notices and limitations; expert must bind intended vector use and attribution to this case. |
| `integrity.recipe_content_digest_match` | integrity | Verify content binding without treating metadata digest as raster hash. |
| `integrity.metadata_only_checksum` | integrity | The demand for whole-raster hashing is not an existing streaming requirement; retain explicit metadata/window hash scopes, source/version evidence and assess residual remote-mutation risk. Expert must adjudicate veto rather than erase it. |
| `quality.calibrated_reflectance_validation` | quality | Define intended exploratory-versus-inferential use, SCL eligibility, uncertainty and independent target criteria; do not require an undefined universal analysis-ready label. |
| `evidence.pointer_validation` | governance | Rebuild evidence pointers and repeat the scoped review; never repair historical outputs. |
| `layout.encoder.consensus` | governance | Specify a bounded raster layout and encoder configuration, then obtain reviews for that exact content. |
| `historical.qa.veto` | governance | Preserve veto; expert adjudication and new reviewed proposal are required. |

## Expert decision package

[Machine-readable issue ledger](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/outputs/scientific_validation/sentinel_review_gap_analysis.json)
retains original findings, cited/current evidence, classification, technical support,
software/documentation/expert requirements, execution necessity and proposed action.
The [version-2 draft recipe](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/outputs/scientific_validation/sentinel_proposed_recipe.json)
adds a correction proposal while preserving old proposals and the original consensus veto. Its old content digest intentionally remains stale, so deterministic QA blocks execution until renewed review.

Use the [per-issue decision form](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/outputs/scientific_validation/expert_decision_template.json)
to approve, reject, revise or request evidence. Every choice is initially null.
This form is **not** a runtime `HumanDecision`; execution still requires matching
fresh consensus, scoped evidence review, resolved vetoes and an explicit exact-recipe
human decision. Any scientific edit invalidates the corresponding approval.
