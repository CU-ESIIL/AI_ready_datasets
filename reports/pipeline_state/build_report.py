"""Rebuild an evidence-led visual PDF from the local audit snapshot.
No source acquisition, model inference or scientific approval is performed here.
"""
import csv,json,hashlib,textwrap
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from matplotlib.colors import ListedColormap
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).parent
D=HERE/'data'; F=HERE/'figures'; F.mkdir(exist_ok=True)
load=lambda n:json.loads((D/n).read_text())
M=load('metrics.json'); B=load('benchmark_tables.json'); OPS=load('operations.json'); INV=load('component_inventory.json'); V=load('verification.json'); MAN=load('run_manifest.json'); S=load('sentinel_example.json')
R=list(csv.DictReader((ROOT/'data/semantics/semantic_resources.csv').open()))
GREEN='#194B43'; MINT='#A8C6B8'; GOLD='#B77E35'; INK='#20333A'; GRAY='#D8DFDA'; CREAM='#F5F3EB'; RED='#97513E'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':INK,'text.color':INK,'xtick.color':INK,'ytick.color':INK,'savefig.facecolor':CREAM,'figure.facecolor':CREAM,'axes.facecolor':CREAM,'svg.fonttype':'none'})
FIGS=[]; PAGES=[]
def fig(name,draw):
 f,ax=plt.subplots(figsize=(8,4.75));draw(f,ax);f.tight_layout(pad=1.3)
 for ext in ['png','svg']:f.savefig(F/f'{name}.{ext}',dpi=180)
 plt.close(f);FIGS.append(name);return name

def box(ax,x,y,w,h,label,fc=GREEN,fs=11):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.018',facecolor=fc,edgecolor='none'))
 ax.text(x+w/2,y+h/2,label,ha='center',va='center',color='white' if fc in [GREEN,RED] else INK,fontsize=fs)
def arrow(ax,a,b,color=GREEN):ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,color=color,lw=1.5))
def chain(labels,columns=2,connect=True):
 def draw(f,ax):
  ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
  rows=(len(labels)+columns-1)//columns;h=min(.18,.65/rows);w=.82/columns
  for i,label in enumerate(labels):
   row,col=divmod(i,columns);x=.06+col*(.9/columns);y=.87-row*(.86/rows)-h
   box(ax,x,y,w,h,label,fc=GREEN if i%2==0 else MINT,fs=10)
   if connect and col and i:arrow(ax,(x-.06,y+h/2),(x-.01,y+h/2))
   if connect and col==0 and row:arrow(ax,(x+w/2,y+h+.07),(x+w/2,y+h+.012))
 return draw

def horizontal_bars(values,xlabel='Number of records',color=GREEN):
 def draw(f,ax):
  items=sorted(values.items(),key=lambda v:v[1]);labels=[k.replace('_',' ') for k,v in items];nums=[v for k,v in items]
  ax.barh(labels,nums,color=color);ax.set_xlabel(xlabel);ax.set_xlim(0,max(nums)*1.22 if nums else 1)
  for i,v in enumerate(nums):ax.text(v+.15,i,str(v),va='center',fontsize=9)
  ax.tick_params(axis='y',labelsize=9)
 return draw

def page(section,title,deck,figure,takeaway,caption,body,evidence,kind='PROJECT RESULT'):
 PAGES.append(dict(section=section,title=title,deck=deck,figure=figure,takeaway=takeaway,caption=caption,body=body,evidence=evidence,kind=kind))

# 01 cover is rendered separately.
# 02–05: complete story before technical detail.
def problem_draw(f,ax):
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 for x,t in [(.02,'Sensor pixel\n10 m • instant'),(.355,'Field measurement\nplot • interval'),(.69,'Specimen record\norganism • method')]:
  box(ax,x,.72,.28,.19,t,fc=MINT,fs=11);arrow(ax,(x+.14,.70),(.5,.54))
 box(ax,.15,.37,.70,.17,'Different meanings • units • rights • support',fs=12)
 arrow(ax,(.5,.35),(.5,.23));box(ax,.15,.05,.70,.18,'Reviewed comparison → justified synthesis',fc=MINT,fs=12)
problem=fig('01_problem',problem_draw)
page('THE SCIENTIFIC PROBLEM','Finding files is only the beginning',
 'Environmental observations were made by different communities, for different purposes. A shared label does not make two measurements comparable.',problem,
 'Meaning must survive the journey.',
 'Pixels, plots and specimens describe different things. The pipeline keeps their definitions, methods and spatial and temporal support visible before any scientific combination.',
 'We built independently callable discovery, harmonization and representation modules. Models help propose interpretations; deterministic code checks and computes. Human review remains part of the scientific method at uncertain or consequential boundaries.',
 'AGENTS.md; src/dataset_prototype/contracts.py; docs/science.md','PROJECT INTERPRETATION')

def architecture(f,ax):
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 levels=[(.91,'Scientific question'),(.71,'Discovery + access | SourceResource'),(.48,'Harmonization + review | JSON recipe'),(.25,'Validated registry + CubeDynamics'),(.03,'Harmonized observation → MOSAIKS → synthesis')]
 for y,t in levels:box(ax,.08,y,.84,.075,t,fs=11)
 for y,t in levels[:-1]:arrow(ax,(.5,y),( .5,y-.105))
 for x,t in [(.08,'Data discovery'),(.53,'Semantic discovery')]:box(ax,x,.805,.39,.06,t,fc=MINT,fs=10)
 for x,t in [(.03,'Ontology evidence'),(.36,'Scientific comparison'),(.69,'Rights + QA + human')]:box(ax,x,.58,.28,.06,t,fc=MINT,fs=9)
 box(ax,.08,.36,.84,.065,'Verde proposes • schema + science validators constrain',fc=MINT,fs=10)
 box(ax,.08,.14,.84,.065,'Bounded source windows • calibrated upstream • compact lineage',fc=MINT,fs=10)
arch=fig('02_architecture',architecture)
page('EXECUTIVE SUMMARY','A scientific question becomes a reviewed computation',
 'Discover sources. Understand their meaning. Harmonize only with evidence. Stream approved transformations. Represent the result for a defined analysis.',arch,
 'AI proposes. Tested software computes.',
 'The central recipe records scientific intent as typed JSON. CubeDynamics executes a bounded subset of reviewed transformations; MOSAIKS accepts the harmonized raster output.',
 'Today this architecture is demonstrable offline, including the real external CubeDynamics package. Historical Sentinel retrieval and live Verde judgments exist, but the real Sentinel embedding path remains blocked by review. Synthesis science is the intended destination, not a validated result of this prototype.',
 'docs/architecture.md; docs/cubedynamics.md; run/cubedynamics-verified/manifest.json')

def maturity(f,ax):
 names=[r['component'] for r in INV];status=[r['implementation_status'] for r in INV];code={'WORKING':2,'PROTOTYPE':1,'PARTIAL':.5,'BLOCKED':0}
 ax.barh(range(len(names)),[code[s] for s in status],color=[GREEN if s=='WORKING' else MINT if s=='PROTOTYPE' else GOLD if s=='PARTIAL' else RED for s in status]);ax.set_yticks(range(len(names)),[n.replace(' and ',' + ') for n in names],fontsize=8);ax.invert_yaxis();ax.set_xlim(0,3.5);ax.set_xticks([])
 for i,s in enumerate(status):ax.text(code[s]+.06,i,s,va='center',fontsize=8)
 for sp in ax.spines.values():sp.set_visible(False)
