# Daily SEO automation prompt

Use `$collect-seo-data` from
`.github/seo-skills/skills/collect-seo-data/SKILL.md` for the single site defined
in `.github/seo-data/site.md`. When a justified site improvement is in scope,
also use `$change-seo-site` from
`.github/seo-skills/skills/change-seo-site/SKILL.md`.

Treat `.github/seo-data/daily-task.md` as the site-specific execution entrypoint.
Create a fresh branch from the current remote default branch using the prefix in
`site.md`. Check the `seo-skills` submodule remote and include an available
allowed update in the same branch. Collect read-only Google Drive and Cloudflare
evidence, then write or append `.github/seo-data/daily/YYYY-MM-DD.md`. Maintain
`status.md`, `plan.md`, and `block.md` according to their roles. Keep raw data
and private identifiers outside Git.

Implement at most one coherent site improvement per main pull request. Run the
smallest relevant local validation, inspect the intended diff, push the branch,
and create a real non-draft pull request. Never substitute a direct default-
branch push, issue, draft PR, or local commit.

Wait for every required and expected CI check. Then self-review the complete
final diff, commits, generated output, and check results. Fix every issue on the
same branch and repeat CI and the complete review. After green CI and a clean
final review, squash-merge the pull request and delete the branch. No human or
second reviewer is required.

For a site change, identify the production deployment triggered by the exact
squash commit, wait for success, and verify the changed behavior on the public
URL. A passing PR check or HTTP 200 alone is not proof of deployment.

After deployment verification, create a metadata-only closeout branch and
non-draft pull request. Update the same day's report and `status.md` with the
real PR, squash commit, CI, deployment, and live-verification evidence. Wait for
CI, self-review, and squash-merge the closeout pull request as well.

No normal step requires human approval. Record a task in `block.md` only if an
external system enforces a human-only action or the required permission is
absent. Never force-push, bypass checks, expose credentials, or fabricate
completion.
