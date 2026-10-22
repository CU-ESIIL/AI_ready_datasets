"""Render measured metadata experiments and blocked review packages; no live I/O."""
from pathlib import Path
import json,csv,hashlib,xml.etree.ElementTree as ET
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import ListedColormap
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
HERE=Path(__file__).parent;ROOT=HERE.parents[1];D=HERE/'data';F=HERE/'figures';F.mkdir(exist_ok=True)
load=lambda n:json.loads((D/n).read_text())
B=load('resource_breadth.json');C=load('canonical_benchmark.json');G=load('resource_depth.json');DS=load('dataset_benchmark.json');S=load('sentinel_review_gap_analysis.json');N=load('neon_sentinel_case.json');V=load('model_experiment/summary.json');P=load('resource_pca.json');MAN=load('run_manifest.json')
GREEN='#174B42';GOLD='#B57B35';INK='#20333A';MINT='#9BBFAE';GRAY='#D6DBD6';CREAM='#F5F3EB';RED='#98513D'
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':CREAM,'axes.facecolor':CREAM,'savefig.facecolor':CREAM,'svg.fonttype':'none'})
figures=[];pages=[]
def fig(name,draw):
 f,ax=plt.subplots(figsize=(8,4.8));draw(f,ax);f.tight_layout(pad=1.2)
 for ext in ['png','svg']:f.savefig(F/f'{name}.{ext}',dpi=180)
 plt.close(f);figures.append(name);return name

def bars(values,label):
 def draw(f,ax):
  items=sorted(values.items(),key=lambda x:x[1]);ax.barh([k for k,v in items],[v for k,v in items],color=GREEN);ax.set_xlabel(label);ax.set_xlim(0,max(v for k,v in items)*1.22)
  for i,(k,v) in enumerate(items):ax.text(v+.1,i,f'{v:g}',va='center',fontsize=10)
 return draw

def diagram(labels):
 def draw(f,ax):
  ax.axis('off');n=len(labels)
  for i,label in enumerate(labels):
   y=.91-i*.85/n;ax.add_patch(FancyBboxPatch((.08,y-.1),.84,.095,boxstyle='round,pad=.01',fc=GREEN if i%2==0 else MINT,ec='none'));ax.text(.5,y-.05,label,ha='center',va='center',color='white' if i%2==0 else INK,fontsize=11)
   if i<n-1:ax.annotate('',xy=(.5,y-.13),xytext=(.5,y-.11),arrowprops={'arrowstyle':'-|>','color':GREEN})
 return draw

def page(title,deck,figure,takeaway,caption,body,evidence,kind='MEASURED PROJECT RESULT'):
 pages.append(dict(title=title,deck=deck,figure=figure,takeaway=takeaway,caption=caption,body=body,evidence=evidence,claim_class=kind))

summaryfig=fig('01_scope',bars({'Canonical observation specifications':len(C['observations']),'Candidate metadata records':len(DS['records']),'Source vocabulary graphs parsed':len(G),'Verde calls (two repeats)':V['call_counts']['total'],'Real scientific releases approved':0},'Objects measured or prepared in this pass'))
page('Can the comparison be justified?',
 'Scientific validation begins by asking what the source measured, what a proposed transformation changes and what evidence would make a comparison defensible.',summaryfig,
 'We measured the boundaries; we did not approve a real-data release.',
 'This pass adds real graph measurements and live model experiments, while preserving a blocked Sentinel review and a proposed NEON–Sentinel case. Candidate counts include heterogeneous product, network, standard and unresolved-product scopes.',
 'The strongest conclusion is about method: structural model validity and successful software execution cannot replace scientific evidence. The following pages separate source facts, measured project results, project assessments, model judgments and proposed experiments.',
 'data/run_manifest.json; data/model_experiment/summary.json; AGENTS.md')

gap_labels={'already-resolved issue':'Already resolved','scientific interpretation requiring an expert':'Expert interpretation','deterministic validation that software can perform':'Software check','issue that should remain unresolved':'Remain unresolved','model criticism that appears unsupported or outside the model jurisdiction':'Unsupported / jurisdiction','rights/licensing evidence':'Rights evidence'}
gapfig=fig('02_sentinel_gaps',bars({gap_labels[k]:v for k,v in Counter(x['classification'] for x in S['blockers']).items()},'Retained findings and added workflow issues'))
page('A veto is evidence to investigate, not an obstacle to erase',
 f"The Sentinel package retains {len(S['blockers'])} issue records, including historical PASS findings and three additional workflow issues. The historical QA decision remains revise.",gapfig,
 'Software can clarify a finding without lifting the veto.',
 'Native raster EPSG:32613 and footprint EPSG:4326 are different roles. Official Sentinel terms now provide source evidence on lawful distribution/modification and attribution, but intended use still needs review.',
 'The whole-raster-hash demand is not supported by the existing bounded-stream contract; per-window hashes have a valid narrower scope. Residual source-mutation risk remains for expert adjudication. Independent suitability, quality criteria, exact sensor support and fresh recipe/layout review remain unresolved.',
 'sentinel_review_gap_analysis.json; expert_decision_template.json; historical scoped review; Sentinel legal notice pp.1–2', 'PROJECT ASSESSMENT')

