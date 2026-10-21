"""Scientific review and allow-listed deterministic execution, independent of MESA."""
from collections import defaultdict
from datetime import timedelta
from .contracts import (QAReport, HarmonizedObservation, ProvenanceRecord, HarmonizationRecipe, SourceResource, RawObservation, HumanDecision, digest, recipe_content_digest)


def assess(recipe, resources, parent_lineage=()):
    by_id = {r.asset_id: r for r in resources}
    errors, review = [], []
    if recipe.agent_review:
        if recipe.agent_review.recipe_content_digest != recipe_content_digest(recipe):
            errors.append("model QA is stale for this scientific recipe content")
        if recipe.agent_review.outcome in {"reject", "request_revision"}:
            errors.append("model QA veto requires recipe revision and renewed model review")
        elif recipe.agent_review.outcome == "require_human_review":
            review.append("model QA requires human review")
    for m in recipe.mappings:
        r = by_id.get(m.source_asset)
        if r is None:
            errors.append("missing source asset")
            continue
        source = next((v for v in r.variables if v.name == m.source_variable), None)
        if source is None:
            errors.append("missing source variable")
            continue
        for lineage in parent_lineage:
            if lineage.source.asset_id == m.source_asset:
                prior = next((x for x in lineage.recipe.mappings if x.source_asset == m.source_asset and x.source_variable == m.source_variable), None)
                if prior is not None:
                    source = prior.target
        if m.relationship in {"not_comparable", "broader_than", "narrower_than", "associated_with", "measures", "derived_from"}:
            errors.append("relationship does not authorize canonical equivalence")
        if m.relationship in {"unknown", "requires_human_review"} or m.novel or m.confidence < .95 or m.disagreement:
            review.append("uncertain, novel, low-confidence or disputed semantics")
        if not m.evidence or m.review_status == "rejected":
            errors.append("unsupported or rejected semantic mapping")
        if (source.definition, source.measurement_method, source.biological_entity, source.ontology_id) != (m.target.definition, m.target.measurement_method, m.target.biological_entity, m.target.ontology_id):
            review.append("scientific meaning requires expert review")
        if r.rights.derivative_use is False or r.rights.redistribution is False:
            errors.append("source rights prohibit V0 exported derivative products")
        elif r.rights.derivative_use is None or r.rights.redistribution is None or r.rights.access_restrictions != "none":
            review.append("uncertain rights or restricted access")
        selected = [o for o in recipe.operations if o.source_variable == m.source_variable]
        if not selected:
            errors.append("mapping has no explicit operation")
        unit, name = source.unit, source.name
        for o in selected:
            if o.operation == "convert_units":
                if o.from_unit != unit:
                    errors.append("conversion input unit mismatch")
                unit = o.to_unit
            if o.operation == "map_variable":
                name = o.target_variable
        if source.unit != m.target.unit and m.relationship == "equivalent_to":
            errors.append("different units require explicit convertible relationship")
        if (unit, name) != (m.target.unit, m.target.name):
            errors.append("operations do not produce declared target variable/unit")
    for o in recipe.operations:
        if o.source_variable not in {m.source_variable for m in recipe.mappings}:
            errors.append("operation lacks semantic mapping")
        if o.operation in {"temporal_mean", "spatial_match"}:
            review.append("change of temporal/spatial support")
        if o.operation in {"join", "spatial_match"} and o.other_asset not in by_id:
            errors.append("join/match references unavailable source")
        if o.operation == "join":
            review.append("cross-source join requires scientific review")
    outcome = "reject" if errors else "require_human_review" if review else "approve"
    return QAReport(recipe_digest=digest(recipe), outcome=outcome, reasons=tuple(dict.fromkeys(errors + review)))


def authorize(recipe, resources, human=None, parent_lineage=()):
    qa = assess(recipe, resources, parent_lineage)
    if recipe.status != "approved":
        raise ValueError("recipe is not approved")
    if qa.outcome in {"reject", "request_revision"}:
        raise ValueError("QA rejected recipe: " + "; ".join(qa.reasons))
    if human is not None and (human.recipe_digest != digest(recipe) or human.status != "approved"):
        raise ValueError("human decision does not approve this exact recipe")
    if qa.outcome == "require_human_review" and human is None:
        raise ValueError("human review required")
    if any(m.relationship in {"unknown", "requires_human_review"} for m in recipe.mappings):
        raise ValueError("abstention requires a revised explicit semantic mapping, not a blanket approval")
    return qa