status=fig('03_status',maturity)
page('EXECUTIVE SUMMARY','A working prototype, with scientific gates still closed',
 f"The audited code exposes {M['registered_operations']} registered operations, including {M['cube_operations']} CubeDynamics operations. All {M['tests']['passed']} local tests pass in the integration environment.",status,
 'Demonstrable does not mean production ready.',
 'These statuses describe bounded repository capabilities. WORKING refers to a demonstrated local contract; PROTOTYPE indicates implemented but restricted behavior. MESA transport is blocked on a verified deployed interface.',
 'What is missing: an expert-reviewed real-data release, independent downstream labels, broader support-changing representations and scale measurements. The immediate milestone is one approved bounded Sentinel demonstration with complete source, review and representation lineage.',
 'data/component_inventory.json; data/test_results.json; docs/PROTOTYPE_STATUS.md')

real=fig('04_real_thread',chain([f"Real Sentinel-2A B08\n{S['acquisition'][:10]}",f"Retained native pixel\nrow {S['window']['row']} • column {S['window']['col']}",f"Stored value {S['window']['dn']} DN\nSCL class {S['window']['scl']}",'Documented coefficients\nscale 0.0001 • offset −0.1','Current real release\nNEEDS HUMAN REVIEW','Generated parallel path\nCubeDynamics → MOSAIKS'],2))
page('FOLLOW ONE OBSERVATION','A real pixel anchors the story',
 'The retained source evidence is a Sentinel-2A near-infrared pixel acquired on 30 July 2023. The report reuses that historical evidence without another remote read.',real,
 'The real observation and the generated demonstration are separate.',
 'The historical pixel has native EPSG:32613 coordinates, a 10 m footprint and instantaneous support. Its extracted-window checksum covers the retained evidence, not the entire remote raster.',
 'A separate historical review concerns a 15 July Sentinel scene and remains rejected/revision-needed. It is evidence about the review mechanism, not approval of this 30 July pixel. The successful CubeDynamics/MOSAIKS example uses explicitly generated data and fixture approval.',
 'run/real-sentinel/window-0.json; snapshot.json; run/scoped-sentinel-review-v4/report.json')

# Source boundaries.
access=fig('05_access',chain(['Earth Search STAC\nreal metadata + retained reads','Native COG reader\nbounded B08 / SCL windows','NEON product metadata\nreal; authenticated files pending','MESA transport\nBLOCKED; deployed schema unverified','Local fixture transport\nMOCKED, explicit','Core SourceResource\ncommon typed contract'],2,False))
page('DISCOVER','A catalog describes an asset; an adapter preserves its meaning',
 'Discovery records what exists and how it can be accessed. It must also retain sensor, version, license and native scientific metadata.',access,
 'A fixture is not an integrated data source.',
 'Sentinel has actual historical retrieval evidence. NEON metadata access was demonstrated; authenticated observation retrieval and sensor-aware normalization are incomplete. Local fixtures exercise contracts without pretending to be live sources.',
 'STAC is a catalog standard, not the whole architecture [2]. MESA is an external access/metadata boundary; its production integration is not implemented here [4]. This report does not count conceptual adapters as real source integrations.',
 'adapters.py; real_data.py; neon.py; stream_rasters.py; docs/development/integrations.md')

roles=fig('06_responsibilities',chain(['MESA / source infrastructure\naccess • references • metadata','This pipeline\nscientific intent • review • typed recipe','CubeDynamics\nreviewed bounded computation','Harmonized products\ncanonical definitions + lineage','MOSAIKS / storage\nfeatures + compact evidence','Synthesis analysis\nrequires its own validation'],1))
page('SYSTEM RESPONSIBILITIES','Access, scientific decisions and computation have different jobs',
 'The prototype keeps these responsibilities separate so that one system cannot silently substitute for another.',roles,
 'CubeDynamics is an execution dependency, not a discovery replacement.',
 'This is a responsibility diagram. The external MESA arrows are planned boundaries. Current native source readers remain upstream of CubeDynamics; no new CubeDynamics loader is called to duplicate discovery.',
 'CubeDynamics contributes public pipe and verb operations backed by xarray/Dask [1]. This pipeline supplies source identity, reviewed meanings, resource limits and approval gates. A future MESA registration path must be built against verified deployed schemas, not guessed endpoints.',
 'docs/cubedynamics.md; docs/development/integrations.md; adapters.MESAClient','PROJECT INTERPRETATION')

# Meaning and scale.
evidence=fig('07_evidence',horizontal_bars(load('evidence_counts.json')['counts'],'Evidence records in one retained review'))
page('UNDERSTAND','Evidence and judgment are different objects',
 'A source statement, a calculated fact and a model opinion carry different scientific weight. The contracts retain those distinctions.',evidence,
 'Missing evidence remains visible.',
 'Counts use only the seven evidence records in the retained scoped Sentinel review. Zero model-judgment and human-decision bars do not mean the project lacks those artifacts: reviews and decisions are separate objects, outside this array.',
 'SOURCE_DOCUMENTED points to source assertions; DERIVED_DETERMINISTICALLY records reproducible calculations; MISSING_EVIDENCE records unresolved requirements. The source label is not a guarantee of truth: reviewers must check what the underlying document actually supports.',
 'run/scoped-sentinel-review-v4/report.json.evidence; review_contracts.py')
land=fig('08_domains',horizontal_bars(load('inventory_counts.json')['domain'],'Resources in canonical inventory'))
page('SEMANTIC LANDSCAPE','Many communities describe different pieces of an observation',
 f"The local inventory contains {M['semantic_resources']} semantic resources, including ontologies, vocabularies, exchange standards and conceptual frameworks.",land,
 'Semantic diversity is useful context, not scientific equivalence.',
 'Each resource has one inventory domain label; these counts are not global field sizes. Scope and coverage judgments are provisional project assessments, not authoritative ontology properties.',
 'The inventory helps discover candidates for biological entities, traits, environments, observations, space, time, units and provenance. A candidate still needs exact-term and version checks before it can support a mapping. No universal ontology or universal latent space is claimed.',
 'data/semantics/semantic_resources.csv; assessments.jsonl; docs/semantics/index.md')
resourcetypes=fig('09_types',horizontal_bars(load('inventory_counts.json')['resource_type'],'Resources by local type'))
page('SEMANTIC LANDSCAPE','An ontology and a catalog standard solve different problems',
 'The resource inventory deliberately includes more than formal ontologies. Their types explain how each might contribute.',resourcetypes,
 'A standard can organize metadata without establishing biological meaning.',
 'Type counts are derived directly from the canonical CSV. Standards, vocabularies, frameworks and historical efforts remain distinguishable rather than being relabeled as ontologies.',
 'For example, STAC can retain a sensor band description; it does not prove that satellite reflectance and a field trait measure the same quantity. Likewise, a taxonomy identifier helps preserve identity but does not justify aggregation from organisms to communities.',
 'semantic_resources.csv.resource_type; docs/semantics/distinctions.md','PROJECT INTERPRETATION')
history=fig('10_history',chain(['Name things\nNCBI Taxonomy','Describe datasets\nDublin Core • EML','Formalize entities\nBFO • UBERON','Formalize relations\nRO','Describe observations\nOBOE • SOSA / SSN','Connect domains\nENVO • OBI','Compose meaning\nreviewed mappings','Preserve lineage\nPROV-O','Orchestrate systems\nproject research direction'],3))
page('SEMANTIC HISTORY','Meaning has accumulated through different kinds of infrastructure',
 'This conceptual progression explains why several semantic systems may be needed for one scientific question.',history,
 'This is not a strict chronology.',
 'Stages overlap and earlier approaches remain useful. Named examples are inventoried resources; their placement is explanatory rather than a measured historical ranking. The inventory also records origin eras, including unknown dates.',
 'The research direction is to orchestrate existing systems while preserving source meaning. It is not to replace them with a universal biological ontology. Expert review is needed to turn provisional resource assessments into justified scientific mappings.',
 'semantic_resources.csv historical_role, era, canonical_uri; docs/semantics/history.md','PROJECT INTERPRETATION')

