# Automated pull-request delivery for consuming repositories

This contract applies to automated data and site changes in every consuming
website repository. Human approval is not required, but a real pull request,
complete CI, final self-review, squash merge, deployment evidence, and live
verification cannot be skipped.

## Main pull request

1. Inspect repository instructions, branch, upstream, dirty files, and current
   submodule state. Preserve unrelated work.
2. Fetch the remote default branch and create a fresh branch from it using the
   prefix in `site.md`.
3. Fetch the `seo-skills` submodule remote. If an allowed newer commit exists,
   update the submodule pointer on the same branch.
4. Implement one coherent scope and update today's daily report and current
   status.
5. Run the smallest authoritative local validations.
6. Stage explicit paths, inspect the staged diff, commit, push, and create a
   real non-draft pull request.
7. Determine the repository's required and expected CI checks. Wait until all
   complete successfully. A missing expected check is not a pass.
8. Read the complete final pull-request diff, commits, changed-file list, check
   results, and mergeability. Review scope, correctness, private-data leakage,
   generated artifacts, tests, and submodule compatibility.
9. If review finds a problem, fix it on the same branch, push, wait for CI again,
   and repeat the complete review.
10. When CI is green and final self-review is clean, squash-merge the pull
    request and delete its branch.

The agent performs the review itself. Do not manufacture approval from a second
identity or bypass branch protection.

## Site deployment

For a site change, capture the squash commit and locate the production
deployment triggered by that exact commit. Use the provider and production
workflow/environment documented in `site.md` plus live repository configuration.

Wait for a successful terminal deployment. A successful PR check is not
deployment evidence. An HTTP 200 is not enough: verify the changed page or
behavior on the configured public URL, including relevant visible rendering,
metadata, links, or performance output.

If deployment fails, diagnose and deliver a corrective pull request through the
same lifecycle. If no safe correction is possible, update `block.md` through a
pull request with the exact evidence and minimal human-only action.

## Closeout pull request

Merge and deployment facts become known after the main pull request is merged,
so create a metadata-only closeout pull request. Update the same day's report and
`status.md` with:

- main pull request URL and squash commit;
- final CI checks and self-review outcome;
- production deployment provider, URL, commit, and conclusion;
- public verification URL, time, and observed result;
- any corrective pull requests or unresolved blockers.

The closeout is a real non-draft pull request. Wait for its CI, self-review the
complete diff, and squash-merge it. A metadata-only closeout does not need to
wait for a site deployment unless it changes rendered or deployed content.

## Prohibited shortcuts

- direct automated push to the consuming repository's default branch;
- force-push, reset, or stash of unrelated work;
- merge while an expected check is queued, missing, skipped, failed, or cancelled;
- merge before the final self-review;
- fake review identities or fabricated evidence;
- treating a local commit, issue, draft PR, workflow URL, or HTTP status alone
  as completed delivery.
