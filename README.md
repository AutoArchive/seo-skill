# SEO Skills

Public, reusable agent skills for evidence-backed SEO operations across many
website repositories.

Mount this repository as a pinned Git submodule at `.github/seo-skills` in each
website repository. Site-specific metadata, status, plans, blockers, and daily
records belong to that website at `.github/seo-data`; they never belong in this
shared collection.

## Skills

- [`collect-seo-data`](skills/collect-seo-data/SKILL.md) reads GA4 and Search
  Console CSV exports from Google Drive, obtains Cloudflare traffic evidence
  through Cloudflare MCP or GraphQL, and writes a public-safe daily Markdown
  record.
- [`change-seo-site`](skills/change-seo-site/SKILL.md) implements one
  evidence-backed site improvement, pushes an anonymous commit to the default
  branch, waits for CI and production deployment, and verifies the live result.

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

Edit only the copied files. Every automated run checks whether the submodule has
a newer allowed commit; when it does, update the pointer in the same anonymous
direct commit as that day's site or data work.

## Direct delivery contract

Use [`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
with an authorized agent scheduler, or make the scheduler invoke the consuming
repository's `.github/seo-data/daily-task.md`. Every daily run must:

1. synchronize a clean local default branch with its remote;
2. write or append `.github/seo-data/daily/YYYY-MM-DD.md` and make any one
   coherent site change plus an available skill-submodule update;
3. run local validation and self-review the complete intended diff;
4. commit with the anonymous repository-local identity documented in `site.md`
   and push the default branch directly, never through a pull request;
5. wait for every expected CI check for that exact commit to succeed;
6. for a site change, wait for the exact commit's production deployment and
   verify the changed behavior at the public URL;
7. push an anonymous metadata-only closeout commit that records real CI,
   deployment, and live verification in the daily report and `status.md`, then
   wait for the closeout commit's CI.

The agent is authorized to perform every normal step without requesting human
approval. Use `block.md` only when an external system actually requires a
human-only act or the necessary account permission does not exist.

Never force-push, bypass failed CI, rewrite another contributor's work, or claim
completion from a workflow URL or HTTP 200 alone. If the remote default branch
advances, rebase only the automation's own commit, rerun validation and review,
and push normally.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay
in Google Drive or the analytics provider. Never commit credentials, OAuth
material, personal emails, account/zone/Drive IDs, IP addresses, user-level analytics,
raw query rows, private URLs, or full API responses. Daily Markdown may contain
aggregated metrics, public URLs, source status, date windows, export filenames,
checksums, decisions, changed files, commit/CI/deployment URLs, and verification
results.

## License

MIT
