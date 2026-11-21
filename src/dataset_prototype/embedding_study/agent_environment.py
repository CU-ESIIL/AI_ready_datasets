"""Verified milestone-1 artifact reuse and representation-scoped dispatch."""
import hashlib
import json
from time import perf_counter_ns
from pathlib import Path
from ..contracts import digest
from .contracts import Dataset, TaskSet, DevelopmentalFeatures, CoordinateArtifact
from .representations import RepresentationView, provenance, load_artifact
from .agent_contracts import ScientificQuery
from .agent_render import alias_maps, public_data


def load_environment(root,snapshot,fixture,tasks,backend):
    root=Path(root);snapshot=root/snapshot
    manifest=json.loads((snapshot/'manifest.json').read_text())
    if manifest['status']!='complete' or manifest['synthetic'] is not True:
        raise ValueError('complete synthetic milestone-1 snapshot required')
    # Verify every retained original artifact, not a forged new fit under old IDs.
    for name,expected in manifest['output_sha256'].items():
        if hashlib.sha256((snapshot/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('milestone-1 artifact integrity failure')
    for name in (fixture,tasks):
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=manifest['input_sha256'][name]:
            raise ValueError('fixture/task identity changed since milestone 1; new protocol needed')
    dataset=Dataset.model_validate_json((root/fixture).read_text())
    taskset=TaskSet.model_validate_json((root/tasks).read_text())
    artifact=load_artifact(snapshot/'pca_artifact.json',dataset)
    features=json.loads((snapshot/'features.json').read_text())
    for h in dataset.histories:
        if features[h.fire_id] is not None:
            typed=DevelopmentalFeatures.model_validate(features[h.fire_id])
            if typed.history_digest!=digest(h):raise ValueError('feature source identity mismatch')
    coord=CoordinateArtifact.model_validate_json((snapshot/'coordinates.json').read_text())
    if coord.artifact_digest!=artifact.artifact_digest or coord.dataset_digest!=digest(dataset):
        raise ValueError('coordinate source/encoder mismatch')
    lineages={h.fire_id:provenance(h) for h in dataset.histories}
    stores={r:RepresentationView(r,p,lineages,backend,artifact) for r,p in {
        'R0':{h.fire_id:h for h in dataset.histories},'R1':features,'R2':coord.model_dump(mode='json')['coordinates']}.items()}
    forward,reverse=alias_maps(dataset)
    return dataset,taskset,stores,forward,reverse,manifest


class Dispatcher:
    def __init__(self,task,allowed,stores,aliases,reverse):
        # Only this task's approved source set may be addressed, not the entire archive.
        self.task=task;self.allowed=tuple(allowed);self.stores=stores
        self.aliases=aliases;self.reverse=reverse
        self.offered=set((*task.fire_ids,*task.candidates))
        self.results={};self.calls=[];self.selected=allowed[0] if len(allowed)==1 else None

    def authorize(self,representation):
        if representation not in self.allowed:raise PermissionError('unauthorized_representation')

    def inspect(self,representation):
        self.authorize(representation)
        return public_data(self.task,representation,self.stores[representation],self.aliases)

    def call(self,representation,operation,arguments):
        self.authorize(representation)
        q=ScientificQuery(operation=operation,**arguments.model_dump())
        public_ids=(*q.fire_ids,*q.candidates)
        if any(i not in self.reverse or self.reverse[i] not in self.offered for i in public_ids):
            raise PermissionError('unoffered_identifier')
        private=q.model_copy(update={'fire_ids':tuple(self.reverse[i] for i in q.fire_ids),
            'candidates':tuple(self.reverse[i] for i in q.candidates)})
        store=self.stores[representation]
        before_compute=store.backend.compute_ns if store.backend else 0
        before_ipc=store.backend.ipc_bytes if store.backend else 0
        started=perf_counter_ns()
        value=store.query(private)
        scientific_ns=perf_counter_ns()-started
        result_id=f'V{len(self.calls)+1:03d}'
        evidence_id='E'+digest({'query':private.model_dump(mode='json'),'representation':representation,
            'histories':[self.stores[representation].lineages[i]['history_digest'] for i in dict.fromkeys((*private.fire_ids,*private.candidates))],
            'answer':value['answer']})[:20]
        public_value=value['answer']
        if operation=='nearest_profile' and public_value is not None:
            public_value=[self.aliases[i] for i in public_value]
        public={'status':'no_result' if value['abstention'] else 'value','result_id':result_id,
            'value':public_value,'unit':value['unit'],'approximate':value['approximate'],
            'evidence_ids':[] if value['abstention'] else [evidence_id]}
        private_record={'representation':representation,'query':private.model_dump(mode='json'),
            'result':value,'public_result':public,'evidence_id':evidence_id,
            'cache_hit':store.last_cache_hit,'logical_input_bytes':store.last_logical_bytes,
            'scientific_dispatch_ns':scientific_ns,
            'worker_compute_ns':store.backend.compute_ns-before_compute if store.backend else 0,
            'worker_ipc_bytes':store.backend.ipc_bytes-before_ipc if store.backend else 0,
            'lineage':{i:self.stores[representation].lineages[i] for i in dict.fromkeys((*private.fire_ids,*private.candidates))}}
        self.calls.append(private_record);self.results[result_id]=private_record
        return public
