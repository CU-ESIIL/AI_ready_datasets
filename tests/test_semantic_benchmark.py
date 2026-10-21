"""Metadata-only diagnostics and genuine Parquet outputs; no scientific performance claims."""
import json
from pathlib import Path
from hashlib import sha256
import pytest
from dataset_prototype.contracts import SourceResource
from dataset_prototype.semantic_resources import load_inventory,ResourceAssessment
from dataset_prototype.semantic_benchmark import compute,run,BenchmarkConfig,SCHEMAS

@pytest.fixture
def resources():return load_inventory('data/semantics/semantic_resources.csv')

def test_inventory_breadth_coverage_and_assessment_traceability(resources):
    assert len(resources)>=85
    ids={r.resource_id for r in resources}
    assert {'bfo','dolce','skos','ncbitaxon','tcs','dwc_cm','microbiome_core','eol','lpt','bari','bon_box','anaee','seek','ecolingua'}<=ids
    assert len({r.resource_type for r in resources})==13
    assessments=[ResourceAssessment.model_validate_json(row) for row in Path('data/semantics/assessments.jsonl').read_text().splitlines()]
    assert {a.resource_id for a in assessments}==ids
    assert all(a.evidence and a.reviewer and not a.expert_reviewed for a in assessments)
    assert {value for r in resources for value in r.coverage.values()}=={'strong','partial','indirect','not_target','unknown'}
    assert next(r for r in resources if r.resource_id=='microbiome_core').acronym!='MCO'

def test_diagnostic_oracle_determinism_no_equivalence(resources,client):
    subset=(resources[0],resources[1])
    tables,portfolio=compute(subset,client.resources,[],BenchmarkConfig(portfolio_budget=1))
    assert (tables,portfolio)==compute(subset,client.resources,[],BenchmarkConfig(portfolio_budget=1))
    assert tables['dataset_ontology_edges']==[]
    assert len(tables['ontology_pairs'])==1 and len(tables['dataset_pairs'])==1
    assert tables['dataset_pairs'][0]['scientific_comparability']=='not_evaluated'
    assert all(m['term_count'] is None for m in tables['ontology_metrics'])
    assert portfolio['status']=='recommendation_for_human_review_only'
    assert len(portfolio['selected'])<=1
    with pytest.raises(ValueError,match='bounds'):
        compute(resources,client.resources,[],BenchmarkConfig(max_resources=2))
    with pytest.raises(ValueError,match='duplicate source'):
        compute(subset,(client.resources[0],client.resources[0]),[])

def test_parquet_roundtrip_manifest_and_empty_schema(tmp_path):
    import pyarrow.parquet as pq
    out=tmp_path/'benchmark'
    result=run('data/semantics/semantic_resources.csv',['data/fixtures/catalog.json'],out)
    assert {p.name for p in out.iterdir()}=={name+'.parquet' for name in SCHEMAS}|{'recommended_portfolio.json','run_manifest.json'}
    assert result['status']=='complete' and result['source_data_read'] is False and result['network_access'] is False
    assert result['score_kind']=='project_metadata_diagnostic'
    for name,record in result['files'].items():
        assert sha256((out/name).read_bytes()).hexdigest()==record['sha256']
        if name.endswith('.parquet'):
            table=pq.read_table(out/name)
            assert table.num_rows==record['rows'] and table.schema.metadata[b'scientific_equivalence']==b'not_evaluated'
    edges=pq.read_table(out/'dataset_ontology_edges.parquet')
    assert edges.num_rows==0 and 'evidence_type' in edges.column_names
    assert len(json.loads((out/'recommended_portfolio.json').read_text())['selected'])<=8
    with pytest.raises(FileExistsError):run('data/semantics/semantic_resources.csv',[],out)

def test_source_namespace_edge_is_not_concept_alignment(resources):
    source=SourceResource.model_validate_json(Path('data/fixtures/semantics/sentinel_source.json').read_text())
    bindings=json.loads(Path('data/semantics/namespace_bindings.json').read_text())
    tables,_=compute(resources,(source,),bindings)
    edges=tables['dataset_ontology_edges']
    assert len(edges)==1 and edges[0]['resource_id']=='stac'
    assert edges[0]['match_basis']=='explicit_annotation_namespace'
    assert 'not evaluated' in edges[0]['term_resolution']
    assert tables['dataset_metrics'][0]['fixture'] is True


def test_assessment_drift_namespace_validation_and_failure_manifest(tmp_path,resources,monkeypatch):
    from dataset_prototype.semantic_resources import load_assessments
    from dataset_prototype.semantic_benchmark import read_metadata_json
    from pydantic import ValidationError
    drift=resources[0].model_copy(update={'limitations':'changed without review'})
    with pytest.raises(ValueError,match='assessment content differ'):
        load_assessments('data/semantics/assessments.jsonl',(drift,*resources[1:]))
    with pytest.raises(ValidationError,match='empty annotation'):
        compute(resources,[],[{'resource_id':'envo','prefixes':[''],'evidence':'fixture'}])
    huge=tmp_path/'too-large.json'
    with huge.open('wb') as handle:handle.truncate(8*1024*1024+1)
    with pytest.raises(ValueError,match='byte budget'):read_metadata_json(huge)
    import pyarrow.parquet as pq
    def failure(*args,**kwargs):raise OSError('explicit generated sink failure')
    monkeypatch.setattr(pq,'write_table',failure)
    out=tmp_path/'failure'
    with pytest.raises(OSError):run('data/semantics/semantic_resources.csv',[],out)
    manifest=json.loads((out/'run_manifest.json').read_text())
    assert manifest['status']=='failed' and manifest['source_data_read'] is False
