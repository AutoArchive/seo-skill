---
name: operate-seo-site
description: Orchestrate one complete scheduled or manually requested SEO operating cycle for a consuming website repository. Use for daily SEO patrols, portfolio site rounds, analytics and search-evidence refreshes, same-cycle technical repair, evidence-backed site improvements, optional research publication, and truthful pull-request, deployment, and Markdown closeout.
---

# Operate SEO Site

## Purpose

Use this skill as the common entrypoint for recurring SEO operation. Keep the
shared workflow here and keep the consuming repository's `daily-task.md` limited
to site-specific priorities, exclusions, rotations, and acceptance checks.

The scheduler lives outside the repository. Do not create a GitHub Actions
workflow, repository cron job, webhook, hosted agent runner, or model-provider
credential merely to invoke this skill. Existing CI and deployment workflows
remain part of delivery.

## Required context

From the consuming repository, read completely:

- repository instructions such as `AGENTS.md` or `CLAUDE.md`;
- the site-owned metadata, daily task, current status, plan, and blocker record;
- promotion or editorial instructions when relevant to today's scope;
- the newest relevant daily records.

Use the consuming repository's existing filenames when its instructions define
equivalent records. Shared templates are examples, not a schema.

## Operating cycle

### 1. Establish site scope and current truth

Resolve exactly one canonical production site, its repository, production
source, timezone, analytics policy, data routes, deployment path, public
verification method, and current operator instructions. Stop rather than mix
properties or repositories when the identity is ambiguous.

Inspect the remote default branch, dirty files, active pull requests, current
production, and known blockers. Preserve unrelated work and do not race another
operator that is still making progress.

### 2. Review the pinned skills

Before writing records or site changes for each planned pull request, begin
`$deliver-github-pr` through its scope and branch-preparation steps. Use the
fresh branch it prepares and preserve unrelated work.

Inspect the `seo-skills` submodule and its allowed upstream branch. If a newer
commit exists, review its complete diff and compatibility before including the
pointer update in the first suitable consuming-repository pull request. Apply
only explicit new requirements with the minimum necessary site changes.

A submodule check or update does not authorize editing the shared skill
repository. Modify the shared repository only when the user explicitly requests
that change.

### 3. Verify analytics and collect evidence

Invoke `$ensure-site-analytics` on every cycle. Verify the implementation in
source, built output, canonical production runtime, URL-reporting behavior, and
provider evidence. Missing, broken, leaking, policy-inconsistent, or unverified
analytics is a technical defect.

Invoke `$collect-seo-data` for the configured finalization window. Read Google
Drive exports and infrastructure analytics through their configured read-only
routes. Preserve source-native semantics, label delayed or missing data
truthfully, and keep raw rows and private provider identifiers outside Git.

### 4. Triage work in priority order

Handle reproducible technical defects before experiments, content, reporting,
or promotion. When a safe repair or rollback exists, invoke
`$deliver-github-pr` as a search-facing site change and finish it during the
same operating cycle and local calendar day. Use a separate focused pull request
for each independent repair when combining them would reduce reviewability.

After technical work, select at most one speculative or experimental site
improvement supported by current evidence. Do not invent a change to make the
schedule appear productive. When the site-specific task calls for a long-form
research article, invoke `$research-blog`. Perform promotion only when the site's
instructions authorize the channel, content, and acceptance check.

### 5. Record public-safe results

Create or update today's normal daily record. Refresh current verified facts in
the status record, keep future work in the plan, and use the blocker record only
for a genuine human-only action, absent permission, legal or billing decision,
or lack of a safe rollback path.

Record outcomes and evidence rather than activity. Do not add a file, heading,
field, validator, or schema merely to match a shared example. Even when metrics
and production are unchanged, deliver a truthful daily record for the invoked
cycle.

### 6. Deliver and close out

Invoke `$deliver-github-pr` for every main, corrective, and closeout change. It
owns the fresh branch, real non-draft pull request, complete expected CI,
mandatory from-scratch final review after CI, squash merge, and any applicable
exact production deployment and public verification. If review or deployment
finds a problem, use its corrective loop and repeat the complete lifecycle. No
human or second reviewer is required.

A preview, workflow URL, script tag, provider export, or HTTP 200 alone is not
completion. Supply final merge, deployment, public acceptance, and verification
criteria to `$deliver-github-pr` and record its evidence through the consuming
site's closeout process.

## Completion criteria

Complete the cycle only when:

- analytics implementation, URL policy, Search Console state, infrastructure
  evidence, and source freshness are verified or truthfully qualified;
- every actionable technical defect is repaired and publicly verified, or has a
  truthful blocker with mitigation evidence;
- today's site-specific work and public-safe evidence are recorded;
- all main and closeout pull requests have green expected CI, a clean
  from-scratch review of the complete final PR, and a squash merge;
- every rendered site change has deployed from the exact squash commit and the
  affected and representative unaffected public behavior has been verified.

Merged head-branch deletion is optional hygiene and is not a completion
criterion.
