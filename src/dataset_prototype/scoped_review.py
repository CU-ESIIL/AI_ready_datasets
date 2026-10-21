"""Independently callable metadata review; the backend has no source-access tools."""
from pathlib import Path
import json
from typing import Literal
from pydantic import Field, create_model, model_validator
from .contracts import Contract, HarmonizationRecipe, SourceResource, digest, recipe_content_digest
from .operations import REGISTRY
from .review import REQUIRED_DOMAINS, synthesize, validate_qa_references, source_set_digest
from .review_contracts import Evidence, SpecialistReview, ReviewFinding, RunManifest

JURISDICTIONS = {
    'semantic': 'Quantity meaning and measurement definition only. Unit 1 means dimensionless; biological equivalence requires evidence.',
    'units': 'Units, documented calibration coefficients and deterministic range-check evidence only. Do not calculate ranges or derive formulas. Negative reflectance is not by itself a calibration failure. Never invent clipping.',
    'support': 'Native CRS, pixel indices, spatial support, instantaneous or interval temporal support and support changes only.',
    'rights': 'Documented permissions, restrictions, attribution and the stated intended operation only. A license label is not the complete terms. Missing terms mean NEEDS_EVIDENCE, not an invented prohibition.',
    'integrity': 'Source/version identifiers, checksum scope, frozen recipe binding and provenance completeness only. Metadata hashes do not cover remote raster bytes.',
    'quality': 'Explicit nodata and mask predicates and suitability for the stated use only. Calibration, quality filtering and analysis readiness are different claims.',
}

class ReviewBundle(Contract):
    recipe: HarmonizationRecipe
    sources: tuple[SourceResource, ...] = Field(min_length=1, max_length=16)
    source_digest: str = Field(pattern=r'^[a-f0-9]{64}$')
    intended_operation: str = Field(min_length=1, max_length=1500)
    evidence: tuple[Evidence, ...] = Field(min_length=1, max_length=96)
    fixture: bool

    @model_validator(mode='after')
    def source_binding(self):
        if self.source_digest != source_set_digest(self.sources):
            raise ValueError('source digest does not match the supplied source resources')
        if {m.source_asset for m in self.recipe.mappings} != {s.asset_id for s in self.sources}:
            raise ValueError('recipe mappings and review sources differ')
        return self

class QASynthesis(Contract):
    finding_ids: tuple[str, ...] = Field(min_length=1)
    decision: Literal['accept', 'revise', 'reject', 'needs_evidence']
    summary: str = Field(min_length=1, max_length=2000)
    # The model has no authority to replace deterministic consensus or human review.
    execution_authorized: Literal[False] = False


