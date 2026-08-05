# SEO Skills

Public, reusable agent skills for evidence-backed SEO operations across many
website repositories.

Mount this repository as a pinned Git submodule at `.github/seo-skills` in each
website repository. Site-specific metadata, status, plans, blockers, and daily
records remain in that website's existing `.github/seo-data` layout.

## Skills

- [`bootstrap-seo-site`](skills/bootstrap-seo-site/SKILL.md) is the mandatory
  first-run and revalidation gate. It performs a read-only audit of the canonical
  domain, DNS and edge path, actual production provider project, source
  repository, production branch, build command, output directory, deployment
  trigger, analytics, and end-to-end commit-to-public deployment chain before
  any site behavior may be changed.
- [`ensure-site-analytics`](skills/ensure-site-analytics/SKILL.md) requires every
  canonical production site to preserve, verify, and repair runtime analytics,
  Search Console coverage, infrastructure analytics where available, and the
  site-owner-selected URL and payload policy.
- [`collect-seo-data`](skills/collect-seo-data/SKILL.md) reads configured analytics
  evidence and writes a public-safe daily Markdown record.
- [`change-seo-site`](skills/change-seo-site/SKILL.md) implements and verifies an
  evidence-backed site change through the actual production delivery path.

## Mandatory bootstrap gate

Every site must complete `$bootstrap-seo-site` before daily collection or site
mutation begins. Bootstrap is a read-only takeover audit, not an optimization
run. It must prove:

```text
source repository + production branch + exact commit
    -> provider production deployment
    -> canonical public hostname
    -> expected deployed content or immutable marker
```

A generated branch, passing workflow, preview deployment, provider build log,
`CNAME`, HTTP 200 response, or repository naming convention is not proof by
itself. The agent must inspect the actual provider project and independently
verify the canonical hostname.

Bootstrap does **not** add a new `.github/seo-data` file or change the consumer
layout. Durable bootstrap state is recorded in the existing `site.md` under
`## Deployment`; the current summary goes in `status.md`; detailed evidence and
rejected candidate paths go in the applicable daily report.

Until `site.md` records a completed, current production map, agents must not
change content, SEO behavior, analytics, DNS, build settings, deployment
settings, dependencies, or provider configuration. Missing or contradictory
evidence blocks mutation; do not guess.

Updating the shared submodule is backward-compatible by default. After a site
completes bootstrap, its existing CI opts into the strict gate with:

```bash
python .github/seo-skills/scripts/validate_seo_data.py \
  --data-root .github/seo-data \
  --require-bootstrap
```

This validates the bootstrap fields inside the existing `site.md` without adding
or renaming SEO-data files.

Bootstrap becomes stale when the canonical domain, DNS or edge provider, hosting
provider, provider project, source repository, production branch, monorepo root,
build command, output directory, deployment trigger, platform architecture,
analytics provider, URL policy, or public commit correspondence changes or may
have changed.

## Mandatory analytics baseline

Every canonical production site must maintain runtime web analytics, Search
Console coverage, infrastructure analytics when available, an owner-selected
`full-url` or `path-only` reporting mode, and an explicit payload policy.

Agents must not remove, disable, replace, gate, materially reduce, redact, or
expand analytics based on their own preference. Bootstrap audits analytics
read-only. Repairs begin only after production ownership is proven.

## Scheduler boundary

The scheduler lives outside every consuming repository, preferably as an
authorized session-level task. Do not add a repository cron job, webhook, hosted
agent runner, or model-provider credential solely to execute these skills.
Existing CI and deployment workflows may be observed or used for delivery, but
they do not host the SEO agent.

## Consumer layout

The layout remains unchanged:

```text
.github/
|-- seo-skills/                 # this repository as a pinned submodule
`-- seo-data/
    |-- site.md                 # identity, analytics, verified production topology
    |-- daily-task.md           # site-specific autonomous daily entrypoint
    |-- promotion.md            # durable public promotion strategy and channels
    |-- status.md               # current verified operating state
    |-- plan.md                 # future work and durable public strategy
    |-- block.md                # only genuinely human-only blockers
    `-- daily/YYYY-MM-DD.md     # detailed record for each local calendar day
```

Add the collection and copy the existing starter files:

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

Do not fill examples by assumption. Invoke `$bootstrap-seo-site`, inspect the
actual public hostname, repositories, provider project, production branch,
build settings, deployment records, and analytics, then replace examples with
verified public-safe facts in the existing files. The first pull request is
metadata-only and must not alter rendered site or provider behavior.

## Consuming-repository contract

Before normal operation:

1. invoke `$bootstrap-seo-site` and complete the read-only production audit;
2. update only existing `.github/seo-data` files, the pinned submodule, and the
   validator invocation;
3. create a metadata-only non-draft pull request;
4. wait for CI, self-review, squash-merge, and reload `site.md` from the default
   branch;
5. begin analytics repair, content, SEO, or deployment changes only after the
   strict bootstrap validation passes.

Every later run must confirm bootstrap remains current, use real pull requests,
wait for all expected CI, self-review the final diff, squash-merge, locate the
exact commit in the actual provider project recorded in `site.md`, and verify the
canonical public hostname. Generated branches and previews are not production
unless the bootstrap evidence proves otherwise.

## Public-data boundary

Assume this repository and consumers are public. Never commit credentials,
OAuth material, personal emails, private account/property/zone/Drive IDs, IP
addresses, user-level analytics rows, raw exports, cookies, authorization
values, private dashboard URLs, or full API responses.

Public-safe deployment metadata may include provider type, public project or
service name, source repository and branch, build command, output directory,
public custom domain, exact source commit, public deployment reference, and
verification result.

## License

MIT