def scales(f,ax):
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 rows=[('Structural','cell → tissue → organ → organism'),('Ecological','organism → population → community → ecosystem → biome'),('Spatial','point → plot → site → landscape → region → globe'),('Temporal','instant → interval → day → season → year → decade'),('Observational','sample → measurement → observation → event → inventory')]
 for i,(a,b) in enumerate(rows):
  y=.85-i*.18;ax.text(.02,y,a.upper(),fontsize=10,fontweight='bold');ax.text(.02,y-.065,b,fontsize=11);ax.axhline(y-.1,color=GRAY,lw=1)
scale=fig('11_scale',scales)
page('WHY SCALE IS HARD','Scale is not one dimension',
 'A 10 m pixel is a spatial support. An instantaneous acquisition is a temporal support. Neither identifies a biological organizational level.',scale,
 'Computational alignment is not scientific equivalence.',
 'These parallel conceptual sequences are not interchangeable ladders. A coordinate match can make observations colocated while leaving their methods, quantities and supports scientifically different.',
 'Resolution describes spacing or detail; support describes the region or interval represented by a measurement. The CubeDynamics adapter checks these separately. Its nearest sampling changes spatial support and needs review; it does not infer a field-to-satellite relationship.',
 'contracts.Support; cube_contracts.CubeInput; cubedynamics_backend.py; docs/semantics/scale.md','PROJECT INTERPRETATION')

# Review / IR.
trust=fig('12_trust',chain(['PROBABILISTIC\nVerde interprets / selects / proposes','TRUST BOUNDARY\nno model tools or arbitrary code','JSON validation\nclosed references + typed parameters','Scientific validation\nmeaning • units • support • rights','Human decision + QA\nexact recipe • veto remains binding','DETERMINISTIC\nregistered execution + provenance'],1))
page('WHAT AI IS ALLOWED TO DO','AI proposes. Tested software computes.',
 'Models return scientific judgments and bounded plans. The executor chooses only implementations already present in the reviewed operation registry.',trust,
 'Valid JSON is necessary, but not enough.',
 'Schema checks reject malformed output and unknown choices. Scientific validators check compatibility and evidence. Model proposals require human review; changing scientific content invalidates prior approval.',
 'OpenClaw is an isolated adapter/runtime boundary pinned to 2026.5.18. The Verde route and returned provider/model must match. Historical live inference exists, while the fresh report demonstration uses a fixture decision model and makes no live inference claim.',
 'decision_ir.py; cube_ir.py; model_agents.py; openclaw_backend.py; AGENTS.md')
reviewfig=fig('13_review',chain(['Enough documented evidence?\nif no → evidence collection + review','Compatible scientific intent?\nif uncertain → expert review','Four specialists + QA\nsame frozen backend recipe','All agree and no prior veto?\nif no → revision, no stream','Exact-recipe human approval\nrequired for model proposals','Authorize source access\nthen stream bounded windows'],1))
page('HUMAN GOVERNANCE','A blocked run can be a successful safety test',
 'The retained real Sentinel review asked for revision. No approval, source access or embedding release was fabricated to make the demonstration appear complete.',reviewfig,
 'Disagreement is preserved for scientific analysis.',
 'The six-domain evidence review covers semantics, units, support, rights, integrity and quality. A separate frozen backend consensus involves four specialists and QA. Both are distinct from the human decision.',
 'The historical model identified a native-CRS mismatch, missing rights evidence and unvalidated downstream quality. Its demand for a whole-raster hash may itself need expert correction: per-window evidence has a narrower valid scope. Later pointer validation rejects unsupported source references, so historical findings are not reusable executable approval.',
 'scoped_review.py; consensus.py; run/scoped-sentinel-review-v4/report.json; docs/development/sentinel-review-refactor.md')
recipe=load('annotated_recipe.json')
irfig=fig('14_json_recipe',chain(['Intent\ncalibrated generated NIR, native support','Core recipe\ncalibrate: DN × scale + offset','Canonical definition\nnir_reflectance • unit 1','Backend operation_id\ncubedynamics.select','Validated parameters\nvariable_ref = request.variable','Fixed implementation\npublic apply + trusted selector'],2))
page('THE JSON BACKBONE','The recipe is an auditable scientific plan',
 'The example is taken from the fresh generated run. Its metadata and code identities bind the reviewed intent to the exact execution context.',irfig,
 'The model selects an offered operation; it does not write the function.',
 'The real recipe also selects a bounded full-window subset and July acquisitions. Backend parameters are closed references to reviewed configuration, not Python expressions. The full JSON is preserved with the editable report data.',
 'A recipe digest binds mappings, operations and review. Source checksums, executor identity, backend version, encoder configuration and preprocessing identity prevent reuse under stale assumptions. Typed JSON is the interface; deterministic validators and scientific review enforce the meaning.',
 'run/cubedynamics-verified/harmonization_context.json; data/annotated_recipe.json; cube_ir.py')

# Registry.
def opmatrix(f,ax):
 flags=['changes_values','changes_units','changes_spatial_support','changes_temporal_support','requires_human_approval'];a=np.array([[int(o[k]) for k in flags] for o in OPS])
 ax.imshow(a,cmap=ListedColormap([CREAM,GREEN]),aspect='auto',vmin=0,vmax=1);ax.set_yticks(range(len(OPS)),[o['operation_id'].replace('cubedynamics.','cd.') for o in OPS],fontsize=8);ax.set_xticks(range(5),['Values','Units','Spatial\nsupport','Temporal\nsupport','Review'],fontsize=9);ax.xaxis.tick_top()
 for y in range(len(OPS)):
  for x in range(5):ax.text(x,y,'●' if a[y,x] else '—',ha='center',va='center',color='white' if a[y,x] else '#A3ACA5',fontsize=8)
registry=fig('15_registry',opmatrix)
page('DETERMINISTIC OPERATIONS','Seventeen operations, each with an explicit boundary',
 'Ten core operations and seven CubeDynamics operations are exposed. Access and MOSAIKS are separate modules, not invented entries in this transformation registry.',registry,
 'Flags describe declared operation effects, not data-derived changes.',
 'The matrix is generated from OperationDefinition metadata. Some core flags are broad defaults, not a complete scientific effect analysis; for example unit conversion and calibration must still validate units at execution. All model proposals require human review even when an operation-level flag is false.',
 'Core categories include units, calibration, semantic rename, quality, temporal, spatial and exact observation join. No operation changes biological level. Registry metadata and exact implementations are provided in the appendix and machine-readable inventory.',
 'operations.REGISTRY version 2; cube_specs.py; data/operations.json')
cube=fig('16_cube',chain(['Remote source\nModule 1 owns access','Bounded native window\nquality + calibration upstream','Reviewed CubeDynamics plan\nselect • subset • calendar','Optional backend operations\nmask • mean • time / grid alignment','Explicit bounded materialization\nonly final selected graph','Harmonized patch → MOSAIKS\nno raw/harmonized files'],1))
page('CUBEDYNAMICS','Stream the data instead of moving the world',
 'The integration uses the actual external CubeDynamics 0.1.0rc3 package. Lazy plans defer values until an explicitly approved bounded compute boundary.',cube,
 'Laziness is a capability, not proof of remote I/O savings.',
 'Seven exposed operations use public pipe/verb APIs. Select, subset and quality masking use fixed adapter functions through public apply; they are not invented upstream verbs. Public unrestricted apply is never a model permission.',
 'The alternative architecture—download, store and load an entire dataset—is conceptually different. This project has no measured network-throughput or speedup result. The real Sentinel representation bridge currently allows only one-band, layout-preserving operations after calibration.',
 'cubedynamics_backend.py; cube_specs.py; docs/development/cubedynamics-audit.md; CubeDynamics [1]')

