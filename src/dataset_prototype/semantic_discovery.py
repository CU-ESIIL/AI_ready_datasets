"""Module 1: preserve declared semantics and retrieve candidates; never approve mappings."""
import json
from .contracts import (SemanticEvidence, SourceSemantics, SourceResource, EvidenceKind, digest)


def source_metadata_digest(source):
    """Bind evidence to the complete pre-enrichment source record, not source raster bytes."""
    return digest(source.model_dump(mode='json', exclude={'semantics'}))


def normalized_evidence(source):
    """Preserve available normalized metadata; do not mislabel adapter prose as native text."""
    rows=[]
    for index, variable in enumerate(source.variables):
        rows.append(SemanticEvidence(source_field=variable.name,
            source_label=variable.name, source_definition=variable.definition,
            unit=variable.unit, method=variable.measurement_method,
            entity_hint=variable.biological_entity, source_concept_id=variable.ontology_id,
            platform=source.metadata.platform, sensor=source.metadata.sensor,
            spatial_support=source.support.spatial, temporal_support=source.support.temporal,
            evidence_type=EvidenceKind.DERIVED_DETERMINISTICALLY,
            evidence_location=f'normalized-source:/variables/{index}',
            source_documentation=source.provenance))
    return tuple(rows)


def stac_evidence(source):
    """Extract only explicit native fields, with source paths. No calibration or variable mapping.

    The band unit describes the documented calibrated quantity, not stored DN.
    Missing fields remain None. STAC common_name is not claimed to be a CF standard name.
    """
    if not source.metadata.native_metadata_json:
        return ()
    native=json.loads(source.metadata.native_metadata_json)
    item=native.get('item', native)
    if 'assets' not in item or 'properties' not in item:
        return ()
    asset=item['assets'].get('nir')
    if asset is None:
        return ()
    band=(asset.get('raster:bands') or [{}])[0]
    eo=(asset.get('eo:bands') or [{}])[0]
    properties=item['properties']
    crs=asset.get('proj:code', item.get('proj:code', properties.get('proj:code')))
    epsg=asset.get('proj:epsg', item.get('proj:epsg', properties.get('proj:epsg')))
    if crs is None and epsg is not None:
        crs=f'EPSG:{epsg}'
    docs=tuple(link['href'] for link in item.get('links',[]) if
               link.get('rel') in {'self','describedby','license'} and isinstance(link.get('href'),str))
    variable=next((v.name for v in source.variables if v.name=='B08_DN'),source.variables[0].name)
    return (SemanticEvidence(source_field=variable,
        source_label=eo.get('common_name', asset.get('title')),
        source_definition=eo.get('description'),
        unit=band.get('unit'), band=eo.get('name'),
        scale=band.get('scale'), offset=band.get('offset'), nodata=band.get('nodata'),
        sensor=','.join(properties['instruments']) if isinstance(properties.get('instruments'),list) else None,
        platform=properties.get('platform'), native_crs=crs,
        spatial_resolution=band.get('spatial_resolution'),
        spatial_resolution_unit='m' if band.get('spatial_resolution') is not None else None,
        # STAC raster:bands spatial_resolution is specified in metres. No inferred temporal duration.
        processing_level=properties.get('s2:product_type'), processing_baseline=properties.get('s2:processing_baseline'),
        source_documentation=docs, evidence_type=EvidenceKind.SOURCE_DOCUMENTED,
        evidence_location='native-stac:/assets/nir; /properties'),
        SemanticEvidence(source_field=variable, evidence_type=EvidenceKind.DERIVED_DETERMINISTICALLY,
            evidence_location='metadata-parser:/stac-raster-conventions',
            source_vocabulary='STAC eo:bands' if eo else None,
            context_hint='Documented raster band unit describes the calibrated quantity, not stored DN; coefficients are not executed here',
            source_documentation=('https://github.com/stac-extensions/raster/tree/v1.1.0',)))


def enrich(source: SourceResource, registry=None):
    """Return a new source with evidence. Existing annotations are never overwritten."""
    source=SourceResource.model_validate(source.model_dump(mode='json'))
    expected=source_metadata_digest(source)
    if source.semantics is not None:
        if source.semantics.source_metadata_digest != expected:
            raise ValueError('semantic evidence is bound to different source metadata')
        return source
    evidence=(*normalized_evidence(source), *stac_evidence(source))
    candidates=[]
    if registry is not None:
        for item in evidence:
            identifier=item.source_concept_uri or item.source_concept_id or item.taxon_identifier
            if identifier:
                candidates.extend(registry.candidates(item, identifier=identifier))
            elif item.source_label:
                candidates.extend(registry.candidates(item))
    semantics=SourceSemantics(evidence=evidence,candidates=tuple(candidates),
        extractor='source-semantic-evidence-v1',source_metadata_digest=expected)
    return source.model_copy(update={'semantics':semantics})
