"""Verify a document artifact, not the scientific pipeline or institutional controls."""
import json,hashlib
from pathlib import Path
from pypdf import PdfReader
HERE=Path(__file__).parent;ROOT=HERE.parents[1]
m=json.loads((HERE/'run_manifest.json').read_text());pdf=ROOT/m['pdf']['path']
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['pdf']['sha256']
pages=PdfReader(pdf).pages;assert len(pages)==m['pdf']['pages']==12
assert all(len(p.extract_text())>700 and '\u25a0' not in p.extract_text() for p in pages)
for r in m['inputs']:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
for path,expected in m['authoring_sources'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected
rows=json.loads((HERE/'data_inventory.json').read_text());assert len(rows)==m['inventory_records']==12
assert all(r['location'] and r['format'] and r['evidence'] and r['management_requirement'] for r in rows)
print('Verified 12 readable PDF pages, 12 inventory classes, input/source hashes and output checksum')
