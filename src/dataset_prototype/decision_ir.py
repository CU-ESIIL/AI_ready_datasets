"""Declarative model decisions over caller-frozen capabilities; no source-data access."""
from datetime import datetime, timezone
from typing import Annotated, Literal
from pydantic import Field, create_model
from .contracts import (Contract, Operation, SemanticMapping, HarmonizationRecipe, Proposal,
                        HumanDecision, digest)
from .operations import REGISTRY, execution_identity

class SelectDecision(Contract):
    authority: Literal['SELECT'] = 'SELECT'
    operation_id: str = Field(min_length=1, max_length=100)
    operation_version: Literal['1'] = '1'
    option_id: str = Field(min_length=1, max_length=100)

class ParameterizeDecision(Contract):
    authority: Literal['PARAMETERIZE'] = 'PARAMETERIZE'
    operation_id: str = Field(min_length=1, max_length=100)
    operation_version: Literal['1'] = '1'
    option_id: str = Field(min_length=1, max_length=100)
    # Values are references or enum selections, never model-authored numbers/formulas.
    target_unit: Literal['degC','K','cm','m','1'] | None = None
    scale_source: Literal['source_metadata.calibration_scale'] | None = None
    offset_source: Literal['source_metadata.calibration_offset'] | None = None

class SemanticMappingProposal(Contract):
    authority: Literal['PROPOSE'] = 'PROPOSE'
    source_evidence_id: str
    candidate_ids: tuple[str,...] = ()
    relationship: Literal['equivalent','convertible','broader','narrower','derived','related','incomparable','unknown']
    evidence: tuple[str,...] = Field(min_length=1)
    confidence: float = Field(ge=0,le=1)
    # This is always a proposal; scientific validation/human review cannot be self-issued.
    status: Literal['NEEDS_EVIDENCE','NEEDS_HUMAN_REVIEW']

Decision = Annotated[SelectDecision | ParameterizeDecision, Field(discriminator='authority')]

class RecipeDecision(Contract):
    ir_version: Literal['1'] = '1'
    capability_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    status: Literal['PROPOSED','NEEDS_EVIDENCE','NEEDS_HUMAN_REVIEW']
    steps: tuple[Decision,...] = Field(default=(),max_length=64)
    rationale: str = Field(min_length=1,max_length=2000)

class ModelDecisionProvenance(Contract):
    model: str
    model_version: str
    prompt_version: str = 'decision-backbone-v2'
    timestamp: datetime
    input_evidence_references: tuple[str,...]
    structured_output_digest: str
    confidence: float | None = Field(default=None,ge=0,le=1)
    evidence_kind: Literal['MODEL_JUDGMENT'] = 'MODEL_JUDGMENT'


class ExecutionResult(Contract):
    status: Literal['PROPOSED','VALIDATED','NEEDS_EVIDENCE','NEEDS_HUMAN_REVIEW','APPROVED',
        'REJECTED','UNSUPPORTED_OPERATION','INVALID_PARAMETERS','PRECONDITION_FAILED',
        'READY_TO_EXECUTE','EXECUTED','EXECUTION_FAILED','INVALID_MODEL_OUTPUT']
    reasons: tuple[str,...] = ()
    recipe: HarmonizationRecipe | None = None
    output_count: int = 0
    evidence_kind: Literal['DERIVED_DETERMINISTICALLY'] = 'DERIVED_DETERMINISTICALLY'
    execution_identity: dict
    proposal_digest: str | None = None
    model_provenance: ModelDecisionProvenance | None = None
    human_decision_digest: str | None = None

class CapabilityOption(Contract):
    option_id: str
    operation_id: str
    operation_version: Literal['1'] = '1'
    operation: Operation
    parameter_sources: dict[str,str]

class CapabilitySpace(Contract):
    schema_version: Literal['1'] = '1'
    source_digest: str
    mapping_digest: str
    registry_digest: str
    options: tuple[CapabilityOption,...] = Field(max_length=64)

    @property
    def identity(self): return digest(self)

    def prompt(self):
        # Resolved numerical coefficients stay outside model decision fields.
        return {'capability_digest':self.identity,'source_digest':self.source_digest,
            'registry_digest':self.registry_digest,
            'options':[{'option_id':o.option_id,'operation_id':o.operation_id,
                'operation_version':o.operation_version,'source_asset':o.operation.source_asset,
                'source_variable':o.operation.source_variable,'target_variable':o.operation.target_variable,
                'from_unit':o.operation.from_unit,'target_unit':o.operation.to_unit,
                'parameter_sources':o.parameter_sources} for o in self.options]}


