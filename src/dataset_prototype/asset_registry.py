"""Local immutable metadata index and content-addressed representation blobs."""
from contextlib import contextmanager
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
from .contracts import digest
from .management_contracts import ArtifactRecord, BlobReference

MAX_DOCUMENT_BYTES = 512 * 1024
MAX_BLOB_BYTES = 256 * 1024 * 1024


def _validate_payload(kind, payload):
    from . import contracts, management_contracts as m
    from .harmonized_rasters import RasterContext
    from .review_contracts import ReviewReport
    from .semantic_resources import SemanticResource, ResourceAssessment
    models = {
        'source': contracts.SourceResource, 'mapping': contracts.SemanticMapping,
        'recipe': contracts.HarmonizationRecipe, 'human_decision': contracts.HumanDecision,
        'context': RasterContext, 'review': ReviewReport,
        'semantic_resource': SemanticResource, 'semantic_assessment': ResourceAssessment,
        'semantic_profile': contracts.SourceSemantics, 'workspace': m.WorkspaceDefinition,
        'service': m.ServiceDefinition, 'allocation': m.AllocationPlan,
        'feedback': m.FeedbackIssue, 'usage': m.UsageMeasurement, 'dataset': m.DatasetEntry,
        'release': m.ReleaseEntry, 'preservation': m.PreservationResult, 'benchmark': m.ScaleProbe,
        'product': m.ProductDefinition,
    }
    if kind in models:
        return models[kind].model_validate(payload).model_dump(mode='json')
    # Encoder, existing run/verification and operation manifests retain native schemas.
    # They are evidence records only and are never interpreted as executable plans.
    if kind not in {'encoder', 'run', 'verification', 'operation_registry'}:
        raise ValueError('unknown artifact kind')
    if not isinstance(payload, dict):
        raise ValueError('metadata object required')
    return payload


