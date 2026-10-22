"""Offline scientific metadata experiments; no execution/approval authority.

Coverage measures provisional dimension support, not term expressibility or equivalence.
Graph metrics inspect explicit local triples without fetching imports or reasoning.
"""
from collections import Counter,defaultdict,deque
from itertools import combinations
from statistics import median
from pathlib import Path
import json,math
from .contracts import digest

VERSION='scientific-validation-v1'
DIMENSIONS=('molecular','genomic','cellular','anatomical','organismal','taxonomic','trait','phenotype','behavior','population','community','ecological_interaction','trophic_relationship','ecosystem','habitat','environmental_context','observation','measurement','sampling','experimental_design','method_protocol','spatial_representation','spatial_support','temporal_representation','temporal_support','quantitative_value','units','provenance')
LEGACY={'anatomical':'anatomy','organismal':'organism','taxonomic':'taxonomy','ecological_interaction':'interaction','environmental_context':'environment','method_protocol':'method','spatial_representation':'space','temporal_representation':'time'}
ORDINAL={'not_target':0,'indirect':1,'partial':2,'strong':3,'unknown':None}

def validate_assertion(row):
    if row.get('score') not in (None,0,1,2,3):raise ValueError('invalid ordinal score')
    if row.get('claim_class') not in {'SOURCE FACT','PROJECT ASSESSMENT','MEASURED PROJECT RESULT','MODEL JUDGMENT','HUMAN JUDGMENT'}:raise ValueError('explicit claim class required')
    if row.get('score') is not None and (not row.get('evidence') or not row.get('evidence_source') or row.get('confidence') is None):raise ValueError('scored assertion requires evidence, source and confidence')
    return row

def breadth(resources):
    rows=[]
    for r in resources:
        for d in DIMENSIONS:
            key=LEGACY.get(d,d);rating=r.get(key,'unknown')
            rows.append(validate_assertion({'resource_id':r['resource_id'],'dimension':d,'score':ORDINAL[rating],
                'evidence':f"Existing assessment {r['assessment_id']}: {key}={rating}" if key in r else 'No dimension-specific assessment exists',
                'evidence_source':[f"data/semantics/semantic_resources.csv#{r['resource_id']}",*json.loads(r['evidence_source'])],
                'confidence':.5 if rating!='unknown' else None,'claim_class':'PROJECT ASSESSMENT',
                'rubric':'0=not targeted by assessed scope (NOT verified absence); 1=peripheral; 2=meaningful; 3=major focus; null=unknown',
                'expert_reviewed':False}))
    return rows

def coverage_benchmark(rows,observations):
    """Exact top-3 search on dimension-level assessment masks; no semantic inference."""
    by=defaultdict(set)
    for r in rows:
        validate_assertion(r)
        if r['score'] is not None and r['score']>=2:by[r['resource_id']].add(r['dimension'])
        else:by[r['resource_id']]  # retain wholly unknown resources
    ids=sorted(by);weights=Counter(req['dimension'] for o in observations for req in o['requirements'])
    relevant=sorted(weights);bits={d:1<<i for i,d in enumerate(relevant)}
    masks={r:sum(bits[d] for d in by[r] if d in bits) for r in ids};den=sum(weights.values())
    def value(mask):return sum(weights[d] for d in relevant if mask&bits[d])
    def union(group):
        m=0
        for r in group:m|=masks[r]
        return m
    exact=[]
    for k in (1,2,3):
        best=max(combinations(ids,k),key=lambda g:(value(union(g)),tuple(-ids.index(x) for x in g)))
        exact.append({'size':k,'resources':best,'covered_requirement_instances':value(union(best)),'denominator':den,'coverage':value(union(best))/den,'claim_class':'MEASURED PROJECT RESULT','interpretation':'exact optimum under provisional dimension rubric; not term-level expressibility'})
    curve=[];chosen=[];current=0
    for _ in ids:
        remaining=[r for r in ids if r not in chosen]
        nxt=min(remaining,key=lambda r:(-value(current|masks[r]),r));new=current|masks[nxt]
        if value(new)==value(current):break
        chosen.append(nxt);curve.append({'size':len(chosen),'resource_added':nxt,'resources':chosen.copy(),'coverage':value(new)/den,'marginal_requirement_instances':value(new)-value(current)});current=new
    per=[]
    for o in observations:
        required={r['dimension'] for r in o['requirements']};best=min(ids,key=lambda r:(-len(by[r]&required),r))
        per.append({'observation_id':o['observation_id'],'domain':o['domain'],'best_single':best,'covered_dimensions':sorted(by[best]&required),'requirements':len(o['requirements']),'best_single_dimension_coverage':len(by[best]&required)/len(required),'remaining_after_all_resources':sorted(required-set().union(*by.values())),'exact_term_expressibility':None,'scientific_mapping_approved':False})
    thresholds=[]
    for threshold in [.5,.75,.9,1.]:
        witness=next((r for r in exact if r['coverage']>=threshold),None)
        greedy=next((r for r in curve if r['coverage']>=threshold),None)
        thresholds.append({'threshold':threshold,'minimum_size':witness['size'] if witness else None,'exact_search_limit':3,'greedy_witness_size':greedy['size'] if greedy else None,'status':'exact within search limit' if witness else 'not reached' if not greedy else 'minimum beyond size 3 not established'})
    pairs=[]
    for a,b in combinations(ids,2):
        total=by[a]|by[b];overlap=by[a]&by[b]
        pairs.append({'left':a,'right':b,'assessed_overlap_jaccard':len(overlap)/len(total) if total else None,'added_dimensions_over_best_single':len(total)-max(len(by[a]),len(by[b])),'scientific_complementarity':None})
    domains={}
    for domain in sorted({o['domain'] for o in observations}):
        subset=[o for o in observations if o['domain']==domain];w=Counter(q['dimension'] for o in subset for q in o['requirements']);c=set();selected=[];series=[]
        for _ in ids:
            nxt=min((r for r in ids if r not in selected),key=lambda r:(-sum(w[d] for d in c|by[r]),r));new=c|by[nxt];gain=sum(w[d] for d in new-c)
            if not gain:break
            selected.append(nxt);c=new;series.append({'size':len(selected),'added':nxt,'coverage':sum(w[d] for d in c)/sum(w.values())})
        domains[domain]=series
    marginals=[]
    for r in ids:
        others=union([i for i in ids if i!=r]);single=masks[r]
        marginals.append({'resource_id':r,'standalone_requirement_instances':value(single),'unique_requirement_instances_vs_all_others':value(others|single)-value(others),'gain_added_to_best_single':value(single|union(exact[0]['resources']))-exact[0]['covered_requirement_instances'],'claim_class':'MEASURED PROJECT RESULT under project dimension rubric'})
    return {'resource_marginals':marginals,'version':VERSION,'score_kind':'project_assessment_dimension_coverage','expert_gold_status':'pending','execution_authorized':False,'exact_best':exact,'greedy_accumulation':curve,'thresholds':thresholds,'observations':per,'resource_pairs':pairs,'subdomains':domains}

