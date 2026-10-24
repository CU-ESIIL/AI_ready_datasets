"""Compose scientific artifacts, local release prototypes, resource plans and recovery."""
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import tempfile
from time import perf_counter, process_time
from .asset_registry import AssetRegistry, restore_snapshot, MAX_DOCUMENT_BYTES
from .contracts import digest, recipe_content_digest
from .management_contracts import (
    AllocationPlan, DatasetEntry, FeedbackIssue, PreservationResult, ProductDefinition,
    ReleaseEntry, ScaleProbe, ServiceDefinition, UsageMeasurement, WorkspaceDefinition,
)

PRODUCTS = {
    'forest_bioresources': 'Forest bioresources',
    'cropland_food': 'Cropland food systems',
    'watershed_water': 'Watershed water resources',
}
BASE_FILES = ('manifest.json', 'records.jsonl', 'verification_labels.jsonl',
              'harmonization_context.json', 'dataset_card.md',
              'encoder/filters.npy', 'encoder/encoder.json', 'encoder/training_context.json')


def _json(path):
    if path.is_symlink() or path.stat().st_size > MAX_DOCUMENT_BYTES:
        raise ValueError('bounded regular metadata file required')
    return json.loads(path.read_text())


def import_dataset(registry, directory, *, track=None):
    """Reverify an existing bounded MOSAIKS bundle; never fetch observations/models."""
    from .embedding_dataset import verify_dataset
    from .harmonized_rasters import RasterContext, authorize_context
    from .semantic_discovery import enrich
    directory = Path(directory).resolve()
    manifest = _json(directory / 'manifest.json')
    if manifest.get('status') != 'complete' or not 1 <= manifest.get('records', 0) <= 4096:
        raise ValueError('import requires complete bounded MOSAIKS output (<=4096 rows)')
    context = RasterContext.model_validate(_json(directory / 'harmonization_context.json'))
    fixture = all(s.metadata.fixture for s in context.plan.resources)
    if not fixture and context.plan.reader != 'sentinel-raster':
        raise ValueError('real bundle imports require the existing gated Sentinel raster path')
    context = authorize_context(context)
    if manifest.get('fixture') != fixture or manifest.get('raw_data_persisted') is not False or manifest.get('harmonized_arrays_persisted') is not False:
        raise ValueError('dataset classification/streaming policy mismatch')
    names = list(BASE_FILES)
    for shard in manifest['shards']:
        if not re.fullmatch(r'vectors-[0-9]{5}\.npy', shard['path']):
            raise ValueError('invalid vector shard filename')
        names.append(shard['path'])
    total = 0
    for name in names:
        path = directory / name
        if path.is_symlink() or not path.resolve().is_relative_to(directory) or not path.is_file():
            raise ValueError('dataset files must be regular files within bundle')
        total += path.stat().st_size
    if total > 512 * 1024 * 1024:
        raise ValueError('dataset exceeds bounded import byte budget')
    # Verify a private representation-only copy: do not modify the caller's bundle.
    with tempfile.TemporaryDirectory(dir=registry.root) as temporary:
        scratch = Path(temporary)
        for name in names:
            target = scratch / name
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(directory / name, target)
        verification = verify_dataset(scratch, scratch / 'verification.json', max_records=4096)
        names.append('verification.json')
        if verification.get('probe_file'):
            names.append('verification_probe.npz')
        refs = {}
        for name in names:
            suffix = Path(name).suffix
            media = {'.json': 'application/json', '.jsonl': 'application/x-ndjson',
                     '.npy': 'application/x-npy', '.npz': 'application/x-npz', '.md': 'text/markdown'}[suffix]
            refs[name] = registry.store_blob(scratch / name, name=name.replace('/', '__'), media_type=media)
        shared = []
        with registry.transaction():
            for source in context.plan.resources:
                entry = registry.put('source', source.dataset, source.model_dump(mode='json'),
                                     fixture=source.metadata.fixture)
                shared.append(entry.artifact_id)
                profile = enrich(source).semantics
                semantic = registry.put('semantic_profile', 'Source semantic evidence: ' + source.asset_id,
                                        profile.model_dump(mode='json'), parents=(entry.artifact_id,), fixture=fixture)
                shared.append(semantic.artifact_id)
            for mapping in context.recipe.mappings:
                mapped = registry.put('mapping', mapping.source_variable + ' to ' + mapping.target.name,
                                      mapping.model_dump(mode='json'), parents=tuple(shared), fixture=fixture)
                shared.append(mapped.artifact_id)
            from .operations import REGISTRY
            operations = registry.put('operation_registry', 'Registered deterministic operations', REGISTRY.manifest(), visibility='public')
            shared.append(operations.artifact_id)
            recipe = registry.put('recipe', context.recipe.recipe_id, context.recipe.model_dump(mode='json'),
                                  parents=tuple(shared), fixture=fixture)
            context_parents = [recipe.artifact_id]
            if context.human:
                human = registry.put('human_decision', 'Existing exact-recipe human decision',
                                     context.human.model_dump(mode='json'), parents=(recipe.artifact_id,), fixture=fixture)
                context_parents.append(human.artifact_id)
            if context.evidence_review:
                review = registry.put('review', 'Existing scientific review report',
                                      context.evidence_review.model_dump(mode='json'), parents=(recipe.artifact_id,), fixture=fixture)
                context_parents.append(review.artifact_id)
            frozen = registry.put('context', 'Frozen harmonization context', context.model_dump(mode='json'),
                                  parents=tuple(context_parents), fixture=fixture)
            encoder = registry.put('encoder', 'MOSAIKS empirical encoder', _json(scratch / 'encoder/encoder.json'),
                                   parents=(frozen.artifact_id,), fixture=fixture,
                                   blobs=tuple(refs[n] for n in names if n.startswith('encoder/')))
            checked = registry.put('verification', 'Held-out numeric verification; scientific validity not established',
                                   verification, parents=(encoder.artifact_id,), fixture=fixture,
                                   blobs=tuple(refs[n] for n in names if n.startswith('verification')))
            data = DatasetEntry(records=manifest['records'], dimensions=manifest['dimensions'],
                                encoder_identity=manifest['encoder_identity'], context_digest=manifest['context_digest'],
                                fixture=fixture, manifest=manifest)
            dataset = registry.put('dataset', 'Generated MOSAIKS diagnostic' if fixture else 'Reviewed-stream MOSAIKS bundle',
                                   data.model_dump(mode='json'), parents=(frozen.artifact_id, encoder.artifact_id, checked.artifact_id),
                                   fixture=fixture, track=track, blobs=tuple(refs[n] for n in names if not n.startswith(('encoder/', 'verification'))))
            run = registry.put('run', 'Completed representation import',
                               {'status': 'complete', 'stage': 'representation_import', 'fixture': fixture,
                                'source_data_read': False, 'checks': 'existing gate + independent artifact re-verification',
                                'source_manifest_digest': digest(manifest)},
                               parents=(dataset.artifact_id,), fixture=fixture, track=track)
        return dataset, checked, run


