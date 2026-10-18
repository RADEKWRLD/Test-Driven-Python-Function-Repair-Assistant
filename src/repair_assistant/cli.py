"""Command-line interface for controlled runs and log inspection."""

from __future__ import annotations

import argparse
import json
import os
import platform
import random
import shutil
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from repair_assistant import __version__
from repair_assistant.agent import MAX_ATTEMPTS, RepairStrategy
from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.event_log import EventLog
from repair_assistant.model import DeepSeekAdapter
from repair_assistant.reporting import generate_experiment_report
from repair_assistant.run import RunService
from repair_assistant.task import TaskSpec


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repair-agent")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="Check Python, Docker CLI, daemon, and image.")
    run = commands.add_parser("run", help="Run one controlled function-repair task.")
    run.add_argument("task_dir", type=Path)
    run.add_argument(
        "--strategy",
        choices=[item.value for item in RepairStrategy],
        default=RepairStrategy.TEST_FEEDBACK.value,
    )
    run.add_argument("--max-attempts", type=_attempt_count, default=MAX_ATTEMPTS)
    run.add_argument("--model", default=os.getenv("REPAIR_ASSISTANT_MODEL", "deepseek-chat"))
    run.add_argument("--image", default="function-repair/sandbox-python:dev")
    run.add_argument("--data-dir", type=Path, default=_data_dir())
    benchmark = commands.add_parser("benchmark", help="Run all tasks under each strategy.")
    benchmark.add_argument("tasks_dir", type=Path, default=Path("benchmarks/tasks"), nargs="?")
    benchmark.add_argument(
        "--strategy",
        action="append",
        choices=[item.value for item in RepairStrategy],
        dest="strategies",
    )
    benchmark.add_argument("--max-attempts", type=_attempt_count, default=MAX_ATTEMPTS)
    benchmark.add_argument(
        "--repetitions",
        type=_positive_int,
        default=1,
        help="Repeat every task/strategy pair this many times.",
    )
    benchmark.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Seed used to randomize benchmark execution order.",
    )
    benchmark.add_argument("--model", default=os.getenv("REPAIR_ASSISTANT_MODEL", "deepseek-chat"))
    benchmark.add_argument("--image", default="function-repair/sandbox-python:dev")
    benchmark.add_argument("--data-dir", type=Path, default=_data_dir())
    events = commands.add_parser("events", help="Verify and print an event log.")
    events.add_argument("run_id")
    events.add_argument("--data-dir", type=Path, default=_data_dir())
    report = commands.add_parser("report", help="Generate SVG, CSV, HTML, and Markdown reports.")
    report.add_argument("report_json", type=Path)
    report.add_argument("--output-dir", type=Path)
    return parser


def _data_dir() -> Path:
    return Path(os.getenv("REPAIR_ASSISTANT_DATA_DIR", "var"))


def _attempt_count(value: str) -> int:
    parsed = int(value)
    if not 1 <= parsed <= MAX_ATTEMPTS:
        raise argparse.ArgumentTypeError(f"must be from 1 to {MAX_ATTEMPTS}")
    return parsed


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return parsed


def _load_environment() -> None:
    discovered = find_dotenv(usecwd=True)
    if discovered:
        load_dotenv(discovered, override=False)


