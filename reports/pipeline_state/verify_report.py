"""Validate artifact consistency; visual review is separately required."""
import hashlib,json
from pathlib import Path
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
m=json.loads((HERE/'data/run_manifest.json').read_text());pdf=ROOT/m['pdf']['path']
assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['pdf']['sha256']
pages=PdfReader(pdf).pages
assert len(pages)==m['pages'] and 25<=len(pages)<=40
assert len(m['figures'])==m['figure_count']
assert all(len(p.extract_text())>200 for p in pages)
assert all('\u25a0' not in p.extract_text() for p in pages), 'Possible missing font glyph'
for f in m['figures']:
 p=HERE/f['svg'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
for f in m['build_sources']:
 p=ROOT/f['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
required={'component','purpose','implementation_status','files','tests','test_status','examples','dependencies','inputs','outputs','contracts','known_limitations','next_steps','evidence'}
for r in json.loads((HERE/'data/component_inventory.json').read_text()):assert required<=set(r)
assert m['tests']['passed']+m['tests']['failed']+m['tests']['skipped']==m['tests']['total']
print(f"Verified {len(pages)} PDF pages, {m['figure_count']} figure hashes, narrative/build hashes, inventory fields and test totals")
