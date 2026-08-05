#!/usr/bin/env python3
"""Derive repeatable opportunities from Google Search Console CSV exports."""

from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import json
import math
import os
import secrets
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

ALIASES = {
    "query": ("query", "top queries", "search query", "queries"),
    "page": ("page", "top pages", "landing page", "landing pages", "url"),
    "clicks": ("clicks",),
    "impressions": ("impressions",),
    "ctr": ("ctr", "click through rate", "click-through rate"),
    "position": ("position", "average position", "avg position"),
}
BUCKETS = (("1-3", 1, 4), ("4-10", 4, 11), ("11-20", 11, 21), ("21+", 21, math.inf))
_EXTERNAL_KEY = os.environ.get("SEO_QUERY_ID_KEY")
_PUBLIC_KEY = _EXTERNAL_KEY.encode() if _EXTERNAL_KEY else secrets.token_bytes(32)


class AnalysisError(ValueError):
    pass


@dataclass(frozen=True)
class Metric:
    key: str
    clicks: float
    impressions: float
    ctr: float
    position: float


@dataclass(frozen=True)
class QueryPage:
    query: str
    page: str
    clicks: float
    impressions: float
    ctr: float
    position: float


def _normalized(value: str) -> str:
    return " ".join(value.strip().lower().replace("_", " ").replace("-", " ").split())


def _column(fieldnames: Sequence[str], name: str) -> str:
    available = {_normalized(item): item for item in fieldnames if item}
    for alias in ALIASES[name]:
        if match := available.get(_normalized(alias)):
            return match
    raise AnalysisError(f"missing {name} column; accepted aliases: {ALIASES[name]}")


def _number(raw: str | None, name: str) -> float:
    text = (raw or "").strip().replace(",", "")
    if not text:
        raise AnalysisError(f"missing {name} value")
    try:
        value = float(text)
    except ValueError as error:
        raise AnalysisError(f"invalid {name} value: {raw!r}") from error
    if not math.isfinite(value):
        raise AnalysisError(f"non-finite {name} value: {raw!r}")
    return value


def ctr_value(raw: str | None) -> float:
    text = (raw or "").strip().replace(",", "")
    percent = text.endswith("%")
    value = _number(text[:-1] if percent else text, "ctr")
    if percent or value > 1:
        value /= 100
    if not 0 <= value <= 1:
        raise AnalysisError(f"ctr outside [0, 1]: {raw!r}")
    return value


def _values(row: dict[str, str], cols: dict[str, str], path: Path, line: int) -> tuple[float, float, float, float]:
    clicks = _number(row.get(cols["clicks"]), "clicks")
    impressions = _number(row.get(cols["impressions"]), "impressions")
    ctr = ctr_value(row.get(cols["ctr"]))
    position = _number(row.get(cols["position"]), "position")
    if min(clicks, impressions, position) < 0 or (impressions and clicks > impressions):
        raise AnalysisError(f"invalid metric values in {path}:{line}")
    return clicks, impressions, ctr, position


def read_metric_csv(path: Path, *, key_kind: str) -> list[Metric]:
    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
    except OSError as error:
        raise AnalysisError(f"cannot read {path}: {error}") from error
    output: list[Metric] = []
    with handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise AnalysisError(f"CSV has no header: {path}")
        cols = {name: _column(reader.fieldnames, name) for name in (key_kind, "clicks", "impressions", "ctr", "position")}
        for line, row in enumerate(reader, 2):
            key = (row.get(cols[key_kind]) or "").strip()
            if key:
                output.append(Metric(key, *_values(row, cols, path, line)))
    if not output:
        raise AnalysisError(f"no usable {key_kind} rows in {path}")
    return output


def read_query_page_csv(path: Path) -> list[QueryPage]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise AnalysisError(f"CSV has no header: {path}")
        cols = {name: _column(reader.fieldnames, name) for name in ("query", "page", "clicks", "impressions", "ctr", "position")}
        output = []
        for line, row in enumerate(reader, 2):
            query, page = (row.get(cols["query"]) or "").strip(), (row.get(cols["page"]) or "").strip()
            if query and page:
                output.append(QueryPage(query, page, *_values(row, cols, path, line)))
    if not output:
        raise AnalysisError(f"no usable query-page rows in {path}")
    return output


def _round(value: float) -> int | float:
    nearest = round(value)
    return int(nearest) if math.isclose(value, nearest, abs_tol=1e-9) else round(value, 3)


def _query_id(query: str) -> str:
    return "query-hmac:" + hmac.new(_PUBLIC_KEY, query.encode(), hashlib.sha256).hexdigest()[:16]


def _identity(key: str, kind: str, public_safe: bool) -> dict[str, str]:
    return {kind: _query_id(key) if kind == "query" and public_safe else key}


