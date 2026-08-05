# Google Cloud and Apps Script setup

## Architecture

Use a standalone Apps Script project linked to a standard Google Cloud project.
The installable Apps Script trigger runs on Google's infrastructure and writes
the weekly artifacts to Drive. The daily SEO agent later reads those artifacts;
it does not produce them.

## API and OAuth sequence

1. Create or select a standard Google Cloud project owned by the operating
   Google account.
2. Enable Google Analytics Admin API, Google Analytics Data API, Google Search
   Console API, and Google Drive API.
3. Configure an External OAuth consent app with a stable support/contact setup.
4. Add the exact manifest scopes from `assets/appsscript.json`.
5. Put the OAuth app into the intended production state before the final consent.
   A consent grant made while an external app remains in Testing can expire
   quickly and silently break an unattended trigger.
6. In Apps Script project settings, link the standard Cloud project by project
   number.
7. Add the Analytics Admin and Analytics Data advanced services and confirm their
   APIs are enabled in the linked Cloud project.
8. Save the manifest and code, select `setupAndRunBackfill`, and complete the
   final consent flow.

Search Console is called through `UrlFetchApp` with
`ScriptApp.getOAuthToken()` because it is not an Apps Script advanced service.
The token must never be logged or stored.

## Required OAuth scopes

```text
https://www.googleapis.com/auth/analytics.readonly
https://www.googleapis.com/auth/webmasters.readonly
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/script.external_request
https://www.googleapis.com/auth/script.scriptapp
```

`drive` is intentionally write-capable because the project creates CSV files in
preselected folders. GA4 and Search Console remain read-only.

## Trigger policy

Use one installable week timer for `runWeeklySeoExport`, normally Monday morning
in the configured site-operations timezone. Apps Script chooses an execution
time within the configured hour window. The code removes only duplicate triggers
for the same handler; it must not delete unrelated project triggers.

The weekly run always exports the previous complete Monday-through-Sunday period,
not a partial current week. Exact filename checks make retries safe. Transient
HTTP/API errors use bounded exponential backoff; a failure for one report or site
is recorded and must not prevent later sites from being attempted.

## Verification checklist

- Apps Script execution finishes, rather than merely starting.
- Each active site reports seven created or seven skipped filenames and no
  errors.
- Each exact Drive folder contains one copy of every expected CSV.
- A repeated backfill creates no duplicates.
- Trigger page shows one `runWeeklySeoExport` time-based trigger.
- OAuth app state and API enablement match the linked standard Cloud project.
- No paused site appears in `SITES` or receives files.