def lazytest(f,ax):
 # Values are parsed from the actual test's declared assertion, not throughput claims.
 import ast
 tree=ast.parse((ROOT/'tests/test_cubedynamics.py').read_text()); matches=[]
 for node in ast.walk(tree):
  if isinstance(node,ast.Assert):
   s=ast.unparse(node.test)
   if 'reads' in s and '[0]' in s:matches.append('reads == [0]')
 if not matches:raise ValueError('Selected-chunk test assertion not found')
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 for i in range(3):box(ax,.08+i*.31,.62,.25,.2,f'Chunk {i}',fc=GREEN if i==0 else GRAY)
 arrow(ax,(.15,.6),(.15,.4));box(ax,.05,.22,.9,.17,'Subset computes chunk 0 only\nMeasured assertion: '+matches[0],fc=MINT,fs=12)
 ax.text(.5,.05,'Generated delayed source • no remote network benchmark',ha='center',fontsize=11)
lazy=fig('17_lazy_evidence',lazytest)
page('STREAMING EVIDENCE','A selected lazy chunk stays selected at execution',
 'An offline delayed-source test records which chunks execute. The bounded subset computes the selected chunk without evaluating the others.',lazy,
 'This is an execution check, not a performance benchmark.',
 'The figure reads the passing test assertion from source. The three boxes explain the tested delayed graph; they are not a measurement of remote file requests. Guard checks additionally bound bytes, dimensions, chunks and task counts before compute.',
 'Every eager output receives an evidence hash; lazy plans are labeled plans rather than completed reads. Metadata checksums and per-window value hashes retain different scopes. No claim is made about complete remote raster immutability.',
 'tests/test_cubedynamics.py selected delayed-chunk test; data/tests.xml; cubedynamics_backend.py')

# Actual retained value transformation (illustrative calculation, no approval).
def calibrated(f,ax):
 dn=S['window']['dn'];scale=S['source_metadata']['calibration_scale'];offset=S['source_metadata']['calibration_offset'];v=dn*scale+offset
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 box(ax,.08,.65,.33,.23,f'{dn} DN\nretained real source',fs=16);box(ax,.59,.65,.33,.23,f'{v:.4f}\ncomputed illustration, unit 1',fc=MINT,fs=14);arrow(ax,(.42,.765),(.57,.765))
 ax.text(.5,.44,f'{dn} × {scale:g} + ({offset:g}) = {v:.4f}',ha='center',fontsize=20)
 ax.text(.5,.22,'No clipping • no resampling • no invented duration',ha='center',fontsize=13)
 ax.text(.5,.08,'NOT an approved harmonized scientific product',ha='center',fontsize=12,color=RED,fontweight='bold')
cal=fig('18_calibration',calibrated)
page('TRANSFORMATION','A stored digital number is not reflectance',
 'The retained Sentinel source metadata supplies the scale and offset. Applying them changes encoded DN into a dimensionless reflectance value.',cal,
 'An exact calculation can still require scientific review.',
 'The displayed arithmetic uses a real retained pixel and its documented asset coefficients. It is a report illustration of calibration, not a newly authorized pipeline product. Source data and coefficients remain unchanged.',
 'Quality class 4 is retained as evidence, not proof of ecological validity. A native 10 m footprint and instantaneous acquisition remain distinct from a geographic bounding box. The next approved real run must preserve these facts through recipe, backend and representation lineage.',
 'data/sentinel_example.json; historical run/real-sentinel/window-0.json; calibration.scale_offset')

# Generated demonstration actual outputs.
def splitfig(f,ax):
 counts=V['counts'];ax.bar(list(counts),list(counts.values()),color=[GREEN,MINT,GOLD]);ax.set_ylabel('Generated windows');ax.set_ylim(0,max(counts.values())*1.35)
 for i,(k,v) in enumerate(counts.items()):ax.text(i,v+.3,str(v),ha='center',fontsize=16)
 ax.text(.5,.92,'Training-only empirical filters; labels stored separately',transform=ax.transAxes,ha='center',fontsize=10)
splits=fig('19_splits',splitfig)
page('REPRESENT','MOSAIKS receives the harmonized output',
 'The fresh generated demonstration calibrates windows, applies real CubeDynamics selection and emits numeric MOSAIKS features with lineage.',splits,
 'Training information must stay inside the training split.',
 f"The run produced {load('embedding_manifest.json')['records']} vectors with {load('embedding_manifest.json')['dimensions']} dimensions. Empirical filters use a bounded eight-window training reference. Spatial groups are disjoint and buffered in the generated layout.",
 'MOSAIKS uses empirical random convolutional features followed by task-specific numerical models [3]. This implementation is a bounded prototype of that approach, not a generic replacement encoder or precomputed satellite feature substitution. Features are not intrinsically interpretable to an LLM.',
 'run/cubedynamics-verified/manifest.json; verification.json; cube_demo.py; mosaiks.py; [3]')

def performance(f,ax):
 keys=['test','mean_baseline','shuffled_label_baseline'];labels=['MOSAIKS + ridge','Training mean','Shuffled labels'];vals=[V[k]['rmse'] for k in keys]
 ax.barh(labels,vals,color=[GREEN,GRAY,GOLD]);ax.invert_yaxis();ax.set_xlabel('Held-out RMSE • generated diagnostic target (lower is better)');ax.set_xlim(0,max(vals)*1.35)
 for i,k in enumerate(keys):ax.text(vals[i]+max(vals)*.03,i,f"{vals[i]:.4f}  |  R² {V[k]['r2']:.3f}",fontsize=10,va='center')
performancefig=fig('20_performance',performance)
page('VERIFICATION','The features carry usable numerical information',
 'Held-out ridge regression predicts the standard deviation of the first harmonized channel. Mean and shuffled-label baselines make the diagnostic comparison explicit.',performancefig,
 'A derived target verifies the pipeline, not independent ecology.',
 'The target is calculated from generated harmonized data and stored separately from vectors. The test set is held out from filter fitting and ridge selection. These are actual fresh-run metrics, not a claim about real landscapes.',
 'Integrity checks include shard/lineage hashes, dimensions, finite values, duplicate vectors and split geography. Independent ecological labels, spatial and temporal transfer, uncertainty and task-specific acceptance remain unmeasured. Numeric model consumption is demonstrated; native LLM understanding is not.',
 'run/cubedynamics-verified/verification.json; embedding_dataset.py; mosaiks_pipeline.py')
lineage=fig('21_lineage',chain(['Representation\nencoder + preprocessing identity','Harmonized observation\ncanonical variable • units • support','Track recipe, if applicable\ntrack provenance remains separate','Core recipe + transformation\nregistry / backend versions','Agent proposal → QA → human\nexact scientific content digests','Source asset → metadata\nversion • license • window evidence'],1))
page('PROVENANCE','Every vector should lead back to its scientific decisions',
 'Read the lineage backwards from a representation to the source. The path must explain both the calculation and the decisions that made it legitimate.',lineage,
 'A compact hash identifies evidence; it does not explain its scope.',
 'Source, recipe, executor, backend, review and encoder identities contribute to lineage. Track-specific products add their own recipe without changing shared immutable sources. Metadata and extracted-window hashes are explicitly different.',
 'The generated release stores vectors, labels and compact lineage, not raw or harmonized raster datasets. Historical snapshot workflows remain labeled legacy examples. External provenance registration remains planned rather than silently attributed to MESA.',
 'provenance.py; storage.py; harmonized_rasters.py; run/cubedynamics-verified/records.jsonl')

# Ontology diagnostics.
DIMS=list(dict.fromkeys(r['dimension'] for r in B['benchmark_coverage']))
ratings={'not_target':0,'indirect':.25,'partial':.5,'strong':1,'unknown':np.nan}
selected=['bfo','iao','ro','go','cl','uberon','ncbitaxon','pato','to','po','envo','obi','sosa','ssn','oboe','ebv','stac','eml','prov','uo']
ids={r['resource_id'] for r in R};selected=[k for k in selected if k in ids]

