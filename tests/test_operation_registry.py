"""Trust-boundary tests run with sockets disabled and VERDE completely unavailable."""
import json
from datetime import datetime, timezone, timedelta
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import Operation, HumanDecision, RawObservation, digest
from dataset_prototype.operations import REGISTRY, execution_identity, UNIT_CONVERSIONS
from dataset_prototype.decision_ir import (RecipeDecision, SelectDecision, ParameterizeDecision,
    build_capabilities, decision_schema, process_output, compile_decision, execute_approved,
    FixtureDecisionModel, request_model_decision, SemanticMappingProposal, validate_mapping_proposal)
from dataset_prototype.harmonization import run, assess


def decision_for(cap):
    return RecipeDecision(capability_digest=cap.identity,status='PROPOSED',rationale='Fixture choice, not scientific evidence',
        steps=tuple(SelectDecision(operation_id=o.operation_id,option_id=o.option_id) for o in cap.options))


def approve(recipe):
    return HumanDecision(recipe_digest=digest(recipe),status='approved',reviewer='generated test reviewer',
        rationale='Synthetic governance test only',timestamp=datetime(2026,10,21,tzinfo=timezone.utc),fixture=True)


def test_registry_closed_versioned_and_described():
    manifest=REGISTRY.manifest()
    assert len([d for d in manifest['operations'] if d['backend']=='core'])==10 and manifest['registry_digest']==execution_identity()['registry_digest']
    for definition in manifest['operations']:
        assert definition['version']=='1' and definition['parameter_schema']['additionalProperties'] is False
        assert definition['preconditions'] and definition['scientific_assumptions'] and definition['tests']
        assert definition['implementation_reference']==('dataset_prototype.operations._execute_rows' if definition['backend']=='core' else 'dataset_prototype.cubedynamics_backend.CubeDynamicsBackend.execute')
    with pytest.raises(ValueError,match='UNSUPPORTED_OPERATION'):REGISTRY.get('spectral.magic_correction')
    with pytest.raises(TypeError):UNIT_CONVERSIONS['K','m']=(7,1)
    entry=REGISTRY.get('unit.convert');entry.parameter_schema.clear()
    assert REGISTRY.get('unit.convert').parameter_schema


def test_structural_then_semantic_validation_and_provenance(bundle):
    r,m,_,raw=bundle
    cap=build_capabilities((r,),(m,));d=decision_for(cap)
    result=process_output(d.model_dump_json(),cap,(r,),(m,))
    assert result.status=='NEEDS_HUMAN_REVIEW'
    p=result.recipe.model_copy(update={'status':'approved'})
    assert assess(p,(r,)).outcome=='require_human_review'
    no,outputs=execute_approved(p,(r,),iter(raw),None)
    assert no.status=='NEEDS_HUMAN_REVIEW' and not outputs
    done,outputs=execute_approved(p,(r,),iter(raw),approve(p))
    assert done.status=='EXECUTED' and done.output_count==len(raw)
    assert outputs[0].value==raw[0].value and outputs[0].provenance.source_records[0]==raw[0]
    assert outputs[0].provenance.execution_identity==execution_identity()
    assert done.evidence_kind=='DERIVED_DETERMINISTICALLY'
    assert 'MODEL_JUDGMENT' in p.proposals[0].configuration


@pytest.mark.parametrize('payload',[
 'print(2 + 2)', 'system("touch /tmp/untrusted")', 'SELECT * FROM source;',
 'x <- mean(c(1, 2))', '{', '```json\n{}\n```',
 json.dumps({'python':'__import__("os").system("touch /tmp/untrusted")'}),
])
def test_arbitrary_languages_and_malformed_json_rejected(bundle,payload):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,))
    assert process_output(payload,cap,(r,),(m,)).status=='INVALID_MODEL_OUTPUT'


@pytest.mark.parametrize('field,value',[
 ('python','lambda x: x*2'),('R','x <- 2'),('sql','DROP TABLE x'),('shell','touch /tmp/x'),
 ('scale',.5),('conversion_factor',100),('statistic','median'),('source_asset','invented'),
 ('approved',True),('expression','x + 273.15'),('template','{{run()}}'),
])
def test_extra_executable_fields_and_numeric_constants_rejected(bundle,field,value):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,));payload=decision_for(cap).model_dump(mode='json')
    payload['steps'][0][field]=value
    assert process_output(json.dumps(payload),cap,(r,),(m,)).status=='INVALID_MODEL_OUTPUT'


