"""Generate accessible, deterministic SVG diagrams from maintained node/edge specs."""
from pathlib import Path
from html import escape
from textwrap import wrap

FIGURES = {
 'system': ('From question to scientific use', 'Three independently callable stages; review gates precede source streaming.',
 [('Question',0,0),('Data + semantic discovery',1,0),('Harmonization & review',1,1),('Representation',1,2),('Downstream science',2,2),('Source metadata',0,1),('Human decision',2,1)], [(0,1),(1,2),(5,2),(2,6),(6,3),(3,4)]),
 'discovery': ('Discovery includes semantic evidence', 'Module 1 retrieves sources and preserves semantic evidence. Module 2 alone proposes scientific mappings.',
 [('Scientific request',1,0),('Data discovery',0,1),('Semantic evidence discovery',2,1),('Access / rights / version',0,2),('Ontologies / vocabularies',2,2),('SourceResource + semantics',1,3),('Module 2: interpret / map',1,4)],[(0,1),(0,2),(1,3),(4,2),(2,5),(3,5),(5,6)]),
 'harmonization': ('Harmonization and review', 'Only allow-listed deterministic operations execute after required review and human approval.',
 [('Frozen recipe',0,0),('Scoped specialists',1,0),('QA synthesis',2,0),('Evidence ledger',0,1),('Human decision',1,1),('Deterministic executor',2,1),('Harmonized window',2,2)],[(0,1),(3,1),(1,2),(2,4),(4,5),(5,6)]),
 'representation': ('MOSAIKS over harmonized rasters', 'Training-only reference windows fit filters; held-out windows are encoded with the frozen model.',
 [('Harmonized windows',0,0),('Train-only filter fit',1,0),('Frozen MOSAIKS model',2,0),('Harmonized held-out tiles',0,1),('Window → vector',1,1),('Vectors + lineage',2,1),('Held-out checks + baselines',2,2)],[(0,1),(1,2),(2,4),(3,4),(4,5),(5,6)]),
 'tracks': ('Shared core, independent tracks', 'Tracks share immutable sources and canonical observations, never mutable interpretation.',
 [('Immutable sources',0,0),('Reviewed core recipes',1,0),('Canonical observations',2,0),('Food security',0,1),('Water security',1,1),('Third track: undefined',2,1)],[(0,1),(1,2),(2,3),(2,4),(2,5)]),
 'provenance': ('Trace a representation back to its source', 'Every representation retains observation lineage, recipes, decisions and source rights.',
 [('Representation',0,0),('Harmonized observation',1,0),('Track recipe, if any',2,0),('Agent + QA + human',0,1),('Transformation / core',1,1),('Source asset',2,1),('Metadata / version / rights',2,2)],[(0,1),(1,2),(2,4),(4,3),(3,5),(5,6)]),
 'semantic-profile': ('Proposed composition of community semantics', 'Provisional profile, not a universal ontology or approved set of mappings.',
 [('I-ADOPT variable structure',1,0),('Biological entities',0,1),('ENVO / SWEET context',1,1),('OBOE / SOSA / BCO',2,1),('RO relationships',1,2),('GeoSPARQL space',0,3),('OWL-Time',1,3),('QUDT / UO units',2,3),('PROV-O lineage',1,4),('Harmonization recipes',1,5)],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(4,5),(4,6),(4,7),(5,8),(6,8),(7,8),(8,9)]),
 'evidence-review': ('Evidence and review states', 'Missing evidence differs from demonstrated failure. Eligibility never grants execution permission.',
 [('Domain evidence',0,0),('Typed finding',1,0),('Frozen recipe digest',2,0),('PASS / N/A',0,1),('NEEDS_EVIDENCE',1,1),('FAIL',2,1),('Eligible for human review',0,2),('Needs review',1,2),('Needs revision',2,2)],[(0,1),(2,1),(1,3),(1,4),(1,5),(3,6),(4,7),(5,8)]),
}

