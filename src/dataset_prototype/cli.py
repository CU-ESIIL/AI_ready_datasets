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
    benchmark = sub.add_parser("semantic-benchmark")
    benchmark.add_argument("--inventory", type=Path, default=Path("data/semantics/semantic_resources.csv"))
    benchmark.add_argument("--sources", type=Path, action="append")
    benchmark.add_argument("--output", type=Path, default=Path("outputs/semantic_benchmark"))
    benchmark.add_argument("--budget", type=int, default=8)
    semantics = sub.add_parser("discover-semantics")
    semantics.add_argument("source", type=Path)
    semantics.add_argument("--output", type=Path, required=True)
    scoped = sub.add_parser("review-metadata")
    scoped.add_argument("bundle", type=Path)
    scoped.add_argument("--runtime", type=Path, default=Path("run/openclaw"))
    scoped.add_argument("--output", type=Path, required=True)
    mosaic_plan = sub.add_parser("mosaiks-plan")
    mosaic_plan.add_argument("plan", type=Path)
    mosaic_plan.add_argument("spec", type=Path)
    mosaic_plan.add_argument("--side", type=int, default=16)
    mosaic_plan.add_argument("--grid", type=int, default=8)
    mosaic_plan.add_argument("--output", type=Path, required=True)
    mosaiks = sub.add_parser("mosaiks-run")
    mosaiks.add_argument("context", type=Path)
    mosaiks.add_argument("spec", type=Path)
    mosaiks.add_argument("--output", type=Path, required=True)
    mosaiks.add_argument("--side", type=int, default=16)
    mosaiks.add_argument("--grid", type=int, default=8)
    verification = sub.add_parser("mosaiks-verify")
    verification.add_argument("dataset", type=Path)
    verification.add_argument("--output", type=Path, required=True)
    demo = sub.add_parser("mosaiks-demo")
    demo.add_argument("--output", type=Path, required=True)
    runner = sub.add_parser("run")
    runner.add_argument("--track", default="food_security")
    runner.add_argument("--all-tracks", action="store_true")
    runner.add_argument("--config", type=Path)
    runner.add_argument("--fixtures", type=Path, default=Path("data/fixtures"))
    runner.add_argument("--output", type=Path, default=Path("run"))
    runner.add_argument("--cache", type=Path, default=Path(".cache/prototype"))
    plan = sub.add_parser("plan-stream")
    plan.add_argument("request", type=Path)
    plan.add_argument("--longitude", type=float, required=True)
    plan.add_argument("--latitude", type=float, required=True)
    plan.add_argument("--max-items", type=int, default=2)
    plan.add_argument("--output", type=Path, required=True)
    consensus = sub.add_parser("consensus")
    consensus.add_argument("plan", type=Path)
    consensus.add_argument("--runtime", type=Path, default=Path("run/openclaw"))
    consensus.add_argument("--max-rounds", type=int, default=2)
    consensus.add_argument("--analysis-from", type=Path)
    consensus.add_argument("--output", type=Path, required=True)
    stream = sub.add_parser("stream-embed")
    stream.add_argument("plan", type=Path)
    stream.add_argument("recipe", type=Path)
    stream.add_argument("--review", type=Path)
    stream.add_argument("--evidence-review", type=Path)
    stream.add_argument("--consensus", type=Path, required=True)
    stream.add_argument("--output", type=Path, required=True)
    acquire = sub.add_parser("acquire-sentinel")
    acquire.add_argument("request", type=Path)
    acquire.add_argument("--longitude", type=float, required=True)
    acquire.add_argument("--latitude", type=float, required=True)
    acquire.add_argument("--max-cloud", type=float, default=20)
    acquire.add_argument("--max-items", type=int, default=5)
    acquire.add_argument("--output", type=Path, required=True)
    propose = sub.add_parser("propose")
    propose.add_argument("snapshot", type=Path)
    propose.add_argument("--backend", choices=["ollama", "openclaw"], default="ollama")
    propose.add_argument("--model")
    propose.add_argument("--runtime", type=Path, default=Path("run/openclaw"))
    propose.add_argument("--endpoint", default="http://127.0.0.1:11434")
    propose.add_argument("--output", type=Path, required=True)
    runtime = sub.add_parser("openclaw")
    runtime.add_argument("action", choices=["start", "status", "stop"])
    runtime.add_argument("--verde-env", type=Path)
    runtime.add_argument("--runtime", type=Path, default=Path("run/openclaw"))
    runtime.add_argument("--image", default="openclaw-local:latest")
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
    schema.add_argument("contract", choices=["ScientificRequest", "SourceResource", "DiscoveryResult", "SemanticMapping", "HarmonizationRecipe", "HarmonizedObservation", "Representation", "ProvenanceRecord", "HumanDecision", "TrackConfig", "StreamPlan", "StreamSample", "EncoderSpec", "ConsensusReport", "MOSAIKSSpec", "RasterContext", "RasterLayout", "ReviewFinding", "ReviewReport", "RunManifest", "Evidence", "SpecialistReview", "ReviewBundle", "SemanticEvidence", "ConceptCandidate", "SourceSemantics"])
    schema.add_argument("--output", type=Path, required=True)
    cube_demo = sub.add_parser("cubedynamics-demo")
    cube_demo.add_argument("--output",type=Path,required=True)
    capability = sub.add_parser("operation-capabilities")
    capability.add_argument("--output",type=Path,required=True)
    demo = sub.add_parser("operation-demo")
    demo.add_argument("--output",type=Path,required=True)
    ir = sub.add_parser("ir-validate")
    ir.add_argument("decision",type=Path)
    ir.add_argument("sources",type=Path)
    ir.add_argument("mappings",type=Path)
    ir.add_argument("--output",type=Path,required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "cubedynamics-demo":
            from .cube_demo import run as cube_demo
            result,report=cube_demo(args.output)
            print(f"{result['records']} generated windows; real CubeDynamics → MOSAIKS; see verification.json")
        elif args.command == "operation-capabilities":
            from .operations import REGISTRY
            write(args.output,REGISTRY.manifest())
        elif args.command == "operation-demo":
            from .operation_demo import run as operation_demo
            result=operation_demo(args.output)
            print(f"{result['status']}; generated fixture result {result['result']}; no live model/source read")
        elif args.command == "ir-validate":
            from .decision_ir import build_capabilities,process_output
            sources=tuple(contracts.SourceResource.model_validate(x) for x in json.loads(args.sources.read_text()))
            mappings=tuple(contracts.SemanticMapping.model_validate(x) for x in json.loads(args.mappings.read_text()))
            result=process_output(args.decision.read_text(),build_capabilities(sources,mappings),sources,mappings)
            write(args.output,result.model_dump(mode='json'))
            print(result.status)
        elif args.command == "semantic-benchmark":
            from .semantic_benchmark import run as benchmark_run, BenchmarkConfig
            paths = args.sources or [Path("data/fixtures/catalog.json"), Path("data/fixtures/semantics/sentinel_source.json")]
            result = benchmark_run(args.inventory, paths, args.output, config=BenchmarkConfig(portfolio_budget=args.budget))
            print(f"{args.output}: {result['resource_count']} resources; {result['source_count']} source records; project metadata diagnostics only")
        elif args.command == "discover-semantics":
            from .semantic_discovery import enrich
            result = enrich(contracts.SourceResource.model_validate_json(args.source.read_text()))
            write(args.output, result.model_dump(mode="json"))
            print(f"{args.output}: semantic evidence only; no equivalence approved; no source data read")
        elif args.command == "review-metadata":
            from .scoped_review import ReviewBundle, review_metadata
            from .openclaw_backend import OpenClawBackend
            result = review_metadata(ReviewBundle.model_validate_json(args.bundle.read_text()),
                                     OpenClawBackend(args.runtime), args.output)
            print(f"{result.model_consensus}; human review pending; no source data read")
        elif args.command == "mosaiks-plan":
            from .stream_contracts import StreamPlan
            from .mosaiks import MOSAIKSSpec
            from .mosaiks_pipeline import RasterLayout,plan_rasters
            result=plan_rasters(StreamPlan.model_validate_json(args.plan.read_text()),MOSAIKSSpec.model_validate_json(args.spec.read_text()),RasterLayout(side=args.side,grid=args.grid))
            write(args.output,result.model_dump(mode="json"))
            print(f"{args.output}: new layout and MOSAIKS configuration need fresh consensus; no source reads")
        elif args.command == "mosaiks-run":
            from .harmonized_rasters import RasterContext, authorize_context
            from .mosaiks import MOSAIKSSpec
            from .stream_rasters import sentinel_harmonized_tiles
            from .mosaiks_pipeline import run as vectorize
            context=authorize_context(RasterContext.model_validate_json(args.context.read_text()))
            spec=MOSAIKSSpec.model_validate_json(args.spec.read_text())
            result=vectorize(sentinel_harmonized_tiles(context,side=args.side,grid=args.grid),context,spec,args.output)
            print(f"{result['records']} MOSAIKS vectors from harmonization outputs: {args.output}")
        elif args.command == "mosaiks-verify":
            from .embedding_dataset import verify_dataset
            print(json.dumps(verify_dataset(args.dataset,args.output),indent=2))
        elif args.command == "mosaiks-demo":
            from .mosaiks_pipeline import demo
            manifest,report=demo(args.output)
            print(json.dumps({'generated_diagnostic_only':True,'vectors':manifest['records'],'verification':report},indent=2))
        elif args.command == "run":
            paths = [Path("tracks") / name / "config.json" for name in ("food_security", "water_security")] if args.all_tracks else [args.config or Path("tracks") / args.track / "config.json"]
            for path in paths:
                print(run(load_track(path), MockMESAClient(args.fixtures), args.output, args.cache))
        elif args.command == "plan-stream":
            from .stream_sources import plan_sentinel
            request = contracts.ScientificRequest.model_validate_json(args.request.read_text())
            plan = plan_sentinel(request, args.longitude, args.latitude, max_items=args.max_items)
            write(args.output, plan.model_dump(mode="json"))
            print(f"{args.output}: metadata only; no raster data read")
        elif args.command == "consensus":
            from .stream_contracts import StreamPlan
            from .consensus import negotiate
            from .openclaw_backend import OpenClawBackend
            plan = StreamPlan.model_validate_json(args.plan.read_text())
            result = negotiate(plan, OpenClawBackend(args.runtime), args.output, max_rounds=args.max_rounds, analysis_from=args.analysis_from)
            print(f"{result.status}: {args.output}; human approval still required")
        elif args.command == "stream-embed":
            from .stream_contracts import StreamPlan, ConsensusReport
            from .stream_sources import sentinel_samples
            from .streaming import stream_embed
            plan = StreamPlan.model_validate_json(args.plan.read_text())
            recipe = contracts.HarmonizationRecipe.model_validate_json(args.recipe.read_text())
            human = contracts.HumanDecision.model_validate_json(args.review.read_text()) if args.review else None
            consensus = ConsensusReport.model_validate_json(args.consensus.read_text())
            from .review_contracts import ReviewReport
            scoped_report = ReviewReport.model_validate_json(args.evidence_review.read_text()) if args.evidence_review else None
            result = stream_embed(plan, recipe, sentinel_samples(plan), args.output, human=human, consensus=consensus, evidence_review=scoped_report)
            print(f"{result['records']} streamed reference vectors: {args.output}")
        elif args.command == "acquire-sentinel":
            from .real_data import acquire_sentinel
            request = contracts.ScientificRequest.model_validate_json(args.request.read_text())
            snapshot = acquire_sentinel(request, args.longitude, args.latitude, args.output, max_cloud=args.max_cloud, max_items=args.max_items)
            print(f"{args.output}: {len(snapshot.records)} actual source observations")
        elif args.command == "propose":
            from .model_agents import OllamaBackend, propose_snapshot
            if args.backend == "openclaw":
                if args.model:
                    raise ValueError("OpenClaw model is fixed by the verified runtime; do not override it per call")
                from .openclaw_backend import OpenClawBackend
                backend = OpenClawBackend(args.runtime)
            else:
                if not args.model: raise ValueError("--model is required for the Ollama backend")
                backend = OllamaBackend(args.model, endpoint=args.endpoint)
            print(propose_snapshot(args.snapshot, args.output, backend))
        elif args.command == "openclaw":
            from .openclaw_runtime import start_runtime, stop_runtime, runtime_status
            if args.action == "start":
                if not args.verde_env: raise ValueError("--verde-env must identify a trusted configured env file")
                info = start_runtime(args.verde_env, args.runtime, args.image)
                print(json.dumps({k: info[k] for k in ["container", "endpoint", "provider", "model", "openclaw_version"]}, indent=2))
            elif args.action == "stop":
                stop_runtime()
                print("Isolated prototype OpenClaw container stopped; artifacts retained")
            else:
                print(json.dumps(runtime_status(args.runtime), indent=2))
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
            from . import stream_contracts
            if args.contract=='MOSAIKSSpec':
                from . import mosaiks as module
            elif args.contract=='RasterContext':
                from . import harmonized_rasters as module
            elif args.contract=='RasterLayout':
                from . import mosaiks_pipeline as module
            elif args.contract in {'ReviewFinding', 'ReviewReport', 'RunManifest', 'Evidence', 'SpecialistReview'}:
                from . import review_contracts as module
            elif args.contract == 'ReviewBundle':
                from . import scoped_review as module
            else:module = contracts if hasattr(contracts, args.contract) else stream_contracts
            write(args.output, getattr(module, args.contract).model_json_schema())
    except (ValueError, OSError, LookupError, NotImplementedError) as error:
        parser.exit(2, f"{args.command}: {error}\n")


if __name__ == "__main__":
    main()
