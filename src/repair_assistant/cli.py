"""Command-line interface for controlled runs and log inspection."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from repair_assistant import __version__
from repair_assistant.agent import RepairStrategy
from repair_assistant.evaluation import aggregate_summaries
from repair_assistant.event_log import EventLog
from repair_assistant.model import DeepSeekAdapter
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
    run.add_argument("--max-attempts", type=int, default=3)
    run.add_argument("--max-turns", type=int, default=12)
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
    benchmark.add_argument("--max-attempts", type=int, default=3)
    benchmark.add_argument("--max-turns", type=int, default=12)
    benchmark.add_argument("--model", default=os.getenv("REPAIR_ASSISTANT_MODEL", "deepseek-chat"))
    benchmark.add_argument("--image", default="function-repair/sandbox-python:dev")
    benchmark.add_argument("--data-dir", type=Path, default=_data_dir())
    events = commands.add_parser("events", help="Verify and print an event log.")
    events.add_argument("run_id")
    events.add_argument("--data-dir", type=Path, default=_data_dir())
    return parser


def _data_dir() -> Path:
    return Path(os.getenv("REPAIR_ASSISTANT_DATA_DIR", "var"))


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
    )
    result = RunService(data_dir=args.data_dir, image=args.image).execute(
        task=task,
        model=model,
        strategy=RepairStrategy(args.strategy),
        max_attempts=args.max_attempts,
        max_turns_per_attempt=args.max_turns,
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
    summaries: list[dict[str, object]] = []
    service = RunService(data_dir=args.data_dir, image=args.image)
    for strategy_value in strategy_values:
        for task_path in task_paths:
            task = TaskSpec.load(task_path)
            model = DeepSeekAdapter(
                api_key=api_key,
                model=args.model,
                base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            )
            result = service.execute(
                task=task,
                model=model,
                strategy=RepairStrategy(strategy_value),
                max_attempts=args.max_attempts,
                max_turns_per_attempt=args.max_turns,
            )
            summary = json.loads((result.run_dir / "summary.json").read_text(encoding="utf-8"))
            summary["task_id"] = task.task_id
            summaries.append(summary)
            print(f"{strategy_value:24} {task.task_id:28} {result.outcome}")
    report = aggregate_summaries(summaries)
    report["created_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    report["raw_runs"] = summaries
    report_dir = args.data_dir.resolve() / "benchmarks"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"benchmark-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Report: {report_path}")
    return 0


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
    raise AssertionError(f"unhandled command: {args.command}")
