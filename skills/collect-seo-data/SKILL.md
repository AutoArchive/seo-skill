---
name: collect-seo-data
description: Collect and normalize public-safe SEO evidence for one website from Google Drive exports of Google Analytics 4 and Search Console and from Cloudflare analytics through MCP or GraphQL. Use for a daily or weekly SEO refresh, analytics reconciliation, evidence-backed SEO audit, or update to .github/seo-data.
---

# Collect SEO Data

## Overview

Collect read-only evidence for exactly one configured site, keep raw data out of
Git, update the site's Markdown operating record, and deliver every consuming-
repository run through a real pull request with CI, self-review, and squash merge.

## Invocation boundary

Invoke this skill from an authorized scheduler outside the consuming repository,
preferably a ChatGPT or equivalent session-level scheduled task. Do not add or
modify GitHub Actions, repository cron jobs, webhooks, hosted agent runners, or
model-provider credential configuration to execute this skill. Existing CI and
deployment workflows may be observed or used for delivery, but must not host the
SEO agent. The invoking session owns model access and connected-tool credentials.

## Required context

From the consuming repository root, read completely:

- repository instructions such as `AGENTS.md` or `CLAUDE.md`;
- `.github/seo-data/site.md` and `daily-task.md`;
- `.github/seo-data/status.md`, `plan.md`, and `block.md`;
- `.github/seo-data/promotion.md` when data supports a promotion decision;
- the newest relevant file under `.github/seo-data/daily/`.

Read [`references/google-drive.md`](references/google-drive.md),
[`references/cloudflare.md`](references/cloudflare.md), and
[`../../references/pull-request-delivery.md`](../../references/pull-request-delivery.md)
before collection or delivery.

Stop rather than combine unrelated properties if `site.md` is missing or names
more than one canonical site. Do not put credentials or private source IDs into
Markdown metadata.

## Workflow

### 1. Prepare the delivery branch and skills

Inspect branch, upstream, dirty files, and submodule state. Fetch the remote
default branch and create a fresh branch using the prefix in `site.md`. Preserve
unrelated work; never stash, reset, or force-push it.

Fetch the `seo-skills` submodule remote. If its allowed default branch has a
newer commit, update the submodule pointer on the same branch and record both old
and new commits. If there is no update, say so. Never edit shared skill files
from the consuming repository.

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

### 5. Escalate discovered technical defects immediately

Evidence collection is not a reporting-only boundary. When collection, public
inspection, repository state, CI, or deployment evidence reveals a reproducible
and actionable technical defect, invoke `$change-seo-site` during the same
scheduled operating cycle and local calendar day.

Do not defer build, CI, deployment, runtime, data-generation, crawlability,
indexability, robots.txt, sitemap, canonical, redirect, metadata,
structured-data, server-rendering, internal-link, accessibility, performance, or
primary user-flow failures merely because the original task was data collection.
Technical repair preempts routine analysis and content work. The one-coherent-
change rule applies per pull request, not per day; use additional focused pull
requests when independent defects must be repaired separately.

If a safe repair cannot be completed because an external system requires a
human-only action, permission is absent, or no safe rollback path exists, record
exact evidence, impact, mitigation attempted, and required external action in
`block.md` through the normal pull-request lifecycle. Do not classify an
ordinary technical decision or a queued check as a human blocker.

### 6. Update Markdown state

Write or append `.github/seo-data/daily/YYYY-MM-DD.md` using the site's local
date and `templates/seo-data/daily.example.md`. Record:

- scope, window, source status, and finalization state;
- aggregate source-native metrics labelled `GA4`, `GSC`, or `Cloudflare`;
- export filenames and optional SHA-256 checksums, never Drive URLs or IDs;
- work performed, submodule movement, validation, decisions, and follow-ups;
- every technical defect discovered, its disposition, and same-cycle repair or
  truthful blocker evidence;
- delivery fields known at the time.

Update `status.md` with the newest verified window and signals. Keep future work
in `plan.md`. Put an item in `block.md` only when an external system genuinely
requires a human-only act or the required permission does not exist.

Raw rows, search queries, user events, IP addresses, personal emails,
credentials, private URLs, account IDs, zone IDs, and Drive file/folder IDs stay
outside Git.

### 7. Validate and create a real pull request

Optionally run the lightweight safety checker:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data
```

It checks stable entrypoints and high-confidence private-data mistakes; it does
not prove data correctness or require a Markdown schema. Do not rewrite valid
site-owned prose to appease it. Run relevant repository tests, inspect the
actual evidence and intended diff, then stage only intended data files and the
submodule pointer, commit, push, and create a non-draft pull request. Do not
substitute a direct default-branch push, issue, draft PR, or local commit.

### 8. Wait for CI, self-review, and squash merge

Wait for all required and expected existing CI checks. Missing, queued, skipped,
cancelled, timed-out, or failed checks are not success. Then read the complete
final diff, commits, generated output, and check results. Fix every issue on the
same branch and repeat CI and the complete review.

After green CI and a clean final self-review, squash-merge the pull request and
delete the branch. No human or second reviewer is required.

### 9. Close out final delivery facts

Open a metadata-only closeout pull request that records the main pull request,
squash commit, and CI evidence in today's report and `status.md`. Wait for its
CI, self-review its final diff, and squash-merge it. A collection-only run does
not require deployment waiting unless metadata changes rendered output.

Any technical repair initiated by this skill must also satisfy
`$change-seo-site` production deployment, public verification, and metadata
closeout requirements before the operating cycle is complete.

## Failure rules

- An HTTP success or non-empty file does not prove complete data; verify dates,
  pagination, schema, finalization, sampling, and GraphQL errors.
- Preserve source semantics. Cloudflare visits, GA4 sessions/users, and Search
  Console clicks are different metrics.
- If a safe automated path is unavailable, record exact evidence in `block.md`
  through a pull request; do not fabricate completion.
- If metrics are unchanged, today's Markdown entry is still delivered through
  the required pull-request lifecycle.
- A confirmed actionable technical defect may not be reduced to a follow-up or
  plan item when a safe same-cycle repair path exists.