def prepare_release(registry, dataset_id, verification_id):
    """Create review-only release metadata; this cannot approve real scientific release."""
    dataset, verification = registry.get(dataset_id), registry.get(verification_id)
    if dataset.kind != 'dataset' or verification.kind != 'verification' or verification_id not in dataset.parents:
        raise ValueError('release requires this dataset and its bound verification')
    if verification.payload.get('status') != 'evaluated':
        raise ValueError('release prototype requires completed held-out evaluation')
    if verification.payload.get('encoder_identity') != dataset.payload['encoder_identity']:
        raise ValueError('release encoder identity mismatch')
    pending, checked = [dataset_id, verification_id], set()
    while pending:
        identifier = pending.pop()
        if identifier in checked:
            continue
        checked.add(identifier)
        if len(checked) > 128:
            raise ValueError('release ancestry exceeds bounded review budget')
        record = registry.get(identifier)
        pending.extend(record.parents)
        for blob in record.blobs:
            registry.check_blob(blob)
    body = ReleaseEntry(dataset_id=dataset_id, verification_id=verification_id,
                        state='diagnostic' if dataset.fixture else 'needs_scientific_release_review',
                        limitation='Local metadata only; no DOI, remote publication, expert approval or independent scientific validity.')
    return registry.put('release', 'Diagnostic release' if dataset.fixture else 'Release awaiting scientific review',
                        body.model_dump(mode='json'), parents=(dataset_id, verification_id),
                        fixture=dataset.fixture, track=dataset.track)