ids=sorted({r['resource_id'] for r in B});dims=list(dict.fromkeys(r['dimension'] for r in B));lookup={(r['resource_id'],r['dimension']):r['score'] for r in B}
selected=[r for r in ['bfo','ro','go','uberon','ncbitaxon','pato','to','po','envo','obi','sosa','ssn','oboe','ebv','stac','eml','prov','uo'] if r in ids]
def breadth(f,ax):
 a=np.array([[lookup[i,d] if lookup[i,d] is not None else np.nan for d in dims] for i in selected]);cmap=plt.get_cmap('YlGn').copy();cmap.set_bad('#B9B9B9');im=ax.imshow(a,cmap=cmap,vmin=0,vmax=3,aspect='auto');ax.set_yticks(range(len(selected)),selected,fontsize=8);ax.set_xticks(range(len(dims)),[d.replace('_',' ') for d in dims],rotation=70,ha='right',fontsize=7);f.colorbar(im,ax=ax,fraction=.025,label='Provisional ordinal scope')
breadthfig=fig('03_breadth',breadth)
page('Breadth is an evidence-linked assessment, not an ontology fact',
 f"{len(B)} assertions extend 86 inventory resources across 28 requested dimensions. Every known score retains evidence, source URLs, confidence and a project-assessment label.",breadthfig,
 'Unknown stays gray; it does not become zero.',
 'The original strong/partial/indirect/not-target coding maps to 3/2/1/0 for scoped comparison. Zero means not targeted in the assessed scope, not verified absence from an ontology. New dimensions without specific evidence remain unknown.',
 'Scores are inherited provisional judgments, not newly expert-validated results. The report does not infer genomic, phenotype, trophic or support coverage merely from broader labels. Exact concept expressibility is assessed separately and remains mostly unresolved.',
 'resource_breadth.json; data/semantics/semantic_resources.csv; assessments.jsonl','PROJECT ASSESSMENT')

def depth(f,ax):
 names=[r['resource_id'] for r in G];ax.bar(np.arange(len(G))-.18,[r['named_classes'] for r in G],.36,color=GREEN,label='Named classes');ax.bar(np.arange(len(G))+.18,[r['max_longest_root_depth'] for r in G],.36,color=GOLD,label='Longest explicit named-class depth');ax.set_xticks(range(len(G)),names);ax.set_ylabel('Count / edge depth (different metrics)');ax.legend(frameon=False)
 for i,r in enumerate(G):ax.text(i-.18,r['named_classes']+.5,str(r['named_classes']),ha='center')
depthfig=fig('04_depth',depth)
page('Three real vocabulary graphs can now be inspected quantitatively',
 'The analysis parses bounded, attributed BFO, SOSA and SSN Turtle snapshots. It counts explicit classes, subclass structure, relations, restrictions, definitions, synonyms, cross-references and imports.',depthfig,
 'A shallow explicit hierarchy does not mean poor scientific coverage.',
 'Graph imports are not followed, blank-node restrictions are counted separately and no OWL inference runs. Depth uses named-class subclass edges within the local snapshot; cycles produce unknown depth rather than a fabricated answer.',
 'SOSA and SSN use modeling patterns that this local named-class hierarchy does not summarize. SSN explicitly imports SOSA, so its local depth is not the depth of the combined model. HTTP-shaped identifiers are counted, but resolvability is not tested. Class counts are not quality scores.',
 'resource_depth.json; data/graphs/manifest.json; W3C license notice; BFO dc:license')

def relationship(f,ax):
 ax.axis('off');edges=[r for r in load('resource_relationships.json') if r['relation']=='declared_import_or_dependency' and r['target'] in ids];nodes=sorted({v for r in edges for v in [r['source'],r['target']]});pos={n:(np.cos(t),np.sin(t)) for n,t in zip(nodes,np.linspace(0,2*np.pi,len(nodes),endpoint=False))}
 for e in edges:ax.plot([pos[e['source']][0],pos[e['target']][0]],[pos[e['source']][1],pos[e['target']][1]],color=MINT,lw=.7,alpha=.5)
 for n,(x,y) in pos.items():ax.scatter(x,y,s=40,c=GREEN);ax.text(x*1.13,y*1.13,n,ha='center',fontsize=8)
 ax.set_xlim(-1.35,1.35);ax.set_ylim(-1.3,1.3);ax.text(0,0,f'{len(edges)} inventory declarations\nSSN → SOSA separately graph-verified',ha='center',bbox={'facecolor':CREAM,'edgecolor':'none'},fontsize=10)
