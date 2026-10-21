"""Generated metadata and ontology candidates only; no network or source-data reads."""
import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from dataset_prototype.contracts import (SemanticEvidence,SourceSemantics,SourceResource,ConceptCandidate,
    EvidenceKind,digest,SemanticMapping)
from dataset_prototype.semantic_discovery import enrich,source_metadata_digest
from dataset_prototype.semantic_resources import SemanticResourceRegistry,load_inventory

@pytest.fixture
def evidence():
    return SemanticEvidence(source_field='temperature',source_label='air temperature',
        source_definition='Generated source definition.',source_vocabulary='example-vocabulary',
        source_concept_id='urn:example:semantic:air-temperature',unit='K',
        evidence_type='SOURCE_DOCUMENTED',evidence_location='fixture:/variables/0',confidence=.7)

@pytest.fixture
def registry():
    return SemanticResourceRegistry(load_inventory('data/semantics/semantic_resources.csv'),
        json.loads(Path('data/fixtures/semantics/concepts.json').read_text()))

def test_partial_complete_roundtrip_and_invalid_evidence(evidence):
    partial=SemanticEvidence(source_field='band',evidence_type='MISSING_EVIDENCE',evidence_location='fixture:/band')
    assert partial.source_concept_id is None and partial.confidence is None
    complete=SemanticEvidence.model_validate({**evidence.model_dump(),
        'source_concept_uri':'urn:example:semantic:air-temperature','standard_name':'example-temperature',
        'standard_name_scheme':'example','unit_scheme':'example','quantity_kind':'temperature',
        'entity_hint':'air','property_hint':'temperature','matrix_hint':'generated atmosphere',
        'context_hint':'fixture','taxon_identifier':'urn:example:taxon','taxon_scheme':'example',
        'method':'generated','protocol':'fixture-v1','sensor':'fixture-sensor','platform':'fixture-platform',
        'spatial_resolution':10,'spatial_resolution_unit':'m','spatial_support':'generated cell',
        'temporal_resolution':'daily','temporal_support':'interval','source_documentation':('urn:example:doc',)})
    assert SemanticEvidence.model_validate_json(complete.model_dump_json())==complete
    for update in [{'evidence_type':'INFERRED_AS_FACT'},{'confidence':1.1},{'spatial_resolution':0}]:
        with pytest.raises(ValidationError):SemanticEvidence.model_validate({**evidence.model_dump(),**update})

def test_source_multiple_systems_preserve_original_and_reject_stale(client,evidence):
    source=client.resources[0];before=digest(source)
    assert 'semantics' not in source.model_dump(mode='json')
    other=evidence.model_copy(update={'source_vocabulary':'another-system','source_concept_id':'urn:other:temperature'})
    semantics=SourceSemantics(evidence=(evidence,other),extractor='explicit-fixture',source_metadata_digest=source_metadata_digest(source))
    annotated=source.model_copy(update={'semantics':semantics})
    validated=SourceResource.model_validate_json(annotated.model_dump_json())
    assert len(validated.semantics.evidence)==2
    assert validated.semantics.evidence[1].source_concept_id=='urn:other:temperature'
    assert digest(source)==before and source.semantics is None
    assert enrich(validated)==validated
    changed=annotated.model_dump(mode='json');changed['version']='changed'
    with pytest.raises(ValidationError,match='different source metadata'):SourceResource.model_validate(changed)
    assert enrich(source).semantics.evidence[0].source_definition==source.variables[0].definition

