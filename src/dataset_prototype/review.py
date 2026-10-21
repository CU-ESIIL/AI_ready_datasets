"""Deterministic synthesis of evidence-bound specialist findings.

This module does not infer scientific truth from prose or authorize execution.
Callers supply an immutable evidence ledger and a frozen scientific recipe digest.
"""
from .contracts import digest
from .review_contracts import Domain, Evidence, EvidenceKind, ReviewReport, Status

REQUIRED_DOMAINS = (Domain.SEMANTIC, Domain.UNITS, Domain.SUPPORT, Domain.RIGHTS,
                    Domain.INTEGRITY, Domain.QUALITY)


def source_set_digest(sources):
    """Stable identity of complete source records, independent of caller order."""
    sources=tuple(sources)
    if len({source.asset_id for source in sources}) != len(sources):
        raise ValueError('duplicate review source identifiers')
    return digest([source.model_dump(mode='json') for source in sorted(sources, key=lambda s:s.asset_id)])


def synthesize(reviews, evidence, *, recipe_content_digest, source_digest,
               required_domains=REQUIRED_DOMAINS):
    """Validate jurisdiction, bindings and references, then compute review state.

    Evidence domains enforce citation ownership; they cannot detect an inaccurate
    natural-language paraphrase. Expert review remains necessary.
    """
    reviews, evidence = tuple(reviews), tuple(evidence)
    ledger = {item.evidence_id: item for item in evidence}
    if len(ledger) != len(evidence):
        raise ValueError('duplicate evidence identifiers')
    domains = [review.reviewer_domain for review in reviews]
    if len(set(domains)) != len(domains) or Domain.QA in domains:
        raise ValueError('one review per specialist; QA cannot add scientific findings')
    findings = {}
    for review in reviews:
        if review.recipe_content_digest != recipe_content_digest:
            raise ValueError('review is bound to a different scientific recipe')
        for finding in review.findings:
            if not finding.finding_id.startswith(review.reviewer_domain.value + '.'):
                raise ValueError('finding identifier must name its owning jurisdiction')
            if finding.finding_id in findings:
                raise ValueError('duplicate finding; cite the existing identifier instead')
            cited = []
            for identifier in finding.evidence:
                if identifier not in ledger:
                    raise ValueError('unknown evidence identifier')
                item = ledger[identifier]
                if item.domain != review.reviewer_domain:
                    raise ValueError('cross-jurisdiction evidence citation')
                cited.append(item)
            if finding.source not in {item.source for item in cited}:
                raise ValueError('finding source must match cited evidence provenance')
            if any((old.reviewer_domain,old.claim.strip().casefold(),old.evidence) ==
                   (finding.reviewer_domain,finding.claim.strip().casefold(),finding.evidence)
                   for old in findings.values()):
                raise ValueError('duplicate claim; reference the existing finding')
            if finding.status == Status.FAIL and not any(item.kind in (
                EvidenceKind.SOURCE_DOCUMENTED, EvidenceKind.OBSERVED_IN_DATA,
                EvidenceKind.DERIVED_DETERMINISTICALLY) for item in cited):
                raise ValueError('FAIL requires documented or measured evidence')
            if finding.status in (Status.PASS, Status.NOT_APPLICABLE) and all(item.kind in (
                EvidenceKind.MISSING_EVIDENCE, EvidenceKind.MODEL_JUDGMENT) for item in cited):
                raise ValueError('PASS requires evidence; NOT_APPLICABLE also requires supported scope evidence')
            findings[finding.finding_id] = finding
    for finding in findings.values():
        if any(ref not in findings or ref == finding.finding_id for ref in finding.references):
            raise ValueError('finding reference must identify another existing finding')
        if not set(finding.supports).issubset(finding.references):
            raise ValueError('explicit support must also reference an existing finding')
        if any(domain not in domains for domain in finding.supporting_reviewers):
            raise ValueError('supporting reviewer has not submitted a bound review')
    # Endorsement is derived from submitted cross-references, never invented by a role.
    for identifier, finding in tuple(findings.items()):
        supporters=tuple(sorted({other.reviewer_domain for other in findings.values()
            if identifier in other.supports and other.reviewer_domain != finding.reviewer_domain}, key=lambda d:d.value))
        if set(finding.supporting_reviewers) - set(supporters):
            raise ValueError('supporting reviewer has not referenced this finding')
        findings[identifier]=finding.model_copy(update={'supporting_reviewers':supporters})
    required_domains = tuple(required_domains)
    missing = tuple(domain for domain in required_domains if domain not in domains)
    required = [f for f in findings.values() if f.reviewer_domain in required_domains]
    unresolved = tuple(f.finding_id for f in findings.values()
                       if f.status in (Status.FAIL, Status.NEEDS_EVIDENCE))
    state = ('needs_revision' if any(f.status == Status.FAIL for f in required)
             else 'needs_review' if missing or any(f.status == Status.NEEDS_EVIDENCE for f in required)
             else 'eligible_for_approval')
    return ReviewReport(recipe_content_digest=recipe_content_digest,
        source_digest=source_digest, reviews=reviews, evidence=evidence, unique_findings=tuple(findings.values()),
        resolved_findings=tuple(f.finding_id for f in findings.values() if f.finding_id not in unresolved),
        unresolved_findings=unresolved, required_domains=required_domains, missing_domains=missing,
        model_consensus=state, human_approval='pending', execution_authorized=False)


def validate_qa_references(report: ReviewReport, finding_ids):
    """QA may select existing findings for synthesis, never invent domain findings."""
    known = {finding.finding_id for finding in report.unique_findings}
    if not set(finding_ids).issubset(known):
        raise ValueError('QA references unknown findings')
    return tuple(dict.fromkeys(finding_ids))
