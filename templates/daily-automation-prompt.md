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

## Preserve the consuming repository contract

Treat the consuming repository's existing `.github/seo-data` files, headings,
titles, section order, and prose as a stable site-owned interface. A shared skill
or checker update must not cause an incidental schema migration.

Do not rename files or headings, replace daily-report titles, reorder sections,
add `promotion.md`, copy starter templates, or add metadata labels merely to
satisfy the shared submodule. Record missing context only when it helps operate
or verify the site. Templates are examples for new repositories only. Change an
established layout only when the site owner's instructions or the consuming
repository itself explicitly require that change.

Use `$collect-seo-data` from
`.github/seo-skills/skills/collect-seo-data/SKILL.md` for the single site defined
in `.github/seo-data/site.md`. When a justified site improvement is in scope,
also use `$change-seo-site` from
`.github/seo-skills/skills/change-seo-site/SKILL.md`.

When the site's daily task requires a long-form research article, invoke
`$publish-research-blog` from
`.github/seo-skills/skills/publish-research-blog/SKILL.md`. It must invoke
`$deep-research-blog` and `$write-readable-research-blog` completely before
repository delivery. Site-specific research programs and topic rotation belong
in the consuming site's existing editorial plan. The public product is a
coherent article; search logs, source matrices, JSON, and metadata do not replace
it.

Research writing should use clear, positive, direct Chinese prose. During the
style audit, reduce repetitive rhetorical forms such as “不是……而是……”, “并非”,
“不只是”, and “这并不意味着”. Preserve negation when it establishes a precise
evidence boundary or a genuine non-equivalence.

Treat `.github/seo-data/daily-task.md` as the site-specific execution entrypoint.
Create a fresh branch from the current remote default branch using the site's
established branch convention. Check the `seo-skills` submodule remote and
include an available allowed update in the same branch only after reviewing its
complete diff and confirming compatibility with the existing consumer layout.
Collect configured read-only evidence, then update the site's existing daily and
durable status records according to their established roles. Keep raw provider
data and private credentials outside Git.

## Mandatory analytics audit

During every run, inspect the analytics semantics in `site.md`, source code,
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
verification, public runtime verification, and closeout. A provider export or
script tag alone is not sufficient proof. Preserve the site's SEO-data layout
while recording the required evidence.

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
the exact evidence, mitigation attempted, and required external action in the
site's existing blocker record through the normal pull-request lifecycle.
Provider queues that run past local midnight do not turn the repair into planned
backlog; continue the same operation until it reaches a truthful terminal
outcome.

Implement one coherent outcome per main pull request. Run the smallest relevant
local validation, inspect the intended diff, push the branch, and create a real
non-draft pull request. Never substitute a direct default-branch push, issue,
draft PR, or local commit. Multiple focused pull requests may be completed in the
same daily cycle when required by the same-cycle technical repair rule.

Wait for every required and expected existing CI check. Then self-review the
complete final diff, commits, generated output, analytics behavior, URL policy,
consumer-layout preservation, and check results. For research articles, also
review claim-level citations, source quality, counterevidence, original synthesis,
readability, jargon explanations, and excessive rhetorical self-negation. Fix
every issue on the same branch and repeat CI and the complete review. After green
CI and a clean final review, squash-merge the pull request. Attempt to delete the
merged head branch only when the available repository tool supports safe branch
deletion. No human or second reviewer is required.

Merged head-branch deletion is best-effort cleanup, not a completion criterion.
Do not create a blocker, require human action, delay closeout, or mark the cycle
incomplete merely because the connector cannot delete branches or a merged
automation branch remains. Never force-delete a default, protected, active, or
unrelated branch.

For a site change, identify the production deployment triggered by the exact
squash commit, wait for success, and verify the changed behavior on the public
URL. When analytics may be affected, verify the expected production loader,
configuration, owner-selected full-URL or path-only behavior, and provider
evidence state. A passing PR check or HTTP 200 alone is not proof of deployment.

After deployment verification, update the site's existing closeout/daily/status
records through its normal pull-request process. Do not introduce a new closeout
file or document outline unless the consuming repository already requires it.
Wait for CI, self-review, and squash-merge the closeout pull request as well.

No normal step requires human approval. Record a blocker only if an external
system enforces a human-only action or the required permission is absent. Never
force-push, bypass checks, expose credentials, contradict the owner-selected URL
policy, restructure consumer data for shared-template conformity, or fabricate
completion.
