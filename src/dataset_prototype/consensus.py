"""Bounded specialist dialogue over metadata; no source-data reader is accepted.

A draft is frozen before review. Every specialist and adversarial QA must agree
on that same content digest. Revision rounds include previous messages/vetoes;
there is no majority vote, forced consensus, or silent QA override.
"""
import json
from pathlib import Path
from .contracts import HarmonizationRecipe, SemanticMapping, Proposal, AgentReview, digest, recipe_content_digest
from .stream_contracts import (SPECIALISTS, REVIEWERS, StreamPlan, AgentMessage, SpecialistFinding,
                              ReviewVote, RecipeDraft, ConsensusReport)
from .harmonization import assess

SPECIALTY = {
 'semantic':'Scientific quantity definitions, measurement methods, entities and ontology. Distinguish encoded DN from calibrated reflectance. Do not equate names.',
 'units':'Instrument calibration, scale/offset, units, missing/nodata and uncertainty. Require exactly documented coefficients; do not invent or silently apply them.',
 'support':'Spatial footprint, CRS, resolution, temporal intervals, alignment and scale. For this stream, preserve each native pixel/acquisition support; no implicit joins or aggregation.',
 'rights':'Source-specific legal notice, attribution, access/derivative/redistribution rights and provenance. Distinguish a catalog label from its linked legal terms, abstaining on unresolved rights.',
 'qa':'Adversarial cross-specialist review: challenge unsupported assertions, scientific information loss, false equivalence, unsafe streaming operations, encoder mismatches, and unresolved disagreements.'}
STREAM_OPERATIONS={'validate','missing','map_variable','convert_units','calibrate','normalize_coordinates'}


def _license_evidence(source):
    native=json.loads(source.metadata.native_metadata_json or '{}')
    collection=native.get('collection',{})
    item=native.get('item',native)
    return {'item_license':item.get('license'),'collection_license':collection.get('license'),
            'license_links':[link for link in (*item.get('links',[]),*collection.get('links',[])) if link.get('rel')=='license']}


def _metadata(plan):
    # Native metadata is retained in the plan; prompts carry a bounded scientific
    # subset plus content-addressed references. No observation values are present.
    return [{'binding_id':b.binding_id,'source':b.source.model_dump(mode='json',exclude={'metadata':{'native_metadata_json'}}),
             'target':b.target.model_dump(mode='json'),'native_license_evidence':_license_evidence(b.source),'metadata_ref':f'metadata:{b.source.checksum}',
             'sampling':{'longitude':b.longitude,'latitude':b.latitude}} for b in plan.bindings]


def _validate_refs(refs,allowed):
    if not refs or not set(refs)<=set(allowed):raise ValueError('agent cited unknown or missing message/metadata references')


def _dialogue(messages):
    return [{**m.model_dump(mode='json',exclude={'payload_json'}),'payload':json.loads(m.payload_json)} for m in messages]


def _compile(plan,draft,messages,backend,round_number):
    by_id={b.binding_id:b for b in plan.bindings}
    if len(draft.bindings)!=len(by_id) or {b.binding_id for b in draft.bindings}!=set(by_id):
        raise ValueError('recipe builder omitted, duplicated, or invented binding IDs')
    mappings=[];operations=[]
    for proposal in draft.bindings:
        binding=by_id[proposal.binding_id]
        if any(o.source_variable!=binding.source_variable or o.operation not in STREAM_OPERATIONS for o in proposal.operations):
            raise ValueError('recipe operation is not bounded-stream executable or changes source identity')
        mappings.append(SemanticMapping(source_asset=binding.source.asset_id,source_variable=binding.source_variable,target=binding.target,
            relationship=proposal.relationship,evidence=proposal.evidence,confidence=proposal.confidence,novel=True,review_status='needs_review'))
        for operation in proposal.operations:
            if operation.source_asset not in {None,binding.source.asset_id}:
                raise ValueError('model operation changes source asset ownership')
            operations.append(operation.model_copy(update={'source_asset':binding.source.asset_id}))
    unique=tuple({o.model_dump_json():o for o in operations}.values())
    proposals=tuple(Proposal(role=m.sender,agent=f"{getattr(backend,'backend_name','model')}:{backend.model}",version=backend._model_digest,
        configuration=getattr(backend,'configuration','bounded model task'),rationale=draft.rationale if m.kind=='draft' else json.loads(m.payload_json).get('assessment','Specialist dialogue'),
        evidence=(m.message_id,*(x for x in [f'prompt_sha256:{m.prompt_digest}' if m.prompt_digest else None,f'response_sha256:{m.response_digest}' if m.response_digest else None] if x)))
        for m in messages if m.kind in {'analysis','draft'})
    return HarmonizationRecipe(recipe_id='consensus-'+digest(plan)[:16],version=str(round_number),scope='core',status='needs_review',
        mappings=tuple(mappings),operations=unique,proposals=proposals,author='metadata-specialist-consensus')


