"""Extend frozen control operators to every held-out prefix without refitting."""
import argparse,gzip,json,hashlib
from pathlib import Path
import numpy as np
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.learned_training_contracts import TrainingConfig
from dataset_prototype.embedding_study.learned_data import generate,PrefixPreprocessor
from dataset_prototype.embedding_study.learned_models import load_checkpoint,state_digest
from dataset_prototype.embedding_study.learned_experiment import perturbations


def main():
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',required=True);args=p.parse_args()
    root=Path(args.results);target=Path(args.output)
    if target.exists():raise ValueError('preserve prior diagnostics; new output required')
    manifest=json.loads((root/'manifest.json').read_text())
    for name,expected in manifest['output_sha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:raise ValueError('frozen artifact changed')
    config=TrainingConfig.model_validate_json((root/'frozen_config.json').read_text());histories,records=generate(config)
    if digest(histories)!=manifest['source_digest']:raise ValueError('source identity mismatch')
    pre=PrefixPreprocessor().fit([r['prefix'] for r in records if r['split']=='train'])
    if pre.state()!=json.loads((root/'preprocessing.json').read_text()):raise ValueError('training-only preprocessing mismatch')
    state=json.loads((root/'model_states.json').read_text())['tcn'];params=load_checkpoint(root/state['checkpoint'],'tcn')
    if state_digest(params)!=state['parameter_digest']:raise ValueError('checkpoint mismatch')
    rows=[]
    for r in records:
        if r['split']=='test':rows.append({'fire_id':r['prefix'].fire_id,'depth':len(r['prefix'].dates),'controls':perturbations(r['prefix'],pre,params)})
    summary={}
    for name in ('temporal_order','same_shape_different_scale','equal_total_reversed_development','nominal_id_relabeling'):
        values=[next(c for c in r['controls'] if c['control']==name)['embedding_l2_change'] for r in rows]
        summary[name]={'n':len(values),'median_l2_change':float(np.median(values)),'min_l2_change':min(values),'max_l2_change':max(values)}
    target.parent.mkdir(parents=True,exist_ok=True)
    value={'version':'m4-controls-extension-v1','scientific_scope':'Predeclared mathematical controls extended to all frozen held-out prefixes, descriptive only; no refit or predictive outcome edits','frozen_manifest_sha256':hashlib.sha256((root/'manifest.json').read_bytes()).hexdigest(),'rows':rows,'summary':summary,'real_source_rows_read':0}
    with gzip.open(target,'wt') as f:json.dump(value,f,sort_keys=True,allow_nan=False)
    print(json.dumps(summary))

if __name__=='__main__':main()
