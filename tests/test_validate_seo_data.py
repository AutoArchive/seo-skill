from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_seo_data.py"
SPEC = importlib.util.spec_from_file_location("validate_seo_data", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateSeoDataTests(unittest.TestCase):
    def write(self, root: Path, relative: str, content: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def make_legacy_layout(self, root: Path) -> None:
        self.write(
            root,
            "site.md",
            """# TSFiction SEO site metadata

- Public site: https://tsfiction.org
- Repository: `cdtsf-library/translate-fiction`
- Runtime analytics required: yes
- Primary runtime provider: Google Analytics 4
- Runtime verification URL: `https://tsfiction.org/`
- URL reporting: `full-url`
- Search analytics required: Google Search Console
- Analytics payload policy: public page-view metadata only

## Connected-tool routing

Use the connected GitHub and Cloudflare tools.
""",
        )
        self.write(
            root,
            "daily-task.md",
            """# TSFiction autonomous daily task

Operate the repository through real pull requests and preserve this document's existing layout.
""",
        )
        self.write(root, "status.md", "# Current operating status\n\nHealthy.\n")
        self.write(root, "plan.md", "# TSFiction operating plan\n\nContinue maintenance.\n")
        self.write(root, "block.md", "# Human-only blockers\n\nNone.\n")
        self.write(
            root,
            "daily/2026-08-05.md",
            "# 2026-08-05 TSFiction operation\n\nExisting consumer-defined daily format.\n",
        )

    def test_accepts_existing_consumer_layout_without_promotion_or_template_headings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_legacy_layout(root)
            self.assertEqual(MODULE.validate(root, date(2026, 8, 5)), 1)

    def test_accepts_additional_consumer_specific_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_legacy_layout(root)
            self.write(root, "deployment-notes.md", "# Custom deployment notes\n\nOwned by this site.\n")
            self.assertEqual(MODULE.validate(root, None), 1)

    def test_rejects_missing_analytics_semantics_without_requiring_a_heading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_legacy_layout(root)
            site = (root / "site.md").read_text(encoding="utf-8")
            (root / "site.md").write_text(
                site.replace("- URL reporting: `full-url`\n", ""), encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "URL reporting"):
                MODULE.validate(root, None)

    def test_rejects_private_values_in_any_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_legacy_layout(root)
            self.write(root, "custom.md", "# Custom\n\n- API token: secret-value\n")
            with self.assertRaisesRegex(ValueError, "credential field"):
                MODULE.validate(root, None)

    def test_requires_requested_daily_date_but_not_a_shared_title(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_legacy_layout(root)
            with self.assertRaisesRegex(ValueError, "missing daily record"):
                MODULE.validate(root, date(2026, 8, 6))


if __name__ == "__main__":
    unittest.main()
