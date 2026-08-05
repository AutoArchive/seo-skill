#!/usr/bin/env python3
"""Validate the public Markdown-only SEO operating directory."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FILES = {
    "bootstrap.md": (
        "# SEO bootstrap",
        "## Status",
        "## Canonical production",
        "## Production source of truth",
        "## Provider deployment evidence",
        "## Public verification",
        "## Non-production and rejected paths",
        "## Analytics and search baseline",
        "## Baseline and rollback",
        "## Invalidation conditions",
    ),
    "site.md": (
        "# Site metadata",
        "## Identity",
        "## Bootstrap",
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
    r"(?im)^\s*[-*]\s*Runtime verification URL:\s*`?https://[^\s`]+`?\s*$"
)
URL_REPORTING_RE = re.compile(
    r"(?im)^\s*[-*]\s*URL reporting:\s*`?(?:full-url|path-only)`?\s*$"
)
SEARCH_ANALYTICS_RE = re.compile(
    r"(?im)^\s*[-*]\s*Search analytics required:\s*(?!`?(?:none|no|optional|disabled)`?\s*$).+\S\s*$"
)
PAYLOAD_POLICY_RE = re.compile(
    r"(?im)^\s*[-*]\s*Analytics payload policy:\s*.+\S\s*$"
)
FIELD_RE_TEMPLATE = r"(?im)^\s*[-*]\s*{label}:\s*(.+?)\s*$"
PLACEHOLDER_RE = re.compile(
    r"(?i)(?:example\.com|owner/repository|example-site|0123456789abcdef|\bunknown\b|\btbd\b|\bTODO\b|replace[- ]?me)"
)
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")


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


def get_field(path: Path, text: str, label: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(label=re.escape(label)))
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing field {label!r} in {path}")
    value = match.group(1).strip().strip("`").strip()
    if not value:
        raise ValueError(f"empty field {label!r} in {path}")
    return value


def normalize_url(value: str) -> str:
    return value.rstrip("/")


def validate_analytics_contract(path: Path, text: str) -> None:
    checks = (
        (ANALYTICS_REQUIRED_RE, "runtime analytics must be explicitly required: yes"),
        (PRIMARY_ANALYTICS_RE, "a primary runtime analytics provider is required"),
        (RUNTIME_VERIFICATION_RE, "a public HTTPS runtime analytics verification URL is required"),
        (URL_REPORTING_RE, "URL reporting must be full-url or path-only"),
        (SEARCH_ANALYTICS_RE, "search analytics must be required"),
        (PAYLOAD_POLICY_RE, "the analytics payload policy is required"),
    )
    for pattern, message in checks:
        if not pattern.search(text):
            raise ValueError(f"{message} in {path}")


def validate_bootstrap_contract(path: Path, text: str) -> dict[str, str]:
    required = {
        "Bootstrap status": "complete",
        "Production chain verified": "yes",
        "Custom-domain attachment verified": "yes",
        "Public content matched exact production commit": "yes",
    }
    values: dict[str, str] = {}
    for label, expected in required.items():
        value = get_field(path, text, label)
        if value.lower() != expected:
            raise ValueError(f"{label} must be {expected!r} in {path}")
        values[label] = value

    verified_at = get_field(path, text, "Bootstrap verified at")
    try:
        date.fromisoformat(verified_at)
    except ValueError as error:
        raise ValueError(f"Bootstrap verified at must be YYYY-MM-DD in {path}") from error
    values["Bootstrap verified at"] = verified_at

    field_names = (
        "Canonical production URL",
        "DNS or edge provider",
        "Production hosting provider",
        "Production project or service",
        "Production source repository",
        "Production source branch",
        "Repository root or monorepo path",
        "Site generator or framework",
        "Production build command",
        "Production output directory",
        "Production deployment trigger",
        "Last verified production commit",
        "Provider evidence method",
        "Public deployment verification method",
        "Public verification URL",
    )
    for label in field_names:
        value = get_field(path, text, label)
        if PLACEHOLDER_RE.search(value):
            raise ValueError(f"placeholder value for {label!r} in {path}")
        values[label] = value

    canonical = values["Canonical production URL"]
    verification_url = values["Public verification URL"]
    if not canonical.startswith("https://"):
        raise ValueError(f"Canonical production URL must use HTTPS in {path}")
    if not verification_url.startswith("https://"):
        raise ValueError(f"Public verification URL must use HTTPS in {path}")

    repository = values["Production source repository"]
    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError(f"Production source repository must be owner/repository in {path}")

    commit = values["Last verified production commit"]
    if not COMMIT_RE.fullmatch(commit) or len(set(commit.lower())) == 1:
        raise ValueError(f"Last verified production commit must be a real git SHA in {path}")

    return values


def validate_site_deployment_contract(path: Path, text: str) -> dict[str, str]:
    if get_field(path, text, "Bootstrap required").lower() != "yes":
        raise ValueError(f"Bootstrap required must be 'yes' in {path}")
    if get_field(path, text, "Normal site mutation allowed only when bootstrap status is complete").lower() != "yes":
        raise ValueError(f"normal mutation must be gated on bootstrap completion in {path}")

    field_names = (
        "Canonical URL",
        "Provider",
        "Production project or service",
        "Production source repository",
        "Production source branch",
        "Repository root or monorepo path",
        "Production build command",
        "Production output directory",
        "Production deployment trigger",
        "Verification URL",
        "Provider deployment evidence method",
        "Public deployment verification method",
    )
    values: dict[str, str] = {}
    for label in field_names:
        value = get_field(path, text, label)
        if PLACEHOLDER_RE.search(value):
            raise ValueError(f"placeholder value for {label!r} in {path}")
        values[label] = value

    if not values["Canonical URL"].startswith("https://"):
        raise ValueError(f"Canonical URL must use HTTPS in {path}")
    if not values["Verification URL"].startswith("https://"):
        raise ValueError(f"Verification URL must use HTTPS in {path}")
    if not REPOSITORY_RE.fullmatch(values["Production source repository"]):
        raise ValueError(f"Production source repository must be owner/repository in {path}")
    return values


def validate_production_agreement(
    bootstrap_path: Path,
    bootstrap: dict[str, str],
    site_path: Path,
    site: dict[str, str],
) -> None:
    comparisons = (
        ("Canonical production URL", "Canonical URL", normalize_url),
        ("Production hosting provider", "Provider", str.lower),
        ("Production project or service", "Production project or service", str.lower),
        ("Production source repository", "Production source repository", str.lower),
        ("Production source branch", "Production source branch", str.lower),
        ("Repository root or monorepo path", "Repository root or monorepo path", str),
        ("Production build command", "Production build command", str),
        ("Production output directory", "Production output directory", str),
        ("Production deployment trigger", "Production deployment trigger", str),
        ("Public verification URL", "Verification URL", normalize_url),
        ("Provider evidence method", "Provider deployment evidence method", str),
        ("Public deployment verification method", "Public deployment verification method", str),
    )
    for bootstrap_label, site_label, normalizer in comparisons:
        left = normalizer(bootstrap[bootstrap_label])
        right = normalizer(site[site_label])
        if left != right:
            raise ValueError(
                f"production metadata mismatch: {bootstrap_label!r} in {bootstrap_path} "
                f"does not agree with {site_label!r} in {site_path}"
            )


def validate(data_root: Path, expected_date: date | None) -> int:
    loaded: dict[str, str] = {}
    for filename, headings in REQUIRED_FILES.items():
        path = data_root / filename
        text = read_required(path, headings)
        scan_public(path, text)
        loaded[filename] = text

    bootstrap_path = data_root / "bootstrap.md"
    site_path = data_root / "site.md"
    bootstrap = validate_bootstrap_contract(bootstrap_path, loaded["bootstrap.md"])
    validate_analytics_contract(site_path, loaded["site.md"])
    site = validate_site_deployment_contract(site_path, loaded["site.md"])
    validate_production_agreement(bootstrap_path, bootstrap, site_path, site)

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
