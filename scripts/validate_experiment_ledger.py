#!/usr/bin/env python3
"""Validate the opt-in SEO experiment ledger format."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPERIMENT_HEADING_RE = re.compile(r"(?im)^#{2,6}\s+(EXP-\d{8}-\d{2,})\b.*$")
EXPERIMENT_STATUS_RE = re.compile(r"(?im)^\s*[-*]\s*Status:\s*`?([a-z-]+)`?\s*$")
MAX_ACTIVE_RE = re.compile(
    r"(?im)^\s*[-*]\s*Maximum active speculative experiments:\s*(\d+)\s*$"
)
VALID_STATUSES = {
    "proposed",
    "active",
    "observing",
    "evaluating",
    "won",
    "lost",
    "inconclusive",
    "aborted",
}
ACTIVE_STATUSES = {"active", "observing", "evaluating"}


def read_nonempty(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"empty {path}")
    return text


def validate(ledger: Path, site: Path | None = None) -> tuple[int, int, int]:
    """Return (recognized experiments, active experiments, configured maximum)."""

    ledger_text = read_nonempty(ledger)
    site_text = read_nonempty(site) if site is not None else ""
    limits = [
        int(match.group(1))
        for text in (site_text, ledger_text)
        for match in MAX_ACTIVE_RE.finditer(text)
    ]
    if len(set(limits)) > 1:
        raise ValueError(f"conflicting maximum active experiment limits for {ledger}")
    maximum_active = limits[0] if limits else 1

    matches = list(EXPERIMENT_HEADING_RE.finditer(ledger_text))
    seen_ids: set[str] = set()
    active_ids: list[str] = []
    for index, match in enumerate(matches):
        experiment_id = match.group(1)
        if experiment_id in seen_ids:
            raise ValueError(f"duplicate experiment ID {experiment_id} in {ledger}")
        seen_ids.add(experiment_id)

        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(ledger_text)
        section = ledger_text[match.end():section_end]
        status_match = EXPERIMENT_STATUS_RE.search(section)
        if status_match is None:
            raise ValueError(f"missing status for experiment {experiment_id} in {ledger}")
        status = status_match.group(1)
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid experiment status {status!r} for {experiment_id} in {ledger}")
        if status in ACTIVE_STATUSES:
            active_ids.append(experiment_id)

    if len(active_ids) > maximum_active:
        raise ValueError(
            f"{len(active_ids)} active experiments exceed limit {maximum_active} in {ledger}: "
            + ", ".join(active_ids)
        )
    return len(matches), len(active_ids), maximum_active


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    try:
        experiments, active, maximum = validate(args.ledger, args.site)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"validated {args.ledger}: {experiments} experiments, "
        f"{active} active, maximum {maximum}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