def review_metadata(bundle: ReviewBundle, backend, output: Path):
    """Save each accepted result and exact traces; never repair or silently retry JSON.

    All reviewers see the identical frozen recipe. Citations are restricted to
    their curated evidence ledger. Cross-domain discussion references finding IDs.
    """
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    def save(name, value):
        (output/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    save('input.json', bundle.model_dump(mode='json'))
    manifest = RunManifest(run_id=output.name, stage='review', status='blocked',
        code_digest=digest({name: (Path(__file__).parent/name).read_text() for name in
            ('review.py', 'review_contracts.py', 'scoped_review.py')}), input_digest=digest(bundle),
        artifacts=('input.json',), fixture=bundle.fixture, source_data_read=False,
        notes=('Model review cannot grant execution permission.',))
    save('manifest.json', manifest.model_dump(mode='json'))
    reviews = []
    recipe_hash = recipe_content_digest(bundle.recipe)
    try:
        for domain in REQUIRED_DOMAINS:
            ledger = [e.model_dump(mode='json') for e in bundle.evidence if e.domain == domain]
            if not ledger:
                raise ValueError(f'missing curated evidence ledger for {domain.value}')
            instruction = ('Review only your jurisdiction: '+JURISDICTIONS[domain.value]+
                '\nReturn SpecialistReview JSON. Use finding IDs prefixed '+domain.value+
                '. and cite only supplied evidence IDs. Bind recipe_content_digest exactly. '
                'PASS/FAIL/NEEDS_EVIDENCE/NOT_APPLICABLE describe scientific evidence, not workflow votes. '
                'Do not repeat other domains; reference existing finding IDs where relevant. '
                'FAIL needs a documented contradiction; unknowns require NEEDS_EVIDENCE. '
                'No tools, code, formulas, arithmetic, source retrieval or execution. Inspect deterministic check results; never calculate them. Human review is mandatory.')
            # Constrain role and identifier syntax in the deployed JSON Schema too.
            finding_schema = create_model(domain.value.title()+'Finding', __base__=ReviewFinding,
                finding_id=(str, Field(pattern=r'^'+domain.value+r'\.[a-z0-9_.-]{1,90}$')),
                reviewer_domain=(Literal[domain], domain),
                evidence=(tuple[Literal[tuple(item['evidence_id'] for item in ledger)], ...], Field(min_length=1, max_length=16)),
                source=(Literal[tuple(dict.fromkeys(item['source'] for item in ledger))], ...))
            role_schema = create_model(domain.value.title()+'Review', __base__=SpecialistReview,
                reviewer_domain=(Literal[domain], domain),
                recipe_content_digest=(Literal[recipe_hash], recipe_hash),
                findings=(tuple[finding_schema, ...], Field(min_length=1, max_length=16)))
            review = backend.generate(domain.value, instruction, {
                'capabilities': {'registry_version':REGISTRY.manifest()['registry_version'],'operations':[{'operation_id':d['operation_id'],'version':d['version']} for d in REGISTRY.manifest()['operations']]},
                'recipe': bundle.recipe.model_dump(mode='json'), 'recipe_content_digest': recipe_hash,
                'intended_operation': bundle.intended_operation, 'evidence': ledger,
                'previous_findings': [{'finding_id': f.finding_id, 'reviewer_domain': f.reviewer_domain.value,
                    'status': f.status.value} for r in reviews for f in r.findings]}, role_schema)
            if review.reviewer_domain != domain:
                raise ValueError('backend substituted specialist jurisdiction')
            # Validate the partial set before accepting the next specialist.
            synthesize((*reviews, review), bundle.evidence, recipe_content_digest=recipe_hash,
                       source_digest=bundle.source_digest)
            reviews.append(review)
            save(domain.value+'.json', review.model_dump(mode='json'))
        report = synthesize(reviews, bundle.evidence, recipe_content_digest=recipe_hash,
                            source_digest=bundle.source_digest)
        save('report.json', report.model_dump(mode='json'))
        qa = backend.generate('qa', 'Synthesize existing finding IDs only. Do not add scientific claims, '
            'change specialist statuses, or grant execution permission. Return accept, revise, reject, or '
            'needs_evidence for synthesis quality; any veto blocks eligibility. Summarize evidence for human review.',
            report.model_dump(mode='json'), QASynthesis)
        validate_qa_references(report, qa.finding_ids)
        save('qa.json', qa.model_dump(mode='json'))
        state = report.model_consensus
        if qa.decision in ('revise', 'reject'):
            state = 'needs_revision'
        elif qa.decision == 'needs_evidence' and state != 'needs_revision':
            state = 'needs_review'
        report = report.model_copy(update={'model_consensus': state,
            'qa_decision': qa.decision, 'qa_finding_ids': qa.finding_ids})
        save('report.json', report.model_dump(mode='json'))
        save('result.json', {'status': report.model_consensus, 'source_data_read': False,
            'fixture': bundle.fixture, 'execution_authorized': False, 'input_digest': digest(bundle)})
        save('manifest.json', manifest.model_copy(update={'status': 'complete',
            'artifacts': tuple(sorted(p.name for p in output.iterdir()))}).model_dump(mode='json'))
        return report
    except Exception as error:
        save('failure.json', {'error_type': type(error).__name__, 'accepted_reviews': len(reviews),
                              'source_data_read': False, 'execution_authorized': False})
        save('manifest.json', manifest.model_copy(update={'status': 'failed',
            'artifacts': tuple(sorted(p.name for p in output.iterdir()))}).model_dump(mode='json'))
        raise
    finally:
        save('traces.json', [trace.model_dump(mode='json') for trace in backend.traces])
        current = json.loads((output/'manifest.json').read_text())
        current['artifacts'] = sorted(p.name for p in output.iterdir())
        save('manifest.json', current)
