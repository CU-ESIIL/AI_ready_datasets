from pathlib import Path
import json
import pytest
from dataset_prototype.orchestration import run,load_track
from dataset_prototype.contracts import Representation, HarmonizedObservation
from dataset_prototype.cli import main
from dataset_prototype.storage import cached


@pytest.mark.parametrize('track',['food_security','water_security'])
def test_complete_offline_pipeline(client,tmp_path,track):
    config=load_track(Path('tracks')/track/'config.json')
    out=run(config,client,tmp_path/'outputs',tmp_path/'cache')
    manifest=json.loads((out/'run_manifest.json').read_text())
    assert manifest['fixture'] and manifest['track']['track']==track
    observations=[HarmonizedObservation.model_validate(x) for x in json.loads((out/'harmonized.json').read_text())]
    vectors=[Representation.model_validate(x) for x in json.loads((out/'representations.json').read_text())]
    assert {x.modality for x in vectors}=={'field','satellite'}
    assert len(vectors)==len(observations)==6
    by_id={x.observation_id:x for x in observations}
    for rep in vectors:
        assert rep.track==track
        for ident,lineage in zip(rep.observation_ids,rep.provenance):
            assert ident in by_id and lineage.recipe.track==track
            assert lineage.recipe.scope=='track'
            assert lineage.parent_observations and lineage.parent_lineage
            assert lineage.parent_lineage[0].recipe.scope=='core'
            assert lineage.source.rights.license=='CC0-1.0'
            assert lineage.source_records[0].value is not None
    downstream=json.loads((out/'downstream.json').read_text())
    assert downstream['pairs']==3 and downstream['fixture_only']
    assert (out/'provenance.jsonld').stat().st_size>0


def test_independence_and_shared_cache(client,tmp_path):
    configs=[load_track(f'tracks/{t}/config.json') for t in ['food_security','water_security']]
    before={p:p.read_bytes() for p in Path('tracks').rglob('*.json')}
    one=run(configs[0],client,tmp_path/'outputs',tmp_path/'cache')
    snapshots={p:p.read_bytes() for p in one.iterdir()}
    cache_before={p:p.read_bytes() for p in (tmp_path/'cache').rglob('*.json')}
    two=run(configs[1],client,tmp_path/'outputs',tmp_path/'cache')
    assert all(p.read_bytes()==value for p,value in snapshots.items())
    assert all(p.read_bytes()==value for p,value in before.items())
    assert {p:p.read_bytes() for p in (tmp_path/'cache').rglob('*.json')}==cache_before
    a=json.loads((one/'run_manifest.json').read_text()); b=json.loads((two/'run_manifest.json').read_text())
    assert a['cache_keys']==b['cache_keys']
    reverse=run(configs[0],client,tmp_path/'repeat',tmp_path/'cache')
    assert all((reverse/p.name).read_bytes()==value for p,value in snapshots.items())
    with pytest.raises(FileExistsError): run(configs[0],client,tmp_path/'outputs',tmp_path/'cache')


def test_new_track_configuration_only(client,tmp_path):
    third=load_track('tracks/third_track/config.json')
    with pytest.raises(ValueError,match='not finalized'): run(third,client,tmp_path/'outputs',tmp_path/'cache')
    third=third.model_copy(update={'enabled':True,'track':'new_fixture_track'})
    assert run(third,client,tmp_path/'outputs',tmp_path/'cache').name=='new_fixture_track'


def test_missing_required_variable(client,tmp_path,config):
    with pytest.raises(ValueError,match='required track variables'):
        run(config.model_copy(update={'variables':config.variables+('absent',)}),client,tmp_path/'outputs',tmp_path/'cache')


def test_cli(tmp_path,capsys):
    main(['run','--all-tracks','--output',str(tmp_path/'out'),'--cache',str(tmp_path/'cache')])
    assert 'water_security' in capsys.readouterr().out
    main(['schema','HarmonizationRecipe','--output',str(tmp_path/'schema.json')])
    assert json.loads((tmp_path/'schema.json').read_text())['additionalProperties'] is False
    main(['discover',str(tmp_path/'out/food_security/request.json'),'--output',str(tmp_path/'discovery.json')])
    assert len(json.loads((tmp_path/'discovery.json').read_text())['candidates'])==2
    with pytest.raises(SystemExit) as exc:
        main(['run','--track','third_track','--output',str(tmp_path/'another')])
    assert exc.value.code==2


def test_cache_corruption(tmp_path):
    value,key=cached(tmp_path,{'identity':1},lambda: {'value':1})
    assert cached(tmp_path,{'identity':1},lambda: None)==(value,key)
    assert cached(tmp_path,{'identity':2},lambda: {'value':1})[1]!=key
    path=tmp_path/'index'/f'{key}.json'
    saved=json.loads(path.read_text()); saved['value']={'value':99}; path.write_text(json.dumps(saved))
    with pytest.raises(ValueError,match='corrupted'): cached(tmp_path,{'identity':1},lambda: None)


def test_second_track_reuses_acquisition_and_core_execution(client,tmp_path,monkeypatch):
    run(load_track('tracks/food_security/config.json'),client,tmp_path/'out',tmp_path/'cache')
    def forbidden(*args,**kwargs):
        raise AssertionError('shared acquisition/core execution should be reused')
    monkeypatch.setattr(client,'fetch',forbidden)
    from dataset_prototype import orchestration
    original=orchestration.harmonization.run
    def no_core(resources,recipe,*args,**kwargs):
        assert recipe.scope!='core'
        return original(resources,recipe,*args,**kwargs)
    monkeypatch.setattr(orchestration.harmonization,'run',no_core)
    assert run(load_track('tracks/water_security/config.json'),client,tmp_path/'out',tmp_path/'cache')


def test_independent_stage_cli(bundle,tmp_path):
    r,m,recipe,raw=bundle
    def save(name,value):
        path=tmp_path/name; path.write_text(json.dumps(value)); return str(path)
    recipe_path=save('recipe.json',recipe.model_dump(mode='json'))
    sources_path=save('sources.json',[r.model_dump(mode='json')])
    records_path=save('records.json',[x.model_dump(mode='json') for x in raw])
    main(['qa',recipe_path,sources_path,'--output',str(tmp_path/'qa.json')])
    assert json.loads((tmp_path/'qa.json').read_text())['outcome']=='approve'
    main(['review',recipe_path,'--reviewer','Fixture test','--rationale','Curated identity','--decision','approved','--output',str(tmp_path/'review.json')])
    main(['harmonize',recipe_path,sources_path,records_path,'--review',str(tmp_path/'review.json'),'--output',str(tmp_path/'obs.json')])
    main(['encode',str(tmp_path/'obs.json'),'--output',str(tmp_path/'vectors.json')])
    assert len(json.loads((tmp_path/'vectors.json').read_text()))==3
