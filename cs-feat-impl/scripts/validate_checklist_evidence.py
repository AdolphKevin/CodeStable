#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

STEP_REQUIRED = {"action", "exit_signal", "proof_required", "status", "evidence", "blocker"}
CHECK_REQUIRED = {
    "item",
    "source",
    "design_ref",
    "proof_required",
    "positive_case",
    "negative_case",
    "typed_signal",
    "forbidden_basis",
    "status",
    "evidence",
    "blocker",
}
STEP_ALLOWED = {"pending", "partial", "blocked", "done"}
CHECK_ALLOWED = {"pending", "partial", "blocked", "passed"}


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def validate(path: Path) -> list[str]:
    data = yaml.safe_load(path.read_text()) or {}
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["checklist must be a YAML mapping"]

    steps = data.get("steps", [])
    checks = data.get("checks", [])
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list")
        steps = []
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
        checks = []

    for index, step in enumerate(steps, 1):
        if not isinstance(step, dict):
            errors.append(f"steps[{index}] must be a mapping")
            continue
        missing = sorted(STEP_REQUIRED - set(step))
        if missing:
            errors.append(f"steps[{index}] missing fields: {', '.join(missing)}")
        status = step.get("status")
        if status not in STEP_ALLOWED:
            errors.append(f"steps[{index}] invalid status: {status!r}")
        if status == "done" and not _nonempty(step.get("evidence")):
            errors.append(f"steps[{index}] status done requires non-empty evidence")
        if status in {"partial", "blocked"} and not _nonempty(step.get("blocker")):
            errors.append(f"steps[{index}] status {status} requires blocker")

    for index, check in enumerate(checks, 1):
        if not isinstance(check, dict):
            errors.append(f"checks[{index}] must be a mapping")
            continue
        missing = sorted(CHECK_REQUIRED - set(check))
        if missing:
            errors.append(f"checks[{index}] missing fields: {', '.join(missing)}")
        status = check.get("status")
        if status not in CHECK_ALLOWED:
            errors.append(f"checks[{index}] invalid status: {status!r}")
        if status == "passed" and not _nonempty(check.get("evidence")):
            errors.append(f"checks[{index}] status passed requires non-empty evidence")
        if status in {"partial", "blocked"} and not _nonempty(check.get("blocker")):
            errors.append(f"checks[{index}] status {status} requires blocker")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate CodeStable feature checklist evidence fields.",
    )
    parser.add_argument("checklist", type=Path)
    args = parser.parse_args()
    errors = validate(args.checklist)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Checklist evidence is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
