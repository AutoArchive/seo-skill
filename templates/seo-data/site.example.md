# Site metadata

## Identity

- Canonical URL: `https://example.com`
- Site name: `example.com`
- Timezone: `America/Los_Angeles`

## Repository

- Default branch: `main`
- Automation branch prefix: `seo/`
- Skill submodule path: `.github/seo-skills`
- Scheduler owner: authorized session-level task outside the repository
- Repository-hosted agent scheduler: prohibited
- Model-provider credentials in repository: prohibited

## Analytics

- Runtime analytics required: yes
- Primary runtime provider: `google-analytics-4`
- Runtime implementation location: source-controlled site configuration
- Runtime verification URL: `https://example.com/`
- URL reporting: `full-url`
- Search analytics required: `google-search-console`
- Search evidence route: Google Drive export described below
- Infrastructure analytics: `cloudflare` when the production zone is available
- Analytics payload policy: transmit the complete browser URL when `full-url` is selected; do not add custom events containing credentials, cookies, authorization values, local files, or application storage unless separately authorized

Runtime analytics is mandatory. Do not remove, disable, replace, gate, or
materially reduce it without an explicit site-owner instruction recorded in the
relevant pull request and daily report. The site owner selects either
`full-url` or `path-only`; agents must implement that mode exactly and must not
silently redact or expand URL reporting. Public browser measurement IDs may live
in runtime source; private account/property identifiers and credentials may not
be stored here.

## Google data

- Google Drive enabled: yes
- Google Drive folder name: `example.com SEO Weekly CSV`
- GA4 export filename pattern: `ga4-*.csv`
- Search Console export filename pattern: `gsc-*.csv`
- Lookback days: 28
- Finalization lag days: 3

## Cloudflare data

- Cloudflare enabled: yes
- Zone hostname: `example.com`
- Preferred dataset: `httpRequestsAdaptiveGroups`

## Deployment

- Provider: `github-actions`
- Production workflow: `Deploy`
- Production environment: `production`
- Verification URL: `https://example.com`

The deployment workflow may build and publish the site, but it must not host or
schedule the SEO agent. Store only durable public metadata here. Never add
private property IDs, Drive IDs, Cloudflare IDs, account identifiers, personal
emails, credentials, raw analytics rows, cookies, authorization values, or
private provider URLs.
