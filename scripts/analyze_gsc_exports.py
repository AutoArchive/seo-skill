#!/usr/bin/env python3
"""Policy-safe public entry point for deterministic Search Console analysis."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from typing import Any

import _gsc_analysis as _impl

AnalysisError = _impl.AnalysisError
Metric = _impl.Metric
QueryPage = _impl.QueryPage
ctr_value = _impl.ctr_value
read_metric_csv = _impl.read_metric_csv
read_query_page_csv = _impl.read_query_page_csv

_MISSING_ROW_LIMITATION = (
    "Keys absent from the current export are not treated as zero because "
    "Search Console may omit rows."
)


def _public_key(key: str, kind: str, public_safe: bool) -> str:
    return _impl._query_id(key) if kind == "query" and public_safe else key


def declines(
    current: Sequence[Metric],
    prior: Sequence[Metric] | None,
    *,
    kind: str,
    minimum_clicks: float,
    threshold: float,
    limit: int,
    public_safe: bool,
) -> list[dict[str, Any]]:
    """Compare only keys present in both finalized exports.

    Search Console can omit rows, so absence from an export is not interpreted as
    zero clicks. This function intentionally narrows the implementation's raw
    candidate set at the public policy boundary.
    """
    if not prior:
        return []
    current_map = _impl._merged(current)
    prior_map = _impl._merged(prior)
    output: list[dict[str, Any]] = []
    for key, old in prior_map.items():
        if old.clicks < minimum_clicks:
            continue
        new = current_map.get(key)
        if new is None:
            continue
        change = (new.clicks - old.clicks) / old.clicks * 100
        if change <= threshold:
            output.append(
                {
                    **_impl._identity(key, kind, public_safe),
                    "clicks_current": _impl._round(new.clicks),
                    "clicks_prior": _impl._round(old.clicks),
                    "clicks_change": _impl._round(new.clicks - old.clicks),
                    "clicks_change_pct": round(change, 3),
                    "position_current": round(new.position, 3),
                    "position_prior": round(old.position, 3),
                }
            )
    return sorted(
        output,
        key=lambda item: (item["clicks_change"], item["clicks_change_pct"]),
    )[:limit]


def analyze(
    *,
    query_rows: Sequence[Metric],
    page_rows: Sequence[Metric],
    prior_query_rows: Sequence[Metric] | None = None,
    prior_page_rows: Sequence[Metric] | None = None,
    query_page_rows: Sequence[QueryPage] | None = None,
    min_impressions: float = 100,
    min_prior_clicks: float = 5,
    ctr_ratio: float = 0.7,
    decline_threshold_pct: float = -20,
    min_secondary_share: float = 0.15,
    limit: int = 20,
    public_safe: bool = False,
) -> dict[str, Any]:
    report = _impl.analyze(
        query_rows=query_rows,
        page_rows=page_rows,
        prior_query_rows=prior_query_rows,
        prior_page_rows=prior_page_rows,
        query_page_rows=query_page_rows,
        min_impressions=min_impressions,
        min_prior_clicks=min_prior_clicks,
        ctr_ratio=ctr_ratio,
        decline_threshold_pct=decline_threshold_pct,
        min_secondary_share=min_secondary_share,
        limit=limit,
        public_safe=public_safe,
    )
    report["opportunities"]["declining_queries"] = declines(
        query_rows,
        prior_query_rows,
        kind="query",
        minimum_clicks=min_prior_clicks,
        threshold=decline_threshold_pct,
        limit=limit,
        public_safe=public_safe,
    )
    report["opportunities"]["declining_pages"] = declines(
        page_rows,
        prior_page_rows,
        kind="page",
        minimum_clicks=min_prior_clicks,
        threshold=decline_threshold_pct,
        limit=limit,
        public_safe=public_safe,
    )
    if _MISSING_ROW_LIMITATION not in report["limitations"]:
        report["limitations"].append(_MISSING_ROW_LIMITATION)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    args = _impl._parser().parse_args(argv)
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
            prior_query_rows=(
                read_metric_csv(args.prior_query_csv, key_kind="query")
                if args.prior_query_csv
                else None
            ),
            prior_page_rows=(
                read_metric_csv(args.prior_page_csv, key_kind="page")
                if args.prior_page_csv
                else None
            ),
            query_page_rows=(
                read_query_page_csv(args.query_page_csv)
                if args.query_page_csv
                else None
            ),
            min_impressions=args.min_impressions,
            min_prior_clicks=args.min_prior_clicks,
            ctr_ratio=args.ctr_ratio,
            decline_threshold_pct=args.decline_threshold_pct,
            min_secondary_share=args.min_secondary_share,
            limit=args.limit,
            public_safe=args.public_safe,
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
