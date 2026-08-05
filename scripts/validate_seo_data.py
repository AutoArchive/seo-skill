#!/usr/bin/env python3
"""Run small, high-confidence checks on public SEO operating data."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


# These are the only shared entrypoints. Everything inside the documents belongs
# to the consuming repository and is intentionally not parsed as a schema.
REQUIRED_ENTRYPOINTS = ("site.md", "daily-task.md")

BEARER_RE = re.compile(r"(?i)\b(?:authorization\s*:\s*)?bearer\s+[A-Za-z0-9._~+/-]+=*\b")
DRIVE_URL_RE = re.compile(r"(?i)https://drive\.google\.com/[^\s)>]+")
PRIVATE_LABEL_RE = re.compile(
    r"(?im)^\s*[-*]?\s*(?:account|zone|folder|file|property|user)\s+id\s*:\s*(?!none\s*$|not recorded\s*$).+"
)
SECRET_LABEL_RE = re.compile(
    r"(?im)^\s*[-*]?\s*(?:api\s+key|api\s+token|access\s+token|password|secret)\s*:\s*(?!none\s*$|not recorded\s*$).+"
)


def read_nonempty(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"empty {path}")
    return text


def scan_public(path: Path, text: str) -> None:
    checks = (
        (BEARER_RE, "bearer credential"),
        (DRIVE_URL_RE, "Google Drive URL with private identifier"),
        (PRIVATE_LABEL_RE, "private source identifier"),
        (SECRET_LABEL_RE, "credential field"),
    )
    for pattern, label in checks:
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            raise ValueError(f"{label} in {path}:{line}")
def validate(data_root: Path, expected_date: date | None) -> int:
    if not data_root.is_dir():
        raise ValueError(f"missing {data_root}")

    for filename in REQUIRED_ENTRYPOINTS:
        path = data_root / filename
        text = read_nonempty(path)
        scan_public(path, text)

    # Scan only for high-confidence credential or private-routing mistakes.
    # Empty optional files and consumer-specific prose are valid.
    for path in sorted(data_root.rglob("*.md")):
        if path.name in REQUIRED_ENTRYPOINTS and path.parent == data_root:
            continue
        text = path.read_text(encoding="utf-8")
        if text.strip():
            scan_public(path, text)

    daily_dir = data_root / "daily"
    if not daily_dir.is_dir():
        raise ValueError(f"missing {daily_dir}")

    daily_count = sum(1 for _ in daily_dir.glob("*.md"))
    if expected_date is not None:
        expected_path = daily_dir / f"{expected_date.isoformat()}.md"
        scan_public(expected_path, read_nonempty(expected_path))
    return daily_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--date", type=date.fromisoformat)
    args = parser.parse_args()
    try:
        daily_count = validate(args.data_root, args.date)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"checked basic SEO-data safety in {args.data_root}: {daily_count} daily records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
