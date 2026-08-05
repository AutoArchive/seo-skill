# Daily SEO task

## Objective

Run one fully autonomous, evidence-backed SEO operating cycle for the site in
`site.md`. No normal step requires human approval.

## Schedule

- Frequency: daily
- Timezone: use `site.md`
- Configuration owner: authorized session-level scheduler outside this repository
- Data window: use the lookback and finalization lag in `site.md`
- Change unit: one coherent outcome per main pull request; multiple focused pull
  requests are required when independent technical defects must be repaired in
  the same cycle

The repository must not contain a GitHub Actions workflow, cron job, webhook,
hosted agent runner, or model-provider credential whose purpose is to execute
this task. The invoking session supplies model access and connected tools.
Existing CI and deployment workflows may remain and may be used as delivery
evidence; they do not run the SEO agent.

## Same-cycle technical repair policy

Any reproducible and actionable technical defect discovered during the run must
be repaired during the same scheduled operating cycle and local calendar day
whenever a safe technical path exists. This includes build, CI, deployment,
runtime, data-generation, crawlability, indexability, robots.txt, sitemap,
canonical, redirect, metadata, structured-data, server-rendering, internal-link,
accessibility, performance, and primary user-flow failures.

Technical repair preempts routine SEO experiments, source discovery, content
production, promotion, and reporting-only work. Do not defer a confirmed defect
merely because another pull request was planned or already opened. Use additional
focused pull requests when necessary. A production regression must be repaired
or safely rolled back, deployed, publicly verified, and closed out before the
cycle is considered complete.

Only a genuine human-only action, unavailable permission, billing or legal
approval, or absence of a safe rollback path may prevent same-cycle completion.
Record exact evidence and mitigation in `block.md`. Provider queues that cross
midnight remain part of the same repair operation rather than future backlog.

## Required sequence

1. Read the pinned `$collect-seo-data` skill, `$change-seo-site` when a site
   change is justified, all `.github/seo-data/*.md` files, and newest reports.
2. Fetch the remote default branch and create a fresh branch from it.
3. Check whether the `seo-skills` submodule has an allowed update and include an
   available update in the same main pull request.
4. Collect finalized configured evidence without committing raw data or private
   identifiers. Mark disabled or unavailable sources accurately; never convert
   missing data into zero.
5. Triage every reproducible technical defect immediately. Invoke
   `$change-seo-site` and complete each actionable repair under the same-cycle
   policy before routine work continues.
6. Write or append `.github/seo-data/daily/YYYY-MM-DD.md`; refresh `status.md`,
   maintain future work in `plan.md`, and keep `block.md` limited to genuine
   human-only or permission blockers.
7. When evidence supports a routine site improvement, implement at most one
   speculative or experimental coherent change. This limit does not apply to
   confirmed technical defects covered by the same-cycle policy.
8. Validate locally, push each branch, and create real non-draft pull requests.
9. Wait for all required and expected existing CI, self-review each complete
   final diff, fix and repeat if needed, then squash-merge. Attempt to delete
   merged head branches when safe deletion is supported, but treat branch
   cleanup as best-effort and non-blocking.
10. For each site change, wait for the exact squash commit to deploy successfully
    through the repository's existing delivery path and verify the changed
    behavior on the public site.
11. Open metadata-only closeout pull requests with final evidence; wait for CI,
    self-review, and squash-merge them.
12. Continue autonomously while safe progress is possible. Record a `block.md`
    item only when an external system enforces a human-only action or required
    permission is absent. A missing branch-deletion operation or an undeleted
    merged automation branch is not a blocker.

## Daily completion

A day is complete only after every confirmed actionable technical defect has
been repaired and verified, or has a truthful human-only blocker with mitigation
evidence, and all main and closeout pull requests are squash-merged. A
site-change day also requires successful production deployments for the exact
squash commits and public verification. Merged branch cleanup is optional
repository hygiene and does not affect completion. A failed or missing CI check,
failed deployment, local-only commit, issue, draft PR, workflow URL, or HTTP 200
alone is not completion.
