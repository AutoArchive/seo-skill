# Daily SEO task

## Objective

Run one fully autonomous, evidence-backed SEO operating cycle for the site in
`site.md`. No normal step requires human approval or a pull request.

## Schedule

- Frequency: daily
- Timezone: use `site.md`
- Data window: use the lookback and finalization lag in `site.md`
- Maximum site changes: one coherent change per main commit

## Required sequence

1. Read the pinned `$collect-seo-data` skill, `$change-seo-site` when a site
   change is justified, all `.github/seo-data/*.md` files, and newest reports.
2. Require a clean local default branch and fast-forward it to the remote.
3. Check whether the `seo-skills` submodule has an allowed update and include an
   available update in the same anonymous daily commit.
4. Collect finalized Google Drive and Cloudflare evidence without committing
   raw data or private identifiers.
5. Write or append `.github/seo-data/daily/YYYY-MM-DD.md`; refresh `status.md`,
   maintain future work in `plan.md`, and keep `block.md` limited to genuine
   human-only or permission blockers.
6. When evidence supports a site improvement, implement at most one coherent
   change and define its production acceptance check before editing.
7. Validate locally, self-review the complete diff, verify the anonymous Git
   identity from `site.md`, commit directly on the default branch, and push
   normally. Never open a pull request or force-push.
8. Wait for all required and expected CI associated with the exact commit. Push
   a corrective commit and repeat when a check fails.
9. For a site change, wait for the exact commit to deploy successfully and
   verify the changed behavior on the public site.
10. Push a metadata-only anonymous closeout commit with final evidence; validate
    and review it, then wait for its exact-commit CI.
11. Continue autonomously while safe progress is possible. Record a `block.md`
    item only when an external system enforces a human-only action or required
    permission is absent.

## Daily completion

A day is complete only after the anonymous main commit and closeout commit are
pushed and their exact-commit CI succeeds. A site-change day also requires a
successful production deployment for the exact main commit and public
verification. A failed or missing CI check, failed deployment, local-only
commit, issue, workflow URL, or HTTP 200 alone is not completion.
