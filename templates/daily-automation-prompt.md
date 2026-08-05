# Daily SEO automation prompt

This prompt is invoked by an authorized scheduler outside the consuming
repository. Do not create or modify repository cron jobs, webhooks, hosted agent
runners, or model-provider credential configuration to schedule this work.

## Mandatory bootstrap gate

Always use `$bootstrap-seo-site` before any other skill. Read the existing
`.github/seo-data/site.md`, especially `## Deployment`, plus `status.md` and the
newest daily report.

If `site.md` does not record all required bootstrap fields, does not say
`Bootstrap status: complete` and `Production chain verified: yes`, contains
placeholder or unknown values, contradicts current provider or public evidence,
or may have become stale, freeze normal operation and run a read-only bootstrap
audit.

Do not add, remove, or rename files under `.github/seo-data` for bootstrap. Store
durable production topology in the existing `site.md`, the current summary in
`status.md`, and detailed evidence and rejected paths in the applicable daily
report.

Do not change site content, metadata, analytics, dependencies, DNS, domains,
build settings, deployment settings, provider configuration, redirects, robots,
sitemap, structured data, or other rendered behavior before bootstrap is
complete.

Bootstrap must independently prove:

```text
source repository + production branch + exact commit
    -> actual provider production deployment
    -> canonical public hostname
    -> expected public content or immutable deployment marker
```

A generated branch, `gh-pages`, `CNAME`, passing repository workflow, preview,
provider build log, or HTTP 200 response is not proof by itself. Inspect the
actual hosting provider project and record plausible but rejected production
paths.

The bootstrap pull request is metadata-only except for the pinned submodule and
CI invocation. It updates only existing SEO-data files and enables strict
validation with:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data \
  --require-bootstrap
```

Updating the submodule alone must remain backward-compatible for sites that have
not yet migrated; do not globally force a new SEO-data file layout.

Re-run bootstrap and freeze mutation when the canonical domain, DNS or edge
provider, hosting provider, provider project, source repository, production
branch, monorepo root, build command, output directory, deployment trigger,
platform architecture, analytics provider, URL reporting policy, or public
commit correspondence changes or may have changed.

Only after bootstrap is complete may normal operation proceed.

## Mandatory analytics audit

Use `$ensure-site-analytics`. Every canonical production site must preserve and
verify runtime analytics, Search Console, and infrastructure analytics where
available. Missing, removed, disabled, leaking, or unverified analytics is an
actionable technical defect.

Do not remove, materially reduce, redact, replace, gate, or expand analytics
based on agent preference. Only an explicit site-owner instruction recorded in
the pull request and daily report may change that requirement.

Use `$collect-seo-data` for the site in `site.md`. When a justified improvement
or repair is in scope, use `$change-seo-site`.

Treat `.github/seo-data/daily-task.md` as the site-specific entrypoint. Read all
existing SEO-data files and newest reports before acting. Contradictions between
metadata and current provider or public evidence invalidate bootstrap.

During every post-bootstrap run, confirm that the runtime provider is deployed,
URL reporting matches `full-url` or `path-only`, Search Console and infrastructure
analytics states are accurate, and missing evidence is labelled missing rather
than converted to zero.

## Same-cycle technical repair

After bootstrap, technical defects take priority over routine SEO experiments,
content production, reporting, and promotion. Repair actionable defects during
the same operating cycle when a safe technical path exists.

A production regression or failed deployment must be diagnosed, repaired or
safely rolled back, deployed through the verified provider project, and checked
on the canonical hostname before closeout. Record a blocker only when an external
system truly requires human action, permission is absent, or no safe rollback
path exists.

## Delivery sequence

1. Confirm bootstrap is complete and current. Otherwise perform only the
   read-only bootstrap lifecycle.
2. Read repository instructions, all existing SEO-data files, newest reports,
   and pinned skills.
3. Fetch the current remote default branch and create a fresh branch.
4. Check the skill submodule upstream and review the full diff before updating.
5. Collect configured read-only evidence within the public-data boundary.
6. Write or append the daily report; maintain `status.md`, `plan.md`, and
   `block.md` according to their existing roles.
7. Triage confirmed technical defects first and define the exact production
   acceptance check before editing.
8. Implement narrowly without changing unrelated deployment paths, providers,
   domains, analytics, or public URLs.
9. Run authoritative repository checks plus the shared validator. Sites that
   completed bootstrap must use `--require-bootstrap`.
10. Inspect the intended diff and generated output, push, and create a real
    non-draft pull request.
11. Wait for every required and expected CI check. Missing, queued, skipped,
    cancelled, timed-out, and failed checks block merge.
12. After CI succeeds, self-review the complete final diff, commits, generated
    output, analytics behavior, production-topology assumptions, and checks.
    Fix and repeat when needed.
13. Squash-merge after green CI and a clean final review.
14. Locate the exact squash commit in the provider project recorded by `site.md`.
    A repository workflow or generated branch is not production unless bootstrap
    proves it.
15. Wait for a successful production deployment and independently verify the
    canonical hostname, preferably against an immutable commit marker.
16. Create a metadata-only closeout pull request recording the actual provider
    deployment and public verification; wait for CI, self-review, and squash
    merge.

No normal step requires human approval. Never mutate an unverified production
path or fabricate completion.

## Completion rule

A run is incomplete unless bootstrap was current before mutation, the actual
provider project and source path were used, all expected CI passed, the final
self-review was clean, the exact squash commit reached production, the canonical
hostname exposed the expected result, and closeout was squash-merged.

A preview, generated branch, provider log, workflow URL, `CNAME`, local artifact,
or HTTP 200 alone is not completion.
