---
name: bootstrap-seo-site
description: Perform the mandatory read-only first-run audit before an agent manages a website. Use when connecting SEO automation to a new site, when the production repository, branch, provider, domain, analytics, or deployment path is uncertain, or when a verified production map may have become stale. Prove the real production topology before any content, SEO, analytics, DNS, build, or deployment behavior is changed.
---

# Bootstrap SEO Site

## Purpose

Establish a verified production map before an agent is allowed to operate a
website. The first run is not an optimization run. It is a read-only takeover
audit that determines, with evidence:

- the canonical public hostname and redirect policy;
- the DNS, edge, hosting, and deployment providers that actually serve it;
- the provider project or service that owns production;
- the source repository and production branch;
- the repository root, build command, and output directory;
- the event or integration that triggers production deployment;
- how an exact source commit maps to a provider production deployment and then
  to the canonical public hostname;
- which analytics and search properties are active;
- which repositories, branches, previews, generated branches, backups, and
  legacy providers exist but do **not** serve production.

A successful build, generated `gh-pages` branch, `CNAME` file, preview URL,
provider build log, repository workflow, or HTTP 200 response is never sufficient
by itself. Production must be proven end to end.

## Stable consumer-data layout

This skill must not add, remove, or rename files under `.github/seo-data`.
Bootstrap evidence is stored only in the existing files:

- durable production topology and bootstrap state in `site.md`, primarily under
  its existing `## Deployment` section;
- the current verified summary in `status.md`;
- detailed evidence, rejected candidate paths, and decisions in the applicable
  `daily/YYYY-MM-DD.md` report;
- future work in `plan.md`;
- only genuine human-only or permission blockers in `block.md`.

Do not create `bootstrap.md` or another new SEO-data file. Do not rename existing
headings solely for bootstrap.

## Mandatory gate

Until bootstrap is complete in `site.md`, the agent must not:

- change content, metadata, structured data, navigation, redirects, robots,
  sitemap, analytics, performance settings, dependencies, build settings, DNS,
  custom domains, deployment configuration, or provider configuration;
- create or merge a site-change pull request;
- claim that a repository, branch, workflow, generated branch, or provider
  project is production;
- report a deployment as successful.

The bootstrap run may create a metadata-only pull request that adds or updates
the pinned skill submodule, existing `.github/seo-data` files, and repository CI
needed to validate the existing metadata contract. It must not alter rendered
site behavior or provider configuration.

If the production chain cannot be proven because provider access is missing or
systems conflict, stop site mutation and record the exact missing evidence. Do
not guess. An urgent repair request does not waive bootstrap: complete the
read-only production audit first, then repair through the verified path in the
same operating cycle when safe.

## Invocation conditions

Invoke this skill when any of the following is true:

- the site has never been managed by these skills;
- `site.md` does not contain a completed, verified production map;
- the canonical hostname, DNS, CDN, hosting provider, provider project, source
  repository, production branch, build command, output directory, deployment
  trigger, or analytics implementation may have changed;
- public content does not match the repository or commit believed to be live;
- two or more plausible deployment paths exist;
- a migration, repository rename, provider migration, branch change, domain
  transfer, or build-system replacement occurred;
- deployment verification previously produced a false positive.

When in doubt, re-bootstrap. A stale production map blocks normal operation.

## Required evidence

### 1. Public hostname and edge

Inspect the canonical hostname and redirects. Record public-safe evidence for:

- canonical scheme and hostname;
- apex and `www` behavior;
- DNS target class or provider-visible routing;
- response headers, TLS hostname, CDN or platform fingerprints, cache behavior,
  and redirect chain;
- representative routes: homepage, robots, sitemap, assets, language routes, and
  a recently changed page;
- any deployment marker, build identifier, source revision, or uniquely
  attributable content fingerprint visible from production.

Do not infer the source repository from page branding or a GitHub link.

### 2. Repository inventory

Inspect every plausible website repository and deployment branch. Record:

- repository owner/name and visibility;
- default branch and recent commits;
- framework or site generator;
- provider configuration files and delivery workflows;
- build commands and output directories;
- generated branches such as `gh-pages` and whether each is production, legacy,
  preview, backup, or unused;
- submodules, theme repositories, manager repositories, and backups;
- evidence for or against each candidate being the production source.

A repository containing the newest content is not necessarily connected to
production. A branch receiving generated files is not necessarily served by the
canonical domain.

### 3. Provider project

Use the actual hosting provider connection whenever available. For Cloudflare
Pages, Vercel, Netlify, GitHub Pages, Workers, object storage, or another
platform, inspect the public-safe portions of:

