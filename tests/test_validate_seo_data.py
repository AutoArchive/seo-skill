from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_seo_data.py"
SPEC = importlib.util.spec_from_file_location("validate_seo_data", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


SITE_BASE = """# Site metadata

## Identity

- Canonical URL: `https://www.real-site.test/`
- Site name: `real-site.test`
- Timezone: `America/Los_Angeles`

## Repository

- Default branch: `main`
- Automation branch prefix: `seo/`
- Skill submodule path: `.github/seo-skills`

## Analytics

- Runtime analytics required: yes
- Primary runtime provider: `google-analytics-4`
- Runtime implementation location: source-controlled config
- Runtime verification URL: `https://www.real-site.test/`
- URL reporting: `full-url`
- Search analytics required: `google-search-console`
- Search evidence route: public-safe export route
- Infrastructure analytics: `cloudflare`
- Analytics payload policy: transmit the complete browser URL and no private custom events

## Deployment

- Provider: `cloudflare-pages`
- Production environment: `production`
- Verification URL: `https://www.real-site.test/`
"""

SITE_BOOTSTRAPPED = """# Site metadata

## Identity

- Canonical URL: `https://www.real-site.test/`
- Site name: `real-site.test`
- Timezone: `America/Los_Angeles`

## Repository

- Default branch: `main`
- Automation branch prefix: `seo/`
- Skill submodule path: `.github/seo-skills`

## Analytics

- Runtime analytics required: yes
- Primary runtime provider: `google-analytics-4`
- Runtime implementation location: source-controlled config
- Runtime verification URL: `https://www.real-site.test/`
- URL reporting: `full-url`
- Search analytics required: `google-search-console`
- Search evidence route: public-safe export route
- Infrastructure analytics: `cloudflare`
- Analytics payload policy: transmit the complete browser URL and no private custom events

## Deployment

- Bootstrap status: complete
- Bootstrap verified at: 2026-08-05
- Production chain verified: yes
- Bootstrap evidence strength: strong
- Provider: `cloudflare-pages`
- Production project or service: `real-site`
- Production source repository: `org/real-site`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Production environment: `production`
- Last verified production commit: `abcdef0123456789abcdef0123456789abcdef01`
- Provider deployment evidence method: connected provider deployment matched to exact source commit
- Public deployment verification method: immutable deployment marker plus representative changed page
- Verification URL: `https://www.real-site.test/deployment.json`
- Preview or non-production paths: provider previews and gh-pages are not production
- Bootstrap invalidation conditions: domain, provider, repository, branch, build, output, trigger, analytics, or public commit correspondence changes
"""

DAILY_TASK = """# Daily SEO task

## Objective

Operate the verified site.

## Required sequence

1. Verify production topology.

## Daily completion

Production must be verified.
"""

PROMOTION = """# Promotion strategy

## Audience

Readers.

## Channels

Search.

## Operating rules

Use verified claims.
"""

STATUS = """# SEO status

## Current state

Current state recorded.

## Current signals

Signals recorded.
"""

PLAN = """# SEO plan

## Purpose

Improve the verified production site.
"""

BLOCK = """# Human-only blockers

None.
"""

DAILY = """# SEO operations — 2026-08-05

## Scope

Test.

## Data window

Test.

## Evidence collected

Test.

## Work performed

Test.

## Validation and self-review

Test.

## Delivery

Test.

## Decisions and follow-ups

Test.
"""


class ValidateSeoDataTests(unittest.TestCase):
    def make_root(self, site: str = SITE_BASE) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "daily").mkdir()
        files = {
            "site.md": site,
            "daily-task.md": DAILY_TASK,
            "promotion.md": PROMOTION,
            "status.md": STATUS,
            "plan.md": PLAN,
            "block.md": BLOCK,
            "daily/2026-08-05.md": DAILY,
        }
        for relative, content in files.items():
            (root / relative).write_text(content, encoding="utf-8")
        return root

    def test_legacy_layout_remains_valid_without_strict_bootstrap(self) -> None:
        root = self.make_root()
        self.assertEqual(MODULE.validate(root, date(2026, 8, 5)), 1)
        self.assertFalse((root / "bootstrap.md").exists())

    def test_strict_bootstrap_accepts_fields_in_existing_site_file(self) -> None:
        root = self.make_root(SITE_BOOTSTRAPPED)
        self.assertEqual(MODULE.validate(root, date(2026, 8, 5), True), 1)
        self.assertFalse((root / "bootstrap.md").exists())

    def test_strict_bootstrap_rejects_legacy_site_until_audit_finishes(self) -> None:
        root = self.make_root()
        with self.assertRaisesRegex(ValueError, "Bootstrap status"):
            MODULE.validate(root, None, True)

    def test_incomplete_bootstrap_fails_in_strict_mode(self) -> None:
        root = self.make_root(
            SITE_BOOTSTRAPPED.replace("Bootstrap status: complete", "Bootstrap status: stale")
        )
        with self.assertRaisesRegex(ValueError, "Bootstrap status"):
            MODULE.validate(root, None, True)

    def test_placeholder_values_fail_in_strict_mode(self) -> None:
        root = self.make_root(
            SITE_BOOTSTRAPPED.replace("org/real-site", "owner/repository")
        )
        with self.assertRaisesRegex(ValueError, "placeholder"):
            MODULE.validate(root, None, True)

    def test_bad_commit_fails_in_strict_mode(self) -> None:
        root = self.make_root(
            SITE_BOOTSTRAPPED.replace(
                "abcdef0123456789abcdef0123456789abcdef01", "not-a-sha"
            )
        )
        with self.assertRaisesRegex(ValueError, "real git SHA"):
            MODULE.validate(root, None, True)


if __name__ == "__main__":
    unittest.main()
