# Deployment and public verification

## Identify the exact deployment

Read deployment metadata from `.github/seo-data/site.md`, then inspect live
repository configuration. The documented workflow or provider name is a routing
hint, not evidence by itself.

Correlate deployment with the exact squash commit produced by the merged
site-change pull request:

- GitHub Actions or Pages: select the production workflow run whose `head_sha`
  equals the commit and whose event/branch matches the default branch.
- Cloudflare Pages: select the production deployment whose source commit equals
  the commit and whose project/domain matches the site.
- Vercel or another provider: use its authenticated connector or CLI to select
  the production deployment for the same commit and project.

Wait through queued and in-progress states. Success means the provider reports a
successful terminal production deployment for that exact commit. Preview builds
and unrelated newer deployments do not satisfy the requirement.

## Respond to failure

Read failed build/deployment logs, identify the narrow cause, and deliver a
corrective pull request through `$deliver-github-pr`, including complete CI and
a from-scratch final review, before repeating the deployment lifecycle. Do not
retry blindly when inputs have not changed. Do not force-push, amend shared
history, or rewrite another contributor's work.

If the provider requires a permission or human-only account action that the
automation cannot perform, write exact evidence and the minimal required action
to `block.md` through a real pull request. Ordinary deployment and verification
do not require approval.

## Verify the public result

After provider success, verify the production URL from `site.md`. Use a normal
browser for rendered content and an HTTP/client inspection for metadata when
needed. Check the changed behavior, not just availability. Examples:

- exact visible heading or content on the intended route;
- rendered title, meta description, canonical, robots directive, and hreflang;
- JSON-LD presence and validity;
- intended internal link target and status;
- sitemap/robots entry;
- response header or redirect chain;
- relevant performance metric when performance was the change.

An HTTP 200, cached preview, provider dashboard success, or source diff alone is
insufficient. Capture public URL, verification time, observed value, a public-
safe deployment URL/ID, and the exact squash commit in the daily report.

## Closeout scope

The closeout pull request may change only
`.github/seo-data/daily/YYYY-MM-DD.md`, `.github/seo-data/status.md`, and a
resolved `block.md` item. It records facts that became available after the main
pull request merged and must not smuggle in another site change. Wait for its
CI, perform the full `$deliver-github-pr` from-scratch review, and squash-merge
it.
