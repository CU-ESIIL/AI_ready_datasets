"""Evidence-only metadata treatments with invariant data, permissions and budgets."""
from ..contracts import digest
from .contracts import OPERATIONS, PIN

OP_UNITS = {'cumulative':'km2','interval_growth':'km2','daily_growth':'km2/day',
    'maximum_daily_growth':'km2/day','peak_date':'ISO_date','sequence_days':'day',
    'pulses':'count_and_dates','profile':'1','front_fraction':'1','profile_distance':'1',
    'pca_distance':'standardized_PC_distance','nearest_profile':'fire_ids','scientific_analog':'fire_ids'}
REGISTRY = {op:{'id':op,'version':'1','parameters':['fire_ids','date','start_date','candidates','approximation_allowed'],
    'output_unit':OP_UNITS[op]} for op in OPERATIONS}
BUDGET = {'max_fires':64,'max_observations_per_fire':512,'network':False,
          'model_code_execution':False,'raw_fallback':False}


def validate_conditions(conditions):
    if set(conditions) != {'M0','M1','M2'}:
        raise ValueError('exactly M0/M1/M2 conditions required')
    if any(set(v) != {'version','evidence'} or v['version']!='metadata-view-v1' for v in conditions.values()):
        raise ValueError('metadata configurations contain evidence only, not executable permissions')
    if any(not isinstance(v['evidence'],dict) for v in conditions.values()):
        raise ValueError('metadata evidence must be a mapping')


def metadata_views(dataset, conditions):
    validate_conditions(conditions)
    shared = {'schema_version':'fire-history-v1','dataset_digest':digest(dataset),
        'observation_manifest_digest':digest([digest(h) for h in dataset.histories]),
        'unit_contract':{'area':'km2','growth':'km2/day'},'operation_registry':REGISTRY,
        'resource_budget':BUDGET,'source_commit':PIN}
    views = {key:{'condition':key,**shared, 'evidence':value['evidence']} for key,value in conditions.items()}
    # Actual source evidence, not a task-specific answer or a new observation.
    views['M2']['evidence']={**views['M2']['evidence'],
        'source_ledger':{digest(h.source):h.source.model_dump(mode='json') for h in dataset.histories}}
    invariant = [digest({k:v for k,v in view.items() if k not in {'condition','evidence'}}) for view in views.values()]
    if len(set(invariant)) != 1:
        raise ValueError('metadata experiment changed observations, tools or resource budget')
    return views