def test_invented_operation_and_invalid_parameters_fail_closed(bundle):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,));d=decision_for(cap);data=d.model_dump(mode='json')
    data['steps'][0]['operation_id']='spectral.magic_correction'
    assert process_output(json.dumps(data),cap,(r,),(m,)).status=='UNSUPPORTED_OPERATION'
    with pytest.raises(ValidationError):decision_schema(cap).model_validate(data)
    o=cap.options[0]
    invalid=d.model_copy(update={'steps':(ParameterizeDecision(operation_id=o.operation_id,option_id=o.option_id,target_unit='K'),)})
    assert process_output(invalid.model_dump_json(),cap,(r,),(m,)).status=='INVALID_PARAMETERS'
    invalid=d.model_copy(update={'capability_digest':'f'*64})
    assert process_output(invalid.model_dump_json(),cap,(r,),(m,)).status=='PRECONDITION_FAILED'


@pytest.mark.parametrize('state',['NEEDS_EVIDENCE','NEEDS_HUMAN_REVIEW'])
def test_abstention_is_explicit_not_failure(bundle,state):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,));d=decision_for(cap).model_copy(update={'status':state,'steps':()})
    assert process_output(d.model_dump_json(),cap,(r,),(m,)).status==state


def test_mock_model_and_transport_failure_never_fallback(bundle):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,));d=decision_for(cap)
    assert request_model_decision(FixtureDecisionModel(d.model_dump_json()),cap,(r,),(m,)).status=='NEEDS_HUMAN_REVIEW'
    class Unavailable:
        def generate(self,*a,**k):raise TimeoutError('offline')
    assert request_model_decision(Unavailable(),cap,(r,),(m,)).status=='INVALID_MODEL_OUTPUT'


def test_metadata_references_resolve_without_model_arithmetic(bundle):
    r,m,_,_=bundle
    r=r.model_copy(update={'variables':(r.variables[0].model_copy(update={'unit':'DN'}),),
        'metadata':r.metadata.model_copy(update={'calibration_scale':.0001,'calibration_offset':-.1})})
    m=m.model_copy(update={'target':m.target.model_copy(update={'unit':'1'}),'relationship':'convertible_to'})
    cap=build_capabilities((r,),(m,));o=cap.options[0]
    assert 'scale' not in cap.prompt()['options'][0] and o.parameter_sources['scale']=='source_metadata.calibration_scale'
    d=decision_for(cap).model_copy(update={'steps':(ParameterizeDecision(operation_id=o.operation_id,option_id=o.option_id,
        scale_source='source_metadata.calibration_scale',offset_source='source_metadata.calibration_offset',target_unit='1'),)})
    recipe=compile_decision(d,cap,(r,),(m,))
    assert recipe.operations[0].scale==.0001 and recipe.operations[0].offset==-.1
    changed=r.model_copy(update={'metadata':r.metadata.model_copy(update={'calibration_offset':0})})
    assert process_output(d.model_dump_json(),cap,(changed,),(m,)).status=='PRECONDITION_FAILED'


def test_semantic_ambiguity_and_invented_ontology_ids():
    proposal=SemanticMappingProposal(source_evidence_id='source.definition',candidate_ids=('a','b'),relationship='unknown',
        evidence=('source.definition',),confidence=.3,status='NEEDS_HUMAN_REVIEW')
    assert validate_mapping_proposal(proposal,evidence_ids=('source.definition',),candidate_ids=('a','b')).status=='NEEDS_HUMAN_REVIEW'
    with pytest.raises(ValueError,match='unknown ontology'):
        validate_mapping_proposal(proposal,evidence_ids=('source.definition',),candidate_ids=('a',))
    with pytest.raises(ValidationError):SemanticMappingProposal.model_validate({**proposal.model_dump(),'status':'APPROVED'})


