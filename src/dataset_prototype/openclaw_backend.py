"""OpenClaw llm-task transport using the isolated Verde runtime.

This is an OpenClaw integration, not a direct call to Verde disguised as one.
The installed plugin supplies tool-free inference plus JSON Schema validation.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
from .contracts import digest
from .model_agents import AgentTrace, SYSTEM
from .network import request_json


class OpenClawBackend:
    backend_name='openclaw-llm-task'
    configuration='bounded-science-v1; OpenClaw llm-task; Verde; no model tools; no fallback'

    def __init__(self, runtime=Path('run/openclaw'), *, http=request_json, timeout=150):
        self.root=Path(runtime)
        self.runtime=json.loads((self.root/'runtime.json').read_text())
        config=json.loads((self.root/'openclaw.json').read_text())
        if digest(config)!=self.runtime['config_digest'] or config['tools']['allow']!=['llm-task']:
            raise ValueError('OpenClaw configuration changed; revalidate the isolated runtime')
        if self.runtime['tools_exposed_to_model'] is not False or self.runtime['plugin']!='llm-task' or self.runtime['openclaw_version']!='2026.5.18':
            raise ValueError('runtime contract is not verified for this OpenClaw plugin')
        self.model=self.runtime['model']
        self.provider=self.runtime['provider']
        if self.provider!='verde' or config['plugins']['entries']['llm-task']['config']['allowedModels']!=[f'verde/{self.model}']:
            raise ValueError('runtime does not restrict inference to the configured Verde model')
        self.endpoint=self.runtime['endpoint']
        from urllib.parse import urlsplit
        url=urlsplit(self.endpoint)
        if url.scheme!='http' or url.hostname not in {'127.0.0.1','localhost','::1'} or url.username or url.password or url.query or url.fragment:
            raise ValueError('isolated gateway must use an explicit loopback endpoint')
        self._token=(self.root/'gateway-token').read_text().strip()
        if not self._token:raise ValueError('missing gateway credential')
        self._model_digest='not-exposed-by-Verde'
        self.http=http
        self.timeout=timeout
        self.traces=[]

    def generate(self,role,instruction,evidence,schema):
        if role not in {'discovery','semantic','units','support','rights','harmonization','qa'}:
            raise ValueError('unknown bounded agent role')
        args={'prompt':SYSTEM+'\n\n'+instruction,
              'input':{'role':role,'evidence':evidence,'output_schema':schema.model_json_schema()},
              'schema':schema.model_json_schema(),'provider':self.provider,'model':f'{self.provider}/{self.model}',
              'temperature':0,'maxTokens':4096,'timeoutMs':120000}
        payload={'tool':'llm-task','sessionKey':f'agent:prototype-{role}:main','args':args}
        prompt=json.dumps(payload,sort_keys=True,allow_nan=False)
        if len(prompt.encode())>48_000:raise ValueError('task exceeds bounded request budget; reduce metadata/dialogue scope')
        raw=None;content='';failure=None
        try:
            raw=self.http(self.endpoint+'/tools/invoke',payload=payload,headers={'Authorization':'Bearer '+self._token},
                          timeout=self.timeout,max_bytes=2_000_000)
            result=raw.get('result',{})
            if raw.get('ok') is not True or result.get('isError'):
                raise ValueError('OpenClaw task failed; inspect gateway response in transcript')
            details=result.get('details',{})
            if details.get('provider')!=self.provider or details.get('model')!=self.model:
                raise ValueError('OpenClaw returned a different provider/model; no fallback permitted')
            if 'json' not in details:raise ValueError('OpenClaw did not return plugin-validated JSON')
            content=json.dumps(details['json'],sort_keys=True,allow_nan=False)
            return schema.model_validate_json(content)
        except Exception as error:
            failure=type(error).__name__
            raise
        finally:
            self.traces.append(AgentTrace(role=role,backend=self.backend_name,model=self.model,model_digest=self._model_digest,
                prompt_digest=digest(prompt),response_digest=digest(content),input_json=prompt,output_json=content,
                timestamp=datetime.now(timezone.utc),error=failure,response_status='failed' if failure else 'plugin_schema_validated',
                runtime_version=self.runtime['openclaw_version'],runtime_config_digest=self.runtime['config_digest'],provider=self.provider,
                response_scope='gateway_validated_json',runtime_response_json=json.dumps(raw,sort_keys=True) if raw is not None else None))
