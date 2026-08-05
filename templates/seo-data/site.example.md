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
property IDs, Drive IDs, Cloudflare IDs, account identifiers, personal emails,
credentials, or private URLs.
