"""Backpressured window → harmonization → encoder → JSONL sink.

Only a bounded microbatch enters the legacy executor. Persisted lineage contains
identifiers and evidence hashes, never raw or harmonized observation values.
"""
import json
from pathlib import Path
from .contracts import digest, recipe_content_digest, HarmonizationRecipe, HumanDecision
from .stream_contracts import StreamPlan, StreamSample, ConsensusReport, REVIEWERS
from .consensus import STREAM_OPERATIONS
from .harmonization import authorize, run as harmonize, transformed_uncertainty
from .representations import run as encode, batches


def preflight(plan,recipe,human=None,consensus=None,evidence_review=None):
    plan=StreamPlan.model_validate(plan.model_dump(mode='json'))
    recipe=HarmonizationRecipe.model_validate(recipe.model_dump(mode='json'))
    human=HumanDecision.model_validate(human.model_dump(mode='json')) if human is not None else None
    consensus=ConsensusReport.model_validate(consensus.model_dump(mode='json')) if consensus is not None else None
    if plan.reader in {'sentinel-pixel','sentinel-raster'}:
        from .stream_sources import validated_native
        for binding in plan.bindings:validated_native(binding)
    if recipe.scope!='core' or any(o.operation not in STREAM_OPERATIONS for o in recipe.operations):
        raise ValueError('streaming supports core scalar operations only; joins/aggregations require a separate bounded design')
    expected={(b.source.asset_id,b.source_variable):b.target for b in plan.bindings}
    actual={(m.source_asset,m.source_variable):m.target for m in recipe.mappings}
    if len(actual)!=len(recipe.mappings) or actual!=expected:
        raise ValueError('recipe targets/source bindings differ from stream plan')
    if recipe.author=='metadata-specialist-consensus':
        if consensus is None or consensus.status!='consensus' or consensus.plan_digest!=digest(plan) or consensus.recipe_content_digest!=recipe_content_digest(recipe):
            raise ValueError('matching completed metadata consensus required')
        if len(consensus.votes)!=len(REVIEWERS) or {role for role,_ in consensus.votes}!=set(REVIEWERS) or any(v.decision!='agree' or v.concerns for _,v in consensus.votes) or consensus.unresolved:
            raise ValueError('all specialists and QA must agree without unresolved concerns')
    if plan.reader in {'sentinel-pixel','sentinel-raster'}:
        from .review_contracts import ReviewReport
        from .review import REQUIRED_DOMAINS, source_set_digest
        if evidence_review is None:
            raise ValueError('real streaming requires a matching evidence-bound review report')
        report = ReviewReport.model_validate(evidence_review.model_dump(mode='json'))
        if (report.recipe_content_digest != recipe_content_digest(recipe)
            or report.source_digest != source_set_digest(plan.resources)
            or report.model_consensus != 'eligible_for_approval'
            or report.qa_decision != 'accept'
            or report.missing_domains
            or set(report.required_domains) != set(REQUIRED_DOMAINS)
            or {r.reviewer_domain for r in report.reviews} != set(REQUIRED_DOMAINS)):
            raise ValueError('evidence review is incomplete, vetoed or bound to different inputs')
        # Recompute findings and evidence checks instead of trusting a serialized label.
        from .review import synthesize, validate_qa_references
        recomputed = synthesize(report.reviews, report.evidence,
            recipe_content_digest=recipe_content_digest(recipe), source_digest=source_set_digest(plan.resources))
        validate_qa_references(recomputed, report.qa_finding_ids)
        if (recomputed.model_consensus != 'eligible_for_approval' or not report.qa_finding_ids
            or report.unique_findings != recomputed.unique_findings):
            raise ValueError('evidence review synthesis or QA references do not match findings')
        # Recompute statuses instead of trusting a serialized eligibility label.
        from .review_contracts import Status
        if any(f.status not in (Status.PASS,Status.NOT_APPLICABLE)
               for review in report.reviews for f in review.findings):
            raise ValueError('evidence review has unresolved specialist findings')
    return authorize(recipe,plan.resources,human)


