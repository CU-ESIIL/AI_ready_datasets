"""MOSAIKS empirical random convolutional features over harmonized raster outputs.

No discovery, download, calibration or source reader belongs in this module.
Filters use train-only sampled patches, contrast normalization and regularized
ZCA as in the MOSAIKS paper. Features pool positive/negative biased responses.
"""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Literal
import json
from pydantic import Field,model_validator
from .contracts import Contract, digest

PAPER='https://www.nature.com/articles/s41467-021-24638-z'
REFERENCE='https://github.com/Global-Policy-Lab/mosaiks-paper/blob/7efb09ed455505562d6bb04c2aaa242ef59f0a82/code/mosaiks/featurization.py'


class MOSAIKSSpec(Contract):
    algorithm: Literal['mosaiks-empirical-rcf-v1']='mosaiks-empirical-rcf-v1'
    input_dtype: Literal['float32']='float32'
    channels: tuple[str,...]=Field(min_length=1,max_length=16)
    units: tuple[str,...]=Field(min_length=1,max_length=16)
    features: int=Field(default=512,ge=16,le=4096,multiple_of=2)
    kernel_size: int=Field(default=3,ge=2,le=6)
    seed: int=Field(default=42,ge=0)
    bias: float=Field(default=1,ge=0)
    input_scale: float=Field(default=1,gt=0)
    zca_bias: float=Field(default=.001,gt=0)
    calibration_tiles: int=Field(default=16,ge=2,le=64)
    filters_per_tile: int=Field(default=32,ge=1,le=128)
    max_tile_side: int=Field(default=64,ge=4,le=128)
    filter_batch: int=Field(default=64,ge=1,le=256)

    @model_validator(mode='after')
    def valid(self):
        if len(self.channels)!=len(self.units) or len(set(self.channels))!=len(self.channels) or self.kernel_size>self.max_tile_side:
            raise ValueError('canonical channel/unit lengths and kernel/tile limits must agree')
        return self


@dataclass(frozen=True)
class HarmonizedRasterPatch:
    """In-memory output of harmonization, not a raw source window.

    values are C,H,W in declared scientific units; all pixels retain native
    support. A content digest plus immutable harmonization lineage binds values.
    """
    values: object
    patch_id: str
    channels: tuple[str,...]
    units: tuple[str,...]
    recipe_digest: str
    observation_digest: str
    lineage: dict
    split: str
    spatial_group: str
    verification_target: float | None=None
    target_name: str | None=None
    target_kind: str | None=None
    verification_evidence: dict | None=None


def file_digest(path):
    h=sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(65536),b''):h.update(chunk)
    return h.hexdigest()


def array_digest(values):
    import numpy as np
    native=np.asarray(values)
    if native.dtype.kind not in 'fiu':raise ValueError('numeric raster/filter dtype required')
    x=np.ascontiguousarray(native,dtype=native.dtype.newbyteorder('<'))
    return digest({'shape':x.shape,'dtype':x.dtype.str,'bytes_sha256':sha256(x.tobytes()).hexdigest()})


def validate_patch(patch,spec,context):
    import numpy as np
    if not isinstance(patch,HarmonizedRasterPatch):raise TypeError('MOSAIKS accepts harmonized raster outputs only')
    from .harmonized_rasters import authorize_context
    context=authorize_context(context)
    if patch.recipe_digest!=digest(context.recipe) or patch.lineage.get('context_digest')!=digest(context):
        raise ValueError('patch context differs from approved harmonization')
    targets={m.target.name:m.target.unit for m in context.recipe.mappings}
    if any(targets.get(name)!=unit for name,unit in zip(spec.channels,spec.units)):
        raise ValueError('encoder channels/units do not match harmonized targets')
    x=np.asarray(patch.values)
    if (x.ndim!=3 or x.shape[0]!=len(spec.channels) or patch.channels!=spec.channels or patch.units!=spec.units
        or len(spec.units)!=len(spec.channels) or min(x.shape[1:])<spec.kernel_size or max(x.shape[1:])>spec.max_tile_side
        or not np.isfinite(x).all() or not patch.spatial_group or patch.split not in {'train','validation','test'}):
        raise ValueError('invalid harmonized raster shape, channel order, units, values or split')
    expected=digest({'values':array_digest(x),'recipe_digest':patch.recipe_digest,'lineage':patch.lineage})
    if patch.observation_digest!=expected or not patch.patch_id:
        raise ValueError('harmonized observation content/lineage mismatch')
    if patch.lineage.get('harmonization_status')!='approved' or patch.lineage.get('recipe_digest')!=patch.recipe_digest:
        raise ValueError('harmonized raster lacks approved recipe lineage')
    return np.asarray(x,dtype=np.float32)


def target_schema_digest(context,spec):
    targets={m.target.name:m.target for m in context.recipe.mappings}
    return digest([targets[name].model_dump(mode='json') for name in spec.channels])