def breadth(f,ax):
 lookup={(r['resource_id'],r['dimension']):r['diagnostic_weight'] for r in B['benchmark_coverage']};a=np.array([[lookup.get((i,d),np.nan) for d in DIMS] for i in selected],dtype=float)
 cmap=plt.get_cmap('YlGn').copy();cmap.set_bad('#BDBDBD');im=ax.imshow(a,vmin=0,vmax=1,cmap=cmap,aspect='auto');ax.set_yticks(range(len(selected)),selected,fontsize=9);ax.set_xticks(range(len(DIMS)),[d.replace('_',' ') for d in DIMS],rotation=65,ha='right',fontsize=8);f.colorbar(im,ax=ax,fraction=.025,pad=.02,label='Assessed coverage weight')
breadthfig=fig('22_breadth',breadth)
page('ONTOLOGY BENCHMARK','Breadth describes assessed scope, not ontology quality',
 f"The benchmark contains {len(B['benchmark_coverage'])} resource-by-dimension rows across {len(DIMS)} dimensions. The figure shows a named illustrative subset; all 86 resources remain in the source tables.",breadthfig,
 'The colors are provisional project judgments.',
 'Strong = 1; partial = 0.5; indirect = 0.25; not-target = 0; unknown is unscored. Equal dimension weights are diagnostic choices, not a scientific measurement scale.',
 'Coverage does not establish exact concepts, term alignment, scientific compatibility or adoption. Hierarchical, relational and annotation depth have not been computed and are NOT YET MEASURED. A broad resource may still lack the exact distinction a question needs.',
 'outputs/semantic_benchmark/benchmark_coverage.parquet; data/semantics/assessments.jsonl')

# Explicit inventory dependency graph only, no inference from scope.
def composition(f,ax):
 ax.axis('off');ax.set_xlim(-1.5,1.5);ax.set_ylim(-1.2,1.2)
 resources={r['resource_id']:r for r in R};edges=[]
 for r in R:
  for t in json.loads(r['imports_or_dependencies']):
   if t in resources:edges.append((r['resource_id'],t))
 nodes=sorted({v for e in edges for v in e});angle=np.linspace(0,2*np.pi,len(nodes),endpoint=False);pos={n:(np.cos(a),np.sin(a)) for n,a in zip(nodes,angle)}
 for a,b in edges:ax.plot([pos[a][0],pos[b][0]],[pos[a][1],pos[b][1]],color=MINT,alpha=.4,lw=.65)
 degree={n:sum(n in e for e in edges) for n in nodes}
 for n,(x,y) in pos.items():
  ax.scatter(x,y,s=35+degree[n]*12,c=GREEN,zorder=3);ax.text(x*1.13,y*1.13,n,ha='center',va='center',fontsize=8)
 ax.text(0,0,f'{len(edges)} declared links\nwithin inventoried resources',ha='center',fontsize=12,bbox={'facecolor':CREAM,'edgecolor':'none','pad':8})
 (D/'inventory_relationships.json').write_text(json.dumps({'relation':'inventory imports_or_dependencies declaration; not parsed OWL','edges':edges},indent=2)+'\n')
comp=fig('23_composition',composition)
page('COMPOSITION','Declared links show where semantic systems already connect',
 'The inventory records imports or dependencies when present in inspected metadata. This graph draws only links whose targets are also in the local inventory.',comp,
 'A declared dependency is not a validated scientific mapping.',
 'The graph is not a parsed OWL import closure, term-level reuse analysis or bridge-centrality benchmark. External target strings are retained in the CSV but excluded from this within-inventory drawing.',
 'Different systems may supply different parts of an observation: an entity, environment, observation method, relation or unit. That is a compositional hypothesis to investigate. This graph alone does not prove interoperability or identify the best ontology portfolio.',
 'semantic_resources.csv.imports_or_dependencies; data/inventory_relationships.json')

def overlap(f,ax):
 names=selected[:14];a=np.eye(len(names));idx={n:i for i,n in enumerate(names)}
 for r in B['ontology_pairs']:
  if r['left_resource'] in idx and r['right_resource'] in idx:a[idx[r['left_resource']],idx[r['right_resource']]]=a[idx[r['right_resource']],idx[r['left_resource']]]=r['assessed_coverage_jaccard']
 im=ax.imshow(a,vmin=0,vmax=1,cmap='YlGn');ax.set_xticks(range(len(names)),names,rotation=60,ha='right',fontsize=9);ax.set_yticks(range(len(names)),names,fontsize=9);f.colorbar(im,ax=ax,label='Assessed dimension overlap (Jaccard)',fraction=.035)
overlapfig=fig('24_overlap',overlap)
page('COMPLEMENTARITY','Different scope may be valuable—but is not enough',
 f"The local pair table evaluates {len(B['ontology_pairs'])} pairs for assessed coverage overlap. A selected matrix makes that limited result visible.",overlapfig,
 'Low overlap is not measured scientific complementarity.',
 'Jaccard compares sets of positively assessed dimensions. It does not evaluate conflicting axioms, redundant concepts, scientific mapping difficulty or useful combined inference. The diagonal is identity for display.',
 'Redundant, overlapping, complementary, different-domain, potential-conflict and unknown are useful future review distinctions. Only assessed scope overlap is computed here. A term-level, task-specific benchmark is needed before labeling promising scientific combinations.',
 'outputs/semantic_benchmark/ontology_pairs.parquet; semantic_benchmark.py')

def accumulation(f,ax):
 p=load('portfolio.json');items=p['selected'];y=np.cumsum([v['marginal_assessed_coverage_gain'] for v in items])/len(DIMS)
 ax.plot(range(1,len(y)+1),y,'o-',color=GREEN,lw=2);ax.set_ylim(0,1.05);ax.set_xlabel('Resources selected by local greedy diagnostic');ax.set_ylabel('Equal-weight assessed coverage');ax.set_xticks(range(1,len(y)+1),[v['resource_id'] for v in items]);ax.grid(axis='y',alpha=.2)
 ax.text(.04,.1,'Not a term-level semantic accumulation experiment',transform=ax.transAxes,color=RED,fontsize=10)
acc=fig('25_portfolio',accumulation)
page('ACCUMULATION','An assessed portfolio adds scope; scientific gain is still a question',
 'The existing greedy diagnostic chooses up to eight resources to cover local assessed dimensions. Its recorded marginal gains can be accumulated without inventing new scores.',acc,
 'This curve measures the rubric, not all scientific meaning.',
 'The curve sums recorded marginal gains and divides by 21 equally weighted dimensions. Unknown values add no assessed gain. Selection is a recommendation for human review, not scientific adoption.',
 'The larger research question—whether specialized resources keep adding task-relevant semantic meaning—remains UNDER ANALYSIS. It requires canonical observations, exact term evidence, expert judgments and held-out questions. Ontology saturation has not been demonstrated.',
 'outputs/semantic_benchmark/recommended_portfolio.json; method and not_established fields')

def gaps(f,ax):
 rows=[r for r in B['semantic_gaps'] if r.get('dimension') in DIMS];values={r['dimension']:r['strong_resources'] for r in rows};horizontal_bars(values,'Resources with strong local assessment')(f,ax)
gap=fig('26_gaps',gaps)
page('SEMANTIC GAPS','A sparse assessment is a place to investigate',
 'The gap table counts strong and unknown resource assessments. It does not prove that an external concept is absent.',gap,
 'A missing concept and a missing scientific rule are different problems.',
 'Counts show the current inventory rubric only. They do not classify whether a gap needs a crosswalk, composition, extension, project concept or scientific transformation rule. The table contains an additional review-oriented gap record beyond the dimension rows.',
 'Support, aggregation, representativeness, uncertainty propagation and cross-scale justification need careful review. An expert should first ask whether the concept already exists, then whether a mapping or scientific rule is needed. Unknown remains an acceptable result.',
 'outputs/semantic_benchmark/semantic_gaps.parquet; docs/semantics/ontology-benchmarking.md')