def stream_embed(plan,recipe,samples,output,*,human=None,consensus=None,evidence_review=None):
    # No iterator is opened before all scientific and human gates have passed.
    plan=StreamPlan.model_validate(plan.model_dump(mode='json'))
    recipe=HarmonizationRecipe.model_validate(recipe.model_dump(mode='json'))
    human=HumanDecision.model_validate(human.model_dump(mode='json')) if human is not None else None
    consensus=ConsensusReport.model_validate(consensus.model_dump(mode='json')) if consensus is not None else None
    if plan.reader=='sentinel-raster' or plan.encoder.method=='mosaiks':raise ValueError('use mosaiks-run for reviewed raster outputs')
    qa=preflight(plan,recipe,human,consensus,evidence_review)
    root=Path(output);root.mkdir(parents=True,exist_ok=False)
    def save(name,value):
        with (root/name).open('x') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False)
    save('data_access_plan.json',plan.model_dump(mode='json'))
    save('recipe.json',recipe.model_dump(mode='json'))
    save('encoder_spec.json',plan.encoder.model_dump(mode='json'))
    save('qa_report.json',qa.model_dump(mode='json'))
    if human:save('human_decision.json',human.model_dump(mode='json'))
    if consensus:save('consensus.json',consensus.model_dump(mode='json'))
    if evidence_review:save('evidence_review.json',evidence_review.model_dump(mode='json'))
    by_binding={b.binding_id:b for b in plan.bindings}
    last_sequence={};count=0;iterator=None
    manifest={'status':'incomplete','records':0,'plan_digest':digest(plan),'recipe_digest':digest(recipe),'encoder_spec_digest':digest(plan.encoder),
              'raw_data_persisted':False,'harmonized_data_persisted':False,'batch_size':plan.batch_size,
              'embedding_kind':plan.encoder.purpose,'stream_executor':'bounded-stream-v1','executor':'allowlist-v2',
              'code_digest':digest({p.name:p.read_text() for p in Path(__file__).parent.glob('*.py')}),'integrity_limit':'Metadata and extracted-window evidence hashes; full remote raster bytes are not pinned or archived.'}
    try:
        iterator=iter(samples)
        with (root/'embeddings.jsonl.partial').open('x') as vectors,(root/'lineage.jsonl.partial').open('x') as lineage:
            for batch in batches(iterator,plan.batch_size):
                sample_by_record={}
                for sample in batch:
                    sample=StreamSample.model_validate(sample.model_dump(mode='json'))
                    binding=by_binding.get(sample.binding_id)
                    if binding is None or (sample.record.asset_id,sample.record.variable)!=(binding.source.asset_id,binding.source_variable):
                        raise ValueError('stream sample does not match binding')
                    if sample.sequence<=last_sequence.get(sample.binding_id,-1):
                        raise ValueError('stream sequence must increase per binding across all batches')
                    last_sequence[sample.binding_id]=sample.sequence
                    key=(sample.record.asset_id,sample.record.record_id)
                    if key in sample_by_record:raise ValueError('duplicate record identity within microbatch')
                    sample_by_record[key]=sample
                observations=harmonize(plan.resources,recipe,(s.record for s in sample_by_record.values()),human)
                for representation in encode(observations,plan.encoder.method):
                    p=representation.provenance[0];raw=p.source_records[0]
                    sample=sample_by_record[(raw.asset_id,raw.record_id)]
                    fields={'observation_ids':representation.observation_ids,'vector':representation.vector,'encoder_spec_digest':digest(plan.encoder),
                            'recipe_digest':digest(recipe),'source_asset':raw.asset_id,'source_record':raw.record_id,
                            'sample_sequence':sample.sequence,'window_evidence_digest':sample.evidence_digest,
                            'modality':representation.modality,'track':representation.track}
                    target=by_binding[sample.binding_id].target
                    fields.update(variable=target.name,unit=target.unit)
                    identity=digest(fields)
                    vectors.write(json.dumps({'representation_id':identity,**fields},allow_nan=False)+'\n')
                    lineage.write(json.dumps({'representation_id':identity,'observation_ids':representation.observation_ids,
                        'source_asset':raw.asset_id,'source_record':raw.record_id,'sample_sequence':sample.sequence,'source_uri':p.source.uri,'source_version':p.source.version,
                        'source_metadata_digest':digest(p.source),'evidence_digest':sample.evidence_digest,'evidence_scope':sample.evidence_scope,
                        'spatial_bbox':sample.spatial_bbox,'native_crs':sample.native_crs,'native_indices':sample.native_indices,
                        'datetime_start':raw.start.isoformat(),'datetime_end':raw.end.isoformat(),'quality_flag':raw.quality_flag,
                        'uncertainty':transformed_uncertainty(raw.uncertainty,[o for o in recipe.operations if o.source_variable==raw.variable and o.source_asset in {None,raw.asset_id}]),'unit':target.unit,
                        'recipe_digest':digest(recipe),'executor':p.executor,'stream_executor':'bounded-stream-v1','qa_digest':digest(qa),'human_decision_digest':digest(human) if human else None,
                        'consensus_digest':digest(consensus) if consensus else None,'evidence_review_digest':digest(evidence_review) if evidence_review else None,'encoder_spec_digest':digest(plan.encoder)},allow_nan=False)+'\n')
                    count+=1
                # Flush before requesting another microbatch: synchronous sink backpressure.
                vectors.flush();lineage.flush()
        if count==0:raise ValueError('stream produced no embeddings')
        (root/'embeddings.jsonl.partial').rename(root/'embeddings.jsonl')
        (root/'lineage.jsonl.partial').rename(root/'lineage.jsonl')
        manifest.update(status='complete',records=count)
    except BaseException as error:
        manifest.update(status='failed',records=count,error_type=type(error).__name__)
        raise
    finally:
        try:
            if iterator is not None and hasattr(iterator,'close'):iterator.close()
        except BaseException as error:
            manifest.update(status='failed',error_type=type(error).__name__)
            raise
        finally:
            save('manifest.json',manifest)
    return manifest
