# Site metadata

## Identity

- Canonical URL: `https://www.example.com/`
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
- Runtime verification URL: `https://www.example.com/`
- URL reporting: `full-url`
- Search analytics required: `google-search-console`
- Search evidence route: Google Drive export described below
- Infrastructure analytics: `cloudflare` when the production zone is available
- Analytics payload policy: transmit the complete browser URL when `full-url` is selected; do not add custom events containing credentials, cookies, authorization values, local files, or application storage unless separately authorized

Runtime analytics is mandatory. Do not remove, disable, replace, gate, or
materially reduce it without an explicit site-owner instruction recorded in the
relevant pull request and daily report. Bootstrap audits analytics read-only;
repairs begin only after production ownership is proven.

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

- Bootstrap status: complete
- Bootstrap verified at: 2026-01-01
- Production chain verified: yes
- Bootstrap evidence strength: strong
- Provider: `cloudflare-pages`
- Production project or service: `example-site`
- Production source repository: `owner/repository`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Production environment: `production`
- Last verified production commit: `0123456789abcdef0123456789abcdef01234567`
- Provider deployment evidence method: connected provider production deployment matched to exact source commit
- Public deployment verification method: immutable deployment marker plus representative changed page
- Verification URL: `https://www.example.com/deployment.json`
- Preview or non-production paths: pull-request previews and generated branches documented in the daily bootstrap report
- Bootstrap invalidation conditions: domain, DNS or edge, provider project, source repository or branch, build command, output directory, deployment trigger, platform architecture, analytics provider, URL policy, or public commit correspondence changes

These values are examples only. `$bootstrap-seo-site` must independently verify
the actual production topology before replacing them. A repository workflow,
generated branch, preview, `CNAME`, provider log, or HTTP 200 response is not
sufficient evidence by itself.

Store only durable public metadata here. Never add private property IDs, Drive
IDs, Cloudflare account or zone IDs, personal emails, credentials, raw analytics
rows, cookies, authorization values, private provider URLs, or full API
responses.
