"""Generate accessible, deterministic SVG diagrams from maintained node/edge specs."""
from pathlib import Path
from html import escape

FIGURES = {
 'system': ('From question to scientific use', 'Three independently callable stages; review gates precede source streaming.',
 [('Question',0,0),('Data + semantic discovery',1,0),('Harmonization & review',1,1),('Representation',1,2),('Downstream science',2,2),('Source metadata',0,1),('Human decision',2,1)], [(0,1),(1,2),(5,2),(2,6),(6,3),(3,4)]),
 'discovery': ('Discovery includes semantic evidence', 'Module 1 retrieves sources and preserves semantic evidence. Module 2 alone proposes scientific mappings.',
 [('Scientific request',1,0),('Data discovery',0,1),('Semantic evidence discovery',2,1),('Access / rights / version',0,2),('Ontologies / vocabularies',2,2),('SourceResource + semantics',1,3),('Module 2: interpret / map',1,4)],[(0,1),(0,2),(1,3),(4,2),(2,5),(3,5),(5,6)]),
 'harmonization': ('Harmonization and review', 'Only allow-listed deterministic operations execute after required review and human approval.',
 [('Frozen recipe',0,0),('Scoped specialists',1,0),('QA synthesis',2,0),('Evidence ledger',0,1),('Human decision',1,1),('Deterministic executor',2,1),('Harmonized window',2,2)],[(0,1),(3,1),(1,2),(2,4),(4,5),(5,6)]),
 'representation': ('MOSAIKS over harmonized rasters', 'Training-only reference windows fit filters; held-out windows are encoded with the frozen model.',
 [('Harmonized windows',0,0),('Train-only filter fit',1,0),('Frozen MOSAIKS model',2,0),('Harmonized held-out tiles',0,1),('Window → vector',1,1),('Vectors + lineage',2,1),('Independent verification',2,2)],[(0,1),(1,2),(2,4),(3,4),(4,5),(5,6)]),
 'tracks': ('Shared core, independent tracks', 'Tracks share immutable sources and canonical observations, never mutable interpretation.',
 [('Immutable sources',0,0),('Reviewed core recipes',1,0),('Canonical observations',2,0),('Food security',0,1),('Water security',1,1),('Third track: undefined',2,1)],[(0,1),(1,2),(2,3),(2,4),(2,5)]),
 'provenance': ('Trace a representation back to its source', 'Every representation retains observation lineage, recipes, decisions and source rights.',
 [('Representation',0,0),('Harmonized observation',1,0),('Track recipe, if any',2,0),('Agent + QA + human',0,1),('Transformation / core',1,1),('Source asset',2,1),('Metadata / version / rights',2,2)],[(0,1),(1,2),(2,4),(4,3),(3,5),(5,6)]),
 'semantic-profile': ('Proposed composition of community semantics', 'Provisional profile, not a universal ontology or approved set of mappings.',
 [('I-ADOPT variable structure',1,0),('Biological entities',0,1),('ENVO / SWEET context',1,1),('OBOE / SOSA / BCO',2,1),('RO relationships',1,2),('GeoSPARQL space',0,3),('OWL-Time',1,3),('QUDT / UO units',2,3),('PROV-O lineage',1,4),('Harmonization recipes',1,5)],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4),(4,5),(4,6),(4,7),(5,8),(6,8),(7,8),(8,9)]),
 'evidence-review': ('Evidence and review states', 'Missing evidence differs from demonstrated failure. Eligibility never grants execution permission.',
 [('Domain evidence',0,0),('Typed finding',1,0),('Frozen recipe digest',2,0),('PASS / N/A',0,1),('NEEDS_EVIDENCE',1,1),('FAIL',2,1),('Eligible for human review',0,2),('Needs review',1,2),('Needs revision',2,2)],[(0,1),(2,1),(1,3),(1,4),(1,5),(3,6),(4,7),(5,8)]),
}

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
        parts.extend([f'<rect x="{x}" y="{y}" width="280" height="64" rx="4" fill="white" stroke="#9fb4a5"/>',
          f'<text x="{x+140}" y="{y+38}" text-anchor="middle" fill="#183d34" font-family="sans-serif" font-size="17">{escape(label)}</text>'])
    return '\n'.join(parts+['</svg>'])+'\n'

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]/'docs/assets/figures'
    for name,(title,description,nodes,edges) in FIGURES.items():
        (root/f'{name}.svg').write_text(render(title,description,nodes,edges))
