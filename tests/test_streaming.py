"""Offline generators exercise consensus and streaming; no raster fixtures downloaded."""
import json
import pytest
from datetime import datetime, timezone
from dataset_prototype.contracts import Operation, HumanDecision, digest, recipe_content_digest
from dataset_prototype.stream_contracts import StreamPlan, StreamBinding, StreamSample, SpecialistFinding, RecipeDraft, RecipeBindingProposal, ReviewVote
from dataset_prototype.streaming import stream_embed
from dataset_prototype.harmonization import assess, run
from dataset_prototype.consensus import negotiate


def setup(bundle,batch_size=2):
    r,m,p,rows=bundle
    sourcevar=r.variables[0].model_copy(update={'name':'B08_DN','unit':'DN'})
    r=r.model_copy(update={'variables':(sourcevar,),'metadata':r.metadata.model_copy(update={'calibration_scale':.0001,'calibration_offset':-.1})})
    target=sourcevar.model_copy(update={'name':'reflectance','unit':'1'})
    m=m.model_copy(update={'source_variable':'B08_DN','target':target,'relationship':'convertible_to'})
    ops=(Operation(operation='calibrate',source_asset=r.asset_id,source_variable='B08_DN',from_unit='DN',to_unit='1',scale=.0001,offset=-.1),Operation(operation='map_variable',source_asset=r.asset_id,source_variable='B08_DN',target_variable='reflectance'))
    p=p.model_copy(update={'mappings':(m,),'operations':ops})
    plan=StreamPlan(question='calibrated reflectance',reader='test-generator',bindings=(StreamBinding(binding_id='b',source=r,source_variable='B08_DN',target=target,longitude=rows[0].longitude,latitude=rows[0].latitude),),batch_size=batch_size)
    def samples(n=5):
        for i in range(n):
            raw=rows[0].model_copy(update={'variable':'B08_DN','record_id':str(i),'value':2000+i,'uncertainty':10})
            yield StreamSample(record=raw,sequence=i,evidence_digest=digest({'window':i}),evidence_scope='test-generated',spatial_bbox=r.support.bbox,native_crs='EPSG:4326',native_indices=(i,),binding_id='b')
    return plan,p,samples


def test_calibration_and_uncertainty_and_coefficients(bundle):
    plan,p,samples=setup(bundle)
    out=list(run(plan.resources,p,(next(samples()).record,)))
    assert out[0].value==pytest.approx(.1)
    assert out[0].uncertainty==pytest.approx(.001)
    wrong=p.model_copy(update={'operations':(p.operations[0].model_copy(update={'offset':0}),p.operations[1])})
    assert assess(wrong,plan.resources).outcome=='reject'


def test_direct_stream_backpressure_no_materialized_data(bundle,tmp_path):
    plan,p,samples=setup(bundle)
    root=tmp_path/'out'
    consumed=[]
    def source():
        for i,s in enumerate(samples(9)):
            if i>=2:
                assert (root/'embeddings.jsonl.partial').stat().st_size>0
            consumed.append(i)
            yield s
    result=stream_embed(plan,p,source(),root)
    vectors=[json.loads(x) for x in (root/'embeddings.jsonl').read_text().splitlines()]
    assert result['status']=='complete' and len(vectors)==len(consumed)==9
    assert vectors[0]['vector']==pytest.approx([.1])
    assert not any('raw' in f.name or 'harmonized' in f.name for f in root.iterdir())
    lines=(root/'lineage.jsonl').read_text()
    assert '"value"' not in lines and 'source_records' not in lines
    assert 'spatial_bbox' in lines and 'evidence_digest' in lines
    assert json.loads(lines.splitlines()[0])['uncertainty']==pytest.approx(.001)


def test_preflight_opens_no_source_before_approval(bundle,tmp_path):
    plan,p,samples=setup(bundle)
    def source():
        raise AssertionError('source opened before approval')
        yield
    with pytest.raises(ValueError,match='not approved'):
        stream_embed(plan,p.model_copy(update={'status':'needs_review'}),source(),tmp_path/'out')
    assert not (tmp_path/'out').exists()
    unsupported=p.model_copy(update={'scope':'track','track':'test','core_recipe':p.recipe_id,'operations':(*p.operations,Operation(operation='temporal_mean',source_variable='B08_DN',target_support='daily'))})
    with pytest.raises(ValueError,match='core scalar'):
        stream_embed(plan,unsupported,source(),tmp_path/'out')


