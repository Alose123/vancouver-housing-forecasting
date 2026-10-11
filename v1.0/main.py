"""Start, inspect, or resume one persisted Stage 1 demonstration."""
import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
from pathlib import Path
import platform
import sys
from uuid import uuid4
from src.agents.backends import DemoBackend, OpenAIBackend
from src.config import Config
from src.orchestrator import Orchestrator
from src.state import WorkflowState
from src.storage import RunStore, bootstrap_demo, create_once


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=["run", "resume", "status", "stage2", "stage2-review", "stage3", "stage4", "stage5", "stage6", "stage7", "stage8"], default="run")
    parser.add_argument("--run-dir", type=Path, default=Path("outputs/demo-run"))
    parser.add_argument("--backend", choices=["demo", "openai"], default="demo")
    parser.add_argument("--choice", help="An exact alternative from the pending review packet.")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    if args.command == "stage8":
        from src.regimes.freeze import verify_numeric
        from src.regimes.storage import verify_prior
        project=Path(__file__).resolve().parent
        state=RunStore(project/'outputs/stage8').load()
        print(json.dumps({'workflow_status':state.workflow_status,'stage8_complete':state.dataset_metadata.get('stage8_complete',False),
                         'numeric_freeze':verify_numeric(project),'preserved_files':verify_prior(project),'stage9_allowed':False},indent=2))
        return
    if args.command == "stage7":
        from src.holdout.workflow import inspect
        print(json.dumps(inspect(Path(__file__).resolve().parent), indent=2))
        return
    if args.command == "stage6":
        from src.enhanced.workflow import inspect
        print(json.dumps(inspect(Path(__file__).resolve().parent), indent=2))
        return
    if args.command == "stage5":
        from src.forecasting.workflow import inspect
        print(json.dumps(inspect(Path(__file__).resolve().parent), indent=2))
        return
    if args.command == "stage4":
        from src.design.workflow import inspect
        print(json.dumps(inspect(Path(__file__).resolve().parent), indent=2))
        return
    if args.command == "stage3":
        from src.audit.workflow import inspect
        print(json.dumps(inspect(Path(__file__).resolve().parent), indent=2))
        return
    if args.command in {"stage2", "stage2-review"}:
        from src.acquisition.workflow import inspect, record_decision
        project = Path(__file__).resolve().parent
        if args.command == "stage2-review":
            if not args.choice or not args.reason:
                parser.error("stage2-review requires --choice and --reason")
            result = record_decision(project,args.choice,args.reason)
        else:
            result = inspect(project)
        print(json.dumps(result,indent=2))
        return
    store = RunStore(args.run_dir)
    if args.command == "status":
        print(json.dumps(store.load().to_dict(), indent=2))
        return
    with store.lock():
        config = Config()
        if store.checkpoint.exists():
            state = store.load()
            if state.dataset_metadata.get("workflow_stage") in {2, 3, 4, 5, 6, 7, 8}:
                parser.error("Use the stage2–stage8 inspection commands; Stage 1 run/resume is prohibited for real-data audit checkpoints.")
            recorded = json.loads((store.root / "environment.json").read_text())
            if recorded["config"] != config.to_dict():
                raise ValueError("Runtime rules differ from the recorded experiment.")
        else:
            if args.command == "resume":
                parser.error("Cannot resume a run that does not exist.")
            bootstrap_demo(store)
            state = WorkflowState(run_id=str(uuid4()), backend=args.backend)
            store.save(state)
            packages = {}
            try:
                packages["openai"] = metadata.version("openai")
            except metadata.PackageNotFoundError:
                pass
            create_once(store.root / "environment.json", json.dumps({
                "python": sys.version, "platform": platform.platform(), "packages": packages,
                "config": config.to_dict(), "backend": args.backend,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }, indent=2))
        backend = DemoBackend() if args.backend == "demo" else OpenAIBackend()
        engine = Orchestrator(state, store, backend, config)
        if args.command == "resume":
            if not args.choice or not args.reason:
                parser.error("resume requires --choice and --reason")
            engine.resume(args.choice, args.reason)
        else:
            engine.run()
    print(f"Status: {state.workflow_status}; current node: {state.current_agent}")
    if state.pending_review:
        print(json.dumps(state.pending_review, indent=2))
        print("Use main.py resume --choice <alternative> --reason '<your justification>'.")
    else:
        print(f"Checkpoint and artifacts: {store.root}")


if __name__ == "__main__":
    main()
