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

Runtime analytics and provider exports are separate requirements. A provider export does not prove the production site still loads analytics, and a script tag alone does not prove evidence arrives. Verify both implementation and resulting evidence.

## Ownership rule

Do not remove, disable, replace, gate, or materially reduce an existing analytics implementation based on agent preference. Such a change requires an explicit site-owner instruction recorded in the relevant pull request and daily report.

The site owner also controls URL reporting. When the site selects full-URL reporting, transmit the complete browser URL, including the query string, exactly as configured by the site. Do not silently strip, hash, redact, or downgrade it. When the site selects path-only reporting, omit the query string. A change between these modes requires an explicit site-owner instruction and corresponding public disclosure.

Public GA measurement IDs and equivalent client-side identifiers may remain in source-controlled runtime configuration because browsers must receive them. Private account IDs, property IDs, credentials, API tokens, OAuth material, raw exports, cookies, and user-level rows must remain outside Git.

## Useful operating context

A future operator should be able to discover the expected runtime provider,
implementation location, public verification route, URL-reporting choice,
search-evidence route, infrastructure source when available, and data boundary.
Use the site's existing records or add the minimum fields or files needed by the
current skill. Do not treat documentation presence as proof that analytics
works.

This skill does not prescribe a universal `.github/seo-data` structure and does
not require a shared validator. If a future skill version explicitly introduces
a new operating artifact or interface, the consuming repository may add the
minimum necessary change when adopting that version.

## Operating workflow

### 1. Audit implementation every run

Inspect source, built output, and the public production URL. Confirm that the expected analytics loader and configuration are present, execute on the canonical production page, and are not blocked by accidental CSP, consent, environment, routing, static-export, or deployment regressions.

For single-page applications, confirm route or view measurement is intentional. Verify that the transmitted page URL matches the owner-selected reporting policy. Under full-URL reporting, complete query strings must be transmitted. Under path-only reporting, query strings must be omitted.

Never add extra custom events containing local filenames, reading text, reading progress, credentials, cookies, authorization values, or application storage values unless the owner separately and explicitly authorizes those fields in the site's operating metadata.

### 2. Audit evidence availability

Use `$collect-seo-data` to inspect finalized analytics and Search Console exports and available infrastructure analytics. Label missing, stale, partial, sampled, delayed, or schema-drifted evidence accurately. Never convert missing analytics into zero traffic.

If runtime instrumentation is present but no evidence arrives after the provider's normal delay, diagnose measurement configuration, deployment identity, filters, consent, script loading, network requests, URL policy, and export routing.

### 3. Repair in the same cycle

Missing or removed runtime analytics, an invalid measurement configuration, broken page-view collection, URL reporting that contradicts the owner-selected policy, absent Search Console ownership, or a production deployment that omits expected analytics is an actionable technical defect. Invoke `$change-seo-site` and repair it during the same operating cycle whenever a safe path exists.

The repair must use `$change-seo-site`, including `$deliver-github-pr` with
complete expected CI and a from-scratch final review after CI, followed by
squash merge, exact deployment verification, public runtime verification, and
metadata closeout.

### 4. Verify production without committing raw analytics data

Verification may inspect public HTML, built assets, browser-visible measurement configuration, CSP, public network destinations, provider debug output, and aggregate reports. Do not commit full request logs, cookies, client IDs, IP addresses, raw event payloads, private provider URLs, or account/property identifiers.

Record the provider, implementation path, public verification URL, verification time, expected page-view behavior, URL reporting mode, evidence status, PR, CI, squash commit, deployment, and any residual risk in the consuming site's normal operating records.

## Completion criteria

Analytics work is complete only when:

- the site's operating records make the expected analytics behavior and URL reporting mode discoverable;
- the primary runtime analytics implementation is present in source and built output;
- the canonical production site exposes the expected implementation;
- production page-view transmission matches the owner-selected policy;
- Search Console and infrastructure analytics states are accurately documented;
- provider evidence is collected or truthfully marked pending/unavailable;
- all repair and closeout pull requests are squash-merged after green CI and a
  clean from-scratch review of the complete final PR.
