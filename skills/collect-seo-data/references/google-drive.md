# Google Drive collection

Use this reference when reading GA4 or Search Console CSV exports stored in
Google Drive.

## Folder and file resolution

1. Read the exact Google Drive folder name from `.github/seo-data/site.md`.
2. Search for a non-trashed folder with that exact name. Include the expected
   parent when the connector supports it.
3. If multiple folders remain, compare parent and owner metadata. Stop as
   ambiguous if one exact folder still cannot be established.
4. List all matching files with pagination and request only useful metadata:
   name, MIME type, modified time, size, checksum, and revision information.
5. Apply the documented GA4 and Search Console filename patterns and run window.
6. Download or stream read-only. Do not rename, move, share, or delete anything.

The Drive API `files.list` method supports search expressions, pagination, and
selective response fields:
<https://developers.google.com/workspace/drive/api/guides/search-files>

## Expected export identity

Prefer deterministic filenames:

```text
ga4-YYYY-MM-DD_YYYY-MM-DD.csv
gsc-query-YYYY-MM-DD_YYYY-MM-DD.csv
gsc-page-YYYY-MM-DD_YYYY-MM-DD.csv
gsc-device-YYYY-MM-DD_YYYY-MM-DD.csv
```

The export or sidecar manifest should identify the canonical site, source,
window, timezone, export time, dimensions, metrics, finalization state, and any
sampling, thresholding, or truncation. Do not silently merge files whose date
ranges, property identity, or aggregation semantics differ.

## Search Console semantics

Typical aggregate metrics are clicks, impressions, CTR, and average position.
Detailed query and page rows remain external. The Search Analytics API uses
Pacific Time dates, can return incomplete recent data, and does not guarantee
every underlying row. Exporters must paginate and record finalization state:
<https://developers.google.com/webmaster-tools/v1/searchanalytics/query>

For higher-volume sites, Search Console bulk export can place daily data in
BigQuery. This is an exporter alternative, not permission to commit BigQuery
identifiers or credentials:
<https://support.google.com/webmasters/answer/12919198?hl=en>

## GA4 semantics

Preserve definitions supplied by the exporter. Useful aggregates can include
sessions, active users, new users, engaged sessions, engagement rate, views,
and key events. Do not equate Cloudflare visits with GA4 sessions or users.

GA4 BigQuery export uses daily event tables that can receive late updates. When
Drive CSVs come from BigQuery, record the query window and refresh policy in the
external export manifest:
<https://support.google.com/analytics/answer/7029846?hl=en-EN>

## Missing or stale files

- Missing expected export: source is blocked or partial; never emit zero.
- Stale export: record the newest available watermark and partial status.
- Changed headers: stop normalization for that file and record schema drift.
- Duplicate data: deduplicate only with documented export identity.