def graph_metrics(path,resource_id):
    """Named-class explicit subclass DAG metrics. No imported closure or OWL inference."""
    from rdflib import Graph,URIRef,BNode,RDF,RDFS,OWL,SKOS
    graph=Graph().parse(Path(path),format='turtle');classes={n for n in graph.subjects(RDF.type,OWL.Class) if isinstance(n,URIRef)}
    classes|={n for n in graph.subjects(RDF.type,RDFS.Class) if isinstance(n,URIRef)}
    parents={n:set(graph.objects(n,RDFS.subClassOf))&classes for n in classes};children={n:{c for c in classes if n in parents[c]} for n in classes}
    roots=sorted((n for n in classes if not parents[n]),key=str);dist={r:0 for r in roots};q=deque(roots)
    while q:
        n=q.popleft()
        for c in children[n]:
            if c not in dist or dist[c]>dist[n]+1:dist[c]=dist[n]+1;q.append(c)
    # Kahn detects cycles, including cycles reachable from a root.
    indegree={n:len(parents[n]) for n in classes};ready=deque(roots);longest={r:0 for r in roots};visited=0
    while ready:
        n=ready.popleft();visited+=1
        for c in children[n]:
            longest[c]=max(longest.get(c,0),longest[n]+1);indegree[c]-=1
            if indegree[c]==0:ready.append(c)
    cycle=visited!=len(classes)
    definitions={URIRef('http://purl.obolibrary.org/obo/IAO_0000115'),SKOS.definition};synonyms={SKOS.altLabel,*[URIRef('http://www.geneontology.org/formats/oboInOwl#'+x) for x in ['hasExactSynonym','hasRelatedSynonym','hasBroadSynonym','hasNarrowSynonym']]}
    imports=sorted(str(x) for x in graph.objects(None,OWL.imports));objectprops={n for n in graph.subjects(RDF.type,OWL.ObjectProperty)}
    declared={n for n in graph.subjects(RDF.type,None) if isinstance(n,URIRef)};reused=sorted({str(n) for triple in graph for n in (triple[0],triple[2]) if isinstance(n,URIRef) and n not in declared and str(n).startswith('http://purl.obolibrary.org/obo/')})
    return {'resource_id':resource_id,'claim_class':'MEASURED PROJECT RESULT','triples':len(graph),'named_classes':len(classes),'max_longest_root_depth':None if cycle else max(longest.values(),default=0),'median_shortest_root_depth':None if cycle or len(dist)!=len(classes) else median(dist.values()) if dist else None,'named_hierarchy_cycle':cycle,'mean_direct_branching':sum(map(len,children.values()))/len(classes) if classes else None,'leaves':sum(not v for v in children.values()),'object_property_declarations':len(objectprops),'distinct_predicates_used':len(set(graph.predicates())),'restrictions':len(set(graph.subjects(RDF.type,OWL.Restriction))),'intersection_expressions':len(set(graph.subjects(OWL.intersectionOf,None))),'definition_triples':sum(1 for _,p,_ in graph if p in definitions),'synonym_triples':sum(1 for _,p,_ in graph if p in synonyms),'xref_triples':sum(1 for _,p,_ in graph if str(p).endswith('hasDbXref')),'http_named_classes':sum(str(n).startswith(('https://','http://')) for n in classes),'identifier_resolvability':'not tested','imports':imports,'version_iris':sorted(str(x) for x in graph.objects(None,OWL.versionIRI)),'external_obo_references':reused,'scope':'explicit local graph only; no imports followed, no entailment, class count is not ontology quality'}

