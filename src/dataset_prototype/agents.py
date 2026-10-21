"""Bounded, deterministic local stand-ins for future OpenClaw workers."""
from .contracts import SemanticMapping, Proposal, HarmonizationRecipe, Operation
from . import discovery


class DiscoveryAgent:
    def propose(self, request, client):
        return discovery.run(request, client)


class SemanticAgent:
    def propose(self, resource, source_variable, target):
        source = next(v for v in resource.variables if v.name == source_variable)
        # Deliberately conservative: names are not compared as evidence.
        meaning = (source.definition, source.measurement_method, source.biological_entity, source.ontology_id)
        desired = (target.definition, target.measurement_method, target.biological_entity, target.ontology_id)
        if meaning == desired and source.unit == target.unit:
            relation, confidence = "equivalent_to", 1.0
        elif meaning == desired and (source.unit, target.unit) in {("degC", "K"), ("K", "degC"), ("cm", "m"), ("m", "cm")}:
            relation, confidence = "convertible_to", 1.0
        else:
            relation, confidence = "unknown", 0.0
        return SemanticMapping(source_asset=resource.asset_id, source_variable=source_variable, target=target,
                               relationship=relation, evidence=("Compared explicit definition, method, entity, ontology and units against curated fixture target", resource.metadata.original_identifier), confidence=confidence)


class HarmonizationAgent:
    def propose(self, mappings, operations, *, scope="core", track=None, core_recipe=None):
        return HarmonizationRecipe(recipe_id=f"{track or 'core'}-fixture", version="1", scope=scope,
            track=track, core_recipe=core_recipe, mappings=tuple(mappings), operations=tuple(operations),
            proposals=(Proposal(role="semantic", rationale="Curated metadata comparison; abstain on unknown meaning", evidence=tuple(m.source_asset for m in mappings)),
                       Proposal(role="harmonization", rationale="Propose explicit allow-listed operations; no execution permission", evidence=tuple(m.source_asset for m in mappings))), author="fixture-maintainer")


class QAAgent:
    def assess(self, recipe, resources):
        from .harmonization import assess
        return assess(recipe, resources)
