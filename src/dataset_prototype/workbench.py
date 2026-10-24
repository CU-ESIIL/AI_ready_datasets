"""Loopback-only operator workbench; no model execution, approvals or remote writes."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
import json
from urllib.parse import parse_qs, urlsplit
from .asset_registry import AssetRegistry
from .management import record_feedback
from .management_contracts import FeedbackIssue


def feature_rows(registry, identifier, *, offset=0, limit=16):
    """Read a bounded page of numerical features and exact observation lineage."""
    import numpy as np
    record = registry.get(identifier)
    if record.kind != 'dataset' or not 0 <= offset < record.payload['records'] or not 1 <= limit <= 32:
        raise ValueError('bounded dataset row page required')
    refs = {blob.name: blob for blob in record.blobs}
    path = registry.check_blob(refs['records.jsonl'])
    rows, matrices = [], {}
    with path.open() as stream:
        for i, line in enumerate(stream):
            if i < offset:
                continue
            if i >= offset + limit:
                break
            row = json.loads(line)
            name = row['vector_shard']
            if name not in matrices:
                matrices[name] = np.load(registry.check_blob(refs[name]), allow_pickle=False, mmap_mode='r')
            vector = matrices[name][row['vector_row']]
            if vector.dtype != np.float32 or vector.shape != (record.payload['dimensions'],) or not np.isfinite(vector).all():
                raise ValueError('feature schema differs from registered dataset')
            rows.append({'record': row, 'vector': vector.tolist()})
    return {'dataset_id': identifier, 'offset': offset, 'dimensions': record.payload['dimensions'],
            'dtype': 'float32', 'rows': rows, 'total': record.payload['records'],
            'next_offset': offset + len(rows) if offset + len(rows) < record.payload['records'] else None,
            'scientific_validation': 'not_established'}


def api(registry, method, target, payload=None):
    """Independently testable, bounded metadata API; explicit issue-only mutation."""
    url = urlsplit(target)
    query = parse_qs(url.query)
    def value(name, default=None):
        return query.get(name, [default])[0]
    if method == 'GET' and url.path == '/api/summary':
        return registry.summary()
    if method == 'GET' and url.path in {'/api/artifacts', '/api/catalog'}:
        page = registry.list(kind=value('kind'), track=value('track'), after=value('after', ''),
                             limit=int(value('limit', '50')), public=url.path == '/api/catalog')
        return {'items': [r.model_dump(mode='json') for r in page['items']], 'next': page['next']}
    if method == 'GET' and url.path.startswith('/api/datasets/') and url.path.endswith('/rows'):
        parts = url.path.split('/')
        if len(parts) != 5:
            raise KeyError('dataset route not found')
        return feature_rows(registry, parts[3], offset=int(value('offset', '0')), limit=int(value('limit', '16')))
    if method == 'GET' and url.path.startswith('/api/artifacts/'):
        identifier = url.path.removeprefix('/api/artifacts/')
        record = registry.get(identifier)
        return {'record': record.model_dump(mode='json'),
                'related': {k: [r.model_dump(mode='json') for r in records]
                            for k, records in registry.related(identifier).items()}}
    if method == 'POST' and url.path == '/api/feedback':
        return record_feedback(registry, FeedbackIssue.model_validate(payload)).model_dump(mode='json')
    raise KeyError('API route not found')


def byte_range(header, size):
    """Single HTTP byte range; no whole-file materialization."""
    if header is None:
        return 0, size - 1, False
    import re
    match = re.fullmatch(r'bytes=(\d*)-(\d*)', header)
    if not match or not size or not any(match.groups()):
        raise ValueError('unsupported byte range')
    first, last = match.groups()
    if not first:
        length = int(last)
        if length <= 0:
            raise ValueError('invalid suffix range')
        start, end = max(0, size - length), size - 1
    else:
        start, end = int(first), min(int(last), size - 1) if last else size - 1
    if start >= size or end < start:
        raise ValueError('range outside object')
    return start, end, True


def server(registry_root, *, host='127.0.0.1', port=8787):
    if host != '127.0.0.1':
        raise ValueError('prototype workbench must bind to IPv4 loopback')
    with AssetRegistry(registry_root):
        pass

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not log URLs, metadata, query strings or request bodies.

        def headers_safe(self):
            authority = f'127.0.0.1:{self.server.server_port}'
            if self.headers.get('Host') != authority:
                raise PermissionError('unexpected host')
            origin = self.headers.get('Origin')
            if origin and origin != 'http://' + authority:
                raise PermissionError('cross-origin request forbidden')

        def respond(self, status, payload, media='application/json'):
            body = json.dumps(payload, allow_nan=False).encode() if media == 'application/json' else payload
            self.send_response(status)
            self.send_header('Content-Type', media + ('; charset=utf-8' if media.startswith('text/') else ''))
            self.send_header('Content-Length', str(len(body)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            try:
                self.headers_safe()
                path = urlsplit(self.path).path
                if path == '/favicon.ico':
                    self.respond(204, b'', 'image/x-icon')
                elif path in {'/', '/app.js', '/style.css'}:
                    name = {'/': 'index.html', '/app.js': 'app.js', '/style.css': 'style.css'}[path]
                    media = {'/': 'text/html', '/app.js': 'text/javascript', '/style.css': 'text/css'}[path]
                    self.respond(200, files('dataset_prototype').joinpath('web', name).read_bytes(), media)
                elif path.startswith('/api/blobs/'):
                    parts = path.split('/')
                    if len(parts) != 5:
                        raise KeyError('blob route not found')
                    _, _, _, identifier, name = parts
                    with AssetRegistry(registry_root) as registry:
                        record = registry.get(identifier)
                        blob = next((b for b in record.blobs if b.name == name), None)
                        if blob is None:
                            raise KeyError('blob not registered')
                        local = registry.check_blob(blob)
                        try:
                            start, end, partial = byte_range(self.headers.get('Range'), blob.bytes)
                        except ValueError:
                            self.send_response(416)
                            self.send_header('Content-Range', f'bytes */{blob.bytes}')
                            self.send_header('Content-Length', '0')
                            self.end_headers()
                            return
                        self.send_response(206 if partial else 200)
                        self.send_header('Content-Type', 'application/octet-stream')
                        self.send_header('Content-Disposition', f'attachment; filename="{blob.name}"')
                        self.send_header('X-Content-Type-Options', 'nosniff')
                        self.send_header('Accept-Ranges', 'bytes')
                        self.send_header('ETag', '"' + blob.sha256 + '"')
                        self.send_header('Content-Length', str(max(0, end - start + 1)))
                        if partial:
                            self.send_header('Content-Range', f'bytes {start}-{end}/{blob.bytes}')
                        self.end_headers()
                        with local.open('rb') as stream:
                            stream.seek(start)
                            remaining = end - start + 1
                            while remaining > 0:
                                block = stream.read(min(65536, remaining))
                                if not block:
                                    break
                                self.wfile.write(block)
                                remaining -= len(block)
                else:
                    with AssetRegistry(registry_root) as registry:
                        self.respond(200, api(registry, 'GET', self.path))
            except PermissionError:
                self.respond(403, {'error': 'local same-origin access required'})
            except KeyError:
                self.respond(404, {'error': 'record or route not found'})
            except (ValueError, OSError):
                self.respond(400, {'error': 'invalid request or failed integrity check'})

        def do_POST(self):
            try:
                self.headers_safe()
                if self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('JSON request required')
                length = int(self.headers.get('Content-Length', '0'))
                if not 1 <= length <= 16384:
                    raise ValueError('bounded request body required')
                payload = json.loads(self.rfile.read(length))
                with AssetRegistry(registry_root) as registry:
                    result = api(registry, 'POST', self.path, payload)
                self.respond(201, result)
            except PermissionError:
                self.respond(403, {'error': 'local same-origin access required'})
            except KeyError:
                self.respond(404, {'error': 'record or route not found'})
            except (ValueError, OSError):
                self.respond(400, {'error': 'invalid issue; select a known group and target'})

    return ThreadingHTTPServer((host, port), Handler)


def serve(registry_root, *, port=8787):
    http = server(registry_root, port=port)
    print(f'AMBER local operator workbench: http://127.0.0.1:{http.server_port}/', flush=True)
    print('Local single-user prototype; feedback only, no scientific approval or live execution.', flush=True)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()