rel=fig('05_relationships',relationship)
page('Composability needs typed, evidence-bearing relationships',
 'The relationship output distinguishes inventory declarations, explicit owl:imports triples and URI references. It does not invent overlaps, complements or conflicts from names.',rel,
 'One graph-verifiable import is stronger evidence than a scope resemblance.',
 'SSN imports the SOSA namespace in the retrieved graph. The wider network shows inventory-level dependency declarations; it is not an inferred import closure or a scientific compatibility graph.',
 'Use of RO/BFO can be investigated through declared references and parsed identifier occurrences. Entity–quality composition, I-ADOPT compatibility, crosswalk correctness and shared-model equivalence are not established by these counts and remain explicit review tasks.',
 'resource_relationships.json; resource_depth.json; original CSV relationship fields')

def canonical(f,ax):
 obs=C['observations'];ax.barh([o['observation_id'].replace('_',' ') for o in obs],[o['best_single_dimension_coverage'] for o in obs],color=GREEN);ax.invert_yaxis();ax.set_xlim(0,1);ax.set_xlabel('Best single-resource assessed dimension coverage');ax.tick_params(axis='y',labelsize=8)
canonicalfig=fig('06_observations',canonical)
page('Twenty-five observations turn the scientific question into requirements',
 'The suite spans traits, populations, communities, interactions, fluxes, soils, samples, genomics, agriculture, satellite reflectance and cross-source context.',canonicalfig,
 'Requirement coverage is not yet proof that an ontology can express the observation.',
 'Each observation has explicit requirement IDs and dimensions rather than prose alone. The chart computes best-single-resource coverage using meaningful-or-major provisional scope scores; it does not resolve exact scientific variables.',
 'A separate term-witness ledger checks real SOSA observation, sampling, procedure and result terms in the retrieved graph. Candidate alignment to a requirement is still a project assessment. Exact quantity, taxonomic and support semantics need term-level expert review; no canonical human gold set is claimed.',
 'data/semantics/validation/canonical_observations.json; canonical_benchmark.json; canonical_term_witnesses.json')

def accumulation(f,ax):
 curve=C['greedy_accumulation'];ax.plot([r['size'] for r in curve],[r['coverage'] for r in curve],'o-',color=GREEN,label='Greedy dimension diagnostic')
 exact=C['exact_best'];ax.scatter([r['size'] for r in exact],[r['coverage'] for r in exact],s=70,marker='s',color=GOLD,label='Exact best set, sizes 1–3',zorder=5);ax.set_ylim(0,1.02);ax.set_xlabel('Number of resources');ax.set_ylabel('Covered canonical requirement instances');ax.legend(frameon=False,fontsize=9);ax.grid(axis='y',alpha=.2)
acc=fig('07_accumulation',accumulation)
best=C['exact_best']
page('Composition adds assessed coverage—but leaves unmeasured meaning',
 f"Exact size-1, size-2 and size-3 searches reach {best[0]['coverage']:.1%}, {best[1]['coverage']:.1%} and {best[2]['coverage']:.1%} of requirement instances under the provisional rubric.",acc,
 'This is now a computed observation-requirement diagnostic, not a term-level accumulation result.',
 'Coverage counts repeated dimension requirements across the 25 observations. Exact enumeration covers all resource combinations through size three; the longer curve is greedy. A greedy witness does not prove minimum set size beyond the exact search.',
 'The result supports investigating composition, not adopting a universal winning ontology. Missing dimensions cap coverage, and ordinal rubric choices affect the curve. Subdomain curves, pair overlap, marginal gains and unattained thresholds are retained independently in the output.',
 'canonical_benchmark.json exact_best, thresholds, resource_pairs and subdomains')

def pca(f,ax):
 x=np.array(P['scores']);ax.scatter(x[:,0],x[:,1],color=GREEN,s=20,alpha=.65)
 for n in ['eml','ebv','sosa','envo','go','pato','bfo']:
  if n in P['resource_ids']:
   i=P['resource_ids'].index(n);ax.annotate(n,(x[i,0],x[i,1]),xytext=(4,4),textcoords='offset points',fontsize=9)
 ax.set_xlabel(f"PC1 ({P['explained_variance_ratio'][0]:.1%})");ax.set_ylabel(f"PC2 ({P['explained_variance_ratio'][1]:.1%})");ax.axhline(0,color=GRAY);ax.axvline(0,color=GRAY)