def run(resources, recipe, records, human=None, parents=()):
    """Yield immutable observations. Records are supplied by any access adapter.

    Aggregation/joins buffer only their selected inputs in V0; direct scalar
    transformations yield one observation at a time.
    """
    resources = tuple(SourceResource.model_validate(r.model_dump(mode="json")) for r in resources)
    recipe = HarmonizationRecipe.model_validate(recipe.model_dump(mode="json"))
    human = HumanDecision.model_validate(human.model_dump(mode="json")) if human is not None else None
    parents = tuple(HarmonizedObservation.model_validate(p.model_dump(mode="json")) for p in parents)
    qa = authorize(recipe, resources, human, tuple(p.provenance for p in parents))
    by_id = {r.asset_id: r for r in resources}
    parents = tuple(parents)
    if recipe.scope == "track":
        if not parents or any(p.track is not None or p.provenance.recipe.recipe_id != recipe.core_recipe for p in parents):
            raise ValueError("track products require matching immutable core observations")
    records = tuple(RawObservation.model_validate(r.model_dump(mode="json")) for r in records)
    if len({(r.asset_id, r.record_id) for r in records}) != len(records):
        raise ValueError("duplicate source record identities")
    if len({p.observation_id for p in parents}) != len(parents):
        raise ValueError("duplicate canonical parent observations")
    for parent in parents:
        if by_id.get(parent.provenance.source.asset_id) != parent.provenance.source:
            raise ValueError("canonical parent source metadata mismatch")
    for raw in records:
        if raw.asset_id not in by_id:
            raise ValueError("record references unknown source")
        source = by_id[raw.asset_id]
        if raw.variable not in {v.name for v in source.variables}:
            raise ValueError("record variable absent from source metadata")
        if not (source.support.start <= raw.start <= raw.end <= source.support.end):
            raise ValueError("record outside source temporal extent")
        if raw.start == raw.end and source.support.temporal != "instantaneous":
            raise ValueError("zero-duration observation requires instantaneous source support")
        x0, y0, x1, y1 = source.support.bbox
        if not (x0 <= raw.longitude <= x1 and y0 <= raw.latitude <= y1):
            raise ValueError("record outside source spatial extent")
    for mapping in recipe.mappings:
        source = by_id[mapping.source_asset]
        selected = [r for r in records if r.asset_id == source.asset_id and r.variable == mapping.source_variable]
        if recipe.scope == "track":
            rows = []
            for parent in parents:
                if parent.provenance.source.asset_id != source.asset_id or parent.source_variable != mapping.source_variable:
                    continue
                raw = parent.provenance.source_records[0].model_copy(update={"start": parent.datetime_start, "end": parent.datetime_end,
                    "longitude": parent.longitude, "latitude": parent.latitude, "uncertainty": parent.uncertainty, "quality_flag": parent.quality_flag})
                rows.append((raw, parent.value, parent.temporal_support, parent.spatial_support, parent.provenance.source_records, (), ()))
        else:
            rows = [(r, r.value, source.support.temporal, source.support.spatial, (r,), (), ()) for r in selected]
        operations = [o for o in recipe.operations if o.source_variable == mapping.source_variable]
        for op in operations:
            if op.operation == "temporal_mean":
                groups = defaultdict(list)
                for row in rows:
                    r = row[0]
                    day = r.start.replace(hour=0, minute=0, second=0, microsecond=0)
                    if r.end > day + timedelta(days=1):
                        raise ValueError("cannot aggregate an interval crossing a day boundary")
                    groups[(r.longitude, r.latitude, day)].append(row)
                aggregated = []
                for (_, _, day), group in sorted(groups.items()):
                    ordered = sorted(group, key=lambda x: x[0].start)
                    if any(a[0].end > b[0].start for a, b in zip(ordered, ordered[1:])):
                        raise ValueError("overlapping observations cannot form a daily mean")
                    if any(x[1] is None for x in group):
                        raise ValueError("explicitly handle missing values before aggregation")
                    durations = [(x[0].end - x[0].start).total_seconds() for x in group]
                    if sum(durations) != 86400 or ordered[0][0].start != day or ordered[-1][0].end != day + timedelta(days=1):
                        raise ValueError("daily mean requires complete nonoverlapping daily coverage")
                    mean = sum(x[1] * duration for x, duration in zip(group, durations)) / 86400
                    raw = group[0][0].model_copy(update={"start": day, "end": day + timedelta(days=1), "uncertainty": None, "quality_flag": "derived_daily_mean"})
                    originals = tuple(r for x in group for r in x[4])
                    aggregated.append((raw, mean, "daily", group[0][3], originals, (), ()))
                rows = aggregated
                continue
            updated = []
            for raw, value, temporal, spatial, originals, related_sources, related_records in rows:
                if op.operation == "convert_units" and value is not None:
                    scale, offset = {("degC", "K"): (1, 273.15), ("K", "degC"): (1, -273.15), ("cm", "m"): (.01, 0), ("m", "cm"): (100, 0)}[(op.from_unit, op.to_unit)]
                    value = value * scale + offset
                elif op.operation == "missing" and value == op.sentinel:
                    value = None
                elif op.operation == "filter":
                    if value is None or (op.minimum is not None and value < op.minimum) or (op.maximum is not None and value > op.maximum):
                        continue
                elif op.operation == "validate" and value is not None:
                    if (op.minimum is not None and value < op.minimum) or (op.maximum is not None and value > op.maximum):
                        raise ValueError("value failed recipe validation")
                elif op.operation in {"join", "spatial_match"}:
                    candidates = [r for r in records if r.asset_id == op.other_asset and r.start == raw.start and r.end == raw.end]
                    tolerance = 0 if op.operation == "join" else op.tolerance
                    matches = [r for r in candidates if abs(r.longitude - raw.longitude) <= tolerance and abs(r.latitude - raw.latitude) <= tolerance]
                    if len(matches) != 1:
                        raise ValueError("join/match requires exactly one aligned record; ambiguous or unmatched input")
                    other = by_id[op.other_asset]
                    if other.support.spatial != spatial and op.operation == "join":
                        raise ValueError("exact join requires equal observational support")
                    if other.rights.derivative_use is not True or other.rights.redistribution is not True:
                        raise ValueError("joined source rights do not permit export")
                    related_sources += (other,)
                    related_records += tuple(matches)
                    if op.operation == "spatial_match":
                        spatial = op.target_support
                # Coordinate normalization is explicit identity for already valid WGS84 inputs.
                updated.append((raw, value, temporal, spatial, originals, related_sources, related_records))
            rows = updated
        for raw, value, temporal, spatial, originals, related_sources, related_records in rows:
            matching_parents = tuple(p for p in parents if p.provenance.source.asset_id == source.asset_id and {r.record_id for r in p.provenance.source_records} & {r.record_id for r in originals})
            if recipe.scope == "track" and not matching_parents:
                raise ValueError("track observation has no core lineage")
            provenance = ProvenanceRecord(source=source, source_records=originals, recipe=recipe, qa=qa, human=human,
                parent_observations=tuple(p.observation_id for p in matching_parents), parent_lineage=tuple(p.provenance for p in matching_parents),
                context_sources=resources, related_sources=related_sources, related_records=related_records)
            fields = dict(variable=mapping.target.name, value=value, unit=mapping.target.unit, biological_entity=mapping.target.biological_entity,
                measurement_method=mapping.target.measurement_method, longitude=raw.longitude, latitude=raw.latitude, spatial_support=spatial,
                datetime_start=raw.start, datetime_end=raw.end, temporal_support=temporal, dataset=source.dataset,
                source=source.source_id, source_variable=mapping.source_variable, source_version=source.version, modality=source.modality,
                uncertainty=raw.uncertainty if all(o.operation != "convert_units" for o in operations) else None,
                quality_flag=raw.quality_flag, ontology_id=mapping.target.ontology_id, semantic_relationships=(mapping,), track=recipe.track,
                provenance=provenance)
            candidate = HarmonizedObservation(observation_id="pending", **fields)
            yield candidate.model_copy(update={"observation_id": digest(candidate.model_dump(mode="json", exclude={"observation_id"}))})
