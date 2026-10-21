"""Isolated, version-matched OpenClaw + Verde runtime management.

Reuses an installed image, reads only explicit Verde settings from a trusted env
file, and never mounts project data, the existing working group, or Docker socket.
"""
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
from urllib.parse import urlsplit
from .contracts import digest

CONTAINER = "dataset-prototype-openclaw"
PORT = 18891
SUPPORTED_VERSION = "2026.5.18"


def read_verde_settings(path):
    keys={"VERDE_LLM_BASE_URL","VERDE_LLM_API_KEY","VERDE_LLM_DEFAULT_MODEL"}
    values={k:os.environ[k] for k in keys if os.environ.get(k)}
    for line in Path(path).read_text().splitlines():
        match=re.fullmatch(r"\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*",line)
        if match and match[1] in keys and match[1] not in values:
            value=match[2]
            if len(value)>=2 and value[0]==value[-1] and value[0] in "\"'": value=value[1:-1]
            values[match[1]]=value
    if any(not values.get(k) or any(c in values[k] for c in "\r\n") or values[k].startswith('${') for k in keys):
        raise ValueError("Verde URL, key and model must be explicitly configured; env file is read as data, not executed")
    parsed=urlsplit(values['VERDE_LLM_BASE_URL'])
    if parsed.scheme!='https' or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Verde base URL must be HTTPS without embedded credentials/query")
    if not re.fullmatch(r"[A-Za-z0-9_./:-]+",values['VERDE_LLM_DEFAULT_MODEL']):
        raise ValueError("invalid configured Verde model identifier")
    return values


def runtime_config(base_url,model):
    route=f"verde/{model}"
    return {
        "gateway":{"mode":"local","bind":"lan","port":PORT,"controlUi":{"allowedOrigins":[f"http://127.0.0.1:{PORT}",f"http://localhost:{PORT}"]},"auth":{"mode":"token","token":"${OPENCLAW_GATEWAY_TOKEN}"}},
        "models":{"mode":"replace","providers":{"verde":{"baseUrl":base_url,"apiKey":"${VERDE_LLM_API_KEY}","api":"openai-completions",
            "models":[{"id":model,"name":model,"reasoning":False,"input":["text"],"contextWindow":32768,"maxTokens":4096,"compat":{"supportsTools":False}}]}}},
        "agents":{"defaults":{"model":{"primary":route,"fallbacks":[]},"workspace":"/prototype/workspace","skipBootstrap":True,"heartbeat":{"every":"0m"},"compaction":{"reserveTokens":8192,"reserveTokensFloor":8192}},
            "list":[{"id":f"prototype-{role}","name":role,"model":route} for role in ["discovery","semantic","units","support","rights","integrity","quality","harmonization","qa"]]},
        "tools":{"allow":["llm-task"]},
        "plugins":{"allow":["llm-task"],"entries":{"llm-task":{"enabled":True,"config":{"defaultProvider":"verde","defaultModel":route,
            "allowedModels":[route],"maxTokens":4096,"timeoutMs":120000}}}},
        "channels":{},
        "update":{"checkOnStart":False},
    }


def _docker(args,**kwargs):
    result=subprocess.run(["docker",*args],capture_output=True,text=True,**kwargs)
    if result.returncode:
        # Docker diagnostics may quote environment/config values. Never return
        # raw stderr from credential-bearing runtime setup to a chat or log.
        raise ValueError(f"Docker operation failed ({args[0]}); inspect runtime state locally without disclosing secrets")
    return result.stdout.strip()