pcafig=fig('08_pca',pca)
page('Exploratory similarity describes the rubric’s structure',
 f"PCA uses {len(P['resource_ids'])} complete-case resources and {len(P['dimensions'])} assessed dimensions. Entirely unmeasured dimensions and incomplete resource rows are excluded, never filled with zero.",pcafig,
 'Nearby points have similar assessed scope, not equivalent concepts.',
 'The centered ordinal vectors are decomposed by singular-value decomposition without imputation. This is a transparent exploratory analysis; it is not an inferential test or an ontology quality ranking.',
 'The shape is conditional on the inventory, the ordinal interpretation and the retained dimensions. Class counts, graph depth and dataset potential are not mixed into this space. Excluded resources and dimensions are listed so the missingness decision remains inspectable.',
 'resource_pca.json; scientific_validation.py analysis methods')

profiles=DS['records'];allfields=sorted({x for r in profiles for x in r['explicit_fields']})
def profilesfig(f,ax):
 a=np.array([[1 if v in r['explicit_fields'] else np.nan for v in allfields] for r in profiles]);cm=ListedColormap([GREEN]);cm.set_bad(GRAY);ax.imshow(a,cmap=cm,aspect='auto');ax.set_yticks(range(len(profiles)),[r['dataset_id'] for r in profiles],fontsize=8);ax.set_xticks(range(len(allfields)),[v.replace('_',' ') for v in allfields],rotation=65,ha='right',fontsize=7)
profilefig=fig('09_datasets',profilesfig)
page('Dataset semantics are documented at different levels of detail',
 'The inventory investigates the eight central sources plus biodiversity, interaction, genomic and phenotyping examples. Each record states whether it describes a product, network, standard or unresolved counterpart.',profilefig,
 'Gray means unassessed—not absent.',
 'Green marks project-coded documented field presence in the selected evidence. Product-level Sentinel metadata can support more detailed assertions than a network landing page; these unequal scopes must not be interpreted as provider-wide quality differences.',
 'eBird’s documentation was blocked by an access challenge; the climate counterpart is unselected; MIAPPE is explicitly a standard comparator, not a dataset. Neither scores nor inventory membership grant access, integration status, scientific compatibility or execution permission.',
 'dataset_benchmark.json; data/semantics/validation/dataset_inventory.json')

def potential(f,ax):
 from collections import defaultdict
 grouped=defaultdict(list)
 for r in profiles:grouped[(r['semantic_diversity_documented_lower_bound'],r['potential_candidate_count'])].append(r['dataset_id'])
 for (x,y),names in sorted(grouped.items()):
  ax.scatter(x,y,color=GREEN,s=40)
  offset=(7,10) if (x,y) not in [(3,2),(6,3)] else (8,-12)
  ax.annotate('\n'.join(sorted(names)),(x,y),xytext=offset,textcoords='offset points',fontsize=9,va='bottom' if offset[1]>0 else 'top',arrowprops={'arrowstyle':'-','color':MINT})
 ax.set_xlabel('Documented semantic dimensions (lower bound)');ax.set_ylabel('Proposed semantic-resource relationships');ax.set_xlim(-.3,7.7);ax.set_ylim(-.4,4.4)
potentialfig=fig('10_potential',potential)
page('Potential is a hypothesis attached to evidence, not a source fact',
 'The diagnostic contrasts documented semantic diversity with the number of curator-proposed semantic-resource relationships. It does not count variables or claim semantic gain.',potentialfig,
 'These are assessed opportunities for expert investigation.',
 'The x-axis is a project-coded lower bound from documented distinct dimensions; missing evidence can lower that bound. The y-axis is a transparent count of proposed relationships, not a validated ontology-potential scale. Datasets at the same coordinates share a label block; ties carry no ranking significance.',
 'Formal ontology references are distinguished from metadata or exchange standards in the ontology-native ranking. Eight separate prioritization rubrics are retained rather than one overall dataset-quality score. Flagship prioritization remains provisional and needs a concrete site, product and scientific question.',
 'dataset_benchmark.json records, edges and rankings','PROJECT ASSESSMENT')

def bipartite(f,ax):
 ax.axis('off');edges=DS['edges'];left=sorted({e['dataset_id'] for e in edges});right=sorted({e['resource_id'] for e in edges});ly={n:.95-i*.9/(len(left)-1) for i,n in enumerate(left)};ry={n:.95-i*.9/(len(right)-1) for i,n in enumerate(right)}
 for e in edges:ax.plot([.18,.82],[ly[e['dataset_id']],ry[e['resource_id']]],color=GREEN if e['claim_class']=='SOURCE FACT' else MINT,lw=1.6 if e['claim_class']=='SOURCE FACT' else .6,alpha=.65,linestyle='-' if e['claim_class']=='SOURCE FACT' else '--')
 for n,y in ly.items():ax.text(.16,y,n,ha='right',va='center',fontsize=9)
 for n,y in ry.items():ax.text(.84,y,n,ha='left',va='center',fontsize=9)
 ax.set_xlim(0,1);ax.set_ylim(0,1)
