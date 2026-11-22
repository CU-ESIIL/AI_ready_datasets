"""Manuscript-oriented tables and figures from recorded transfer results only."""
import argparse,csv,json
from pathlib import Path

METHODS=['raw','interpretable','PCA4','frozen_A','shared_AD','task_specific','direct_MLP','shared_AD_end_to_end','shared_mlp_end_to_end']

def generate(root,target):
    root=Path(root);target=Path(target);e=json.loads((root/'evaluation.json').read_text());r=json.loads((root/'retrieval.json').read_text());c=json.loads((root/'reuse_economics.json').read_text());m=json.loads((root/'manifest.json').read_text())
    lines=['# Milestone 5 manuscript results tables','','Synthetic convenience cohort; 256 held-out prefixes / 64 fires. B–E independently defined but correlated; A already observed in M4. All per-fire intervals are descriptive, conditional on fitted models, not wildfire population inference.','',
      '| Strategy | A log MSE ↓ | B log MSE ↓ | C Brier ↓ | D log MSE ↓ |','| --- | ---: | ---: | ---: | ---: |']
    for method in METHODS:
        values=[e[method][t]['test']['brier' if t=='C' else 'mse_log1p'] for t in 'ABCD']
        lines.append('| '+method+' | '+' | '.join(f'{x:.6f}' for x in values)+' |')
    lines+=['','Frozen A uses the exact M4 checkpoint. Shared AD is jointly supervised on all four tasks, so its gains are not A-only transfer. Aligned specific uses the A checkpoint for A and separately trained B/C/D encoders. Direct/shared MLPs are capacity/supervision controls.','',
      '| Task | Strategy | Raw minus method paired loss | Descriptive 95% fire interval |','| --- | --- | ---: | --- |']
    for task in 'BCD':
        for method in ['frozen_A','shared_AD','task_specific','direct_MLP']:
            p=e[method][task]['paired_vs_raw'];lo,hi=p['descriptive_fire_resampling_95_interval']
            lines.append(f"| {task} | {method} | {p['raw_minus_method_mean_squared_loss']:.6f} | [{lo:.6f}, {hi:.6f}] |")
    lines+=['','Positive raw-minus-method values favor the method on the corresponding predeclared task loss. No task selection, population p-values or multiplicity-adjusted confirmatory claim. Regression intervals and C reliability/calibration/depth/stratum results remain in full evaluation JSON.','',
      '| View | Direct representation P@10 ↑ | E-supervised head P@10 ↑ | Direct rank correlation |','| --- | ---: | ---: | ---: |']
    for method in ['raw','interpretable','PCA4','frozen_A','shared_AD','specific_B','specific_C','specific_D','specific_E']:
        a=r[method]['representation_distance'];b=r[method]['E_supervised_head_distance'];rho=a['mean_rank_correlation']
        lines.append(f"| {method} | {a['mean_fire_precision_at_k']:.4f} | {b['mean_fire_precision_at_k']:.4f} | {rho:.4f} |")
    lines+=['',f"Direct E MLP supervised-output P@10: {r['direct_MLP_E']['E_supervised_head_distance']['mean_fire_precision_at_k']:.4f}. Chance reference k/gallery: {r['raw']['representation_distance']['chance_precision_at_k']:.4f}.",
      'Relevance is held-out future-pattern geometry, not ecology. Same-fire candidates excluded. Precision equals recall because both selected/relevant sets have k=10. E-supervised heads use extra training labels and are not zero-shot distances.','',
      '| View | Training (all current seeds, s) | AD bundle on demand (µs) | AD heads on stored vector (µs) | Vector file bytes |','| --- | ---: | ---: | ---: | ---: |']
    for method in ['raw','interpretable','PCA4','frozen_A','shared_AD']:
        v=c['views'][method];bundle=v['bundles'][-1];training=c['training_costs'].get(method,0)/1e9
        label='historical '+f"{m['original_A_training_ns_historical']/1e9:.3f}" if method=='frozen_A' else f'{training:.3f}' if method=='shared_AD' else 'head fits separate'
        lines.append(f"| {method} | {label} | {bundle['on_demand_shared_encoding_plus_heads_ns']/1000:.3f} | {bundle['materialized_heads_ns']/1000:.3f} | {v['storage_bytes']} |")
    lines+=['',f"Separate task-specific AD encoder bundle: {c['task_specific_encoders'][-1]['separate_encoders_plus_heads_ns']/1000:.3f} µs. Current network training all strategies: {m['current_network_training_ns']/1e9:.3f} s. All training/head fit costs and materialization break-even bundles are recorded separately.",
      'File sizes exclude common lineage/checkpoints; not complete-interface storage. Raw/summary/PCA head fitting and original PCA construction are separate baselines. Cached complete bundles are stronger rivals for identical requests. Refresh/maintenance frequency and labor remain unmeasured.']
    target.write_text('\n'.join(lines)+'\n')
    probes=json.loads((root/'information_probes.json').read_text())['views']
    with target.with_name('information-probes-m5.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['view','probe','property','mse','r2_descriptive']);writer.writeheader()
        for view,v in probes.items():
            for kind in ('linear','nonlinear_rbf'):
                for row in v[kind]:writer.writerow({'view':view,'probe':kind,**row})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--output',required=True);a=p.parse_args();generate(a.results,a.output)
