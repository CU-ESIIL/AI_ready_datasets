"""Bounded, offline metadata diagnostics; never scientific equivalence or ontology adoption."""
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import platform
from typing import Literal
from pydantic import Field
from .contracts import Contract, SourceResource, digest
from .semantic_discovery import enrich
from .semantic_resources import COVERAGE_DIMENSIONS, load_inventory, load_assessments, NamespaceBinding

RATING={'strong':1.,'partial':.5,'indirect':.25,'not_target':0.,'unknown':None}
SEMANTIC_FIELDS=('source_label','source_definition','source_concept_id','source_concept_uri',
    'source_vocabulary','standard_name','standard_name_scheme','unit','unit_scheme','quantity_kind',
    'entity_hint','property_hint','matrix_hint','context_hint','taxon_identifier','taxon_scheme',
    'method','protocol','sensor','platform','spatial_resolution','spatial_support',
    'temporal_resolution','temporal_support','native_crs','processing_level','processing_baseline')

class BenchmarkConfig(Contract):
    schema_version: Literal['1']='1'
    portfolio_budget: int=Field(default=8,ge=1,le=64)
    max_resources: int=Field(default=256,ge=1,le=256)
    max_datasets: int=Field(default=128,ge=1,le=128)
    score_kind: Literal['project_metadata_diagnostic']='project_metadata_diagnostic'

# Explicit schemas retain useful types even when a diagnostic has zero rows.
SCHEMAS={
 'ontology_metrics': [('resource_id','s'),('resource_type','s'),('coverage_score','f'),('known_dimensions','i'),('unknown_dimensions','i'),('core_candidate','b'),('verification_scope','s'),('term_count','i'),('score_kind','s')],
 'ontology_pairs': [('left_resource','s'),('right_resource','s'),('assessed_coverage_jaccard','f'),('shared_dimensions','ls'),('unknown_dimensions','i'),('relationship','s')],
 'benchmark_coverage': [('resource_id','s'),('dimension','s'),('rating','s'),('diagnostic_weight','f'),('assessment_id','s')],
 'semantic_gaps': [('gap_id','s'),('dimension','s'),('strong_resources','i'),('unknown_resources','i'),('interpretation','s')],
 'dataset_metrics': [('dataset_key','s'),('asset_id','s'),('version','s'),('fixture','b'),('variables','i'),('evidence_records','i'),('native_records','i'),('model_judgment_records','i'),('present_fields','ls'),('documentation_score','f'),('source_digest','s')],
 'dataset_ontology_edges': [('dataset_key','s'),('resource_id','s'),('identifier','s'),('match_basis','s'),('evidence_location','s'),('evidence_type','s'),('term_resolution','s')],
 'dataset_pairs': [('left_dataset','s'),('right_dataset','s'),('field_presence_jaccard','f'),('shared_resource_references','ls'),('scientific_comparability','s')],
 'dataset_rankings': [('rank','i'),('dataset_key','s'),('asset_id','s'),('documentation_score','f'),('score_kind','s')],
}


def read_metadata_json(path):
    with Path(path).open('rb') as handle:
        content=handle.read(8*1024*1024+1)
    if len(content)>8*1024*1024:raise ValueError('input exceeds metadata byte budget')
    return json.loads(content)


def _jaccard(left,right):
    union=set(left)|set(right)
    return len(set(left)&set(right))/len(union) if union else None


