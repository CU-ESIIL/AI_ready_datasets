"""Offline consistency checks; no acquisition, inference or scientific execution."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from pypdf import PdfReader
HERE=Path(__file__).parent;ROOT=HERE.parents[1]
load=lambda n:json.loads((HERE/'data'/n).read_text())
def main():
 m=load('run_manifest.json');pdf=ROOT/m['report']['pdf'];assert hashlib.sha256(pdf.read_bytes()).hexdigest()==m['report']['sha256'];pages=PdfReader(pdf).pages;assert len(pages)==m['report']['pages']
 assert all(len(p.extract_text())>200 and '\u25a0' not in p.extract_text() for p in pages)
 for f in m['report']['figures']:assert hashlib.sha256((HERE/f['path']).read_bytes()).hexdigest()==f['sha256']
 for f in m['outputs']:assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
 for f in m['build_sources']:assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
 rows=load('resource_breadth.json');assert len(rows)==m['counts']['breadth_assertions'];assert any(r['score'] is None for r in rows)
 assert all(r['claim_class']=='PROJECT ASSESSMENT' and (r['score'] is None or (r['evidence'] and r['evidence_source'] and r['confidence'] is not None)) for r in rows)
 assert all(not load(n)['execution_authorized'] for n in ['canonical_benchmark.json','dataset_benchmark.json','sentinel_review_gap_analysis.json','expert_decision_template.json','neon_sentinel_case.json'])
 assert load('expert_decision_template.json')['decision'] is None
 calls=HERE/'data/model_experiment/calls.jsonl';s=load('model_experiment/summary.json');assert hashlib.sha256(calls.read_bytes()).hexdigest()==s['input_calls_sha256'];assert len(calls.read_text().splitlines())==s['call_counts']['total']
 assert all(not r['execution_authorized'] and r['human_gold_accuracy'] is None for r in load('model_experiment/evaluations.json'))
 for name,result in m['test_environments'].items():
  filename='tests.xml' if name=='integration' else 'core-tests.xml';assert hashlib.sha256((HERE/'data'/filename).read_bytes()).hexdigest()==result['xml_sha256']
 tests=ET.parse(HERE/'data/tests.xml');cases=tests.findall('.//testcase');failures=sum(c.find('failure') is not None or c.find('error') is not None for c in cases);assert failures==0
 print(f'Verified {len(pages)} pages, {len(m["report"]["figures"])} figure hashes, {len(rows)} assertions, {s["call_counts"]["total"]} inert calls and {len(cases)} passing test records; no approval granted')
if __name__=='__main__':main()
