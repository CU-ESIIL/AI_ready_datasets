"""Closed CubeDynamics selections reuse the existing decision IR and scientific recipe."""
from typing import Literal
from pydantic import Field, create_model
from .contracts import BackendOperation, digest
from .decision_ir import RecipeDecision, SelectDecision
from .cube_contracts import CubeCapabilitySpace,CubeOption
from .cube_specs import SPECS
from .cubedynamics_backend import context_digest, CubeError
from .operations import REGISTRY, execution_identity


def capabilities(recipe,sources,configuration):
    choices=[]
    for identifier,(_,_,parameters,*_) in SPECS.items():
        if identifier.endswith('.select') and configuration.variable is None:continue
        if identifier.endswith('.subset') and configuration.window is None:continue
        if identifier.endswith('.month_filter') and not configuration.months:continue
        if identifier.endswith('.quality_mask') and 'quality' not in configuration.inputs:continue
        if identifier.endswith('.temporal_mean') and configuration.target_temporal_support is None:continue
        if identifier.endswith(('.align_time','.align_nearest')) and 'reference' not in configuration.inputs:continue
        step=BackendOperation(operation_id=identifier,parameters={key:value['const'] for key,value in parameters.items()})
        choices.append(CubeOption(option_id='option:'+digest(step),step=step))
    return CubeCapabilitySpace(context_digest=context_digest(configuration,sources),base_recipe_digest=digest(recipe),options=tuple(choices))


def selection_schema(space):
    if not space.options:raise CubeError('NEEDS_EVIDENCE','no applicable backend choices')
    selection=create_model('CubeSelection',__base__=SelectDecision,
        operation_id=(Literal[tuple(o.step.operation_id for o in space.options)],...),
        option_id=(Literal[tuple(o.option_id for o in space.options)],...))
    return create_model('CubeRecipeDecision',__base__=RecipeDecision,
        capability_digest=(Literal[space.identity],space.identity),
        steps=(tuple[selection,...],Field(default=(),max_length=16)))


def compile_decision(decision,space,recipe,sources,configuration):
    decision=RecipeDecision.model_validate(decision.model_dump(mode='json'))
    if decision.status!='PROPOSED':raise CubeError(decision.status,decision.rationale)
    if space!=capabilities(recipe,sources,configuration) or decision.capability_digest!=space.identity:
        raise CubeError('PRECONDITION_FAILED','stale source/configuration/base recipe capability')
    if not decision.steps or len(decision.steps)>16:raise CubeError('INVALID_PARAMETERS','bounded nonempty backend plan required')
    by_id={o.option_id:o.step for o in space.options};steps=[]
    for choice in decision.steps:
        definition=REGISTRY.get(choice.operation_id)
        if definition.backend!='cubedynamics':raise CubeError('UNSUPPORTED_OPERATION','not a CubeDynamics operation')
        if choice.authority!='SELECT' or choice.option_id not in by_id or by_id[choice.option_id].operation_id!=choice.operation_id:
            raise CubeError('INVALID_PARAMETERS','only offered reference-bound backend choices permitted')
        steps.append(by_id[choice.option_id])
    if len(set(s.operation_id for s in steps))!=len(steps):raise CubeError('INVALID_PARAMETERS','duplicate backend operations')
    # Preserve prior scientific vetoes; never convert an old review into a fresh approval.
    return recipe.model_copy(update={'backend_operations':tuple(steps),'backend_context_digest':space.context_digest,
        'status':'needs_review','execution_identity':execution_identity()})