bip=fig('11_bipartite',bipartite)
page('Explicit references and potential mappings are different edges',
 'The bipartite graph preserves source-documented standard or identifier references separately from proposed resource connections.',bip,
 'Dashed edges are project hypotheses, not scientific mappings.',
 'Solid links describe scoped documentation: Sentinel/STAC, OBIS/Darwin Core and EML, GBIF guidance/Darwin Core and a MGnify sample/ENVO. These do not automatically validate individual terms or all records in a provider.',
 'Candidate edges retain their source evidence and pending expert review. The graph does not silently promote namespace recognition into variable equivalence. A larger graph needs versioned concept-level witnesses, reviewed relation types and independent assessment of meaning preserved or lost.',
 'dataset_benchmark.json.edges; source assertions and scope fields')

questions=load('requested_dataset_pairs.json')
def pairfig(f,ax):
 values={q['left']+' + '+q['right']:q['diagnostic']['added_dimensions_over_best_single'] for q in questions};bars(values,'Additional documented dimensions over the richer member')(f,ax)
pair=fig('12_pairs',pairfig)
page('Pairs can add documented dimensions without becoming compatible',
 'Nine requested scientific pair questions are evaluated against the inventory, including NEON–Sentinel, NEON–TRY, trait–community and flux–satellite combinations.',pair,
 'The pair score does not measure science value or matching feasibility.',
 'The bar counts dimensions documented for only one member beyond the richer member’s set. It is sensitive to incomplete documentation and mixed inventory scopes. All pair records retain scientific_compatibility = unknown and unverified site/time overlap.',
 'BioTIME + climate remains blocked on choosing an actual climate product. ORNL DAAC needs a product, and trait–community comparisons need taxonomic and aggregation rules. The ranked pair table prioritizes review questions rather than declaring a scientifically valid combination.',
 'requested_dataset_pairs.json; dataset_benchmark.json.pairs and pair_ranking')

def location(f,ax):
 a=N['neon']['site_coordinate'];b=N['sentinel']['old_planning_coordinate'];ax.scatter([a[0]],[a[1]],s=80,color=GREEN,label='Public NIWO site coordinate');ax.scatter([b[0]],[b[1]],s=80,marker='x',color=GOLD,label='Historical Sentinel planning point');ax.plot([a[0],b[0]],[a[1],b[1]],'--',color=GRAY);ax.set_xlabel('Longitude (degrees)');ax.set_ylabel('Latitude (degrees)');ax.ticklabel_format(useOffset=False);ax.legend(frameon=False,fontsize=9);ax.margins(.35);ax.text(.03,.5,f"{N['coordinate_diagnostic']['old_planning_point_to_public_site_coordinate_m']/1000:.2f} km planning-point separation\nNeither point proves sensor position",transform=ax.transAxes,fontsize=11)
loc=fig('13_neon_sentinel_support',location)
page('NIWO is evidence-backed, but sensor colocation is not established',
 'Public NEON metadata confirms July 2023 availability for the air-temperature product at NIWO. The retained Sentinel scene footprint contains the published NIWO coordinate.',loc,
 'A site coordinate is not a sensor footprint.',
 'The existing Sentinel planning point differs from the public site coordinate by about 2.4 km. This descriptive haversine diagnostic compares planning coordinates only, not actual instrument supports or distances between matched observations.',
 'The proposed case uses a tower air-temperature interval as environmental context for instantaneous NIR reflectance. Exact sensor/height, units, interval convention, quality flags, release/file identity and source observations remain missing. NEON authentication is absent; no observation file is downloaded.',
 'neon_sentinel_case.json; neon-product.json; neon-site.json; retained sentinel-stream-plan.json')

cross=fig('14_cross_source',diagram(['NEON: aspirated air temperature\nheight-specific • one-/thirty-minute mean','Sentinel: calibrated B08 NIR reflectance\n10 m pixel • instantaneous acquisition','Proposed contextual relationship\nretain independent quantities and supports','Existing exact-support join is insufficient\nscientific association method remains undefined','STOP at expert/data/capability gate\nno equivalence • no cross-source execution']))
page('The useful relationship is contextual, not equivalent',
 'The review package includes a registered Sentinel calibration/rename recipe fragment and a deliberately unbound NEON branch.',cross,
 'Conceptual proposal: preserve the difference between measurements.',
 'An exact observation join requires equal support and intervals; nearest grid sampling does not supply tower sensor support or a scientifically justified point-to-pixel relationship. Those operations cannot be repurposed silently.',
 'A reviewed interval-to-instant contextual association is a genuinely missing capability. Its time convention, sensor selection, spatial relation, tolerance, uncertainty and scientific purpose must be defined before implementation. No operation ID or executable formula is invented to fill that gap.',
 'neon_sentinel_case.json.missing_deterministic_capability; sentinel_proposed_recipe.json','CONCEPTUAL PROPOSAL')

