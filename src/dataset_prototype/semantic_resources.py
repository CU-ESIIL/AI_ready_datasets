"""Validated landscape inventory and portal-independent concept-candidate retrieval."""
import csv
import json
from pathlib import Path
from typing import Literal, Protocol
from pydantic import Field, model_validator
from .contracts import Contract, ConceptCandidate, SemanticEvidence, EvidenceKind

COVERAGE_DIMENSIONS=('molecular','cellular','anatomy','organism','taxonomy','trait','behavior',
    'population','community','interaction','ecosystem','habitat','environment','space','time',
    'observation','sampling','method','units','scale_support','provenance')
Coverage=Literal['strong','partial','indirect','not_target','unknown']

class SemanticResource(Contract):
    assessment_id: str = Field(min_length=1)
    resource_id: str = Field(pattern=r'^[a-z][a-z0-9_-]+$')
    name: str
    acronym: str
    resource_type: Literal['formal_ontology','application_ontology','upper_ontology','relation_ontology',
        'controlled_vocabulary','thesaurus','classification','exchange_standard','metadata_standard',
        'semantic_framework','conceptual_model','historical_effort','resource_network']
    domain: str
    era: str
    first_release_or_origin: str
    maintainer: str
    status: Literal['active_registry','inactive_registry','documented','historical','unresolved']
    canonical_uri: str | None
    documentation_uri: str | None
    license: str | None
    coverage: dict[str, Coverage]
    key_contribution: str
    historical_role: str
    problem_originally_addressed: str
    relationship_to_prior_work: str
    current_relevance: str
    project_role: str
    core_candidate: bool
    domain_candidate: bool
    interoperability_only: bool
    historical_precedent: bool
    machine_access: str
    format: str
    resolvable_identifiers: bool | None
    api_available: bool | None
    imports_or_dependencies: tuple[str,...]
    known_crosswalks: tuple[str,...]
    overlaps: tuple[str,...]
    limitations: str
    notes: str
    evidence_source: tuple[str,...]
    last_verified: str | None
    verification_scope: Literal['registry_metadata','primary_documentation','reference_only','unresolved']

    @model_validator(mode='after')
    def dimensions(self):
        if set(self.coverage)!=set(COVERAGE_DIMENSIONS):
            raise ValueError('coverage must identify every dimension explicitly')
        return self

class AssessmentContent(Contract):
    coverage: dict[str, Coverage]
    project_role: str
    core_candidate: bool
    domain_candidate: bool
    interoperability_only: bool
    historical_precedent: bool
    era: str
    historical_role: str
    limitations: str
    overlaps: tuple[str,...]


class ResourceAssessment(Contract):
    assessment_id: str
    resource_id: str
    assessment: AssessmentContent
    reviewer: str
    date: str
    evidence: tuple[str,...]
    confidence: float = Field(ge=0,le=1)
    notes: str
    expert_reviewed: bool = False


def load_inventory(path):
    records=[]
    if Path(path).stat().st_size>8*1024*1024:raise ValueError('inventory exceeds metadata byte budget')
    with Path(path).open(newline='') as handle:
        for row in csv.DictReader(handle):
            row['coverage']={key:row.pop(key) for key in COVERAGE_DIMENSIONS}
            for key in ('core_candidate','domain_candidate','interoperability_only','historical_precedent','resolvable_identifiers','api_available'):
                value=row[key]
                if value not in {'true','false',''}:raise ValueError('invalid inventory boolean')
                row[key]={'true':True,'false':False,'':None}[value]
            for key in ('imports_or_dependencies','known_crosswalks','overlaps','evidence_source'):
                row[key]=json.loads(row[key])
            for key in ('canonical_uri','documentation_uri','license','last_verified'):
                row[key]=row[key] or None
            resource=SemanticResource.model_validate(row)
            if set(resource.coverage)!=set(COVERAGE_DIMENSIONS):raise ValueError('incomplete coverage dimensions')
            records.append(resource)
    if len({r.resource_id for r in records})!=len(records):raise ValueError('duplicate semantic resource identity')
    return tuple(records)


