#!/usr/bin/env python3
"""Validate declarative SEO operating-loop evaluation cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DECISIONS = {
    "repair",
    "experiment",
    "monitor",
    "unknown",
    "public-safe-summary",
}


def validate_case(path: Path, case: Any, seen_ids: set[str]) -> None:
    if not isinstance(case, dict):
        raise ValueError(f"evaluation case must be an object in {path}")
    identifier = case.get("id")
    prompt = case.get("prompt")
    decision = case.get("expected_decision")
    expectations = case.get("expectations")
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError(f"evaluation case has no ID in {path}")
    if identifier in seen_ids:
        raise ValueError(f"duplicate evaluation ID {identifier!r}")
    seen_ids.add(identifier)
    if not isinstance(prompt, str) or len(prompt.strip()) < 40:
        raise ValueError(f"evaluation {identifier!r} has an inadequate prompt")
    if not isinstance(decision, str) or decision not in ALLOWED_DECISIONS:
        raise ValueError(
            f"evaluation {identifier!r} has invalid expected decision {decision!r}"
        )
    if not isinstance(expectations, list) or len(expectations) < 2:
        raise ValueError(f"evaluation {identifier!r} needs at least two expectations")
    if any(not isinstance(item, str) or len(item.strip()) < 10 for item in expectations):
        raise ValueError(f"evaluation {identifier!r} has an invalid expectation")


def validate(path: Path, seen_ids: set[str]) -> int:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error
    if payload.get("schema_version") != 1:
        raise ValueError(f"unsupported schema_version in {path}")
    if not isinstance(payload.get("suite"), str) or not payload["suite"].strip():
        raise ValueError(f"missing suite in {path}")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"no evaluation cases in {path}")
    for case in cases:
        validate_case(path, case, seen_ids)
    return len(cases)


def main() -> int:
    try:
        paths = sorted((ROOT / "evals").glob("*.json"))
        if not paths:
            raise ValueError("no evaluation files found")
        seen_ids: set[str] = set()
        count = sum(validate(path, seen_ids) for path in paths)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {count} evaluation cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