# Conceptual research figures carry status in their visible titles and descriptions.
FIGURES.update({
 'system': ('From scientific question to synthesis', 'Architecture and intended semantic work; capability status is documented beside the figure.',
 [('Scientific question',1,0),('Data discovery',0,1),('Semantic discovery',2,1),('SourceResource + evidence',1,2),('Mapping / comparison',0,3),('Evidence review',2,3),('Harmonization recipe',1,4),('Deterministic execution',1,5),('Harmonized observations',1,6),('Representation → vectors',1,7),('Synthesis science',1,8),('Community semantic systems',0,2),('QA + human decision',2,4)],
 [(0,1),(0,2),(1,3),(2,3),(11,2),(11,4),(3,4),(3,5),(4,6),(5,12),(6,12),(12,7),(7,8),(8,9),(9,10)]),
 'biological-organization': ('Intersecting organizations of biology', 'Conceptual perspectives, not a universal ladder. No shared is-a or containment relation is asserted.',
 [('Structural: cell / organ',0,0),('Ecological: population / community',1,0),('Taxonomic: species / genus ranks',2,0),('Space: plot / site / landscape',0,1),('Time: instant / interval / year',1,1),('Observation: sample / event',2,1),('Functional / trophic groups',0,2),('Genomic relationships',1,2),('Environmental / experimental',2,2),('Explicit relations + support',1,3)], [(i,9) for i in range(9)]),
 'semantic-landscape': ('Many systems, complementary responsibilities', 'Conceptual families represented in the local inventory; no automatic mappings or universal ontology.',
 [('Biology: PCO / OBA / PATO',0,0),('Environment: ENVO / SWEET',1,0),('Observation: OBOE / SOSA',2,0),('Variable structure: I-ADOPT',0,1),('Relations: RO',1,1),('Taxon identity: NCBITaxon',2,1),('Space / time / units',0,2),('Provenance: PROV-O',1,2),('Community standards',2,2),('Candidate composition + review',1,3)],[(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9)]),
 'semantic-mapping': ('Compare scientific meaning before mapping', 'Conceptual review workflow. Full automated decomposition and ontology alignment are planned.',
 [('Source variable A',0,0),('Compare definitions',1,0),('Source variable B',2,0),('Entity / property / taxon',0,1),('Biological level / matrix',1,1),('Entity / property / taxon',2,1),('Method / unit / environment',0,2),('Compare context',1,2),('Method / unit / environment',2,2),('Space / time / support',0,3),('Provenance / evidence',1,3),('Space / time / support',2,3),('Equivalent / convertible?',0,4),('Broader / narrower / derived?',1,4),('Related / incomparable / unknown?',2,4),('Evidence + confidence + review',1,5)],[(0,1),(2,1),(0,3),(2,5),(3,6),(5,8),(6,9),(8,11),(9,10),(11,10),(10,12),(10,13),(10,14),(12,15),(13,15),(14,15)]),
 'ontology-analysis': ('Ontology analysis — research framework', 'Planned graph and observation-level analysis; existing output measures assessed inventory coverage only.',
 [('Breadth: semantic dimensions',0,0),('Depth: hierarchy / relations',1,0),('Depth: annotation detail',2,0),('Overlap: shared meanings?',0,1),('Complementarity: added meaning?',1,1),('Composability: compatible links?',2,1),('Canonical observation tests',1,2),('Evidence + gaps + human review',1,3)],[(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,7)]),
 'ontology-accumulation': ('Ontology accumulation — proposed experiment', 'Conceptual alternatives, not plotted results. Compare added resources against complete observation meaning.',
 [('Add semantic resources',1,0),('Assess additional coverage',1,1),('Early saturation?',0,2),('Long-tail contributions?',2,2),('Versioned evidence + uncertainty',1,3)],[(0,1),(1,2),(1,3),(2,4),(3,4)]),
 'dataset-framework': ('Dataset semantics — three distinct questions', 'Conceptual profiles. Current metadata-field presence does not compute potential or diversity.',
 [('Explicit use: declared IDs',0,0),('Potential: recoverable meaning',1,0),('Diversity: distinct dimensions',2,0),('Inspect source annotations',0,1),('Inspect definitions / methods',1,1),('Inspect entities / supports',2,1),('Evidence-quality profile',1,2),('Human-selected demonstration',1,3)],[(0,3),(1,4),(2,5),(3,6),(4,6),(5,6),(6,7)]),
 'semantic-history': ('Semantic capabilities accumulate', 'Conceptual progression, not strict chronology. These capabilities coexist and recur across communities.',
 [('Name things',1,0),('Describe datasets',1,1),('Formalize entities',1,2),('Formalize relationships',1,3),('Formalize observations',1,4),('Formalize methods',1,5),('Connect domains',1,6),('Compose meaning',1,7),('Preserve lineage',1,8),('Orchestrate semantic systems',1,9)],[(i,i+1) for i in range(9)]),
 'provenance': ('Trace vectors back to source semantic evidence', 'Backward audit traversal, not execution order. Actual provenance branches and retains rejected history separately.',
 [('Representation + model identity',1,0),('Harmonized observation / window',1,1),('Track recipe, if applicable',1,2),('Core recipe + transformation',1,3),('Agent proposal + QA findings',1,4),('Human decision, when required',1,5),('Mapping + candidate concepts',1,6),('Source semantic evidence',1,7),('Source asset + metadata',1,8),('Version / license / native support',1,9)],[(i,i+1) for i in range(9)]),
})

