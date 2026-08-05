---
name: ensure-site-analytics
description: Require, preserve, verify, and repair analytics for every SEO-managed production site. Use during site onboarding, every scheduled operating cycle, and any change that may affect analytics scripts, page-view collection, Search Console, infrastructure analytics, consent behavior, or analytics privacy boundaries.
---

# Ensure Site Analytics

## Non-negotiable baseline

Every canonical production site managed by this skill collection must have analytics. A site may choose its approved provider, but `none`, silently disabled instrumentation, or an unverified analytics deployment is not an acceptable steady state.

At minimum, each site must declare and maintain:

- one runtime web analytics provider that records public page views, with Google Analytics 4 as the default when the site already has a GA4 measurement configuration;
- Google Search Console coverage for search impressions, clicks, indexing, and query/page evidence;
- infrastructure traffic analytics, such as Cloudflare Web Analytics or GraphQL HTTP analytics, whenever the production provider exposes it;
- a public-safe analytics privacy boundary that forbids sending user content, credentials, private identifiers, imported filenames, book titles, reading text, reading progress, private source URLs, cookies, authorization values, or sensitive query parameters.

Runtime analytics and provider exports are separate requirements. A GA4 CSV in Drive does not prove the production site still loads GA4. A script tag alone does not prove data collection works. Verify both implementation and resulting evidence.

## Ownership rule

Do not remove, disable, replace, gate, or materially reduce an existing analytics implementation based on agent preference. Such a change requires an explicit site-owner instruction recorded in the relevant pull request and daily report. Privacy concerns must be addressed by minimizing payloads, stripping sensitive query strings, disabling advertising signals when appropriate, and documenting behavior—not by silently removing measurement.

Public GA measurement IDs and equivalent client-side identifiers may remain in source-controlled runtime configuration because browsers must receive them. Private account IDs, property IDs, credentials, API tokens, OAuth material, raw exports, and user-level rows must remain outside Git.

## Required site metadata

`.github/seo-data/site.md` must contain an `## Analytics` section with all of the following:

- `Runtime analytics required: yes`
- a named primary runtime provider;
- a source-controlled implementation location;
- a public runtime verification URL;
- Search Console requirement and evidence route;
- infrastructure analytics provider or an accurate unavailable state;
- a concise forbidden-payload boundary.

The shared validator must reject a consuming repository that omits this section, marks runtime analytics as optional, or leaves the primary provider unnamed.

## Operating workflow

### 1. Audit implementation every run

Inspect source, built output, and the public production URL. Confirm that the expected analytics loader and configuration are present, execute on the canonical production page, and are not blocked by accidental CSP, consent, environment, routing, static-export, or deployment regressions.

For single-page applications, confirm route or view measurement is intentional. Strip sensitive query parameters before page-view transmission. Never include import URLs, search terms containing private data, local filenames, document titles derived from user content, reader state, or application storage values.

### 2. Audit evidence availability

Use `$collect-seo-data` to inspect finalized GA4 and Search Console exports and available infrastructure analytics. Label missing, stale, partial, sampled, delayed, or schema-drifted evidence accurately. Never convert missing analytics into zero traffic.

If runtime instrumentation is present but no evidence arrives after the provider's normal delay, diagnose measurement configuration, deployment identity, filters, consent, script loading, network requests, and export routing.

### 3. Repair in the same cycle

Missing or removed runtime analytics, an invalid measurement configuration, broken page-view collection, sensitive query leakage, absent Search Console ownership, or a production deployment that omits expected analytics is an actionable technical defect. Invoke `$change-seo-site` and repair it during the same operating cycle whenever a safe path exists.

The repair must use a fresh branch, real non-draft pull request, required CI, complete final self-review, squash merge, exact deployment verification, public runtime verification, and metadata closeout. Do not defer it merely because another site or content change already shipped that day.

### 4. Verify production without exposing private data

Verification may inspect public HTML, built assets, browser-visible measurement configuration, CSP, public network destinations, provider debug output, and aggregate reports. Do not commit full request logs, cookies, client IDs, IP addresses, raw event payloads, private provider URLs, or account/property identifiers.

Record the provider, implementation path, public verification URL, verification time, expected page-view behavior, sensitive-query handling, evidence status, PR, CI, squash commit, deployment, and any residual risk in the daily report and `status.md`.

## Completion criteria

Analytics work is complete only when:

- `site.md` declares the required analytics baseline;
- the primary runtime analytics implementation is present in source and built output;
- the canonical production site exposes the expected implementation;
- sensitive query parameters and user-owned reading data are excluded from analytics payloads;
- Search Console and infrastructure analytics states are accurately documented;
- provider evidence is collected or truthfully marked pending/unavailable;
- all repair and closeout pull requests are squash-merged after green CI and clean self-review.