def start_runtime(env_file,root=Path('run/openclaw'),image='openclaw-local:latest'):
    root=Path(root).resolve()
    if not re.fullmatch(r"[A-Za-z0-9_./:@-]+",image):raise ValueError("invalid image identifier")
    values=read_verde_settings(env_file)
    version=_docker(['run','--rm','--entrypoint','openclaw',image,'--version'],timeout=30)
    if SUPPORTED_VERSION not in version:
        raise ValueError("OpenClaw version not verified; inspect plugin/schema before upgrading this adapter")
    existing=_docker(['ps','-a','--filter',f'name=^/{CONTAINER}$','--format','{{.Names}}'])
    if existing:
        raise ValueError("isolated prototype container already exists; use status or stop it explicitly before reconfiguration")
    root.mkdir(parents=True,exist_ok=True);root.chmod(0o700)
    for name in ['state','workspace']:(root/name).mkdir(exist_ok=True)
    config=runtime_config(values['VERDE_LLM_BASE_URL'],values['VERDE_LLM_DEFAULT_MODEL'])
    history=root/'config-history';history.mkdir(exist_ok=True)
    if (root/'openclaw.json').exists():
        old=json.loads((root/'openclaw.json').read_text())
        (history/f'{digest(old)}.json').write_text(json.dumps(old,indent=2)+'\n')
    (root/'openclaw.json').write_text(json.dumps(config,indent=2)+'\n')
    (history/f'{digest(config)}.json').write_text(json.dumps(config,indent=2)+'\n')
    token_path=root/'gateway-token'
    token=secrets.token_urlsafe(40)
    token_path.write_text(token);token_path.chmod(0o600)
    env_path=root/'runtime.env'
    env_values={'VERDE_LLM_API_KEY':values['VERDE_LLM_API_KEY'],'OPENCLAW_GATEWAY_TOKEN':token,
                'OPENCLAW_STATE_DIR':'/prototype/state','OPENCLAW_CONFIG_PATH':'/prototype/openclaw.json','OPENCLAW_DISABLE_BONJOUR':'1'}
    env_path.write_text(''.join(f'{k}={v}\n' for k,v in env_values.items()));env_path.chmod(0o600)
    common=['--env-file',str(env_path),'--mount',f'type=bind,src={root / "openclaw.json"},dst=/prototype/openclaw.json,readonly',
            '--mount',f'type=bind,src={root / "state"},dst=/prototype/state',
            '--mount',f'type=bind,src={root / "workspace"},dst=/prototype/workspace']
    # Validate with the actual installed schema before starting a service.
    _docker(['run','--rm',*common,'--entrypoint','openclaw',image,'config','validate'],timeout=30)
    identifier=_docker(['run','-d','--name',CONTAINER,'--label','dataset-prototype.runtime=true','--read-only','--cap-drop','ALL',
        '--security-opt','no-new-privileges','--pids-limit','256','--cpus','2','--memory','4g','--tmpfs','/tmp:rw,nosuid,size=512m',
        '-p',f'127.0.0.1:{PORT}:{PORT}',*common,'--entrypoint','openclaw',image,'gateway','run','--port',str(PORT)],timeout=30)
    image_id=_docker(['image','inspect',image,'--format','{{.Id}}'])
    public={'container':CONTAINER,'container_id':identifier,'image':image,'image_id':image_id,'openclaw_version':SUPPORTED_VERSION,
        'endpoint':f'http://127.0.0.1:{PORT}','provider':'verde','model':values['VERDE_LLM_DEFAULT_MODEL'],
        'config_digest':digest(config),'plugin':'llm-task','tools_exposed_to_model':False,'token_file':'gateway-token',
        'provider_model_digest':None,'response_scope':'OpenClaw plugin-validated JSON; raw provider text and usage are not exposed by this plugin version'}
    (root/'runtime.json').write_text(json.dumps(public,indent=2)+'\n')
    return public


def stop_runtime():
    label=_docker(['inspect',CONTAINER,'--format','{{index .Config.Labels "dataset-prototype.runtime"}}'])
    if label!='true':raise ValueError("refusing to stop a container not owned by this adapter")
    _docker(['stop',CONTAINER],timeout=30)
    _docker(['rm',CONTAINER],timeout=30)


def runtime_status(root=Path('run/openclaw')):
    public=json.loads((Path(root)/'runtime.json').read_text())
    result=subprocess.run(['docker','inspect',CONTAINER,'--format','{{.State.Status}}'],capture_output=True,text=True)
    public['container_state']=result.stdout.strip() if result.returncode==0 else 'not present or Docker unavailable'
    public['gateway_readiness']='not probed; container state alone does not prove provider inference'
    return public