def compute(resources,sources,bindings,config=BenchmarkConfig()):
    """Pure calculations over bounded metadata; scores cannot feed harmonization approvals."""
    resources=tuple(resources);sources=tuple(sources)
    if not resources:raise ValueError('nonempty resource inventory required')
    if len(resources)>config.max_resources or len(sources)>config.max_datasets:
        raise ValueError('metadata diagnostic input exceeds explicit bounds')
    if len({r.resource_id for r in resources})!=len(resources):raise ValueError('duplicate resource ID')
    bindings=tuple(NamespaceBinding.model_validate(binding) if isinstance(binding,dict) else binding for binding in bindings)
    ids={r.resource_id for r in resources}
    if any(binding.resource_id not in ids for binding in bindings):raise ValueError('unknown namespace resource')
    tables={name:[] for name in SCHEMAS}
    for resource in resources:
        known=[RATING[value] for value in resource.coverage.values() if value!='unknown']
        tables['ontology_metrics'].append(dict(resource_id=resource.resource_id,resource_type=resource.resource_type,
            coverage_score=sum(known)/len(COVERAGE_DIMENSIONS),known_dimensions=len(known),
            unknown_dimensions=len(COVERAGE_DIMENSIONS)-len(known),core_candidate=resource.core_candidate,
            verification_scope=resource.verification_scope,term_count=None,score_kind=config.score_kind))
        tables['benchmark_coverage'].extend(dict(resource_id=resource.resource_id,dimension=dimension,
            rating=rating,diagnostic_weight=RATING[rating],assessment_id=resource.assessment_id)
            for dimension,rating in resource.coverage.items())
    for left,right in combinations(sorted(resources,key=lambda r:r.resource_id),2):
        dims=[key for key in COVERAGE_DIMENSIONS if 'unknown' not in (left.coverage[key],right.coverage[key])]
        numerator=sum(min(RATING[left.coverage[k]],RATING[right.coverage[k]]) for k in dims)
        denominator=sum(max(RATING[left.coverage[k]],RATING[right.coverage[k]]) for k in dims)
        tables['ontology_pairs'].append(dict(left_resource=left.resource_id,right_resource=right.resource_id,
            assessed_coverage_jaccard=numerator/denominator if denominator else None,
            shared_dimensions=[key for key in dims if RATING[left.coverage[key]]>0 and RATING[right.coverage[key]]>0],
            unknown_dimensions=len(COVERAGE_DIMENSIONS)-len(dims),relationship='assessed_scope_overlap_only'))
    for dimension in COVERAGE_DIMENSIONS:
        strong=sum(r.coverage[dimension]=='strong' for r in resources)
        unknown=sum(r.coverage[dimension]=='unknown' for r in resources)
        tables['semantic_gaps'].append(dict(gap_id='coverage.'+dimension,dimension=dimension,strong_resources=strong,
            unknown_resources=unknown,interpretation='Local project assessment only; not evidence that no external resource exists.'))
    tables['semantic_gaps'].append(dict(gap_id='research.cross_support_justification',dimension='cross_support_justification',
        strong_resources=None,unknown_resources=len(resources),
        interpretation='Open literature-review hypothesis; this benchmark does not measure scientific justification for cross-scale transformations.'))
    namespaces={}
    for source in sources:
        source=enrich(source)
        key=digest(source)
        if key in namespaces:raise ValueError('duplicate source metadata record')
        evidence=source.semantics.evidence
        factual=[e for e in evidence if e.evidence_type.value in {'SOURCE_DOCUMENTED','OBSERVED_IN_DATA','DERIVED_DETERMINISTICALLY'}]
        fields=sorted({field for field in SEMANTIC_FIELDS if any(getattr(e,field) not in (None,'',()) for e in factual)})
        tables['dataset_metrics'].append(dict(dataset_key=key,asset_id=source.asset_id,version=source.version,
            fixture=source.metadata.fixture,variables=len(source.variables),evidence_records=len(evidence),
            native_records=sum(e.evidence_type.value=='SOURCE_DOCUMENTED' for e in evidence),
            model_judgment_records=sum(e.evidence_type.value=='MODEL_JUDGMENT' for e in evidence),
            present_fields=fields,documentation_score=len(fields)/len(SEMANTIC_FIELDS),source_digest=key))
        refs=set();seen=set()
        for item in factual:
            annotations=[value for value in (item.source_concept_id,item.source_concept_uri,item.source_vocabulary,
                item.standard_name_scheme,item.unit_scheme,item.taxon_identifier,item.taxon_scheme) if value]
            for annotation in annotations:
                for binding in bindings:
                    if annotation in binding.exact or any(annotation.startswith(prefix) for prefix in binding.prefixes):
                        edge=(binding.resource_id,annotation,item.evidence_location,item.evidence_type.value)
                        if edge in seen:continue
                        seen.add(edge);refs.add(binding.resource_id)
                        tables['dataset_ontology_edges'].append(dict(dataset_key=key,resource_id=edge[0],identifier=annotation,
                            match_basis='explicit_annotation_namespace',evidence_location=item.evidence_location,
                            evidence_type=item.evidence_type.value,term_resolution='namespace_only; concept existence and equivalence not evaluated'))
        namespaces[key]=refs
    metrics=sorted(tables['dataset_metrics'],key=lambda x:x['dataset_key'])
    for left,right in combinations(metrics,2):
        tables['dataset_pairs'].append(dict(left_dataset=left['dataset_key'],right_dataset=right['dataset_key'],
            field_presence_jaccard=_jaccard(left['present_fields'],right['present_fields']),
            shared_resource_references=sorted(namespaces[left['dataset_key']]&namespaces[right['dataset_key']]),
            scientific_comparability='not_evaluated'))
    for rank,row in enumerate(sorted(metrics,key=lambda x:(-x['documentation_score'],x['asset_id'],x['dataset_key'])),1):
        tables['dataset_rankings'].append(dict(rank=rank,dataset_key=row['dataset_key'],asset_id=row['asset_id'],
            documentation_score=row['documentation_score'],score_kind=config.score_kind))
    # Greedy, equal-dimension weighted set cover; the budget and all marginal gains are recorded.
    covered={key:0. for key in COVERAGE_DIMENSIONS};chosen=[]
    eligible=[r for r in resources if r.status not in {'historical','unresolved','inactive_registry'}
        and r.verification_scope in {'registry_metadata','primary_documentation'}]
    for _ in range(config.portfolio_budget):
        choices=[]
        for resource in eligible:
            if resource.resource_id in {item['resource_id'] for item in chosen}:continue
            gain=sum(max(0,(RATING[resource.coverage[k]] or 0)-covered[k]) for k in COVERAGE_DIMENSIONS)
            choices.append((-gain,not resource.core_candidate,resource.resource_id,resource))
        if not choices:break
        negative,_,_,resource=min(choices,key=lambda x:x[:3])
        if negative>=0:break
        chosen.append({'resource_id':resource.resource_id,'marginal_assessed_coverage_gain':-negative})
        for key in covered:covered[key]=max(covered[key],RATING[resource.coverage[key]] or 0)
    portfolio={'schema_version':'1','status':'recommendation_for_human_review_only','score_kind':config.score_kind,
        'method':'greedy equal-dimension coverage; unknown contributes no assessed gain; core-candidate then ID tie break',
        'budget':config.portfolio_budget,'selected':chosen,'assessed_coverage':covered,
        'not_established':['scientific_equivalence','ontology_quality','term_alignment','scientific_adoption','dataset_suitability']}
    return tables,portfolio


