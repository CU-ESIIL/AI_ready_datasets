"""CLI for reproducible fixture runs, independent stages, schema and review."""
import argparse
import json
from pathlib import Path
from . import contracts
from .adapters import MockMESAClient
from .orchestration import load_track, run, write


def main(argv=None):
    parser = argparse.ArgumentParser(prog="prototype")
    sub = parser.add_subparsers(dest="command", required=True)
    runner = sub.add_parser("run")
    runner.add_argument("--track", default="food_security")
    runner.add_argument("--all-tracks", action="store_true")
    runner.add_argument("--config", type=Path)
    runner.add_argument("--fixtures", type=Path, default=Path("data/fixtures"))
    runner.add_argument("--output", type=Path, default=Path("run"))
    runner.add_argument("--cache", type=Path, default=Path(".cache/prototype"))
    acquire = sub.add_parser("acquire-sentinel")
    acquire.add_argument("request", type=Path)
    acquire.add_argument("--longitude", type=float, required=True)
    acquire.add_argument("--latitude", type=float, required=True)
    acquire.add_argument("--max-cloud", type=float, default=20)
    acquire.add_argument("--max-items", type=int, default=5)
    acquire.add_argument("--output", type=Path, required=True)
    propose = sub.add_parser("propose")
    propose.add_argument("snapshot", type=Path)
    propose.add_argument("--model", required=True)
    propose.add_argument("--endpoint", default="http://127.0.0.1:11434")
    propose.add_argument("--output", type=Path, required=True)
    neon = sub.add_parser("neon-files")
    neon.add_argument("--product", required=True)
    neon.add_argument("--site", required=True)
    neon.add_argument("--month", required=True)
    neon.add_argument("--release", required=True)
    neon.add_argument("--filename")
    neon.add_argument("--output", type=Path, required=True)
    discovery = sub.add_parser("discover")
    discovery.add_argument("request", type=Path)
    discovery.add_argument("--fixtures", type=Path, default=Path("data/fixtures"))
    discovery.add_argument("--output", type=Path, required=True)
    executor = sub.add_parser("harmonize")
    executor.add_argument("recipe", type=Path)
    executor.add_argument("sources", type=Path)
    executor.add_argument("records", type=Path)
    executor.add_argument("--review", type=Path)
    executor.add_argument("--parents", type=Path)
    executor.add_argument("--output", type=Path, required=True)
    encoder = sub.add_parser("encode")
    encoder.add_argument("observations", type=Path)
    encoder.add_argument("--encoder", choices=["scalar", "squared"], default="scalar")
    encoder.add_argument("--output", type=Path, required=True)
    qa = sub.add_parser("qa")
    qa.add_argument("recipe", type=Path)
    qa.add_argument("sources", type=Path)
    qa.add_argument("--output", type=Path, required=True)
    review = sub.add_parser("review")
    review.add_argument("recipe", type=Path)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--rationale", required=True)
    review.add_argument("--decision", choices=["approved", "rejected"], required=True)
    review.add_argument("--output", type=Path, required=True)
    schema = sub.add_parser("schema")
    schema.add_argument("contract", choices=["ScientificRequest", "SourceResource", "DiscoveryResult", "SemanticMapping", "HarmonizationRecipe", "HarmonizedObservation", "Representation", "ProvenanceRecord", "HumanDecision", "TrackConfig"])
    schema.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            paths = [Path("tracks") / name / "config.json" for name in ("food_security", "water_security")] if args.all_tracks else [args.config or Path("tracks") / args.track / "config.json"]
            for path in paths:
                print(run(load_track(path), MockMESAClient(args.fixtures), args.output, args.cache))
        elif args.command == "acquire-sentinel":
            from .real_data import acquire_sentinel
            request = contracts.ScientificRequest.model_validate_json(args.request.read_text())
            snapshot = acquire_sentinel(request, args.longitude, args.latitude, args.output, max_cloud=args.max_cloud, max_items=args.max_items)
            print(f"{args.output}: {len(snapshot.records)} actual source observations")
        elif args.command == "propose":
            from .model_agents import OllamaBackend, propose_snapshot
            print(propose_snapshot(args.snapshot, args.output, OllamaBackend(args.model, endpoint=args.endpoint)))
        elif args.command == "neon-files":
            from .neon import NEONClient
            client = NEONClient()
            if args.filename:
                client.acquire_file(args.product, args.site, args.month, args.release, args.filename, args.output)
            else:
                write(args.output, client.files(args.product, args.site, args.month, args.release))
        elif args.command == "discover":
            from .discovery import run as discover
            request = contracts.ScientificRequest.model_validate_json(args.request.read_text())
            write(args.output, discover(request, MockMESAClient(args.fixtures)).model_dump(mode="json"))
        elif args.command == "harmonize":
            from .harmonization import run as execute
            recipe = contracts.HarmonizationRecipe.model_validate_json(args.recipe.read_text())
            sources = tuple(contracts.SourceResource.model_validate(r) for r in json.loads(args.sources.read_text()))
            records = tuple(contracts.RawObservation.model_validate(r) for r in json.loads(args.records.read_text()))
            review = contracts.HumanDecision.model_validate_json(args.review.read_text()) if args.review else None
            parents = tuple(contracts.HarmonizedObservation.model_validate(r) for r in json.loads(args.parents.read_text())) if args.parents else ()
            write(args.output, [o.model_dump(mode="json") for o in execute(sources, recipe, records, review, parents)])
        elif args.command == "encode":
            from .representations import run as encode
            observations = (contracts.HarmonizedObservation.model_validate(r) for r in json.loads(args.observations.read_text()))
            write(args.output, [r.model_dump(mode="json") for r in encode(observations, args.encoder)])
        elif args.command == "qa":
            from .harmonization import assess
            recipe = contracts.HarmonizationRecipe.model_validate_json(args.recipe.read_text())
            sources = tuple(contracts.SourceResource.model_validate(r) for r in json.loads(args.sources.read_text()))
            write(args.output, assess(recipe, sources).model_dump(mode="json"))
        elif args.command == "review":
            from datetime import datetime, timezone
            recipe = contracts.HarmonizationRecipe.model_validate_json(args.recipe.read_text())
            decision = contracts.HumanDecision(recipe_digest=contracts.digest(recipe), status=args.decision, reviewer=args.reviewer, rationale=args.rationale, timestamp=datetime.now(timezone.utc))
            write(args.output, decision.model_dump(mode="json"))
        else:
            write(args.output, getattr(contracts, args.contract).model_json_schema())
    except (ValueError, OSError, LookupError, NotImplementedError) as error:
        parser.exit(2, f"{args.command}: {error}\n")


if __name__ == "__main__":
    main()
