# SEO Skills

Public, reusable agent skills for evidence-backed SEO operations across many
website repositories.

Mount this repository as a pinned Git submodule at `.github/seo-skills` in each
website repository. Site-specific metadata, status, plans, blockers, and daily
records belong to that website at `.github/seo-data`; they never belong in this
shared collection.

## Skills

- [`operate-seo-site`](skills/operate-seo-site/SKILL.md) is the common entrypoint
  for one complete site operating cycle. It reads the repository-specific daily
  task, reviews the pinned skills, verifies analytics, collects evidence,
  prioritizes same-cycle technical repair, invokes optional content work, and
  carries every change through truthful delivery and closeout.
- [`deliver-github-pr`](skills/deliver-github-pr/SKILL.md) owns the reusable
  delivery lifecycle for main, corrective, and closeout changes: focused
  implementation, fresh branch, real non-draft pull request, complete CI, a
  from-scratch final review after CI, squash merge, applicable production
  deployment, public acceptance, and closeout.
- [`configure-google-seo-export`](skills/configure-google-seo-export/SKILL.md)
  configures Google-managed weekly GA4 and Search Console CSV exports into one
  Drive folder per site, including an idempotent immediate backfill and a
  Google Apps Script installable trigger that does not depend on an agent,
  browser, or personal computer staying online.
- [`ensure-site-analytics`](skills/ensure-site-analytics/SKILL.md) requires every
  canonical production site to preserve, verify, and repair runtime analytics,
  Search Console coverage, infrastructure analytics where available, and the
  site-owner-selected URL and payload policy.
- [`collect-seo-data`](skills/collect-seo-data/SKILL.md) reads GA4 and Search
  Console CSV exports from Google Drive, obtains Cloudflare traffic evidence
  through Cloudflare MCP or GraphQL, and writes a public-safe daily Markdown
  record.
- [`research-blog`](skills/research-blog/SKILL.md) owns one complete long-form
  research publication: multi-round public-web and Sider Scholar research,
  multilingual evidence collection, a clear thesis and reader use, rich developed
  prose, citations, counterevidence, limitations, original synthesis, pull-request
  delivery, production deployment, and public verification.

## Skill boundaries

- `$operate-seo-site` decides what the current operating cycle should do and in
  which order.
- `$research-blog` owns research, writing, article review, and publication quality.
- `$deliver-github-pr` owns how every repository change is implemented and
  carried through PR, CI, final review, merge, applicable production deployment,
  public acceptance, and closeout.

Search-facing incremental-change and blast-radius rules are a conditional
reference inside `$deliver-github-pr`, not a second delivery skill.

## Research publication boundary

The shared skill defines the reusable research and writing method. Topic programs,
local editorial identity, and site-specific acceptance checks belong to each
consuming site's existing editorial files.

Long-form research publication should invoke the skills in this order:

```text
site editorial plan
→ $research-blog
→ $deliver-github-pr
```

The public product is a coherent article. Search logs, claim matrices, source
notes, JSON, and metadata are supporting infrastructure and do not replace the
article.

A normal research article uses multiple rounds of public-web Deep Research and
Sider Scholar, searches every materially relevant language, and includes Japanese
research when Japanese concepts are involved. The normal source floor is 40
substantive sources: at least 20 academic sources and at least 20 primary,
community, archival, institutional, specialist-blog, creator, or platform
sources. Chinese main text is at least 5,000 characters unless the consuming site
sets a higher floor.

The article keeps one clear thesis and one explicit reader use from opening to
conclusion. It matches or exceeds the consuming site's strongest long-form work in
content richness, paragraph development, flow, and depth. Author-written prose is
collaborative, affirmative, and free of defensive constructions while preserving
all evidence, counterarguments, limitations, qualifications, and original
synthesis.

## Consumer repository configuration

The files under `.github/seo-data` are maintained by each consuming repository.
The templates in this repository are starting points, not a schema enforced by
this repository.

A difference from the shared examples alone does not require a migration. When a
current skill explicitly introduces new information or an operating artifact,
the consuming repository may add the minimum fields, files, or workflow changes
needed to follow that requirement. The consuming repository may choose the most
suitable filenames, headings, section order, and prose unless the current skill
explicitly defines an interface.

This repository does not ship a validator or CI check for the structure of a
consuming repository's `.github/seo-data` directory.

