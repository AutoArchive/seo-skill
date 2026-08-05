---
name: change-seo-site
description: Implement and deliver an evidence-backed SEO or GEO change in a website repository through a real pull request. Use when changing content, metadata, structured data, internal links, crawlability, performance, or other search-facing behavior and the change must pass CI, receive an automated final self-review, squash merge, deploy successfully, and be verified on the public site.
---

# Change SEO Site

## Overview

Ship one coherent SEO improvement from current evidence to verified production.
Every consuming-repository change uses a real pull request, waits for CI,
receives a complete final self-review, squash-merges, waits for the exact
production deployment, verifies the live result, and closes out the Markdown
operating record.

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

## Workflow

### 1. Select one evidence-backed change

Use current data, `status.md`, `plan.md`, repository issues, and live inspection
to choose at most one coherent outcome. Define before editing:

- the observed problem and supporting evidence;
- the target public page or behavior;
- files expected to change;
- local validation and expected CI;
- the production deployment and live acceptance check.

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
testable changes visible in generated output.

This skill authorizes site changes, pull-request delivery, squash merge,
deployment wait, verification, and corrective pull requests without human
approval. It does not authorize exposing secrets or fabricating endorsements.

### 4. Record the work

Write or append `.github/seo-data/daily/YYYY-MM-DD.md`. Record evidence, intended
outcome, changed files, validation, submodule movement, and pending delivery
fields. Update `status.md` with current facts and `plan.md` with future work. Use
`block.md` only for a genuine human-only or permission blocker.

### 5. Validate and create the real pull request

Run the repository's smallest authoritative checks plus:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data
```

Read the intended diff and generated output. Review correctness, SEO semantics,
public-data safety, scope, regressions, tests, and submodule compatibility.
Stage explicit paths, commit, push the fresh branch, and create a real non-draft
pull request. Its body must state evidence, scope, tests, deployment target,
acceptance check, and any submodule update.

### 6. Wait for CI and self-review

Wait until every required and expected existing CI check reaches success. Treat
missing, queued, skipped, cancelled, timed-out, and failed checks as not ready.

After CI is green, read the complete final pull-request diff, commits, generated
output, and check results. Fix every issue on the same branch, wait for CI again,
and repeat the complete self-review. No human or second reviewer is required.

### 7. Squash merge

Only after green CI and a clean final self-review, squash-merge the real pull
request and delete its branch. Capture the pull-request URL and resulting squash
commit. Never push the automated change directly to the default branch, bypass
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

Create a metadata-only closeout branch and non-draft pull request. Update today's
report and `status.md` with the main PR, squash commit, CI, deployment, public
URL, verification time, and observed result. Wait for CI, self-review the entire
closeout diff, and squash-merge it. No deployment wait is needed unless the
closeout changes rendered output.

## Completion criteria

Do not report completion until all are true:

- a real change pull request exists and is squash-merged;
- all required and expected CI checks passed;
- the agent completed a clean final diff review after CI;
- the exact squash commit deployed successfully to production;
- the changed behavior was verified on the public site;
- a closeout pull request recorded the evidence and was squash-merged.