def record_feedback(registry, issue):
    issue = FeedbackIssue.model_validate(issue)
    target = registry.get(issue.target_id)
    groups = {r.payload['group_id'] for r in registry.all(kind='workspace')}
    if issue.group_id not in groups:
        raise ValueError('unknown working group')
    return registry.put('feedback', issue.summary, issue.model_dump(mode='json'),
                        parents=(target.artifact_id,), fixture=target.fixture, track=target.track)


def seed_management(registry, *, inventory, assessments):
    """Import existing semantic metadata and explicit planned management components."""
    from .semantic_resources import load_inventory, load_assessments
    from .operations import REGISTRY
    resources = load_inventory(inventory)
    assessed = load_assessments(assessments, resources)
    with registry.transaction():
        resources_by_id = {}
        for resource in resources:
            item = registry.put('semantic_resource', resource.name, resource.model_dump(mode='json'), visibility='public')
            resources_by_id[resource.resource_id] = item.artifact_id
        for assessment in assessed:
            registry.put('semantic_assessment', 'Project assessment: ' + assessment.resource_id,
                         assessment.model_dump(mode='json'), parents=(resources_by_id[assessment.resource_id],), visibility='public')
        registry.put('operation_registry', 'Registered deterministic operations', REGISTRY.manifest(), visibility='public')
        for track, name in PRODUCTS.items():
            registry.put('product', name, ProductDefinition(track=track, name=name).model_dump(mode='json'), track=track)
        for i in range(1, 10):
            cohort, n = ('governance', i) if i <= 3 else ('synthesis', i - 3)
            body = WorkspaceDefinition(group_id=f'{cohort}-{n}', cohort=cohort,
                                       years=(1, 2) if i <= 3 else (2, 3),
                                       quota_bytes=2_000_000_000_000 if i <= 3 else 5_000_000_000_000,
                                       retention='Planning quota only; no storage reserved. Preserve cited research outputs; scratch closeout requires notice.')
            registry.put('workspace', f'{cohort.title()} group {n}', body.model_dump(mode='json'))
        for name, capability, host, boundary, limitation in (
            ('Local artifact index', 'PROTOTYPE', 'local SQLite + filesystem', 'Metadata, lineage, content-addressed files', 'Single host; no authenticated multi-user permissions'),
            ('Scientific execution', 'WORKING', 'existing Python modules', 'Approved harmonization to MOSAIKS', 'Generated demo; historical real vetoes remain binding'),
            ('MESA/iRODS', 'PLANNED', 'partner deployment unconfirmed', 'Discovery and lifecycle adapter boundary', 'No invented endpoints or duplicated partner implementation'),
            ('OSN distribution', 'PLANNED', 'OSN', 'S3-compatible release distribution', 'No remote connection, capacity award or backup implied'),
            ('NDP discovery', 'PLANNED', 'NDP', 'Public catalog/API federation', 'Local API is not a deployed NDP integration'),
            ('TACC preservation', 'PLANNED', 'TACC Corral/Ranch subject to agreement', 'Independent preservation', 'Local snapshot is not a remote deposit or ten-year agreement'),
        ):
            registry.put('service', name, ServiceDefinition(name=name, capability=capability, host=host,
                         boundary=boundary, limitation=limitation).model_dump(mode='json'))
        for resource, unit, quantity, evidence in (
            ('OSN pilot', 'GB', 50000, 'https://support.access-ci.org/documentation/resources/osn'),
            ('Jetstream2 development CPU', 'CPU_SU', 600000, 'https://docs.jetstream-cloud.org/general/access/'),
            ('Jetstream2 active workspace', 'GB', 40000, 'https://docs.jetstream-cloud.org/general/quotas/'),
        ):
            body = AllocationPlan(provider='ACCESS', resource=resource, unit=unit, requested=quantity,
                                  period='three-year planning envelope; tier/period must be negotiated',
                                  evidence_uri=evidence, verified_at='2026-10-23',
                                  limitation='Not requested or awarded. OSN >50 TB requires provider discussion; 40 TB Jetstream2 assumes Maximize approval. CPU excludes full production/services.')
            registry.put('allocation', resource, body.model_dump(mode='json'))
    return registry.summary()


