---
name: deliver-github-pr
description: Deliver one authorized, coherent repository change through a real GitHub pull request. Use when an agent must prepare a fresh branch, validate and stage an intentional diff, open a non-draft PR, wait for every required and expected CI check, restart review from the original request after CI, fix and repeat when needed, and squash-merge without human review.
---

# Deliver GitHub PR

## Purpose

Own the reusable GitHub pull-request lifecycle. The calling skill owns what to
change and any post-merge production work; this skill owns the branch, PR, CI,
from-scratch final review, repair loop, and squash merge.

Read [`references/pull-request-delivery.md`](references/pull-request-delivery.md)
completely before delivery.

## Required context

Resolve the explicit user request, repository instructions, remote default
branch, current worktree, intended files, authoritative local checks, expected
GitHub checks, and whether an existing pull request is already in scope.

Do not modify, supersede, close, or merge another contributor's pull request
unless the user explicitly authorizes that exact action. Preserve unrelated
work and do not race an active operator.

## Workflow

### 1. Confirm one coherent scope

State the requested outcome, why it is necessary, the smallest compatible diff,
what behavior must remain unchanged, and the validation that can prove the
result. Split unrelated outcomes into separate pull requests.

### 2. Prepare the branch safely

Inspect branch, upstream, dirty files, and dependency or submodule state. Fetch
the remote default branch. Create or confirm a fresh branch from it for this
delivery, or check out the explicitly authorized existing pull-request branch.
Never stash, reset, force-push, or overwrite unrelated work.

### 3. Validate and open the pull request

Run the smallest authoritative local checks. Stage only intended paths and read
the staged diff before committing. Push the branch and create a real non-draft
pull request whose description records the rationale, scope, preserved behavior,
validation, risks, rollback, and post-merge acceptance check when applicable.

Do not substitute an issue, draft PR, local commit, direct default-branch push,
or workflow URL for delivery.

### 4. Wait for complete CI

Determine both required and expected checks from repository configuration,
branch rules, existing workflows, and normal project behavior. Wait until every
expected check reaches a successful terminal conclusion. Missing, queued,
skipped, cancelled, timed-out, neutral when success is expected, and failed
checks prohibit merge.

### 5. Restart review from the beginning

After CI succeeds, begin a new review pass; do not continue an earlier pre-CI
review or rely on memory of the edits.

Re-read the original user request and repository instructions. Then inspect the
complete base-to-head diff, changed-file list, every commit, PR description,
generated output, dependency pointers, test and check results, mergeability, and
any review comments. Verify scope, correctness, edge cases, regressions, private-
data safety, rollback, and caller-specific acceptance criteria.

If review finds any issue, fix it on the same branch, rerun relevant local
checks, push, wait for every expected CI check again, and restart this entire
from-scratch review step. A partial review of only the latest fix is prohibited.

No second identity or human reviewer is required. Never fabricate approval.

### 6. Squash merge and hand off

Only after green CI and a clean from-scratch review, squash-merge the pull
request. Capture its URL and exact squash commit. Delete the merged head branch
only when safe deletion is supported; branch cleanup is not a completion
criterion.

Return the PR, CI, review, and squash evidence to the caller. The caller remains
responsible for production deployment, public verification, and closeout. Use
this skill again for every corrective or metadata-only closeout pull request.

## Completion criteria

Complete GitHub delivery only when:

- the intended diff is committed on the authorized branch and represented by a
  real non-draft pull request;
- every required and expected check succeeded;
- the agent restarted review after CI and inspected the complete final PR from
  the original request through the final head;
- any review fix completed a new CI wait and another full restart review;
- the final PR was squash-merged and its exact commit was captured.
