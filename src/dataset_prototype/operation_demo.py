"""Explicit synthetic end-to-end trust-boundary demonstration; no live inference/access."""
from datetime import datetime, timezone
import json
from pathlib import Path
from .adapters import MockMESAClient
from .agents import SemanticAgent
from .contracts import RawObservation, HumanDecision, digest
from .decision_ir import (build_capabilities, RecipeDecision, SelectDecision,
    FixtureDecisionModel, request_model_decision, execute_approved, process_output,
    SemanticMappingProposal)
from .operations import REGISTRY


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    root=Path(__file__).resolve().parents[2]
    source=MockMESAClient(root/'data/fixtures').resources[0]
    variable=source.variables[0]
    target=variable.model_copy(update={'unit':'cm'})
    mapping=SemanticAgent().propose(source,variable.name,target)
    cap=build_capabilities((source,),(mapping,))
    model_json=RecipeDecision(capability_digest=cap.identity,status='PROPOSED',
        steps=tuple(SelectDecision(operation_id=o.operation_id,option_id=o.option_id) for o in cap.options),
        rationale='Select the offered metres-to-centimetres operation for the fixed fixture target.').model_dump_json()
    result=request_model_decision(FixtureDecisionModel(model_json),cap,(source,),(mapping,))
    if result.recipe is None:raise ValueError(result.status)
    approved=result.recipe.model_copy(update={'status':'approved'})
    human=HumanDecision(recipe_digest=digest(approved),status='approved',reviewer='synthetic-demo-reviewer',
        rationale='Generated governance illustration only; no real scientific approval.',
        timestamp=datetime(2026,10,21,tzinfo=timezone.utc),fixture=True)
    def generated_records():
        yield RawObservation(record_id='generated-height',asset_id=source.asset_id,variable=variable.name,value=2,
            longitude=source.support.bbox[0],latitude=source.support.bbox[1],start=source.support.start,end=source.support.end)
    executed,observations=execute_approved(approved,(source,),generated_records(),human)
    if executed.status!='EXECUTED':raise ValueError(executed.status)
    bad=json.loads(model_json);bad['steps'][0]['operation_id']='spectral.magic_correction'
    rejected=process_output(json.dumps(bad),cap,(source,),(mapping,))
    ambiguity=SemanticMappingProposal(source_evidence_id='fixture:definition',candidate_ids=('urn:fixture:a','urn:fixture:b'),
        relationship='unknown',evidence=('fixture:definition',),confidence=.2,status='NEEDS_HUMAN_REVIEW')
    artifacts={'source-metadata.json':source.model_dump(mode='json'),'capabilities.json':cap.model_dump(mode='json'),
        'capability-manifest.json':REGISTRY.manifest(),'model-output.json':json.loads(model_json),
        'proposed-recipe.json':result.recipe.model_dump(mode='json'),'approved-fixture-recipe.json':approved.model_dump(mode='json'),
        'fixture-human-decision.json':human.model_dump(mode='json'),
        'unsupported-operation.json':rejected.model_dump(mode='json'),'ambiguous-mapping.json':ambiguity.model_dump(mode='json')}
    report={'fixture':True,'live_model_called':False,'source_data_read':False,'status':executed.status,
        'result':{'value':observations[0].value,'unit':observations[0].unit},
        'model_proposal_digest':digest(json.loads(model_json)),'model_provenance':result.model_provenance.model_dump(mode='json'),'deterministic_validation':result.status,
        'execution_identity':executed.execution_identity,'human_decision_digest':digest(human),
        'observation_evidence_digest':digest(observations[0]),'provenance_digest':digest(observations[0].provenance),
        'unsupported_status':rejected.status,'ambiguous_status':ambiguity.status,
        'note':'Generated illustration; no raw/harmonized datasets are persisted.'}
    artifacts['result.json']=report
    for name,data in artifacts.items():(output/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    return report
