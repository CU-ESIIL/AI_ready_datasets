"""Thin composition of discovery, harmonization and representation modules."""
from pathlib import Path
import json
from .contracts import ScientificRequest, TrackConfig, Operation, RawObservation, HarmonizedObservation
from .adapters import MockMESAClient
from .agents import DiscoveryAgent, SemanticAgent, HarmonizationAgent, QAAgent
from . import harmonization, representations, provenance
from .storage import cached


def load_track(path):
    return TrackConfig.model_validate_json(Path(path).read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def run(config: TrackConfig, client, output: Path, cache: Path):
    if not config.enabled:
        raise ValueError("track scientific scope not finalized; track is disabled")
    request = ScientificRequest(question=config.question, support=config.support, variables=config.variables,
                                modalities=config.modalities, track=config.track)
    discovery = DiscoveryAgent().propose(request, client)
    resources = tuple(c.resource for c in discovery.candidates)
    if not resources:
        raise ValueError("discovery returned no resources")
    found = {v.name for r in resources for v in r.variables}
    if not set(config.variables) <= found:
        raise ValueError("discovery lacks required track variables")
    cache_refs = []
    records = []
    for resource in resources:
        saved, key = cached(cache, {"kind": "source", "source": resource.model_dump(mode="json")},
                            lambda: [r.model_dump(mode="json") for r in client.fetch(resource.asset_id)])
        records.extend(RawObservation.model_validate(r) for r in saved)
        cache_refs.append(key)
    semantic = SemanticAgent()
    mappings = tuple(semantic.propose(r, v.name, v) for r in resources for v in r.variables if v.name in config.variables)
    agent = HarmonizationAgent()
    operations = tuple(Operation(operation="validate", source_variable=m.source_variable) for m in mappings)
    proposed = agent.propose(mappings, operations)
    qa = QAAgent().assess(proposed, resources)
    if qa.outcome != "approve":
        raise ValueError("core fixture proposal needs review")
    core = proposed.model_copy(update={"status": "approved"})
    saved, key = cached(cache, {"kind": "core", "sources": [r.model_dump(mode="json") for r in resources],
                               "recipe": core.model_dump(mode="json"), "executor": "allowlist-v2"},
                        lambda: [o.model_dump(mode="json") for o in harmonization.run(resources, core, records)])
    canonical = tuple(HarmonizedObservation.model_validate(o) for o in saved)
    cache_refs.append(key)
    # V0 tracks only select declared variables; they encode no food/water model.
    track_proposal = agent.propose(mappings, operations, scope="track", track=config.track, core_recipe=core.recipe_id)
    track_recipe = track_proposal.model_copy(update={"status": "approved"})
    observations = tuple(harmonization.run(resources, track_recipe, records, parents=canonical))
    vectors = tuple(representations.run(iter(observations), config.encoder))
    target = Path(output) / config.track
    target.mkdir(parents=True, exist_ok=False)
    artifacts = {
        "request.json": request.model_dump(mode="json"), "sources.json": [r.model_dump(mode="json") for r in resources],
        "proposed_recipe.json": {"core": proposed.model_dump(mode="json"), "track": track_proposal.model_dump(mode="json")},
        "qa_report.json": {"core": QAAgent().assess(core, resources).model_dump(mode="json"), "track": QAAgent().assess(track_recipe, resources).model_dump(mode="json")},
        "review.json": {"status": "approved", "mechanism": "deterministic QA for conservative fixture identity mappings", "human": None},
        "approved_recipe.json": {"core": core.model_dump(mode="json"), "track": track_recipe.model_dump(mode="json")},
        "harmonized.json": [o.model_dump(mode="json") for o in observations], "representations.json": [r.model_dump(mode="json") for r in vectors],
        "provenance.jsonld": provenance.export(vectors),
    }
    from .science import summarize
    artifacts["downstream.json"] = summarize(observations)
    from .contracts import digest
    import sys
    from importlib.metadata import version
    code_hash = digest({p.name: p.read_text() for p in sorted(Path(__file__).parent.glob("*.py"))})
    manifest = {"code_hash": code_hash, "python": sys.version, "dependencies": {"pydantic": version("pydantic")}, "prototype_version": "0.1.0", "executor": "allowlist-v2", "fixture": all(r.metadata.fixture for r in resources),
                "track": config.model_dump(mode="json"), "cache_keys": cache_refs,
                "artifacts": {name: digest(value) for name, value in artifacts.items()},
                "reproduce": "prototype run --config <saved-track-config.json> --output <new-directory> --cache <cache-directory>"}
    for name, value in artifacts.items():
        write(target / name, value)
    write(target / "run_manifest.json", manifest)
    return target
