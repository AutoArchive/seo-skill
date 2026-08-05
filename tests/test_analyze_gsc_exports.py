from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import analyze_gsc_exports as gsc  # noqa: E402


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ParseTests(unittest.TestCase):
    def test_ctr_accepts_percent_and_ratio(self) -> None:
        self.assertAlmostEqual(gsc.ctr_value("2.5%"), 0.025)
        self.assertAlmostEqual(gsc.ctr_value("0.025"), 0.025)
        self.assertAlmostEqual(gsc.ctr_value("2.5"), 0.025)

    def test_header_aliases_and_bom_are_supported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queries.csv"
            path.write_text(
                "\ufeffTop queries,Clicks,Impressions,CTR,Average position\n"
                "ebpf profiler,12,1000,1.2%,8.4\n",
                encoding="utf-8",
            )
            rows = gsc.read_metric_csv(path, key_kind="query")
        self.assertEqual(rows[0].key, "ebpf profiler")
        self.assertAlmostEqual(rows[0].ctr, 0.012)
        self.assertAlmostEqual(rows[0].position, 8.4)


class AnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.current_queries = [
            gsc.Metric("high ctr", 100, 1000, 0.10, 7.0),
            gsc.Metric("low ctr", 5, 1000, 0.005, 7.5),
            gsc.Metric("declining query", 20, 800, 0.025, 12.0),
            gsc.Metric("top query", 200, 1000, 0.20, 2.0),
        ]
        self.prior_queries = [
            gsc.Metric("high ctr", 90, 900, 0.10, 7.2),
            gsc.Metric("low ctr", 4, 900, 0.004444, 7.7),
            gsc.Metric("declining query", 80, 1000, 0.08, 8.0),
            gsc.Metric("top query", 190, 950, 0.20, 2.1),
        ]
        self.current_pages = [
            gsc.Metric("https://example.com/a", 20, 1000, 0.02, 10.0),
            gsc.Metric("https://example.com/b", 10, 500, 0.02, 15.0),
        ]
        self.prior_pages = [
            gsc.Metric("https://example.com/a", 50, 1100, 0.04545, 8.0),
            gsc.Metric("https://example.com/b", 8, 450, 0.01778, 15.5),
        ]
        self.query_pages = [
            gsc.QueryPage("shared query", "https://example.com/a", 8, 600, 0.0133, 8.0),
            gsc.QueryPage("shared query", "https://example.com/b", 5, 400, 0.0125, 11.0),
            gsc.QueryPage("single query", "https://example.com/a", 3, 500, 0.006, 14.0),
        ]

    def test_opportunities_declines_and_cannibalization(self) -> None:
        report = gsc.analyze(
            query_rows=self.current_queries,
            page_rows=self.current_pages,
            prior_query_rows=self.prior_queries,
            prior_page_rows=self.prior_pages,
            query_page_rows=self.query_pages,
            min_impressions=100,
            min_prior_clicks=5,
            ctr_ratio=0.7,
            decline_threshold_pct=-20,
            min_secondary_share=0.15,
            limit=20,
        )
        opportunities = report["opportunities"]
        self.assertIn(
            "low ctr",
            [item["query"] for item in opportunities["low_ctr_queries"]],
        )
        declining_queries = {
            item["query"]: item for item in opportunities["declining_queries"]
        }
        self.assertEqual(declining_queries["declining query"]["clicks_change"], -60)
        declining_pages = {
            item["page"]: item for item in opportunities["declining_pages"]
        }
        self.assertEqual(declining_pages["https://example.com/a"]["clicks_change"], -30)
        self.assertEqual(
            opportunities["cannibalization_candidates"][0]["query"],
            "shared query",
        )

    def test_public_safe_hashes_queries_but_not_pages(self) -> None:
        report = gsc.analyze(
            query_rows=self.current_queries,
            page_rows=self.current_pages,
            prior_query_rows=self.prior_queries,
            prior_page_rows=self.prior_pages,
            query_page_rows=self.query_pages,
            min_impressions=100,
            public_safe=True,
        )
        striking = report["opportunities"]["striking_distance_queries"]
        self.assertTrue(all(item["query"].startswith("query-hmac:") for item in striking))
        declining_pages = report["opportunities"]["declining_pages"]
        self.assertEqual(declining_pages[0]["page"], "https://example.com/a")
        rendered = json.dumps(report)
        for query in ("high ctr", "low ctr", "declining query", "shared query"):
            self.assertNotIn(f'"query": "{query}"', rendered)

    def test_duplicate_rows_are_aggregated_for_period_comparison(self) -> None:
        current = [
            gsc.Metric("q", 5, 100, 0.05, 10),
            gsc.Metric("q", 5, 100, 0.05, 12),
        ]
        prior = [gsc.Metric("q", 20, 200, 0.10, 8)]
        result = gsc.declines(
            current,
            prior,
            kind="query",
            minimum_clicks=1,
            threshold=-20,
            limit=10,
            public_safe=False,
        )
        self.assertEqual(result[0]["clicks_current"], 10)
        self.assertEqual(result[0]["clicks_change_pct"], -50.0)


class CliTests(unittest.TestCase):
    def test_cli_writes_public_safe_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            query_path = directory_path / "query.csv"
            page_path = directory_path / "page.csv"
            output_path = directory_path / "report.json"
            write_csv(
                query_path,
                ["Query", "Clicks", "Impressions", "CTR", "Position"],
                [
                    {
                        "Query": "private query text",
                        "Clicks": 10,
                        "Impressions": 1000,
                        "CTR": "1%",
                        "Position": 8,
                    }
                ],
            )
            write_csv(
                page_path,
                ["Page", "Clicks", "Impressions", "CTR", "Position"],
                [
                    {
                        "Page": "https://example.com/",
                        "Clicks": 10,
                        "Impressions": 1000,
                        "CTR": "1%",
                        "Position": 8,
                    }
                ],
            )
            exit_code = gsc.main(
                [
                    "--query-csv",
                    str(query_path),
                    "--page-csv",
                    str(page_path),
                    "--public-safe",
                    "--output",
                    str(output_path),
                    "--min-impressions",
                    "1",
                ]
            )
            report = output_path.read_text(encoding="utf-8")
        self.assertEqual(exit_code, 0)
        self.assertNotIn("private query text", report)
        self.assertIn("query-hmac:", report)


if __name__ == "__main__":
    unittest.main()