def _doctor() -> int:
    print(f"Repair Assistant {__version__}")
    print(f"Python: {platform.python_version()}")
    docker = shutil.which("docker")
    print(f"Docker CLI: {docker or 'not found'}")
    if not docker:
        return 1
    try:
        daemon = subprocess.run(
            [docker, "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        image = subprocess.run(
            [docker, "image", "inspect", "function-repair/sandbox-python:dev"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        print("Docker daemon: timeout")
        return 1
    print(f"Docker daemon: {daemon.stdout.strip() or daemon.stderr.strip()}")
    print(f"Sandbox image: {'ready' if image.returncode == 0 else 'not built'}")
    return 0 if daemon.returncode == 0 and image.returncode == 0 else 1


def _run(args: argparse.Namespace) -> int:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("DEEPSEEK_API_KEY is required for a live run.", file=sys.stderr)
        return 2
    task = TaskSpec.load(args.task_dir)
    model = DeepSeekAdapter(
        api_key=api_key,
        model=args.model,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        ca_bundle=os.getenv("REPAIR_ASSISTANT_CA_BUNDLE"),
    )
    result = RunService(data_dir=args.data_dir, image=args.image).execute(
        task=task,
        model=model,
        strategy=RepairStrategy(args.strategy),
        max_attempts=args.max_attempts,
    )
    print(f"Run: {result.run_id}")
    print(f"Outcome: {result.outcome.upper()}")
    print(f"Attempts: {len(result.agent.attempts)}")
    print(f"First hidden: {'PASS' if result.first_hidden.passed else 'FAIL'}")
    print(f"Final hidden: {'PASS' if result.final_hidden.passed else 'FAIL'}")
    print(f"Summary: {result.run_dir / 'summary.json'}")
    return 0 if result.outcome == "passed" else 1


def _benchmark(args: argparse.Namespace) -> int:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("DEEPSEEK_API_KEY is required for a live benchmark.", file=sys.stderr)
        return 2
    task_paths = sorted(path.parent for path in args.tasks_dir.resolve().glob("*/task.json"))
    if not task_paths:
        print(f"No task manifests found under {args.tasks_dir}", file=sys.stderr)
        return 2
    strategy_values = args.strategies or [item.value for item in RepairStrategy]
    schedule = _benchmark_schedule(
        task_paths,
        strategy_values,
        repetitions=args.repetitions,
        seed=args.seed,
    )
    summaries: list[dict[str, object]] = []
    service = RunService(data_dir=args.data_dir, image=args.image)
    execution_order: list[dict[str, object]] = []
    for repetition, strategy_value, task_path in schedule:
        task = TaskSpec.load(task_path)
        model = DeepSeekAdapter(
            api_key=api_key,
            model=args.model,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            ca_bundle=os.getenv("REPAIR_ASSISTANT_CA_BUNDLE"),
        )
        result = service.execute(
            task=task,
            model=model,
            strategy=RepairStrategy(strategy_value),
            max_attempts=args.max_attempts,
        )
        summary = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
        summary["task_id"] = task.task_id
        summary["repetition"] = repetition
        summaries.append(summary)
        execution_order.append(
            {
                "position": len(execution_order) + 1,
                "repetition": repetition,
                "strategy": strategy_value,
                "task_id": task.task_id,
                "run_id": result.run_id,
            }
        )
        print(f"r{repetition:02d} {strategy_value:24} {task.task_id:28} {result.outcome}")
    report = aggregate_summaries(summaries)
    created_at = datetime.now(UTC)
    report["created_at"] = created_at.isoformat().replace("+00:00", "Z")
    report["design"] = {
        "repair_protocol": "shared-public-test-stopping-v2",
        "repetitions": args.repetitions,
        "randomization_seed": args.seed,
        "max_attempts": args.max_attempts,
        "model_calls_per_attempt": 1,
        "execution_order": execution_order,
    }
    report["raw_runs"] = summaries
    report_root = args.data_dir.resolve() / "benchmarks"
    experiment_dir = report_root / f"benchmark-{created_at.strftime('%Y%m%dT%H%M%S%fZ')}"
    experiment_dir.mkdir(parents=True, exist_ok=False)
    report_path = experiment_dir / "report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    visual_report = generate_experiment_report(report, experiment_dir)
    print(f"Report: {report_path}")
    print(f"Visual report: {visual_report}")
    return 0


def _benchmark_schedule(
    task_paths: Sequence[Path],
    strategy_values: Sequence[str],
    *,
    repetitions: int,
    seed: int,
) -> list[tuple[int, str, Path]]:
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    jobs = [
        (repetition, strategy, task_path)
        for repetition in range(1, repetitions + 1)
        for strategy in strategy_values
        for task_path in task_paths
    ]
    random.Random(seed).shuffle(jobs)
    return jobs


def _events(args: argparse.Namespace) -> int:
    path = args.data_dir.resolve() / "runs" / args.run_id / "events.jsonl"
    if not path.exists():
        print(f"Run log not found: {path}", file=sys.stderr)
        return 2
    first = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    events = list(EventLog(path, run_id=first["run_id"], task_id=first["task_id"]).read())
    for event in events:
        print(f"{event['sequence']:03d} {event['occurred_at']} {event['type']}")
    print(f"Integrity: OK ({len(events)} events)")
    return 0


def _report(args: argparse.Namespace) -> int:
    report_path = args.report_json.resolve()
    if not report_path.is_file():
        print(f"Benchmark report not found: {report_path}", file=sys.stderr)
        return 2
    data = json.loads(report_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("raw_runs"), list):
        print("The input is not a benchmark report with raw_runs.", file=sys.stderr)
        return 2
    if args.output_dir is not None:
        output_dir = args.output_dir
    elif report_path.name == "report.json":
        output_dir = report_path.parent
    else:
        output_dir = report_path.parent / f"{report_path.stem}-visuals"
    visual_report = generate_experiment_report(data, output_dir)
    print(f"Visual report: {visual_report}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    _load_environment()
    args = _parser().parse_args(argv)
    if args.command == "doctor":
        return _doctor()
    if args.command == "run":
        return _run(args)
    if args.command == "benchmark":
        return _benchmark(args)
    if args.command == "events":
        return _events(args)
    if args.command == "report":
        return _report(args)
    raise AssertionError(f"unhandled command: {args.command}")