The repository's own [validation workflow](.github/workflows/validate.yml) has a
narrow boundary: it compiles this repository's scripts and checks shared skill
frontmatter and local Markdown links. It provides minimum pull-request CI for the
shared package and never inspects or enforces a consuming site's files.

## Mandatory analytics baseline

Every canonical production site managed by these skills must have analytics.
The site chooses its approved provider, but an absent, silently disabled, or
unverified runtime analytics implementation is a technical defect, not a normal
privacy mode.

Each site must make the operating answer discoverable in its notes: which runtime
provider is expected, where it is implemented, how production is checked, whether
query strings are included, where search evidence arrives, and which data must
never be collected. A paragraph, list, table, or repository instruction is equally
valid; exact labels are not required.

Infrastructure analytics such as Cloudflare should also be documented whenever
the production provider exposes it. Agents must not remove, disable, replace,
gate, materially reduce, redact, or expand existing analytics based on their own
preference. Such a change requires an explicit site-owner instruction recorded in
the pull request and daily report.

When the site chooses full-URL reporting, transmit the complete browser URL,
including the query string. When it chooses path-only reporting, omit the query
string. Verify the implemented behavior directly.

## Scheduler boundary

The scheduler lives outside every consuming repository. The preferred setup is
an authorized ChatGPT or other session-level scheduled task that opens the
repository through connected tools and invokes
[`operate-seo-site`](skills/operate-seo-site/SKILL.md). The reusable launcher is
[`templates/daily-automation-prompt.md`](templates/daily-automation-prompt.md),
while the consuming repository's `.github/seo-data/daily-task.md` contains only
site-specific priorities, exclusions, rotations, and acceptance checks.

Do not add a GitHub Actions workflow, repository cron job, webhook runner, hosted
bot, provider SDK, or model-runner configuration solely to execute these skills. A
consuming repository must not require `OPENAI_API_KEY` or another model-provider
credential for SEO scheduling. Existing CI and deployment workflows remain valid
and may be observed or used for delivery.

### Google export automation is provider-managed

The external session scheduler runs the daily SEO agent. It must not be used to
produce recurring GA4 or Search Console files. Configure those exports with
[`configure-google-seo-export`](skills/configure-google-seo-export/SKILL.md): a
Google Apps Script project owned by the Google account runs the weekly export
inside Google and writes CSV artifacts to Drive. Codex, ChatGPT, Chrome, and the
operator's computer may all be offline when that trigger fires.

Keep site folder IDs, GA4 property IDs, OAuth grants, and other private routing
values only in the private Apps Script project. The shared skill and consuming
repositories contain policy and filenames, not those identifiers.

## Recommended onboarding layout

The following is one reasonable starting point for a new repository:

```text
.github/
|-- seo-skills/                 # this repository as a pinned submodule
`-- seo-data/
    |-- site.md                 # durable public metadata and tool routing
    |-- daily-task.md           # short site-specific operating checklist
    |-- status.md               # current verified operating state
    |-- plan.md                 # future work and durable public strategy
    |-- block.md                # only genuinely human-only blockers
    |-- promotion.md            # optional promotion strategy
    `-- daily/YYYY-MM-DD.md     # consumer-defined daily record
```

For a new site, copy whichever starter files are useful. For an existing site,
apply explicit new skill requirements with the minimum necessary changes; no
change is needed merely because its layout differs from this example.

## Consuming-repository pull-request contract

Configure the schedule in the authorized session-level scheduler, not in the
website repository. Invoke `$operate-seo-site` for each scheduled cycle and use
`$deliver-github-pr` for every main, corrective, and closeout pull request. Every
automated change still requires a fresh branch, real non-draft pull request, all
required and expected CI, a from-scratch final review of the complete PR after
CI, squash merge, and truthful closeout. For rendered site changes,
`$deliver-github-pr` also requires the exact production deployment and public
verification before completion.

Merged head-branch deletion remains best-effort repository hygiene. Never push
automated consuming-repository changes directly to the default branch, bypass
checks, or report a preview as production.

## Public-data boundary

Assume this repository and consuming repositories are public. Raw exports stay in
Google Drive or the analytics provider. Public browser measurement IDs may remain
in runtime source because clients must receive them. Never commit credentials,
OAuth material, personal emails, private account/property/zone/Drive IDs, IP
addresses, user-level analytics rows, raw provider exports, cookies, authorization
values, or full API responses.

## License

MIT
