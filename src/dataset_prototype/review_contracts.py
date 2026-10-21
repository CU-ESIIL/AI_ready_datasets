"""Versioned evidence-first review contracts, separate from legacy dialogue votes."""
from enum import Enum
from typing import Literal
from pydantic import Field,model_validator
from .contracts import Contract, EvidenceKind


class Domain(str,Enum):
    SEMANTIC='semantic'
    UNITS='units'
    SUPPORT='support'
    RIGHTS='rights'
    INTEGRITY='integrity'
    QUALITY='quality'
    QA='qa'


class Status(str,Enum):
    PASS='PASS'
    FAIL='FAIL'
    NEEDS_EVIDENCE='NEEDS_EVIDENCE'
    NOT_APPLICABLE='NOT_APPLICABLE'


class Evidence(Contract):
    evidence_id: str=Field(min_length=1)
    domain: Domain
    kind: EvidenceKind
    source: str=Field(min_length=1)
    statement: str=Field(min_length=1,max_length=3000)
    content_digest: str=Field(pattern=r'^[a-f0-9]{64}$')


class ReviewFinding(Contract):
    schema_version: Literal['1']='1'
    finding_id: str=Field(pattern=r'^[a-z][a-z0-9_.-]{2,100}$')
    reviewer_domain: Domain
    status: Status
    claim: str=Field(min_length=1,max_length=2000)
    evidence: tuple[str,...]=Field(min_length=1,max_length=16)
    source: str=Field(min_length=1)
    severity: Literal['info','warning','blocker']='blocker'
    required_action: str=Field(min_length=1,max_length=2000)
    confidence: float=Field(ge=0,le=1)
    supporting_reviewers: tuple[Domain,...]=()
    references: tuple[str,...]=()
    supports: tuple[str,...]=()


class SpecialistReview(Contract):
    reviewer_domain: Domain
    recipe_content_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    findings: tuple[ReviewFinding,...]=Field(min_length=1,max_length=16)

    @model_validator(mode='after')
    def ownership(self):
        if any(f.reviewer_domain!=self.reviewer_domain for f in self.findings):
            raise ValueError('specialist cannot own findings outside its jurisdiction')
        return self


class ReviewReport(Contract):
    schema_version: Literal['1']='1'
    recipe_content_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    source_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    reviews: tuple[SpecialistReview,...]
    evidence: tuple[Evidence,...]
    unique_findings: tuple[ReviewFinding,...]
    resolved_findings: tuple[str,...]
    unresolved_findings: tuple[str,...]
    required_domains: tuple[Domain,...]
    missing_domains: tuple[Domain,...]
    model_consensus: Literal['eligible_for_approval','needs_review','needs_revision']
    qa_decision: Literal['accept','revise','reject','needs_evidence'] | None = None
    qa_finding_ids: tuple[str,...] = ()
    human_approval: Literal['pending','not_requested']='not_requested'
    execution_authorized: Literal[False]=False


class RunManifest(Contract):
    schema_version: Literal['1']='1'
    run_id: str
    stage: Literal['discovery','harmonization','representation','review']
    status: Literal['complete','failed','blocked']
    code_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    input_digest: str=Field(pattern=r'^[a-f0-9]{64}$')
    artifacts: tuple[str,...]
    fixture: bool
    source_data_read: bool
    notes: tuple[str,...]=()
