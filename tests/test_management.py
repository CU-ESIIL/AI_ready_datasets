"""Offline integration, governance, integrity and recovery tests for local operations."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from dataset_prototype.asset_registry import AssetRegistry, restore_snapshot
from dataset_prototype.contracts import digest
from dataset_prototype.management import (
    import_dataset, prepare_release, record_feedback, seed_management, scale_probe, export_metadata,
)
from dataset_prototype.management_contracts import AllocationPlan, FeedbackIssue
from dataset_prototype.mosaiks_pipeline import demo as scientific_demo
from dataset_prototype.workbench import api, byte_range, server


@pytest.fixture
def registry(tmp_path):
    with AssetRegistry(tmp_path / 'registry') as value:
        yield value


@pytest.fixture
def bundle(tmp_path):
    root = tmp_path / 'dataset'
    scientific_demo(root)
    return root


def seed(registry):
    return seed_management(registry, inventory=Path('data/semantics/semantic_resources.csv'),
                           assessments=Path('data/semantics/assessments.jsonl'))


def metadata(registry, index=0, **kwargs):
    return registry.put('run', f'Generated {index}', {'index': index, 'status': 'failed'}, fixture=True, **kwargs)


def test_immutable_identity_pagination_and_parent_integrity(registry):
    source = metadata(registry)
    repeat = metadata(registry)
    assert source == repeat
    child = metadata(registry, 1, parents=(source.artifact_id,))
    page = registry.list(limit=1)
    assert page['next'] and len(page['items']) == 1
    second = registry.list(after=page['next'], limit=1)
    assert len(second['items']) == 1 and not second['next']
    assert page['items'][0].artifact_id != second['items'][0].artifact_id
    assert registry.related(child.artifact_id)['parents'] == [source]
    with pytest.raises(KeyError):
        metadata(registry, 2, parents=('0' * 64,))
    registry.db.execute('UPDATE artifacts SET body=? WHERE id=?', ('{}', source.artifact_id))
    with pytest.raises(ValueError):
        registry.get(source.artifact_id)


def test_public_projection_track_boundaries_and_generated_identity(registry):
    private = metadata(registry)
    with pytest.raises(ValueError, match='controlled parent'):
        metadata(registry, 1, parents=(private.artifact_id,), visibility='public')
    assert not registry.list(public=True)['items']
    food = metadata(registry, 1, track='cropland_food')
    with pytest.raises(ValueError, match='cross-track'):
        metadata(registry, 2, parents=(food.artifact_id,), track='watershed_water')
    with pytest.raises(ValueError, match='generated evidence'):
        registry.put('encoder', 'Incorrect real identity', {}, parents=(private.artifact_id,), fixture=False)
    with pytest.raises(ValueError, match='unknown artifact kind'):
        registry.put('arbitrary-code', 'No dynamic operations', {})


def test_blob_dedup_corruption_and_untrusted_paths(registry, tmp_path):
    path = tmp_path / 'vectors.npy'
    path.write_bytes(b'generated numeric output placeholder for storage test')
    blob = registry.store_blob(path, name='vectors.npy', media_type='application/x-npy')
    a = metadata(registry, 1, blobs=(blob,))
    metadata(registry, 2, blobs=(blob,))
    summary = registry.summary()
    assert summary['registered_blob_bytes'] == path.stat().st_size
    assert summary['referenced_blob_bytes'] == path.stat().st_size * 2
    with pytest.raises(ValueError):
        registry.store_blob(path, name='../runtime.env', media_type='application/x-npy')
    link = tmp_path / 'link'
    link.symlink_to(path)
    with pytest.raises(ValueError):
        registry.store_blob(link, name='link.npy', media_type='application/x-npy')
    registry.check_blob(blob).write_bytes(b'bad')
    with pytest.raises(ValueError, match='size mismatch'):
        registry.check()
    assert registry.get(a.artifact_id).kind == 'run'


def test_transaction_rolls_back_on_missing_lineage(registry):
    with pytest.raises(KeyError):
        with registry.transaction():
            metadata(registry)
            metadata(registry, 2, parents=('0' * 64,))
    assert registry.summary()['artifacts'] == 0


def test_seed_reuses_semantic_catalog_and_plans_are_not_awards(registry):
    result = seed(registry)
    assert result['counts']['workspace'] == 9 and result['counts']['product'] == 3
    assert result['counts']['semantic_resource'] == 86
    assert {r.payload['status'] for r in registry.all(kind='allocation')} == {'planning_estimate'}
    assert all(r.payload['state'] == 'planned' for r in registry.all(kind='product'))
    assert all(r.payload['scientific_scope_status'] == 'requires_scientific_definition' for r in registry.all(kind='product'))
    again = seed(registry)
    assert again['artifacts'] == result['artifacts']
    with pytest.raises(ValueError, match='award evidence'):
        AllocationPlan(provider='ACCESS', resource='OSN', unit='GB', requested=50000,
                       period='Y1', limitation='test', status='awarded')


def test_real_pipeline_bundle_import_has_complete_lineage_without_input_mutation(registry, bundle):
    before = {p.relative_to(bundle): sha256(p.read_bytes()).hexdigest() for p in bundle.rglob('*') if p.is_file()}
    dataset, verification, run = import_dataset(registry, bundle, track='cropland_food')
    assert dataset.payload['records'] == 32 and dataset.payload['dimensions'] == 128
    assert dataset.fixture and verification.payload['status'] == 'evaluated'
    assert dataset.payload['scientific_validation'] == 'not_established'
    assert run.payload['source_data_read'] is False
    release = prepare_release(registry, dataset.artifact_id, verification.artifact_id)
    assert release.payload['state'] == 'diagnostic' and release.payload['scientific_approval'] is False
    assert not registry.list(public=True, kind='release')['items']
    assert registry.summary()['counts']['source'] == 1
    assert registry.summary()['counts']['semantic_profile'] == 1
    assert registry.summary()['counts']['recipe'] == 1
    assert registry.check()['status'] == 'fixity_checked'
    page = api(registry, 'GET', f'/api/datasets/{dataset.artifact_id}/rows?offset=16&limit=3')
    assert len(page['rows']) == 3 and page['next_offset'] == 19
    assert page['dimensions'] == 128 and page['rows'][0]['record']['split'] == 'validation'
    assert len(page['rows'][0]['vector']) == 128
    with pytest.raises(ValueError):
        api(registry, 'GET', f'/api/datasets/{dataset.artifact_id}/rows?limit=100')
    after = {p.relative_to(bundle): sha256(p.read_bytes()).hexdigest() for p in bundle.rglob('*') if p.is_file()}
    assert before == after
    original_source = json.loads((bundle / 'harmonization_context.json').read_text())['plan']['bindings'][0]['source']
    saved_source = next(registry.all(kind='source')).payload
    assert original_source['rights'] == saved_source['rights']
    assert original_source['support'] == saved_source['support']
    assert all('raw' not in b.name and 'harmonized_arrays' not in b.name for r in registry.all() for b in r.blobs)
    shared_bytes = registry.summary()['registered_blob_bytes']
    second, _, _ = import_dataset(registry, bundle, track='watershed_water')
    assert second.artifact_id != dataset.artifact_id
    assert registry.summary()['counts']['source'] == 1
    assert registry.summary()['registered_blob_bytes'] == shared_bytes


@pytest.mark.parametrize('failure', ['failed', 'fixture', 'traversal', 'corruption', 'symlink', 'budget'])
def test_import_rejects_invalid_bundles(registry, bundle, failure):
    path = bundle / 'manifest.json'
    manifest = json.loads(path.read_text())
    if failure == 'failed':
        manifest['status'] = 'failed'
    elif failure == 'fixture':
        manifest['fixture'] = False
    elif failure == 'traversal':
        manifest['shards'][0]['path'] = '../../runtime.env'
    elif failure == 'corruption':
        (bundle / manifest['shards'][0]['path']).write_bytes(b'corrupt')
    elif failure == 'symlink':
        source = bundle / manifest['shards'][0]['path']
        other = bundle.parent / 'outside.npy'
        source.rename(other)
        source.symlink_to(other)
    else:
        manifest['records'] = 4097
    path.write_text(json.dumps(manifest))
    with pytest.raises((ValueError, OSError)):
        import_dataset(registry, bundle)
    assert registry.summary()['artifacts'] == 0


def test_release_requires_this_datasets_verification(registry, bundle):
    dataset, verification, _ = import_dataset(registry, bundle)
    wrong = registry.put('verification', 'unrelated check', verification.payload, fixture=True)
    with pytest.raises(ValueError, match='bound verification'):
        prepare_release(registry, dataset.artifact_id, wrong.artifact_id)
    encoder = next(registry.all(kind='encoder'))
    blob = next(b for b in encoder.blobs if b.name.endswith('filters.npy'))
    registry.check_blob(blob).write_bytes(b'corrupt encoder')
    with pytest.raises(ValueError):
        prepare_release(registry, dataset.artifact_id, verification.artifact_id)


def test_generated_reader_cannot_be_reclassified_as_real(registry, bundle):
    path = bundle / 'harmonization_context.json'
    context = json.loads(path.read_text())
    context['plan']['bindings'][0]['source']['metadata']['fixture'] = False
    path.write_text(json.dumps(context))
    manifest_path = bundle / 'manifest.json'
    manifest = json.loads(manifest_path.read_text()); manifest['fixture'] = False
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='gated Sentinel raster path'):
        import_dataset(registry, bundle)
    assert registry.summary()['artifacts'] == 0


def test_snapshot_restores_all_metadata_and_blob_integrity(registry, tmp_path):
    seed(registry)
    source = tmp_path / 'evidence.json'
    source.write_text('{"generated":true}')
    blob = registry.store_blob(source, name='evidence.json', media_type='application/json')
    parent = metadata(registry, blobs=(blob,))
    metadata(registry, 1, parents=(parent.artifact_id,))
    manifest = registry.snapshot(tmp_path / 'backup')
    restored = restore_snapshot(tmp_path / 'backup', tmp_path / 'restored')
    assert restored['records_checked'] == manifest['records']
    with AssetRegistry(tmp_path / 'restored') as other:
        assert {r.artifact_id for r in other.all()} == {r.artifact_id for r in registry.all()}
        assert other.get(parent.artifact_id) == parent
    with pytest.raises(ValueError, match='outside'):
        registry.snapshot(registry.root / 'nested')
    (tmp_path / 'backup' / 'blobs' / blob.sha256).write_bytes(b'broken')
    with pytest.raises(ValueError, match='integrity mismatch'):
        restore_snapshot(tmp_path / 'backup', tmp_path / 'corrupt-restored')


def test_snapshot_detects_manifest_and_record_edits(registry, tmp_path):
    metadata(registry)
    registry.snapshot(tmp_path / 'backup')
    (tmp_path / 'backup' / 'records.jsonl').write_text('{}\n')
    with pytest.raises(ValueError, match='record integrity'):
        restore_snapshot(tmp_path / 'backup', tmp_path / 'restored')


def test_snapshot_is_consistent_while_other_connection_adds_feedback(registry, tmp_path, monkeypatch):
    metadata(registry)
    original = registry.all
    inserted = False
    def interleaved(**filters):
        nonlocal inserted
        for record in original(**filters):
            yield record
            if not inserted:
                inserted = True
                with AssetRegistry(registry.root) as writer:
                    metadata(writer, 999)
    monkeypatch.setattr(registry, 'all', interleaved)
    manifest = registry.snapshot(tmp_path / 'consistent')
    assert manifest['records'] == 1
    assert registry.summary()['artifacts'] == 2
    assert restore_snapshot(tmp_path / 'consistent', tmp_path / 'restored')['records_checked'] == 1


def test_api_feedback_is_version_bound_and_never_approval(registry):
    seed(registry)
    target = metadata(registry)
    issue = FeedbackIssue(target_id=target.artifact_id, group_id='synthesis-1', category='interface',
                          summary='A UI test issue', detail='Generated reproduction evidence only')
    response = api(registry, 'POST', '/api/feedback', issue.model_dump(mode='json'))
    assert response['parents'] == [target.artifact_id]
    assert response['payload']['permission'] == 'issue_only_no_execution_authority'
    assert registry.get(target.artifact_id) == target
    assert api(registry, 'GET', '/api/artifacts?kind=feedback&limit=1')['items'][0]['artifact_id'] == response['artifact_id']
    assert not api(registry, 'GET', '/api/catalog?kind=feedback')['items']
    with pytest.raises(KeyError):
        api(registry, 'POST', '/api/approve', {})
    with pytest.raises(ValueError):
        api(registry, 'GET', '/api/artifacts?limit=1000')
    with pytest.raises(ValueError):
        api(registry, 'POST', '/api/feedback', {**issue.model_dump(), 'state': 'approved'})


def test_http_origin_request_size_and_download_ranges(registry, tmp_path, monkeypatch):
    # Exercise the actual HTTP handler in memory; offline tests never connect sockets.
    path = tmp_path / 'vectors.npy'
    path.write_bytes(b'0123456789')
    blob = registry.store_blob(path, name='vectors.npy', media_type='application/x-npy')
    target = metadata(registry, blobs=(blob,))
    import dataset_prototype.workbench as workbench
    monkeypatch.setattr(workbench, 'ThreadingHTTPServer', lambda address, handler:
                        SimpleNamespace(RequestHandlerClass=handler, server_port=8787, server_close=lambda: None))
    http = server(registry.root, port=0)
    try:
        handler = object.__new__(http.RequestHandlerClass)
        handler.server = http
        handler.wfile = BytesIO()
        handler.rfile = BytesIO(b'{}')
        handler.headers = {'Host': f'127.0.0.1:{http.server_port}', 'Range': 'bytes=2-5'}
        handler.path = f'/api/blobs/{target.artifact_id}/vectors.npy'
        statuses, headers = [], {}
        handler.send_response = statuses.append
        handler.send_header = headers.__setitem__
        handler.end_headers = lambda: None
        handler.do_GET()
        assert statuses == [206] and headers['Content-Range'] == 'bytes 2-5/10'
        assert handler.wfile.getvalue() == b'2345'
        handler.wfile = BytesIO(); statuses.clear()
        handler.headers = {'Host': 'attacker.example', 'Origin': 'https://attacker.example'}
        handler.path = '/api/summary'
        handler.do_GET()
        assert statuses == [403]
        handler.wfile = BytesIO(); statuses.clear()
        handler.headers = {'Host': f'127.0.0.1:{http.server_port}', 'Content-Type': 'application/json', 'Content-Length': '1000000'}
        handler.path = '/api/feedback'
        handler.do_POST()
        assert statuses == [400]
    finally:
        http.server_close()


@pytest.mark.parametrize('header,expected', [('bytes=0-4', (0, 4, True)), ('bytes=5-', (5, 9, True)), ('bytes=-3', (7, 9, True)), (None, (0, 9, False))])
def test_byte_ranges(header, expected):
    assert byte_range(header, 10) == expected


@pytest.mark.parametrize('header', ['bytes=10-', 'bytes=4-2', 'bytes=0-1,3-4', 'bytes=-0', 'bytes=-'])
def test_invalid_byte_ranges(header):
    with pytest.raises(ValueError):
        byte_range(header, 10)


def test_scale_probe_is_explicitly_metadata_not_raster_throughput(registry):
    result = scale_probe(registry, 150)
    assert result.payload['generated_records'] == 150
    assert result.payload['scope'] == 'generated_metadata_index_only'
    assert result.payload['write_seconds'] >= 0
    assert registry.summary()['counts']['run'] == 150
    with pytest.raises(ValueError):
        scale_probe(registry, 100001)


def test_portable_exports_preserve_metadata_and_provenance(registry, tmp_path):
    seed(registry)
    parent = metadata(registry)
    child = metadata(registry, 1, parents=(parent.artifact_id,))
    manifest = export_metadata(registry, tmp_path / 'export')
    assert manifest['counts']['product'] == 3 and manifest['counts']['workspace'] == 9
    for name, checksum in manifest['files'].items():
        assert sha256((tmp_path / 'export' / name).read_bytes()).hexdigest() == checksum
    graph = json.loads((tmp_path / 'export' / 'provenance.jsonld').read_text())
    relation = next(r for r in graph['@graph'] if r['@id'] == 'urn:sha256:' + child.artifact_id)
    assert relation['prov:wasDerivedFrom'] == [{'@id': 'urn:sha256:' + parent.artifact_id}]
    assert (tmp_path / 'export' / 'schemas' / 'ArtifactRecord.json').exists()


def test_generated_window_scale_controls_preserve_split_and_no_input_persistence(tmp_path):
    manifest, verification = scientific_demo(tmp_path / 'larger', records=64, features=32)
    assert manifest['records'] == 64 and manifest['dimensions'] == 32
    assert verification['counts'] == {'train': 32, 'validation': 16, 'test': 16}
    assert manifest['raw_data_persisted'] is False and manifest['harmonized_arrays_persisted'] is False
    with pytest.raises(ValueError, match='32..1024'):
        scientific_demo(tmp_path / 'invalid', records=65)
