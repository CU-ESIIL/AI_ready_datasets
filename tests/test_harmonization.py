from datetime import timedelta, datetime, timezone
import pytest
from pydantic import ValidationError
from dataset_prototype.agents import SemanticAgent, HarmonizationAgent
from dataset_prototype.contracts import Operation, HumanDecision, digest, HarmonizationRecipe
from dataset_prototype.harmonization import run, assess


def execute(bundle,recipe=None,resources=None,records=None,human=None,parents=()):
    r,m,p,raw=bundle
    return tuple(run(resources or (r,),recipe or p,raw if records is None else records,human,parents))


def approve_human(recipe):
    return HumanDecision(recipe_digest=digest(recipe),status='approved',reviewer='fixture expert',rationale='synthetic test only',timestamp=datetime.now(timezone.utc),fixture=True)


def test_exact_mapping_and_originals(bundle):
    r,m,p,raw=bundle
    assert m.relationship=='equivalent_to'
    result=execute(bundle)
    assert result==execute(bundle)
    assert result[0].value==raw[0].value
    assert result[0].provenance.source_records==(raw[0],)
    assert result[0].provenance.source.rights==r.rights
    assert result[0].ontology_id==m.target.ontology_id


def test_similar_names_do_not_establish_equivalence(bundle):
    r,m,p,raw=bundle
    target=m.target.model_copy(update={'definition':'different scientific quantity'})
    proposed=SemanticAgent().propose(r,m.source_variable,target)
    assert proposed.relationship=='unknown' and proposed.confidence==0
    recipe=p.model_copy(update={'mappings':(proposed,)})
    assert assess(recipe,(r,)).outcome=='require_human_review'
    with pytest.raises(ValueError,match='human review'): execute(bundle,recipe)
    with pytest.raises(ValueError,match='abstention'): execute(bundle,recipe,human=approve_human(recipe))


@pytest.mark.parametrize('unit,target,value', [('cm','m',.02),('degC','K',275.15),('K','degC',-271.15),('m','cm',200.)])
def test_unit_conversion(bundle,unit,target,value):
    r,m,p,raw=bundle
    v=r.variables[0].model_copy(update={'unit':unit})
    r=r.model_copy(update={'variables':(v,)})
    m=SemanticAgent().propose(r,v.name,v.model_copy(update={'unit':target}))
    p=p.model_copy(update={'mappings':(m,),'operations':(Operation(operation='convert_units',source_variable=v.name,from_unit=unit,to_unit=target),)})
    assert execute((r,m,p,raw))[0].value==pytest.approx(value)
    assert raw[0].value==2


def test_incompatible_units_and_unknown_operation():
    with pytest.raises(ValidationError): Operation(operation='convert_units',source_variable='x',from_unit='kg',to_unit='K')
    with pytest.raises(ValidationError): Operation(operation='exec',source_variable='x')


def test_conversion_mismatch_rejected(bundle):
    r,m,p,raw=bundle
    p=p.model_copy(update={'operations':(Operation(operation='convert_units',source_variable=m.source_variable,from_unit='degC',to_unit='K'),)})
    assert assess(p,(r,)).outcome=='reject'
    with pytest.raises(ValueError,match='QA rejected'): execute(bundle,p)


def test_variable_mapping(bundle):
    r,m,p,raw=bundle
    m=m.model_copy(update={'target':m.target.model_copy(update={'name':'height'})})
    p=p.model_copy(update={'mappings':(m,),'operations':(Operation(operation='map_variable',source_variable=m.source_variable,target_variable='height'),)})
    assert execute(bundle,p)[0].variable=='height'


def test_missing_filter_validation(bundle):
    r,m,p,raw=bundle
    p=p.model_copy(update={'scope':'track','track':'test','core_recipe':bundle[2].recipe_id,'operations':(Operation(operation='missing',source_variable=m.source_variable,sentinel=2),Operation(operation='filter',source_variable=m.source_variable,minimum=3,maximum=5))})
    parents=execute(bundle)
    result=execute(bundle,p,parents=parents)
    assert [x.value for x in result]==[4]
    invalid=bundle[2].model_copy(update={'operations':(Operation(operation='validate',source_variable=m.source_variable,maximum=1),)})
    with pytest.raises(ValueError,match='validation'): execute(bundle,invalid)
    missing=bundle[2].model_copy(update={'operations':(Operation(operation='missing',source_variable=m.source_variable,sentinel=2),)})
    assert execute(bundle,missing)[0].value is None


