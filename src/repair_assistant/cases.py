"""Collect pytest case outcomes inside the existing sandbox, never on the host."""

from __future__ import annotations

import ast
import shlex
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from pathlib import Path
from uuid import uuid4

from repair_assistant.sandbox import Sandbox
from repair_assistant.types import CommandResult


def declared_cases(directory: Path) -> tuple[str, ...]:
    """Read test syntax without importing tests or candidate implementations."""
    names = []
    for path in sorted(directory.rglob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            # Parametrized/external suites are reported at their observed granularity.
            if (
                isinstance(node, ast.FunctionDef)
                and node.name.startswith("test_")
                and not node.decorator_list
            ):
                names.append(f"{path.stem}::{node.name}")
    return tuple(names)


def parse_junit(source: str) -> dict[str, str]:
    root = ET.fromstring(source)
    if root.tag not in {"testsuites", "testsuite"}:
        raise ValueError("not a pytest JUnit report")
    cases: dict[str, str] = {}
    for case in root.iter("testcase"):
        module = case.get("classname", "").rsplit(".", 1)[-1]
        name = case.get("name", "unknown")
        key = f"{module}::{name}"
        if key in cases:
            raise ValueError(f"duplicate JUnit case: {key}")
        status = "passed"
        for tag, outcome in (("skipped", "not_run"), ("failure", "failed"), ("error", "error")):
            if case.find(tag) is not None:
                status = outcome
        cases[key] = status
    return cases


def execute_cases(
    sandbox: Sandbox,
    command: str,
    *,
    expected: tuple[str, ...],
    timeout_seconds: int,
) -> tuple[CommandResult, dict[str, str], bool]:
    report_path = f"/tmp/repair-cases-{uuid4().hex}.xml"
    options = shlex.quote(f"-p no:cacheprovider --junitxml={report_path}")
    result = sandbox.execute(f"PYTEST_ADDOPTS={options} {command}", timeout_seconds=timeout_seconds)
    report = sandbox.execute(f"cat {shlex.quote(report_path)}", timeout_seconds=10)
    cases: dict[str, str] = {}
    complete = False
    if report.exit_code == 0:
        try:
            cases = parse_junit(report.stdout)
            complete = bool(cases) and all(name in cases for name in expected)
        except (ET.ParseError, ValueError):
            pass
    missing = "timeout" if result.timed_out else "error" if result.exit_code == 2 else "not_run"
    for name in expected:
        cases.setdefault(name, missing)
    if not cases:
        cases["__suite__"] = missing
    return result, cases, complete and not result.timed_out


def compare_cases(before: Mapping[str, str], after: Mapping[str, str]) -> dict[str, int]:
    comparable = {"passed", "failed"}
    common = before.keys() & after.keys()
    fixed = sum(before[k] == "failed" and after[k] == "passed" for k in common)
    regressed = sum(before[k] == "passed" and after[k] == "failed" for k in common)
    unavailable = sum(
        before.get(k) not in comparable or after.get(k) not in comparable
        for k in before.keys() | after.keys()
    )
    return {
        "fixed": fixed,
        "regressed": regressed,
        "net_improvement": fixed - regressed,
        "unavailable": unavailable,
    }
