from datetime import timedelta
import json
import pytest
from pydantic import ValidationError
from dataset_prototype.discovery import run
from dataset_prototype.adapters import MockMESAClient, MESAClient
from dataset_prototype.contracts import SourceResource, Support


def test_search_contract_and_determinism(client, request_model):
    first = run(request_model, client)
    assert first == run(request_model, client)
    assert len(first.candidates) == 2
    for c in first.candidates:
        assert c.rationale
        assert c.resource.version == 'fixture-1'
        assert c.resource.rights.redistribution is True
        assert c.resource.metadata.original_identifier.startswith('synthetic:')
        assert client.get_provenance(c.resource.asset_id)
        assert client.fetch(c.resource.asset_id)


@pytest.mark.parametrize('field,value', [('modalities',('flux',)), ('variables',('unknown',))])
def test_filter(client, request_model, field, value):
    assert not run(request_model.model_copy(update={field:value}),client).candidates


def test_spatial_temporal_filters(client, request_model):
    s=request_model.support
    for support in [s.model_copy(update={'bbox':(0,0,1,1)}),s.model_copy(update={'start':s.start+timedelta(days=20),'end':s.end+timedelta(days=20)})]:
        result=run(request_model.model_copy(update={'support':support}),client)
        assert not result.candidates and result.warnings


def test_missing_metadata_rejected(client):
    source=client.resources[0].model_dump(mode='json'); del source['rights']
    with pytest.raises(ValidationError): SourceResource.model_validate(source)
    with pytest.raises(LookupError): client.fetch('absent')


def test_duplicate_results(client,request_model):
    class Duplicate:
        def search(self,request): return client.resources*2
    assert len(run(request_model,Duplicate()).candidates)==2
    class Conflict:
        def search(self,request): return (client.resources[0],client.resources[0].model_copy(update={'dataset':'conflict'}))
    with pytest.raises(ValueError,match='conflicting'): run(request_model,Conflict())


def test_source_checksum_and_immutable_models(client,tmp_path):
    r=client.resources[0]
    with pytest.raises(ValidationError): r.version='changed'
    with pytest.raises(ValidationError): r.rights.license='changed'
    root=tmp_path
    (root/'catalog.json').write_text(json.dumps([r.model_dump(mode='json')]))
    (root/'neon').mkdir(); (root/r.uri).write_text('[]')
    with pytest.raises(ValueError,match='checksum'): MockMESAClient(root).fetch(r.asset_id)


def test_mesa_does_not_invent_api():
    for name in ['search','describe','fetch','register','get_provenance']:
        with pytest.raises(NotImplementedError,match='unverified'): getattr(MESAClient(),name)('test')


def test_invalid_support():
    with pytest.raises(ValidationError): Support(bbox=[2,0,1,1],start='2023-01-01T00:00:00Z',end='2023-01-02T00:00:00Z',spatial='plot',temporal='daily')


def test_satellite_identity_support_and_original_ids(client):
    satellite=client.describe('fixture-sentinel')
    assert satellite.metadata.sensor=='MSI fixture'
    assert satellite.metadata.platform=='Sentinel-2 fixture'
    assert satellite.metadata.stac_version=='1.0.0'
    assert satellite.support.spatial=='synthetic_common_footprint'
    assert satellite.support.temporal=='daily'
    raw=client.fetch(satellite.asset_id)[0]
    assert raw.asset_id==satellite.asset_id and raw.record_id=='sentinel-0'
