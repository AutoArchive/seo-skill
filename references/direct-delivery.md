# Anonymous direct delivery

This contract applies to every data and site change. Human approval and pull
requests are not used. Local validation, final self-review, anonymous commits,
exact-commit CI, deployment evidence, and live verification cannot be skipped.

## Main commit

1. Inspect repository instructions, default branch, upstream, dirty files, and
   submodule state. Preserve unrelated work.
2. Require a clean local default branch, fetch its remote, and fast-forward it.
   If it cannot be synchronized safely, stop and record the exact conflict.
3. Fetch the `seo-skills` submodule remote. If an allowed newer commit exists,
   update the submodule pointer in the same daily commit.
4. Implement one coherent scope and update today's daily report and current
   status.
5. Run the smallest authoritative local validations.
6. Read the complete intended diff and review scope, correctness, private-data
   leakage, generated artifacts, tests, and submodule compatibility.
7. Configure the repository-local anonymous author from `site.md`. Verify the
   effective name and email with their config origins immediately before commit.
8. Stage explicit paths, inspect the staged diff, and commit on the default
   branch. Fetch once more; if the remote advanced, rebase only this automation
   commit, rerun validation and review, then push normally. Never force-push.
9. Capture the pushed commit and wait for every expected CI check associated
   with that exact commit. Missing, queued, skipped, cancelled, timed-out, or
   failed checks are not success.
10. If CI fails, diagnose and push a narrow corrective commit. Wait for CI on
    the new exact commit. Do not amend already-pushed history.

## Site deployment

For a site change, locate the production deployment triggered by the exact
pushed commit. Use the provider and production workflow/environment documented
in `site.md` plus live repository configuration.

Wait for a successful terminal production deployment. A CI start, workflow URL,
provider preview, or HTTP 200 is not enough. Verify the changed page or behavior
on the configured public URL, including relevant visible rendering, metadata,
links, or performance output.

If deployment fails, diagnose and push a corrective commit using this same
validation, review, push, CI, and deployment lifecycle. If no safe automated
path remains, update `block.md` with the exact evidence and minimal human-only
action in a direct anonymous commit.

## Closeout commit

CI, merge-equivalent delivery, and deployment facts become known after the main
commit, so push one metadata-only closeout commit. Update the same day's report
and `status.md` with:

- main commit and CI run/check URLs;
- final local review and CI outcome;
- production deployment provider, URL, commit, and conclusion;
- public verification URL, time, and observed result;
- any corrective commits or unresolved blockers.

The closeout commit may change only the day's report, `status.md`, and a resolved
`block.md` item. Validate and self-review it, push it with the same anonymous
identity, and wait for its exact-commit CI. It does not need a deployment wait
unless it changes rendered or deployed output.

## Prohibited shortcuts

- opening a pull request for automated work;
- force-push, reset, or stash of unrelated work;
- amending or rewriting already-pushed shared history;
- treating missing, queued, skipped, failed, or cancelled CI as success;
- exposing a personal Git author identity or fabricating evidence;
- treating a local commit, issue, workflow URL, or HTTP status alone as delivery.