@pytest.mark.parametrize('change',[{'confidence':.2},{'novel':True},{'disagreement':True},{'relationship':'requires_human_review'}])
def test_review_triggers(bundle,change):
    r,m,p,raw=bundle
    p=p.model_copy(update={'mappings':(m.model_copy(update=change),)})
    assert assess(p,(r,)).outcome=='require_human_review'
    with pytest.raises(ValueError,match='human review'): execute(bundle,p)


def test_wrong_relationship_and_rejection(bundle):
    r,m,p,raw=bundle
    p=p.model_copy(update={'mappings':(m.model_copy(update={'relationship':'not_comparable'}),)})
    assert assess(p,(r,)).outcome=='reject'
    with pytest.raises(ValueError): execute(bundle,p)


@pytest.mark.parametrize('right,value,outcome',[('redistribution',None,'require_human_review'),('derivative_use',False,'reject')])
def test_rights_review(bundle,right,value,outcome):
    r,m,p,raw=bundle
    r=r.model_copy(update={'rights':r.rights.model_copy(update={right:value})})
    assert assess(p,(r,)).outcome==outcome
    with pytest.raises(ValueError): execute((r,m,p,raw))


def test_status_and_bound_human_decision(bundle):
    r,m,p,raw=bundle
    with pytest.raises(ValueError,match='not approved'): execute(bundle,p.model_copy(update={'status':'proposed'}))
    with pytest.raises(ValueError,match='exact recipe'): execute(bundle,human=approve_human(p.model_copy(update={'version':'2'})))
    assert execute(bundle,human=approve_human(p))


def test_core_track_separation(bundle):
    r,m,p,raw=bundle
    bad=p.model_dump(); bad['operations']=[Operation(operation='temporal_mean',source_variable=m.source_variable,target_support='daily').model_dump()]
    with pytest.raises(ValidationError,match='track scope'): HarmonizationRecipe.model_validate(bad)
    track=p.model_copy(update={'scope':'track','track':'water','core_recipe':p.recipe_id})
    with pytest.raises(ValueError,match='core observations'): execute(bundle,track)
    assert execute(bundle,track,parents=execute(bundle))[0].track=='water'


def test_daily_aggregation_and_missing_coverage(bundle):
    r,m,p,raw=bundle
    parents=execute(bundle)
    p=p.model_copy(update={'scope':'track','track':'test','core_recipe':p.recipe_id,'operations':(Operation(operation='temporal_mean',source_variable=m.source_variable,target_support='daily'),)})
    first=raw[0]; middle=first.start+timedelta(hours=12)
    rows=(first.model_copy(update={'record_id':'a','end':middle}),first.model_copy(update={'record_id':'b','start':middle,'value':4}))
    # Parents must refer to source records actually used.
    core=bundle[2]
    parents=execute(bundle,core,records=rows)
    with pytest.raises(ValueError,match='human review'): execute(bundle,p,records=rows,parents=parents)
    result=execute(bundle,p,records=rows,human=approve_human(p),parents=parents)
    assert result[0].value==3 and result[0].temporal_support=='daily'
    assert len(result[0].provenance.source_records)==2
    with pytest.raises(ValueError,match='coverage'): execute(bundle,p,records=rows[:1],human=approve_human(p),parents=parents[:1])
    with pytest.raises(ValueError,match='duplicate'): execute(bundle,p,records=rows,human=approve_human(p),parents=(parents[0],parents[0]))