# Dataset diagnostics.
DATA=B['dataset_metrics'];labels={r['dataset_key']:('retained Sentinel metadata' if not r['fixture'] else r['asset_id']) for r in DATA}
def profiles(f,ax):
 fields=sorted({v for r in DATA for v in r['present_fields']});a=np.array([[v in r['present_fields'] for v in fields] for r in DATA]);ax.imshow(a,cmap=ListedColormap([GRAY,GREEN]),aspect='auto',vmin=0,vmax=1);ax.set_yticks(range(len(DATA)),[labels[r['dataset_key']] for r in DATA],fontsize=9);ax.set_xticks(range(len(fields)),[v.replace('_',' ') for v in fields],rotation=65,ha='right',fontsize=9)
profile=fig('27_dataset_profiles',profiles)
page('DATASET SEMANTICS','Three source records reveal metadata differences',
 'The benchmark uses two synthetic fixture records and one retained real Sentinel metadata record. These are asset/version records, not three provider-wide assessments.',profile,
 'A present field is not necessarily complete or scientifically adequate.',
 'Green indicates a field extracted by the metadata parser; gray indicates absence. The plotted columns are the union of observed fields, not a claim that all possible semantic dimensions were tested.',
 'Documentation rankings are project diagnostics. They do not rank scientific data quality or dataset suitability. The current sample is too small and mixed in evidence type to support broad conclusions about NEON, Sentinel or other providers.',
 'outputs/semantic_benchmark/dataset_metrics.parquet; dataset_rankings.parquet')

def quadrants(f,ax):
 ax.remove()
 for i,(xlabel,tl,tr,bl,br) in enumerate([
  ('Explicit ontology use','Candidate demonstration','Documented + promising','Review science need','Explicit use, limited gain'),
  ('Semantic diversity','Easy benchmark','Possible flagship','Review science need','Hard but interesting')]):
  a=f.add_subplot(1,2,i+1);a.set_xlim(0,1);a.set_ylim(0,1);a.axvline(.5,color=GRAY);a.axhline(.5,color=GRAY);a.set_xticks([0,1],['Low','High']);a.set_yticks([0,1],['Low','High']);a.set_xlabel(xlabel,fontsize=11)
  if i==0:a.set_ylabel('Ontology potential',fontsize=11)
  for x,y,t in [(.25,.75,tl),(.75,.75,tr),(.25,.25,bl),(.75,.25,br)]:a.text(x,y,textwrap.fill(t,16),ha='center',va='center',fontsize=9)
  a.set_title('Conceptual only • no points',fontsize=10,color=RED)
 f.suptitle('Metrics NOT YET MEASURED',fontsize=12,y=.98,color=RED)
quad=fig('28_potential',quadrants)
page('DATASET POTENTIAL','The useful next question has not been scored yet',
 'Two proposed analyses compare ontology potential against explicit ontology use, and against semantic diversity. Neither currently has validated dataset metrics.',quad,
 'No real datasets are placed in these quadrants.',
 'The two panels explain separate planned comparisons. Explicit use and diversity have different x-axes and must be measured separately; they are not interchangeable numerical values.',
 'Potential means a reviewed opportunity to make currently implicit meaning computable. A rubric would need evidence of entities, methods, supports, identifiers and scientific use cases. The report preserves the idea without fabricating flagship candidates or coordinates.',
 'docs/semantics/dataset-benchmarking.md; docs/development/documentation-sync-audit.md','PLANNED WORK')

def datasetnetwork(f,ax):
 ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
 for i,r in enumerate(DATA):box(ax,.03,.75-i*.27,.5,.15,labels[r['dataset_key']],fc=GREEN if not r['fixture'] else MINT,fs=10)
 box(ax,.72,.45,.23,.18,'STAC\nnamespace',fc=MINT,fs=13)
 positions={r['dataset_key']:.825-i*.27 for i,r in enumerate(DATA)}
 for r in B['dataset_ontology_edges']:arrow(ax,(.54,positions[r['dataset_key']]),(.70,.54))
 ax.text(.7,.18,'One declared namespace association\nNo resolved term equivalence',ha='center',fontsize=11)
network=fig('29_dataset_network',datasetnetwork)
page('DATASET–RESOURCE RELATIONSHIPS','A namespace reference is useful but limited evidence',
 'The dataset-edge table contains one extracted STAC namespace association. It does not contain a resolved ontology concept mapping.',network,
 'No inferred dataset–ontology edges are drawn.',
 'The parser recognizes an explicit metadata namespace; term existence, exact concept identity and scientific equivalence are not evaluated. The fixture records have no such extracted edges in this table.',
 'A richer graph should distinguish explicitly uses, implements standard, provides identifiers, reviewed mapping and potential mapping. Those relations need different evidence. Adding arrows merely because a dataset and ontology concern the environment would hide the scientific work.',
 'outputs/semantic_benchmark/dataset_ontology_edges.parquet; semantic_discovery.py')

def datasetpairs(f,ax):
 n=len(DATA);a=np.eye(n);idx={r['dataset_key']:i for i,r in enumerate(DATA)}
 for r in B['dataset_pairs']:i,j=idx[r['left_dataset']],idx[r['right_dataset']];a[i,j]=a[j,i]=r['field_presence_jaccard']
 im=ax.imshow(a,vmin=0,vmax=1,cmap='YlGn');names=[labels[r['dataset_key']] for r in DATA];ax.set_xticks(range(n),names,rotation=20,ha='right',fontsize=9);ax.set_yticks(range(n),names,fontsize=9)
 for i in range(n):
  for j in range(n):ax.text(j,i,f'{a[i,j]:.2f}',ha='center',va='center',fontsize=15,color='white' if a[i,j]>.65 else INK)
 f.colorbar(im,ax=ax,fraction=.04,label='Metadata field-presence Jaccard')
pairs=fig('30_dataset_pairs',datasetpairs)
page('DATASET PAIRS','Shared metadata structure is not shared scientific meaning',
 'The three pair records compare field presence. This is the available pair result; ecological complementarity, science value and cross-scale opportunity are not scored.',pairs,
 'These pairs do not rank real provider combinations.',
 'The matrix uses the same three source metadata records as the profile. Values compare sets of extracted field names, not measurements, taxa, units or support compatibility. Identity diagonals are supplied for display.',
 'NEON–Sentinel, trait–community and other combinations may be useful future questions, but the present benchmark does not establish them. A valid ranking needs independently reviewed variables, supports, licenses, scientific objectives and transformation rules.',
 'outputs/semantic_benchmark/dataset_pairs.parquet; scientific_comparability = not_evaluated')

# Confidence and maturity.
testfig=fig('31_tests',horizontal_bars(M['tests']['by_module'],'Passing tests in integration environment'))
page('SOFTWARE CONFIDENCE','The suite tests guardrails as well as successful calculations',
 f"{M['tests']['passed']} passed; {M['tests']['failed']} failed; {M['tests']['skipped']} skipped. The integration environment includes actual CubeDynamics; tests use offline data.",testfig,
 'Passing software tests do not validate ecological conclusions.',
 'The suite exercises malformed model output, stale decisions, unknown operations, support/rights checks, lazy bounded computation, track independence, provenance and held-out numerical diagnostics.',
 'This is test count by module, not line coverage or a percentage of all scientific behavior. Code coverage is NOT YET MEASURED. Independent scientific labels, expert semantic adjudication, remote throughput and production reliability need separate evaluation.',
 'data/tests.xml; data/test_results.json; tests/; docs/testing.md')

