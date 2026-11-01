#!/usr/bin/env python3
"""Build all 164 FeedbackEval HumanEval tasks with HumanEval+ hidden tests."""

from __future__ import annotations

import argparse
import base64
import copy
import gzip
import hashlib
import json
import pickle
import pprint
import re
import shutil
import sys
import textwrap
import zlib
from pathlib import Path
from typing import Any

FEEDBACKEVAL_COMMIT = "bd8d8aefbc2319e9fdab5b1b85091b0665a48e50"
EVALPLUS_VERSION = "v0.1.10"
PLATFORM_UNSTABLE_INPUTS = {"HumanEval/32": {285}}

sys.set_int_max_str_digits(0)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as source:
            return [json.loads(line) for line in source if line.strip()]
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _numeric_id(value: object) -> int:
    return int(str(value).rsplit("/", 1)[-1])


def _public_pytest(test_source: str, entry_point: str) -> str:
    ending = re.compile(rf"\n\s*check\(\s*{re.escape(entry_point)}\s*\)\s*$")
    definitions, replacements = ending.subn("", test_source.rstrip(), count=1)
    if replacements != 1:
        raise ValueError(f"public test does not end with check({entry_point})")
    return (
        "from solution import *  # noqa: F403\n\n"
        f"{definitions.strip()}\n\n\n"
        "def test_public_suite():\n"
        f"    check({entry_point})  # noqa: F405\n"
    )


def _reference_outputs(problem: dict[str, Any], inputs: list[Any]) -> list[Any]:
    namespace: dict[str, Any] = {}
    exec(str(problem["prompt"]) + str(problem["canonical_solution"]), namespace)
    function = namespace[str(problem["entry_point"])]
    return [function(*copy.deepcopy(arguments)) for arguments in inputs]


def _curated_inputs(problem: dict[str, Any]) -> tuple[list[Any], int]:
    inputs = list(problem["base_input"]) + list(problem["plus_input"])
    if str(problem["entry_point"]) != "find_zero":
        return inputs, 0

    namespace: dict[str, Any] = {}
    exec(str(problem["prompt"]) + str(problem["canonical_solution"]), namespace)
    candidate = namespace["find_zero"]
    polynomial = namespace["poly"]
    atol = float(problem["atol"])
    valid = []
    excluded_indices = PLATFORM_UNSTABLE_INPUTS.get(str(problem["task_id"]), set())
    for index, arguments in enumerate(inputs):
        if index in excluded_indices:
            continue
        output = candidate(*copy.deepcopy(arguments))
        if abs(polynomial(*arguments, output)) <= atol:
            valid.append(arguments)
    return valid, len(inputs) - len(valid)


def _compressed_outputs(outputs: list[Any]) -> str:
    payload = base64.b85encode(zlib.compress(pickle.dumps(outputs, protocol=5), level=9)).decode()
    chunks = textwrap.wrap(payload, width=100)
    encoded = "\n".join(f"    b{chunk!r}" for chunk in chunks)
    return f"EXPECTED = pickle.loads(zlib.decompress(base64.b85decode(\n{encoded}\n)))\n"


def _is_float_output(value: Any) -> bool:
    if isinstance(value, float):
        return True
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(isinstance(item, float) for item in value)
    )


def _framed(payload: bytes) -> bytes:
    return len(payload).to_bytes(8, "big") + payload


