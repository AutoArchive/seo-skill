from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "site_snapshot.py"
SPEC = importlib.util.spec_from_file_location("site_snapshot", PATH)
assert SPEC and SPEC.loader
SITE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SITE)


def args(root: Path, **changes):
    values = dict(
        root=root,
        base_url="https://example.com",
        sitemap="sitemap.xml",
        route=[],
        exclude_html=[],
        ignore_link_prefix=[],
        require_title=False,
        require_one_h1=False,
        require_unique_titles=False,
        canonical="off",
        check_internal_links=False,
        check_sitemap_coverage=False,
        require_file=[],
        require_text=[],
        require_text_count=[],
        expect_sitemap_url=[],
        forbid_sitemap_url=[],
        sitemap_exact=False,
        output=None,
        baseline=None,
        diff_output=None,
        snapshot_only=False,
    )
    values.update(changes)
    return Namespace(**values)


def page(title: str, route: str, body: str = "", links: str = "") -> str:
    canonical = "https://example.com/" if route == "/" else f"https://example.com{route}"
    return f"<html><head><title>{title}</title><link rel='canonical' href='{canonical}'></head><body><h1>{title}</h1>{body}{links}</body></html>"


def write(root: Path, relative: str, text: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_sitemap(root: Path, urls: list[tuple[str, str]]) -> None:
    rows = "".join(f"<url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>" for url, lastmod in urls)
    write(root, "sitemap.xml", f"<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>{rows}</urlset>")


class SiteSnapshotTests(unittest.TestCase):
    def test_common_checks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "index.html", page("Home", "/", links="<a href='/docs/'>Docs</a>"))
            write(root, "docs/index.html", page("Docs", "/docs/"))
            write_sitemap(root, [("https://example.com/", "2026-08-01"), ("https://example.com/docs/", "2026-08-02")])
            options = args(root, require_title=True, require_one_h1=True, require_unique_titles=True, canonical="same-route", check_internal_links=True, check_sitemap_coverage=True)
            self.assertEqual(SITE.selected_failures(SITE.scan(options), options), {})

    def test_common_failures_are_selected_only_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "index.html", "<html><body><a href='/missing/'>Missing</a></body></html>")
            write_sitemap(root, [])
            options = args(root, require_title=True, require_one_h1=True, canonical="present", check_internal_links=True, check_sitemap_coverage=True)
            failures = SITE.selected_failures(SITE.scan(options), options)
            self.assertIn("missing_titles", failures)
            self.assertIn("h1_mismatches", failures)
            self.assertIn("missing_canonicals", failures)
            self.assertIn("broken_internal_links", failures)

    def test_required_text_and_exact_sitemap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "index.html", page("Home", "/") + "G-TEST G-TEST")
            write(root, "robots.txt", "Sitemap: https://example.com/sitemap.xml")
            write(root, "404.html", "not found")
            write_sitemap(root, [("https://example.com/", "")])
            options = args(root, route=["/"], require_file=["404.html"], require_text=[["robots.txt", "sitemap.xml"]], require_text_count=[["index.html", "G-TEST", "2"]], expect_sitemap_url=["https://example.com/"], sitemap_exact=True)
            self.assertEqual(SITE.selected_failures(SITE.scan(options), options), {})

    def test_snapshot_diff_tracks_page_and_sitemap_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "index.html", page("Old", "/"))
            write_sitemap(root, [("https://example.com/", "2026-08-01")])
            before = SITE.scan(args(root))
            write(root, "index.html", page("New", "/"))
            write(root, "docs/index.html", page("Docs", "/docs/"))
            write_sitemap(root, [("https://example.com/", "2026-08-02"), ("https://example.com/docs/", "2026-08-02")])
            after = SITE.scan(args(root))
            delta = SITE.diff(before, after)
            self.assertEqual(delta["pages_added"], ["/docs/"])
            self.assertIn("title", delta["pages_changed"]["/"])
            self.assertEqual(delta["sitemap_urls_added"], ["https://example.com/docs"])
            self.assertIn("https://example.com/", delta["sitemap_lastmod_changed"])
            self.assertIn("Pages added (1)", SITE.markdown(delta))

    def test_snapshot_json_is_portable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, "index.html", page("Home", "/"))
            write_sitemap(root, [("https://example.com/", "")])
            snapshot = SITE.scan(args(root))
            path = root / "snapshot.json"
            SITE.write_json(path, snapshot)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["schema_version"], 1)
            self.assertIn("/", loaded["pages"])


if __name__ == "__main__":
    unittest.main()
