"""Synthetic scientific oracles, information loss, isolation and real pinned replay."""
from copy import deepcopy
from datetime import date
import gzip
import json
import os
from pathlib import Path
import numpy as np
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import digest
from dataset_prototype.embedding_study.contracts import Dataset, FireHistory, TaskSet, PCAArtifact
from dataset_prototype.embedding_study.metadata import metadata_views, validate_conditions
from dataset_prototype.embedding_study.reference import profile_oracle, front_oracle, ReferenceAnswers
from dataset_prototype.embedding_study.evaluation import evaluate
from dataset_prototype.embedding_study.representations import (RepresentationView, make_features,
    fit_artifact, coordinates, provenance, load_artifact, save_artifact)
from dataset_prototype.embedding_study.backend import UpstreamBackend
from dataset_prototype.embedding_study.runner import run_benchmark

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/'data/fixtures/embedding_utility/histories.json'
TASKS = ROOT/'data/fixtures/embedding_utility/tasks.json'
CONFIG = ROOT/'reports/embedding_utility/fire_vase/config/benchmark.json'
METADATA = ROOT/'reports/embedding_utility/fire_vase/config/metadata.json'


@pytest.fixture
def dataset():
    return Dataset.model_validate_json(FIXTURE.read_text())


@pytest.fixture
def histories(dataset):
    return {h.fire_id:h for h in dataset.histories}


@pytest.fixture
def tasks():
    return {t.task_id:t for t in TaskSet.model_validate_json(TASKS.read_text()).tasks}


@pytest.fixture
def backend():
    root,python = os.environ.get('FIRE_VASE_ROOT'),os.environ.get('FIRE_VASE_PYTHON')
    if not root or not python:
        pytest.skip('pinned upstream replay requires explicit FIRE_VASE_ROOT/FIRE_VASE_PYTHON; no mock fallback')
    with UpstreamBackend(root,python) as value:
        yield value


def test_missing_zero_and_unknown_are_distinct(histories):
    zero=histories['eval-zeros'].observations[2]
    missing=histories['eval-missing'].observations[2]
    after=histories['eval-missing'].observations[3]
    assert zero.available and zero.daily_growth==0
    assert not missing.available and missing.daily_growth is None and missing.cumulative_area is None
    assert after.available and after.days_since_previous==2 and after.daily_growth is None
    assert not histories['eval-missing'].profile_eligible
    assert not histories['eval-omitted'].profile_eligible
    assert histories['eval-unknown-baseline'].observations[0].daily_growth is None
    assert histories['eval-all-zero'].complete_sequence and not histories['eval-all-zero'].profile_eligible


@pytest.mark.parametrize('change', ['order','duplicate','negative','growth','gap','units','null_date','missing_as_zero','decreasing','availability'])
def test_scientific_schema_rejects_inconsistent_inputs(histories,change):
    h=histories['eval-constant'].model_dump(mode='json')
    if change=='order': h['observations'].reverse()
    if change=='duplicate': h['observations'][1]['date']=h['observations'][0]['date']
    if change=='negative': h['observations'][0]['cumulative_area']=-1
    if change=='growth': h['observations'][1]['daily_growth']=99
    if change=='gap': h['observations'][1]['days_since_previous']=2
    if change=='units': h['area_unit']='ha'
    if change=='null_date': h['observations'][0]['date']=None
    if change=='missing_as_zero': h['observations'][0]['available']=False
    if change=='decreasing': h['observations'][1]['cumulative_area']=0
    if change=='availability': h['observations'][0]['available_at']='2019-12-30T00:00:00Z'
    with pytest.raises(ValidationError): FireHistory.model_validate(h)


