---
name: change-seo-site
description: Implement and deliver an evidence-backed SEO or GEO change in a website repository through a real pull request. Use when changing content, metadata, structured data, internal links, crawlability, performance, or other search-facing behavior and the change must pass CI, receive an automated final self-review, squash merge, deploy successfully, and be verified on the public site.
---

# Change SEO Site

## Overview

Ship evidence-backed SEO improvements from current evidence to verified
production. Every consuming-repository change uses a real pull request, waits
for CI, receives a complete final self-review, squash-merges, waits for the exact
production deployment, verifies the live result, and closes out the Markdown
operating record.

A coherent change remains the unit of one main pull request. It is not a daily
quota. A daily operating cycle may and must deliver multiple focused pull
requests when independent actionable technical defects are discovered.

## Incremental change and blast-radius policy

Search-facing production changes must be incremental, independently reviewable,
reversible, and attributable to one clear problem or hypothesis. A coherent
outcome is not permission to modernize or rewrite the whole site at once.

Before editing rendered behavior, capture the current production baseline that
is relevant to the proposed change. Depending on scope, this includes the exact
source commit and release, affected canonical URLs, titles and descriptions,
route and redirect ownership, navigation, sitemap and robots output, structured
data, representative screenshots, generated HTML, internal links, analytics
window and source freshness, and the current public acceptance result. Missing
analytics is uncertainty, not evidence that a broad change is safe.

For routine SEO, GEO, content, and product-site work:

- change the smallest independently deployable public behavior that can test the
  hypothesis or fix the observed problem;
- preserve unrelated design, copy, navigation, routes, canonical ownership,
  redirects, metadata, analytics, and content;
- prefer additive or local edits before replacement, deletion, consolidation,
  or migration;
- isolate variables where practical: do not change page purpose, information
  architecture, navigation, visual system, titles, descriptions, and route
  ownership in one experiment;
- state the blast radius, affected route family, expected search/user effect,
  acceptance check, and exact rollback before implementation;
- verify representative unaffected pages when a shared component or template is
  modified.

A routine cycle must not perform an unphased full-site redesign, bulk content
rewrite, mass route or canonical migration, navigation and information-
architecture replacement, design-system replacement, or simultaneous
content/metadata/redirect overhaul. Qualitative preference, a new template,
missing analytics, a desire to make the site look modern, or a general SEO audit
is not sufficient evidence for such a change.

When a large migration is genuinely required, split it into independently
reviewable and deployable phases. Each phase must preserve a usable production
site, define its own acceptance checks and rollback point, and avoid depending on
unmerged later phases for correctness. Establish the migration baseline and plan
before the first rendered phase. Do not remove indexed content or public routes
until their replacement, redirect behavior, canonical ownership, internal links,
sitemap output, and production rendering have been verified.

The only exception to incremental delivery is an active production incident or
confirmed severe regression for which a smaller safe repair or rollback is not
available. Even then, prefer restoring the last known-good public behavior over
combining the repair with redesign or unrelated improvement work.

## Invocation boundary

Invoke this skill from an authorized scheduler outside the consuming repository,
preferably a ChatGPT or equivalent session-level scheduled task. Do not add or
modify GitHub Actions, repository cron jobs, webhooks, hosted agent runners, or
model-provider credential configuration to execute this skill. Existing CI and
deployment workflows may be observed or used for delivery, but must not host the
SEO agent. The invoking session owns model access and connected-tool credentials.

## Required context

Read completely:

- repository instructions such as `AGENTS.md` and `CLAUDE.md`;
- `.github/seo-data/site.md`, `daily-task.md`, `status.md`, `plan.md`, and
  `block.md`;
- the newest relevant reports in `.github/seo-data/daily/`;
- [`references/deployment-verification.md`](references/deployment-verification.md);
- [`../../references/pull-request-delivery.md`](../../references/pull-request-delivery.md).

When current analytics are needed, use `$collect-seo-data` first. Do not invent a
site change merely to satisfy the schedule. A no-op day may update only the daily
evidence record, but it still follows the pull-request lifecycle.

## Same-cycle technical repair SLA

A reproducible technical defect discovered during a scheduled run must be
repaired during that same operating cycle and local calendar day whenever a safe
technical path exists. This requirement covers, at minimum:

- failed, stuck, or non-reproducible builds and CI;
- failed deployments, runtime errors, broken production routes, or data-generation failures;
- crawlability, indexability, robots.txt, sitemap, canonical, redirect, metadata,
  structured-data, server-rendering, and internal-link regressions;
- broken primary user flows, severe accessibility defects, and material
  performance regressions;
- broken external or internal links that materially damage discovery or use.

Technical repair preempts routine content, promotion, source-discovery, and SEO
experiment work. Do not move an actionable defect into `plan.md` only because a
different change was already selected. The one-coherent-outcome rule is per pull
request, not per day: deliver additional focused pull requests when independent
repairs should not be combined.

For a production regression, continue through diagnosis, repair or safe
rollback, CI, squash merge, exact production-deployment verification, public
acceptance checks, and metadata closeout. If provider queues cross local
midnight, continue the same repair operation rather than classifying it as
future planned work.

Only a genuine human-only action, absent permission, legal constraint, billing
approval, or lack of a safe rollback path may prevent same-cycle completion. In
that case, record exact evidence, mitigation attempted, and the required external
action in `block.md` through a real pull request. Never disguise an ordinary
technical decision or queued check as a human blocker.

## Workflow