def unresolved_review(registry, context_id):
    """Exercise six-domain missing-evidence review without manufacturing approvals."""
    from .harmonized_rasters import RasterContext
    from .review_contracts import Evidence, ReviewFinding, SpecialistReview
    from .review import REQUIRED_DOMAINS, source_set_digest, synthesize
    entry = registry.get(context_id)
    context = RasterContext.model_validate(entry.payload)
    ledger, reviews = [], []
    for domain in REQUIRED_DOMAINS:
        identifier = domain.value + '.independent_validation_missing'
        ledger.append(Evidence(evidence_id=identifier, domain=domain, kind='MISSING_EVIDENCE',
                               source='generated-management-demo', statement='No independent scientific release review is supplied for these generated diagnostics.',
                               content_digest=digest({'domain': domain.value, 'context': context_id})))
        finding = ReviewFinding(finding_id=identifier, reviewer_domain=domain, status='NEEDS_EVIDENCE',
                                claim='Generated pipeline results do not establish scientific release readiness.',
                                evidence=(identifier,), source='generated-management-demo',
                                required_action='Obtain independent domain evidence and actual expert review.', confidence=1)
        reviews.append(SpecialistReview(reviewer_domain=domain, recipe_content_digest=recipe_content_digest(context.recipe), findings=(finding,)))
    report = synthesize(reviews, ledger, recipe_content_digest=recipe_content_digest(context.recipe),
                        source_digest=source_set_digest(context.plan.resources))
    return registry.put('review', 'Six-domain release review: evidence missing', report.model_dump(mode='json'),
                        parents=(context_id,), fixture=True)


def scale_probe(registry, records):
    """Bounded metadata-only indexing experiment; does not pretend to encode rasters."""
    if not 1 <= records <= 100000:
        raise ValueError('metadata probe must contain 1..100000 records')
    started = perf_counter()
    with registry.transaction():
        for i in range(records):
            registry.put('run', f'Generated metadata probe {i}',
                         {'generated_index': i, 'status': 'complete', 'scope': 'metadata_index_only'}, fixture=True)
    duration = perf_counter() - started
    started = perf_counter()
    registry.list(kind='run', limit=50)
    query_duration = perf_counter() - started
    registry.db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
    body = ScaleProbe(generated_records=records, write_seconds=duration,
                      page_query_seconds=query_duration, database_bytes=(registry.root / 'registry.sqlite3').stat().st_size)
    return registry.put('benchmark', 'Generated metadata index scale probe', body.model_dump(mode='json'), fixture=True)