protocol=fig('15_experiment',diagram(['Same 25 tasks • two repeats • one Verde model\njs2/gpt-oss-120b via tool-free OpenClaw','A: natural-language content\nJSON envelope required by installed transport','B: schema-constrained decision\nregistered IDs • references • explicit dispositions','C: deterministic validation of the same B output\nno new model call','D: C plus pending human gate\nno scientific execution in any arm']))
page('The first experiment isolates boundaries, not general model capability',
 f"{V['call_counts']['total']} live calls returned {V['call_counts']['returned']} successful responses and {V['call_counts']['failed']} failures; failures are preserved without repair or mocked replacement.",protocol,
 'Conceptual protocol, backed by retained exact calls.',
 'A uses unconstrained prose inside a mandatory JSON text envelope, so it is not a fully unconstrained provider baseline. B restricts decisions; C and D re-evaluate the same B response deterministically rather than drawing extra samples.',
 'Only the configured Verde model is tested. The smaller-local-model hypothesis and inter-model disagreement remain untested. Draft reference answers are assistant-authored project assessments, not human gold; expert scientific accuracy and unsafe-proposal rates remain unknown.',
 'data/model_experiment/calls.jsonl; summary.json.protocol; decision_tasks.json','CONCEPTUAL PROPOSAL')

def errorfig(f,ax):
 values={'Schema-valid B decisions':V['arms']['B']['metrics']['schema_valid']['numerator'],'Pass scenario checks':V['arms']['C']['metrics']['scientific_valid']['numerator'],'Cite supplied evidence IDs':V['arms']['B']['metrics']['evidence_grounded']['numerator'],'Agree with draft reference':V['arms']['B']['metrics']['draft_oracle_agreement']['numerator']};bars(values,'Decisions out of 50 constrained responses')(f,ax)
errors=fig('16_constraint_results',errorfig)
page('Valid JSON did not establish an evidence-grounded decision',
 f"All 50 B decisions were schema-valid; {50-V['arms']['C']['metrics']['scientific_valid']['numerator']} failed the scenario’s deterministic scientific/reference checks.",errors,
 'The backbone rejected selected plans with no evidence citations.',
 'None of the 50 constrained decisions cited a supplied evidence ID. Passing scenario checks includes abstention/review dispositions; it does not mean that 36 scientific transformations were validated or executed. Citation membership is a syntactic check, not proof of factual grounding.',
 'Agreement with the draft oracle is reported only as a development diagnostic. Human-adjudicated accuracy is unavailable. The human gate blocks every execution because no approval is supplied; zero executions are enforced by the experiment, not evidence that the model is scientifically competent.',
 'data/model_experiment/evaluations.json; summary.json; decision_experiment.py')

def latency(f,ax):
 vals=[V['latency_seconds'][a]['median'] for a in ['A','B']];ax.bar(['A: prose envelope','B: bounded decision'],vals,color=[MINT,GREEN]);ax.set_ylabel('Median call latency (seconds)');ax.set_ylim(0,max(vals)*1.35)
 for i,x in enumerate(vals):ax.text(i,x+.1,f'{x:.2f} s',ha='center',fontsize=14)
 ax.text(.5,.93,'Same configured provider/model; token cost unavailable',transform=ax.transAxes,ha='center',fontsize=10)
lat=fig('17_latency',latency)
page('Repeatability needs more than temperature zero',
 'The pilot retains latency and exact normalized responses for every call. Token usage, cost and provider weight hashes are not exposed by this plugin and remain unknown.',lat,
 'Different wording and different decisions are separate questions.',
 f"Across successful repeat pairs, exact normalized-response matches were {V['reproducibility']['A']['exact_response_matches']}/{V['reproducibility']['A']['successful_repeat_pairs']} for A and {V['reproducibility']['B']['exact_response_matches']}/{V['reproducibility']['B']['successful_repeat_pairs']} for B. Structured action/operation/concept/reference stability was {V['reproducibility']['B']['stable_action_and_operation']}/{V['reproducibility']['B']['successful_repeat_pairs']} for B.",
 'Latency is exploratory for one run, not a speed or cost superiority claim. Pairing and task types must be retained in later statistical comparisons. The original started_at field was recorded after receipt in this runner version; elapsed_seconds records duration and the caveat is retained.',
 'data/model_experiment/summary.json latency_seconds, reproducibility and protocol')

