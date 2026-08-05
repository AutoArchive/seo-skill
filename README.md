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
  evidence-backed site improvement through a real pull request, waits for CI,
  self-reviews the final diff, squash-merges it, and waits for deployment and
  live verification.

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

Use [`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md)
with an authorized agent scheduler, or make the scheduler invoke the consuming
repository's `.github/seo-data/daily-task.md`. Every daily run in a consuming
website repository must:

1. create a fresh branch and write or append
   `.github/seo-data/daily/YYYY-MM-DD.md`;
2. include the intended data or site changes and any available submodule update;
3. push the branch and create a real, non-draft pull request;
4. wait until all required and expected CI checks finish successfully;
5. self-review the complete final diff, commits, and check results;
6. fix issues on the same branch and repeat CI and self-review when needed;
7. squash-merge the pull request and delete its branch without human review;
8. for a site change, wait for the exact squash commit's production deployment
   and verify the public result;
9. open a metadata-only closeout pull request with the verified delivery facts,
   then apply the same CI, self-review, and squash-merge rules to that closeout.

The agent is authorized to perform every normal step without requesting human
approval. Use `block.md` only when an external system actually requires a
human-only act or the necessary account permission does not exist.

Do not push automated consuming-repository changes directly to the default
branch. A failed, cancelled, skipped, queued, or missing expected check blocks
merge. If a site-change deployment cannot be identified or fails, the operation
is not complete.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay
in Google Drive or the analytics provider. Never commit credentials, OAuth
material, personal emails, account/zone/Drive IDs, IP addresses, user-level
analytics, raw query rows, private URLs, or full API responses. Daily Markdown
may contain aggregated metrics, public URLs, source status, date windows, export
filenames, checksums, decisions, changed files, PR/CI/deployment URLs, and
verification results.

## License

MIT