def _bucket(position: float) -> str:
    return next((name for name, low, high in BUCKETS if low <= position < high), "unknown")


def _summary(rows: Sequence[Metric]) -> dict[str, Any]:
    clicks, impressions = sum(r.clicks for r in rows), sum(r.impressions for r in rows)
    position = sum(r.position * r.impressions for r in rows) / impressions if impressions else statistics.fmean(r.position for r in rows)
    return {"rows": len(rows), "clicks": _round(clicks), "impressions": _round(impressions),
            "ctr": round(clicks / impressions if impressions else 0, 6), "position": round(position, 3)}


def _metric(row: Metric, kind: str, public_safe: bool) -> dict[str, Any]:
    return {**_identity(row.key, kind, public_safe), "clicks": _round(row.clicks),
            "impressions": _round(row.impressions), "ctr": round(row.ctr, 6), "position": round(row.position, 3)}


def _merged(rows: Sequence[Metric]) -> dict[str, Metric]:
    groups: dict[str, list[Metric]] = defaultdict(list)
    for row in rows:
        groups[row.key].append(row)
    output = {}
    for key, items in groups.items():
        clicks, impressions = sum(x.clicks for x in items), sum(x.impressions for x in items)
        position = sum(x.position * x.impressions for x in items) / impressions if impressions else statistics.fmean(x.position for x in items)
        output[key] = Metric(key, clicks, impressions, clicks / impressions if impressions else 0, position)
    return output


def _declines(current: Sequence[Metric], prior: Sequence[Metric] | None, kind: str, minimum: float,
              threshold: float, limit: int, public_safe: bool) -> list[dict[str, Any]]:
    if not prior:
        return []
    now, before, output = _merged(current), _merged(prior), []
    for key, old in before.items():
        if old.clicks < minimum:
            continue
        new = now.get(key, Metric(key, 0, 0, 0, old.position))
        change = (new.clicks - old.clicks) / old.clicks * 100
        if change <= threshold:
            output.append({**_identity(key, kind, public_safe), "clicks_current": _round(new.clicks),
                           "clicks_prior": _round(old.clicks), "clicks_change": _round(new.clicks - old.clicks),
                           "clicks_change_pct": round(change, 3), "position_current": round(new.position, 3),
                           "position_prior": round(old.position, 3)})
    return sorted(output, key=lambda item: (item["clicks_change"], item["clicks_change_pct"]))[:limit]


def declines(current: Sequence[Metric], prior: Sequence[Metric] | None, *, kind: str, minimum_clicks: float, threshold: float, limit: int, public_safe: bool) -> list[dict[str, Any]]:
    """Public wrapper used by tests and other deterministic tooling."""
    return _declines(current, prior, kind, minimum_clicks, threshold, limit, public_safe)


def _cannibalization(rows: Sequence[QueryPage] | None, minimum: float, secondary_share: float,
                     limit: int, public_safe: bool) -> list[dict[str, Any]]:
    groups: dict[str, list[QueryPage]] = defaultdict(list)
    for row in rows or []:
        if row.impressions >= minimum:
            groups[row.query].append(row)
    output = []
    for query, items in groups.items():
        if len(items) < 2:
            continue
        items.sort(key=lambda row: (-row.impressions, -row.clicks, row.page))
        total = sum(row.impressions for row in items)
        share = items[1].impressions / total if total else 0
        if share >= secondary_share:
            output.append({**_identity(query, "query", public_safe), "total_impressions": _round(total),
                           "secondary_impression_share": round(share, 4),
                           "pages": [{"page": row.page, "clicks": _round(row.clicks),
                                      "impressions": _round(row.impressions),
                                      "impression_share": round(row.impressions / total, 4),
                                      "ctr": round(row.ctr, 6), "position": round(row.position, 3)}
                                     for row in items[:5]]})
    return sorted(output, key=lambda item: (-float(item["total_impressions"]), -item["secondary_impression_share"]))[:limit]


