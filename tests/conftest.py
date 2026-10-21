from pathlib import Path
import pytest
from dataset_prototype.adapters import MockMESAClient
from dataset_prototype.orchestration import load_track
from dataset_prototype.contracts import ScientificRequest, Operation
from dataset_prototype.agents import SemanticAgent, HarmonizationAgent


@pytest.fixture
def client():
    return MockMESAClient(Path('data/fixtures'))


@pytest.fixture
def config():
    return load_track('tracks/food_security/config.json')


@pytest.fixture
def request_model(config):
    return ScientificRequest(question=config.question, support=config.support, variables=config.variables, modalities=config.modalities)


@pytest.fixture
def bundle(client):
    r = client.resources[0]
    v = r.variables[0]
    mapping = SemanticAgent().propose(r, v.name, v)
    recipe = HarmonizationAgent().propose((mapping,), (Operation(operation='validate', source_variable=v.name),)).model_copy(update={'status':'approved'})
    return r, mapping, recipe, client.fetch(r.asset_id)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    import socket
    def forbidden(*args, **kwargs):
        raise AssertionError('Tests must not access the network')
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    monkeypatch.setattr(socket.socket, 'connect', forbidden)
