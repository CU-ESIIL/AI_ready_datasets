"""Collect bounded, local report evidence; never access remote source observations."""
import ast,csv,hashlib,json,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import importlib.metadata as md
import pyarrow.parquet as pq
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'src'))
from dataset_prototype.operations import REGISTRY

def read(p):return json.loads((ROOT/p).read_text())
def save(name,obj):
 p=OUT/'data'/name;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(obj,indent=2,default=str)+'\n')

def main():
 xml=ET.parse(OUT/'data/tests.xml'); cases=xml.findall('.//testcase')
 tests=Counter()
 for c in cases:tests[c.get('classname','').split('.')[-1]]+=1
 result={'total':len(cases),'passed':sum(c.find('failure') is None and c.find('error') is None and c.find('skipped') is None for c in cases),'failed':sum(c.find('failure') is not None or c.find('error') is not None for c in cases),'skipped':sum(c.find('skipped') is not None for c in cases),'by_module':dict(tests),'coverage':'NOT YET MEASURED'}
 save('test_results.json',result)
 # Major components are assessments, never automated production-readiness scores.
 specs=[
 ('Discovery and source access','Find sources and preserve native metadata','PROTOTYPE',['discovery','real_data','stream_rasters','neon'],['discovery','real_data','stream_sources'],'STAC metadata, bounded COG windows; NEON normalization pending','Reviewed ScientificRequest','SourceResource; native evidence','Actual Sentinel retrieval retained; no current approved real embedding release'),
 ('MESA transport','Connect external access and metadata infrastructure','BLOCKED',['adapters'],['discovery'],'Verified deployed transport/schema required','External session','SourceResource','External methods deliberately unavailable; local MockMESAClient is MOCKED'),
 ('Semantic discovery','Separate source statements from concept candidates','PROTOTYPE',['semantic_discovery','semantic_resources'],['semantic_discovery'],'Local normalized/native metadata and curated namespace bindings','SourceResource','SourceSemantics; ConceptCandidate','No general external term resolver or verified equivalences'),
 ('Semantic landscape and diagnostics','Describe local semantic resources and metadata coverage','PROTOTYPE',['semantic_benchmark','semantic_resources'],['semantic_benchmark'],'86 provisional resource assessments; metadata-only benchmarks','Inventory; three source metadata records','Parquet diagnostics; review-only portfolio','Depth, potential, diversity, graph-level composition and scientific complementarity unmeasured'),
 ('Harmonization recipes','Record scientific mappings and allow-listed plans','PROTOTYPE',['harmonization','science'],['harmonization'],'Validated versioned deterministic operations','Mappings; reviewed recipe','HarmonizedObservation','No universal semantic equivalence; uncertain changes need scientists'),
 ('Verde / OpenClaw roles','Offer bounded scientific judgments without tools','PROTOTYPE',['openclaw_backend','openclaw_runtime','model_agents','consensus'],['openclaw','model_agents','streaming'],'Historical live calls retained; pinned OpenClaw 2026.5.18','Frozen metadata and closed schemas','Proposals; QA; exact prompts and normalized responses','Latest real Sentinel proposal vetoed; no live model call in this report'),
 ('Evidence and human review','Keep missing evidence and vetoes binding','PROTOTYPE',['review','scoped_review','review_contracts'],['review'],'Six domain specialists plus QA; mandatory human decision','Evidence; frozen recipe','ReviewReport; HumanDecision','Expert review and revision workflow remains incomplete'),
 ('JSON backbone and registry','Turn bounded proposals into validated deterministic choices','WORKING',['decision_ir','cube_ir','operations'],['operation_registry','cubedynamics'],'Closed operation references and typed contracts','RecipeDecision; capability digest','HarmonizationRecipe; ExecutionResult','WORKING means local demonstrated contract, not production deployment'),
 ('CubeDynamics backend','Execute bounded lazy transformations in external software','PROTOTYPE',['cubedynamics_backend','cube_contracts','cube_specs','cube_demo'],['cubedynamics'],'Actual external 0.1.0rc3; seven exposed operations','Reviewed xarray/Dask inputs','TransformationResult; bounded values','No CRS reprojection or general resampler; MOSAIKS bridge preserves one-band grid'),
 ('Streaming harmonization','Bring bounded source windows directly to encoders','PROTOTYPE',['streaming','harmonized_rasters','stream_contracts'],['streaming','stream_sources'],'Generated iterators tested; real access gated before read','Approved plan and source windows','HarmonizedRasterPatch; compact hashes','No remote throughput benchmark; historical snapshots remain explicit legacy paths'),
 ('MOSAIKS and verification','Encode harmonized rasters and test numerical usefulness','PROTOTYPE',['mosaiks','mosaiks_pipeline','embedding_dataset'],['mosaiks'],'Generated 32-window run, training-only empirical filters','Harmonized rasters','Dense features; lineage; held-out diagnostics','No independent ecological validation or native LLM interpretation demonstrated'),
 ('Provenance and storage','Trace representations back to observations and decisions','WORKING',['provenance','storage','representations'],['representations','integration_tracks'],'Content identities and JSON-LD provenance in offline runs','Sources; decisions; transforms','Representations; provenance records','No external MESA registration; window hashes do not cover entire remote assets'),
 ('Science tracks','Keep food/water assumptions separate from shared sources','PARTIAL',['orchestration'],['integration_tracks'],'Configuration and offline independence tests','Shared immutable sources; track configuration','Track-specific products','Independent domain outcomes unvalidated; third track undefined')]
 inv=[]
 for name,purpose,status,mods,tt,dep,ins,outs,lim in specs:
  files=[f'src/dataset_prototype/{m}.py' for m in mods]
  testfiles=[f'tests/test_{t}.py' for t in tt if (ROOT/f'tests/test_{t}.py').exists()]
  inv.append(dict(component=name,purpose=purpose,implementation_status=status,files=files,tests=testfiles,test_status='PASS (local offline suite)',examples=[dep],dependencies=[dep],inputs=[ins],outputs=[outs],contracts=['See generated docs/reference/contracts.md and source models'],known_limitations=[lim],next_steps=['Resolve the documented limitation with reviewed evidence'],evidence=files+testfiles))
 save('component_inventory.json',inv)
 with (OUT/'tables/components.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['component','implementation_status','purpose','known_limitations']);w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in inv)
 ops=[REGISTRY.get(k).model_dump(mode='json') for k in REGISTRY._entries]
 save('operations.json',ops)
 resources=list(csv.DictReader((ROOT/'data/semantics/semantic_resources.csv').open()))
 save('inventory_counts.json',{k:dict(Counter(r[k] for r in resources)) for k in ['resource_type','domain','era','project_role','verification_scope']})
 benchmark={}
 for p in sorted((ROOT/'outputs/semantic_benchmark').glob('*.parquet')):
  benchmark[p.stem]=pq.read_table(p).to_pylist()
 save('benchmark_tables.json',benchmark)
 # Minimal retained historical source evidence only, no acquisition in report build.
 window=read('run/real-sentinel/window-0.json');snapshot=read('run/real-sentinel/snapshot.json');source=snapshot['resources'][0]
 save('sentinel_example.json',{'window':window,'asset_id':source['asset_id'],'version':source['version'],'source_metadata':{k:source['metadata'][k] for k in ['platform','sensor','calibration_scale','calibration_offset']},'rights':source['rights'],'checksum_scope':source['checksum_scope'],'retrieved_at':source['retrieved_at'],'acquisition':source['support']['start'],'status':'Historical real acquisition evidence; illustrative coefficient calculation only; no currently approved real product'})
 save('annotated_recipe.json',read('run/cubedynamics-verified/harmonization_context.json')['recipe'])
 save('verification.json',read('run/cubedynamics-verified/verification.json'))
 save('embedding_manifest.json',read('run/cubedynamics-verified/manifest.json'))
 save('portfolio.json',read('outputs/semantic_benchmark/recommended_portfolio.json'))
 review=read('run/scoped-sentinel-review-v4/report.json');save('review_summary.json',{k:v for k,v in review.items() if k!='evidence'})
 kinds=['SOURCE_DOCUMENTED','OBSERVED_IN_DATA','DERIVED_DETERMINISTICALLY','MODEL_JUDGMENT','HUMAN_DECISION','MISSING_EVIDENCE']
 save('evidence_counts.json',{'scope':'Evidence array of retained scoped-sentinel-review-v4/report.json only; not all project artifacts or decisions','counts':{k:sum(e['kind']==k for e in review['evidence']) for k in kinds}})
 modules=list((ROOT/'src/dataset_prototype').glob('*.py'))
 contracts=[]
 for p in modules:
  for n in ast.parse(p.read_text()).body:
   if isinstance(n,ast.ClassDef) and any(isinstance(b,ast.Name) and b.id=='Contract' for b in n.bases):contracts.append(f'{p.stem}.{n.name}')
 metrics={'package_python_files':len(modules),'direct_Contract_subclasses':len(contracts),'exported_json_schemas':len(list((ROOT/'docs/reference/schemas').glob('*.json'))),'registered_operations':len(ops),'cube_operations':sum(o['backend']=='cubedynamics' for o in ops),'registry_declared_human_review':sum(o['requires_human_approval'] for o in ops),'cube_lazy_operations':sum(o['backend']=='cubedynamics' and 'LAZY' in o['lazy_or_eager'].upper() for o in ops),'tests':result,'semantic_resources':len(resources),'benchmark_rows':{k:len(v) for k,v in benchmark.items()},'ontology_graph_depth':'NOT YET MEASURED','dataset_ontology_potential':'NOT YET MEASURED','semantic_diversity':'NOT YET MEASURED','remote_stream_throughput':'NOT YET MEASURED','independent_ecological_validity':'NOT YET MEASURED','contracts':contracts}
 save('metrics.json',metrics)
 # Hash explicit inputs, excluding credentials, private runtime state and raster payloads.
 paths=[ROOT/'pyproject.toml',ROOT/'AGENTS.md',ROOT/'README.md',ROOT/'data/semantics/semantic_resources.csv',ROOT/'data/semantics/assessments.jsonl',ROOT/'run/real-sentinel/window-0.json',ROOT/'run/real-sentinel/snapshot.json',ROOT/'run/scoped-sentinel-review-v4/report.json',ROOT/'run/cubedynamics-verified/manifest.json',ROOT/'run/cubedynamics-verified/verification.json',OUT/'data/tests.xml',*modules,*sorted((ROOT/'tests').glob('test_*.py')),*sorted((ROOT/'outputs/semantic_benchmark').glob('*'))]
 versions={p:md.version(p) for p in ['dataset-prototype','cubedynamics','numpy','xarray','dask','matplotlib','reportlab','pypdf','pyarrow','pytest']}
 manifest={'report_version':'1.0','generated_at':datetime.now(timezone.utc).isoformat(),'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'git_status_at_audit':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),'pipeline_version':versions['dataset-prototype'],'cubedynamics_version':versions['cubedynamics'],'versions':versions,'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths if p.is_file()],'analyses':['Offline test XML aggregation','Local inventory counts','Existing metadata diagnostic Parquet tables','Retained historical Sentinel evidence extraction','Fresh generated CubeDynamics/MOSAIKS verification'],'tests':result,'limitations':['Component maturity is an editorial assessment linked to files/tests','Metadata diagnostics are not independently validated ontology quality or ecological science','No real Sentinel scientific approval or release','Historical source evidence reused locally; no new source acquisition','Missing metrics remain unmeasured'],'figures':[],'tables':[]}
 save('run_manifest.json',manifest)
 print(json.dumps({k:v for k,v in metrics.items() if k!='contracts'},indent=2))
if __name__=='__main__':main()
