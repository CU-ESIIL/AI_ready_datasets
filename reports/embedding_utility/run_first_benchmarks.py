"""Exploratory generated diagnostics. No agent calls, remote reads or raster writes."""
from pathlib import Path
import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from time import perf_counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataset_prototype.embedding_utility import generated_tile, ridge_predictions, strict_break_even
from dataset_prototype.mosaiks import MOSAIKSSpec, MOSAIKSEncoder
from dataset_prototype.harmonized_rasters import RasterContext, harmonize_window
from dataset_prototype.contracts import (Variable, SourceResource, Support, Metadata,
    Rights, SemanticMapping, HarmonizationRecipe, Operation, Proposal, digest)
from dataset_prototype.stream_contracts import StreamPlan, StreamBinding

ROOT = Path(__file__).resolve().parent
SEEDS = (17, 29, 43)
SIZES = (16, 32, 64, 128, 256)
DIMENSIONS = (16, 64, 128)
TARGETS = ('mean', 'texture_std', 'corner_pixel', 'unrelated_random')
ARMS = ('mean_baseline', 'summaries_ridge', 'pixels_ridge', 'mosaiks_ridge', 'hybrid_ridge')


def context_for(seed):
    when = datetime(2026, 11, 20, tzinfo=timezone.utc)
    variable = Variable(name='generated_value', definition='Unitless synthetic benchmark value, no ecological meaning',
        unit='1', measurement_method='generated_tile-v1 seeded Gaussian brightness/texture')
    source = SourceResource(source_id='embedding-utility-generated-v1', dataset='Generated representation diagnostics',
        asset_id=f'synthetic-{seed}', version='1', uri='generator://embedding-utility-v1', modality='satellite',
        variables=(variable,), support=Support(bbox=(-106,39,-104,41), start=when, end=when,
            spatial='fictional grid for generated diagnostics only', temporal='instantaneous'),
        metadata=Metadata(fixture=True, description='Generated numbers, no provider observations', original_identifier=f'synthetic-{seed}'),
        rights=Rights(license='CC0-1.0', attribution='Project-authored generated diagnostics', derivative_use=True, redistribution=True),
        checksum=digest({'generator':'generated_tile-v1','seed':seed,'side':12,'records':448}),
        checksum_scope='metadata', retrieved_at=when, provenance=('embedding-utility-generated-v1',))
    mapping = SemanticMapping(source_asset=source.asset_id, source_variable=variable.name, target=variable,
        relationship='equivalent_to', evidence=('Synthetic identity only',), confidence=1, review_status='approved')
    recipe = HarmonizationRecipe(recipe_id='embedding-utility-synthetic-identity', version='1', scope='core',
        status='approved', author='deterministic-generated-diagnostic', mappings=(mapping,),
        operations=(Operation(operation='map_variable',source_variable=variable.name,target_variable=variable.name),),
        proposals=(Proposal(role='harmonization',rationale='Identity for synthetic diagnostics only',evidence=('generated',)),))
    plan = StreamPlan(question='Generated offline diagnostics only',reader='test-generator',
        bindings=(StreamBinding(binding_id='generated',source=source,source_variable=variable.name,target=variable,longitude=-105,latitude=40),))
    return RasterContext(plan=plan,recipe=recipe)


def patch(context, seed, i):
    source = context.plan.resources[0]
    values = generated_tile(seed, i)
    split = 'train' if i < 256 else 'validation' if i < 320 else 'test'
    lineage = {'bbox':[-105+i*.001,40,-105+(i+1)*.001,40.0005],
        'native_crs':'fictional-generated-grid','native_window':[0,i*12,12,12],
        'source_assets':[source.asset_id], 'datetime_start':source.support.start.isoformat(),
        'datetime_end':source.support.end.isoformat(), 'quality_policy':'generated finite values; no source masks'}
    return harmonize_window({(source.asset_id,source.variables[0].name):values},context=context,
        patch_id=f'{seed}-{i}',lineage=lineage,split=split,spatial_group=f'generated-{seed}-{i}')


