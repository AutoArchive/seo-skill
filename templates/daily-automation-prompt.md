# Daily SEO automation prompt

Use `$collect-seo-data` from
`.github/seo-skills/skills/collect-seo-data/SKILL.md` for the single site defined
in `.github/seo-data/site.md`. When a justified site improvement is in scope,
also use `$change-seo-site` from
`.github/seo-skills/skills/change-seo-site/SKILL.md`.

Treat `.github/seo-data/daily-task.md` as the site-specific execution entrypoint.
Synchronize a clean local default branch with its remote. Check the
`seo-skills` submodule remote and include an available allowed update in the same
daily commit. Collect read-only Google Drive and Cloudflare evidence, then write
or append `.github/seo-data/daily/YYYY-MM-DD.md`. Maintain `status.md`, `plan.md`,
and `block.md` according to their roles. Keep raw data and private identifiers
outside Git.

Implement at most one coherent site improvement per main commit. Run the
smallest relevant validation and self-review the complete intended diff.
Configure and verify the anonymous repository-local Git identity from `site.md`,
commit directly on the default branch, fetch once more, safely rebase only the
automation's own commit if necessary, and push normally. Never open a pull
request or force-push.

Wait for every required and expected CI check associated with the exact pushed
commit. If a check fails, diagnose and push a corrective commit, then wait for
the new exact commit's CI. For a site change, identify the production deployment
for that exact commit, wait for success, and verify the changed behavior on the
configured public URL. CI success or HTTP 200 alone is not proof of deployment.

After CI and deployment verification, push a metadata-only anonymous closeout
commit that updates the same day's report and `status.md` with the real commit,
CI, deployment, and live-verification evidence. Validate and self-review the
closeout diff and wait for its exact-commit CI as well.

No normal step requires human approval. Record a task in `block.md` only if an
external system enforces a human-only action or the required permission is
absent. Never expose credentials, rewrite shared history, or fabricate
completion.