def test_metadata_isolation_and_no_secret_permissions(dataset):
    conditions=json.loads(METADATA.read_text())
    views=metadata_views(dataset,conditions)
    for field in ('dataset_digest','observation_manifest_digest','operation_registry','resource_budget','unit_contract'):
        assert len({digest(v[field]) for v in views.values()})==1
    assert len({digest(v['evidence']) for v in views.values()})==3
    for v in views.values():
        assert 'reference_answer' not in json.dumps(v)
    conditions['M2']['resource_budget']={'network':True}
    with pytest.raises(ValueError,match='evidence only'): validate_conditions(conditions)


def test_independent_analytic_answers_and_information_loss(dataset,histories,tasks):
    reference=ReferenceAnswers(dataset,3)
    assert profile_oracle(histories['eval-constant'])==pytest.approx([.05]*20)
    assert sum(profile_oracle(histories['eval-front']))==pytest.approx(1)
    assert profile_oracle(histories['eval-constant'])==profile_oracle(histories['eval-scaled'])
    assert reference.answer(tasks['area-constant'])==30
    assert reference.answer(tasks['area-scaled'])==300
    assert reference.answer(tasks['front-fraction'])==pytest.approx(26/30)
    assert reference.answer(tasks['back-fraction'])==pytest.approx(4/30)
    assert reference.answer(tasks['daily-zero'])==0
    assert reference.answer(tasks['daily-missing']) is None
    assert reference.answer(tasks['daily-after-gap']) is None
    assert reference.answer(tasks['interval-gap'])==6
    assert reference.answer(tasks['max-zero'])==0
    assert reference.answer(tasks['peak-back'])=='2020-01-06'
    assert reference.answer(tasks['duration'])==6
    assert reference.answer(tasks['pulses'])=={'count':2,'dates':['2020-01-02','2020-01-05']}
    assert reference.answer(tasks['scientific-analogs']) is None
    # Full-profile distance responds to ordering despite equal final totals.
    assert reference.answer(tasks['distance-order']) > 0


def test_evaluator_states_and_fabrication_penalty(tasks):
    task=tasks['area-constant']; numeric={'answer':30.,'abstention':False,'unit':'km2','approximate':False}
    assert evaluate(task,'R0',numeric,30)['status']=='correct'
    bad={**numeric,'answer':31}
    assert evaluate(task,'R0',bad,30)['status']=='incorrect'
    fabricated=evaluate(task,'R2',numeric,30)
    assert fabricated['status']=='incorrect' and fabricated['unsupported_answer'] and fabricated['scientific_validity']=='FAIL'
    abstention={**numeric,'answer':None,'abstention':True}
    assert evaluate(task,'R2',abstention,30)['status']=='correct_abstention'
    assert evaluate(task,'R0',abstention,30)['status']=='incorrect_abstention'
    assert evaluate(task,'R0',numeric,30,execution_error=('InvalidOperation','unknown'))['status']=='invalid_scientific_operation'
    assert evaluate(task,'R0',numeric,30,execution_error=('RuntimeError','failed'))['status']=='execution_failure'
    assert evaluate(task,'R0',{**numeric,'answer':float('nan')},30)['scientific_validity']=='FAIL'
    assert evaluate(task,'R0',{**numeric,'unit':'ha'},30)['scientific_validity']=='FAIL'


def test_training_identity_is_unique(dataset):
    data=dataset.model_dump(mode='json');data['histories'][-1]['fire_id']=data['histories'][0]['fire_id']
    with pytest.raises(ValidationError,match='crossing splits'): Dataset.model_validate(data)
    data=dataset.model_dump(mode='json');data['histories'][0]['source']['synthetic']=False
    with pytest.raises(ValidationError,match='synthetic'): Dataset.model_validate(data)


