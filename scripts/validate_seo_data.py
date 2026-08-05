#!/usr/bin/env python3
"""Validate the public Markdown-only SEO operating directory."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FILES = {
    "site.md": (
        "# Site metadata",
        "## Identity",
        "## Repository",
        "## Analytics",
        "## Deployment",
    ),
    "daily-task.md": ("# Daily SEO task", "## Objective", "## Required sequence", "## Daily completion"),
    "promotion.md": ("# Promotion strategy", "## Audience", "## Channels", "## Operating rules"),
    "status.md": ("# SEO status", "## Current state", "## Current signals"),
    "plan.md": ("# SEO plan", "## Purpose"),
    "block.md": ("# Human-only blockers",),
}
DAILY_HEADINGS = (
    "## Scope",
    "## Data window",
    "## Evidence collected",
    "## Work performed",
    "## Validation and self-review",
    "## Delivery",
    "## Decisions and follow-ups",
)
EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
BEARER_RE = re.compile(r"(?i)\b(?:authorization\s*:\s*)?bearer\s+[A-Za-z0-9._~+/-]+=*\b")
DRIVE_URL_RE = re.compile(r"(?i)https://drive\.google\.com/[^\s)>]+")
PRIVATE_LABEL_RE = re.compile(
    r"(?im)^\s*[-*]?\s*(?:account|zone|folder|file|property|user)\s+id\s*:\s*(?!none\s*$|not recorded\s*$).+"
)
SECRET_LABEL_RE = re.compile(
    r"(?im)^\s*[-*]?\s*(?:api\s+key|api\s+token|access\s+token|password|secret|email)\s*:\s*(?!none\s*$|not recorded\s*$).+"
)
ANALYTICS_REQUIRED_RE = re.compile(
    r"(?im)^\s*[-*]\s*Runtime analytics required:\s*yes\s*$"
)
PRIMARY_ANALYTICS_RE = re.compile(
    r"(?im)^\s*[-*]\s*Primary runtime provider:\s*(?!`?(?:none|disabled|optional|not configured)`?\s*$).+\S\s*$"
)
RUNTIME_VERIFICATION_RE = re.compile(
    r"(?im)^\s*[-*]\s*Runtime verification URL:\s*https://[^\s]+\s*$"
)
SEARCH_ANALYTICS_RE = re.compile(
    r"(?im)^\s*[-*]\s*Search analytics required:\s*(?!`?(?:none|no|optional|disabled)`?\s*$).+\S\s*$"
)
FORBIDDEN_PAYLOADS_RE = re.compile(
    r"(?im)^\s*[-*]\s*Forbidden analytics payloads:\s*.+\S\s*$"
)


def read_required(path: Path, headings: tuple[str, ...]) -> str:
    if not path.is_file():
        raise ValueError(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    for heading in headings:
        if heading not in text:
            raise ValueError(f"missing heading {heading!r} in {path}")
    return text


def scan_public(path: Path, text: str) -> None:
    checks = (
        (EMAIL_RE, "email-like value"),
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


def validate_analytics_contract(path: Path, text: str) -> None:
    checks = (
        (ANALYTICS_REQUIRED_RE, "runtime analytics must be explicitly required: yes"),
        (PRIMARY_ANALYTICS_RE, "a primary runtime analytics provider is required"),
        (RUNTIME_VERIFICATION_RE, "a public HTTPS runtime analytics verification URL is required"),
        (SEARCH_ANALYTICS_RE, "search analytics must be required"),
        (FORBIDDEN_PAYLOADS_RE, "the forbidden analytics payload boundary is required"),
    )
    for pattern, message in checks:
        if not pattern.search(text):
            raise ValueError(f"{message} in {path}")


def validate(data_root: Path, expected_date: date | None) -> int:
    loaded: dict[str, str] = {}
    for filename, headings in REQUIRED_FILES.items():
        path = data_root / filename
        text = read_required(path, headings)
        scan_public(path, text)
        loaded[filename] = text

    validate_analytics_contract(data_root / "site.md", loaded["site.md"])

    daily_dir = data_root / "daily"
    if not daily_dir.is_dir():
        raise ValueError(f"missing {daily_dir}")

    daily_count = 0
    seen_dates: set[date] = set()
    for path in sorted(daily_dir.glob("*.md")):
        try:
            file_date = date.fromisoformat(path.stem)
        except ValueError as error:
            raise ValueError(f"daily filename must be YYYY-MM-DD: {path}") from error
        if file_date in seen_dates:
            raise ValueError(f"duplicate daily date: {file_date}")
        seen_dates.add(file_date)
        text = read_required(path, DAILY_HEADINGS)
        expected_title = f"# SEO operations — {file_date.isoformat()}"
        if expected_title not in text:
            raise ValueError(f"daily title does not match filename in {path}")
        scan_public(path, text)
        daily_count += 1

    if expected_date is not None and expected_date not in seen_dates:
        raise ValueError(f"missing daily record for {expected_date.isoformat()}")
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
    print(f"validated {args.data_root}: {daily_count} daily records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