def build_capabilities(resources, mappings):
    """Conservative core options only; scientific targets are fixed by deterministic caller.

    General track operations remain registered, but are never autonomously offered.
    Missing coefficients produce no calibration capability, never guessed values.
    """
    resources=tuple(resources); mappings=tuple(mappings)
    by_id={r.asset_id:r for r in resources};options=[]
    def add(identifier, operation, sources):
        REGISTRY.validate(operation)
        fields={'operation_id':identifier,'operation_version':'1','operation':operation.model_dump(mode='json'),
                'parameter_sources':sources}
        options.append(CapabilityOption(option_id='option:'+digest(fields),**fields))
    for m in mappings:
        r=by_id[m.source_asset]
        v=next(v for v in r.variables if v.name==m.source_variable)
        base={'source_asset':r.asset_id,'source_variable':v.name}
        if v.unit==m.target.unit:
            add('quality.validate_bounds',Operation(operation='validate',**base),{})
        elif (v.unit,m.target.unit) in {('degC','K'),('K','degC'),('cm','m'),('m','cm')}:
            add('unit.convert',Operation(operation='convert_units',from_unit=v.unit,to_unit=m.target.unit,**base),
                {'from_unit':'source.variables.unit','to_unit':'fixed_mapping.target.unit','constants':'units-v1'})
        elif v.unit=='DN' and m.target.unit=='1' and r.metadata.calibration_scale is not None and r.metadata.calibration_offset is not None:
            add('calibration.scale_offset',Operation(operation='calibrate',from_unit='DN',to_unit='1',
                scale=r.metadata.calibration_scale,offset=r.metadata.calibration_offset,**base),
                {'scale':'source_metadata.calibration_scale','offset':'source_metadata.calibration_offset'})
        if v.name!=m.target.name:
            add('semantic.rename',Operation(operation='map_variable',target_variable=m.target.name,**base),
                {'target_variable':'fixed_mapping.target.name'})
    return CapabilitySpace(source_digest=digest([r.model_dump(mode='json') for r in resources]),
        mapping_digest=digest([m.model_dump(mode='json') for m in mappings]),
        registry_digest=execution_identity()['registry_digest'],options=tuple(options))


def decision_schema(capabilities):
    """Closed enum schema for deployed model tasks, plus server-side revalidation."""
    if not capabilities.options: raise ValueError('NEEDS_EVIDENCE: no supported capabilities')
    ids=tuple(dict.fromkeys(o.operation_id for o in capabilities.options))
    options=tuple(o.option_id for o in capabilities.options)
    selected=create_model('BoundedSelection',__base__=SelectDecision,
        operation_id=(Literal[ids],...),option_id=(Literal[options],...))
    parameterized=create_model('BoundedParameters',__base__=ParameterizeDecision,
        operation_id=(Literal[ids],...),option_id=(Literal[options],...))
    step=Annotated[selected | parameterized,Field(discriminator='authority')]
    return create_model('BoundedRecipeDecision',__base__=RecipeDecision,
        capability_digest=(Literal[capabilities.identity],capabilities.identity),
        steps=(tuple[step,...],Field(default=(),max_length=64)))