def test_failure_partial_and_monotonic_sequences(bundle,tmp_path):
    plan,p,samples=setup(bundle,batch_size=1)
    first=next(samples())
    with pytest.raises(ValueError,match='sequence'):
        stream_embed(plan,p,iter((first,first)),tmp_path/'out')
    result=json.loads((tmp_path/'out/manifest.json').read_text())
    assert result['status']=='failed' and result['records']==1
    assert not (tmp_path/'out/embeddings.jsonl').exists()
    assert (tmp_path/'out/embeddings.jsonl.partial').exists()


class Negotiators:
    model='offline-test';_model_digest='offline-test';traces=[]
    def __init__(self,revise=True):self.revise=revise
    def generate(self,role,instruction,evidence,schema):
        refs=tuple(row['metadata_ref'] for row in evidence['metadata'])
        dialogue=evidence.get('dialogue',[])
        if schema is SpecialistFinding:
            return SpecialistFinding(assessment='Check explicit source scale/offset and native support',constraints=('Preserve support',),concerns=(),evidence_refs=refs)
        if schema is RecipeDraft:
            required=[m['message_id'] for m in dialogue if m['kind']==('analysis' if evidence['round']==1 else 'review') and m['round']==evidence['round']-1]
            binding=evidence['metadata'][0]
            return RecipeDraft(bindings=(RecipeBindingProposal(binding_id=binding['binding_id'],relationship='convertible_to',evidence=('Documented scale/offset',),confidence=1,
                operations=(Operation(operation='calibrate',source_variable='B08_DN',from_unit='DN',to_unit='1',scale=.0001,offset=-.1),Operation(operation='map_variable',source_variable='B08_DN',target_variable='reflectance'))),),rationale='Use documented calibration',responds_to=tuple(required))
        peer=next(m['message_id'] for m in dialogue if m['sender']!=role and m['kind']=='analysis')
        number=max(m['round'] for m in dialogue)
        revise=self.revise and role=='units' and number==1
        return ReviewVote(decision='revise' if revise else 'agree',rationale='Responding to peer and shared draft',concerns=('Make calibration rationale explicit',) if revise else (),responds_to=(evidence['draft_message_id'],peer),evidence_refs=refs)


def test_consensus_revision_shared_digest_and_human_gate(bundle,tmp_path):
    plan,p,samples=setup(bundle)
    result=negotiate(plan,Negotiators(),tmp_path/'consensus')
    assert result.status=='consensus' and result.rounds==2
    from dataset_prototype.contracts import HarmonizationRecipe
    proposed=HarmonizationRecipe.model_validate_json((tmp_path/'consensus/proposed_recipe.json').read_text())
    assert recipe_content_digest(proposed)==result.recipe_content_digest
    assert proposed.status=='needs_review'
    approved=proposed.model_copy(update={'status':'approved'})
    with pytest.raises(ValueError,match='human review'):
        stream_embed(plan,approved,samples(),tmp_path/'out',consensus=result)
    human=HumanDecision(recipe_digest=digest(approved),status='approved',reviewer='offline-test-only',rationale='Known generated calibration test',timestamp=datetime.now(timezone.utc))
    assert stream_embed(plan,approved,samples(),tmp_path/'out',human=human,consensus=result)['records']==5
    changed=plan.model_copy(update={'batch_size':1})
    with pytest.raises(ValueError,match='consensus'):
        stream_embed(changed,approved,samples(),tmp_path/'stale',human=human,consensus=result)


def test_bounded_disagreement_is_not_consensus(bundle,tmp_path):
    plan,_,_=setup(bundle)
    result=negotiate(plan,Negotiators(),tmp_path/'consensus',max_rounds=1)
    assert result.status=='needs_revision' and result.unresolved


def test_calibration_is_asset_scoped_even_with_shared_band_name(bundle,tmp_path):
    plan,p,samples=setup(bundle)
    first=next(samples())
    r=plan.resources[0]
    second_source=r.model_copy(update={'asset_id':r.asset_id+'-second','metadata':r.metadata.model_copy(update={'calibration_scale':.01,'calibration_offset':0})})
    binding=plan.bindings[0].model_copy(update={'binding_id':'second','source':second_source})
    plan=plan.model_copy(update={'bindings':(*plan.bindings,binding)})
    second_mapping=p.mappings[0].model_copy(update={'source_asset':second_source.asset_id})
    second_ops=tuple(o.model_copy(update={'source_asset':second_source.asset_id,**({'scale':.01,'offset':0} if o.operation=='calibrate' else {})}) for o in p.operations)
    p=p.model_copy(update={'mappings':(*p.mappings,second_mapping),'operations':(*p.operations,*second_ops)})
    second=first.model_copy(update={'binding_id':'second','record':first.record.model_copy(update={'asset_id':second_source.asset_id})})
    stream_embed(plan,p,iter((first,second)),tmp_path/'out')
    vectors=[json.loads(line)['vector'][0] for line in (tmp_path/'out/embeddings.jsonl').read_text().splitlines()]
    assert vectors==pytest.approx([.1,20])


