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
  Search Console coverage, infrastructure analytics where available, and the
  site-owner-selected URL and payload policy.
- [`collect-seo-data`](skills/collect-seo-data/SKILL.md) reads GA4 and Search
  Console CSV exports from Google Drive, obtains Cloudflare traffic evidence
  through Cloudflare MCP or GraphQL, and writes a public-safe daily Markdown
  record.
- [`change-seo-site`](skills/change-seo-site/SKILL.md) implements one
  evidence-backed site improvement through a real pull request, waits for CI,
  self-reviews the final diff, squash-merges it, and waits for deployment and
  live verification.

## Consumer-owned data contract

`.github/seo-data` is a stable, consumer-owned interface. The shared skill may
require durable semantic declarations, but it must not rewrite a consuming
repository's document structure merely to match shared examples.

A submodule update must not, solely for compatibility with this repository:

- rename existing SEO-data files or headings;
- reorder existing sections;
- replace a site's established title or daily-report format;
- require `promotion.md` or another optional file that the site did not already
  use;
- copy template prose over site-specific operating instructions.

The validator checks the stable entrypoints `site.md`, `daily-task.md`, the
`daily/` directory, public-data safety, valid daily filenames, and required
analytics declarations. It accepts consumer-specific files, titles, headings,
section order, and prose. Templates are onboarding examples for new sites, not a
migration schema for existing sites.

## Mandatory analytics baseline

Every canonical production site managed by these skills must have analytics.
The site chooses its approved provider, but an absent, silently disabled, or
unverified runtime analytics implementation is a technical defect, not a normal
privacy mode.

At minimum each site's existing `site.md` must declare, anywhere in its current
layout:

- `Runtime analytics required: yes`;
- a named primary runtime provider;
- a public runtime verification URL;
- `URL reporting: full-url` or `URL reporting: path-only`;
- required search analytics;
- an explicit analytics payload policy.

Infrastructure analytics such as Cloudflare should also be documented whenever
the production provider exposes it. Agents must not remove, disable, replace,
gate, materially reduce, redact, or expand existing analytics based on their own
preference. Such a change requires an explicit site-owner instruction recorded
in the pull request and daily report.

When `site.md` says `full-url`, the complete browser URL, including the query
string, must be transmitted. When it says `path-only`, the query string must be
omitted. The shared validator checks these semantic declarations without
requiring an `## Analytics` heading or any other document restructuring.

## Scheduler boundary

The scheduler lives outside every consuming repository. The preferred setup is
an authorized ChatGPT or other session-level scheduled task that opens the
repository through connected tools and invokes
[`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
or the consuming repository's `.github/seo-data/daily-task.md`.

Do not add a GitHub Actions workflow, repository cron job, webhook runner,
hosted bot, provider SDK, or model-runner configuration solely to execute these
skills. A consuming repository must not require `OPENAI_API_KEY` or another
model-provider credential for SEO scheduling. Existing CI and deployment
workflows remain valid and may be observed or used for delivery.

## Recommended onboarding layout

The following is a recommendation for a new repository, not a required layout
for an existing consumer:

```text
.github/
|-- seo-skills/                 # this repository as a pinned submodule
`-- seo-data/
    |-- site.md                 # durable public metadata and tool routing
    |-- daily-task.md           # site-specific autonomous daily entrypoint
    |-- status.md               # current verified operating state
    |-- plan.md                 # future work and durable public strategy
    |-- block.md                # only genuinely human-only blockers
    |-- promotion.md            # optional promotion strategy
    `-- daily/YYYY-MM-DD.md     # consumer-defined daily record
```

For a new site, copy whichever starter files are useful and then edit the copies.
For an existing site, preserve its current layout and add only missing semantic
declarations in the most natural existing location.

## Consuming-repository pull-request contract

Configure the schedule in the authorized session-level scheduler, not in the
website repository. Each daily run must:

1. read and enforce `$ensure-site-analytics`;
2. preserve the consumer-owned `.github/seo-data` layout;
3. create a fresh branch and update the site's existing daily record and durable
   status files as appropriate;
4. include the intended data or site changes and any reviewed submodule update;
5. create a real, non-draft pull request;
6. wait until all required and expected CI checks finish successfully;
7. self-review the complete final diff, commits, generated output, submodule
   movement, and check results;
8. fix issues on the same branch and repeat CI and self-review when needed;
9. squash-merge without human review;
10. verify the exact production deployment and public result;
11. complete any site-required metadata closeout through the same PR discipline.

Merged head-branch deletion is best-effort repository hygiene, not a completion
criterion. Never push automated consuming-repository changes directly to the
default branch, bypass checks, or report a preview as production.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay
in Google Drive or the analytics provider. Public browser measurement IDs may
remain in runtime source because clients must receive them. Never commit
credentials, OAuth material, personal emails, private account/property/zone/Drive
IDs, IP addresses, user-level analytics rows, raw provider exports, cookies,
authorization values, or full API responses.

## License

MIT