def analyze(*, query_rows: Sequence[Metric], page_rows: Sequence[Metric],
            prior_query_rows: Sequence[Metric] | None = None, prior_page_rows: Sequence[Metric] | None = None,
            query_page_rows: Sequence[QueryPage] | None = None, min_impressions: float = 100,
            min_prior_clicks: float = 5, ctr_ratio: float = .7, decline_threshold_pct: float = -20,
            min_secondary_share: float = .15, limit: int = 20, public_safe: bool = False) -> dict[str, Any]:
    groups: dict[str, list[Metric]] = defaultdict(list)
    for row in query_rows:
        if row.impressions >= min_impressions:
            groups[_bucket(row.position)].append(row)
    medians = {name: statistics.median(x.ctr for x in items) for name, items in groups.items() if len(items) >= 2}
    low_ctr = [(row, medians[_bucket(row.position)]) for row in query_rows
               if row.impressions >= min_impressions and _bucket(row.position) in medians
               and row.ctr < medians[_bucket(row.position)] * ctr_ratio]
    low_ctr.sort(key=lambda item: (-(item[0].impressions * (item[1] - item[0].ctr)), item[0].key))
    striking = [row for row in query_rows if row.impressions >= min_impressions and 4 <= row.position <= 20]
    score = lambda row: row.impressions * max(0, min(1, (21 - row.position) / 17)) * (1 - row.ctr)
    striking.sort(key=lambda row: (-score(row), -row.impressions, row.position, row.key))
    bucket_summaries = []
    for name, _, _ in BUCKETS:
        items = [row for row in query_rows if _bucket(row.position) == name]
        bucket_summaries.append({"bucket": name, **(_summary(items) if items else
                                 {"rows": 0, "clicks": 0, "impressions": 0, "ctr": 0, "position": None})})
    limitations = [
        "Search Console exports may omit low-volume rows; this report describes only supplied rows.",
        "Opportunity lists are prioritization aids, not ranking or traffic forecasts.",
        "Equivalent finalized current and prior windows are required; CSV rows cannot prove window identity.",
    ]
    if not prior_query_rows or not prior_page_rows:
        limitations.append("One or more prior-period exports were absent, so decline analysis is partial.")
    if not query_page_rows:
        limitations.append("No query-page export was supplied, so cannibalization candidates were not computed.")
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "public_safe": public_safe,
        "parameters": {"min_impressions": min_impressions, "min_prior_clicks": min_prior_clicks,
                       "ctr_ratio": ctr_ratio, "decline_threshold_pct": decline_threshold_pct,
                       "min_secondary_share": min_secondary_share, "limit": limit},
        "summary": {"queries": _summary(query_rows), "pages": _summary(page_rows)},
        "position_buckets": bucket_summaries,
        "site_ctr_medians_by_position_bucket": {key: round(value, 6) for key, value in sorted(medians.items())},
        "opportunities": {
            "striking_distance_queries": [{**_metric(row, "query", public_safe),
                                             "opportunity_score": round(score(row), 3),
                                             "position_bucket": _bucket(row.position)} for row in striking[:limit]],
            "low_ctr_queries": [{**_metric(row, "query", public_safe), "position_bucket": _bucket(row.position),
                                  "site_bucket_median_ctr": round(median, 6),
                                  "ctr_vs_median_ratio": round(row.ctr / median, 4)} for row, median in low_ctr[:limit]],
            "declining_queries": _declines(query_rows, prior_query_rows, "query", min_prior_clicks,
                                            decline_threshold_pct, limit, public_safe),
            "declining_pages": _declines(page_rows, prior_page_rows, "page", min_prior_clicks,
                                          decline_threshold_pct, limit, public_safe),
            "cannibalization_candidates": _cannibalization(query_page_rows, min_impressions,
                                                             min_secondary_share, limit, public_safe),
        },
        "limitations": limitations,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-csv", type=Path, required=True)
    parser.add_argument("--page-csv", type=Path, required=True)
    parser.add_argument("--prior-query-csv", type=Path)
    parser.add_argument("--prior-page-csv", type=Path)
    parser.add_argument("--query-page-csv", type=Path)
    parser.add_argument("--min-impressions", type=float, default=100)
    parser.add_argument("--min-prior-clicks", type=float, default=5)
    parser.add_argument("--ctr-ratio", type=float, default=.7)
    parser.add_argument("--decline-threshold-pct", type=float, default=-20)
    parser.add_argument("--min-secondary-share", type=float, default=.15)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--public-safe", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if min(args.min_impressions, args.min_prior_clicks) < 0 or args.limit < 1:
            raise AnalysisError("minimums must be non-negative and limit must be positive")
        if not 0 < args.ctr_ratio < 1 or not 0 < args.min_secondary_share < 1:
            raise AnalysisError("ratio arguments must be between 0 and 1")
        if args.decline_threshold_pct >= 0:
            raise AnalysisError("--decline-threshold-pct must be negative")
        report = analyze(
            query_rows=read_metric_csv(args.query_csv, key_kind="query"),
            page_rows=read_metric_csv(args.page_csv, key_kind="page"),
            prior_query_rows=read_metric_csv(args.prior_query_csv, key_kind="query") if args.prior_query_csv else None,
            prior_page_rows=read_metric_csv(args.prior_page_csv, key_kind="page") if args.prior_page_csv else None,
            query_page_rows=read_query_page_csv(args.query_page_csv) if args.query_page_csv else None,
            min_impressions=args.min_impressions, min_prior_clicks=args.min_prior_clicks,
            ctr_ratio=args.ctr_ratio, decline_threshold_pct=args.decline_threshold_pct,
            min_secondary_share=args.min_secondary_share, limit=args.limit, public_safe=args.public_safe,
        )
        rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (AnalysisError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
