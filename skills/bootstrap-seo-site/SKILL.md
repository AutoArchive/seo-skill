---
name: bootstrap-seo-site
description: Perform the mandatory read-only first-run audit before an agent manages a website. Use when connecting SEO automation to a new site, when the production repository, branch, provider, domain, analytics, or deployment path is uncertain, or when an existing bootstrap has become stale. Prove the real production topology and record it before any content, SEO, analytics, DNS, build, or deployment behavior is changed.
---

# Bootstrap SEO Site

## Purpose

Establish a verified production map before an agent is allowed to operate a
website. The first run is not an optimization run. It is a read-only takeover
audit whose job is to answer, with evidence:

- which public hostname is canonical;
- which edge, DNS, hosting, and deployment providers serve it;
- which provider project or service owns production;
- which repository and branch are the production source of truth;
- which build command and output directory create the deployed site;
- which event or workflow triggers production deployment;
- how an exact source commit is matched to a provider deployment and then to the
  public hostname;
- which analytics and search properties are actually active;
- which other repositories, branches, preview deployments, generated branches,
  or legacy platforms exist but do **not** serve production.

A successful build, a generated `gh-pages` branch, a `CNAME` file, a preview URL,
a provider dashboard entry, an HTTP 200 response, or a repository workflow name
is never sufficient by itself. Production must be proven end to end.

## Mandatory gate

Until bootstrap is complete and recorded in
`.github/seo-data/bootstrap.md`, the agent must not:

- change content, metadata, structured data, navigation, redirects, robots,
  sitemap, analytics, performance settings, dependencies, build settings, DNS,
  custom domains, deployment configuration, or provider configuration;
- create or merge a site-change pull request;
- claim that a repository, branch, workflow, generated branch, or provider project
  is production;
- report a deployment as successful.

The bootstrap run may create a metadata-only pull request that adds the pinned
skill submodule and verified `.github/seo-data` files. It must not alter rendered
site behavior. If the production chain cannot be proven because access is
missing or systems conflict, stop site mutation and report the exact missing
evidence. Do not guess.

An explicit user request for an immediate repair does not waive bootstrap. Finish
the read-only topology audit first, then perform the repair in the same operating
cycle only after the production path is proven.

## Invocation conditions

Invoke this skill when any of the following is true:

- the site has never been managed by these skills;
- `bootstrap.md` is missing;
- `Bootstrap status` is not `complete`;
- the canonical hostname, DNS, CDN, hosting provider, provider project, source
  repository, production branch, build command, output directory, deployment
  trigger, or analytics implementation may have changed;
- public content does not match the repository or commit believed to be live;
- two or more plausible deployment paths exist;
- a migration, repository rename, provider migration, branch change, domain
  transfer, or build-system replacement occurred;
- deployment verification previously produced a false positive.

When in doubt, re-bootstrap. A stale bootstrap blocks normal daily operation.

## Required evidence classes

Use all connected provider and repository tools that are available. The final
map must combine multiple independent evidence classes rather than relying on a
single artifact.

### 1. Public hostname and edge evidence

Inspect the canonical public hostname and relevant redirects. Record:

- canonical scheme and hostname;
- apex and `www` behavior;
- DNS target class or provider-visible routing without committing private zone or
  account IDs;
- response headers, TLS hostname, CDN or platform fingerprints, cache behavior,
  and redirect chain;
- a representative set of public routes, including homepage, robots, sitemap,
  assets, and a recently changed page;
- any deployment marker, build identifier, source revision, or content fingerprint
  visible from production.

Do not infer the source repository from page branding or a GitHub link.

### 2. Repository inventory

Inspect every plausible website repository and deployment branch. Record:

- repository owner/name and visibility;
- default branch and recent commits;
- site generator or application framework;
- provider configuration files and deployment workflows;
- build commands and output directories;
- generated branches such as `gh-pages` and whether they are production,
  legacy, preview, backup, or unused;
- submodules, theme repositories, manager repositories, and backup repositories;
- evidence for or against each repository being the production source.

A repository containing the newest content is not necessarily connected to
production. A branch receiving generated files is not necessarily served by the
canonical domain.

### 3. Provider project audit

Use the actual hosting provider connection whenever available. For Cloudflare
Pages, Vercel, Netlify, GitHub Pages, Workers, object storage, or another platform,
record the public-safe portions of:

