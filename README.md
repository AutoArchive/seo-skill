# SEO Skills

Public, reusable agent skills for evidence-backed SEO operations across many
website repositories.

Mount this repository as a pinned Git submodule at `.github/seo-skills` in each
website repository. Site-specific bootstrap evidence, metadata, status, plans,
blockers, and daily records belong to that website at `.github/seo-data`; they
never belong in this shared collection.

## Skills

- [`bootstrap-seo-site`](skills/bootstrap-seo-site/SKILL.md) is the mandatory
  first-run and revalidation gate. It performs a read-only audit of the canonical
  domain, DNS and edge path, production provider project, source repository,
  production branch, build command, output directory, deployment trigger,
  analytics, and end-to-end commit-to-public deployment chain before any site
  behavior may be changed.
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

## Mandatory bootstrap gate

Every site must complete `$bootstrap-seo-site` before daily collection or site
mutation begins. Bootstrap is a read-only takeover audit, not an optimization
run. It must prove the real production chain:

```text
source repository + production branch + exact commit
    -> provider production deployment
    -> canonical public hostname
    -> expected deployed content or immutable marker
```

A generated branch, passing workflow, preview deployment, provider build log,
`CNAME` file, HTTP 200 response, or repository naming convention is not proof by
itself. The agent must inspect the actual provider project and independently
verify the canonical public hostname.

The consuming repository records the result in
`.github/seo-data/bootstrap.md`. Until that file says `Bootstrap status:
complete` and `Production chain verified: yes`, agents must not change content,
SEO behavior, analytics, DNS, build settings, deployment settings, dependencies,
or provider configuration. If evidence is missing or contradictory, stop
mutation and report the exact missing evidence rather than guessing.

Bootstrap becomes stale and normal operation freezes when the canonical domain,
DNS or edge provider, hosting provider, provider project, source repository,
production branch, monorepo root, build command, output directory, deployment
trigger, platform architecture, analytics provider, URL reporting policy, or
public commit correspondence changes or may have changed.

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
- an explicit owner-selected URL reporting mode: `full-url` or `path-only`;
- an explicit analytics payload policy.

Agents must not remove, disable, replace, gate, materially reduce, redact, or
expand existing analytics based on their own preference. Such a change requires
an explicit site-owner instruction recorded in the pull request and daily
report. When `site.md` says `full-url`, the complete browser URL, including the
query string, must be transmitted. When it says `path-only`, the query string
must be omitted.

Bootstrap audits analytics read-only. Repairs begin only after production
ownership is proven and bootstrap is complete.

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
    |-- bootstrap.md            # verified production topology and takeover gate
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
cp .github/seo-skills/templates/seo-data/bootstrap.example.md .github/seo-data/bootstrap.md
cp .github/seo-skills/templates/seo-data/site.example.md .github/seo-data/site.md
cp .github/seo-skills/templates/seo-data/daily-task.example.md .github/seo-data/daily-task.md
cp .github/seo-skills/templates/seo-data/promotion.example.md .github/seo-data/promotion.md
cp .github/seo-skills/templates/seo-data/status.example.md .github/seo-data/status.md
cp .github/seo-skills/templates/seo-data/plan.example.md .github/seo-data/plan.md
cp .github/seo-skills/templates/seo-data/block.example.md .github/seo-data/block.md
```

Do not fill the examples by assumption. Invoke `$bootstrap-seo-site`, inspect the
actual public hostname, repositories, provider project, production branch,
build settings, deployment records, and analytics, then replace example values
with verified public-safe facts. The first pull request is metadata-only and must
not alter rendered site or provider behavior.

Edit only the copied files. Every consuming-repository run checks whether the
submodule has a newer allowed commit; when it does, the same pull request must
include the updated submodule pointer and any required metadata migration.

## Consuming-repository pull-request contract

Configure the schedule in the authorized session-level scheduler, not in the
website repository. Each invocation uses
[`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
or the consuming repository's `.github/seo-data/daily-task.md`.

Before normal operation, the agent must:

1. invoke `$bootstrap-seo-site` and complete a read-only production topology
   audit;
2. create a metadata-only bootstrap pull request containing the pinned submodule,
   `bootstrap.md`, and consistent `.github/seo-data` files;
3. wait for CI, self-review the full diff, squash-merge, and reload the bootstrap
   record from the default branch;
4. begin analytics repair, content, SEO, or deployment changes only after the
   bootstrap gate is complete.

Every later daily run must:

1. confirm bootstrap is still complete and not invalidated;
2. read and enforce `$ensure-site-analytics`, including source, built output,
   production runtime, URL policy, Search Console, infrastructure analytics, and
   provider evidence;
3. create a fresh branch and write or append
   `.github/seo-data/daily/YYYY-MM-DD.md`;
4. include the intended data or site changes and any available submodule update;
5. push the branch and create a real, non-draft pull request;
6. wait until all required and expected CI checks finish successfully;
7. self-review the complete final diff, commits, and check results;
8. fix issues on the same branch and repeat CI and self-review when needed;
9. squash-merge the pull request without human review, then attempt to delete
   its merged head branch when the available repository tool supports safe
   branch deletion;
10. for a site change, wait for the exact squash commit's **actual production
    provider deployment** and verify the canonical public hostname, not a
    generated branch or preview;
11. open a metadata-only closeout pull request with the verified delivery facts,
    then apply the same CI, self-review, and squash-merge rules to that closeout.

Merged head-branch deletion is best-effort repository hygiene, not a completion
criterion. Never force-delete a default, protected, active, or unrelated branch.

The agent is authorized to perform every normal step without requesting human
approval. Use `block.md` only when an external system actually requires a
human-only act or the necessary account permission does not exist.

Do not push automated consuming-repository changes directly to the default
branch. A failed, cancelled, skipped, queued, or missing expected check blocks
merge. If the actual production deployment cannot be identified or the canonical
public hostname cannot be matched to the exact source commit, the operation is
not complete.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay
in Google Drive or the analytics provider. Public browser measurement IDs may
remain in runtime source because clients must receive them. Never commit
credentials, OAuth material, personal emails, private account/property/zone/Drive
IDs, IP addresses, user-level analytics rows, raw provider exports, cookies,
authorization values, private dashboard URLs, or full API responses.

Public-safe deployment metadata may include provider type, public project or
service name, source repository and branch, build command, output directory,
public custom domain, public workflow or deployment URL, exact source commit,
and verification result. Daily Markdown may contain aggregated metrics, public
URLs, source status, date windows, export filenames, checksums, decisions,
changed files, PR/CI/deployment URLs, and verification results.

## License

MIT
