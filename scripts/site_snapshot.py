#!/usr/bin/env python3
"""Optional static-site SEO checks and sitemap/build snapshot diffs.

Uses only the Python standard library. Site-specific content, deployment, and
provider rules belong in the consuming repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import sys
from collections import defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

SCHEMA = 1
DEFAULT_EXCLUDES = {"404.html", "500.html"}


class Error(ValueError):
    pass


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts: list[str] = []
        self.h1 = 0
        self.canonical = ""
        self.description = ""
        self.robots = ""
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): v or "" for k, v in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "link" and "canonical" in attrs.get("rel", "").casefold().split():
            self.canonical = attrs.get("href", "").strip()
        elif tag == "meta":
            name = attrs.get("name", "").casefold()
            if name == "description":
                self.description = attrs.get("content", "").strip()
            elif name == "robots":
                self.robots = attrs.get("content", "").strip()
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key].strip())

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def canon(url: str) -> str:
    p = urlsplit(url)
    path = p.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((p.scheme.casefold(), p.netloc.casefold(), path, "", ""))


def base_url(value: str) -> str:
    p = urlsplit(value)
    if p.scheme not in {"http", "https"} or not p.netloc:
        raise Error(f"invalid base URL: {value!r}")
    return urlunsplit((p.scheme, p.netloc, p.path.rstrip("/"), "", ""))


def route_url(base: str, route: str) -> str:
    return f"{base}/" if route == "/" else f"{base}{route}"


def file_route(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return f"/{rel[:-10].strip('/')}/"
    return f"/{rel[:-5].strip('/')}"


def candidates(root: Path, route: str) -> list[Path]:
    path = unquote(urlsplit(route).path or "/")
    norm = posixpath.normpath(path)
    if path.endswith("/") and not norm.endswith("/"):
        norm += "/"
    if norm in {"", ".", "/"}:
        return [root / "index.html"]
    rel = norm.lstrip("/")
    direct = root / PurePosixPath(rel)
    if norm.endswith("/"):
        return [direct / "index.html"]
    return [direct] if PurePosixPath(rel).suffix else [direct, root / f"{rel}.html", direct / "index.html"]


def discover(root: Path, excludes: set[str]) -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root).as_posix()
        if rel in excludes or path.name in excludes:
            continue
        route = file_route(root, path)
        if route in pages:
            raise Error(f"multiple files map to {route}: {pages[route]} and {path}")
        pages[route] = path
    if not pages:
        raise Error(f"no HTML files under {root}")
    return pages


def sitemap(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if not path.is_file():
        raise Error(f"missing sitemap: {path}")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise Error(f"invalid sitemap {path}: {exc}") from exc
    result: dict[str, str] = {}
    for node in root.iter():
        if not node.tag.endswith("url"):
            continue
        loc = lastmod = ""
        for child in node:
            if child.tag.endswith("loc") and child.text:
                loc = child.text.strip()
            elif child.tag.endswith("lastmod") and child.text:
                lastmod = child.text.strip()
        if loc:
            result[canon(loc)] = lastmod
    return result


def internal(base: str, route: str, value: str) -> str | None:
    value = value.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    absolute = urljoin(route_url(base, route), value)
    p = urlsplit(absolute)
    if p.scheme not in {"http", "https"} or p.netloc.casefold() != urlsplit(base).netloc.casefold():
        return None
    path = unquote(p.path or "/")
    if path != "/" and value.endswith("/") and not path.endswith("/"):
        path += "/"
    return path


def select_routes(found: dict[str, Path], requested: list[str]) -> list[str]:
    if not requested:
        return sorted(found)
    selected: list[str] = []
    for raw in requested:
        route = raw if raw.startswith("/") else f"/{raw}"
        match = route if route in found else next((r for r in found if r.rstrip("/") == route.rstrip("/")), None)
        if match is None:
            raise Error(f"generated route not found: {route}")
        if match not in selected:
            selected.append(match)
    return sorted(selected)


def read_page(root: Path, path: Path, route: str, base: str) -> dict[str, object]:
    data = path.read_bytes()
    parser = Page()
    try:
        parser.feed(data.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise Error(f"HTML is not UTF-8: {path}") from exc
    links = sorted({target for value in parser.links if (target := internal(base, route, value))})
    return {
        "file": path.relative_to(root).as_posix(),
        "title": parser.title,
        "description": parser.description,
        "h1_count": parser.h1,
        "canonical": urljoin(route_url(base, route), parser.canonical) if parser.canonical else "",
        "robots": parser.robots,
        "content_hash": hashlib.sha256(data).hexdigest(),
        "internal_targets": links,
    }


def text_failures(root: Path, required: list[list[str]], counted: list[list[str]]) -> list[dict[str, object]]:
    failures: list[dict[str, object]] = []
    checks = [(file, text, 1) for file, text in required]
    for file, text, raw_count in counted:
        try:
            count = int(raw_count)
        except ValueError as exc:
            raise Error(f"invalid text count: {raw_count!r}") from exc
        if count < 1:
            raise Error("text count must be positive")
        checks.append((file, text, count))
    for file, text, count in checks:
        path = root / file
        observed = path.read_text(encoding="utf-8").count(text) if path.is_file() else 0
        if observed < count:
            failures.append({"file": file, "text": text, "required": count, "observed": observed})
    return failures


def scan(args: argparse.Namespace) -> dict[str, object]:
    root = args.root.resolve()
    if not root.is_dir():
        raise Error(f"missing output root: {root}")
    base = base_url(args.base_url)
    found = discover(root, DEFAULT_EXCLUDES | set(args.exclude_html))
    routes = select_routes(found, args.route)
    sm_path = root / args.sitemap if args.sitemap else None
    sm = sitemap(sm_path)
    same_site = {url: value for url, value in sm.items() if urlsplit(url).netloc.casefold() == urlsplit(base).netloc.casefold()}

    pages: dict[str, dict[str, object]] = {}
    for route in routes:
        page = read_page(root, found[route], route, base)
        url = canon(route_url(base, route))
        page["in_sitemap"] = url in same_site
        page["sitemap_lastmod"] = same_site.get(url, "")
        pages[route] = page

    titles: dict[str, list[str]] = defaultdict(list)
    for route, page in pages.items():
        if page["title"]:
            titles[str(page["title"])].append(route)

    ignored = tuple(args.ignore_link_prefix or ["/_next/"])
    broken: dict[str, list[str]] = {}
    for route, page in pages.items():
        missing = [target for target in page["internal_targets"] if not any(str(target).startswith(p) for p in ignored) and not any(p.exists() for p in candidates(root, str(target)))]
        if missing:
            broken[route] = sorted(set(missing))

    build_urls = {canon(route_url(base, route)) for route, page in pages.items() if "noindex" not in str(page["robots"]).casefold()}
    expected = {canon(url) for url in args.expect_sitemap_url}
    forbidden = {canon(url) for url in args.forbid_sitemap_url}
    issues = {
        "missing_titles": sorted(r for r, p in pages.items() if not p["title"]),
        "duplicate_titles": {t: sorted(rs) for t, rs in titles.items() if len(rs) > 1},
        "h1_mismatches": {r: p["h1_count"] for r, p in pages.items() if p["h1_count"] != 1},
        "missing_canonicals": sorted(r for r, p in pages.items() if not p["canonical"]),
        "canonical_mismatches": {r: {"expected": route_url(base, r), "observed": p["canonical"]} for r, p in pages.items() if p["canonical"] and canon(str(p["canonical"])) != canon(route_url(base, r))},
        "broken_internal_links": broken,
        "build_not_in_sitemap": sorted(build_urls - set(same_site)),
        "sitemap_not_in_build": sorted(set(same_site) - build_urls),
        "missing_required_files": sorted(file for file in args.require_file if not (root / file).exists()),
        "required_text_failures": text_failures(root, args.require_text, args.require_text_count),
        "missing_expected_sitemap_urls": sorted(expected - set(same_site)),
        "forbidden_sitemap_urls": sorted(forbidden & set(same_site)),
        "unexpected_sitemap_urls": sorted(set(same_site) - expected) if args.sitemap_exact else [],
    }
    return {
        "schema_version": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "base_url": base,
        "pages": pages,
        "sitemap": {"path": str(sm_path) if sm_path else None, "urls": dict(sorted(same_site.items()))},
        "issues": issues,
    }


def selected_failures(snapshot: dict[str, object], args: argparse.Namespace) -> dict[str, object]:
    issues = snapshot["issues"]
    enabled = {
        "missing_titles": args.require_title,
        "duplicate_titles": args.require_unique_titles,
        "h1_mismatches": args.require_one_h1,
        "missing_canonicals": args.canonical in {"present", "same-route"},
        "canonical_mismatches": args.canonical == "same-route",
        "broken_internal_links": args.check_internal_links,
        "build_not_in_sitemap": args.check_sitemap_coverage,
        "sitemap_not_in_build": args.check_sitemap_coverage,
        "missing_required_files": True,
        "required_text_failures": True,
        "missing_expected_sitemap_urls": True,
        "forbidden_sitemap_urls": True,
        "unexpected_sitemap_urls": args.sitemap_exact,
    }
    return {name: value for name, value in issues.items() if enabled[name] and value}


def diff(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    old_pages, new_pages = before.get("pages", {}), after.get("pages", {})
    old_routes, new_routes = set(old_pages), set(new_pages)
    fields = ("title", "description", "h1_count", "canonical", "robots", "content_hash", "in_sitemap", "sitemap_lastmod")
    changed = {}
    for route in sorted(old_routes & new_routes):
        values = {field: {"before": old_pages[route].get(field), "after": new_pages[route].get(field)} for field in fields if old_pages[route].get(field) != new_pages[route].get(field)}
        if values:
            changed[route] = values
    old_sm = before.get("sitemap", {}).get("urls", {})
    new_sm = after.get("sitemap", {}).get("urls", {})
    return {
        "pages_added": sorted(new_routes - old_routes),
        "pages_removed": sorted(old_routes - new_routes),
        "pages_changed": changed,
        "sitemap_urls_added": sorted(set(new_sm) - set(old_sm)),
        "sitemap_urls_removed": sorted(set(old_sm) - set(new_sm)),
        "sitemap_lastmod_changed": {url: {"before": old_sm[url], "after": new_sm[url]} for url in sorted(set(old_sm) & set(new_sm)) if old_sm[url] != new_sm[url]},
    }


def markdown(delta: dict[str, object]) -> str:
    lines = ["# Static site snapshot diff", ""]
    for title, key in (("Pages added", "pages_added"), ("Pages removed", "pages_removed"), ("Sitemap URLs added", "sitemap_urls_added"), ("Sitemap URLs removed", "sitemap_urls_removed")):
        items = delta[key]
        lines += [f"## {title} ({len(items)})", *([f"- `{item}`" for item in items] or ["- None"]), ""]
    changes = delta["pages_changed"]
    lines += [f"## Pages changed ({len(changes)})", *([f"- `{route}`: {', '.join(sorted(values))}" for route, values in changes.items()] or ["- None"]), ""]
    lastmod = delta["sitemap_lastmod_changed"]
    lines += [f"## Sitemap lastmod changed ({len(lastmod)})", *([f"- `{url}`: `{value['before']}` → `{value['after']}`" for url, value in lastmod.items()] or ["- None"]), ""]
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def arguments() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--base-url", required=True)
    p.add_argument("--sitemap")
    p.add_argument("--route", action="append", default=[])
    p.add_argument("--exclude-html", action="append", default=[])
    p.add_argument("--ignore-link-prefix", action="append", default=[])
    p.add_argument("--require-title", action="store_true")
    p.add_argument("--require-one-h1", action="store_true")
    p.add_argument("--require-unique-titles", action="store_true")
    p.add_argument("--canonical", choices=("off", "present", "same-route"), default="off")
    p.add_argument("--check-internal-links", action="store_true")
    p.add_argument("--check-sitemap-coverage", action="store_true")
    p.add_argument("--require-file", action="append", default=[])
    p.add_argument("--require-text", action="append", nargs=2, default=[], metavar=("FILE", "TEXT"))
    p.add_argument("--require-text-count", action="append", nargs=3, default=[], metavar=("FILE", "TEXT", "COUNT"))
    p.add_argument("--expect-sitemap-url", action="append", default=[])
    p.add_argument("--forbid-sitemap-url", action="append", default=[])
    p.add_argument("--sitemap-exact", action="store_true")
    p.add_argument("--output", type=Path, help="optional JSON snapshot")
    p.add_argument("--baseline", type=Path, help="optional earlier snapshot")
    p.add_argument("--diff-output", type=Path, help="optional Markdown increment log")
    p.add_argument("--snapshot-only", action="store_true", help="record facts without failing selected checks")
    return p.parse_args()


def main() -> int:
    args = arguments()
    try:
        snapshot = scan(args)
        if args.output:
            write_json(args.output, snapshot)
        if args.baseline:
            try:
                before = json.loads(args.baseline.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise Error(f"cannot read baseline {args.baseline}: {exc}") from exc
            if before.get("schema_version") != SCHEMA:
                raise Error(f"unsupported baseline schema: {args.baseline}")
            text = markdown(diff(before, snapshot))
            if args.diff_output:
                args.diff_output.parent.mkdir(parents=True, exist_ok=True)
                args.diff_output.write_text(text, encoding="utf-8")
            else:
                print(text)
        failures = {} if args.snapshot_only else selected_failures(snapshot, args)
        pages = snapshot["pages"]
        urls = snapshot["sitemap"]["urls"]
        print(f"Static SEO snapshot: {len(pages)} pages, {len(urls)} sitemap URLs.")
        if failures:
            print(json.dumps(failures, ensure_ascii=False, indent=2, sort_keys=True), file=sys.stderr)
            return 1
        print("Selected optional checks passed.")
        return 0
    except (OSError, UnicodeError, Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
