---
name: change-seo-site
description: Implement and deliver an evidence-backed SEO or GEO change directly in a website repository. Use when changing content, metadata, structured data, internal links, crawlability, performance, or other search-facing behavior and the anonymous pushed commit must pass CI, deploy successfully, and be verified on the public site.
---

# Change SEO Site

## Overview

Ship one coherent SEO improvement from current evidence to verified production.
Every change uses an anonymous direct commit to the default branch, waits for
exact-commit CI and production deployment, verifies the live result, and closes
out the Markdown operating record with another anonymous commit.

## Required context

Read completely:

- repository instructions such as `AGENTS.md` and `CLAUDE.md`;
- `.github/seo-data/site.md`, `daily-task.md`, `status.md`, `plan.md`, and
  `block.md`;
- the newest relevant reports in `.github/seo-data/daily/`;
- [`references/deployment-verification.md`](references/deployment-verification.md);
- [`../../references/direct-delivery.md`](../../references/direct-delivery.md).

When current analytics are needed, use `$collect-seo-data` first. Do not invent a
site change merely to satisfy the schedule. A no-op day may update only the daily
evidence record through the same anonymous direct-commit lifecycle.

## Workflow

### 1. Select one evidence-backed change

Use current data, `status.md`, `plan.md`, repository issues, and live inspection
to choose at most one coherent outcome. Define before editing:

- the observed problem and supporting evidence;
- the target public page or behavior;
- files expected to change;
- local validation and expected CI;
- the production deployment and live acceptance check.

### 2. Synchronize the default branch and skills

Inspect branch, upstream, dirty files, and submodule state. Require a clean local
default branch and fast-forward it to its remote. Preserve unrelated work.

Fetch the `seo-skills` submodule remote. If a newer allowed commit exists,
update the submodule pointer in the same main commit and review compatibility.
Do not edit submodule files locally.

### 3. Implement narrowly

Follow the site's architecture and content rules. Preserve public paths,
canonical ownership, navigation, and unrelated content unless evidence-backed
scope explicitly requires a change. Prefer reversible, source-controlled,
testable changes visible in generated output.

This skill authorizes site changes, direct repository delivery, deployment wait,
verification, and corrective commits without human approval. It does not
authorize exposing secrets or fabricating external endorsements.

### 4. Record the work

Write or append `.github/seo-data/daily/YYYY-MM-DD.md`. Record evidence, intended
outcome, changed files, validation, submodule movement, and pending delivery
fields. Update `status.md` with current facts and `plan.md` with future work. Use
`block.md` only for a genuine human-only or permission blocker.

### 5. Validate and self-review

Run the repository's smallest authoritative checks plus:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data
```

Read the complete intended diff and generated output. Review correctness, SEO
semantics, public-data safety, scope, regressions, tests, and submodule
compatibility. Fix every issue before committing.

### 6. Commit and push anonymously

Configure the repository-local anonymous name and email from `site.md` and
verify effective config values and origins. Stage explicit paths, inspect the
staged diff, and commit directly on the default branch. Fetch once more; if the
remote advanced, rebase only the automation's own commit, rerun validation and
self-review, then push normally. Never open a pull request, force-push, or amend
already-pushed history.

### 7. Wait for exact-commit CI

Capture the pushed commit and wait for every required and expected check tied to
that exact commit. Missing, queued, skipped, cancelled, timed-out, or failed
checks are not ready. If CI fails, diagnose and push a corrective commit through
the same validation and review process, then wait for the new exact commit.

### 8. Wait for production deployment

Locate the production deployment triggered by the exact successful commit using
the provider, workflow, environment, and verification URL in `site.md` plus live
repository configuration. Wait for a successful terminal state. A CI start,
workflow URL, preview, or HTTP 200 alone does not prove deployment.

If deployment fails, diagnose and push a corrective commit, then repeat CI and
deployment waiting. Continue while safe progress is possible. Record a blocker
only when an external human-only action or missing permission is the true cause.

### 9. Verify production and close out

Inspect the public site and verify the acceptance check defined before editing,
including relevant visible content, title, description, canonical, structured
data, links, robots/sitemap output, headers, redirects, or performance signal.

Push a metadata-only anonymous closeout commit that updates today's report and
`status.md` with the main commit, CI, deployment, public URL, verification time,
and observed result. Validate and self-review the closeout diff and wait for its
exact-commit CI. No deployment wait is needed unless the closeout changes
rendered site output.

## Completion criteria

Do not report completion until all are true:

- the anonymous main commit was pushed to the default branch;
- all required and expected CI checks for the exact commit passed;
- the exact commit deployed successfully to production;
- the changed behavior was verified on the public site;
- an anonymous closeout commit recorded the evidence and its CI passed.