def quadrant():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 620" role="img" aria-labelledby="title desc">
<title id="title">Dataset selection — conceptual framework</title><desc id="desc">Ontology potential vertically, semantic diversity horizontally. No dataset positions or scores have been measured here.</desc>
<rect width="960" height="620" rx="8" fill="#f3f5ef"/>
<g font-family="sans-serif" fill="#173e35" text-anchor="middle">
<text x="480" y="40" font-size="23">Dataset selection — conceptual framework</text>
<path d="M120 310H840 M480 110V520" stroke="#547568" stroke-width="2"/>
<text x="480" y="85" font-size="18">High ontology potential ↑</text>
<text x="480" y="560" font-size="18">Low ontology potential</text>
<text x="250" y="290" font-size="17">Low semantic diversity</text><text x="710" y="290" font-size="17">High semantic diversity →</text>
<text x="250" y="190" font-size="21">Easy benchmarks</text><text x="710" y="190" font-size="21">Ideal flagship candidates</text>
<text x="250" y="430" font-size="21">Low priority for this objective</text><text x="710" y="430" font-size="21">Hard but interesting</text>
<text x="480" y="600" font-size="16">No real dataset placements; suitability depends on question, rights and evidence.</text>
</g></svg>''' + '\n'

def render(title, description, nodes, edges):
    width, height = 960, 118 + 125*(1+max(n[2] for n in nodes))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>',
      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#547568"/></marker></defs>',
      f'<rect width="{width}" height="{height}" fill="#f3f5ef" rx="8"/>',
      f'<text x="28" y="38" fill="#173e35" font-family="sans-serif" font-size="23" font-weight="600">{escape(title)}</text>']
    for a,b in edges:
        _,ax,ay=nodes[a];_,bx,by=nodes[b]
        x1,y1=30+310*ax+140,85+125*ay+32
        x2,y2=30+310*bx+140,85+125*by+32
        if ay==by:
            x1+=140 if bx>ax else -140;x2-=140 if bx>ax else -140
        else:y1+=32 if by>ay else -32;y2-=32 if by>ay else -32
        parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="#547568" stroke-width="2" marker-end="url(#arrow)"/>')
    for label,col,row in nodes:
        x,y=30+310*col,85+125*row
        label_lines=wrap(label, width=30, break_long_words=False)
        text_lines=''.join(f'<tspan x="{x+140}" dy="{0 if i==0 else 20}">{escape(line)}</tspan>' for i,line in enumerate(label_lines))
        parts.extend([f'<rect x="{x}" y="{y}" width="280" height="64" rx="4" fill="white" stroke="#9fb4a5"/>',
          f'<text x="{x+140}" y="{y+38-10*(len(label_lines)-1)}" text-anchor="middle" fill="#183d34" font-family="sans-serif" font-size="17">{text_lines}</text>'])
    return '\n'.join(parts+['</svg>'])+'\n'

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]/'docs/assets/figures'
    for name,(title,description,nodes,edges) in FIGURES.items():
        (root/f'{name}.svg').write_text(render(title,description,nodes,edges))

    (root/'dataset-quadrant.svg').write_text(quadrant())
