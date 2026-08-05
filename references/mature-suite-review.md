# Mature SEO skill-suite review

Review date: 2026-08-05.

This note records the external designs considered for this repository and the
patterns adopted or intentionally rejected. It is design provenance, not an
endorsement of every SEO claim in the referenced projects.

## Compared suites

### AgriciDaniel/claude-seo

Repository: <https://github.com/AgriciDaniel/claude-seo>

Useful pattern:

- a small routing surface backed by specialized audit, page, technical, content,
  schema, sitemap, performance, GEO, local, backlink, and Google-data modules;
- progressive disclosure through references rather than one unbounded prompt;
- structured audit artifacts and explicit error handling;
- deterministic helper scripts and optional data-provider extensions.

Adopted here:

- separate baseline audit and experiment-planning skills;
- shared evidence contract;
- deterministic helper scripts outside the language-model reasoning path.

Not adopted:

- reproducing a large catalog of overlapping skills before the operating loop is
  validated;
- a universal numeric health score that can hide missing evidence.

### Bhanunamikaze/Agentic-SEO-Skill

Repository: <https://github.com/Bhanunamikaze/Agentic-SEO-Skill>

Useful pattern:

- scripts gather observable page and provider facts;
- findings distinguish evidence, impact, action, severity, and confidence;
- unknown data is not silently converted into a finding;
- cross-agent packaging and explicit regression scenarios.

Adopted here:

- typed finding records;
- confidence labels and an `unknown` disposition;
- standard-library analysis and schema validation in CI.

Not adopted:

- requiring free-form model reasoning logs as a durable artifact;
- precise scores derived from weak or incomplete evidence.

### inhouseseo/superseo-skills

Repository: <https://github.com/inhouseseo/superseo-skills>

Useful pattern:

- a page audit starts with the page's actual purpose and search intent;
- current competitor pages may provide context for format and coverage gaps;
- recommendations name concrete page elements instead of returning a generic
  checklist.

Adopted here:

- optional, time-stamped competitive evidence for intent and content-gap work;
- explicit page type, target outcome, and exact affected resource.

Not adopted:

- treating third-party ranking-factor claims as established facts;
- assuming a competitor comparison replaces first-party Search Console,
  deployment, or live-site evidence.

### nowork-studio/NotFair

Repository: <https://github.com/nowork-studio/NotFair>

Useful pattern:

- establish a mechanically verifiable baseline;
- perform one falsifiable action rather than many confounded edits;
- record expected effect, observation window, and rollback;
- lock affected resources while evidence matures;
- allow a no-op check instead of manufacturing activity;
- keep durable experiment state separate from prompt memory.

Adopted here:

- a durable consumer-owned experiment ledger, with `experiments.md` as the
  recommended new-site filename;
- one active speculative experiment by default;
- URL/template/query-cluster resource locks;
- finalized observation windows and explicit outcomes;
- technical-repair override with experiment-confounder handling.

This is the main operational change in this revision.

### addyosmani/web-quality-skills

Repository: <https://github.com/addyosmani/web-quality-skills>

Useful pattern:

- focused skills for SEO, performance, Core Web Vitals, accessibility, and a
  composed web-quality audit;
- deterministic audit scripts;
- portability across agent hosts.

Adopted here:

- keep technical web-quality checks as observable audit dimensions;
- avoid putting all performance and accessibility knowledge into one SEO prompt;
- retain standard-library tools and host-neutral Markdown contracts.

## Official constraints used

The implementation also follows first-party documentation rather than relying
only on community prompts:

- Search Console Search Analytics API:
  <https://developers.google.com/webmaster-tools/v1/searchanalytics/query>
- Search Console URL Inspection result:
  <https://developers.google.com/webmaster-tools/v1/urlInspection.index/UrlInspectionResult>
- Google Search Essentials:
  <https://developers.google.com/search/docs/essentials>
- Structured data general guidelines:
  <https://developers.google.com/search/docs/appearance/structured-data/sd-policies>

Relevant consequences:

- Search Console exports may omit low-volume rows and recent data may be
  incomplete, so missing rows are not zero;
- current and prior windows must have equivalent dimensions and finalization
  state;
- structured data must represent visible page content and does not guarantee a
  rich result;
- crawlability, useful content, descriptive titles/headings/link text, and
  verifiable production behavior remain the baseline.

## Resulting architecture

The repository keeps its existing strengths—autonomous PR delivery, CI,
self-review, squash merge, exact deployment verification, public verification,
and metadata closeout—and adds the missing decision layer:

```text
collect evidence
      |
      v
deterministic derivation
      |
      v
typed baseline audit
      |
      +--> confirmed defect --> same-cycle repair
      |
      +--> eligible opportunity --> one controlled experiment
      |
      `--> insufficient or immature evidence --> monitor / no-op
```

This avoids two common failure modes: a broad audit that never ships anything,
and an autonomous content bot that continuously changes pages without measuring
whether prior changes worked.