def run(inventory_path,source_paths,output,*,bindings_path=Path('data/semantics/namespace_bindings.json'),config=BenchmarkConfig()):
    """Write requested Parquet artifacts and failure-aware checksummed manifest; metadata only."""
    import pyarrow as pa
    import pyarrow.parquet as pq
    output=Path(output)
    if output.exists():raise FileExistsError('benchmark output already exists; use a fresh directory')
    source_paths=tuple(map(Path,source_paths))
    if len(source_paths)>config.max_datasets:raise ValueError('too many source metadata paths')
    planned_inputs=[Path(inventory_path),Path(bindings_path),*source_paths,
                    Path(inventory_path).with_name('assessments.jsonl')]
    if sum(path.stat().st_size for path in planned_inputs)>16*1024*1024:
        raise ValueError('run exceeds total metadata byte budget')
    resources=load_inventory(inventory_path)
    assessment_path=Path(inventory_path).with_name('assessments.jsonl')
    load_assessments(assessment_path,resources)
    sources=[]
    for path in source_paths:
        records=read_metadata_json(path)
        sources.extend(SourceResource.model_validate(row) for row in (records if isinstance(records,list) else [records]))
    bindings=read_metadata_json(bindings_path)
    # Validate/compute before creating artifacts. No discovery service or raster reader is called.
    tables,portfolio=compute(resources,sources,bindings,config)
    output.mkdir(parents=True,exist_ok=False)
    inputs=[Path(inventory_path),Path(bindings_path),*map(Path,source_paths)]
    assessments=Path(inventory_path).with_name('assessments.jsonl')
    if assessments.exists():inputs.append(assessments)
    verification=Path(inventory_path).with_name('verification_sources.json')
    if verification.exists():inputs.append(verification)
    manifest={'schema_version':'1','status':'incomplete','score_kind':config.score_kind,
        'scientific_validation':'not_established','source_data_read':False,'network_access':False,
        'created_at':datetime.now(timezone.utc).isoformat(),'runtime':{'python':platform.python_version(),'pyarrow':pa.__version__},'config':config.model_dump(mode='json'),
        'code_digest':digest({name:(Path(__file__).parent/name).read_text() for name in
            ['semantic_benchmark.py','semantic_resources.py','semantic_discovery.py','contracts.py']}),
        'inputs':[{ 'path':str(path),'sha256':sha256(path.read_bytes()).hexdigest()} for path in inputs],
        'source_metadata_digests':[digest(enrich(source)) for source in sources],
        'resource_count':len(resources),'source_count':len(sources),'fixture_sources':sum(s.metadata.fixture for s in sources),
        'files':{},'limitations':['Inventory and coverage are provisional project assessments, not ontology graph measurements.',
            'Dataset rankings measure metadata field presence, not evidence correctness or scientific quality.',
            'Dataset-ontology edges are namespace references, not accepted mappings.',
            'No raw or harmonized source observations are accessed or saved.']}
    def save_manifest():
        (output/'run_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    save_manifest()
    types={'s':pa.string(),'f':pa.float64(),'i':pa.int64(),'b':pa.bool_(),'ls':pa.list_(pa.string())}
    try:
        for name,fields in SCHEMAS.items():
            schema=pa.schema([(field,types[kind]) for field,kind in fields],metadata={b'score_kind':config.score_kind.encode(),b'scientific_equivalence':b'not_evaluated',
                b'inputs_digest':digest(manifest['inputs']).encode(),b'code_digest':manifest['code_digest'].encode(),
                b'config_digest':digest(config).encode()})
            table=pa.Table.from_pylist(tables[name],schema=schema)
            path=output/(name+'.parquet')
            pq.write_table(table,path.with_suffix('.partial'),compression='zstd',version='2.6')
            path.with_suffix('.partial').rename(path)
            # Real Parquet round trip and identity, including empty tables.
            reopened=pq.read_table(path)
            if not reopened.equals(table):raise ValueError('Parquet round-trip mismatch')
            manifest['files'][path.name]={'sha256':sha256(path.read_bytes()).hexdigest(),'rows':table.num_rows,'schema':str(table.schema)}
        portfolio.update(inputs_digest=digest(manifest['inputs']),code_digest=manifest['code_digest'],config_digest=digest(config))
        path=output/'recommended_portfolio.json'
        path.write_text(json.dumps(portfolio,indent=2,sort_keys=True)+'\n')
        manifest['files'][path.name]={'sha256':sha256(path.read_bytes()).hexdigest()}
        manifest['status']='complete'
    except BaseException as error:
        manifest.update(status='failed',error_type=type(error).__name__)
        raise
    finally:save_manifest()
    return manifest