- provider and project or service name;
- custom domains attached to the project;
- production branch;
- connected source repository;
- build command and output directory;
- root directory or monorepo path;
- deployment trigger;
- latest successful production deployment, its source commit, and timestamp;
- preview deployment behavior;
- relevant environment variable **names**, never secret values;
- whether a second provider or legacy deployment still exists.

Provider project names may be recorded when public-safe. Never commit account,
zone, property, project IDs that the repository policy treats as private,
credentials, tokens, private dashboard URLs, or full provider API responses.

### 4. End-to-end production proof

Prove one exact chain:

```text
source repository + production branch + exact commit
    -> provider production deployment
    -> canonical public hostname
    -> expected public content or immutable deployment marker
```

Use provider deployment evidence plus independent public verification. Preferred
proof includes an immutable commit marker exposed by the deployed site. When the
site has no marker, use a uniquely attributable content fingerprint and record
that the proof is weaker. Never substitute a preview deployment or generated
branch for the canonical hostname.

Explicitly list every plausible but rejected path and why it is not production.

### 5. Analytics and search audit

Invoke `$ensure-site-analytics` only as a read-only audit during bootstrap. Map:

- runtime analytics provider and source implementation;
- production runtime verification URL;
- owner-selected `full-url` or `path-only` policy;
- Search Console coverage;
- infrastructure analytics provider;
- public-safe evidence routes;
- discrepancies between source, generated output, production runtime, and
  provider evidence.

Do not repair analytics during bootstrap. Record defects for the first permitted
site-change cycle after the production topology is complete.

### 6. Baseline and safety snapshot

Before any future mutation, record a compact baseline:

- representative public URLs and observed status;
- current title, canonical, robots, sitemap, language routing, analytics loader,
  and deployment marker behavior;
- current production commit and provider deployment;
- known broken routes or production regressions;
- rollback path and last known good deployment when the provider exposes it;
- repositories or branches that must not be modified for production changes.

## Bootstrap record

Create `.github/seo-data/bootstrap.md` from the shared template. It must contain
verified, public-safe facts and at minimum:

- `Bootstrap status: complete`;
- verification date;
- canonical production URL;
- production provider and project or service;
- DNS or edge provider;
- production source repository and branch;
- build command and output directory;
- deployment trigger;
- exact last verified production commit;
- provider deployment evidence method;
- public deployment verification method;
- production chain verification result;
- known preview, legacy, backup, and non-production paths;
- analytics and Search Console state;
- invalidation conditions.

Update `site.md`, `status.md`, `plan.md`, and `block.md` to agree with the
bootstrap. Contradictions block completion.

## Bootstrap pull request

The bootstrap pull request is metadata-only except for adding the pinned skill
submodule and repository-local validation needed to protect the metadata
contract. It must not change the rendered site or provider configuration.

The pull request must include:

- the evidence used to identify production;
- candidate paths examined and rejected;
- the verified end-to-end production chain;
- known uncertainty and evidence strength;
- analytics state;
- changed metadata files;
- validation performed;
- confirmation that no site behavior changed.

Wait for existing CI, self-review the complete diff, and squash-merge. Human
review is not required unless repository policy enforces it. After merge, reload
the files from the default branch and confirm the bootstrap record is present.
Only then may normal daily or site-change operation begin.

## Invalidation and re-bootstrap

Bootstrap immediately becomes stale when any of these changes or is credibly
suspected to have changed:

- canonical domain, apex/`www` policy, DNS target, CDN, proxy, or edge provider;
- hosting or deployment provider;
- provider project or service;
- source repository, production branch, monorepo root, build command, output
  directory, deployment trigger, or deployment credentials route;
- site generator or platform architecture;
- analytics provider or URL reporting policy;
- public production content no longer matches the expected source commit;
- a second deployment path starts serving the canonical hostname.

When invalidated, normal operations freeze. Re-run this skill and update the
bootstrap record through a metadata-only pull request before changing the site.

## Completion criteria

Bootstrap is complete only when all are true:

- the canonical hostname and redirect behavior are known;
- the real production provider project is identified;
- the production source repository and branch are identified;
- build command, output directory, and deployment trigger are identified;
- an exact source commit is matched to a production deployment;
- that deployment is independently matched to the canonical public hostname;
- preview, legacy, generated, backup, and rejected paths are documented;
- analytics and search state are audited without mutation;
- `.github/seo-data/bootstrap.md` and related metadata agree;
- the metadata-only bootstrap pull request passed CI, was self-reviewed, and was
  squash-merged.

If any item is missing, bootstrap is incomplete and site mutation remains
prohibited.
