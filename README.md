# SEO Skills

Public, reusable agent skills for evidence-backed SEO operations across many
website repositories.

Mount this repository as a pinned Git submodule at `.github/seo-skills` in each
website repository. Site-specific metadata, status, plans, blockers, and daily
records belong to that website at `.github/seo-data`; they never belong in this
shared collection.

## Skills

- [`ensure-site-analytics`](skills/ensure-site-analytics/SKILL.md) requires every
  canonical production site to preserve, verify, and repair runtime analytics,
  Search Console coverage, infrastructure analytics where available, and a
  strict user-data boundary.
- [`collect-seo-data`](skills/collect-seo-data/SKILL.md) reads GA4 and Search
  Console CSV exports from Google Drive, obtains Cloudflare traffic evidence
  through Cloudflare MCP or GraphQL, and writes a public-safe daily Markdown
  record.
- [`change-seo-site`](skills/change-seo-site/SKILL.md) implements one
  evidence-backed site improvement through a real pull request, waits for CI,
  self-reviews the final diff, squash-merges it, and waits for deployment and
  live verification.

## Mandatory analytics baseline

Every canonical production site managed by these skills must have analytics.
The site chooses its approved provider, but an absent, silently disabled, or
unverified runtime analytics implementation is a technical defect, not a normal
privacy mode.

At minimum each site must maintain:

- one runtime web analytics provider for public page views, using GA4 by default
  when an existing GA4 measurement configuration is available;
- Google Search Console coverage;
- infrastructure traffic analytics such as Cloudflare when the production
  provider exposes it;
- a documented privacy boundary that excludes user content, credentials,
  imported filenames, book titles, reading text and progress, private source
  URLs, cookies, authorization values, and sensitive query parameters.

Agents must not remove, disable, replace, gate, or materially reduce existing
analytics based on their own preference. Such a change requires an explicit
site-owner instruction recorded in the pull request and daily report. Address
privacy by minimizing payloads and stripping sensitive values, not by silently
removing measurement.

The consuming repository's `.github/seo-data/site.md` must include the required
`## Analytics` contract. The shared validator rejects sites that omit it, mark
runtime analytics as optional, or fail to name a primary provider.

## Scheduler boundary

The scheduler lives outside every consuming repository. The preferred setup is
an authorized ChatGPT or other session-level scheduled task that opens the
repository through connected tools and invokes
[`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
or the consuming repository's `.github/seo-data/daily-task.md`.

Do not add a GitHub Actions workflow, repository cron job, webhook runner,
hosted bot, provider SDK, or model-runner configuration solely to execute these
skills. A consuming repository must not require `OPENAI_API_KEY` or another
model-provider credential for SEO scheduling. The invoking session owns its
model access and connected-tool credentials outside Git.

Existing repository CI and deployment workflows remain valid. The session-level
scheduler may observe, wait for, or invoke an existing delivery workflow when
that repository already uses it, but those workflows must not host the SEO
agent itself.

## Consumer layout

```text
.github/
|-- seo-skills/                 # this repository as a pinned submodule
`-- seo-data/
    |-- site.md                 # durable public metadata and tool routing
    |-- daily-task.md           # site-specific autonomous daily entrypoint
    |-- promotion.md            # durable public promotion strategy and channels
    |-- status.md               # current verified operating state
    |-- plan.md                 # future work and durable public strategy
    |-- block.md                # only genuinely human-only blockers
    `-- daily/YYYY-MM-DD.md     # detailed record for each local calendar day
```

Add the collection and copy the starter files:

```bash
git submodule add https://github.com/AutoArchive/seo-skill.git .github/seo-skills
mkdir -p .github/seo-data/daily
cp .github/seo-skills/templates/seo-data/site.example.md .github/seo-data/site.md
cp .github/seo-skills/templates/seo-data/daily-task.example.md .github/seo-data/daily-task.md
cp .github/seo-skills/templates/seo-data/promotion.example.md .github/seo-data/promotion.md
cp .github/seo-skills/templates/seo-data/status.example.md .github/seo-data/status.md
cp .github/seo-skills/templates/seo-data/plan.example.md .github/seo-data/plan.md
cp .github/seo-skills/templates/seo-data/block.example.md .github/seo-data/block.md
```

Edit only the copied files. Every consuming-repository run checks whether the
submodule has a newer allowed commit; when it does, the same pull request must
include the updated submodule pointer.

## Consuming-repository pull-request contract

Configure the schedule in the authorized session-level scheduler, not in the
website repository. Each invocation uses
[`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
or the consuming repository's `.github/seo-data/daily-task.md`. Every daily run
in a consuming website repository must:

1. read and enforce `$ensure-site-analytics`, including source, built-output,
   production, Search Console, infrastructure analytics, and privacy checks;
2. create a fresh branch and write or append
   `.github/seo-data/daily/YYYY-MM-DD.md`;
3. include the intended data or site changes and any available submodule update;
4. push the branch and create a real, non-draft pull request;
5. wait until all required and expected CI checks finish successfully;
6. self-review the complete final diff, commits, and check results;
7. fix issues on the same branch and repeat CI and self-review when needed;
8. squash-merge the pull request without human review, then attempt to delete
   its merged head branch when the available repository tool supports safe
   branch deletion;
9. for a site change, wait for the exact squash commit's production deployment
   and verify the public result, including expected analytics when affected;
10. open a metadata-only closeout pull request with the verified delivery facts,
    then apply the same CI, self-review, and squash-merge rules to that closeout.

Merged head-branch deletion is best-effort repository hygiene, not a completion
criterion. A connector that does not expose branch deletion, or a harmless
failure to delete an already-merged automation branch, must not create a
`block.md` item, require human action, delay closeout, or make the daily cycle
incomplete. Never force-delete a default, protected, active, or unrelated
branch.

The agent is authorized to perform every normal step without requesting human
approval. Use `block.md` only when an external system actually requires a
human-only act or the necessary account permission does not exist.

Do not push automated consuming-repository changes directly to the default
branch. A failed, cancelled, skipped, queued, or missing expected check blocks
merge. If a site-change deployment cannot be identified or fails, the operation
is not complete.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay
in Google Drive or the analytics provider. Public browser measurement IDs may
remain in runtime source because clients must receive them. Never commit
credentials, OAuth material, personal emails, private account/property/zone/Drive
IDs, IP addresses, user-level analytics, raw query rows, private URLs, cookies,
authorization values, or full API responses. Daily Markdown may contain
aggregated metrics, public URLs, source status, date windows, export filenames,
checksums, decisions, changed files, PR/CI/deployment URLs, and verification
results.

## License

MIT
