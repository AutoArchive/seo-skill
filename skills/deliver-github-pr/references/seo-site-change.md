# Search-facing site change policy

Read this reference only for a website change that affects content, metadata,
structured data, internal links, crawlability, performance, analytics, routes,
or other search-facing public behavior.

## Keep the change incremental

Make the smallest independently deployable, reversible, and reviewable change
that fixes one observed problem or tests one supported hypothesis. Preserve
unrelated design, copy, navigation, public paths, canonical ownership,
redirects, metadata, analytics, and content.

Before editing, capture the relevant production baseline and state:

- evidence for the problem or hypothesis;
- affected route family and representative unaffected routes;
- expected search or user effect;
- exact public acceptance check; and
- rollback point.

Prefer additive or local edits before replacement, deletion, consolidation, or
migration. Do not combine page purpose, information architecture, navigation,
visual system, titles, descriptions, and route ownership in one routine change.
Missing analytics or a general desire to modernize is not evidence that a broad
change is safe.

Split a necessary large migration into independently useful, deployable phases.
Each phase must preserve a usable production site, have its own acceptance and
rollback, and not depend on an unmerged later phase for correctness. During an
active incident, prefer the smallest safe repair or restoration of the last
known-good behavior.

## Prioritize confirmed defects

A reproducible build, CI, deployment, runtime, crawlability, indexability,
robots, sitemap, canonical, redirect, metadata, structured-data,
server-rendering, internal-link, analytics, accessibility, performance, or
primary-flow defect takes priority over speculative SEO work and should be
repaired in the same operating cycle whenever a safe path exists.

The coherent-scope rule applies per pull request, not per day. Use separate
focused pull requests for independent repairs. A routine cycle may select at
most one speculative SEO experiment; this limit does not apply to confirmed
technical defects.

Only a genuine permission, legal, billing, human-only, or no-safe-rollback
constraint is a blocker. Record the exact evidence and mitigation instead of
moving an actionable technical defect into a future plan.

## Supply domain checks to delivery

Follow the consuming site's architecture and content rules. Validate generated
output and search semantics locally. Give `$deliver-github-pr` the baseline,
blast radius, affected and unaffected routes, deployment target, public
acceptance checks, and rollback.

After deployment, public verification must inspect the changed behavior rather
than availability alone. Verify representative unaffected routes whenever a
shared component, template, route rule, or build path changed.
