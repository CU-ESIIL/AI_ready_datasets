# Data management workbench

**PROTOTYPE — executable local operations, generated scientific diagnostics.**
The workbench connects existing discovery metadata, scientific contracts and
MOSAIKS outputs to an immutable artifact index, portable registries, local file
distribution, cohort feedback, resource accounting and tested recovery. It does
not replace the three independently callable scientific stages or MESA discovery.

![Local scientific artifacts, SQLite index, UI, resource plans and preservation boundary.](assets/figures/management.svg)

*Project-authored diagram; [maintained source](https://github.com/CU-ESIIL/AI_ready_datasets/blob/main/scripts/generate_figures.py).
OSN/NDP/TACC are planned deployment boundaries, not connected services.*

## Start and inspect

From the repository root, install the existing `dev,embeddings` extras, then:

```sh
prototype management-demo --output run/amber-workbench --metadata-records 10000
prototype workbench --registry run/amber-workbench/registry --port 8787
```

To exercise more actual generated harmonization/encoding work, choose a new run:

```sh
prototype management-demo --output run/management-256 --windows 256 --features 512
```

Window counts are bounded to 32–1,024 in multiples of four; features follow the
existing MOSAIKS 16–4,096 even-dimension contract. The generated layout stays within
its source bounds, with half training and one quarter each validation/test. Actual
local timings are useful for regression, not estimates of remote global throughput.

Open `http://127.0.0.1:8787/`. The command fails if the output already exists;
choose a new output name to preserve earlier evidence. The scientific demo runs
32 generated windows through actual harmonization and MOSAIKS (128 features),
train-only empirical filter fitting and held-out numeric verification. No source
observations, models or ontology graphs are downloaded. Native LLM understanding
and independent ecological validity remain unestablished.

The workbench has release, planned-product, source, semantic-resource/assessment,
recipe, review, dataset, encoder, group, allocation, measured-usage, service,
preservation, feedback and scale-test views. Selecting a record reveals its
versioned upstream/downstream references and integrity-checked files. The three
product definitions (forest bioresources, cropland food, watershed water) remain
planned and require scientific definitions. They do not activate a third science
track or turn one diagnostic dataset into three scientific datasets.

## Durable files and registries

```text
run/amber-workbench/
  demo_manifest.json
  dataset/                    # existing native MOSAIKS bundle, generated inputs
  registry/
    registry.sqlite3          # indexed metadata, immutable identities and links
    blobs/<prefix>/<sha256>   # deduplicated representation/encoder/verification files
  registries/
    source.jsonl, mapping.jsonl, recipe.jsonl, context.jsonl
    semantic_resource.jsonl, semantic_assessment.jsonl, semantic_profile.jsonl
    operation_registry.jsonl, review.jsonl, run.jsonl
    encoder.jsonl, verification.jsonl, dataset.jsonl, release.jsonl
    product.jsonl, workspace.jsonl, service.jsonl, allocation.jsonl
    usage.jsonl, feedback.jsonl, benchmark.jsonl, preservation.jsonl
    provenance.jsonld         # PROV-inspired metadata derivations, not equivalences
    schemas/*.json
    export_manifest.json      # export counts, file checksums and controlled scope
  preservation/
    snapshot/                 # records.jsonl, manifest.json, checked blob copies
    restored/                 # actually restored SQLite/CAS index, not just a plan
```

Only kinds present in a run are exported. The demo does not invent an actual
human decision; `human_decision.jsonl` appears only when an existing decision is
registered/imported. Model transcripts remain in their original review workflows;
no model calls or fabricated responses are produced by this demo. The generated
six-domain review deliberately reports missing independent scientific evidence;
it cannot authorize execution. Diagnostic feature generation uses the existing
explicit generated-data path, not this unresolved scientific-release review.

The native bundle contains `vectors-*.npy`, `records.jsonl`,
`harmonization_context.json`, `manifest.json`, `encoder/{filters.npy,encoder.json,training_context.json}`,
`verification_labels.jsonl`, `verification.json`, an optional fitted
`verification_probe.npz`, and `dataset_card.md`. Registration rechecks the existing
scientific gates, encoder identity, row/shard hashes, geographic/split leakage and
held-out diagnostics using a private representation-only copy. It does not modify
the input bundle. Raw and harmonized arrays are never indexed or persisted.

## Independent commands

```sh
prototype management-seed --registry run/index
prototype management-register source source.json --title "Existing source evidence" --registry run/index
prototype management-import run/mosaiks-example --registry run/index
prototype management-check --registry run/index
prototype management-export --registry run/index --output run/portable-registries
prototype management-scale --registry run/index --records 10000
prototype management-snapshot --registry run/index --output run/local-snapshot
prototype management-restore run/local-snapshot --output run/restored-index
```

`management-register` accepts existing typed source, semantic, recipe, review,
human-decision, workspace, service, allocation and usage metadata. Generated
records require explicit `--fixture`. Registration stores evidence; it grants no
execution or release authority. Python `prepare_release` creates only a
`diagnostic` or `needs_scientific_release_review` record. There is no automatic
scientific publication, approval, DOI assignment or cloud write.

## Contracts, identity and visibility

`ArtifactRecord` identities bind kind, payload, fixture/track/visibility, parents
and blob references; creation timestamps are retained separately. Re-registration
is idempotent. Existing parents are required, so references form an insertion DAG.
Shared artifacts may support separate tracks; cross-track derivation is rejected
without a separately reviewed scientific association. Generated inputs cannot be
reclassified as real dataset, release, context, encoder or verification products.
Public children cannot expose controlled parent records. Files are content-addressed
and copied with byte limits and exclusive publication; repeated imports reuse
the same bytes. Fixity is not adversarial authentication or evidence of scientific truth.

The local operator UI can inspect controlled records. `/api/catalog` returns only
public metadata; the demo intentionally does not publish its dataset/release.
Local snapshots/exports include controlled records and must not be uploaded to a
public site automatically. New directories use restrictive permissions, but the
prototype has no encryption or authenticated multi-user access control.

## API and feedback

| Route | Behavior |
| --- | --- |
| `GET /api/summary` | Observed local index/blob bytes and artifact counts |
| `GET /api/artifacts?kind=recipe&track=...&limit=30&after=...` | Keyset pagination; 1–100 records/page |
| `GET /api/artifacts/<id>` | Metadata and parent/child links; up to 100 children |
| `GET /api/catalog` | Public metadata projection only |
| `GET /api/datasets/<id>/rows?offset=0&limit=16` | 1–32 feature vectors and exact row lineage; float32 inputs, JSON numerical response |
| `GET /api/blobs/<id>/<registered-name>` | Checked files, ETag and single HTTP byte ranges |
| `POST /api/feedback` | Issue bound to exact artifact/version and a known group |

Feedback fields are `target_id`, `group_id`, `category`, `summary`, and `detail`.
Categories are semantics, harmonization, representation, rights, or interface.
Issues remain open and never approve recipes, modify sources, resolve vetoes or
start jobs. Scientific revision continues through existing review contracts and
new immutable products. No approval or arbitrary-execution endpoint exists.

The server binds IPv4 loopback only, checks Host/Origin, accepts bounded JSON
feedback and emits a restrictive content security policy. It is for a trusted
single-user development environment, not an Internet service. No tokens, network
discovery, remote credentials, executable plugins or automatic fallback paths are added.

## Groups, resource plans and measured scale

Nine planned workspace records model three governance groups in Years 1–2 and
six synthesis groups in Years 2–3. Their 2 TB/5 TB quotas are estimates, not
reserved disks. The aggregate 36 TB plan needs a suitable shared-storage award.
Three allocation records preserve source URLs and planning units: 50,000 GB OSN,
600,000 Jetstream2 development CPU SUs and 40,000 GB active workspace. None is
requested or awarded; production, persistent services, GPU experiments, protection
and post-award retention need separate measured requests/agreements.

The optional 1–100,000-record probe measures generated metadata insertion time,
a bounded page query and SQLite file bytes. This is actual local indexing work,
not synthetic global-raster throughput or ACCESS scaling evidence. Demo usage
records distinguish wall/process CPU seconds and record counts from provider billing.
Summary bytes distinguish unique stored files from references to shared bytes.

## Recovery, tests and remaining work

Local snapshots record exact artifact IDs, metadata/blob checksums and a manifest
digest. Restore validates file bounds, record counts, content identity, parent
dependencies and file hashes into a fresh index. Demo recovery happens before its
preservation-result record, so the restored snapshot intentionally lacks that later
record. Failures are retained; they are not promoted as successful deposits.

Offline tests cover parent integrity, byte deduplication, track isolation, generated
classification, controlled/public visibility, review-only releases, corruption,
unsafe paths, input non-mutation, schema export, actual recovery, API issue limits,
Host checks and bounded range downloads. Run `pytest -q tests/test_management.py`.

Remaining production work includes authenticated role/group approval, scientific
release adjudication, persistent identifiers, distributed queues and array indexes,
larger-than-4,096-row bundle verification, schema migrations, lifecycle enforcement,
scheduled backup/recovery, remote S3 adapters and confirmed MESA/iRODS/NDP/TACC
deployments. This local storage layer is not a copied remote infrastructure stack.

[Scientific gates](review/index.md) · [MOSAIKS](mosaiks-embeddings.md) ·
[Architecture](architecture.md) · [Generated schemas](reference/contracts.md)