def test_authorization_before_read_and_stale_implementation(bundle):
    r,m,_,_=bundle;cap=build_capabilities((r,),(m,));p=compile_decision(decision_for(cap),cap,(r,),(m,))
    def forbidden():
        raise AssertionError('must not read before review')
        yield
    result,_=execute_approved(p,(r,),forbidden(),None)
    assert result.status=='NEEDS_HUMAN_REVIEW'
    p=p.model_copy(update={'status':'approved','execution_identity':{**execution_identity(),'registry_digest':'stale'}})
    result,_=execute_approved(p,(r,),forbidden(),approve(p))
    assert result.status=='PRECONDITION_FAILED'


@pytest.mark.parametrize('legacy,parameters,expected',[
 ('validate',{'minimum':0,'maximum':3},2),('convert_units',{'from_unit':'m','to_unit':'cm'},200),
 ('calibrate',{'from_unit':'DN','to_unit':'1','scale':.01,'offset':-.1},-.08),
 ('map_variable',{'target_variable':'canonical'},2),('missing',{'sentinel':2},None),
 ('normalize_coordinates',{},2),('filter',{'minimum':1,'maximum':3},2),
 ('temporal_mean',{'target_support':'daily'},2),
 ('join',{'other_asset':'other'},2),('spatial_match',{'other_asset':'other','target_support':'site','tolerance':0},2),
])
def test_every_registered_dispatch_input_output_edge_and_lineage(bundle,legacy,parameters,expected):
    r,m,_,raw=bundle;first=raw[0]
    # These are generated, in-memory rows matching the independently tested executor contract.
    first=first.model_copy(update={'end':first.start+timedelta(days=1)})
    row=(first,2,'daily',r.support.spatial,(first,),(),())
    other=r.model_copy(update={'asset_id':'other'})
    peer=first.model_copy(update={'asset_id':'other'})
    op=Operation(operation=legacy,source_variable=m.source_variable,**parameters)
    result=REGISTRY.execute_rows(op,[row],(first,peer),{r.asset_id:r,'other':other})
    assert result[0][1]==pytest.approx(expected) if expected is not None else result[0][1] is None
    assert result[0][4]==(first,)  # Original observations and values survive every operation.
    if legacy in ('join','spatial_match'):assert result[0][5]==(other,) and result[0][6]==(peer,)
    bad=op.model_copy(update={'scale':123}) if legacy!='calibrate' else op.model_copy(update={'to_unit':'kg'})
    with pytest.raises(ValueError):REGISTRY.execute_rows(bad,[row],(first,),{r.asset_id:r})


def test_registered_qa_checks_and_model_cannot_change_the_library(bundle):
    from dataset_prototype.operations import execute_check
    from dataset_prototype.model_agents import Critique
    r,_,p,_=bundle
    assert execute_check('schema.recipe',p,(r,))['status']=='PASS'
    assert execute_check('recipe.scientific_preconditions',p,(r,))['qa']['outcome']=='approve'
    with pytest.raises(ValueError):execute_check('statistic.magic',p,(r,))
    with pytest.raises(ValidationError):Critique(outcome='approve',reasons=('test',),recommended_checks=('calculate_something',))


def test_cli_offline_end_to_end_demo_and_manifest(tmp_path,capsys):
    from dataset_prototype.cli import main
    main(['operation-capabilities','--output',str(tmp_path/'capabilities.json')])
    assert len(json.loads((tmp_path/'capabilities.json').read_text())['operations'])==17
    main(['operation-demo','--output',str(tmp_path/'demo')])
    report=json.loads((tmp_path/'demo/result.json').read_text())
    assert report['status']=='EXECUTED' and report['result']=={'value':200,'unit':'cm'}
    assert report['unsupported_status']=='UNSUPPORTED_OPERATION' and report['ambiguous_status']=='NEEDS_HUMAN_REVIEW'
    assert report['model_provenance']['model']=='fixture-decision-model'
    assert report['live_model_called'] is False and report['source_data_read'] is False


def test_runtime_package_has_no_code_evaluation_or_shell_dispatch():
    import ast
    from pathlib import Path
    root=Path(__file__).parents[1]/'src/dataset_prototype'
    for path in root.glob('*.py'):
        tree=ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                assert not (isinstance(node.func,ast.Name) and node.func.id in {'eval','exec','compile'}),path
                assert not any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords),path