maturity_rows=[('Discovery','discovery',1),('Source access','real_data',1),('Semantic discovery','semantic_discovery',1),('Ontology lookup','semantic_discovery',0),('Semantic mapping','harmonization',1),('Human review','review',1),('JSON recipe','operation_registry',1),('Schema validation','operation_registry',1),('Scientific validation','harmonization',1),('Operation registry','operation_registry',1),('CubeDynamics execution','cubedynamics',1),('Provenance','representations',1),('Harmonized observation','harmonization',1),('Representation','mosaiks',1),('Science tracks','integration_tracks',1)]
def matrix(f,ax):
 a=[]
 for name,t,demonstrated in maturity_rows:a.append([1,1,1,demonstrated,1,0])
 ax.imshow(a,cmap=ListedColormap([GRAY,GREEN]),aspect='auto');ax.set_yticks(range(len(a)),[r[0] for r in maturity_rows],fontsize=9);ax.set_xticks(range(6),['Designed','Implemented','Tested','Demonstrated','Documented','Production\nready'],fontsize=8);ax.xaxis.tick_top()
 for i,row in enumerate(a):
  for j,v in enumerate(row):ax.text(j,i,'●' if v else '—',ha='center',va='center',color='white' if v else INK,fontsize=9)
 (HERE/'tables/maturity.json').write_text(json.dumps([{'component':r[0],'evidence':f'tests/test_{r[1]}.py','columns':dict(zip(['designed','implemented','tested','demonstrated','documented','production_ready'],a[i])),'scope':'bounded prototype behavior only; ontology lookup local candidates only; science validation deterministic rules, not independent ecology'} for i,r in enumerate(maturity_rows)],indent=2)+'\n')
mat=fig('32_maturity',matrix)
page('PROJECT MATURITY','There is a broad local demonstration, not a production service',
 'The matrix assesses bounded prototype behavior from source, tests, documentation and retained examples. It does not claim that each row is scientifically complete.',mat,
 'No component is labeled production ready.',
 'Ontology lookup is limited to local candidates and namespace evidence; no live term-level service is demonstrated. Source access has real historical Sentinel evidence, while MESA transport and NEON observation normalization remain incomplete.',
 'Scientific validation here means deterministic preconditions and review gates. It does not mean independent ecological validation. Science tracks demonstrate configuration separation and shared-source immutability, not validated food or water security outcomes.',
 'tables/maturity.json; data/component_inventory.json; docs/architecture/current-state.md','PROJECT INTERPRETATION')

limits=fig('33_limits',chain(['Demonstrated locally\ntyped plans • bounded deterministic execution','Partially solved\nreal access • evidence-driven review','Active research\nsupport changes • semantic composition','Not yet measured\nontology depth • potential • throughput','Needs human review\nreal Sentinel plan • rights • QA veto','No current claim\nproduction service • ecological validity'],2,False))
page('WHAT REMAINS DIFFICULT','The hardest gaps are scientific, not just computational',
 'The current system can stop an unsupported analysis. It cannot yet resolve every ambiguity or prove that a derived representation is useful for a real ecological question.',limits,
 'The limitations define the next experiment.',
 'MESA transport is blocked, general reprojection/resampling is unexposed, and the MOSAIKS bridge preserves a single native band/grid. Model review can contain mistaken claims or unsupported evidence pointers and needs expert revision.',
 'Ontology scores remain provisional metadata diagnostics. Depth, validated composition, dataset potential/diversity and term-level accumulation are unmeasured. Geographic/temporal transfer and independent outcome validation remain open. No unmeasured speedup or universal representation is claimed.',
 'docs/PROTOTYPE_STATUS.md; docs/development/cubedynamics-audit.md; semantic benchmark methods')
road=fig('34_roadmap',chain(['NOW\npreserve evidence and reviewed boundaries','Next working demonstration\nexpert-approved bounded real Sentinel stream','Multi-dataset harmonization\nexplicit variables, support and rights','Semantic benchmark validation\nexpert terms + canonical observations','Science-track demonstrations\nindependent targets + acceptance criteria','Scale-up\nmeasure I/O, memory, throughput and transfer'],1))
page('WHERE THE PROJECT GOES NEXT','One approved real demonstration is the next meaningful milestone',
 'The roadmap follows observed gaps rather than arbitrary calendar dates. Each stage needs evidence that the previous assumptions remain valid.',road,
 'Make one scientific claim reviewable before making many.',
 'First resolve the real Sentinel recipe, rights evidence, native-CRS wording, quality criteria and historical veto with experts. Re-run fresh frozen consensus and human review before source access. Then stream a small bounded area directly into MOSAIKS and verify lineage and held-out independent targets.',
 'Lessons: finding data is easier than justifying comparisons; alignment does not prove equivalence; constrained JSON makes model decisions inspectable; human review belongs at consequential boundaries. The research opportunity is a human-governed scientific compiler. Novelty remains a hypothesis alongside STAC, observation ontologies, PROV, MOSAIKS and existing workflow systems—not an established priority claim.',
 'docs/development/decisions.md; AGENTS.md; [1–7]','PLANNED WORK')

# Render editable content first; machine-readable source is the authoritative report narrative.
(HERE/'report.json').write_text(json.dumps(PAGES,indent=2,ensure_ascii=False)+'\n')
md=['# From Scientific Question to Harmonized Data','','Report version 1.0. Narrative source also stored as report.json.','']
for i,p in enumerate(PAGES,2):
 md += [f"## {i}. {p['title']}",'',p['deck'],'',f"![{p['takeaway']}](figures/{p['figure']}.svg)",'',f"**{p['takeaway']}** {p['caption']}",'',p['body'],'',f"Evidence: {p['evidence']}. Claim class: {p['kind']}.",'']
(HERE/'report.md').write_text('\n'.join(md))
PDF=ROOT/'output/pdf/AI_ready_pipeline_state_report.pdf';PDF.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(PDF),pagesize=(612,792));c.setTitle('From Scientific Question to Harmonized Data');c.setAuthor('ESIIL | AI-ready datasets prototype');c.setSubject('Evidence-led pipeline state report; version 1.0')
STYLE=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16,textColor=colors.HexColor(INK))
SMALL=ParagraphStyle('small',parent=STYLE,fontSize=8.5,leading=12)
TITLE=ParagraphStyle('title',parent=STYLE,fontName='Helvetica-Bold',fontSize=25,leading=29)
CAP=ParagraphStyle('cap',parent=STYLE,fontSize=10,leading=14)
LAYOUT=[]
def para(text,x,top,w,style,maxheight=None):
 text=text.replace('&','&amp;').replace('→',' → ')
 p=Paragraph(text,style);_,h=p.wrap(w,750)
 if maxheight is not None and h>maxheight:raise ValueError(f'Text overflow {h}>{maxheight}: {text[:70]}')
 p.drawOn(c,x,top-h);return top-h

def base(n,section):
 c.setFillColor(colors.HexColor(CREAM));c.rect(0,0,612,792,fill=1,stroke=0)
 c.setFillColor(colors.HexColor(GREEN));c.rect(45,749,25,3,fill=1,stroke=0)
 c.setFont('Helvetica-Bold',8);c.drawString(80,748,section.upper())
 c.setStrokeColor(colors.HexColor(GRAY));c.line(45,48,567,48)
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor(INK));c.drawString(45,31,'ESIIL  /  AI-READY ENVIRONMENTAL DATA  /  STATE REPORT 1.0');c.drawRightString(567,31,str(n))

