---
name: collect-seo-data
description: Collect and normalize public-safe SEO evidence for one website from Google Drive exports of Google Analytics 4 and Search Console and from Cloudflare analytics through MCP or GraphQL. Use for a daily or weekly SEO refresh, analytics reconciliation, evidence-backed SEO audit, or update to .github/seo-data.
---

# Collect SEO Data

## Overview

Collect read-only evidence for exactly one configured site, keep raw data out of
Git, update the site's Markdown operating record, and deliver each run through
anonymous direct commits with exact-commit CI verification.

## Required context

From the consuming repository root, read completely:

- repository instructions such as `AGENTS.md` or `CLAUDE.md`;
- `.github/seo-data/site.md` and `daily-task.md`;
- `.github/seo-data/status.md`, `plan.md`, and `block.md`;
- `.github/seo-data/promotion.md` when data supports a promotion decision;
- the newest relevant file under `.github/seo-data/daily/`.

Read [`references/google-drive.md`](references/google-drive.md),
[`references/cloudflare.md`](references/cloudflare.md), and
[`../../references/direct-delivery.md`](../../references/direct-delivery.md)
before collection or delivery.

Stop rather than combine unrelated properties if `site.md` is missing or names
more than one canonical site. Do not put credentials or private source IDs into
Markdown metadata.

## Workflow

### 1. Synchronize the default branch and skills

Inspect the default branch, upstream, dirty files, and submodule state. Require a
clean local default branch and fast-forward it to its remote. Preserve unrelated
work; never stash, reset, or force-push it.

Fetch the `seo-skills` submodule remote. If its allowed default branch has a
newer commit, update the submodule pointer in the same daily commit and record
both old and new commits. If there is no update, say so. Never edit shared skill
files from the consuming repository.

### 2. Establish the data window

Use the site timezone, lookback, and finalization lag documented in `site.md`.
Prefer finalized data. If a source only offers fresh or partial data, label it
partial and record its watermark. Do not compare partial and final periods as
though they were equivalent.

### 3. Read Google exports from Drive

Resolve the configured folder by exact name, exclude trashed items, and select
files using documented filename patterns and the time window. Read matching CSV
files without moving, renaming, sharing, or rewriting them.

Google Drive is the artifact store. Each export must identify GA4 or Search
Console and preserve its metric semantics. Treat missing files, duplicate
folders, schema drift, truncation, and stale data as evidence; never turn them
into zero or guess missing values.

### 4. Read Cloudflare analytics

Discover current Cloudflare MCP tools at runtime. Prefer the official GraphQL
Analytics MCP server. Use the general Cloudflare MCP or GraphQL Analytics API
only as a read-only fallback. Resolve exactly one zone by the hostname in
`site.md`, query the same window, request only needed aggregates, and inspect
both returned data and GraphQL errors.

Do not mutate DNS, cache, Workers, Pages, security, or analytics settings.

### 5. Update Markdown state

Write or append `.github/seo-data/daily/YYYY-MM-DD.md` using the site's local
date and `templates/seo-data/daily.example.md`. Record:

- scope, window, source status, and finalization state;
- aggregate source-native metrics labelled `GA4`, `GSC`, or `Cloudflare`;
- export filenames and optional SHA-256 checksums, never Drive URLs or IDs;
- work performed, submodule movement, validation, decisions, and follow-ups;
- delivery facts known before the main commit.

Update `status.md` with the newest verified window and signals. Keep future work
in `plan.md`. Put an item in `block.md` only when an external system genuinely
requires a human-only act or the required permission does not exist.

Raw rows, search queries, user events, IP addresses, emails, credentials,
private URLs, account IDs, zone IDs, and Drive file/folder IDs stay outside Git.

### 6. Validate, review, commit, and push

Run:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data
```

Run relevant repository tests. Self-review the complete intended diff. Configure
the repository-local anonymous name and email from `site.md`, verify their
effective values and origins, stage explicit paths, and commit on the default
branch. Fetch once more; if the remote advanced, rebase only this automation
commit, rerun validation and review, then push normally. Never open a pull
request, force-push, or amend already-pushed history.

### 7. Wait for CI and close out

Wait for all expected CI checks associated with the exact pushed commit. Missing,
queued, skipped, cancelled, timed-out, or failed checks are not success. Diagnose
failures and push a narrow corrective commit, then wait for the new commit's CI.

After success, push one metadata-only anonymous closeout commit that records the
main commit and CI evidence in today's report and `status.md`. Validate and
self-review its diff and wait for its exact-commit CI. A collection-only run
does not require deployment waiting unless metadata changes rendered output.

## Failure rules

- An HTTP success or non-empty file does not prove complete data; verify dates,
  pagination, schema, finalization, sampling, and GraphQL errors.
- Preserve source semantics. Cloudflare visits, GA4 sessions/users, and Search
  Console clicks are different metrics.
- If a safe automated path is unavailable, record exact evidence in `block.md`
  through an anonymous direct commit; do not fabricate completion.
- If metrics are unchanged, today's Markdown entry is still the daily change
  and is delivered through the same anonymous direct-commit lifecycle.