class MOSAIKSEncoder:
    def __init__(self,spec,filters,training_ids,training_context_digest,canonical_schema_digest,training_context=None):
        import numpy as np
        self.spec=MOSAIKSSpec.model_validate(spec.model_dump(mode='json'))
        self.filters=np.asarray(filters,dtype=np.float32)
        shape=(spec.features//2,len(spec.channels),spec.kernel_size,spec.kernel_size)
        if self.filters.shape!=shape or not np.isfinite(self.filters).all():raise ValueError('invalid filter bank')
        self.training_ids=tuple(training_ids)
        self.training_context_digest=training_context_digest
        self.canonical_schema_digest=canonical_schema_digest
        self.training_context=training_context
        self.identity=digest({'spec':digest(spec),'filters':array_digest(self.filters),'training_observations':self.training_ids,'training_context_digest':training_context_digest,'canonical_schema_digest':canonical_schema_digest})

    @classmethod
    def fit(cls,patches,spec,context):
        import numpy as np
        from .harmonized_rasters import authorize_context
        context=authorize_context(context)
        rng=np.random.default_rng(spec.seed)
        samples=[];ids=[]
        # Consume a bounded training-only calibration stream. Never fit on holdout.
        iterator=iter(patches)
        try:
            for _ in range(spec.calibration_tiles):
                p=next(iterator,None)
                if p is None:break
                x=validate_patch(p,spec,context)*spec.input_scale
                if p.split!='train':raise ValueError('filter calibration accepts training split only')
                ids.append(p.observation_digest)
                for _ in range(spec.filters_per_tile):
                    r=int(rng.integers(0,x.shape[1]-spec.kernel_size+1));c=int(rng.integers(0,x.shape[2]-spec.kernel_size+1))
                    samples.append(x[:,r:r+spec.kernel_size,c:c+spec.kernel_size].copy())
        finally:
            if hasattr(iterator,'close'):iterator.close()
        if len(ids)<2 or len(set(ids))!=len(ids):raise ValueError('at least two distinct training tiles required')
        bank=np.stack(samples).reshape(len(samples),-1).astype(np.float64)
        bank-=bank.mean(axis=1,keepdims=True)
        norms=np.linalg.norm(bank,axis=1,keepdims=True)
        bank/=np.where(norms<1e-8,1,norms)
        covariance=bank.T@bank/len(bank)
        eigenvalues,eigenvectors=np.linalg.eigh(covariance)
        # Paper normalize_patches applies the inverse square root twice.
        whitened=bank@((eigenvectors/(np.maximum(eigenvalues,0)+spec.zca_bias))@eigenvectors.T)
        if not np.isfinite(whitened).all() or np.linalg.norm(whitened)<=0:raise ValueError('degenerate calibration patches')
        chosen=rng.choice(len(whitened),spec.features//2,replace=len(whitened)<spec.features//2)
        filters=whitened[chosen].reshape(-1,len(spec.channels),spec.kernel_size,spec.kernel_size)
        return cls(spec,filters,ids,digest(context),target_schema_digest(context,spec),context)

    def encode(self,patch,context):
        import numpy as np
        from numpy.lib.stride_tricks import sliding_window_view
        x=validate_patch(patch,self.spec,context)*self.spec.input_scale
        if target_schema_digest(context,self.spec)!=self.canonical_schema_digest:raise ValueError('canonical scientific definitions differ from encoder calibration')
        k=self.spec.kernel_size
        windows=sliding_window_view(x,(k,k),axis=(1,2))
        positive=[];negative=[]
        for start in range(0,len(self.filters),self.spec.filter_batch):
            response=np.einsum('crsij,fcij->frs',windows,self.filters[start:start+self.spec.filter_batch],optimize=True)
            positive.extend(np.maximum(response-self.spec.bias,0).mean(axis=(1,2)).tolist())
            negative.extend(np.maximum(-response-self.spec.bias,0).mean(axis=(1,2)).tolist())
        vector=np.array(positive+negative,dtype=np.float32)
        if not np.isfinite(vector).all():raise ValueError('nonfinite MOSAIKS vector')
        return vector

    def save(self,root):
        import numpy as np
        root=Path(root);root.mkdir(parents=True,exist_ok=False)
        from .harmonized_rasters import authorize_context
        if self.training_context is None:raise ValueError('training context required to publish MOSAIKS encoder')
        authorize_context(self.training_context)
        if digest(self.training_context)!=self.training_context_digest:raise ValueError('training context identity mismatch')
        (root/'training_context.json').write_text(self.training_context.model_dump_json(indent=2)+'\n')
        np.save(root/'filters.npy',self.filters,allow_pickle=False)
        (root/'encoder.json').write_text(json.dumps({'spec':self.spec.model_dump(mode='json'),'identity':self.identity,
            'filters_digest':array_digest(self.filters),'training_observations':self.training_ids,'training_context_digest':self.training_context_digest,'canonical_schema_digest':self.canonical_schema_digest,'numpy_version':np.__version__,
            'method_reference':REFERENCE,'paper':PAPER,'variant':'empirical MOSAIKS; global mean pooling; no local pooling or image resize; no input clipping or unit conversion'},indent=2)+'\n')

    @classmethod
    def load(cls,root):
        import numpy as np
        root=Path(root);metadata=json.loads((root/'encoder.json').read_text())
        from .harmonized_rasters import RasterContext,authorize_context
        training=authorize_context(RasterContext.model_validate_json((root/'training_context.json').read_text()))
        if digest(training)!=metadata['training_context_digest']:raise ValueError('encoder training context integrity mismatch')
        model=cls(MOSAIKSSpec.model_validate(metadata['spec']),np.load(root/'filters.npy',allow_pickle=False),metadata['training_observations'],metadata['training_context_digest'],metadata['canonical_schema_digest'],training)
        if model.identity!=metadata['identity'] or array_digest(model.filters)!=metadata['filters_digest']:raise ValueError('encoder artifact integrity mismatch')
        return model
