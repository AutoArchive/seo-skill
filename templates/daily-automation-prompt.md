# Daily SEO automation prompt

This prompt is invoked by an authorized scheduler outside the consuming
repository, preferably a ChatGPT or equivalent session-level scheduled task.
Do not create or modify GitHub Actions, repository cron jobs, webhooks, hosted
agent runners, or model-provider credential configuration to schedule this
work. Existing CI and deployment workflows may be observed or used for delivery,
but must not host the SEO agent.

## Mandatory bootstrap gate

Always read and enforce `$bootstrap-seo-site` from
`.github/seo-skills/skills/bootstrap-seo-site/SKILL.md` before any other skill.
Read `.github/seo-data/bootstrap.md` completely.

If `bootstrap.md` is missing, does not say `Bootstrap status: complete`, does not
say `Production chain verified: yes`, contains example or unknown values, or may
have become stale, freeze normal operation and run a read-only bootstrap audit.
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
provider build log, HTTP 200 response, or repository name is not proof by itself.
Inspect the actual hosting provider project and record plausible but rejected
production paths. The first-run pull request is metadata-only except for the
pinned skill submodule and repository-local validation protecting the metadata
contract.

Re-run bootstrap and freeze mutation when the canonical domain, DNS or edge
provider, hosting provider, provider project, source repository, production
branch, monorepo root, build command, output directory, deployment trigger,
platform architecture, analytics provider, URL reporting policy, or public
commit correspondence changes or may have changed.

Only after bootstrap is complete may the run proceed below.

## Mandatory analytics audit

Always use `$ensure-site-analytics` from
`.github/seo-skills/skills/ensure-site-analytics/SKILL.md`. Every canonical
production site must preserve and verify runtime analytics, Search Console, and
infrastructure analytics where available. Missing, removed, disabled, leaking,
or unverified analytics is an actionable technical defect.

Do not remove, materially reduce, redact, replace, gate, or expand analytics
based on agent preference. Only an explicit site-owner instruction recorded in
the pull request and daily report may change that requirement.

Use `$collect-seo-data` from
`.github/seo-skills/skills/collect-seo-data/SKILL.md` for the single site defined
in `.github/seo-data/site.md`. When a justified site improvement or repair is in
scope, use `$change-seo-site` from
`.github/seo-skills/skills/change-seo-site/SKILL.md`.

Treat `.github/seo-data/daily-task.md` as the site-specific execution entrypoint.
Read `bootstrap.md`, `site.md`, `status.md`, `plan.md`, `block.md`, and the newest
daily reports before acting. Contradictions between these files and current
provider or public evidence invalidate bootstrap and block mutation.

During every post-bootstrap run, inspect the analytics contract in `site.md`,
source code, generated output, canonical production URL, and provider evidence.
Confirm that:

- the named runtime provider is implemented and deployed;
- public page views are intentionally collected;
- URL reporting exactly matches `full-url` or `path-only`;
- `full-url` includes the complete browser query string without agent redaction;
- `path-only` omits the query string;
- no extra custom events containing credentials, cookies, authorization values,
  local files, or application storage have been introduced without explicit
  owner authorization;
- Search Console and infrastructure analytics states are accurate;
- missing or stale provider evidence is labelled missing or stale rather than
  converted to zero.

If runtime analytics is absent, broken, or contradicts the URL policy, repair it
during the same operating cycle through a focused pull request, actual provider
production deployment verification, canonical-host runtime verification, and
closeout. A Drive export or script tag alone is not sufficient proof.

## Same-cycle technical repair requirement

Technical defects take priority over routine SEO experiments, source discovery,
content production, reporting, and promotion work. When a post-bootstrap run
discovers a reproducible and actionable defect in build, CI, actual deployment,
runtime behavior, analytics, crawlability, indexability, accessibility,
performance, broken links, redirects, canonical signals, metadata, structured
data, robots.txt, sitemap output, server rendering, or primary user flows,
repair it during the same scheduled operating cycle and local calendar day
whenever a safe technical path exists.