def export_metadata(registry, destination):
    """Portable controlled JSONL registries and PROV-inspired lineage, without arrays."""
    from contextlib import ExitStack
    from . import management_contracts
    from .contracts import Contract
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False, mode=0o700)
    counts = {}
    with ExitStack() as stack:
        handles = {}
        graph = stack.enter_context((destination / 'provenance.jsonld').open('x'))
        graph.write('{"@context":{"prov":"http://www.w3.org/ns/prov#"},"@graph":[')
        first = True
        for record in registry.all():
            if record.kind not in handles:
                handles[record.kind] = stack.enter_context((destination / (record.kind + '.jsonl')).open('x'))
            handles[record.kind].write(record.model_dump_json() + '\n')
            counts[record.kind] = counts.get(record.kind, 0) + 1
            if not first:
                graph.write(',')
            json.dump({'@id': 'urn:sha256:' + record.artifact_id, '@type': 'prov:Entity',
                       'prov:wasDerivedFrom': [{'@id': 'urn:sha256:' + parent} for parent in record.parents]}, graph)
            first = False
        graph.write(']}\n')
    schemas = destination / 'schemas'
    schemas.mkdir()
    for name, model in vars(management_contracts).items():
        if isinstance(model, type) and issubclass(model, Contract) and model is not Contract:
            (schemas / (name + '.json')).write_text(json.dumps(model.model_json_schema(), indent=2) + '\n')
    manifest = {'format': 'amber-registry-export-v1', 'counts': counts,
                'scope': 'controlled operator export; not public catalog or scientific equivalence graph',
                'files': {str(p.relative_to(destination)): sha256(p.read_bytes()).hexdigest()
                          for p in sorted(destination.rglob('*')) if p.is_file()}}
    (destination / 'export_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def demo(output, *, inventory, assessments, metadata_records=0, windows=32, features=128):
    """Actual generated harmonization/MOSAIKS + all management artifacts, no services."""
    from .mosaiks_pipeline import demo as mosaiks_demo
    root = Path(output)
    root.mkdir(parents=True, exist_ok=False)
    started, cpu = perf_counter(), process_time()
    mosaiks_demo(root / 'dataset', records=windows, features=features)
    with AssetRegistry(root / 'registry') as registry:
        seed_management(registry, inventory=inventory, assessments=assessments)
        dataset, verification, _ = import_dataset(registry, root / 'dataset')
        release = prepare_release(registry, dataset.artifact_id, verification.artifact_id)
        context_id = next(p for p in dataset.parents if registry.get(p).kind == 'context')
        unresolved_review(registry, context_id)
        record_feedback(registry, FeedbackIssue(target_id=release.artifact_id, group_id='synthesis-1',
                        category='representation', summary='Independent scientific labels are missing',
                        detail='Generated derived diagnostics exercise numeric consumption only; this issue is not an execution decision.'))
        for metric, value in (('wall_seconds', perf_counter() - started), ('process_cpu_seconds', process_time() - cpu), ('records', dataset.payload['records'])):
            measurement = UsageMeasurement(activity='generated end-to-end demo', metric=metric, value=value,
                                           scope='local process; no provider billing, model call or source download')
            registry.put('usage', metric, measurement.model_dump(mode='json'), parents=(release.artifact_id,), fixture=True)
        if metadata_records:
            scale_probe(registry, metadata_records)
        snapshot = registry.snapshot(root / 'preservation' / 'snapshot')
        recovery = restore_snapshot(root / 'preservation' / 'snapshot', root / 'preservation' / 'restored')
        body = PreservationResult(snapshot_digest=snapshot['snapshot_digest'], records=snapshot['records'],
                                  blobs=len(snapshot['blobs']), bytes=sum(b['bytes'] for b in snapshot['blobs'].values()))
        registry.put('preservation', 'Local fixity and actual restore test', body.model_dump(mode='json'),
                     parents=(release.artifact_id,), fixture=True)
        export_metadata(registry, root / 'registries')
        result = {'status': 'complete', 'fixture': True, 'dataset_id': dataset.artifact_id,
                  'release_id': release.artifact_id, 'registry': str((root / 'registry').resolve()),
                  'summary': registry.summary(), 'recovery': recovery,
                  'limitations': ['No approved real scientific release', 'No cloud services or awarded resources',
                                  'Three products are planned metadata, not three fabricated global datasets']}
        (root / 'demo_manifest.json').write_text(json.dumps(result, indent=2) + '\n')
        return result