base(1,'Research synthesis • 21 October 2026')
para('From Scientific Question<br/>to Harmonized Data',45,708,520,ParagraphStyle('cover',parent=TITLE,fontSize=34,leading=40))
para('State of the AI-Ready Environmental Data Pipeline',45,598,520,ParagraphStyle('subtitle',parent=STYLE,fontSize=17,leading=24))
c.drawImage(ImageReader(str(ROOT/'docs/assets/blue-marble-2002.jpg')),146,214,width=320,height=320,mask='auto')
para('Preserve meaning. Make decisions visible.<br/>Bring reviewed computation to bounded data streams.',68,186,480,ParagraphStyle('tag',parent=STYLE,fontSize=16,leading=22,alignment=1))
para(f"ESIIL • AI_ready_datasets • pipeline {MAN['pipeline_version']}<br/>Audit commit {MAN['git_commit'][:12]} • report version 1.0<br/>Repository: github.com/CU-ESIIL/AI_ready_datasets",45,104,522,SMALL)
c.showPage()
for n,p in enumerate(PAGES,2):
 base(n,p['section']);para(p['title'],45,713,522,TITLE,65);para(p['deck'],45,639,522,STYLE,66)
 c.drawImage(ImageReader(str(F/f"{p['figure']}.png")),42,270,width=528,height=313.5,mask='auto')
 para('<b>'+p['takeaway']+'</b> '+p['caption'],45,252,522,CAP,73)
 para(p['body'],45,171,522,STYLE,96)
 para(f"{p['kind']}  |  Evidence: {p['evidence']}",45,69,522,ParagraphStyle('evidence',parent=SMALL,fontSize=7,leading=9),20)
 LAYOUT.append({'page':n,'figure':p['figure'],'title':p['title']});c.showPage()
# Compact appendices are deliberately tables, not more decorative figures.
n=len(PAGES)+2;base(n,'Technical appendix • quantities and methods');para('What the numbers count',45,713,522,TITLE)
y=660
rows=[('Package Python files',M['package_python_files'],'Includes __init__.py; file count, not architectural module count'),('Direct Contract subclasses',M['direct_Contract_subclasses'],'AST class declarations directly inheriting Contract; not all nested types'),('Exported JSON schemas',M['exported_json_schemas'],'Generated top-level files in docs/reference/schemas'),('Registered operations',M['registered_operations'],'10 core + 7 external-backend operations'),('Cube lazy-capable operations',M['cube_lazy_operations'],'All 7 support lazy inputs; explicit bounded materialization optional'),('Registry human-review flags',M['registry_declared_human_review'],'Operation-level flags only; all model proposals still require review'),('Semantic resources / dimensions',f"{M['semantic_resources']} / {len(DIMS)}",'Canonical provisional inventory and existing equal-weight rubric'),('Resource-pair diagnostics',len(B['ontology_pairs']),'All unordered pairs among 86 resources; scope overlap only'),('Source metadata records',len(DATA),'2 synthetic + 1 retained real asset/version; not whole providers'),('Term-level benchmark observations','NOT YET MEASURED','1,806 coverage rows are not canonical scientific observations'),('Coverage / remote speed / ontology depth','NOT YET MEASURED','Test counts and lazy checks are not substitutes')]
for a,b,d in rows:
 y=para(f'<b>{a}: {b}</b><br/>{d}',45,y,522,CAP)-12
para('Reproducibility: audit.py reads an explicit allow-list of local artifacts; build_report.py generates SVG/PNG figures, editable narrative and this PDF. run_manifest.json records input hashes, package versions, the audit commit and test results. Figure source hashes are recorded after rendering. Historical run inputs are not acquired again.',45,160,522,STYLE,90)
para('Full tables: data/operations.json; tables/components.csv; tables/maturity.json; data/metrics.json.',45,65,522,SMALL,20);c.showPage()
n+=1;base(n,'Technical appendix • operation inventory');para('The exact execution surface',45,713,522,TITLE)
y=660
for o in OPS:
 api=o.get('upstream_api') or 'core deterministic implementation'
 line=f"<b>{o['operation_id']}</b> — {o['backend']}<br/>{api}"
 y=para(line,45,y,522,ParagraphStyle('op',parent=CAP,fontSize=9,leading=12))-8
para('No access, representation, arbitrary Python, general reprojection or biological-level conversion is registered. Full preconditions, parameter schemas and tests are in data/operations.json. Core effect flags can be coarse defaults; inspect execution validation for scientific effects.',45,100,522,CAP,55);c.showPage()
n+=1;base(n,'Technical appendix • versions and attribution');para('Methods, precedents and sources',45,713,522,TITLE)
y=658
refs=[
 '[1] CubeDynamics. CU-ESIIL external package, installed 0.1.0rc3. https://github.com/CU-ESIIL/cubedynamics and https://cu-esiil.github.io/cubedynamics/ . Upstream checkout inspected: 4c6afea9565b. Local wheel and repository dependency declarations differ; see audit.',
 '[2] STAC specification. https://stacspec.org/ and https://github.com/radiantearth/stac-spec . Catalog metadata describes assets; it is not the full harmonization infrastructure.',
 '[3] Rolf et al. (2021). A generalizable and accessible approach to machine learning with global satellite imagery. Nature Communications 12, 4392. https://doi.org/10.1038/s41467-021-24638-z . MOSAIKS is methodological precedent; prototype results are separate.',
 '[4] MESA technical documentation and server source. https://idss-mesa.github.io/docs/ and https://github.com/idss-mesa/mesa-mcp . External transport remains unavailable in this prototype; verify deployed schemas before integration.',
 '[5] OBO Foundry registry and resource primary documentation. https://obofoundry.org/ . Per-resource canonical/documentation URLs and verification scopes are preserved in data/semantics/semantic_resources.csv; all 86 rows accompany the report inputs.',
 '[6] W3C PROV-O. https://www.w3.org/TR/prov-o/ . W3C/OGC SOSA/SSN. https://www.w3.org/TR/vocab-ssn/ . Existing provenance and observation standards are related work, not project inventions.',
 '[7] Source evidence: Element 84 Earth Search STAC and Copernicus Sentinel-2 metadata. https://earth-search.aws.element84.com/v1 . Contains modified Copernicus Sentinel data (2023), accessed via Element 84. License evidence and unresolved review requirements remain explicit.',
 '[8] Cover: NASA Earth Observatory, Blue Marble 2002, MODIS/Terra composite. https://science.nasa.gov/resource/blue-marble-2002/ . Existing attributed website image reused for educational reporting; not a prototype source dataset or NASA endorsement.'
]
for r in refs:y=para(r,45,y,522,SMALL)-12
versions='; '.join(k+' '+v for k,v in MAN['versions'].items())
para('<b>Build environment:</b> Python 3.12; '+versions+'.<br/><b>Claim classes:</b> external facts are attributed; project results use local artifacts; project interpretations are editorial judgments; planned work has not been executed.',45,150,522,SMALL,85)
c.showPage();c.save()
# Copy the canonical CSV so the report evidence snapshot is portable.
import shutil
shutil.copyfile(ROOT/'data/semantics/semantic_resources.csv',D/'semantic_resources.csv')
shutil.copyfile(ROOT/'data/semantics/assessments.jsonl',D/'resource_assessments.jsonl')
MAN['figures']=[{'id':k,'svg':f'figures/{k}.svg','sha256':hashlib.sha256((F/f'{k}.svg').read_bytes()).hexdigest()} for k in FIGS]
MAN['tables']=['tables/components.csv','tables/maturity.json','data/metrics.json','data/operations.json','data/benchmark_tables.json']
MAN['report_source']=['report.json','report.md','audit.py','build_report.py']
MAN['pages']=n;MAN['figure_count']=len(FIGS);MAN['pdf']={'path':str(PDF.relative_to(ROOT)),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()};MAN['rendered_at']=datetime.now(timezone.utc).isoformat()
MAN['build_sources']=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [HERE/'audit.py',HERE/'build_report.py',HERE/'report.json',HERE/'report.md']]
(D/'run_manifest.json').write_text(json.dumps(MAN,indent=2)+'\n');(D/'page_inventory.json').write_text(json.dumps(LAYOUT,indent=2)+'\n')
print(f'{PDF}: {n} pages, {len(FIGS)} figures')