def _stable_output_bytes(value: Any) -> bytes:
    if value is None:
        return b"n"
    if isinstance(value, bool):
        return b"b1" if value else b"b0"
    if isinstance(value, int):
        magnitude = abs(value).to_bytes(max(1, (abs(value).bit_length() + 7) // 8), "big")
        return (b"i-" if value < 0 else b"i+") + _framed(magnitude)
    if isinstance(value, float):
        return b"f" + value.hex().encode("ascii")
    if isinstance(value, str):
        return b"s" + _framed(value.encode("utf-8"))
    if isinstance(value, dict):
        items = [
            (_stable_output_bytes(key), _stable_output_bytes(item)) for key, item in value.items()
        ]
        items.sort(key=lambda item: item[0])
        return b"d" + b"".join(_framed(key) + _framed(item) for key, item in items)
    if isinstance(value, list):
        return b"l" + b"".join(_framed(_stable_output_bytes(item)) for item in value)
    if isinstance(value, tuple):
        return b"t" + b"".join(_framed(_stable_output_bytes(item)) for item in value)
    raise TypeError(f"unsupported output type: {type(value).__name__}")


def _output_descriptor(value: Any, atol: float) -> tuple[str, Any]:
    if atol != 0 or _is_float_output(value):
        return ("value", value)
    return ("sha256", hashlib.sha256(_stable_output_bytes(value)).hexdigest())


def _hidden_pytest(problem: dict[str, Any]) -> tuple[str, int]:
    entry_point = str(problem["entry_point"])
    inputs, removed = _curated_inputs(problem)
    inputs_source = pprint.pformat(inputs, width=100, sort_dicts=True)
    if entry_point == "find_zero":
        check_source = """
    failures = []
    for index, arguments in enumerate(INPUTS):
        output = candidate(*copy.deepcopy(arguments))
        coefficients = arguments[0]
        residual = sum(
            coefficient * math.pow(output, power)
            for power, coefficient in enumerate(coefficients)
        )
        if not abs(residual) <= ATOL:
            failures.append(index)
    if failures:
        raise AssertionError(f"HumanEval+ cases failed: {failures}")
"""
        expected_source = ""
        suite_body = textwrap.dedent(check_source).strip()
    else:
        outputs = _reference_outputs(problem, inputs)
        descriptors = [_output_descriptor(output, float(problem["atol"])) for output in outputs]
        expected_source = _compressed_outputs(descriptors)
        check_source = """
        output = candidate(*copy.deepcopy(arguments))
        comparison, expected = EXPECTED[index]
        if comparison == "sha256":
            if _output_sha256(output) == expected:
                continue
            raise AssertionError(f"HumanEval+ case {index} failed")
        try:
            exact_match = bool(output == expected)
        except (TypeError, ValueError):
            exact_match = False
        effective_atol = ATOL
        if effective_atol == 0 and _is_floats(expected):
            effective_atol = 1e-6
        if exact_match:
            continue
        if effective_atol != 0:
            if type(output) is not type(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong type")
            if isinstance(expected, (list, tuple)) and len(output) != len(expected):
                raise AssertionError(f"HumanEval+ case {index} returned the wrong length")
            if np.allclose(output, expected, rtol=1e-7, atol=effective_atol):
                continue
        raise AssertionError(f"HumanEval+ case {index} failed")
"""
        dedented = textwrap.dedent(check_source).strip()
        loop_body = "\n".join(f"    {line}" if line else "" for line in dedented.splitlines())
        suite_body = "for index, arguments in enumerate(INPUTS):\n" + loop_body
    indented_suite = "\n".join(f"    {line}" if line else "" for line in suite_body.splitlines())
    source = (
        "import base64\n"
        "import copy\n"
        "import hashlib\n"
        "import math\n\n"
        "import pickle\n"
        "import zlib\n\n"
        "import numpy as np\n\n"
        "from solution import *  # noqa: F403\n\n"
        f"INPUTS = {inputs_source}\n"
        f"ATOL = {float(problem['atol'])!r}\n"
        f"{expected_source}\n"
        "def _is_floats(value):\n"
        "    if isinstance(value, float):\n"
        "        return True\n"
        "    return (\n"
        "        isinstance(value, (list, tuple))\n"
        "        and bool(value)\n"
        "        and all(isinstance(item, float) for item in value)\n"
        "    )\n\n\n"
        "def _framed(payload):\n"
        "    return len(payload).to_bytes(8, 'big') + payload\n\n\n"
        "def _stable_output_bytes(value):\n"
        "    if value is None:\n"
        "        return b'n'\n"
        "    if isinstance(value, bool):\n"
        "        return b'b1' if value else b'b0'\n"
        "    if isinstance(value, int):\n"
        "        size = max(1, (abs(value).bit_length() + 7) // 8)\n"
        "        magnitude = abs(value).to_bytes(size, 'big')\n"
        "        return (b'i-' if value < 0 else b'i+') + _framed(magnitude)\n"
        "    if isinstance(value, float):\n"
        "        return b'f' + value.hex().encode('ascii')\n"
        "    if isinstance(value, str):\n"
        "        return b's' + _framed(value.encode('utf-8'))\n"
        "    if isinstance(value, dict):\n"
        "        items = [(_stable_output_bytes(key), _stable_output_bytes(item)) "
        "for key, item in value.items()]\n"
        "        items.sort(key=lambda item: item[0])\n"
        "        return b'd' + b''.join(_framed(key) + _framed(item) for key, item in items)\n"
        "    if isinstance(value, list):\n"
        "        return b'l' + b''.join(_framed(_stable_output_bytes(item)) for item in value)\n"
        "    if isinstance(value, tuple):\n"
        "        return b't' + b''.join(_framed(_stable_output_bytes(item)) for item in value)\n"
        "    raise TypeError(f'unsupported output type: {type(value).__name__}')\n\n\n"
        "def _output_sha256(value):\n"
        "    return hashlib.sha256(_stable_output_bytes(value)).hexdigest()\n\n\n"
        "def test_humaneval_plus_suite():\n"
        f"    candidate = {entry_point}  # noqa: F405\n"
        f"{indented_suite}\n"
    )
    return source, removed


def import_full(
    feedback_path: Path,
    evalplus_jsonl: Path,
    output: Path,
    *,
    candidate_pool_path: Path | None = None,
    overrides_path: Path | None = None,
) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    feedback_rows = {_numeric_id(row["_id"]): row for row in _read_jsonl(feedback_path)}
    overrides = json.loads(overrides_path.read_text(encoding="utf-8")) if overrides_path else {}
    pool_rows = {}
    if candidate_pool_path is not None:
        pool_rows = {
            _numeric_id(row.get("_id") or row.get("task_id")): row
            for row in _read_jsonl(candidate_pool_path)
        }
    plus_rows = {_numeric_id(row["task_id"]): row for row in _read_jsonl(evalplus_jsonl)}
    expected = set(range(164))
    if set(feedback_rows) != expected or set(plus_rows) != expected:
        raise ValueError("both sources must contain exactly HumanEval/0 through HumanEval/163")

    staging = output.with_name(f".{output.name}.staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    tasks = []
    oracle_invalid_inputs_removed = 0
    try:
        for number in range(164):
            feedback = feedback_rows[number]
            plus = plus_rows[number]
            candidate = feedback["false_results"][0]
            candidate_index = 0
            candidate_file = feedback_path.name
            if str(number) in overrides:
                candidate_index = int(overrides[str(number)])
                if candidate_pool_path is None or number not in pool_rows:
                    raise ValueError(f"candidate pool missing for override HumanEval/{number}")
                candidates = pool_rows[number]["false_results"]
                if not 0 <= candidate_index < len(candidates):
                    raise ValueError(f"invalid candidate override HumanEval/{number}")
                candidate = candidates[candidate_index]
                candidate_file = candidate_pool_path.name
            entry_point = str(plus["entry_point"])
            code = str(candidate["generate_code"]).rstrip() + "\n"
            public_source = _public_pytest(str(feedback["test"]), entry_point)
            hidden_source, removed = _hidden_pytest(plus)
            oracle_invalid_inputs_removed += removed
            compile(public_source, f"HumanEval/{number}/test_public.py", "exec")
            compile(hidden_source, f"HumanEval/{number}/test_hidden.py", "exec")

            task_id = f"feedbackeval-humaneval-{number:03d}"
            task_dir = staging / task_id
            tests = task_dir / "workspace/tests"
            hidden = task_dir / "hidden_tests"
            tests.mkdir(parents=True)
            hidden.mkdir()
            (task_dir / "workspace/solution.py").write_text(code, encoding="utf-8")
            (tests / "test_public.py").write_text(public_source, encoding="utf-8")
            (hidden / "test_hidden.py").write_text(hidden_source, encoding="utf-8")
            task = {
                "schema_version": 1,
                "task_id": task_id,
                "title": f"FeedbackEval HumanEval repair: {entry_point}",
                "goal": (
                    f"Repair {entry_point} so it satisfies its documented behavior and the "
                    "public examples while preserving its signature."
                ),
                "constraints": [
                    "Only edit solution.py.",
                    "Do not add dependencies or modify tests.",
                    f"Keep the public function {entry_point} and its signature unchanged.",
                ],
                "editable_paths": ["solution.py"],
                "public_verification": {
                    "command": "python -m pytest -q tests",
                    "protected_paths": ["tests"],
                },
                "hidden_verification": {
                    "tests": "hidden_tests",
                    "command": "python -m pytest -q /hidden_tests",
                },
                "test_version": "feedbackeval-base-evalplus-v0.1.10-hidden-v2",
                "provenance": {
                    "repair_dataset": "FeedbackEval/HumanEval_feedback_test",
                    "feedbackeval_commit": FEEDBACKEVAL_COMMIT,
                    "source_task_id": f"HumanEval/{number}",
                    "candidate_source": candidate.get("source", "unknown"),
                    "candidate_file": candidate_file,
                    "candidate_index": candidate_index,
                    "candidate_sha256": _sha256(code.encode()),
                    "public_tests": "FeedbackEval frozen HumanEval base tests",
                    "hidden_tests": "EvalPlus HumanEval+ v0.1.10 base+extra inputs and oracle",
                    "evalplus_version": EVALPLUS_VERSION,
                    "oracle_invalid_inputs_removed": removed,
                    "correct_code_included": False,
                    "precomputed_feedback_included": False,
                },
            }
            (task_dir / "task.json").write_text(
                json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            tasks.append(
                {
                    "task_id": task_id,
                    "source_task_id": f"HumanEval/{number}",
                    "candidate_source": candidate.get("source", "unknown"),
                    "candidate_file": candidate_file,
                    "candidate_index": candidate_index,
                    "candidate_sha256": _sha256(code.encode()),
                }
            )

        manifest = {
            "schema_version": 1,
            "dataset": "FeedbackEval HumanEval full + HumanEval+ hidden",
            "feedbackeval_commit": FEEDBACKEVAL_COMMIT,
            "evalplus_version": EVALPLUS_VERSION,
            "count": len(tasks),
            "selection": {"method": "complete-HumanEval", "outcome_blind": True},
            "candidate_overrides": overrides,
            "oracle_invalid_inputs_removed": oracle_invalid_inputs_removed,
            "test_policy": {
                "public": "FeedbackEval frozen HumanEval base tests",
                "hidden": (
                    "HumanEval+ v0.1.10 base and extra inputs with EvalPlus-equivalent "
                    "comparison, mounted only for final scoring"
                ),
                "correct_code_copied": False,
                "precomputed_feedback_copied": False,
                "curation": (
                    "remove only inputs rejected by the official reference implementation "
                    "under the official EvalPlus oracle"
                ),
            },
            "source_sha256": {
                "feedbackeval": _sha256(feedback_path.read_bytes()),
                "candidate_pool": (
                    _sha256(candidate_pool_path.read_bytes()) if candidate_pool_path else None
                ),
                "evalplus_jsonl_gz": _sha256(evalplus_jsonl.read_bytes()),
            },
            "tasks": tasks,
        }
        (staging / "dataset-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        staging.rename(output)
        return manifest
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("feedback", type=Path)
    parser.add_argument("evalplus_jsonl", type=Path)
    parser.add_argument(
        "--output", type=Path, default=Path("benchmarks/feedbackeval-humaneval-full")
    )
    parser.add_argument("--candidate-pool", type=Path)
    parser.add_argument("--overrides", type=Path)
    args = parser.parse_args()
    manifest = import_full(
        args.feedback.resolve(),
        args.evalplus_jsonl.resolve(),
        args.output.resolve(),
        candidate_pool_path=args.candidate_pool.resolve() if args.candidate_pool else None,
        overrides_path=args.overrides.resolve() if args.overrides else None,
    )
    print(f"Imported {manifest['count']} tasks into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
