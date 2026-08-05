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


BOOTSTRAP = """# SEO bootstrap

## Status

- Bootstrap status: complete
- Bootstrap verified at: 2026-08-05
- Production chain verified: yes
- Evidence strength: strong

## Canonical production

- Canonical production URL: `https://www.real-site.test/`
- Apex and www behavior: apex redirects to www
- DNS or edge provider: `cloudflare`
- Production hosting provider: `cloudflare-pages`
- Production project or service: `real-site`

## Production source of truth

- Production source repository: `org/real-site`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Site generator or framework: `hugo`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Last verified production commit: `abcdef0123456789abcdef0123456789abcdef01`

## Provider deployment evidence

- Provider evidence method: connected provider deployment matched to exact source commit
- Latest verified production deployment: 2026-08-05 production deployment
- Custom-domain attachment verified: yes
- Production branch verified: yes
- Connected repository verified: yes
- Build command and output directory verified: yes
- Preview deployment behavior: pull requests create previews

## Public verification

- Public deployment verification method: immutable deployment marker plus representative changed page
- Public verification URL: `https://www.real-site.test/deployment.json`
- Representative homepage verified: yes
- Robots and sitemap verified: yes
- Recent changed page verified: yes
- Public content matched exact production commit: yes

## Non-production and rejected paths

- Generated branches: `gh-pages` is not production
- Preview providers or projects: provider previews only
- Legacy providers or projects: none
- Backup repositories: none
- Rejected production candidates: generated branch rejected by provider configuration

## Analytics and search baseline

- Runtime analytics provider: `google-analytics-4`
- Runtime analytics production verification: verified
- URL reporting mode: `full-url`
- Google Search Console: configured
- Infrastructure analytics: `cloudflare`
- Analytics discrepancies: none

## Baseline and rollback

- Representative routes: homepage, robots, sitemap, article
- Current title and canonical behavior: verified
- Current language routing: verified
- Current analytics loader: verified
- Current deployment marker: verified
- Last known good production deployment: abcdef0123456789abcdef0123456789abcdef01
- Rollback method: provider rollback
- Known production defects: none

## Invalidation conditions

Re-run bootstrap when production topology changes.
"""

SITE = """# Site metadata

## Identity

- Canonical URL: `https://www.real-site.test/`
- Site name: `real-site.test`
- Timezone: `America/Los_Angeles`

## Bootstrap

- Bootstrap required: yes
- Bootstrap record: `.github/seo-data/bootstrap.md`
- Normal site mutation allowed only when bootstrap status is complete: yes

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
- Production project or service: `real-site`
- Production source repository: `org/real-site`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Production environment: `production`
- Verification URL: `https://www.real-site.test/deployment.json`
- Provider deployment evidence method: connected provider deployment matched to exact source commit
- Public deployment verification method: immutable deployment marker plus representative changed page
- Preview or non-production paths: provider previews and gh-pages
"""

DAILY_TASK = """# Daily SEO task

## Objective

Operate only after bootstrap.

## Required sequence

1. Verify bootstrap.

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

Bootstrap complete.

## Current signals

Production verified.
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
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "daily").mkdir()
        files = {
            "bootstrap.md": BOOTSTRAP,
            "site.md": SITE,
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

    def test_valid_bootstrap_and_site_contract_pass(self) -> None:
        root = self.make_root()
        self.assertEqual(MODULE.validate(root, date(2026, 8, 5)), 1)

    def test_missing_bootstrap_fails(self) -> None:
        root = self.make_root()
        (root / "bootstrap.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            MODULE.validate(root, None)

    def test_incomplete_bootstrap_fails(self) -> None:
        root = self.make_root()
        path = root / "bootstrap.md"
        path.write_text(BOOTSTRAP.replace("Bootstrap status: complete", "Bootstrap status: stale"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Bootstrap status"):
            MODULE.validate(root, None)

    def test_provider_mismatch_fails(self) -> None:
        root = self.make_root()
        path = root / "site.md"
        path.write_text(SITE.replace("Provider: `cloudflare-pages`", "Provider: `github-pages`"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "production metadata mismatch"):
            MODULE.validate(root, None)

    def test_placeholder_values_fail(self) -> None:
        root = self.make_root()
        path = root / "bootstrap.md"
        path.write_text(BOOTSTRAP.replace("org/real-site", "owner/repository"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "placeholder"):
            MODULE.validate(root, None)


if __name__ == "__main__":
    unittest.main()
