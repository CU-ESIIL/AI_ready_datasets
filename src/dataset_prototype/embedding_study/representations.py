"""Strict R0/R1/R2 views and registered deterministic queries with no hidden fallback."""
from pathlib import Path
import numpy as np
from ..contracts import digest
from .contracts import FEATURE_ORDER, PIN, UPSTREAM_SHA256, OPERATIONS, PCAArtifact, DevelopmentalFeatures


class InsufficientInformation(Exception):
    """An evidence/representation limitation, not scientific failure."""


class InvalidOperation(Exception):
    """Unknown capability or an attempt to change scientific meaning."""


def provenance(history):
    return {'fire_id':history.fire_id,'history_digest':digest(history),'primary_profile_eligible':history.profile_eligible,'source':history.source.model_dump(mode='json'),
        'observation_ids':[o.observation_id for o in history.observations], 'source_unit':history.area_unit,
        'native_quality_flags':{o.observation_id:list(o.quality_flags) for o in history.observations},
        'upstream_commit':PIN,'upstream_operation_sha256':UPSTREAM_SHA256,
        'scientific_scope':'synthetic mechanics only; no real-science approval'}


def make_features(history, backend):
    if not history.profile_eligible:
        return None
    values = backend.call('features',list(history.growth))
    # The materialized shape view intentionally omits absolute size, native dates,
    # observation count and peak indices. The separate provenance sidecar retains
    # observation identifiers; their count can support the declared sequence-length query.
    return DevelopmentalFeatures(history_digest=digest(history),profile=values['profile'],traits=values['traits']).model_dump(mode='json')


def fit_artifact(dataset, features, backend, components):
    training = [h for h in dataset.histories if h.split=='train' and h.profile_eligible]
    if len(training) < components+1:
        raise ValueError('insufficient training fires; no evaluation-data fallback')
    x = [features[h.fire_id]['profile'] for h in training]
    fitted = backend.call('fit_pca',x)
    if fitted['explained_variance'][components-1] <= 1e-12:
        raise ValueError('requested components exceed supported training variation')
    body = {'version':'fire-vase-pca-v1','source_commit':PIN,'upstream_sha256':UPSTREAM_SHA256,
        'backend_versions':backend.versions,'feature_order':FEATURE_ORDER,
        'training_ids':tuple(h.fire_id for h in training),
        'training_history_digests':tuple(digest(h) for h in training),'training_feature_digest':digest(x),
        'mean':tuple(fitted['mean']),'scale':tuple(fitted['scale']),
        'components':tuple(tuple(v) for v in fitted['loadings'][:components]),
        'explained_variance':tuple(fitted['explained_variance'][:components])}
    return PCAArtifact(**body,artifact_digest=digest(body))


def coordinates(profile, artifact):
    return (((np.array(profile)-artifact.mean)/artifact.scale)@np.array(artifact.components).T).tolist()


def save_artifact(artifact, path):
    Path(path).write_text(artifact.model_dump_json(indent=2)+'\n')


def load_artifact(path, dataset=None):
    artifact = PCAArtifact.model_validate_json(Path(path).read_text())
    if dataset is not None:
        training = [h for h in dataset.histories if h.split=='train' and h.profile_eligible]
        if tuple(h.fire_id for h in training) != artifact.training_ids or tuple(digest(h) for h in training) != artifact.training_history_digests:
            raise ValueError('PCA training identity differs from declared training cohort')
    return artifact


