# Daily SEO automation prompt

This prompt is invoked by an authorized scheduler outside the consuming
repository, preferably a ChatGPT or equivalent session-level scheduled task.
Do not create or modify GitHub Actions, repository cron jobs, webhooks, hosted
agent runners, or model-provider credential configuration to schedule this
work. Use the model access and connected tools supplied by the invoking session;
the consuming repository does not need `OPENAI_API_KEY` or an equivalent secret.
Existing CI and deployment workflows may be observed or used for delivery, but
must not host the SEO agent.

Always use `$ensure-site-analytics` from
`.github/seo-skills/skills/ensure-site-analytics/SKILL.md`. Every canonical
production site must preserve and verify runtime analytics, Search Console, and
infrastructure analytics where available. Missing, removed, disabled, leaking,
or unverified analytics is an actionable technical defect. Do not remove,
materially reduce, redact, or expand analytics based on agent preference; only
an explicit site-owner instruction recorded in the pull request and daily report
may change that requirement.

Use `$collect-seo-data` from
`.github/seo-skills/skills/collect-seo-data/SKILL.md` for the single site defined
in `.github/seo-data/site.md`. When a justified site improvement is in scope,
also use `$change-seo-site` from
`.github/seo-skills/skills/change-seo-site/SKILL.md`.

Treat `.github/seo-data/daily-task.md` as the site-specific execution entrypoint.
Create a fresh branch from the current remote default branch using the prefix in
`site.md`. Check the `seo-skills` submodule remote and include an available
allowed update in the same branch. Collect configured read-only evidence, then
write or append `.github/seo-data/daily/YYYY-MM-DD.md`. Maintain `status.md`,
`plan.md`, and `block.md` according to their roles. Keep raw provider data and
private credentials outside Git.

## Mandatory analytics audit

During every run, inspect the analytics contract in `site.md`, source code,
generated output, canonical production URL, and provider evidence. Confirm that:

- the named runtime provider is implemented and deployed;
- public page views are intentionally collected;
- URL reporting exactly matches `URL reporting: full-url` or `path-only`;
- `full-url` includes the complete browser query string without agent redaction;
- `path-only` omits the query string;
- no extra custom events containing credentials, cookies, authorization values,
  local files, or application storage have been introduced without explicit
  owner authorization;
- Search Console and infrastructure analytics states are accurate;
- missing or stale provider evidence is labelled missing or stale rather than
  converted to zero.

If runtime analytics is absent, broken, or contradicts the URL policy, repair it
during the same operating cycle through a focused pull request, exact deployment
verification, public runtime verification, and closeout. A Drive export or script
tag alone is not sufficient proof.

## Same-cycle technical repair requirement

Technical defects take priority over routine SEO experiments, source discovery,
content production, reporting, and promotion work. When the run discovers a
reproducible and actionable defect in build, CI, deployment, data generation,
runtime behavior, analytics, crawlability, indexability, accessibility,
performance, broken links, redirects, canonical signals, metadata, structured
data, robots.txt, sitemap output, server rendering, or primary user flows,
repair it during the same scheduled operating cycle and local calendar day
whenever a safe technical path exists.

Do not intentionally defer an actionable defect to a future daily run merely
because another improvement was planned or because one pull request already
exists. The one-coherent-change limit applies per main pull request, not per day.
Use additional focused pull requests when independent repairs cannot be reviewed
coherently together. A production regression or failed deployment preempts
routine work and must be diagnosed, repaired or safely rolled back, deployed,
and verified before the cycle is closed.

If the defect cannot be completed because an external system enforces a
human-only action, permission is absent, or no safe rollback path exists, record
the exact evidence, mitigation attempted, and required external action in
`block.md` through the normal pull-request lifecycle. Provider queues that run
past local midnight do not turn the repair into planned backlog; continue the
same operation until it reaches a truthful terminal outcome.

Implement one coherent outcome per main pull request. Run the smallest relevant
local validation, inspect the intended diff, push the branch, and create a real
non-draft pull request. Never substitute a direct default-branch push, issue,
draft PR, or local commit. Multiple focused pull requests may be completed in the
same daily cycle when required by the same-cycle technical repair rule.

Wait for every required and expected existing CI check. Then self-review the
complete final diff, commits, generated output, analytics behavior, URL policy,
and check results. Fix every issue on the same branch and repeat CI and the
complete review. After green CI and a clean final review, squash-merge the pull
request. Attempt to delete the merged head branch only when the available
repository tool supports safe branch deletion. No human or second reviewer is
required.

Merged head-branch deletion is best-effort cleanup, not a completion criterion.
Do not create a `block.md` item, require human action, delay closeout, or mark the
cycle incomplete merely because the connector cannot delete branches or a
merged automation branch remains. Never force-delete a default, protected,
active, or unrelated branch.

For a site change, identify the production deployment triggered by the exact
squash commit, wait for success, and verify the changed behavior on the public
URL. When analytics may be affected, verify the expected production loader,
configuration, owner-selected full-URL or path-only behavior, and provider
evidence state. A passing PR check or HTTP 200 alone is not proof of deployment.

After deployment verification, create a metadata-only closeout branch and
non-draft pull request. Update the same day's report and `status.md` with the
real PR, squash commit, CI, deployment, analytics verification, URL policy, and
live-verification evidence. Wait for CI, self-review, and squash-merge the
closeout pull request as well.

No normal step requires human approval. Record a task in `block.md` only if an
external system enforces a human-only action or the required permission is
absent. Never force-push, bypass checks, expose credentials, contradict the
owner-selected URL policy, or fabricate completion.