def test_pinned_upstream_profiles_pulses_and_negative_inputs(backend,dataset):
    for h in dataset.histories:
        if h.profile_eligible:
            features=make_features(h,backend)
            assert features['profile']==pytest.approx(profile_oracle(h),abs=1e-12)
            assert sum(features['profile'])==pytest.approx(1,abs=1e-12)
            assert min(features['profile'])>=0
            assert features['traits']['front_loaded_fraction']==pytest.approx(front_oracle(h),abs=1e-12)
            assert backend.call('features',list(h.growth))['peak_growth_km2_per_day']==max(h.growth)
    assert backend.call('pulses',[1,10,1,1,10,1])['pulse_indices']==[1,4]
    assert backend.call('pulses',[0,0,0])['pulse_count']==0
    for operation,values in [('features',[0,0,0]),('features',[1,-1,2]),('fit_pca',[[1]*19]*3),('eval','__import__("os")')]:
        with pytest.raises(ValueError): backend.call(operation,values)


def build_views(backend,dataset):
    features={h.fire_id:make_features(h,backend) for h in dataset.histories}
    artifact=fit_artifact(dataset,features,backend,3)
    payloads={'R0':{h.fire_id:h for h in dataset.histories},'R1':features,
        'R2':{i:coordinates(f['profile'],artifact) if f else None for i,f in features.items()}}
    lineage={h.fire_id:provenance(h) for h in dataset.histories}
    return {r:RepresentationView(r,p,lineage,backend,artifact) for r,p in payloads.items()},artifact


def test_views_preserve_answers_and_abstain_without_fallback(backend,dataset,tasks):
    views,artifact=build_views(backend,dataset)
    reference=ReferenceAnswers(dataset,3)
    for r,view in views.items():
        result=view.query(tasks['area-constant'])
        assert (result['answer']==30) if r=='R0' else result['abstention']
        assert view.query(tasks['scientific-analogs'])['abstention']
        assert view.query(tasks['duration'])['answer']==6  # retained provenance counts, even in R1/R2
        assert view.query(tasks['duration'])['answer']==6
        if r!='R0':
            assert 'cumulative_area' not in json.dumps(view.payloads)
            assert 'daily_growth' not in json.dumps(view.payloads)
        assert view.query(tasks['pca-geometry'])['answer']==pytest.approx(reference.answer(tasks['pca-geometry']),abs=1e-8)
    assert views['R0'].query(tasks['daily-zero'])['answer']==0
    assert views['R0'].query(tasks['daily-after-gap'])['abstention']
    assert views['R1'].query(tasks['front-fraction'])['answer']==pytest.approx(26/30)
    calls=backend.calls
    assert views['R1'].query(tasks['front-fraction'])['answer']==pytest.approx(26/30)
    assert views['R1'].last_cache_hit and backend.calls==calls
    assert views['R2'].query(tasks['profile-front'])['abstention']
    assert views['R1'].payloads['eval-constant']['profile']==views['R1'].payloads['eval-scaled']['profile']
    assert views['R2'].payloads['eval-constant']==pytest.approx(views['R2'].payloads['eval-scaled'])
    missing=tasks['area-constant'].model_copy(update={'fire_ids':('absent-fire',)})
    from dataset_prototype.embedding_study.representations import InvalidOperation
    with pytest.raises(InvalidOperation): views['R0'].query(missing)
    unknown=tasks['area-constant'].model_copy(update={'operation':'run_python'})
    with pytest.raises(InvalidOperation): views['R0'].query(unknown)
    assert views['R0'].query(tasks['pulses'])['answer']==reference.answer(tasks['pulses'])
    assert all(not i.startswith('eval') for i in artifact.training_ids)


