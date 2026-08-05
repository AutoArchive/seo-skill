# Production deployment and public verification

Read this reference whenever a change can affect production, rendered output,
or another public artifact. The caller supplies the domain-specific acceptance
criteria; this reference owns how deployment and closeout are proven.

## Identify the exact deployment

Read the repository's deployment notes, then inspect live workflow and provider
configuration. Documented names are routing hints, not proof. Correlate the
production deployment with the exact squash commit:

- GitHub Actions or Pages: require the production run's `head_sha`, event, and
  branch to match the squash commit and default branch.
- Cloudflare Pages: require the production deployment's source commit, project,
  and domain to match.
- Vercel or another provider: use its authenticated connector or CLI to select
  the production deployment for the same commit and project.

Wait through queued and in-progress states. Success means a successful terminal
production deployment for that exact commit. A preview or unrelated newer
deployment does not satisfy the requirement.

## Respond to failure

Read build or deployment logs, identify the narrow cause, and use
`$deliver-github-pr` for a corrective pull request with complete CI and a new
from-scratch final review. Do not retry blindly when inputs have not changed.
After the corrective squash merge, monitor the replacement commit.

If a provider requires a permission or genuinely human-only account action that
the agent cannot perform, record exact evidence, mitigation, and the minimal
required action through the repository's normal blocker and pull-request
process. Ordinary deployment waiting and verification require no approval.

## Verify the public result

After provider success, inspect the canonical public target. Use a normal
browser for rendered behavior and an HTTP or client inspection for metadata when
needed. Check the actual requested outcome and representative unaffected
behavior. Depending on scope, this can include visible content, title,
description, canonical, structured data, links, robots and sitemap output,
headers, redirects, runtime analytics, or a performance signal.

An HTTP 200, cached preview, provider dashboard success, source diff, or passing
workflow alone is insufficient. Capture the public URL, verification time,
observed value, public-safe deployment identifier, and exact squash commit.

## Closeout

Record facts that became available after merge in the repository's existing
operating records. Keep the closeout change metadata-only unless a new rendered
fix is genuinely required. Deliver the closeout with `$deliver-github-pr`,
including complete CI and another from-scratch final review. A closeout requires
another deployment wait only when it changes production or rendered output.