def negotiate(plan:StreamPlan,backend,output,*,max_rounds=2,analysis_from=None):
    if not 1<=max_rounds<=3:raise ValueError('consensus rounds must be bounded to 1..3')
    plan=StreamPlan.model_validate(plan.model_dump(mode='json'))
    if plan.reader=='sentinel-pixel':
        from .stream_sources import validated_native
        for binding in plan.bindings:validated_native(binding)
    root=Path(output);root.mkdir(parents=True,exist_ok=False)
    messages=[];rounds=[];recipe=None;reused_draft=None
    def save(name,value):
        with (root/name).open('x') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False)
    def publish(role,kind,round_number,result,reply_to=(),content_digest=None):
        trace=backend.traces[-1] if getattr(backend,'traces',()) else None
        fields=dict(round=round_number,sender=role,kind=kind,reply_to=tuple(reply_to),recipe_content_digest=content_digest,
                    payload_json=result.model_dump_json(),prompt_digest=trace.prompt_digest if trace else None,response_digest=trace.response_digest if trace else None)
        message=AgentMessage(message_id='message:'+digest(fields),**fields)
        messages.append(message)
        # Append/flush each exchange so interrupted model calls do not erase history.
        with (root/'dialogue.jsonl').open('a') as f:f.write(message.model_dump_json()+'\n')
        return message
    save('data_access_plan.json',plan.model_dump(mode='json'))
    save('encoder_spec.json',plan.encoder.model_dump(mode='json'))
    metadata=_metadata(plan);evidence_ids=[row['metadata_ref'] for row in metadata]
    base={'question':plan.question,'metadata':metadata,'encoder':plan.encoder.model_dump(mode='json'),
          'constraints':['metadata-only planning; no data values','bounded reads directly into embeddings; no raw/harmonized materialization',
                         'target identities fixed by caller','human approval remains required; model confidence is not approval']}
    base['executor_contract']={
        'executor':'allowlist-v2; bounded-stream-v1',
        'calibration':'value * exact source calibration_scale + exact source calibration_offset',
        'uncertainty':'abs(scale) times supplied scalar uncertainty; unknown stays unknown; calibration-parameter covariance is not modeled',
        'quality_policy':'Sentinel reader requires SCL in {4,5,6} and DN != 0; any rejection fails explicitly; actual mask values cannot exist in metadata-only planning',
        'geometry':'Native NIR/SCL pixels are not resampled. Geographic coordinates/bounds are EPSG:4326; actual native CRS and indices are retained per window in lineage',
        'range_policy':'No metadata-derived physical valid range is supplied. Do not silently clip values or invent bounds; request scientific review if needed',
        'sink':'Vectors plus compact lineage including quality flags and calibrated uncertainty; no raw or harmonized observation objects persisted',
        'integrity':'Verify native metadata hash, normalized calibration/support identity, and hash each extracted window; full remote raster-byte immutability is not guaranteed',
        'review':'All model proposals need an exact-recipe human decision; no source iterator is opened first'}
    try:
        if analysis_from is not None:
            # Explicit retry of a failed draft. Reuse only content-checked metadata
            # analyses; never repair or accept the invalid response.
            prior=Path(analysis_from)
            previous_plan=StreamPlan.model_validate_json((prior/'data_access_plan.json').read_text())
            if digest(previous_plan)!=digest(plan) or not (prior/'failure.json').exists():
                raise ValueError('analysis reuse requires a failed run with this exact plan')
            previous=[AgentMessage.model_validate_json(line) for line in (prior/'dialogue.jsonl').read_text().splitlines()]
            if len(previous) not in {4,5} or tuple(m.sender for m in previous[:4])!=SPECIALISTS or any(m.kind!='analysis' or m.round!=0 for m in previous[:4]) or (len(previous)==5 and (previous[-1].kind!='draft' or previous[-1].sender!='harmonization' or previous[-1].round!=1)):
                raise ValueError('only initial analyses and an optional unreviewed first draft may be reused')
            from .model_agents import AgentTrace
            traces=[AgentTrace.model_validate(t) for t in json.loads((prior/'agent_traces.json').read_text())]
            if not 5<=len(traces)<=32:
                raise ValueError('bounded failed-run traces required for reuse')
            for message in previous:
                matches=[t for t in traces if t.role==message.sender and t.prompt_digest==message.prompt_digest and t.response_digest==message.response_digest]
                if len(matches)!=1:raise ValueError('reused message lacks a unique trace')
                trace=matches[0]
                fields=message.model_dump(mode='json',exclude={'message_id'})
                if trace.model!=backend.model or trace.model_digest!=backend._model_digest:
                    raise ValueError('analysis reuse cannot change the configured model')
                if message.message_id!='message:'+digest(fields) or message.prompt_digest!=trace.prompt_digest or message.response_digest!=trace.response_digest or trace.role!=message.sender or trace.error:
                    raise ValueError('reused analysis trace identity mismatch')
                if trace.prompt_digest!=digest(trace.input_json) or trace.response_digest!=digest(trace.output_json):
                    raise ValueError('reused analysis transcript content changed')
                schema=SpecialistFinding if message.kind=='analysis' else RecipeDraft
                result=schema.model_validate_json(message.payload_json)
                if result!=schema.model_validate_json(trace.output_json):
                    raise ValueError('reused message differs from validated trace')
                if message.kind=='analysis':_validate_refs(result.evidence_refs,evidence_ids)
                else:
                    required={m.message_id for m in previous[:4]}
                    if set(result.responds_to)!=required:raise ValueError('reused draft did not answer all initial analyses')
                    reused_draft=(result,message)
            backend.traces.extend(traces)
            messages.extend(previous)
            with (root/'dialogue.jsonl').open('x') as f:
                for message in previous:f.write(message.model_dump_json()+'\n')
            retry={'previous_run':str(prior),'previous_traces_digest':digest([t.model_dump(mode='json') for t in traces]),
                   'rejected_response_json':traces[-1].output_json,
                   'reason':'Previous run failed schema or message-reference validation. The last response is rejected; request a fresh response for that stage. Reused draft content still requires all five fresh peer reviews.'}
            if len(retry['rejected_response_json'].encode())>8000:raise ValueError('failed draft exceeds bounded retry context')
            save('retry_context.json',retry)
            base['retry_context']={k:retry[k] for k in ('previous_traces_digest','reason')}
        else:
            for specialist in SPECIALISTS:
                finding=backend.generate(specialist,SPECIALTY[specialist]+' Analyze only the supplied metadata for the stated target and streaming encoder. Give concise evidence-grounded constraints and concerns. Do not read data. Cite supplied metadata_ref values.',
                    base,SpecialistFinding)
                _validate_refs(finding.evidence_refs,evidence_ids)
                publish(specialist,'analysis',0,finding)
        votes=[];status='needs_revision'
        for number in range(1,max_rounds+1):
            known=[m.message_id for m in messages]
            if number==1 and reused_draft is not None:
                draft,draft_message=reused_draft
            else:
                draft=backend.generate('harmonization','Build or revise the allow-listed streaming recipe from the specialists\' actual messages. Reply to ALL initial specialist analysis IDs (or ALL previous-round review IDs for a revision), address every previous critique, and preserve the fixed targets/support. For calibration use the exact explicit source metadata scale/offset. Never add joins, aggregations, sensor assumptions or encoder preprocessing to core harmonization. Every operation.source_variable MUST remain the original binding.source_variable (B08_DN), including map_variable; the executor scopes operations by original source identity. Calibration MUST explicitly set from_unit="DN", to_unit="1", scale and offset. Use a calibrate DN→1 operation followed by map_variable when the stated target is physical reflectance; raw-DN preservation needs no calibration. Abstain on unresolved meaning.',
                    {**base,'dialogue':_dialogue(messages),'round':number},RecipeDraft)
                _validate_refs(draft.responds_to,known)
                required={m.message_id for m in messages if (m.kind=='analysis' if number==1 else m.kind=='review' and m.round==number-1)}
                if not required<=set(draft.responds_to):raise ValueError('recipe builder did not answer all specialist findings or prior reviews')
                draft_message=publish('harmonization','draft',number,draft,draft.responds_to)
            recipe=_compile(plan,draft,messages,backend,number)
            content=recipe_content_digest(recipe)
            # A metadata/operation mismatch cannot be voted away by the agents.
            deterministic=assess(recipe,plan.resources)
            context={**base,'recipe':recipe.model_dump(mode='json'),'recipe_content_digest':content,
                     'draft_message_id':draft_message.message_id,'dialogue':_dialogue(messages),
                     'deterministic_qa':deterministic.model_dump(mode='json')}
            votes=[]
            for specialist in REVIEWERS:
                # Each later reviewer can see earlier current-round replies too.
                context['dialogue']=_dialogue(messages)
                context['allowed_peer_message_ids']=[m.message_id for m in messages if m.sender!=specialist and m.kind in {'analysis','review'}]
                vote=backend.generate(specialist,SPECIALTY[specialist]+' Review this exact recipe content and the other specialists\' findings/replies. Your responds_to MUST include the draft_message_id AND at least one ID from allowed_peer_message_ids. Do not cite your own analysis as the peer. Discuss the selected peer finding. Agree only if your concerns are resolved by the actual recipe/metadata. Distinguish native DN from the explicit target after calibration. Native calibration and legal-notice metadata remain in source provenance. Do not invent missing fields or require a learned encoder for the documented reference features. Request revision or abstain on uncertainty; no forced agreement. Agreement is not human approval.',context,ReviewVote)
                _validate_refs(vote.responds_to,[m.message_id for m in messages])
                if draft_message.message_id not in vote.responds_to:raise ValueError('reviewer did not review the current shared draft')
                peers={m.message_id for m in messages if m.sender!=specialist and m.kind in {'analysis','review'}}
                if not set(vote.responds_to)&peers:raise ValueError('reviewer must respond to another specialist, not only the draft')
                _validate_refs(vote.evidence_refs,evidence_ids)
                publish(specialist,'review',number,vote,vote.responds_to,content)
                votes.append((specialist,vote))
            unresolved=tuple(f'{role}: {concern}' for role,v in votes for concern in v.concerns)
            decisions={v.decision for _,v in votes}
            if 'reject' in decisions:status='rejected'
            elif 'abstain' in decisions:status='abstained'
            elif decisions=={'agree'} and not unresolved and deterministic.outcome!='reject':status='consensus'
            else:status='needs_revision'
            if deterministic.outcome=='reject':unresolved+=deterministic.reasons
            rounds.append({'round':number,'content_digest':content,'status':status,'votes':[(r,v.model_dump(mode='json')) for r,v in votes],
                           'deterministic_qa':deterministic.model_dump(mode='json')})
            save(f'round-{number}-recipe.json',recipe.model_dump(mode='json'))
            save(f'round-{number}-votes.json',rounds[-1])
            if status in {'consensus','rejected','abstained'}:break
        final_digest=recipe_content_digest(recipe)
        review=AgentReview(recipe_content_digest=final_digest,outcome='require_human_review' if status=='consensus' else 'reject' if status=='rejected' else 'request_revision',
            reasons=('All specialists and QA agreed on this content; explicit human review still required',) if status=='consensus' else unresolved or ('Consensus not achieved; do not execute',),
            reviewer='specialist-consensus:'+digest(rounds))
        recipe=recipe.model_copy(update={'agent_review':review})
        report=ConsensusReport(status=status,plan_digest=digest(plan),recipe_content_digest=final_digest,rounds=len(rounds),votes=tuple(votes),unresolved=unresolved)
        save('proposed_recipe.json',recipe.model_dump(mode='json'))
        save('consensus.json',report.model_dump(mode='json'))
        save('qa_report.json',assess(recipe,plan.resources).model_dump(mode='json'))
        summary=['# Metadata harmonization review',f'Consensus status: **{status}**.',
                 'No source data was read. No human approval has been recorded.',
                 f'Recipe content digest: `{final_digest}`.',
                 'Encoder: '+plan.encoder.encoder+' '+plan.encoder.version+'. '+plan.encoder.purpose+'.',
                 'Inspect proposed_recipe.json, qa_report.json, consensus.json, dialogue.jsonl and agent_traces.json together.']
        for binding in plan.bindings:
            summary.extend(['',f'## {binding.binding_id}',
                f'{binding.source_variable} → {binding.target.name}; output unit: {binding.target.unit}.',
                binding.target.definition,
                f'Documented source calibration: scale={binding.source.metadata.calibration_scale}; offset={binding.source.metadata.calibration_offset}.',
                'Source version: '+binding.source.version+'. License: '+binding.source.rights.license+'.',
                binding.source.rights.attribution])
        summary.extend(['','## Model review findings','These are model judgments for scientific evaluation, not established scientific facts.'])
        for role,vote in votes:
            summary.extend(['',f'### {role}: {vote.decision}',vote.rationale,*['- '+c for c in vote.concerns]])
        (root/'review_summary.md').write_text('\n\n'.join(summary)+'\n')
        save('review.json',{'status':'needs_review' if status=='consensus' else 'needs_revision','human_approved':False,'recipe_digest':digest(recipe)})
        save('execution_contract.json',{'plan_digest':digest(plan),'recipe_content_digest':final_digest,'encoder_spec_digest':digest(plan.encoder),
             'executor_contract':base['executor_contract'],'data_materialization':False,'source_reads_require_approved_recipe':True,'batch_size':plan.batch_size,
             'stream_operations':sorted(STREAM_OPERATIONS),'unsupported_in_stream':['unbounded joins','unbounded aggregations','full-scene reads'],
             'embedding_kind':plan.encoder.purpose})
        return report
    except Exception as error:
        save('failure.json',{'type':type(error).__name__,'reason':'Consensus did not complete; retained dialogue/traces; no data read or transformation executed','validation_detail':str(error)[:1600] if isinstance(error,ValueError) else 'See failed task trace'})
        raise
    finally:
        save('agent_traces.json',[t.model_dump(mode='json') for t in getattr(backend,'traces',())])