def resolve_decision(decision, capabilities, resources, mappings):
    """Return only caller-owned operations; reject stale identities or altered parameters."""
    decision=RecipeDecision.model_validate(decision.model_dump(mode='json'))
    current=build_capabilities(resources,mappings)
    if capabilities!=current or decision.capability_digest!=current.identity:
        raise ValueError('PRECONDITION_FAILED: stale source, mapping or operation registry')
    if decision.status!='PROPOSED': raise ValueError(decision.status)
    if not decision.steps:raise ValueError('INVALID_PARAMETERS: empty operation plan')
    by_id={o.option_id:o for o in current.options};resolved=[]
    for step in decision.steps:
        REGISTRY.get(step.operation_id)
        option=by_id.get(step.option_id)
        if option is None or option.operation_id!=step.operation_id:
            raise ValueError('INVALID_PARAMETERS: option is not offered for this operation/source')
        if isinstance(step,ParameterizeDecision):
            if step.target_unit is not None and step.target_unit!=option.operation.to_unit:
                raise ValueError('INVALID_PARAMETERS: target unit contradicts frozen target')
            for field in ('scale','offset'):
                supplied=getattr(step,field+'_source')
                if supplied is not None and option.parameter_sources.get(field)!=supplied:
                    raise ValueError('INVALID_PARAMETERS: coefficient reference is not applicable')
        resolved.append(option.operation)
    if len({o.model_dump_json() for o in resolved})!=len(resolved):
        raise ValueError('INVALID_PARAMETERS: duplicate operations')
    return tuple(resolved)


def compile_decision(decision, capabilities, resources, mappings, *, model='unattributed-model', model_version='not-supplied'):
    operations=resolve_decision(decision,capabilities,resources,mappings)
    return HarmonizationRecipe(recipe_id='ir:'+digest(decision),version='1',scope='core',status='needs_review',
        author='deterministic-ir-compiler-v1',mappings=tuple(mappings),operations=operations,
        execution_identity=execution_identity(),
        proposals=(Proposal(role='harmonization',agent=model,version=model_version,configuration='decision-ir-v1; MODEL_JUDGMENT',
            rationale=decision.rationale,evidence=('model_proposal:'+digest(decision),'capability:'+capabilities.identity)),))


def process_output(text, capabilities, resources, mappings, *, model='unattributed-model', model_version='not-supplied'):
    """Safe typed boundary. No fallback, repair, code generation or source-data reads."""
    identity=execution_identity()
    try: decision=RecipeDecision.model_validate_json(text)
    except ValueError:
        return ExecutionResult(status='INVALID_MODEL_OUTPUT',reasons=('Output does not match decision IR.',),execution_identity=identity)
    if decision.status!='PROPOSED':
        return ExecutionResult(status=decision.status,reasons=(decision.rationale,),execution_identity=identity,proposal_digest=digest(decision))
    try:
        recipe=compile_decision(decision,capabilities,resources,mappings,model=model,model_version=model_version)
        from .harmonization import assess
        qa=assess(recipe,resources)
        status='REJECTED' if qa.outcome=='reject' else 'NEEDS_HUMAN_REVIEW'
        return ExecutionResult(status=status,recipe=recipe,reasons=qa.reasons,execution_identity=identity,proposal_digest=digest(decision))
    except (ValueError,KeyError,StopIteration) as error:
        message=str(error); status=message.split(':',1)[0]
        if status not in {'UNSUPPORTED_OPERATION','INVALID_PARAMETERS','PRECONDITION_FAILED'}:status='PRECONDITION_FAILED'
        return ExecutionResult(status=status,reasons=(message,),execution_identity=identity,proposal_digest=digest(decision))


def execute_approved(recipe, resources, records, human, *, parents=()):
    """No backend accepted or called. All existing scientific gates remain binding."""
    from .harmonization import authorize, run
    identity=execution_identity()
    if not all(r.metadata.fixture for r in resources):
        return ExecutionResult(status='PRECONDITION_FAILED',reasons=('Real sources require approved bounded streaming context.',),execution_identity=identity),()
    try:
        if recipe.status!='approved' or human is None or human.status!='approved' or human.recipe_digest!=digest(recipe):
            return ExecutionResult(status='NEEDS_HUMAN_REVIEW',execution_identity=identity),()
        authorize(recipe,resources,human,tuple(p.provenance for p in parents))
    except ValueError as error:
        return ExecutionResult(status='PRECONDITION_FAILED',reasons=(str(error),),execution_identity=identity),()
    from itertools import islice
    records=iter(records)
    try:
        bounded=tuple(islice(records,1025))
    finally:
        if hasattr(records,'close'):records.close()
    if len(bounded)>1024:
        return ExecutionResult(status='PRECONDITION_FAILED',reasons=('Fixture execution bounded to 1024 records.',),execution_identity=identity),()
    try:
        outputs=tuple(run(resources,recipe,bounded,human,parents))
        return ExecutionResult(status='EXECUTED',output_count=len(outputs),recipe=recipe,execution_identity=identity,
            human_decision_digest=digest(human)),outputs
    except ValueError as error:
        return ExecutionResult(status='EXECUTION_FAILED',reasons=(str(error),),execution_identity=identity),()

