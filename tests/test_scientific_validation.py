"""Offline tests of metadata analysis, unknowns, provenance and inert decision evaluation."""
import csv,json,copy
from pathlib import Path
import pytest
from pydantic import ValidationError
from dataset_prototype.scientific_validation import validate_assertion,breadth,coverage_benchmark,dataset_diagnostics,graph_metrics
from dataset_prototype.decision_experiment import decision_schema,scientific_evaluate,evaluate_response
from dataset_prototype.contracts import digest
ROOT=Path(__file__).resolve().parents[1]
def inputs():
 resources=list(csv.DictReader((ROOT/'data/semantics/semantic_resources.csv').open()))
 observations=json.loads((ROOT/'data/semantics/validation/canonical_observations.json').read_text())
 return resources,observations

def task(ident='unit_temperature'):
 return next(t for t in json.loads((ROOT/'data/fixtures/validation/decision_tasks.json').read_text()) if t['task_id']==ident)
def choice(t,**kw):return {'task_digest':digest(t),'action':'SELECT','operation_id':'unit.convert','concept_id':None,'parameter_ref':'registry.constants','evidence_ids':['source.statement'],'rationale':'Select only an authoritative registry constant',**kw}

def test_breadth_preserves_unknown_and_evidence():
 resources,_=inputs();rows=breadth(resources)
 assert len(rows)==86*28
 genomic=[r for r in rows if r['dimension']=='genomic']
 assert all(r['score'] is None for r in genomic)
 assert all(r['claim_class']=='PROJECT ASSESSMENT' and not r['expert_reviewed'] for r in rows)
 assert all(r['evidence_source'] for r in rows)

@pytest.mark.parametrize('key',['evidence','evidence_source','confidence'])
def test_scored_assertions_need_evidence(key):
 row={'score':2,'claim_class':'PROJECT ASSESSMENT','evidence':'provisional scope','evidence_source':['source'],'confidence':.5};row[key]=None
 with pytest.raises(ValueError):validate_assertion(row)

def test_deterministic_benchmark_regeneration_and_no_approval():
 r,o=inputs();a=coverage_benchmark(breadth(r[:8]),o[:3]);b=coverage_benchmark(breadth(r[:8]),o[:3])
 assert a==b and not a['execution_authorized'] and a['expert_gold_status']=='pending'
 assert all(v['exact_term_expressibility'] is None and not v['scientific_mapping_approved'] for v in a['observations'])
 assert a['exact_best'][0]['coverage']<=a['exact_best'][1]['coverage']<=a['exact_best'][2]['coverage']

def test_dataset_scores_not_compatibility_or_integration():
 records=json.loads((ROOT/'data/semantics/validation/dataset_inventory.json').read_text());before=copy.deepcopy(records);d=dataset_diagnostics(records)
 assert records==before and not d['execution_authorized']
 assert all(p['scientific_compatibility'] is None and not p['execution_authorized'] for p in d['pairs'])
 assert next(r for r in d['records'] if r['dataset_id']=='ebird')['semantic_diversity_documented_lower_bound']==0
 assert all(not r['unknown_fields_are_zero'] for r in d['records'])


def test_graph_metrics_explicit_dag_and_missing_resolution(tmp_path):
 pytest.importorskip('rdflib')
 p=tmp_path/'graph.ttl';p.write_text('@prefix owl:<http://www.w3.org/2002/07/owl#>. @prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#>. <urn:A> a owl:Class. <urn:B> a owl:Class; rdfs:subClassOf <urn:A>. <urn:C> a owl:Class; rdfs:subClassOf <urn:B>.')
 m=graph_metrics(p,'generated');assert m['named_classes']==3 and m['max_longest_root_depth']==2 and m['median_shortest_root_depth']==1 and m['leaves']==1
 assert m['identifier_resolvability']=='not tested'
 p.write_text(p.read_text()+'<urn:A> rdfs:subClassOf <urn:C>.')
 m=graph_metrics(p,'cycle');assert m['named_hierarchy_cycle'] and m['max_longest_root_depth'] is None

@pytest.mark.parametrize('changes',[{'operation_id':'invented.operation'},{'concept_id':'ENVO:999999999'},{'scale':42},{'code':'print(1)'},{'parameter_ref':'model.constant'},{'task_digest':'stale'}])
def test_model_cannot_expand_capabilities_or_constants(changes):
 t=task();d=choice(t,**changes)
 with pytest.raises(ValidationError):decision_schema(t).model_validate(d)

@pytest.mark.parametrize('ident',['same_name','same_units','same_taxon','same_coordinate','same_timestamp','metadata_injection','bypass_review','shell_sql','ambiguous_method','conflicting_coefficients','rights_label','quality_missing','support_unknown','recipe_edit'])
def test_scientific_preconditions_fail_closed(ident):
 t=task(ident)
 with pytest.raises(ValueError):scientific_evaluate(choice(t),t)


def test_valid_plan_still_has_no_execution_permission():
 t=task();r=scientific_evaluate(choice(t),t)
 assert r['eligible_for_expert_review'] and not r['execution_authorized']
 d=evaluate_response(choice(t),t,'D');assert not d['execution_authorized'] and d['human_gate'].startswith('pending')


def test_registry_and_validators_unchanged_by_inert_model_text(tmp_path):
 paths=[ROOT/'src/dataset_prototype/operations.py',ROOT/'src/dataset_prototype/harmonization.py'];before=[p.read_bytes() for p in paths]
 t=task('metadata_injection');marker=tmp_path/'should-not-exist';payload=f'```python\n__import__("pathlib").Path({str(marker)!r}).write_text("bad")\n```'
 r=evaluate_response(payload,t,'A')
 assert r['detected_patterns']['code_block'] and not marker.exists() and [p.read_bytes() for p in paths]==before
 assert r['human_gold_accuracy'] is None and r['schema_valid'] is None


def test_unsupported_evidence_pointer_and_scientific_edit():
 t=task()
 with pytest.raises(ValueError,match='evidence'):scientific_evaluate(choice(t,evidence_ids=['invented']),t)
 d=choice(t);t['facts']['units']=['DN','K']
 with pytest.raises(ValidationError):scientific_evaluate(d,t)


def test_calibration_uses_documented_source_not_model_numbers():
 t=task('calibration_documented');d=choice(t,operation_id='calibration.scale_offset',parameter_ref='source.calibration')
 assert scientific_evaluate(d,t)['eligible_for_expert_review']
 t['facts'].pop('calibration');d['task_digest']=digest(t)
 with pytest.raises(ValueError,match='coefficients'):scientific_evaluate(d,t)


def test_expert_forms_and_historical_veto_are_not_approvals():
 root=ROOT/'reports/scientific_validation/data'
 form=json.loads((root/'expert_decision_template.json').read_text());assert form['decision'] is None and not form['execution_authorized']
 case=json.loads((root/'sentinel_review_gap_analysis.json').read_text());assert case['historical_consensus_review']['outcome']=='request_revision' and all(not c['veto_lifted'] for c in case['historical_veto_claims'])
 from dataset_prototype.contracts import HarmonizationRecipe,SourceResource
 from dataset_prototype.harmonization import assess
 recipe=HarmonizationRecipe.model_validate_json((root/'sentinel_proposed_recipe.json').read_text())
 assert recipe.agent_review.outcome=='request_revision' and recipe.status=='needs_review'
 # Even an empty source set cannot conceal the inherited veto in deterministic QA.
 qa=assess(recipe,());assert any('veto' in x for x in qa.reasons)