def load_assessments(path, resources):
    if Path(path).stat().st_size>8*1024*1024:raise ValueError('assessments exceed metadata byte budget')
    assessments=tuple(ResourceAssessment.model_validate_json(line) for line in Path(path).read_text().splitlines() if line)
    lookup={assessment.assessment_id:assessment for assessment in assessments}
    if len(lookup)!=len(assessments):raise ValueError('duplicate assessment identity')
    for resource in resources:
        assessment=lookup.get(resource.assessment_id)
        if assessment is None or assessment.resource_id!=resource.resource_id:
            raise ValueError('missing bound resource assessment')
        expected=AssessmentContent.model_validate({key:getattr(resource,key) for key in AssessmentContent.model_fields})
        if expected!=assessment.assessment:raise ValueError('resource and assessment content differ')
    return assessments


class NamespaceBinding(Contract):
    resource_id: str
    exact: tuple[str,...] = ()
    prefixes: tuple[str,...] = ()
    evidence: str = Field(min_length=1)

    @model_validator(mode='after')
    def valid(self):
        if not self.exact and not self.prefixes:raise ValueError('binding needs exact identifiers or prefixes')
        if any(not item.strip() for item in (*self.exact,*self.prefixes)):
            raise ValueError('empty annotation binding is unsafe')
        return self

class ConceptRecord(Contract):
    identifier: str
    label: str
    ontology: str
    definition: str | None = None
    domain: str | None = None
    source_uri: str
    relationships: tuple[tuple[str,str], ...] = ()
    fixture: bool

class SemanticResolver(Protocol):
    """External access belongs behind explicit adapters, with no automatic network fallback."""
    def search(self,label,domain=None): ...
    def lookup(self,identifier): ...
    def describe(self,identifier): ...
    def relationships(self,identifier): ...
    def source(self,identifier): ...

class SemanticResourceRegistry:
    """Index of semantic resources and declared concepts; not the pipeline architecture."""
    def __init__(self, resources, concepts=(), *, adapters=()):
        self.resources=tuple(resources)
        self.concepts=tuple(ConceptRecord.model_validate(c) if isinstance(c,dict) else c for c in concepts)
        if len({c.identifier for c in self.concepts})!=len(self.concepts):raise ValueError('duplicate concept identifier')
        self.adapters=tuple(adapters)

    def search(self,label,domain=None):
        if not label.strip():return ()
        needle=label.casefold()
        local=tuple(c for c in self.concepts if needle in c.label.casefold() and (domain is None or c.domain==domain))
        return local+tuple(c for adapter in self.adapters for c in adapter.search(label,domain))

    def search_resources(self,label,domain=None):
        needle=label.casefold()
        return tuple(r for r in self.resources if needle in (r.name+' '+r.acronym).casefold()
                     and (domain is None or r.domain==domain))

    def lookup(self,identifier):
        for record in self.concepts:
            if record.identifier==identifier:return record
        for adapter in self.adapters:
            result=adapter.lookup(identifier)
            if result is not None:return result
        return None

    def describe(self,identifier):
        record=self.lookup(identifier)
        if record is None:raise LookupError('unknown concept identifier')
        return record

    def relationships(self,identifier):return self.describe(identifier).relationships
    def source(self,identifier):return self.describe(identifier).source_uri

    def candidates(self,evidence: SemanticEvidence, *, identifier=None):
        records=(self.lookup(identifier),) if identifier else self.search(evidence.source_label or '')
        candidates=[]
        for record in records:
            if record is None:continue
            basis=('model_inferred' if evidence.evidence_type==EvidenceKind.MODEL_JUDGMENT else
                   'source_annotation' if identifier and evidence.evidence_type==EvidenceKind.SOURCE_DOCUMENTED else
                   'normalized_identifier' if identifier and evidence.evidence_type==EvidenceKind.DERIVED_DETERMINISTICALLY else
                   'exact_vocabulary_match' if record.label.casefold()==(evidence.source_label or '').casefold() else 'lexical')
            candidates.append(ConceptCandidate(identifier=record.identifier,label=record.label,ontology=record.ontology,
                definition=record.definition,match_basis=basis,evidence=(evidence,),confidence=evidence.confidence))
        return tuple(candidates)
