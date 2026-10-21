"""Version-matched OpenClaw boundary tests; no Docker or remote API required."""
import json
from pathlib import Path
import pytest
from dataset_prototype.contracts import digest
from dataset_prototype.model_agents import CandidateChoice
from dataset_prototype.openclaw_backend import OpenClawBackend
from dataset_prototype.openclaw_runtime import runtime_config, read_verde_settings


@pytest.fixture
def runtime(tmp_path):
    config=runtime_config('https://llm-api.cyverse.ai/v1','js2/gpt-oss-120b')
    (tmp_path/'openclaw.json').write_text(json.dumps(config))
    (tmp_path/'gateway-token').write_text('test-only-gateway-token')
    record={'config_digest':digest(config),'tools_exposed_to_model':False,'plugin':'llm-task','openclaw_version':'2026.5.18',
            'provider':'verde','model':'js2/gpt-oss-120b','endpoint':'http://127.0.0.1:18891'}
    (tmp_path/'runtime.json').write_text(json.dumps(record))
    return tmp_path


def test_isolated_config_has_no_fallback_or_model_tools():
    cfg=runtime_config('https://llm-api.cyverse.ai/v1','js2/gpt-oss-120b')
    assert cfg['tools']['allow']==['llm-task']
    assert cfg['agents']['defaults']['model']['fallbacks']==[]
    assert cfg['agents']['defaults']['heartbeat']['every']=='0m'
    assert cfg['agents']['defaults']['compaction']=={'reserveTokens':8192,'reserveTokensFloor':8192}
    assert cfg['channels']=={}
    provider=cfg['models']['providers']['verde']
    assert provider['apiKey']=='${VERDE_LLM_API_KEY}'
    assert provider['models'][0]['compat']['supportsTools'] is False
    assert cfg['plugins']['entries']['llm-task']['config']['defaultModel']=='verde/js2/gpt-oss-120b'
    assert len(cfg['agents']['list'])==9


def test_credentials_read_as_data_never_executed(tmp_path,monkeypatch):
    for name in ['VERDE_LLM_BASE_URL','VERDE_LLM_API_KEY','VERDE_LLM_DEFAULT_MODEL']:monkeypatch.delenv(name,raising=False)
    path=tmp_path/'verde.env'
    path.write_text('VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1\nVERDE_LLM_API_KEY="test-key-$(never-execute)"\nVERDE_LLM_DEFAULT_MODEL=js2/gpt-oss-120b\nSLACK_BOT_TOKEN=do-not-copy\n')
    settings=read_verde_settings(path)
    assert settings['VERDE_LLM_API_KEY']=='test-key-$(never-execute)'
    assert 'SLACK_BOT_TOKEN' not in settings
    path.write_text('VERDE_LLM_BASE_URL=http://untrusted.example\nVERDE_LLM_API_KEY=test\nVERDE_LLM_DEFAULT_MODEL=m\n')
    with pytest.raises(ValueError,match='HTTPS'):read_verde_settings(path)


def test_gateway_calls_plugin_not_direct_verde(runtime):
    calls=[]
    def http(url,**kwargs):
        calls.append((url,kwargs));args=kwargs['payload']['args']
        assert url=='http://127.0.0.1:18891/tools/invoke'
        assert kwargs['payload']['tool']=='llm-task'
        assert kwargs['payload']['sessionKey']=='agent:prototype-discovery:main'
        assert args['model']=='verde/js2/gpt-oss-120b' and args['provider']=='verde'
        assert args['schema']['additionalProperties'] is False
        return {'ok':True,'result':{'details':{'provider':'verde','model':'js2/gpt-oss-120b','json':{'asset_ids':[],'rationale':'Abstain'}}}}
    backend=OpenClawBackend(runtime,http=http)
    assert backend.generate('discovery','Choose candidates',{},CandidateChoice).asset_ids==()
    trace=backend.traces[0]
    assert trace.backend=='openclaw-llm-task' and trace.provider=='verde'
    assert trace.model_digest=='not-exposed-by-Verde'
    assert trace.response_scope=='gateway_validated_json'
    assert trace.runtime_version=='2026.5.18'
    assert 'test-only-gateway-token' not in trace.model_dump_json()
    assert trace.input_tokens is None and trace.output_tokens is None


@pytest.mark.parametrize('response',[
 {'ok':True,'result':{'details':{'provider':'other','model':'js2/gpt-oss-120b','json':{}}}},
 {'ok':True,'result':{'details':{'provider':'verde','model':'fallback','json':{}}}},
 {'ok':False,'error':{'message':'failed'}},
 {'ok':True,'result':{'isError':True,'content':[]}},
 {'ok':True,'result':{'details':{'provider':'verde','model':'js2/gpt-oss-120b','json':{'invalid':1}}}}
])
def test_gateway_failure_or_substitution_never_falls_back(runtime,response):
    backend=OpenClawBackend(runtime,http=lambda *a,**k:response)
    with pytest.raises(ValueError):backend.generate('qa','Critique',{},CandidateChoice)
    assert len(backend.traces)==1 and backend.traces[0].error


def test_modified_runtime_or_extra_tools_rejected(runtime):
    cfg=json.loads((runtime/'openclaw.json').read_text());cfg['tools']['allow'].append('exec')
    (runtime/'openclaw.json').write_text(json.dumps(cfg))
    with pytest.raises(ValueError,match='configuration changed'):OpenClawBackend(runtime)


def test_credentials_never_follow_cross_origin_redirects():
    from urllib.request import Request
    from dataset_prototype.network import CredentialRedirectGuard,AccessError
    guard=CredentialRedirectGuard()
    request=Request('http://127.0.0.1:18891/tools/invoke',headers={'Authorization':'Bearer test-only'})
    with pytest.raises(AccessError,match='another origin'):
        guard.redirect_request(request,None,302,'Found',{},'https://untrusted.example/collect')