### 1. Triage evidence and define pull-request units

Use current data, `status.md`, `plan.md`, repository issues, CI/deployment state,
and live inspection to identify work. First classify any technical defects under
the same-cycle SLA. Then define one coherent outcome for each main pull request.
For every outcome, define before editing:

- the observed problem and supporting evidence;
- the current production baseline and why the proposed blast radius is the
  smallest safe one;
- the target public page or behavior;
- files expected to change;
- affected and representative unaffected routes;
- local validation and expected CI;
- the production deployment, live acceptance check, and rollback path.

A routine scheduled run may select at most one speculative or experimental SEO
improvement. This limit does not apply to confirmed technical defects that must
be repaired under the same-cycle SLA.

### 2. Prepare branch and dependency update

Inspect branch, upstream, dirty files, and submodule state. Fetch the remote
default branch and create a fresh branch using the prefix in `site.md`. Preserve
unrelated work.

Fetch the `seo-skills` submodule remote. If a newer allowed commit exists,
update the submodule pointer in the same pull request and review compatibility.
Do not edit submodule files locally.

### 3. Implement narrowly

Follow the site's architecture and content rules. Preserve public paths,
canonical ownership, navigation, and unrelated content unless evidence-backed
scope explicitly requires a change. Prefer reversible, source-controlled,
testable changes visible in generated output. Enforce the incremental change and
blast-radius policy above; do not turn a focused improvement into an incidental
site migration.

This skill authorizes site changes, pull-request delivery, squash merge,
deployment wait, verification, corrective pull requests, and safe rollback
without human approval. It does not authorize exposing secrets or fabricating
endorsements.

### 4. Record the work

Write or append `.github/seo-data/daily/YYYY-MM-DD.md`. Record evidence, intended
outcome, baseline, blast radius, changed files, rollback, validation, submodule
movement, and pending delivery fields. Update `status.md` with current facts and
`plan.md` with future work. Use `block.md` only for a genuine human-only or
permission blocker.

For same-cycle technical repairs, explicitly record discovery time, severity,
user or crawler impact, root cause, mitigation, repair PR, CI, exact deployment,
live verification, and whether any residual risk remains.

### 5. Validate and create the real pull request

Run the repository's smallest authoritative checks. The shared SEO-data checker
is optional and intentionally narrow:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data
```

Do not restructure Markdown or add labels merely to make the checker happy; it
cannot prove an SEO change is correct. Read the intended diff and generated
output. Review correctness, SEO semantics,
public-data safety, scope, blast radius, regressions, tests, rollback, and
submodule compatibility. Stage explicit paths, commit, push the fresh branch,
and create a real non-draft pull request. Its body must state evidence, baseline,
scope, affected and unaffected routes, tests, rollback, deployment target,
acceptance check, and any submodule update.

### 6. Wait for CI and self-review

Wait until every required and expected existing CI check reaches success. Treat
missing, queued, skipped, cancelled, timed-out, and failed checks as not ready.

After CI is green, read the complete final pull-request diff, commits, generated
output, and check results. Fix every issue on the same branch, wait for CI again,
and repeat the complete self-review. No human or second reviewer is required.

### 7. Squash merge and optional branch cleanup

Only after green CI and a clean final self-review, squash-merge the real pull
request. Capture the pull-request URL and resulting squash commit. Attempt to
delete the merged head branch only when the available repository tool supports
safe branch deletion.

Merged head-branch deletion is best-effort repository hygiene, not a completion
criterion. A connector that does not expose branch deletion, or a harmless
failure to delete an already-merged automation branch, must not create a
`block.md` item, require human action, delay closeout, or make the operation
incomplete. Never force-delete a default, protected, active, or unrelated
branch. Never push the automated change directly to the default branch, bypass
checks, or force-push.

### 8. Wait for production deployment

Locate the production deployment triggered by the exact squash commit using the
provider, workflow, environment, and verification URL in `site.md` plus live
repository configuration. Wait for a successful terminal state. A PR check,
workflow URL, preview, or HTTP 200 alone does not prove deployment.

If deployment fails, diagnose and deliver a corrective pull request through the
same lifecycle, then repeat CI and deployment waiting. Continue while safe
progress is possible. Record a blocker only when an external human-only action
or missing permission is the true cause.

### 9. Verify production and close out

Inspect the public site and verify the acceptance check defined before editing,
including relevant visible content, title, description, canonical, structured
data, links, robots/sitemap output, headers, redirects, or performance signal.
Verify the affected route and the representative unaffected routes selected in
the baseline so an unexpected shared-template regression is not mistaken for a
successful focused change.

Create a metadata-only closeout branch and non-draft pull request. Update today's
report and `status.md` with the main PR, squash commit, CI, deployment, public
URL, verification time, and observed result. Wait for CI, self-review the entire
closeout diff, and squash-merge it. No deployment wait is needed unless the
closeout changes rendered output. Branch cleanup may be attempted or skipped as
unsupported without affecting closeout completion.

## Completion criteria

Do not report completion until all are true:

- every confirmed same-cycle technical defect has either been repaired and
  verified or has a truthful human-only blocker with mitigation evidence;
- each real change pull request exists and is squash-merged;
- all required and expected CI checks passed;
- the agent completed a clean final diff review after CI;
- the exact squash commit deployed successfully to production;
- the changed behavior and representative unaffected behavior were verified on
  the public site;
- a closeout pull request recorded the evidence and was squash-merged.

Deletion of merged automation branches is not required for completion.
