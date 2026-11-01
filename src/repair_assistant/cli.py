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
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from repair_assistant import __version__
from repair_assistant.agent import MAX_ATTEMPTS, RepairStrategy
from repair_assistant.benchmark import run_benchmark
from repair_assistant.costs import Pricing
from repair_assistant.event_log import EventLog
from repair_assistant.model import DeepSeekAdapter, ModelAdapter
from repair_assistant.output_paths import GROUP_DIRECTORIES, create_output_directory
from repair_assistant.reporting import generate_experiment_report
from repair_assistant.run import RunService
from repair_assistant.task import TaskSpec
from repair_assistant.terminal import format_code_changes


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
    run.add_argument("--model", default=os.getenv("REPAIR_ASSISTANT_MODEL", "deepseek-flash"))
    run.add_argument("--image", default="function-repair/sandbox-python:dev")
    run.add_argument("--data-dir", type=Path, default=_data_dir())
    run.add_argument("--pricing-file", type=Path)
    benchmark = commands.add_parser("benchmark", help="Run all tasks under each strategy.")
    benchmark.add_argument(
        "tasks_dir", type=Path, default=Path("benchmarks/feedbackeval-humaneval"), nargs="?"
    )
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
    benchmark.add_argument("--model", default=os.getenv("REPAIR_ASSISTANT_MODEL", "deepseek-flash"))
    benchmark.add_argument("--image", default="function-repair/sandbox-python:dev")
    benchmark.add_argument("--data-dir", type=Path, default=_data_dir())
    benchmark.add_argument("--pricing-file", type=Path)
    benchmark.add_argument(
        "--resume", type=Path, help="Continue unfinished jobs; skip all saved results."
    )
    events = commands.add_parser("events", help="Read and print an ordinary JSONL event log.")
    events.add_argument("run_id")
    events.add_argument("--data-dir", type=Path, default=_data_dir())
    report = commands.add_parser("report", help="Generate CSV, Markdown, and four SVG figures.")
    report.add_argument("report_json", type=Path)
    report.add_argument("--output-dir", type=Path)
    return parser


def _data_dir() -> Path:
    return Path(os.getenv("REPAIR_ASSISTANT_DATA_DIR", "results"))


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


def _environment_positive_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return _positive_int(value)
    except (argparse.ArgumentTypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a positive integer") from exc


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
    try:
        model = _model_adapter(args.model)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    task = TaskSpec.load(args.task_dir)
    result = RunService(
        data_dir=args.data_dir,
        image=args.image,
        pricing=Pricing.load(args.pricing_file) if args.pricing_file else None,
    ).execute(
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
    summary = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
    print(format_code_changes(result.run_dir, summary, secrets=model.sensitive_values))
    print(f"Summary: {result.run_dir / 'summary.json'}")
    return 0 if result.outcome == "passed" else 1


def _benchmark(args: argparse.Namespace) -> int:
    try:
        _model_adapter(args.model)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    task_paths = sorted(path.parent for path in args.tasks_dir.resolve().glob("*/task.json"))
    if not task_paths:
        print(f"No task manifests found under {args.tasks_dir}", file=sys.stderr)
        return 2
    strategy_values = args.strategies or [item.value for item in RepairStrategy]
    if args.max_attempts != MAX_ATTEMPTS:
        raise ValueError("formal v3 benchmark requires --max-attempts 3 (arms 1/3/3)")
    if len(set(strategy_values)) != len(strategy_values):
        raise ValueError("benchmark strategies must not be repeated")
    if set(strategy_values) != {item.value for item in RepairStrategy}:
        raise ValueError(
            "formal v3 benchmark requires all three strategies; use run for single-arm debugging"
        )
    schedule = _benchmark_schedule(
        task_paths,
        strategy_values,
        repetitions=args.repetitions,
        seed=args.seed,
    )
    experiment_dir = run_benchmark(
        schedule=schedule,
        model_factory=lambda: _model_adapter(args.model),
        image=args.image,
        data_dir=args.data_dir,
        seed=args.seed,
        repetitions=args.repetitions,
        pricing=Pricing.load(args.pricing_file) if args.pricing_file else None,
        resume=args.resume,
    )
    print(f"Report: {experiment_dir / 'report.json'}")
    print(f"Course report: {experiment_dir / 'report.md'}")
    return 0


def _model_adapter(model: str) -> ModelAdapter:
    base_url = os.getenv("REPAIR_ASSISTANT_BASE_URL", "").strip()
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required for a DeepSeek live run.")
    return DeepSeekAdapter(
        api_key=api_key,
        model=model,
        base_url=base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        timeout_seconds=_environment_positive_int("REPAIR_ASSISTANT_MODEL_TIMEOUT_SECONDS", 120),
        max_tokens=_environment_positive_int("REPAIR_ASSISTANT_MAX_TOKENS", 8192),
        ca_bundle=os.getenv("REPAIR_ASSISTANT_CA_BUNDLE"),
    )


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
    root = args.data_dir.resolve() / "runs"
    locations = [root, *(root / group for group in GROUP_DIRECTORIES.values())]
    paths = [base / args.run_id / "events.jsonl" for base in locations]
    found = [path for path in paths if path.is_file()]
    if not found:
        print(f"Run log not found under {root}: {args.run_id}", file=sys.stderr)
        return 2
    if len(found) > 1:
        print("Run log is ambiguous; pass group_a/<run_id> or the matching group.", file=sys.stderr)
        return 2
    path = found[0]
    first = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    events = list(EventLog(path, run_id=first["run_id"], task_id=first["task_id"]).read())
    for event in events:
        print(f"{event['sequence']:03d} {event['occurred_at']} {event['type']}")
    print(f"Events: {len(events)} (ordinary JSONL; no tamper verification)")
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
        output_dir = create_output_directory(report_path.parent / "reports")
    visual_report = generate_experiment_report(data, output_dir)
    print(f"Course report: {visual_report}")
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