known=Counter(r['dimension'] for r in B if r['score'] is not None)
gaps=fig('18_missingness',bars({d:len(ids)-known[d] for d in dims},'Resources without a dimension-specific assessment'))
page('Unknowns define the next scientific work',
 'The largest gaps are not automatically gaps in existing ontologies; they are gaps in this project’s evidence and reviewed measurement design.',gaps,
 'Do not turn unmeasured scope into an invented absence claim.',
 'The next semantic experiment needs exact term witnesses, expert mappings and a human-authored canonical gold set. The next model experiment needs blinded prose coding, expert decisions, more models and a pre-specified policy for malformed/unsafe proposals.',
 'The next cross-source case needs bounded authenticated NEON observations, actual sensor-position metadata and an approved contextual association method. Independent ecological outcome data are required before claiming scientific validity of MOSAIKS representations. No new scientific operation was added in this pass.',
 'resource_breadth.json; expert_gold_template.json; neon_sentinel_case.json; AGENTS.md','PROJECT ASSESSMENT')

# Editable narrative and tables precede the PDF.
(HERE/'report.json').write_text(json.dumps(pages,indent=2)+'\n')
(HERE/'report.md').write_text('# Scientific validation: evidence, limits and next experiments\n\n'+'\n\n'.join(f"## {i+1}. {p['title']}\n\n{p['deck']}\n\n![{p['takeaway']}](figures/{p['figure']}.svg)\n\n**{p['takeaway']}** {p['caption']}\n\n{p['body']}\n\nEvidence: {p['evidence']}\n\nClaim class: {p['claim_class']}" for i,p in enumerate(pages))+'\n')
(HERE/'tables').mkdir(exist_ok=True)
for name,rows in [('sentinel_issues',S['blockers']),('resource_depth',G),('canonical_optima',C['exact_best']),('dataset_rankings',[{'rubric':k,**v} for k,items in DS['rankings'].items() for v in items])]:
 (HERE/'tables'/f'{name}.json').write_text(json.dumps(rows,indent=2)+'\n')