class AssetRegistry:
    """Single-host prototype. SQLite/CAS is not authentication or remote storage."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.blob_root = self.root / 'blobs'
        self.blob_root.mkdir(exist_ok=True, mode=0o700)
        self.db = sqlite3.connect(self.root / 'registry.sqlite3', timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=NORMAL')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS artifacts(
                id TEXT PRIMARY KEY, kind TEXT NOT NULL, track TEXT,
                visibility TEXT NOT NULL, fixture INTEGER NOT NULL, body TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS by_kind ON artifacts(kind,id);
            CREATE INDEX IF NOT EXISTS by_track ON artifacts(track,id);
            CREATE INDEX IF NOT EXISTS by_visibility ON artifacts(visibility,kind,id);
            CREATE TABLE IF NOT EXISTS links(
                child TEXT REFERENCES artifacts(id), parent TEXT REFERENCES artifacts(id),
                PRIMARY KEY(child,parent));
            CREATE INDEX IF NOT EXISTS by_parent ON links(parent,child);
        ''')
        self._batch = False

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @contextmanager
    def transaction(self):
        if self._batch:
            raise ValueError('nested registry transactions unsupported')
        self._batch = True
        try:
            with self.db:
                self.db.execute('BEGIN')
                yield self
        finally:
            self._batch = False

    def _blob_path(self, checksum):
        import re
        if not re.fullmatch('[a-f0-9]{64}', checksum):
            raise ValueError('invalid blob checksum')
        path = self.blob_root / checksum[:2] / checksum
        if not path.resolve().is_relative_to(self.blob_root.resolve()):
            raise ValueError('blob path escapes registry')
        return path

    def store_blob(self, path, *, name, media_type):
        """Copy bounded known output files, never recursively ingest a run directory."""
        source = Path(path)
        if source.is_symlink() or not source.is_file() or source.stat().st_size > MAX_BLOB_BYTES:
            raise ValueError('bounded regular output file required')
        reference = BlobReference(sha256='0' * 64, bytes=source.stat().st_size,
                                  name=name, media_type=media_type)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.blob_root, delete=False) as handle:
                temporary = Path(handle.name)
                checksum = sha256()
                size = 0
                with source.open('rb') as stream:
                    for block in iter(lambda: stream.read(65536), b''):
                        size += len(block)
                        if size > MAX_BLOB_BYTES:
                            raise ValueError('output grew beyond byte budget')
                        checksum.update(block)
                        handle.write(block)
            reference = reference.model_copy(update={'sha256': checksum.hexdigest(), 'bytes': size})
            destination = self._blob_path(reference.sha256)
            destination.parent.mkdir(exist_ok=True)
            try:
                os.link(temporary, destination)
            except FileExistsError:
                self.check_blob(reference)
            return reference
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def check_blob(self, reference):
        path = self._blob_path(reference.sha256)
        if path.is_symlink() or not path.is_file() or path.stat().st_size != reference.bytes:
            raise ValueError('blob missing or size mismatch')
        checksum = sha256()
        with path.open('rb') as handle:
            for block in iter(lambda: handle.read(65536), b''):
                checksum.update(block)
        if checksum.hexdigest() != reference.sha256:
            raise ValueError('blob integrity mismatch')
        return path

    def put(self, kind, title, payload, *, parents=(), track=None, fixture=False,
            visibility='controlled', blobs=(), created_at=None):
        payload = _validate_payload(kind, payload)
        if kind == 'source' and payload['metadata']['fixture'] != fixture:
            raise ValueError('source fixture classification mismatch')
        if kind == 'dataset' and payload['fixture'] != fixture:
            raise ValueError('dataset fixture classification mismatch')
        body = dict(schema_version='1', kind=kind, title=title, fixture=fixture,
                    visibility=visibility, track=track, parents=list(parents), payload=payload,
                    blobs=[b.model_dump(mode='json') for b in blobs])
        identifier = digest(body)
        record = ArtifactRecord(artifact_id=identifier, **body,
                                **({'created_at': created_at} if created_at else {}))
        encoded = record.model_dump_json()
        if len(encoded.encode()) > MAX_DOCUMENT_BYTES:
            raise ValueError('metadata document exceeds byte budget')
        for parent in record.parents:
            previous = self.get(parent)
            if previous.track and record.track and previous.track != record.track:
                raise ValueError('cross-track derivation requires a separate reviewed association')
            if record.visibility == 'public' and previous.visibility != 'public':
                raise ValueError('public artifact cannot disclose controlled parent')
            if record.kind in {'dataset', 'release', 'context', 'encoder', 'verification'} and previous.fixture and not record.fixture:
                raise ValueError('generated evidence cannot become real scientific output')
        for blob in record.blobs:
            self.check_blob(blob)
        def insert():
            saved = self.db.execute('SELECT body FROM artifacts WHERE id=?', (identifier,)).fetchone()
            if saved:
                return self.get(identifier)
            self.db.execute('INSERT INTO artifacts VALUES(?,?,?,?,?,?)',
                            (identifier, kind, track, visibility, int(fixture), encoded))
            self.db.executemany('INSERT INTO links VALUES(?,?)',
                                [(identifier, parent) for parent in record.parents])
            return record
        if self._batch:
            return insert()
        with self.db:
            return insert()

    def get(self, identifier):
        row = self.db.execute('SELECT * FROM artifacts WHERE id=?', (identifier,)).fetchone()
        if row is None:
            raise KeyError('artifact not found')
        record = ArtifactRecord.model_validate_json(row['body'])
        if (record.artifact_id, record.kind, record.track, record.visibility, int(record.fixture)) != (
                row['id'], row['kind'], row['track'], row['visibility'], row['fixture']):
            raise ValueError('index and artifact identity mismatch')
        return record

    def list(self, *, kind=None, track=None, public=False, after='', limit=50):
        if not 1 <= limit <= 100:
            raise ValueError('page size must be 1..100')
        where, args = ['id>?'], [after]
        for column, value in (('kind', kind), ('track', track)):
            if value is not None:
                where.append(column + '=?')
                args.append(value)
        if public:
            where.append("visibility='public'")
        rows = self.db.execute('SELECT id FROM artifacts WHERE ' + ' AND '.join(where) +
                               ' ORDER BY id LIMIT ?', (*args, limit + 1)).fetchall()
        items = [self.get(row['id']) for row in rows[:limit]]
        return {'items': items, 'next': items[-1].artifact_id if len(rows) > limit else None}

    def all(self, **filters):
        after = ''
        while True:
            page = self.list(after=after, limit=100, **filters)
            yield from page['items']
            if not page['next']:
                break
            after = page['next']

    def related(self, identifier):
        self.get(identifier)
        return {
            'parents': [self.get(r[0]) for r in self.db.execute('SELECT parent FROM links WHERE child=? ORDER BY parent', (identifier,))],
            'children': [self.get(r[0]) for r in self.db.execute('SELECT child FROM links WHERE parent=? ORDER BY child LIMIT 100', (identifier,))],
        }

    def summary(self):
        counts = dict(self.db.execute('SELECT kind,COUNT(*) FROM artifacts GROUP BY kind'))
        unique = {}
        references = 0
        for record in self.all():
            for blob in record.blobs:
                references += blob.bytes
                unique[blob.sha256] = blob.bytes
        occupied = sum(p.stat().st_size for p in self.blob_root.rglob('*') if p.is_file() and not p.is_symlink())
        return {'counts': counts, 'artifacts': sum(counts.values()),
                'registered_blob_bytes': sum(unique.values()), 'referenced_blob_bytes': references,
                'cas_occupied_bytes': occupied, 'unreferenced_blob_bytes': occupied - sum(unique.values()),
                'database_bytes': sum(p.stat().st_size for p in self.root.glob('registry.sqlite3*')),
                'scope': 'local occupied bytes; not provisioned capacity or physical replication',
                'remote_services': 'not connected; no cloud allocation or retention agreement implied'}

    def check(self):
        count = 0
        for record in self.all():
            for parent in record.parents:
                self.get(parent)
            linked = {r[0] for r in self.db.execute('SELECT parent FROM links WHERE child=?', (record.artifact_id,))}
            if linked != set(record.parents):
                raise ValueError('lineage index mismatch')
            for blob in record.blobs:
                self.check_blob(blob)
            count += 1
        if self.db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('SQLite integrity check failed')
        return {'records_checked': count, 'status': 'fixity_checked', 'scientific_validation': 'not_established'}

    def snapshot(self, destination):
        """Local controlled backup, not a remote archival deposit or retention grant."""
        with self.transaction():
            return self._snapshot(destination)

    def _snapshot(self, destination):
        """One consistent SQLite read snapshot, including concurrent UI feedback."""
        destination = Path(destination).resolve()
        if destination.is_relative_to(self.root) or self.root.is_relative_to(destination):
            raise ValueError('snapshot must be outside the active registry')
        destination.mkdir(parents=True, exist_ok=False, mode=0o700)
        self.check()
        entries = []
        blobs = {}
        with (destination / 'records.jsonl').open('x') as stream:
            for record in self.all():
                stream.write(record.model_dump_json() + '\n')
                entries.append(record.artifact_id)
                for blob in record.blobs:
                    blobs[blob.sha256] = blob
        (destination / 'blobs').mkdir()
        for checksum, blob in blobs.items():
            target = destination / 'blobs' / checksum
            shutil.copyfile(self.check_blob(blob), target)
            computed = sha256()
            with target.open('rb') as handle:
                for block in iter(lambda: handle.read(65536), b''):
                    computed.update(block)
            if target.stat().st_size != blob.bytes or computed.hexdigest() != checksum:
                raise ValueError('snapshot copy integrity mismatch')
        body = {'format': 'amber-local-backup-v1', 'scope': 'controlled local snapshot; no remote deposit',
                'records': len(entries), 'records_sha256': sha256((destination / 'records.jsonl').read_bytes()).hexdigest(),
                'blobs': {k: b.model_dump(mode='json') for k, b in sorted(blobs.items())}}
        body['snapshot_digest'] = digest(body)
        (destination / 'manifest.json').write_text(json.dumps(body, indent=2) + '\n')
        return body


def restore_snapshot(source, destination):
    """Validate a bounded local backup and restore dependency order into a fresh index."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.exists():
        raise FileExistsError('restore destination must be new')
    for name, maximum in (('manifest.json', MAX_DOCUMENT_BYTES), ('records.jsonl', 128 * 1024 * 1024)):
        path = source / name
        if path.is_symlink() or path.stat().st_size > maximum:
            raise ValueError('snapshot file exceeds safety bounds')
    manifest = json.loads((source / 'manifest.json').read_text())
    identity = manifest.pop('snapshot_digest')
    if digest(manifest) != identity or manifest['format'] != 'amber-local-backup-v1':
        raise ValueError('snapshot manifest integrity mismatch')
    if sha256((source / 'records.jsonl').read_bytes()).hexdigest() != manifest['records_sha256']:
        raise ValueError('snapshot record integrity mismatch')
    records = [ArtifactRecord.model_validate_json(line) for line in (source / 'records.jsonl').read_text().splitlines()]
    if len(records) != manifest['records'] or len({r.artifact_id for r in records}) != len(records):
        raise ValueError('snapshot record counts mismatch')
    with AssetRegistry(destination) as registry:
        for checksum, value in manifest['blobs'].items():
            blob = BlobReference.model_validate(value)
            if checksum != blob.sha256:
                raise ValueError('snapshot blob identity mismatch')
            path = source / 'blobs' / checksum
            if path.is_symlink() or not path.resolve().is_relative_to(source):
                raise ValueError('unsafe snapshot blob path')
            copied = registry.store_blob(path, name=blob.name, media_type=blob.media_type)
            if copied != blob:
                raise ValueError('snapshot blob integrity mismatch')
        pending = {r.artifact_id: r for r in records}
        inserted = set()
        with registry.transaction():
            while pending:
                ready = [r for r in pending.values() if set(r.parents) <= inserted]
                if not ready:
                    raise ValueError('snapshot lineage missing or cyclic')
                for record in ready:
                    registry.put(record.kind, record.title, record.payload, parents=record.parents,
                                 fixture=record.fixture, track=record.track, visibility=record.visibility,
                                 blobs=record.blobs, created_at=record.created_at)
                    inserted.add(record.artifact_id)
                    del pending[record.artifact_id]
        return registry.check()
