"""Streaming MOSAIKS dataset publication and bounded downstream verification."""
from pathlib import Path
import json
from .contracts import digest
from .harmonized_rasters import authorize_context
from .mosaiks import MOSAIKSEncoder,validate_patch


def write_dataset(patches,model,context,output,*,batch_size=16):
    import numpy as np
    if not 1<=batch_size<=64:raise ValueError('embedding batch must be 1..64')
    context=authorize_context(context)  # before opening the harmonized stream
    root=Path(output);root.mkdir(parents=True,exist_ok=False)
    (root/'harmonization_context.json').write_text(context.model_dump_json(indent=2)+'\n')
    model.save(root/'encoder')
    manifest={'format':'mosaiks-dataset-v1','status':'incomplete','records':0,'dimensions':model.spec.features,
        'dtype':'float32','encoder_identity':model.identity,'context_digest':digest(context),'shards':[],
        'code_digest':digest({p.name:p.read_text() for p in Path(__file__).parent.glob('*.py')}),'numpy_version':np.__version__,
        'fixture':all(s.metadata.fixture for s in context.plan.resources),'split_counts':{'train':0,'validation':0,'test':0},
        'batch_size':batch_size,'raw_data_persisted':False,'harmonized_arrays_persisted':False,
        'vector_semantics':'MOSAIKS empirical random convolutional features, not text/LLM tokens',
        'lineage':'harmonization_context.json plus records.jsonl','labels':'verification_labels.jsonl; excluded from vectors'}
    iterator=None
    try:
        iterator=iter(patches)
        with (root/'records.jsonl.partial').open('x') as records,(root/'verification_labels.jsonl.partial').open('x') as labels:
            vectors=[];rows=[]
            def flush():
                if not vectors:return
                name=f'vectors-{len(manifest["shards"]):05d}.npy'
                matrix=np.stack(vectors).astype(np.float32)
                with (root/(name+'.partial')).open('xb') as f:np.save(f,matrix,allow_pickle=False)
                (root/(name+'.partial')).rename(root/name)
                for i,row in enumerate(rows):
                    row.update(vector_shard=name,vector_row=i)
                    manifest['split_counts'][row['split']]+=1
                    records.write(json.dumps(row,allow_nan=False)+'\n')
                manifest['shards'].append({'path':name,'rows':len(rows),'content_digest':__import__('hashlib').sha256((root/name).read_bytes()).hexdigest()})
                manifest['records']+=len(rows);vectors.clear();rows.clear();records.flush();labels.flush()
            for patch in iterator:
                validate_patch(patch,model.spec,context)
                vector=model.encode(patch,context)
                identity=digest({'observation':patch.observation_digest,'encoder':model.identity})
                vectors.append(vector)
                rows.append({'representation_id':identity,'patch_id':patch.patch_id,'observation_digest':patch.observation_digest,
                    'recipe_digest':patch.recipe_digest,'encoder_identity':model.identity,'split':patch.split,'spatial_group':patch.spatial_group,
                    'lineage':patch.lineage,'channels':patch.channels,'units':patch.units})
                if patch.verification_target is not None:
                    if patch.target_kind not in {'independent-label','derived-diagnostic','proxy-label'} or not patch.target_name:
                        raise ValueError('verification labels require a declared origin/name')
                    evidence=patch.verification_evidence
                    if patch.target_kind in {'independent-label','proxy-label'}:
                        required={'source','version','uri','license','measurement_method','spatial_alignment','temporal_alignment'}
                        if not evidence or not required<=set(evidence) or not all(evidence[k] for k in required):raise ValueError('independent/proxy labels require source and alignment provenance')
                    else:evidence={'derived_from':patch.observation_digest,'independent':False,'statistic':patch.target_name}
                    labels.write(json.dumps({'evidence':evidence,'representation_id':identity,'target':patch.verification_target,'target_name':patch.target_name,'target_kind':patch.target_kind},allow_nan=False)+'\n')
                if len(vectors)==batch_size:flush()
            flush()
        if not manifest['records']:raise ValueError('empty embedding dataset')
        (root/'records.jsonl.partial').rename(root/'records.jsonl')
        (root/'verification_labels.jsonl.partial').rename(root/'verification_labels.jsonl')
        from .mosaiks import file_digest
        manifest['records_sha256']=file_digest(root/'records.jsonl')
        manifest['labels_sha256']=file_digest(root/'verification_labels.jsonl')
        manifest['status']='complete'
        (root/'dataset_card.md').write_text('# MOSAIKS feature dataset\n\n'+
            ('Generated diagnostics only; no provider data or ecological validation.\n\n' if manifest['fixture'] else 'Real-data derived features; scientific suitability requires task verification.\n\n')+
            f"{manifest['records']} vectors × {manifest['dimensions']} float32 features.\n\n"+
            'Input: approved harmonization raster outputs. Encoder: empirical MOSAIKS; frozen training-only filters.\n\n'+
            'Splits: '+json.dumps(manifest['split_counts'])+'.\n\n'+
            'Read encoder/encoder.json and harmonization_context.json for channel meanings, units, source/version/license and review lineage.\n\n'+
            'verification_labels.jsonl declares target provenance. Derived diagnostics are not independent ground truth. Run mosaiks-verify before scientific reuse.\n\n'+
            'Source attribution and terms:\n\n'+'\n'.join('- '+s.rights.attribution+' Source terms: '+s.rights.license+'; version: '+s.version for s in context.plan.resources)+'\n')
    except BaseException as error:
        manifest.update(status='failed',error_type=type(error).__name__)
        raise
    finally:
        try:
            if iterator is not None and hasattr(iterator,'close'):iterator.close()
        except BaseException as error:
            manifest.update(status='failed',error_type=type(error).__name__)
            raise
        finally:(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def verify_dataset(root,output,*,max_records=2048):
    """Frozen features → train-only standardization/ridge → held-out evaluation.

    Bounded small-AOI verification, never an unbounded whole-dataset load.
    No claim that arbitrary AI models can decode feature dimensions natively.
    """
    import numpy as np
    from hashlib import sha256
    root=Path(root);manifest=json.loads((root/'manifest.json').read_text())
    if manifest['status']!='complete' or not 1<=manifest['records']<=max_records<=4096:
        raise ValueError('verification requires complete bounded dataset')
    model=MOSAIKSEncoder.load(root/'encoder')
    from .harmonized_rasters import RasterContext
    context=authorize_context(RasterContext.model_validate_json((root/'harmonization_context.json').read_text()))
    if digest(context)!=manifest['context_digest'] or model.identity!=manifest['encoder_identity']:
        raise ValueError('dataset encoder/context identity mismatch')
    def safe_file(name):
        p=(root/name).resolve()
        if not p.is_relative_to(root.resolve()):raise ValueError('dataset path escaped root')
        return p
    matrices={}
    for shard in manifest['shards']:
        path=safe_file(shard['path'])
        if sha256(path.read_bytes()).hexdigest()!=shard['content_digest']:raise ValueError('vector shard integrity mismatch')
        matrix=np.load(path,allow_pickle=False)
        if matrix.dtype!=np.float32 or matrix.shape!=(shard['rows'],model.spec.features) or not np.isfinite(matrix).all():
            raise ValueError('invalid AI feature matrix')
        matrices[shard['path']]=matrix
    from .mosaiks import file_digest
    if file_digest(root/'records.jsonl')!=manifest['records_sha256'] or file_digest(root/'verification_labels.jsonl')!=manifest['labels_sha256']:raise ValueError('dataset records/labels integrity mismatch')
    rows=[json.loads(x) for x in (root/'records.jsonl').read_text().splitlines()]
    labels={}
    for line in (root/'verification_labels.jsonl').read_text().splitlines():
        label=json.loads(line)
        if label['representation_id'] in labels:raise ValueError('duplicate verification label')
        labels[label['representation_id']]=label
    if len(rows)!=manifest['records'] or sum(len(m) for m in matrices.values())!=len(rows):raise ValueError('dataset row count mismatch')
    ids=set();observations=set();groups={};positions=set();feature_hashes={};data=[];targets=[];split=[];label_origins=set()
    for row in rows:
        identity=row['representation_id'];observation=row['observation_digest']
        if identity!=digest({'observation':observation,'encoder':model.identity}) or row['encoder_identity']!=model.identity or row['recipe_digest']!=digest(context.recipe):
            raise ValueError('row lineage/encoder identity mismatch')
        if identity in ids or observation in observations:raise ValueError('duplicate observation in verification set')
        ids.add(identity);observations.add(observation)
        position=(row['vector_shard'],row['vector_row'])
        if position in positions:raise ValueError('duplicate vector position')
        positions.add(position)
        vector=matrices[position[0]][position[1]]
        signature=sha256(vector.tobytes()).hexdigest()
        # Identical features can be genuine collisions (for example uniform tiles), not proof of label leakage.
        feature_hashes[signature]=row['split']
        previous=groups.setdefault(row['spatial_group'],row['split'])
        if previous!=row['split']:raise ValueError('spatial group leakage between train/validation/test')
        if identity not in labels:raise ValueError('verification target missing')
        label=labels[identity];label_origins.add((label['target_name'],label['target_kind']))
        data.append(vector);targets.append(label['target']);split.append(row['split'])
    if len(label_origins)!=1:raise ValueError('incompatible verification targets')
    holdout_ids={r['observation_digest'] for r in rows if r['split']!='train'}
    if set(model.training_ids)&holdout_ids:raise ValueError('filter calibration leakage into held-out splits')
    for i,a in enumerate(rows):
        bbox=a['lineage'].get('bbox')
        if bbox is None or len(bbox)!=4 or not (-180<=bbox[0]<bbox[2]<=180 and -90<=bbox[1]<bbox[3]<=90):raise ValueError('valid geographic support required for verification')
        for b in rows[i+1:]:
            other=b['lineage'].get('bbox')
            if a['split']!=b['split'] and other is not None and max(bbox[0],other[0])<min(bbox[2],other[2]) and max(bbox[1],other[1])<min(bbox[3],other[3]):
                raise ValueError('geographic overlap between verification splits')
    x=np.asarray(data,dtype=np.float64);y=np.asarray(targets,dtype=np.float64);split=np.asarray(split)
    if not np.isfinite(y).all():raise ValueError('nonfinite verification targets')
    counts={s:int((split==s).sum()) for s in ('train','validation','test')}
    result={'status':'insufficient_data','native_numeric_consumption':True,'scientific_validation':'not_established',
        'zero_vectors':int((np.linalg.norm(x,axis=1)==0).sum()),'distinct_feature_vectors':len(feature_hashes),
        'counts':counts,'target':list(next(iter(label_origins))),'encoder_identity':model.identity,
        'split_policy':'caller-declared disjoint spatial groups; requires independent audit of geography and target provenance',
        'limitations':['Single area/time does not establish geographic or temporal transfer','Derived/proxy targets do not establish independent scientific validity','Features are not intrinsically interpretable to an LLM']}
    if counts['train']>=8 and counts['validation']>=4 and counts['test']>=4:
        train=split=='train';validation=split=='validation';test=split=='test'
        mean=x[train].mean(0);std=x[train].std(0);std[std<1e-8]=1
        z=(x-mean)/std;ym=y[train].mean()
        def fit(alpha,target):
            a=z[train];return a.T@np.linalg.solve(a@a.T+alpha*np.eye(a.shape[0]),target-target.mean()),target.mean()
        candidates=[]
        for alpha in (.01,1.,100.):
            coef,intercept=fit(alpha,y[train]);candidates.append((float(np.mean((z[validation]@coef+intercept-y[validation])**2)),alpha,coef,intercept))
        _,alpha,coef,intercept=min(candidates,key=lambda c:c[0]);prediction=z[test]@coef+intercept
        rng=np.random.default_rng(42);shuffled,si=fit(alpha,rng.permutation(y[train]))
        def metrics(prediction):
            error=float(np.mean((prediction-y[test])**2));variance=float(np.mean((y[test]-y[test].mean())**2))
            return {'rmse':float(np.sqrt(error)),'r2':1-error/variance if variance>0 else None}
        probe=root/'verification_probe.npz'
        np.savez(probe,mean=mean,std=std,coefficients=coef,intercept=np.array(intercept),encoder_identity=np.array(model.identity),ridge_alpha=np.array(alpha))
        result.update(probe_file=probe.name,probe_sha256=file_digest(probe))
        result.update(status='evaluated',ridge_alpha=alpha,test=metrics(prediction),mean_baseline=metrics(np.full(test.sum(),ym)),
            shuffled_label_baseline=metrics(z[test]@shuffled+si),nonconstant_feature_dimensions=int((x[train].std(0)>1e-8).sum()))
    Path(output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result



def predict_vectors(vectors,probe_path,*,encoder_identity,expected_sha256):
    """A saved native numerical ML consumer, bound to one MOSAIKS coordinate space."""
    import numpy as np
    from .mosaiks import file_digest
    if file_digest(probe_path)!=expected_sha256:raise ValueError('verification probe integrity mismatch')
    with np.load(probe_path,allow_pickle=False) as probe:
        if str(probe['encoder_identity'].item())!=encoder_identity:raise ValueError('prediction encoder identity mismatch')
        x=np.asarray(vectors,dtype=np.float64)
        if x.ndim!=2 or not 1<=len(x)<=4096 or x.shape[1]!=len(probe['mean']) or not np.isfinite(x).all():
            raise ValueError('invalid native vector matrix')
        return ((x-probe['mean'])/probe['std'])@probe['coefficients']+probe['intercept']