def test_spatial_and_join_checks(bundle,client):
    r,m,p,raw=bundle
    other=client.resources[1]; other_rows=client.fetch(other.asset_id)
    p=p.model_copy(update={'scope':'track','track':'test','core_recipe':p.recipe_id,'operations':(Operation(operation='join',source_variable=m.source_variable,other_asset=other.asset_id),)})
    parents=execute(bundle)
    resources=(r,other)
    result=execute(bundle,p,resources=resources,records=raw+other_rows,human=approve_human(p),parents=parents)
    assert result[0].provenance.related_records[0].asset_id==other.asset_id
    with pytest.raises(ValueError,match='ambiguous'): execute(bundle,p,resources=resources,records=raw+other_rows+(other_rows[0].model_copy(update={'record_id':'ambiguous'}),),human=approve_human(p),parents=parents)
    bad=other.model_copy(update={'support':other.support.model_copy(update={'spatial':'pixel'})})
    with pytest.raises(ValueError,match='equal observational support'): execute(bundle,p,resources=(r,bad),records=raw+other_rows,human=approve_human(p),parents=parents)
    match=p.model_copy(update={'operations':(Operation(operation='spatial_match',source_variable=m.source_variable,other_asset=other.asset_id,tolerance=.001,target_support='site'),)})
    assert execute(bundle,match,resources=resources,records=raw+other_rows,human=approve_human(match),parents=parents)[0].spatial_support=='site'


def test_coordinates_and_invalid_records(bundle):
    r,m,p,raw=bundle
    p=p.model_copy(update={'operations':(Operation(operation='normalize_coordinates',source_variable=m.source_variable),)})
    assert execute(bundle,p)[0].crs=='EPSG:4326'
    with pytest.raises(ValueError,match='outside source'): execute(bundle,p,records=(raw[0].model_copy(update={'longitude':0}),))


def test_recipe_schema(bundle):
    schema=HarmonizationRecipe.model_json_schema()
    assert schema['additionalProperties'] is False
    data=bundle[2].model_dump(); data['arbitrary_code']='print(1)'
    with pytest.raises(ValidationError): HarmonizationRecipe.model_validate(data)


def test_track_uses_canonical_value_after_core_conversion(bundle):
    r,m,p,raw=bundle
    target=m.target.model_copy(update={'unit':'cm'})
    m=m.model_copy(update={'target':target,'relationship':'convertible_to'})
    core=p.model_copy(update={'mappings':(m,),'operations':(Operation(operation='convert_units',source_variable=m.source_variable,from_unit='m',to_unit='cm'),)})
    canonical=execute(bundle,core)
    track=core.model_copy(update={'scope':'track','track':'food','core_recipe':core.recipe_id,'operations':(Operation(operation='validate',source_variable=m.source_variable),)})
    products=execute(bundle,track,parents=canonical)
    assert products[0].value==200 and products[0].unit=='cm'
    assert canonical[0].value==200 and raw[0].value==2
    assert products[0].provenance.parent_observations==(canonical[0].observation_id,)


def test_observation_schema_rejects_false_lineage(bundle):
    from dataset_prototype.contracts import HarmonizedObservation
    observation=execute(bundle)[0]
    for field,value in [('unit','kg'),('track','other'),('source_version','fake')]:
        payload=observation.model_dump(mode='json'); payload[field]=value
        with pytest.raises(ValidationError): HarmonizedObservation.model_validate(payload)


def test_ontology_and_methods_survive(bundle):
    r,m,p,raw=bundle
    variable=r.variables[0].model_copy(update={'ontology_id':'fixture:height'})
    r=r.model_copy(update={'variables':(variable,)})
    mapping=SemanticAgent().propose(r,variable.name,variable)
    p=p.model_copy(update={'mappings':(mapping,)})
    observation=execute((r,mapping,p,raw))[0]
    assert observation.ontology_id=='fixture:height'
    assert observation.measurement_method==variable.measurement_method
    assert observation.provenance.source.variables[0].ontology_id=='fixture:height'


def test_low_confidence_can_be_reviewed_but_rejection_blocks(bundle):
    r,m,p,raw=bundle
    p=p.model_copy(update={'mappings':(m.model_copy(update={'confidence':.5}),)})
    human=approve_human(p)
    assert execute(bundle,p,human=human)[0].provenance.human==human
    with pytest.raises(ValueError,match='exact recipe'):
        execute(bundle,p,human=human.model_copy(update={'status':'rejected'}))


def test_recipe_without_source_or_operation_is_rejected(bundle):
    r,m,p,raw=bundle
    assert assess(p,()).outcome=='reject'
    broken=p.model_copy(update={'operations':(Operation(operation='validate',source_variable='absent'),)})
    assert assess(broken,(r,)).outcome=='reject'