PDF=ROOT/'output/pdf/AI_ready_scientific_validation_report.pdf';PDF.parent.mkdir(exist_ok=True,parents=True)
c=canvas.Canvas(str(PDF),pagesize=(612,792));c.setTitle('Scientific validation: evidence, limits and next experiments');c.setAuthor('ESIIL | AI-ready datasets prototype')
styles={'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=24,leading=28,textColor=colors.HexColor(INK)),'body':ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16,textColor=colors.HexColor(INK)),'caption':ParagraphStyle('caption',fontName='Helvetica',fontSize=10,leading=14,textColor=colors.HexColor(INK)),'small':ParagraphStyle('small',fontName='Helvetica',fontSize=7.5,leading=10,textColor=colors.HexColor(INK))}
def text(s,x,y,w,style,maxh):
 p=Paragraph(s.replace('&','&amp;'),styles[style]);_,h=p.wrap(w,750)
 if h>maxh:raise ValueError(f'Text block overflow {h}>{maxh}: {s[:80]}')
 p.drawOn(c,x,y-h);return y-h

def base(n):
 c.setFillColor(colors.HexColor(CREAM));c.rect(0,0,612,792,fill=1,stroke=0);c.setFillColor(colors.HexColor(GREEN));c.setFont('Helvetica-Bold',8);c.drawString(45,749,'ESIIL / SCIENTIFIC VALIDATION / 22 OCTOBER 2026');c.setStrokeColor(colors.HexColor(GRAY));c.line(45,48,567,48);c.setFont('Helvetica',8);c.drawString(45,31,'EVIDENCE • MEASURED RESULTS • ASSESSMENTS • UNRESOLVED SCIENCE');c.drawRightString(567,31,str(n))
for n,p in enumerate(pages,1):
 base(n);text(p['title'],45,712,522,'title',65);text(p['deck'],45,641,522,'body',65)
 c.drawImage(str(F/f"{p['figure']}.png"),42,270,width=528,height=317,mask='auto')
 text('<b>'+p['takeaway']+'</b> '+p['caption'],45,250,522,'caption',78);text(p['body'],45,165,522,'body',90);text(p['claim_class']+' | '+p['evidence'],45,68,522,'small',20);c.showPage()
# Technical scope and source attributions, no new result charts.
test_cases=ET.parse(D/'tests.xml').findall('.//testcase')
core_cases=ET.parse(D/'core-tests.xml').findall('.//testcase')
core_skips=sum(c.find('skipped') is not None for c in core_cases)
MAN['test_environments']={}
for name,cases,filename in [('integration',test_cases,'tests.xml'),('core',core_cases,'core-tests.xml')]:
 failures=sum(c.find('failure') is not None or c.find('error') is not None for c in cases);skips=sum(c.find('skipped') is not None for c in cases)
 MAN['test_environments'][name]={'total':len(cases),'passed':len(cases)-failures-skips,'failed':failures,'skipped':skips,'xml_sha256':hashlib.sha256((D/filename).read_bytes()).hexdigest()}
base(19);text('What the experiment does—and does not—establish',45,712,522,'title',65)
y=637
sections=[('Deterministic software','Checks structures, source references, known operations, explicit unit pairs, source calibration references, support conflicts and exact-context identities. It does not decide uncertain scientific equivalence.'),('Bounded AI','Produced actual tool-free model judgments with exact prompts, schemas, provider/model identity and normalized responses. No response was executed; scientific usefulness is not established by JSON validity.'),('Scientists','Must define intended use, sensor/interval support, contextual association, rights attribution, acceptance criteria, canonical mappings and the gold standard. The issue template is not a runtime approval.'),('Evidence and statistical limits','PCA and coverage use provisional ordinal scope assessments. Exact set enumeration stops at size three. Graph metrics inspect only three local snapshots and no imported closure. Dataset records have mixed scopes and unknown fields. No p-value or causal model-competence claim is made.'),('Version and provenance',f"{len(test_cases)} integration tests pass offline; core run: {len(core_cases)-core_skips} passed with {core_skips} optional skips. The new recipe retains the original stale consensus veto, requiring renewed review. Baseline commit {MAN['git_commit']}; pipeline {MAN['versions']['dataset-prototype']}; external CubeDynamics {MAN['versions']['cubedynamics']}; rdflib {MAN['versions']['rdflib']}. All newly added code is metadata analysis or inert evaluation, not a scientific operation or new execution pathway."),('Next experiment','Resolve the expert issue form; obtain sensor-aware bounded NEON evidence; specify and test a scientifically justified association operation only after review; establish independent labels and a human gold set before making scientific accuracy claims.')]
for heading,body in sections:y=text('<b>'+heading+'</b><br/>'+body,45,y,522,'body',110)-18
c.showPage();base(20);text('Reproducibility, sources and review',45,712,522,'title',65)
y=641
sources=[('Repository methods','AGENTS.md; src/dataset_prototype/scientific_validation.py and decision_experiment.py; analysis scripts, typed recipes, tests and retained historical reviews.'),('Ontology snapshots','BFO 2020: https://github.com/BFO-ontology/BFO-2020 ; CC BY 4.0, contributors retained. SOSA/SSN: https://www.w3.org/TR/vocab-ssn/ ; W3C/OGC authors; unmodified snapshots and full W3C license retained.'),('Source metadata','NEON DP1.00002.001 RELEASE-2025 description and public NIWO product/site metadata; CC BY 4.0, product citation/DOI required before scientific use. Sentinel legal notice: https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice ; contains modified Copernicus Sentinel data (2023), accessed via Earth Search.'),('Dataset evidence','Per-assertion primary URLs, scope, interpretation and confidence are retained in data/semantics/validation/dataset_inventory.json. Resource canonical URLs and assessment evidence remain in the existing semantic inventory.'),('External computation','CubeDynamics public API inspected at installed 0.1.0rc3; no source access loaders or upstream source code copied. Upstream documentation: https://cu-esiil.github.io/cubedynamics/ . No change to the pinned backend.'),('Build and verification','analyze.py calculates offline results; evaluate_retained_calls.py scores inert calls; build_report.py generates SVG/PNG figures and the PDF. verify.py checks hashes, counts, approval invariants and PDF integrity. Rebuild instructions and known missing measurements are in README.md.')]
for heading,body in sources:y=text('<b>'+heading+'</b><br/>'+body,45,y,522,'caption',100)-16
text('No new source observations or raster datasets were downloaded or persisted. Public vocabulary graphs and product/site metadata are retained as evidence. This report is separate from the dated pipeline-state report, which remains a historical snapshot.',45,115,522,'caption',60)
c.showPage();c.save()
MAN['report']={'version':'1.0','pages':20,'pdf':str(PDF.relative_to(ROOT)),'sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),'figures':[{'path':f'figures/{n}.svg','sha256':hashlib.sha256((F/f'{n}.svg').read_bytes()).hexdigest()} for n in figures]}
MAN['model_experiment']={'calls':V['call_counts'],'calls_sha256':V['input_calls_sha256'],'human_gold':None,'execution_authorized':False}
MAN['build_sources']=[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [Path(__file__),HERE/'report.json',HERE/'report.md',HERE/'evaluate_retained_calls.py']]
(D/'run_manifest.json').write_text(json.dumps(MAN,indent=2)+'\n');print(f'{PDF}: 20 pages, {len(figures)} figures')
