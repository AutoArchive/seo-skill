#!/usr/bin/env python3
"""Validate collection skill metadata and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(path: Path, text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"missing YAML frontmatter in {path}")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError(f"unterminated YAML frontmatter in {path}") from error
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line in {path}: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def validate_skill(skill_dir: Path) -> None:
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        raise ValueError(f"missing {skill_path}")
    text = skill_path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(skill_path, text)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != skill_dir.name or not NAME_RE.fullmatch(name):
        raise ValueError(f"invalid skill name in {skill_path}: {name!r}")
    if len(description) < 40 or len(description) > 1024 or "TODO" in description:
        raise ValueError(f"invalid skill description in {skill_path}")
    if "TODO" in text:
        raise ValueError(f"TODO remains in {skill_path}")

    agent_path = skill_dir / "agents" / "openai.yaml"
    agent_text = agent_path.read_text(encoding="utf-8")
    for required in ("display_name:", "short_description:", "default_prompt:", f"${name}"):
        if required not in agent_text:
            raise ValueError(f"missing {required!r} in {agent_path}")


def validate_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            raise ValueError(f"broken local link in {path}: {raw_target}")


def main() -> int:
    try:
        skill_dirs = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
        if not skill_dirs:
            raise ValueError("no skills found")
        for skill_dir in skill_dirs:
            validate_skill(skill_dir)
        for path in ROOT.rglob("*.md"):
            validate_links(path)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_dirs)} skills and local Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
