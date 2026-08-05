---
name: audit-seo-site
description: Audit one production website using reproducible repository, build, live-site, analytics, and optional competitive evidence. Use for onboarding, periodic baselines, regression investigation, opportunity discovery, or before choosing SEO work; produce typed findings and route confirmed defects to repair and speculative opportunities to controlled experiments.
---

# Audit SEO Site

## Overview

Create a reproducible baseline for one canonical production site. This skill
finds defects and opportunities; it does not manufacture a daily change quota.
Every conclusion follows
[`../../references/evidence-and-experiment-contract.md`](../../references/evidence-and-experiment-contract.md).

Use this skill for:

- first-time site onboarding;
- a scheduled baseline audit;
- revalidation after a site, framework, domain, or deployment change;
- investigation of a search, traffic, indexing, or performance regression;
- opportunity discovery when no confirmed technical defect remains.

## Required context

Read completely:

- repository instructions such as `AGENTS.md` and `CLAUDE.md`;
- `.github/seo-data/site.md` and `daily-task.md`;
- all other existing consumer-owned files under `.github/seo-data/`;
- the site's declared durable experiment ledger, with `experiments.md` only the
  recommended new-site filename;
- the newest relevant daily reports;
- `$ensure-site-analytics`, `$collect-seo-data`, `$change-seo-site`, and
  `$plan-seo-experiment`.

Confirm exactly one canonical site. Stop rather than merge evidence from
different properties, environments, domains, or analytics identities. Preserve
the consumer's filenames, headings, section order, titles, and daily-report
format; do not migrate it to the shared examples merely to use this skill.

## Audit modes

Choose and record one mode:

- `baseline`: broad initial or periodic assessment;
- `revalidation`: verify a known set of invariants after change;
- `incident`: investigate a concrete regression or failure;
- `opportunity`: inspect current evidence for one controlled improvement.

A baseline is not a promise to crawl every URL. State the sampled page set,
coverage, blind spots, and evidence freshness.

## Workflow

### 1. Establish scope and sampling

Identify the site architecture, public page types, deployment path, and
measurement sources. Build a sample that normally includes:

- homepage and primary conversion or documentation paths;
- one or more pages from each important template;
- top landing pages and declining pages from finalized Search Console evidence;
- recently changed or deployed pages;
- URLs referenced by robots.txt, sitemap, canonical, redirect, or structured-data
  findings.

Prefer deterministic URL discovery from repository routes, generated output,
sitemaps, and Search Console page exports. Do not imply full-site coverage when
the crawl or sample is capped.

### 2. Collect deterministic evidence

Inspect source, generated output, CI/deployment configuration, and canonical
production behavior. At minimum, check when applicable:

- status codes, redirect chains, canonical ownership, indexability, robots.txt,
  sitemap membership, and server-rendered discoverability;
- title, description, H1 and heading structure, language and hreflang behavior,
  structured data, Open Graph metadata, and internal links;
- rendering differences between source and executed output;
- mobile layout, accessibility failures that block primary use, and material
  performance regressions;
- runtime analytics implementation, URL policy, Search Console evidence, and
  infrastructure analytics;
- content intent, update state, evidence of first-hand expertise, and whether the
  page adds information beyond its own existing cluster;
- AI-search citability only as an observable content and crawler-access property,
  never as a guaranteed ranking or citation claim.

Use `$collect-seo-data` for provider evidence. When compatible Search Console CSV
exports are available, run the deterministic analyzer:

```bash
python .github/seo-skills/scripts/analyze_gsc_exports.py \
  --query-csv /temporary/current-query.csv \
  --page-csv /temporary/current-page.csv \
  --prior-query-csv /temporary/prior-query.csv \
  --prior-page-csv /temporary/prior-page.csv \
  --query-page-csv /temporary/current-query-page.csv \
  --output /temporary/gsc-analysis.json
```

The detailed output is local evidence. Do not commit raw query terms. Use
`--public-safe` before committing a reviewed derived artifact.

Competitive inspection is optional and must record query, locale, collection
time, sampled results, and fetch failures. It supports intent and content-gap
analysis; it does not prove a ranking factor.

### 3. Write typed findings

For every material finding, record the full finding contract: ID, category,
resource, severity, confidence, evidence class, exact observation, impact,
recommended action, verification, disposition, dependencies, and automation
eligibility.

Do not issue an unsupported health score. A coarse category rating is allowed
only when the inspected checks and missing evidence are shown. Prefer a short,
ordered set of evidence-backed findings over a long generic checklist.

### 4. Route each finding

- Confirmed invariant failure or reproducible regression: invoke
  `$change-seo-site` and complete the same-cycle repair when safe.
- Otherwise-valid behavior with a plausible improvement: invoke
  `$plan-seo-experiment`; do not edit first and invent a hypothesis later.
- Insufficient evidence: mark `unknown` and define the smallest next observation.
- No justified action: record a truthful no-op.

Active experiment resource locks do not block unrelated audits. They do block a
new speculative edit to the same resource. A technical repair may override a
lock but must mark the experiment confounded, aborted, or inconclusive.

### 5. Persist the baseline

Write the audit mode, scope, sampled URLs or templates, evidence windows,
findings, dispositions, and limitations into the current consumer-defined daily
report. Update the site's existing durable current-status record, when it uses
one, with:

- last baseline audit date and mode;
- audit coverage and evidence watermark;
- unresolved confirmed defects;
- active experiment and earliest review date;
- next scheduled baseline.

Detailed raw crawl or analytics output remains outside Git unless it is
explicitly public-safe and useful for durable review. Do not create, rename, or
restructure SEO-data files solely to match the shared onboarding templates.

### 6. Deliver through the repository lifecycle

Audit-only metadata changes still use a fresh branch, real non-draft pull
request, required and expected CI, complete final self-review, squash merge, and
metadata closeout according to the shared delivery contract.

Any site repair or experiment implementation must also satisfy exact deployment
and public verification requirements from `$change-seo-site`.

## Completion criteria

The audit is complete only when:

- scope, sampling, evidence freshness, and limitations are explicit;
- material claims use the evidence contract;
- findings have stable IDs and dispositions;
- confirmed safe-to-fix defects were repaired or truthfully blocked;
- speculative work was routed through experiment planning and resource locks;
- state and daily records were delivered through the pull-request lifecycle.