def resource_edges(resources,metrics):
    edges=[]
    for r in resources:
        for target in json.loads(r['imports_or_dependencies']):edges.append({'source':r['resource_id'],'target':target,'relation':'declared_import_or_dependency','claim_class':'SOURCE FACT','evidence':json.loads(r['evidence_source']),'verification':'inventory declaration; not graph-verified'})
    for m in metrics:
        for target in m['imports']:edges.append({'source':m['resource_id'],'target':target,'relation':'imports','claim_class':'MEASURED PROJECT RESULT','evidence':[m['resource_id']+'.ttl'],'verification':'explicit owl:imports triple'})
        for target in m['external_obo_references']:edges.append({'source':m['resource_id'],'target':target,'relation':'references_identifier','claim_class':'MEASURED PROJECT RESULT','evidence':[m['resource_id']+'.ttl'],'verification':'URI occurrence only; no equivalence inferred'})
    return edges

def dataset_diagnostics(records,resource_types=None):
    """Declared-dimension lower bounds and project-candidate potential; no unknown imputation."""
    rows=[];edges=[];resource_types=resource_types or {}
    for d in records:
        facts=d['assertions']
        for a in facts:
            if not a['evidence_source'] or not a['statement']:raise ValueError('dataset assertion needs evidence')
        dims=set(x for a in facts for x in a['semantic_dimensions']);candidates=d['candidate_resources']
        known_fields=set(x for a in facts for x in a['explicit_fields'])
        rows.append({'dataset_id':d['dataset_id'],'scope':d['scope'],'semantic_diversity_documented_lower_bound':len(dims),'documented_dimensions':sorted(dims),'explicit_fields':sorted(known_fields),'machine_access_documented':any('machine_access' in a['explicit_fields'] for a in facts),'potential_candidate_count':len(candidates),'ontology_potential_kind':'PROJECT ASSESSMENT: count of curator-proposed resource relationships; not semantic gain','explicit_formal_ontology_references':sum(resource_types.get(c['resource_id']) in {'formal_ontology','upper_ontology','application_ontology','relation_ontology'} for c in d['explicit_resource_links']),'explicit_ontology_use':d['explicit_resource_links'],'evidence_assertions':len(facts),'integration_status':d['integration_status'],'unknown_fields_are_zero':False,'execution_authorized':False})
        for c in candidates:edges.append({'dataset_id':d['dataset_id'],'resource_id':c['resource_id'],'relation':'potentially_maps_to','claim_class':'PROJECT ASSESSMENT','evidence':c['evidence'],'review_status':'needs expert review'})
        for c in d['explicit_resource_links']:edges.append({'dataset_id':d['dataset_id'],'resource_id':c['resource_id'],'relation':c['relation'],'claim_class':'SOURCE FACT','evidence':c['evidence'],'term_resolution':False})
    pairs=[]
    for a,b in combinations(rows,2):
        x,y=set(a['documented_dimensions']),set(b['documented_dimensions'])
        pairs.append({'left':a['dataset_id'],'right':b['dataset_id'],'shared_documented_dimensions':sorted(x&y),'distinct_documented_dimensions':sorted(x^y),'union_documented_dimensions':len(x|y),'added_dimensions_over_best_single':len(x|y)-max(len(x),len(y)),'scientific_compatibility':None,'site_time_overlap_verified':False,'execution_authorized':False})
    criteria={'ontology_native':lambda r:r['explicit_formal_ontology_references'],'ontology_ready':lambda r:r['potential_candidate_count'],'cross_scale':lambda r:len(set(r['documented_dimensions'])&{'space','time','support','organism','community','ecosystem'}),'multimodal':lambda r:len(set(r['documented_dimensions'])&{'genomic','trait','environment','observation','interaction'}),'community_ecosystem':lambda r:len(set(r['documented_dimensions'])&{'community','ecosystem'}),'interaction':lambda r:int('interaction' in r['documented_dimensions']),'semantic_stress_test':lambda r:r['semantic_diversity_documented_lower_bound'],'flagship_review_candidate':lambda r:len(r['explicit_fields'])+r['potential_candidate_count']}
    rankings={name:[{'dataset_id':r['dataset_id'],'rubric_value':fn(r),'rank':i+1,'kind':'review prioritization diagnostic; ties share scientific standing; not dataset quality'} for i,r in enumerate(sorted(rows,key=lambda r:(-fn(r),r['dataset_id'])))] for name,fn in criteria.items()}
    return {'records':rows,'edges':edges,'pairs':pairs,'rankings':rankings,'pair_ranking':sorted(pairs,key=lambda r:(-r['added_dimensions_over_best_single'],-r['union_documented_dimensions'],r['left'],r['right'])),'execution_authorized':False}
