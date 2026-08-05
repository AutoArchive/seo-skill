---
name: deliver-github-pr
description: Deliver one authorized, coherent repository change through a real GitHub pull request and, when applicable, the exact production deployment and public acceptance check. Use when an agent must implement or package a focused change, open a non-draft PR, wait for complete CI, restart review from the original request, squash-merge, monitor production, repair failures, verify the public result, and close out without human review.
---

# Deliver GitHub PR

## Purpose

Own one repository change from a confirmed scope through truthful completion.
This skill owns the branch, implementation boundary, pull request, CI,
from-scratch final review, squash merge, and any applicable production
deployment, public acceptance, corrective change, and metadata closeout.

The calling skill supplies domain evidence and acceptance criteria. It does not
reimplement GitHub or deployment mechanics.

Always read
[`references/pull-request-delivery.md`](references/pull-request-delivery.md).
When the change has a production deployment or rendered public output, also read
[`references/deployment-verification.md`](references/deployment-verification.md).
For search-facing website changes, additionally read
[`references/seo-site-change.md`](references/seo-site-change.md).

## Required context

Resolve the explicit user request, repository instructions, remote default
branch, current worktree, intended files, authoritative local checks, expected
GitHub checks, and whether an existing pull request is explicitly in scope.

Before editing, state whether the change affects production or public output. If
it does, resolve the production provider, project or service, source repository
and branch, build and output path, canonical public URL, exact acceptance check,
representative unaffected behavior, and rollback. Repository notes are routing
hints; verify live configuration when it can drift.

Do not modify, supersede, close, or merge another contributor's pull request
unless the user explicitly authorizes that exact action. Preserve unrelated
work and do not race an active operator.

## Workflow

### 1. Confirm one coherent scope

State the requested outcome, evidence, smallest compatible diff, preserved
behavior, validation, risk, rollback, and post-merge acceptance check. Split
unrelated outcomes into separate pull requests.

### 2. Prepare the branch safely

Inspect branch, upstream, dirty files, active pull requests, and dependency or
submodule state. Fetch the remote default branch. Create or confirm a fresh
branch from it, or check out the explicitly authorized existing pull-request
branch. Never stash, reset, force-push, or overwrite unrelated work.

### 3. Implement, validate, and open the pull request

Make the narrowest change that achieves the scoped outcome. Run the smallest
authoritative local checks and inspect generated output when relevant. Stage
only intended paths and read the staged diff before committing.

Push the branch and create a real non-draft pull request whose description
records the rationale, scope, preserved behavior, validation, risks, rollback,
deployment target, and public acceptance check when applicable.

Do not substitute an issue, draft PR, local commit, direct default-branch push,
preview, or workflow URL for delivery.

### 4. Wait for complete CI

Determine required and expected checks from repository configuration, branch
rules, existing workflows, and normal project behavior. Wait until every
expected check reaches a successful terminal conclusion. Missing, queued,
skipped, cancelled, timed-out, action-required, failed, and neutral when success
is expected all prohibit merge.

### 5. Restart review from the beginning

After CI succeeds, begin a new review pass. Re-read the original user request
and repository instructions, then inspect the complete base-to-head diff,
changed-file list, every commit, PR description, generated output, dependency
pointers, test and check results, mergeability, review comments, and all
caller-supplied domain acceptance criteria.

Verify scope, correctness, edge cases, regressions, private-data safety,
rollback, deployment assumptions, and affected and representative unaffected
behavior. Do not rely on the earlier editing review or review only the latest
commit.

If review finds any issue, fix it on the same branch, rerun local checks, push,
wait for complete CI again, and restart this entire review from the original
request. No second identity or human reviewer is required. Never fabricate
approval.

### 6. Squash merge

Only after green CI and a clean from-scratch review, squash-merge the pull
request. Capture its URL and exact squash commit. Delete the merged head branch
only when safe deletion is supported; branch cleanup is not a completion
criterion.

### 7. Monitor production when applicable

If the change has no production deployment or public output, record that fact
and proceed to closeout. Otherwise locate the production deployment triggered
by the exact squash commit and wait through queued and in-progress states until
the provider reports a successful terminal production result.

On failure, diagnose the narrow cause and deliver a corrective pull request
through this complete workflow. After its squash merge, monitor the replacement
commit. Continue while safe progress is possible; a real human-only permission,
legal, billing, or no-safe-rollback blocker must be recorded truthfully rather
than treated as success.

### 8. Verify publicly and close out

Run the public acceptance check defined before editing. Verify the changed
behavior and representative unaffected behavior; an HTTP 200, source diff,
preview, check mark, or provider dashboard alone is insufficient.

Record the final PR, CI, review, squash commit, deployment, public URL,
verification time, observed result, and residual risk in the repository's
normal operating records. Deliver any metadata-only closeout through this same
PR, CI, restart-review, and squash lifecycle. Wait for another deployment only
if the closeout changes deployed or rendered output.

## Completion criteria

Complete delivery only when:

- the authorized diff was represented by a real non-draft pull request;
- every required and expected check succeeded;
- the agent restarted review after CI and inspected the complete final PR from
  the original request;
- every review or corrective fix completed a new CI wait and another full
  restart review;
- the final pull request was squash-merged and its exact commit was captured;
- every applicable production deployment for the final change succeeded for
  that exact commit;
- every applicable public acceptance and representative unaffected check
  passed; and
- required closeout evidence was itself delivered through the same lifecycle.