class RepresentationView:
    def __init__(self, representation, payloads, lineages, backend, artifact):
        if representation not in {'R0','R1','R2'}:
            raise ValueError('unknown representation')
        self.representation = representation
        self.payloads = payloads
        self.lineages = lineages
        self.backend = backend
        self.artifact = artifact
        self.cache = {}
        self.last_cache_hit = False
        self.last_logical_bytes = 0

    def _profile(self, fire_id):
        payload = self.payloads[fire_id]
        if self.representation == 'R0':
            result = make_features(payload, self.backend)
            if result is None:
                raise InsufficientInformation('history ineligible for completed developmental profile')
            return result
        if self.representation == 'R1':
            if payload is None:
                raise InsufficientInformation('no valid developmental profile for this history')
            return payload
        raise InsufficientInformation('truncated coordinates cannot exactly recover full profile or original values')

    def _coordinates(self, fire_id):
        if self.representation == 'R2':
            if self.payloads[fire_id] is None:
                raise InsufficientInformation('no valid PCA coordinates')
            return self.payloads[fire_id]
        return coordinates(self._profile(fire_id)['profile'], self.artifact)

    def query(self, task):
        key = digest({'operation':task.operation,'fire_ids':task.fire_ids,'date':task.date.isoformat() if task.date else None,
            'start_date':task.start_date.isoformat() if task.start_date else None,'candidates':task.candidates,
            'approximation_allowed':task.approximation_allowed,'artifact':self.artifact.artifact_digest})
        self.last_cache_hit = key in self.cache
        self.last_logical_bytes = 0
        if key in self.cache:
            return self.cache[key]
        try:
            answer = self._query(task)
        except InsufficientInformation as error:
            result = {'answer':None,'abstention':True,'reason':str(error),'approximate':False,'unit':task.unit}
        else:
            result = {'answer':answer,'abstention':False,'reason':None,
                'approximate':self.representation=='R2' and task.operation=='nearest_profile','unit':task.unit}
        self.cache[key] = result
        return result

    def _query(self, task):
        if task.operation not in OPERATIONS:
            raise InvalidOperation('operation not in fixed benchmark allowlist')
        if task.operation == 'scientific_analog':
            raise InsufficientInformation('independent scientific relevance evidence not available')
        ids = tuple(dict.fromkeys((*task.fire_ids,*task.candidates)))
        if any(i not in self.payloads for i in ids):
            raise InvalidOperation('unknown fire identifier')
        self.last_logical_bytes = sum(len((self.payloads[i].model_dump_json() if self.representation=='R0'
            else __import__('json').dumps(self.payloads[i],sort_keys=True)).encode()) for i in ids)
        op, first = task.operation, task.fire_ids[0]
        if op=='sequence_days' and self.representation!='R0':
            if self.payloads[first] is None or not self.lineages[first]['primary_profile_eligible']:
                raise InsufficientInformation('no validated consecutive-profile context')
            observation_ids=self.lineages[first]['observation_ids']
            self.last_logical_bytes+=len(__import__('json').dumps(observation_ids).encode())
            # A successfully created primary feature/coordinate has exactly one
            # evidenced one-day increment per source ID. This uses retained
            # provenance, not inversion of normalized values or raw fallback.
            return len(observation_ids)
        if op in {'cumulative','interval_growth','daily_growth','maximum_daily_growth','peak_date','sequence_days','pulses'}:
            if self.representation != 'R0':
                raise InsufficientInformation('normalized shape/coordinates do not retain original area/date/sequence/pulse locations')
            h = self.payloads[first]
            rows = {o.date:o for o in h.observations if o.available}
            if op in {'cumulative','daily_growth'}:
                if task.date not in rows:
                    raise InsufficientInformation('requested observation unavailable')
                value = rows[task.date].cumulative_area if op=='cumulative' else rows[task.date].daily_growth
                if value is None:
                    raise InsufficientInformation('growth during temporal gap is unknown')
                return value
            if op == 'interval_growth':
                if task.date not in rows or task.start_date not in rows:
                    raise InsufficientInformation('interval endpoints unavailable')
                return rows[task.date].cumulative_area-rows[task.start_date].cumulative_area
            if not h.complete_sequence:
                raise InsufficientInformation('complete consecutive daily sequence required for this declared task')
            growth = tuple(o.daily_growth for o in h.observations)
            if op == 'maximum_daily_growth':
                return max(growth)
            if op == 'peak_date':
                return h.observations[growth.index(max(growth))].date.isoformat()
            if op == 'sequence_days':
                return (h.observations[-1].date-h.baseline_date).days
            result = self.backend.call('pulses',list(growth))
            return {'count':result['pulse_count'],'dates':[h.observations[i].date.isoformat() for i in result['pulse_indices']]}
        if op == 'profile':
            return self._profile(first)['profile']
        if op == 'front_fraction':
            return self._profile(first)['traits']['front_loaded_fraction']
        if op == 'profile_distance':
            a,b = (np.array(self._profile(i)['profile']) for i in task.fire_ids)
            return float(np.linalg.norm(a-b))
        if op == 'pca_distance':
            a,b = (np.array(self._coordinates(i)) for i in task.fire_ids)
            return float(np.linalg.norm(a-b))
        if op == 'nearest_profile':
            # R2 explicitly evaluates an approximate geometry, never claims exact
            # profile neighbors or scientifically meaningful fire analogs.
            def reconstructed(i):
                z=np.asarray(self._coordinates(i))
                return (z@np.asarray(self.artifact.components))*np.asarray(self.artifact.scale)+np.asarray(self.artifact.mean)
            accessor = reconstructed if self.representation=='R2' else lambda i:self._profile(i)['profile']
            q = np.array(accessor(first))
            distances = [(float(np.linalg.norm(q-np.array(accessor(i)))),i) for i in task.candidates]
            return [i for _,i in sorted(distances)[:2]]
        raise InvalidOperation('no implementation for operation')
