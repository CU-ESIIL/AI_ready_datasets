"""Seal executed M8 artifacts; byte identity is not scientific/rights approval."""
import argparse,hashlib,importlib.metadata,json,platform,sys
from datetime import datetime,timezone
from pathlib import Path


def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);post=json.loads((out/'validation/postflight.json').read_text());historical=[]
 for name,key in [('milestone-7-3-execution/execution-manifest.json','artifact_sha256'),('full-population-v1/manifest.json','outputs_and_code_sha256')]:
  path=out.parent/name;record=json.loads(path.read_text());checked=[]
  for old,digest in record[key].items():
   if old.startswith('reports/embedding_utility/fire_vase/'):
    assert sha(Path(old))==digest,old;checked.append(old)
  historical.append({'manifest':str(path),'manifest_sha256':sha(path),'historical_report_artifacts_unchanged':len(checked),'scope':'frozen historical report artifacts; global documentation/configuration intentionally evolves'})
 deps={k:importlib.metadata.version(k) for k in ('numpy','scipy','pyarrow','matplotlib','pydantic','pytest','mkdocs','mkdocs-material')}
 artifacts={}
 for path in sorted(out.rglob('*')):
  if path.is_file() and path.name!='execution-manifest.json':artifacts[path.relative_to(out).as_posix()]={'sha256':sha(path),'bytes':path.stat().st_size,'private':path.is_relative_to(out/'private'),'invalid_initial_archive':path.is_relative_to(out/'private/initial-uncentered-probe')}
 scripts=sorted(set(Path('scripts').glob('*fire_vase*m8*.py'))|set(Path('scripts').glob('*fire_vase*milestone8.py')))
 tracked=[*scripts,Path('src/dataset_prototype/embedding_study/observed_state.py'),Path('src/dataset_prototype/embedding_study/utility_learning.py'),Path('tests/test_fire_vase_utility_learning.py')]
 docs=['README.md','AGENTS.md','CHANGELOG.md','mkdocs.yml','pyproject.toml','docs/PROTOTYPE_STATUS.md','docs/analysis/fire-vase-utility.md','docs/testing.md','docs/examples.md','docs/image-credits.md','docs/development/decisions.md','docs/reference/modules.md','reports/embedding_utility/fire_vase/README.md','reports/embedding_utility/fire_vase/implementation-plan.md']
 result={'version':'fire-vase-m8-real-observed-state-v1','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'status':'EXECUTED_REAL_OBSERVED_STATE_UTILITY_EXPERIMENT','scope':'full native population, fixed scientific-property-state encoding; not end-to-end raw sequence/polygon learning','authority':'direct investigator project authorization and explicit M8 internal training request; no invented third-party rights receipt or scientific PASS','source_postflight':post['source_postflight'],'historical_preservation':historical,'population':{'native_ids':278865,'native_rows':627033,'one':161200,'two':47992,'three_plus':69673,'train':194980,'validation':41894,'test':41991},'neural_primary_fits':75,'neural_control_and_update_fits':21,'model_seed':20260828,'LLM_calls':0,'source_modifications':False,'external_publication':False,'python':sys.version,'platform':platform.platform(),'dependencies':deps,'implementation_sha256':{str(p):sha(p) for p in tracked},'documentation_sha256':{p:sha(Path(p)) for p in docs},'artifact_sha256':artifacts,'retained_checkpoints':'private NPZ; no pickle; checkpoint-inventory.json; invalid initial probe artifacts explicitly archived','unknown':['native measurement QA and operational availability','independent ecological validity','source physical duration/extinction','filesystem physical bytes read','production concurrency/network latency','true source-update cost','scientifically meaningful effect/equivalence threshold','training-seed variability','third-party external publication/redistribution clearance'],'verification':{'postflight':post['status'],'pytest_log':'validation/pytest-final.txt','strict_docs_log':'validation/mkdocs-strict.txt','figure_QA':'validation/figure-review.json'},'reproduction':'reproducibility.md; commands require real existing local lake; preserve versioned output identities'}
 (out/'execution-manifest.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(f'SEALED {len(artifacts)} artifacts; {len(scripts)} implementation scripts')
if __name__=='__main__':main()
