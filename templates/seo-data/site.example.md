# Site metadata

## Identity

- Canonical URL: `https://www.example.com/`
- Site name: `example.com`
- Timezone: `America/Los_Angeles`

## Bootstrap

- Bootstrap required: yes
- Bootstrap record: `.github/seo-data/bootstrap.md`
- Normal site mutation allowed only when bootstrap status is complete: yes

`bootstrap.md` is the production-topology source of truth. Do not copy these
example values into a consuming repository without independently verifying the
actual domain, provider project, source repository, branch, build settings,
deployment trigger, and canonical public output.

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
- Runtime verification URL: `https://www.example.com/`
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

Bootstrap audits analytics read-only. Repairs begin only after the production
chain is independently verified.

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

- Provider: `cloudflare-pages`
- Production project or service: `example-site`
- Production source repository: `owner/repository`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Production environment: `production`
- Verification URL: `https://www.example.com/deployment.json`
- Provider deployment evidence method: connected provider production deployment matched to exact source commit
- Public deployment verification method: immutable deployment marker plus representative changed page
- Preview or non-production paths: pull-request previews and any generated branches listed in `bootstrap.md`

These values must agree with `.github/seo-data/bootstrap.md` and the current
provider configuration. A repository workflow, generated branch, preview,
`CNAME`, provider log, or HTTP 200 is not sufficient evidence that this is the
production path.

The deployment workflow or provider integration may build and publish the site,
but it must not host or schedule the SEO agent. Store only durable public
metadata here. Never add private property IDs, Drive IDs, Cloudflare account or
zone IDs, personal emails, credentials, raw analytics rows, cookies,
authorization values, private provider URLs, or full API responses.