class FixtureDecisionModel:
    """Explicit offline model replacement; never a live inference fallback."""
    model='fixture-decision-model'
    _model_digest='fixture-v1'
    traces=()
    def __init__(self, output): self.output=output
    def generate(self, role, instruction, evidence, schema): return schema.model_validate_json(self.output)

class DecisionBindingProposal(Contract):
    binding_id: str
    relationship: str
    evidence: tuple[str,...] = Field(min_length=1)
    confidence: float = Field(ge=0,le=1)
    decision: RecipeDecision

class DecisionRecipeDraft(Contract):
    bindings: tuple[DecisionBindingProposal,...] = Field(min_length=1,max_length=16)
    rationale: str = Field(min_length=1)
    responds_to: tuple[str,...] = Field(min_length=1)


def binding_capabilities(binding):
    # Target identity is supplied by the deterministic plan, not by the model.
    mapping=SemanticMapping(source_asset=binding.source.asset_id,source_variable=binding.source_variable,
        target=binding.target,relationship='unknown',evidence=('fixed caller target; not an approved mapping',),confidence=0)
    return build_capabilities((binding.source,),(mapping,)),mapping


def validate_mapping_proposal(proposal, *, evidence_ids, candidate_ids):
    proposal=SemanticMappingProposal.model_validate(proposal.model_dump(mode='json'))
    if proposal.source_evidence_id not in evidence_ids or not set(proposal.evidence)<=set(evidence_ids):
        raise ValueError('NEEDS_EVIDENCE: unknown semantic evidence reference')
    if not set(proposal.candidate_ids)<=set(candidate_ids):
        raise ValueError('NEEDS_EVIDENCE: unknown ontology candidate')
    return proposal  # Never returns an approved mapping or an executable operation.


def draft_schema(plan):
    from typing import Union
    from .contracts import Relation
    bindings=[]
    for binding in plan.bindings:
        capabilities,_=binding_capabilities(binding)
        bindings.append(create_model('Binding_'+str(len(bindings)),__base__=DecisionBindingProposal,
            binding_id=(Literal[binding.binding_id],...),relationship=(Relation,...),
            decision=(decision_schema(capabilities),...)))
    item=bindings[0] if len(bindings)==1 else Annotated[Union[tuple(bindings)],Field(discriminator='binding_id')]
    return create_model('BoundedDecisionDraft',__base__=DecisionRecipeDraft,
                        bindings=(tuple[item,...],Field(min_length=1,max_length=16)))


def request_model_decision(backend, capabilities, resources, mappings):
    """Transport/schema errors become explicit states; never invoke a fallback model."""
    if not capabilities.options:
        return ExecutionResult(status='NEEDS_EVIDENCE',reasons=('No supported metadata-backed capability.',),execution_identity=execution_identity())
    try:
        decision=backend.generate('harmonization',
            'Select offered capabilities only. No code, arithmetic, formulas or invented parameters. '
            'Return NEEDS_EVIDENCE or NEEDS_HUMAN_REVIEW rather than guess.',
            {'available_operations':capabilities.prompt()},decision_schema(capabilities))
        result=process_output(decision.model_dump_json(),capabilities,resources,mappings,
            model=backend.model,model_version=backend._model_digest or 'not-exposed')
        provenance=ModelDecisionProvenance(model=backend.model,model_version=backend._model_digest or 'not-exposed',
            timestamp=datetime.now(timezone.utc),input_evidence_references=('source_metadata:'+capabilities.source_digest,
                'mapping:'+capabilities.mapping_digest,'capabilities:'+capabilities.identity),structured_output_digest=digest(decision))
        return result.model_copy(update={'model_provenance':provenance})
    except (ValueError,OSError,TimeoutError) as error:
        return ExecutionResult(status='INVALID_MODEL_OUTPUT',reasons=(type(error).__name__,),execution_identity=execution_identity())