def write_csv(path, rows):
    with path.open('w',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    output = Path(sys.argv[1]) if len(sys.argv)>1 else Path('run/embedding_utility/first-benchmarks-v1')
    output.mkdir(parents=True,exist_ok=False)
    rows, timings = [], []
    for seed in SEEDS:
        context = context_for(seed)
        # Only compact summary features and vectors retained; patches regenerated on demand.
        raw = np.stack([generated_tile(seed,i).ravel() for i in range(448)])  # bounded synthetic-only reference
        summaries = np.column_stack([raw.mean(1),raw.std(1),raw.min(1),raw.max(1)])
        labels = np.column_stack([raw.mean(1),raw.std(1),raw[:,0],np.random.default_rng(seed+1000).normal(size=448)])
        for dimensions in DIMENSIONS:
            spec = MOSAIKSSpec(channels=('generated_value',),units=('1',),features=dimensions,
                seed=seed,input_scale=32,calibration_tiles=16)
            start = perf_counter()
            encoder = MOSAIKSEncoder.fit((patch(context,seed,i) for i in range(16)),spec,context)
            fit_seconds = perf_counter()-start
            vectors=[]; encode_seconds=0.
            for i in range(448):
                p=patch(context,seed,i)
                start=perf_counter(); vectors.append(encoder.encode(p,context)); encode_seconds+=perf_counter()-start
            vectors=np.stack(vectors)
            assert len(set(encoder.training_ids)) == 16
            timings.append({'seed':seed,'dimensions':dimensions,'filter_fit_seconds':fit_seconds,
                'encode_seconds_448_tiles':encode_seconds,'encoder_identity':encoder.identity,
                'synthetic_float32_input_bytes_per_tile':144*4,'float32_vector_bytes_per_tile':dimensions*4})
            features={'summaries_ridge':summaries,'pixels_ridge':raw,
                'mosaiks_ridge':vectors,'hybrid_ridge':np.column_stack([summaries,vectors])}
            for n in SIZES:
                for j,target in enumerate(TARGETS):
                    y=labels[:,j]; scale=float(y[:n].std())
                    for arm in ARMS:
                        if arm=='mean_baseline':
                            prediction=np.full(128,y[:n].mean()); alpha=None
                        else:
                            x=features[arm]
                            prediction,alpha=ridge_predictions(x[:n],y[:n],x[256:320],y[256:320],x[320:])
                        rmse=float(np.sqrt(np.mean((prediction-y[320:])**2)))
                        rows.append({'seed':seed,'dimensions':dimensions,'train_labels':n,'target':target,
                            'arm':arm,'rmse':rmse,'nrmse_train_std':rmse/scale,'validation_alpha':alpha})
            print(f'Finished seed={seed}, dimensions={dimensions}',flush=True)
    write_csv(output/'scores.csv',rows); write_csv(output/'timings.csv',timings)
    fig,axs=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    colors=dict(zip(ARMS,('0.5','#00816a','#8054aa','#d45b16','#2276b5')))
    names={'mean_baseline':'Training mean','summaries_ridge':'4 summaries + ridge','pixels_ridge':'144 pixels + ridge',
        'mosaiks_ridge':'128 MOSAIKS + ridge','hybrid_ridge':'Summaries + MOSAIKS'}
    for ax,target in zip(axs.flat,TARGETS):
        for arm in ARMS:
            scores=np.array([[next(r['nrmse_train_std'] for r in rows if r['seed']==seed and r['dimensions']==128
                and r['train_labels']==n and r['target']==target and r['arm']==arm) for n in SIZES] for seed in SEEDS])
            ax.plot(SIZES,scores.mean(0),label=names[arm],color=colors[arm])
            ax.fill_between(SIZES,scores.min(0),scores.max(0),color=colors[arm],alpha=.09)
        ax.set(title=target,xlabel='Training labels (fixed 16 training filter-reference tiles)',ylabel='Test RMSE / training-target SD',xscale='log',yscale='log')
        ax.set_xticks(SIZES, labels=[str(n) for n in SIZES])
        ax.minorticks_off()
        ax.grid(alpha=.2)
    axs[0,0].legend(fontsize=8)
    fig.suptitle('Generated diagnostics: learning curves (3 seeds; bands = min–max, not confidence intervals)', fontsize=12)
    fig.savefig(output/'learning_curves.png',dpi=150); fig.savefig(output/'learning_curves.svg'); plt.close(fig)
    fig,axs=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
    for target in TARGETS:
        values=[np.mean([r['nrmse_train_std'] for r in rows if r['target']==target and r['dimensions']==d
            and r['train_labels']==256 and r['arm']=='mosaiks_ridge']) for d in DIMENSIONS]
        axs[0].plot(DIMENSIONS,values,marker='o',label=target)
    axs[0].set(xlabel='MOSAIKS dimensions',ylabel='Test RMSE / training-target SD',yscale='log',title='Exploratory representation-size curve');axs[0].legend(fontsize=8)
    for d in DIMENSIONS:
        selected=[t for t in timings if t['dimensions']==d]
        axs[1].scatter([d*4],[np.mean([t['encode_seconds_448_tiles']/448*1000 for t in selected])],label=f'{d} features')
    axs[1].axvline(144*4,color='0.4',ls='--',label='12×12 float32 input payload')
    axs[1].set(xlabel='Vector payload bytes / tile (metadata/filters excluded)',ylabel='Mean encode time / tile (ms)',title='Measured local encoding, no source I/O');axs[1].legend(fontsize=8)
    fig.savefig(output/'dimension_curves.png',dpi=150);fig.savefig(output/'dimension_curves.svg');plt.close(fig)
    # Assumed abstract cost units: an algebra exercise, never measured agent costs.
    q=np.arange(1,201)
    scenarios=[('Savings possible',120,3,1,0),('With fixed refresh cost',120,3,1,60),('Direct already cheap',120,.5,1,0)]
    fig,axs=plt.subplots(1,3,figsize=(12,3.6),layout='constrained');cost_rows=[]
    for ax,(name,prep,direct,embedded,refresh) in zip(axs,scenarios):
        ax.plot(q,q*direct,label='Direct');ax.plot(q,prep+refresh+q*embedded,label='Embedding')
        crossing=strict_break_even(prep,direct,embedded,refresh=refresh)
        if crossing:ax.axvline(crossing,color='0.5',ls=':')
        ax.set(title=name,xlabel='Questions',ylabel='Assumed cumulative cost units');ax.legend(fontsize=8)
        cost_rows.append({'scenario':name,'preparation':prep,'direct_per_query':direct,'embedding_per_query':embedded,
            'fixed_refresh_cost':refresh,'first_strictly_cheaper_query':crossing})
    fig.suptitle('Illustrative algebra only — these costs were NOT measured')
    fig.savefig(output/'break_even.png',dpi=150);fig.savefig(output/'break_even.svg');plt.close(fig)
    (output/'cost_scenarios.json').write_text(json.dumps(cost_rows,indent=2)+'\n')
    code_paths=[Path(__file__),*sorted(Path('src/dataset_prototype').glob('*.py'))]
    manifest={'status':'complete','kind':'exploratory-generated-diagnostic','agent_calls':0,'source_downloads':0,
        'scientific_validity':'not_established','raw_or_harmonized_files_written':False,
        'seeds':SEEDS,'dimensions':DIMENSIONS,'label_counts':SIZES,'split_counts':{'train':256,'validation':64,'test':128},
        'labels':'derived input statistics; unrelated_random is independent synthetic noise, not scientific evidence',
        'filter_reference':'first 16 training tiles, fixed across nested label counts; no holdout fit',
        'uncertainty':'three generator/encoder seeds, no real geographic replication; min–max bands only',
        'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),
        'cost_scenarios':'assumed abstract units, not measured agent costs','created_at':datetime.now(timezone.utc).isoformat(),
        'code_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in code_paths},
        'outputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(output,flush=True)


if __name__=='__main__':
    main()
