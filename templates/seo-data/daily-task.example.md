# Daily SEO task

## Objective

Run one fully autonomous, evidence-backed SEO operating cycle for the site in
`site.md`, but only after the mandatory production bootstrap is complete and
current. No normal post-bootstrap step requires human approval.

## Schedule

- Frequency: daily
- Timezone: use `site.md`
- Configuration owner: authorized session-level scheduler outside this repository
- Data window: use the lookback and finalization lag in `site.md`
- Change unit: one coherent outcome per main pull request; multiple focused pull
  requests are required when independent technical defects must be repaired in
  the same cycle

The repository must not contain a cron job, webhook, hosted agent runner, or
model-provider credential whose purpose is to execute this task. Existing CI and
deployment workflows may remain and may be used as delivery evidence; they do
not run the SEO agent.

## Mandatory bootstrap policy

Read `$bootstrap-seo-site`, the existing `site.md`, `status.md`, and newest daily
report before every run. Bootstrap state and durable production topology live in
`site.md` under its existing `## Deployment` section. Do not create, remove, or
rename files under `.github/seo-data` for bootstrap.

If `site.md` does not say `Bootstrap status: complete` and `Production chain
verified: yes`, lacks required production fields, contains placeholders,
contradicts current provider or public evidence, or may have become stale, freeze
normal operation and perform a read-only bootstrap audit.

Do not change content, metadata, analytics, dependencies, redirects, DNS,
domains, build settings, deployment settings, provider settings, robots,
sitemap, structured data, or rendered behavior until bootstrap proves:

```text
source repository + production branch + exact commit
    -> actual provider production deployment
    -> canonical public hostname
    -> expected deployed content or immutable marker
```

A passing workflow, generated branch, `gh-pages`, `CNAME`, preview, provider log,
or HTTP 200 response is not enough. The bootstrap pull request is metadata-only
except for the pinned skill submodule and CI invocation. It updates only existing
SEO-data files.

After bootstrap, CI must opt into strict validation:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data \
  --require-bootstrap
```

Re-bootstrap whenever the domain, DNS or edge provider, hosting provider,
provider project, source repository, production branch, monorepo root, build
command, output directory, deployment trigger, platform architecture, analytics
provider, URL policy, or public commit correspondence changes or may have
changed.

## Mandatory analytics policy

Every canonical production site must have runtime web analytics, Search Console
coverage, and infrastructure analytics when the verified provider exposes it.
Read and enforce `$ensure-site-analytics` on every post-bootstrap run.

Do not remove, disable, replace, gate, materially reduce, redact, or expand
analytics based on agent preference. Missing, broken, leaking,
policy-inconsistent, or unverified analytics is a same-cycle technical defect.

## Same-cycle technical repair policy

After bootstrap, any reproducible and actionable technical defect discovered
during the run must be repaired during the same operating cycle whenever a safe
technical path exists. This includes build, CI, the verified production
deployment, runtime, analytics, crawlability, indexability, robots.txt, sitemap,
canonical, redirect, metadata, structured data, server rendering, internal
links, accessibility, performance, and primary user-flow failures.

Technical repair preempts routine SEO experiments, content production,
promotion, and reporting-only work. A production regression must be repaired or
safely rolled back through the provider project recorded in `site.md`, deployed,
publicly verified on the canonical hostname, and closed out before the cycle is
complete.

Only a genuine human-only action, unavailable permission, billing or legal
approval, or absence of a safe rollback path may block completion. Record exact
evidence and mitigation in `block.md`.

## Required sequence

1. Read `$bootstrap-seo-site`, `site.md`, `status.md`, and current public/provider
   evidence. If bootstrap is incomplete or stale, perform only the read-only
   bootstrap lifecycle and stop normal mutation.
2. Read the pinned `$ensure-site-analytics`, `$collect-seo-data`, and
   `$change-seo-site` skills, all existing `.github/seo-data/*.md` files, and the
   newest reports.
3. Fetch the remote default branch and create a fresh branch from its exact
   latest commit.
4. Check the `seo-skills` submodule upstream, review the full diff, and include a
   compatible pointer update and any existing-file metadata migration in the
   same pull request.
5. Audit analytics metadata, source, built output, canonical production runtime,
   owner-selected URL reporting, Search Console, infrastructure analytics, and
   provider evidence.
6. Collect finalized configured evidence without committing raw data or private
   provider identifiers. Mark unavailable or partial sources accurately.
7. Triage every reproducible technical defect immediately and complete each
   actionable repair before routine work.
8. Write or append `.github/seo-data/daily/YYYY-MM-DD.md`; refresh `status.md`,
   maintain future work in `plan.md`, and keep `block.md` limited to genuine
   human-only or permission blockers.
9. When evidence supports a routine improvement, implement at most one
   speculative coherent change. This limit does not apply to confirmed defects.
10. Validate locally, using `--require-bootstrap` after bootstrap, push each
    branch, and create real non-draft pull requests.
11. Wait for all required and expected CI. Self-review each complete final diff,
    production-topology assumptions, analytics and URL behavior, generated
    output, and checks; fix and repeat if needed, then squash-merge.
12. For each site change, locate the exact squash commit in the actual provider
    project recorded in `site.md`, wait for successful production deployment,
    and independently verify the canonical public hostname. Do not accept a
    preview, generated branch, workflow URL, `CNAME`, or HTTP 200 alone.
13. Open metadata-only closeout pull requests with final evidence; wait for CI,
    self-review, and squash-merge them.
14. Continue autonomously while safe progress is possible. Record a blocker only
    when an external system enforces a human-only action or permission is absent.

## Daily completion

A day is complete only after bootstrap was current before mutation, mandatory
analytics is present and verified, every actionable defect has been repaired or
truthfully blocked, all main and closeout pull requests are squash-merged, the
exact commit reached the verified provider project, and the canonical hostname
independently exposed the expected result.

A failed or missing CI check, failed provider deployment, preview, generated
branch, local commit, issue, draft PR, workflow URL, provider export, `CNAME`, or
HTTP 200 alone is not completion.
