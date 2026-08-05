# SEO bootstrap

## Status

- Bootstrap status: complete
- Bootstrap verified at: 2026-01-01
- Production chain verified: yes
- Evidence strength: strong

Normal site mutation is prohibited unless this file says `Bootstrap status:
complete` and the production chain remains current. Re-run
`$bootstrap-seo-site` whenever an invalidation condition is met.

## Canonical production

- Canonical production URL: `https://example.com/`
- Apex and www behavior: apex redirects to canonical `www` host
- DNS or edge provider: `cloudflare`
- Production hosting provider: `cloudflare-pages`
- Production project or service: `example-site`

Do not record private account IDs, zone IDs, provider tokens, private dashboard
URLs, personal emails, or full API responses.

## Production source of truth

- Production source repository: `owner/repository`
- Production source branch: `main`
- Repository root or monorepo path: `/`
- Site generator or framework: `hugo`
- Production build command: `hugo --minify --gc`
- Production output directory: `public`
- Production deployment trigger: provider Git integration on pushes to `main`
- Last verified production commit: `0123456789abcdef0123456789abcdef01234567`

## Provider deployment evidence

- Provider evidence method: connected provider deployment record matched to the exact source commit
- Latest verified production deployment: public-safe provider deployment name or timestamp
- Custom-domain attachment verified: yes
- Production branch verified: yes
- Connected repository verified: yes
- Build command and output directory verified: yes
- Preview deployment behavior: pull requests create non-production preview URLs

## Public verification

- Public deployment verification method: immutable `/deployment.json` marker plus representative page fingerprint
- Public verification URL: `https://example.com/deployment.json`
- Representative homepage verified: yes
- Robots and sitemap verified: yes
- Recent changed page verified: yes
- Public content matched exact production commit: yes

An HTTP 200 response alone is not verification. Generated branches, previews,
provider build logs, and repository workflows are evidence only when connected
to the canonical hostname through the proven production chain.

## Non-production and rejected paths

- Generated branches: `gh-pages` exists but does not serve the canonical production hostname
- Preview providers or projects: list public-safe names and purposes
- Legacy providers or projects: list public-safe names and whether disabled
- Backup repositories: list owner/name and confirm they are not production sources
- Rejected production candidates: record each plausible path and the evidence that rejected it

## Analytics and search baseline

- Runtime analytics provider: `google-analytics-4`
- Runtime analytics production verification: verified on canonical production URL
- URL reporting mode: `full-url`
- Google Search Console: configured
- Infrastructure analytics: `cloudflare`
- Analytics discrepancies: none known

Bootstrap audits analytics without changing it. Repairs happen only after this
bootstrap is complete and through the normal site-change pull-request lifecycle.

## Baseline and rollback

- Representative routes: homepage, robots.txt, sitemap.xml, one current article, one language route
- Current title and canonical behavior: verified
- Current language routing: verified
- Current analytics loader: verified
- Current deployment marker: verified
- Last known good production deployment: public-safe commit or provider deployment reference
- Rollback method: provider rollback or redeploy of last known good commit
- Known production defects: none, or list concise verified defects

## Invalidation conditions

Re-run bootstrap and freeze normal site mutation when any of these changes or may
have changed:

- canonical domain, apex/`www` redirect, DNS target, CDN, proxy, or edge provider;
- hosting provider or provider project;
- source repository, production branch, monorepo root, build command, output
  directory, or deployment trigger;
- site generator or platform architecture;
- analytics provider or URL reporting policy;
- canonical production content no longer matches the expected source commit;
- another provider or deployment path starts serving the canonical hostname.
