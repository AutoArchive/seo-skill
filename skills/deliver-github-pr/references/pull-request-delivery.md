# Pull-request delivery checklist

Use this checklist for a main, corrective, data-only, or metadata-only pull
request. The calling skill supplies domain-specific evidence and acceptance
requirements.

## Prepare and open

1. Re-read the exact user request and repository instructions.
2. Inspect the default branch, upstream, dirty files, active pull requests, and
   dependency pointers. Preserve unrelated work.
3. Define one coherent result, smallest compatible diff, preserved behavior,
   authoritative checks, risk, rollback, deployment applicability, and public
   acceptance when applicable.
4. Fetch the remote default branch and create a fresh branch, unless the user
   explicitly authorized updating an existing pull-request branch.
5. Implement narrowly, run local validation, and inspect generated output when
   applicable.
6. Stage explicit paths. Read the complete staged diff before commit.
7. Commit, push, and create a real non-draft pull request. Make the description
   match the final scope and evidence.

## Determine and wait for CI

Inspect repository workflow files, branch rules, the pull request's check suite,
and recent equivalent pull requests when needed. Identify checks that are
required by configuration and checks normally expected for the changed scope.

Wait for all of them. Do not treat a missing expected check as success. Queued,
skipped, cancelled, timed-out, neutral when success is expected, action-required,
and failed conclusions prohibit merge.

## From-scratch final review

Start only after CI is green. Deliberately discard the earlier editing review
and reconstruct the work from its source:

1. Re-read the original user request and every applicable repository rule.
2. Verify the PR base, head, title, description, author, mergeability, commits,
   changed-file list, and complete base-to-head diff.
3. Inspect generated output, test results, CI logs or summaries, dependency and
   submodule movement, and review comments relevant to the final head.
4. Check that every changed line supports the requested outcome and that no
   requested behavior is missing.
5. Check correctness, regression risk, error paths, public or private data
   leakage, secrets, site-specific information in shared code, compatibility,
   rollback, deployment routing, and caller-supplied acceptance criteria.
6. Re-run or independently inspect the evidence most likely to catch a false
   positive.

If any issue is found, fix it on the same branch, update the PR description when
scope or evidence changed, push, wait for complete CI, and restart this checklist
from item 1. Reviewing only the incremental fix is not sufficient.

## Merge and handoff

Squash-merge only after the final head has green CI and a clean from-scratch
review. Capture the PR URL, final checks, review conclusion, and exact squash
commit. Attempt safe branch deletion only when supported.

If production applies, continue immediately with
[`deployment-verification.md`](deployment-verification.md). Any corrective or
closeout change is a new pull request and repeats this entire checklist.

## Prohibited shortcuts

- direct automated push to the default branch;
- force-push, reset, stash, or overwrite of unrelated work;
- draft PR, issue, local commit, preview, workflow URL, provider status, or HTTP
  status used as a substitute for completed delivery;
- merge before every expected check succeeds;
- merge based on a pre-CI or latest-commit-only review;
- fake reviewer identities, fabricated evidence, or bypassed branch protection.