Do not intentionally defer an actionable defect merely because another
improvement was planned or one pull request already exists. The one-coherent-
change limit applies per main pull request, not per day. Use additional focused
pull requests when independent repairs cannot be reviewed coherently together.
A production regression or failed deployment preempts routine work and must be
diagnosed, repaired or safely rolled back, deployed through the **verified
production provider**, and checked on the canonical public hostname before the
cycle is closed.

If the defect cannot be completed because an external system enforces a
human-only action, permission is absent, or no safe rollback path exists, record
the exact evidence, mitigation attempted, and required external action in
`block.md` through the normal pull-request lifecycle. Provider queues that cross
local midnight remain part of the same operation.

## Delivery sequence

1. Confirm bootstrap is complete and current. If not, run only
   `$bootstrap-seo-site` and finish the metadata-only bootstrap lifecycle.
2. Read repository instructions, all `.github/seo-data/*.md` files, newest daily
   reports, and the pinned skills.
3. Fetch the current remote default branch and create a fresh branch using the
   prefix in `site.md`.
4. Check the `seo-skills` submodule remote and include a compatible update in the
   same branch after reviewing its full diff and metadata migration requirements.
5. Collect configured read-only evidence, preserving the public-data boundary.
6. Write or append `.github/seo-data/daily/YYYY-MM-DD.md`; maintain `status.md`,
   `plan.md`, and `block.md` according to their roles.
7. Triage confirmed technical defects first. Define one coherent outcome per main
   pull request and define the exact public acceptance check before editing.
8. Implement narrowly without changing unrelated deployment paths, provider
   projects, branches, domains, analytics, or public URLs.
9. Run authoritative repository checks plus the shared SEO-data validator.
10. Inspect the intended diff and generated output, push the branch, and create a
    real non-draft pull request. Never substitute a direct default-branch push,
    issue, draft PR, or local commit.
11. Wait for every required and expected CI check. Missing, queued, skipped,
    cancelled, timed-out, and failed checks are not ready.
12. After CI succeeds, self-review the complete final diff, commits, generated
    output, analytics behavior, production-topology assumptions, and check
    results. Fix every issue on the same branch and repeat CI and review.
13. Squash-merge after green CI and a clean final review. Attempt merged branch
    deletion only when the connector safely supports it; cleanup is non-blocking.
14. Locate the deployment triggered by the exact squash commit in the **provider
    project recorded by bootstrap.md and site.md**. A repository workflow or
    generated branch is not production unless bootstrap explicitly proves it.
15. Wait for a successful terminal production deployment, then verify the
    canonical public hostname with cache-busting requests or provider-supported
    checks. Match the exact commit through an immutable marker when possible, or
    record a weaker unique content fingerprint.
16. When analytics may be affected, verify the expected production loader,
    configuration, owner-selected URL policy, and provider evidence state.
17. Create a metadata-only closeout branch and non-draft pull request recording
    the main PR, squash commit, CI, actual provider deployment, canonical-host
    verification, analytics result, and submodule state. Wait for CI, self-review,
    and squash-merge the closeout.

No normal step requires human approval. Record a task in `block.md` only if an
external system enforces a human-only action or required permission is absent.
Never force-push, bypass checks, expose credentials, contradict the owner-selected
URL policy, mutate an unverified production path, or fabricate completion.

## Completion rule

A run is incomplete unless:

- bootstrap was complete and current before mutation;
- the real production provider, project, repository, branch, build, and output
  path were used;
- all required and expected CI passed;
- final automated self-review was clean;
- the exact squash commit reached the actual production provider;
- the canonical public hostname independently exposed the expected change;
- analytics behavior was verified when relevant;
- the metadata-only closeout pull request passed CI, was self-reviewed, and was
  squash-merged.

A preview, generated branch, provider build log, workflow URL, `CNAME`, local
artifact, or HTTP 200 alone is not completion.
