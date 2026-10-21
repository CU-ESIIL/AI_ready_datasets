"""Render canonical inventory and auditable project assessments as readable Markdown."""
from pathlib import Path
import json
from dataset_prototype.semantic_resources import load_inventory,COVERAGE_DIMENSIONS,ResourceAssessment,load_assessments
ROOT=Path(__file__).resolve().parents[1]

def safe(value):return str(value or 'Not established').replace('|',' / ').replace('\n',' ')

def main():
    source=ROOT/'data/semantics';target=ROOT/'docs/semantics';target.mkdir(exist_ok=True)
    resources=load_inventory(source/'semantic_resources.csv')
    assessments=load_assessments(source/'assessments.jsonl', resources)
    if {r.resource_id for r in resources}!={a.resource_id for a in assessments}:raise ValueError('assessment/resource coverage mismatch')
    for name in ('semantic_resources.csv','assessments.jsonl','namespace_bindings.json','verification_sources.json'):
        (target/name).write_bytes((source/name).read_bytes())
    lines=['# Ontology and semantic-resource landscape','',
      f'A growing landscape inventory of **{len(resources)} resources**, not an exhaustive list or an adoption decision. '
      'Formal and application ontologies, standards, classifications, thesauri, frameworks and historical efforts serve different purposes.','',
      'The canonical CSV lives in `data/semantics/semantic_resources.csv`. This page and the '
      '[coverage matrix](comparison.md) are generated with `python scripts/generate_semantics.py`. '
      '[Download every inventory field](semantic_resources.csv), [auditable project assessments](assessments.jsonl) or [inspected registry fact evidence](verification_sources.json).','',
      'Resource identities, registry status and cited documentation are **resource facts** with a verification scope. '
      'Coverage, candidate roles, eras, limitations and influence are **provisional project assessments** '
      'by the coding assistant, not expert-reviewed ontology properties. Unknown release dates/rights stay unknown. '
      'A milestone below is not necessarily the first release; eras overlap.','',
      '!!! note "Do not collapse distinctions"\n    '
      '[Organism, taxon, population and community](distinctions.md) describe different things. '
      'An ontology, vocabulary and exchange standard are also different kinds of resource. '
      '[Scale is not one dimension](scale-support.md).','',
      '## Master inventory','',
      '| Resource | Kind / domain | Era and origin/milestone | Contribution (project reading) | Project role | Verification |',
      '| --- | --- | --- | --- | --- | --- |']
    for r in resources:
        lines.append(f'| [{safe(r.name)}](#{r.resource_id}) | `{r.resource_type}` / {safe(r.domain)} | {safe(r.era)}; {safe(r.first_release_or_origin)} | {safe(r.key_contribution)} | {safe(r.project_role)} | {r.verification_scope} |')
    lines+=['','## Resource details, limitations and evidence','',
      'An empty crosswalk/dependency field means **not recorded in this review**, not that none exists. '
      'Registry dependency metadata is not a parsed OWL-import graph. Resolvable identifiers mean '
      'the source declares persistent identifiers; live resolution of every term was not tested. '
      'Portal APIs are not assumed from a downloadable OWL file.','']
    for r in resources:
        lines.extend([f'### {r.name} {{ #{r.resource_id} }}','',
          f'**Identity and status:** {r.acronym}; `{r.resource_type}`; {r.status}.',
          f'**Milestone / era:** {r.first_release_or_origin}; {r.era}.',
          f'**Maintainer evidence:** {r.maintainer}.',
          f'**Original problem / contribution (project reading):** {r.problem_originally_addressed}.',
          f'**Relationship to prior work:** {r.relationship_to_prior_work}.',
          f'**Historical role:** {r.historical_role}.',
          f'**Current relevance:** {r.current_relevance}.',
          f'**Does not establish:** {r.limitations}.',
          f'**Access / format:** {r.machine_access}; {r.format}.',
          f'**License:** {safe(r.license)}. This record is not a blanket redistribution permission.',
          f'**Dependencies recorded:** {", ".join(r.imports_or_dependencies) or "Not recorded"}. '
          f'**Crosswalks recorded:** {", ".join(r.known_crosswalks) or "Not recorded"}.',
          f'**Evidence:** '+', '.join(f'[source {i+1}]({uri})' for i,uri in enumerate(r.evidence_source))+'.',
          f'**Canonical resource link:** '+(f'[resource]({r.canonical_uri})' if r.canonical_uri else 'Unresolved; no URI invented')+'.',
          f'**Verification:** {r.verification_scope}; last verified {r.last_verified or "not established"}. '
          f'Assessment `{r.assessment_id}`, coding-assistant, 2026-10-21; expert review pending.',''])
    (target/'landscape.md').write_text('\n'.join(lines))
    short={'molecular':'Molecule','cellular':'Cell','taxonomy':'Taxon','scale_support':'Scale/support'}
    legend={'strong':'S','partial':'P','indirect':'I','not_target':'—','unknown':'?'}
    lines=['# Semantic resource comparison','',
      'This matrix compares **assessed scope**, not term counts, logical quality or scientific compatibility. '
      '**S** strong target; **P** partial target; **I** indirect support through a general model; '
      '**—** not a target of this assessed use; **?** identity/scope not sufficiently established. '
      'Ratings are project judgments with [reviewer/evidence records](assessments.jsonl).','',
      'Unknown is not failure. A dash does not prove absence of every relevant term. '
      'Read the [limitations and evidence](landscape.md#resource-details-limitations-and-evidence) before selecting a resource. '
      'The source CSV retains the complete enum values.','',
      '<div class="semantic-matrix" markdown>','',
      '| Resource | '+' | '.join(short.get(k,k.replace('_',' ').title()) for k in COVERAGE_DIMENSIONS)+' |',
      '| '+' | '.join(['---']*(len(COVERAGE_DIMENSIONS)+1))+' |']
    for r in resources:
        lines.append('| ['+r.acronym+'](landscape.md#'+r.resource_id+') | '+' | '.join(legend[r.coverage[k]] for k in COVERAGE_DIMENSIONS)+' |')
    lines+=['','</div>','',
      '## Compare unlike systems with care','',
      'PCO describes organism groups; GeoSPARQL describes geographic geometry and relations. '
      'QUDT addresses quantities/units; PROV-O records derivation. Their assessed overlap '
      'does not make them substitutes. I-ADOPT supplies variable structure while domain '
      'resources supply component meanings. Compare versions, definitions, entity types, '
      'relations and support using the [human workflow](review-workflow.md).','',
      '## Diagnostic benchmark','',
      'The [benchmark guide](benchmark.md) defines all Parquet outputs, scoring formulas '
      'and limits. No ontology graph is loaded and no crosswalk is approved.','']
    (target/'comparison.md').write_text('\n'.join(lines))

if __name__=='__main__':main()
