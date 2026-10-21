# OpenClaw with the Verde API

The prototype now has a separate `OpenClawBackend` that invokes the actual
OpenClaw **`llm-task` plugin through `/tools/invoke`**. It does not call Verde
directly and label that an OpenClaw run. The same four bounded role contracts,
scientific QA, model-review veto, and human-review requirements remain in place.

## Runtime boundary

The adapter targets the already installed `openclaw-local:latest` image containing
OpenClaw **2026.5.18**. Its installed documentation and plugin implementation were
inspected before choosing this interface. The plugin runs prompt-only inference
with `disableTools: true`, validates JSON Schema, and returns parsed JSON together
with the actual provider/model. Other OpenClaw versions require explicit inspection
and adapter tests; setup fails instead of assuming newer documentation applies.

The isolated `dataset-prototype-openclaw` container has:

- A gateway published on **127.0.0.1:18891** with generated bearer authentication.
- Only the `llm-task` plugin/tool allow-listed; no tools exposed to the inference.
- Verde as its sole provider/model route, with no fallback models.
- Four role identifiers and independent prompt-only role calls.
- No Slack/channels, scheduled model heartbeat, existing working-group state,
  repository data, home directory, or Docker socket mounted.
- Separate writable runtime state and an empty workspace under ignored `run/`;
  a read-only container filesystem, dropped capabilities and resource limits.

The container listens on its internal network interface so Docker port forwarding
works; only the host loopback interface is published. Gateway authentication is
operator-level for this isolated instance, not a per-role authorization system.
Never publish its port or share its bearer token with untrusted clients.

## Start, inspect, and use

Docker must be running, and the existing image must be installed. No image build,
model download, or OpenClaw upgrade is performed automatically.

```bash
prototype openclaw start --verde-env /path/to/openclaw_container/.env
prototype openclaw status
prototype propose run/real-sentinel --backend openclaw \
  --runtime run/openclaw --output run/my-openclaw-proposal
```

`run/real-sentinel` is an acquired, checksummed snapshot from
[the real-data workflow](real-data-agents.md). Use a fresh output directory each run.
Allow the gateway a few seconds to finish startup before calling it. Status reports
container state and configuration; it does not prove successful provider inference.
The proposal command is the live contract test.

The trusted env file must contain:

```dotenv
VERDE_LLM_BASE_URL=https://llm-api.cyverse.ai/v1
VERDE_LLM_API_KEY=YOUR_LOCAL_KEY
VERDE_LLM_DEFAULT_MODEL=js2/gpt-oss-120b
```

These are configuration examples, not a request to place real keys in tracked
files. The operator's process environment takes precedence. The reader selects
only these three fields and never executes shell expressions from the file.
Slack and other credentials are not copied. A private generated runtime env file
contains only the credential and variables needed by this isolated gateway.
`run/` is ignored, its runtime directory has mode 0700, and credential files have
mode 0600. Docker administrators remain trusted and can inspect container secrets.

The existing key and `js2/gpt-oss-120b` availability were verified using the
configured Verde `/models` endpoint. Use the URL granted to your team: current
[AI-VERDE documentation](https://aiverde-docs.cyverse.ai/api/) also describes a newer
generic base URL, so do not rewrite a working team configuration from an example.

To stop just this prototype runtime while retaining its artifacts:

```bash
prototype openclaw stop
```

Stop verifies the container's ownership label. The existing working-group containers,
models, Slack setup, sibling repository and credentials are not reconfigured.
Starting again requires an explicit stop first; old configuration digests are
retained under the ignored runtime's `config-history/` directory.

## Compatibility findings

The installed version resolves bare `js2/gpt-oss-120b` as a provider-qualified
reference. Task requests must instead use `verde/js2/gpt-oss-120b`. The response
must identify provider `verde` and model `js2/gpt-oss-120b`; substitutions fail.

Verde's server rejected an empty `tools: []` array. The installed OpenClaw model
schema supports `compat.supportsTools: false`, which removes the unsupported tool
schema surface while preserving tool-free inference. No dummy tool or execution
capability is introduced to work around this error. Both failed live attempts
were retained in separate proposal directories.

## Evidence and limits

Each role records the exact submitted task envelope, schema, prompt/response
content digests, role, configured and returned provider/model, runtime version,
configuration digest, and returned plugin envelope. Prompt/response references
are attached to recipe proposal evidence. Unknown roles, changed runtime policy,
wrong provider/model, transport failures and invalid JSON/schema results fail
without an Ollama or mock fallback.

This version of the OpenClaw plugin returns **validated, normalized JSON**, not
raw provider text, token usage, or a model-weights digest. It can remove Markdown
fences before parsing. The adapter labels this response scope explicitly,
leaves usage unknown, and records the model digest as unavailable. It does not
misrepresent a configuration/image digest as the model weights or claim an exact
raw-provider transcript. Runtime provenance is additional to scientific provenance.

A completed model call is not approval to transform data. Inspect discovery,
semantic mappings, proposed recipe, model QA, deterministic QA, review status and
traces. All model proposals require human review. QA rejection/revision remains
a veto bound to scientific recipe content.

## Verified live result — 2026-10-21

The four roles completed through this gateway against an actual Sentinel snapshot.
Every response reported provider `verde`, model `js2/gpt-oss-120b`, and passed both
plugin and client contract validation. The local artifacts are under
`run/openclaw-verde-no-tools/`, including all four traces and prompt/response references.

Model QA returned `request_revision`, raising calibration/target-context, license
label, and alignment-evidence concerns. Some claims may reflect model confusion
about the intentionally retained raw-DN target; they require expert evaluation,
not silent acceptance as scientific fact. Deterministic QA enforced the veto and
no harmonized data or representations were executed from this proposal. Runtime
integration success is separate from scientific recipe acceptance.

The gateway is left running for subsequent work. `prototype openclaw status` shows
its current container state; `prototype openclaw stop` stops only this isolated
instance. The expanded offline suite passes 79 tests, and the strict documentation
build succeeds.

## Metadata specialists and context budget

The streaming module adds units, support, and rights specialists alongside semantic
analysis, recipe construction, and adversarial QA. Their shared dialogue is
metadata-only; see [streaming harmonization](streaming-harmonization.md).

A live multi-review run exposed the installed runtime's default 20,000-token
compaction reserve within the configured 32,768-token context window. A roughly
13,182-token prompt then failed the gateway precheck, returning HTTP 500/empty
output. Inspection of the installed schema and session-management documentation
confirmed `agents.defaults.compaction.reserveTokens` and `reserveTokensFloor`.
Both are now 8,192 for this tool-free one-shot runtime, above the task's 4,096-token
output cap. The request byte limit still applies, and oversized contexts fail
rather than silently removing scientific evidence. Runtime configuration history
and failed task transcripts remain retained.

## Deterministic backbone and model trust

VERDE interprets, selects, parameterizes, compares and proposes. It does not author
scientific computation. New model plans select closed, source-bound capabilities;
metadata coefficients and mathematical operations are resolved by tested code.
Schema validation, scientific checks, existing vetoes and human decisions remain
separate gates. Approved recipes execute without a model. See
[deterministic execution and model trust](architecture/model-trust.md) for the registry, IR contracts,
examples, provenance and current limits.