def test_encoder_spec_cannot_mislabel_implemented_preprocessing():
    from dataset_prototype.stream_contracts import EncoderSpec
    with pytest.raises(ValueError,match='encoder identity'):
        EncoderSpec(preprocessing='learned normalization')
    with pytest.raises(ValueError,match='encoder identity'):
        EncoderSpec(method='squared',encoder='scalar-and-square',dimensionality=2)
    assert EncoderSpec(method='squared',encoder='scalar-and-square',dimensionality=2,preprocessing='append square; no scaling').dimensionality==2


def test_empty_stream_is_explicit_failure(bundle,tmp_path):
    plan,p,_=setup(bundle)
    with pytest.raises(ValueError,match='no embeddings'):
        stream_embed(plan,p,iter(()),tmp_path/'out')
    assert json.loads((tmp_path/'out/manifest.json').read_text())['status']=='failed'


def test_unanimous_models_cannot_override_metadata_qa(bundle,tmp_path):
    plan,_,_=setup(bundle)
    class WrongCalibration(Negotiators):
        def generate(self,role,instruction,evidence,schema):
            result=super().generate(role,instruction,evidence,schema)
            if schema is RecipeDraft:
                b=result.bindings[0]
                b=b.model_copy(update={'operations':(b.operations[0].model_copy(update={'offset':0}),b.operations[1])})
                return result.model_copy(update={'bindings':(b,)})
            return result
    result=negotiate(plan,WrongCalibration(revise=False),tmp_path/'bad',max_rounds=1)
    assert {v.decision for _,v in result.votes}=={'agree'}
    assert result.status=='needs_revision'
    assert any('calibration disagrees' in reason for reason in result.unresolved)


def test_explicit_retry_reuses_validated_analyses_without_repair(bundle,tmp_path):
    from dataset_prototype.model_agents import AgentTrace
    class Traced(Negotiators):
        def __init__(self,fail=False):super().__init__(revise=False);self.traces=[];self.fail=fail;self.calls=[]
        def generate(self,role,instruction,evidence,schema):
            self.calls.append(role)
            result=super().generate(role,instruction,evidence,schema)
            bad=self.fail is True and role=='harmonization'
            if self.fail=='peer' and schema is ReviewVote and role=='semantic':
                own=next(m['message_id'] for m in evidence['dialogue'] if m['sender']==role)
                result=result.model_copy(update={'responds_to':(evidence['draft_message_id'],own)})
            input_json=json.dumps(evidence,sort_keys=True)
            output_json='{"invalid":"draft"}' if bad else result.model_dump_json()
            self.traces.append(AgentTrace(role=role,backend='test',model=self.model,model_digest=self._model_digest,prompt_digest=digest(input_json),response_digest=digest(output_json),input_json=input_json,output_json=output_json,timestamp=datetime.now(timezone.utc),error='ValueError' if bad else None))
            if bad:raise ValueError('invalid draft')
            return result
    plan,_,_=setup(bundle)
    with pytest.raises(ValueError,match='invalid draft'):
        negotiate(plan,Traced(fail=True),tmp_path/'failed')
    resumed=Traced()
    result=negotiate(plan,resumed,tmp_path/'retry',analysis_from=tmp_path/'failed')
    assert result.status=='consensus' and resumed.calls[0]=='harmonization'
    assert len(resumed.calls)==6 and len(resumed.traces)==11
    assert (tmp_path/'failed/failure.json').exists() and (tmp_path/'retry/retry_context.json').exists()
    with pytest.raises(ValueError,match='another specialist'):
        negotiate(plan,Traced(fail='peer'),tmp_path/'failed-peer')
    reviewer=Traced()
    assert negotiate(plan,reviewer,tmp_path/'fresh-review',analysis_from=tmp_path/'failed-peer').status=='consensus'
    assert len(reviewer.calls)==5 and 'harmonization' not in reviewer.calls
    changed=plan.model_copy(update={'batch_size':1})
    with pytest.raises(ValueError,match='exact plan'):
        negotiate(changed,Traced(),tmp_path/'wrong',analysis_from=tmp_path/'failed')
