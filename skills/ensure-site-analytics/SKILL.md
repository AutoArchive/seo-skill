---
name: ensure-site-analytics
description: Require, preserve, verify, and repair analytics for every SEO-managed production site. Use during site onboarding, every scheduled operating cycle, and any change that may affect analytics scripts, page-view collection, Search Console, infrastructure analytics, consent behavior, URL reporting, or analytics privacy boundaries.
---

# Ensure Site Analytics

## Non-negotiable baseline

Every canonical production site managed by this skill collection must have analytics. A site may choose its approved provider, but `none`, silently disabled instrumentation, or an unverified analytics deployment is not an acceptable steady state.

At minimum, each site must declare and maintain:

- one runtime web analytics provider that records public page views, with Google Analytics 4 as the default when the site already has a GA4 measurement configuration;
- Google Search Console coverage for search impressions, clicks, indexing, and query/page evidence;
- infrastructure traffic analytics, such as Cloudflare Web Analytics or GraphQL HTTP analytics, whenever the production provider exposes it;
- an explicit URL reporting policy chosen by the site owner: `full-url` or `path-only`;
- a documented analytics data boundary for content, credentials, identifiers, cookies, authorization values, and application-specific state.

Runtime analytics and provider exports are separate requirements. A GA4 CSV in Drive does not prove the production site still loads GA4. A script tag alone does not prove data collection works. Verify both implementation and resulting evidence.

## Ownership rule

Do not remove, disable, replace, gate, or materially reduce an existing analytics implementation based on agent preference. Such a change requires an explicit site-owner instruction recorded in the relevant pull request and daily report.

The site owner also controls URL reporting. When `site.md` says `URL reporting: full-url`, transmit the complete browser URL, including the query string, exactly as configured by the site. Do not silently strip, hash, redact, or downgrade it. When `site.md` says `URL reporting: path-only`, omit the query string. A change between these modes requires an explicit site-owner instruction and corresponding public disclosure.

Public GA measurement IDs and equivalent client-side identifiers may remain in source-controlled runtime configuration because browsers must receive them. Private account IDs, property IDs, credentials, API tokens, OAuth material, raw exports, cookies, and user-level rows must remain outside Git.

## Required site metadata

`.github/seo-data/site.md` must contain an `## Analytics` section with all of the following:

- `Runtime analytics required: yes`
- a named primary runtime provider;
- a source-controlled implementation location;
- a public runtime verification URL;
- `URL reporting: full-url` or `URL reporting: path-only`;
- Search Console requirement and evidence route;
- infrastructure analytics provider or an accurate unavailable state;
- an explicit analytics payload policy.

The shared validator must reject a consuming repository that omits this section, marks runtime analytics as optional, leaves the primary provider unnamed, or omits the URL reporting mode.

## Operating workflow

### 1. Audit implementation every run

Inspect source, built output, and the public production URL. Confirm that the expected analytics loader and configuration are present, execute on the canonical production page, and are not blocked by accidental CSP, consent, environment, routing, static-export, or deployment regressions.

For single-page applications, confirm route or view measurement is intentional. Verify that the transmitted page URL matches the owner-selected `URL reporting` policy. Under `full-url`, complete query strings—including application import URLs or other state carried in the address bar—must be transmitted. Under `path-only`, query strings must be omitted.

Never add extra custom events containing local filenames, reading text, reading progress, credentials, cookies, authorization values, or application storage values unless the owner separately and explicitly authorizes those fields in `site.md`.

### 2. Audit evidence availability

Use `$collect-seo-data` to inspect finalized GA4 and Search Console exports and available infrastructure analytics. Label missing, stale, partial, sampled, delayed, or schema-drifted evidence accurately. Never convert missing analytics into zero traffic.

If runtime instrumentation is present but no evidence arrives after the provider's normal delay, diagnose measurement configuration, deployment identity, filters, consent, script loading, network requests, URL policy, and export routing.

### 3. Repair in the same cycle

Missing or removed runtime analytics, an invalid measurement configuration, broken page-view collection, URL reporting that contradicts `site.md`, absent Search Console ownership, or a production deployment that omits expected analytics is an actionable technical defect. Invoke `$change-seo-site` and repair it during the same operating cycle whenever a safe path exists.

The repair must use a fresh branch, real non-draft pull request, required CI, complete final self-review, squash merge, exact deployment verification, public runtime verification, and metadata closeout. Do not defer it merely because another site or content change already shipped that day.

### 4. Verify production without committing raw analytics data

Verification may inspect public HTML, built assets, browser-visible measurement configuration, CSP, public network destinations, provider debug output, and aggregate reports. Do not commit full request logs, cookies, client IDs, IP addresses, raw event payloads, private provider URLs, or account/property identifiers.

Record the provider, implementation path, public verification URL, verification time, expected page-view behavior, URL reporting mode, evidence status, PR, CI, squash commit, deployment, and any residual risk in the daily report and `status.md`.

## Completion criteria

Analytics work is complete only when:

- `site.md` declares the required analytics baseline and URL reporting mode;
- the primary runtime analytics implementation is present in source and built output;
- the canonical production site exposes the expected implementation;
- production page-view transmission matches the owner-selected full-URL or path-only policy;
- Search Console and infrastructure analytics states are accurately documented;
- provider evidence is collected or truthfully marked pending/unavailable;
- all repair and closeout pull requests are squash-merged after green CI and clean self-review.