- provider and project or service name;
- custom domains attached to the project;
- production branch;
- connected source repository;
- build command and output directory;
- root directory or monorepo path;
- deployment trigger;
- latest successful production deployment, source commit, and timestamp;
- preview deployment behavior;
- relevant environment variable **names**, never secret values;
- any second provider or legacy deployment.

Never commit credentials, account or zone IDs, private dashboard URLs, or full
provider responses.

### 4. End-to-end proof

Prove one exact chain:

```text
source repository + production branch + exact commit
    -> provider production deployment
    -> canonical public hostname
    -> expected public content or immutable deployment marker
```

Use provider deployment evidence plus independent public verification. Prefer an
immutable commit marker exposed by the deployed site. If none exists, use a
uniquely attributable content fingerprint and record the weaker evidence level.
Never substitute a preview or generated branch for the canonical hostname.

Explicitly list every plausible but rejected path and why it is not production.

### 5. Analytics and search

Invoke `$ensure-site-analytics` only as a read-only audit during bootstrap. Map:

- runtime analytics provider and source implementation;
- production runtime verification URL;
- owner-selected `full-url` or `path-only` policy;
- Search Console coverage;
- infrastructure analytics provider;
- public-safe evidence routes;
- discrepancies among source, generated output, production runtime, and provider
  evidence.

Do not repair analytics during bootstrap. Record defects for the first permitted
site-change cycle after production ownership is proven.

### 6. Baseline and rollback

Record a compact baseline in the existing status and daily files:

- representative public URLs and observed status;
- title, canonical, robots, sitemap, language routing, analytics loader, and
  deployment marker behavior;
- current production commit and provider deployment;
- known broken routes or regressions;
- rollback path and last known good deployment when available;
- repositories or branches that must not be modified for production changes.

## Required `site.md` fields

Keep the existing `site.md` file and headings. Under its existing
`## Deployment` section, record verified public-safe fields with these labels:

- `Bootstrap status: complete`
- `Bootstrap verified at: YYYY-MM-DD`
- `Production chain verified: yes`
- `Bootstrap evidence strength: strong` or an explicitly qualified weaker value
- `Provider`
- `Production project or service`
- `Production source repository`
- `Production source branch`
- `Repository root or monorepo path`
- `Production build command`
- `Production output directory`
- `Production deployment trigger`
- `Last verified production commit`
- `Provider deployment evidence method`
- `Public deployment verification method`
- `Verification URL`
- `Preview or non-production paths`
- `Bootstrap invalidation conditions`

These fields supplement the existing structure; they do not create a new file or
heading. `site.md`, `status.md`, and the daily report must agree.

## Backward-compatible validation

Updating the shared submodule must not make every legacy consumer fail
immediately. The shared validator therefore remains compatible by default.

After a site completes bootstrap, update its existing CI command to opt into the
strict gate:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data \
  --require-bootstrap
```

The opt-in must be included in the metadata-only bootstrap pull request. Once
enabled, it must not be removed unless the site is intentionally decommissioned
or explicitly migrated through a reviewed change.

## Bootstrap pull request

The bootstrap pull request must be metadata-only except for the pinned submodule
and validator invocation. It must include:

- evidence identifying production;
- candidate paths examined and rejected;
- the end-to-end production chain;
- uncertainty and evidence strength;
- analytics state;
- changed existing metadata files;
- validation performed;
- confirmation that rendered site and provider behavior did not change.

Wait for existing CI, self-review the complete diff, and squash-merge. Reload
`site.md` from the default branch and confirm the strict bootstrap validator is
enabled. Only then may normal operation begin.

## Invalidation and re-bootstrap

Bootstrap becomes stale when any of these changes or is credibly suspected to
have changed:

- canonical domain, apex/`www` policy, DNS target, CDN, proxy, or edge provider;
- hosting provider or provider project;
- source repository, production branch, monorepo root, build command, output
  directory, deployment trigger, or credential route;
- site generator or platform architecture;
- analytics provider or URL reporting policy;
- public production content no longer matches the expected source commit;
- a second deployment path starts serving the canonical hostname.

When invalidated, normal operations freeze. Re-run this skill and update only the
existing SEO-data files through a metadata-only pull request before changing the
site.

## Completion criteria

Bootstrap is complete only when:

- the canonical hostname and redirects are known;
- the real provider project is identified;
- the source repository and production branch are identified;
- build command, output directory, and deployment trigger are identified;
- an exact commit is matched to a provider production deployment;
- that deployment is independently matched to the canonical hostname;
- preview, legacy, generated, backup, and rejected paths are documented;
- analytics and search state are audited without mutation;
- the existing `site.md`, `status.md`, and daily report agree;
- CI uses `--require-bootstrap` and passes;
- the metadata-only bootstrap pull request was self-reviewed and squash-merged.

If any item is missing, site mutation remains prohibited.
