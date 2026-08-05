#!/usr/bin/env python3
"""Materialize and validate one consuming repository SEO-data fixture."""

from __future__ import annotations

import shutil
import tempfile
from datetime import date
from pathlib import Path

from validate_seo_data import validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "seo-data"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="seo-skill-templates-") as directory:
        data_root = Path(directory)
        for name in (
            "site",
            "daily-task",
            "promotion",
            "status",
            "plan",
            "block",
            "experiments",
        ):
            shutil.copyfile(TEMPLATES / f"{name}.example.md", data_root / f"{name}.md")
        daily_dir = data_root / "daily"
        daily_dir.mkdir()
        shutil.copyfile(TEMPLATES / "daily.example.md", daily_dir / "2026-08-04.md")
        daily_count = validate(data_root, date(2026, 8, 4))
        if daily_count != 1:
            raise ValueError(f"expected one daily record, found {daily_count}")
    print("template fixture is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