def test_registry_candidate_bases_never_approve(evidence,registry):
    annotated=registry.candidates(evidence,identifier=evidence.source_concept_id)[0]
    assert annotated.match_basis=='source_annotation' and annotated.confidence==.7
    assert annotated.evidence==(evidence,)
    lexical=evidence.model_copy(update={'source_label':'temperature','source_concept_id':None})
    results=registry.candidates(lexical)
    assert {c.match_basis for c in results}=={'lexical','exact_vocabulary_match'}
    inferred=evidence.model_copy(update={'evidence_type':EvidenceKind.MODEL_JUDGMENT})
    assert registry.candidates(inferred)[0].match_basis=='model_inferred'
    normalized=evidence.model_copy(update={'evidence_type':EvidenceKind.DERIVED_DETERMINISTICALLY})
    assert registry.candidates(normalized,identifier=normalized.source_concept_id)[0].match_basis=='normalized_identifier'
    assert registry.lookup('urn:missing') is None
    assert registry.source(annotated.identifier)=='urn:example:semantic:vocabulary'
    assert registry.relationships(annotated.identifier)[0][0]=='broader'
    assert registry.search_resources('population')[0].resource_id=='pco'
    assert not isinstance(annotated,SemanticMapping)
    assert 'relationship' not in annotated.model_dump() and 'review_status' not in annotated.model_dump()
    for extra in [{'relationship':'equivalent_to'},{'review_status':'approved'},{'approved':True}]:
        with pytest.raises(ValidationError):ConceptCandidate.model_validate({**annotated.model_dump(),**extra})
    with pytest.raises(ValidationError,match='model judgment'):
        ConceptCandidate.model_validate({**annotated.model_dump(),'match_basis':'model_inferred'})
    with pytest.raises(ValidationError,match='source-documented'):
        ConceptCandidate.model_validate({**annotated.model_dump(),'evidence':[inferred.model_dump()]})

def test_discovery_enriches_without_mutating_or_fetching(client,request_model,registry):
    from dataset_prototype.discovery import run
    originals=tuple(digest(source) for source in client.resources)
    class MetadataOnly:
        def search(self,request):return client.search(request)
        def fetch(self,*args):raise AssertionError('discovery must not read observations')
    result=run(request_model,MetadataOnly(),semantic_registry=registry)
    assert all(candidate.resource.semantics for candidate in result.candidates)
    assert originals==tuple(digest(source) for source in client.resources)
    assert all('scientific comparability remains unapproved' in candidate.rationale for candidate in result.candidates)

def test_sentinel_extracts_documented_calibration_not_a_mapping():
    source=SourceResource.model_validate_json(Path('data/fixtures/semantics/sentinel_source.json').read_text())
    original=source.model_dump(mode='json')
    result=enrich(source)
    native=next(e for e in result.semantics.evidence if e.evidence_type==EvidenceKind.SOURCE_DOCUMENTED)
    assert (native.band,native.platform,native.scale,native.offset,native.unit,native.spatial_resolution)==('B08','sentinel-2b',.0001,-.1,'1',10)
    assert native.native_crs=='EPSG:32613' and native.processing_baseline=='05.09'
    assert native.processing_level=='S2MSI2A' and native.standard_name is None
    assert native.source_label=='nir' and result.variables[0].unit=='DN'
    assert result.support.start==result.support.end and native.temporal_resolution is None
    assert native.evidence_location.startswith('native-stac:')
    assert result.semantics.candidates==() and 'mappings' not in result.model_dump()
    assert source.model_dump(mode='json')==original

def test_adapter_failure_has_no_mock_fallback(registry):
    class Unavailable:
        def lookup(self,identifier):raise ConnectionError('explicit unavailable resolver')
    bounded=SemanticResourceRegistry(registry.resources,adapters=(Unavailable(),))
    with pytest.raises(ConnectionError):bounded.lookup('urn:unknown')


def test_uri_validation_and_identical_labels_do_not_merge_concepts(evidence,registry):
    with pytest.raises(ValidationError,match='URI/IRI'):
        SemanticEvidence.model_validate({**evidence.model_dump(),'source_concept_uri':'not a URI'})
    from dataset_prototype.semantic_resources import ConceptRecord
    other=registry.concepts[0].model_copy(update={'identifier':'urn:another:air-temperature','ontology':'another-vocabulary'})
    index=SemanticResourceRegistry(registry.resources,(*registry.concepts,other))
    candidates=index.candidates(evidence.model_copy(update={'source_concept_id':None}))
    assert len(candidates)==2 and len({candidate.identifier for candidate in candidates})==2
    assert all(candidate.match_basis=='exact_vocabulary_match' for candidate in candidates)
    assert all('relationship' not in type(candidate).model_fields for candidate in candidates)
    with pytest.raises(ValidationError,match='supplied label'):
        ConceptCandidate.model_validate({**candidates[0].model_dump(),'label':'different quantity'})
