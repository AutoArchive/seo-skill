---
name: configure-google-seo-export
description: Configure and verify Google-managed weekly GA4 and Search Console CSV exports into one Google Drive folder per site. Use when onboarding sites, replacing an agent or computer timer, backfilling the previous complete week, repairing stale exports, or documenting how SEO evidence reaches Drive without exposing private Google identifiers in Git.
---

# Configure Google SEO Export

## Outcome

Create one private Google Apps Script project that runs inside Google, exports
the previous complete Monday-through-Sunday window, and writes seven idempotent
CSV files plus one GA4 source manifest into each active site's Drive folder:

- one GA4 organic landing-page report;
- one private GA4 source manifest that binds the CSV to its domain, property,
  and date range;
- six Search Console reports: queries, pages, countries, devices, search
  appearance, and dates.

This is provider-managed export automation. Do not substitute a Codex task,
ChatGPT task, repository cron job, GitHub Action, browser loop, local process, or
always-on computer.

## Private configuration boundary

Assume this skill repository and every consuming repository are public. Keep
Drive folder IDs, GA4 account/property IDs, Google Cloud project numbers, OAuth
material, emails, raw exports, and user-level rows only in the private Apps
Script/Google Cloud project.

The template in [`assets/Code.gs`](assets/Code.gs) contains placeholders. Replace
them only inside the private Apps Script editor. Never commit the populated
configuration. Public daily records may name sites, date windows, filenames,
checksums, row counts, aggregate metrics, and success/failure state.

## Required reading

Read [`references/google-cloud-setup.md`](references/google-cloud-setup.md) before
changing Google Cloud, OAuth, Apps Script, triggers, or Drive routing. Read
[`../collect-seo-data/references/google-drive.md`](../collect-seo-data/references/google-drive.md)
before validating or consuming the resulting files.

## Workflow

### 1. Establish exact scope

List active canonical sites and exclusions. For each active site, resolve exactly
one Drive destination folder, one GA4 property, and one Search Console property.
Omit paused sites entirely. Do not infer that similarly named properties or
folders are interchangeable.

Every site must have an explicit GA4 property ID in the private `SITES` array.
Never resolve properties by display name: duplicate names are valid in GA4 and
can silently route a site to the wrong property. Reuse the site's established
property unless the owner explicitly authorizes a migration.

Confirm that the Google account can read each GA4 and Search Console property
and create files in each destination folder. Folder sharing is a separate
permission-changing action; do not change it unless the owner specified the
recipient and exact role.

### 2. Configure the Google-owned project

Create a standalone Apps Script project and link it to a standard Google Cloud
project. Follow the OAuth, API, and consent sequence in the setup reference.
Install [`assets/appsscript.json`](assets/appsscript.json) and
[`assets/Code.gs`](assets/Code.gs), then populate only the private copy's `SITES`
array and timezone.

The manifest grants the narrow read scopes needed for GA4 and Search Console,
plus Drive file creation, outbound Google API calls, and trigger management. Do
not broaden scopes merely to simplify implementation.

### 3. Run an immediate idempotent backfill

Run `setupAndRunBackfill` interactively after the final production OAuth consent.
It installs the weekly trigger and exports the previous complete Monday-through-
Sunday period immediately.

Run the function a second time. Every expected filename, including the GA4
source manifest, must be reported as skipped, with no duplicate files and no errors. A successful authorization
screen, HTTP response, or execution start is not proof of complete export.

An existing GA4 CSV is reusable only when its adjacent source manifest matches
the configured domain, property ID, and date window. Missing or mismatched
manifests are errors: quarantine the stale artifacts, then rerun the period.
Never treat filename existence alone as proof that the export is current.

### 4. Verify artifacts and trigger

For every active site, inspect the exact Drive folder and confirm all seven
filenames share the same completed-week prefix:

```text
YYYY-MM-DD_to_YYYY-MM-DD_ga4_organic_landing_pages.csv
YYYY-MM-DD_to_YYYY-MM-DD_ga4_source.json
YYYY-MM-DD_to_YYYY-MM-DD_gsc_queries.csv
YYYY-MM-DD_to_YYYY-MM-DD_gsc_pages.csv
YYYY-MM-DD_to_YYYY-MM-DD_gsc_countries.csv
YYYY-MM-DD_to_YYYY-MM-DD_gsc_devices.csv
YYYY-MM-DD_to_YYYY-MM-DD_gsc_search_appearance.csv
YYYY-MM-DD_to_YYYY-MM-DD_gsc_dates.csv
```

Confirm exactly one installable time trigger targets `runWeeklySeoExport`.
Run `auditExporterHealth` and require `ok: true`; this checks unique sites,
explicit private routing, and the single-trigger invariant without logging IDs.
Record its day, hour window, timezone, last execution, per-site outcome, and any
provider delay outside the public repository when those details contain private
routing data.

### 5. Monitor without moving automation out of Google

The daily SEO agent uses `$collect-seo-data` to detect missing, stale, duplicate,
or schema-drifted exports. If the weekly export fails, diagnose Apps Script
execution history, OAuth grant state, API enablement, quotas, property access,
and destination permissions. Repair the Google project and re-run the same
completed period; do not create a second scheduler elsewhere.

When the active site list changes, update the private `SITES` array, run the
backfill, verify idempotency, and retain one weekly trigger. A shared skill update
must never overwrite the populated private configuration.

## Completion criteria

The setup is complete only when:

- the OAuth app is in the intended production state and final consent succeeds;
- all required APIs are enabled on the linked standard Cloud project;
- the immediate backfill creates seven CSV files and one GA4 source manifest per active site;
- a second run skips all eight exact filenames per site without errors;
- exactly one Google-owned weekly trigger exists;
- paused sites are absent;
- no private routing identifiers or raw data entered Git.