def test_artifact_integrity_and_training_only_fit(backend,dataset,tmp_path):
    views,artifact=build_views(backend,dataset)
    path=tmp_path/'artifact.json';save_artifact(artifact,path)
    assert load_artifact(path,dataset).artifact_digest==artifact.artifact_digest
    changed=dataset.model_dump(mode='json')
    # Change an evaluation fire's shape as well as size. Fit must not move.
    h=next(h for h in changed['histories'] if h['fire_id']=='eval-scaled')
    running=0
    for index,o in enumerate(h['observations']):
        value=1 if index==0 else 50
        running+=value
        o['cumulative_area']=running;o['daily_growth']=value
    modified=Dataset.model_validate(changed)
    _,again=build_views(backend,modified)
    assert again.artifact_digest==artifact.artifact_digest
    bad=json.loads(path.read_text());bad['mean'][0]+=1;path.write_text(json.dumps(bad))
    with pytest.raises(ValidationError,match='integrity'): load_artifact(path,dataset)
    swapped=dataset.model_dump(mode='json');swapped['histories'][0]['split']='evaluation'
    save_artifact(artifact,path)
    with pytest.raises(ValueError,match='training identity'): load_artifact(path,Dataset.model_validate(swapped))


def test_full_benchmark_replay_and_metadata_cache_isolation(backend,tmp_path):
    # The explicit upstream fixture confirms availability; each run owns its worker.
    config=json.loads(CONFIG.read_text());config['repeats']=1
    path=tmp_path/'config.json';path.write_text(json.dumps(config))
    # Config is intentionally outside root for tests; relative data paths still use root.
    outputs=[]
    for name in ('first','second'):
        manifest,summary=run_benchmark(path,tmp_path/name,upstream=backend.upstream,
            upstream_python=os.environ['FIRE_VASE_PYTHON'],repository_root=ROOT)
        assert manifest['status']=='complete' and summary['metadata_invariance']
        with gzip.open(tmp_path/name/'results.jsonl.gz','rt') as f: rows=[json.loads(line) for line in f]
        assert len(rows)==29*3*3*2
        assert all(r['provenance_complete'] for r in rows)
        assert all(r['cache_hit']==(r['cache_mode']=='warm') for r in rows)
        assert all(r['status']=='correct_abstention' for r in rows if not r['answerable'])
        assert any(p['phase']=='load_existing_pca_coordinates' and p['file_read_bytes']>0 for p in json.loads((tmp_path/name/'preparation.json').read_text()))
        outputs.append(manifest['deterministic_results_digest'])
    assert outputs[0]==outputs[1]
    with pytest.raises(FileExistsError):
        run_benchmark(path,tmp_path/'first',upstream=backend.upstream,upstream_python=os.environ['FIRE_VASE_PYTHON'],repository_root=ROOT)


def test_typed_feature_and_coordinate_contracts_reject_invalid_payloads(dataset):
    from dataset_prototype.embedding_study.contracts import DevelopmentalFeatures, CoordinateArtifact
    with pytest.raises(ValidationError):
        DevelopmentalFeatures(history_digest=digest(dataset.histories[0]),profile=[0]*20,traits={})
    with pytest.raises(ValidationError,match='dimension'):
        CoordinateArtifact(version='fire-vase-coordinates-v1',artifact_digest='a'*64,dataset_digest='b'*64,dimensions=3,coordinates={'x':[1,2]})


def test_unavailable_or_wrong_upstream_is_not_mocked(tmp_path):
    import sys
    with pytest.raises((ValueError, __import__('subprocess').CalledProcessError)):
        UpstreamBackend(ROOT,sys.executable)
    config=json.loads(CONFIG.read_text());config['repeats']=1
    path=tmp_path/'config.json';path.write_text(json.dumps(config))
    with pytest.raises((ValueError, __import__('subprocess').CalledProcessError)):
        run_benchmark(path,tmp_path/'failed',upstream=ROOT,upstream_python=sys.executable,repository_root=ROOT)
    manifest=json.loads((tmp_path/'failed/manifest.json').read_text())
    assert manifest['status']=='failed' and manifest['agent_calls']==0


def test_empty_training_cohort_fails_before_any_fit(dataset):
    data=dataset.model_dump(mode='json')
    for history in data['histories']:
        history['split']='evaluation'
    with pytest.raises(ValueError,match='training fires'):
        ReferenceAnswers(Dataset.model_validate(data),3)
