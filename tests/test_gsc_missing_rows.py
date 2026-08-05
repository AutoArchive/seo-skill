from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_gsc_exports as gsc  # noqa: E402


class MissingRowPolicyTests(unittest.TestCase):
    def test_missing_current_query_is_not_treated_as_zero_decline(self) -> None:
        result = gsc.declines(
            [],
            [gsc.Metric("possibly omitted", 20, 200, 0.10, 8)],
            kind="query",
            minimum_clicks=1,
            threshold=-20,
            limit=10,
            public_safe=False,
        )
        self.assertEqual(result, [])

    def test_analyze_records_missing_row_semantics(self) -> None:
        report = gsc.analyze(
            query_rows=[gsc.Metric("current", 5, 100, 0.05, 8)],
            page_rows=[gsc.Metric("https://example.com/", 5, 100, 0.05, 8)],
            prior_query_rows=[gsc.Metric("omitted", 20, 200, 0.10, 8)],
            prior_page_rows=[gsc.Metric("https://example.com/", 5, 100, 0.05, 8)],
            min_impressions=1,
            min_prior_clicks=1,
        )
        self.assertEqual(report["opportunities"]["declining_queries"], [])
        self.assertTrue(
            any("not treated as zero" in item for item in report["limitations"])
        )


if __name__ == "__main__":
    unittest.main()
