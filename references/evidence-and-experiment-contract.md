# SEO evidence and experiment contract

Use this contract whenever a skill creates a finding, selects work, or evaluates
a deployed SEO change. The purpose is to keep observations, decisions, and
claims reproducible across sites and scheduled runs.

## Evidence classes

Every material claim must name one evidence class:

- `direct`: observed in repository source, generated output, an HTTP response,
  rendered production output, or a provider response for the exact target;
- `provider-aggregate`: aggregate GA4, Search Console, Cloudflare, CrUX, or other
  provider data with an identified window and finalization state;
- `derived`: a deterministic calculation whose source rows, parameters, and
  method are known;
- `competitive`: current public search-result or competitor-page evidence with
  collection time and locale when relevant;
- `hypothesis`: an unverified explanation or expected effect that requires a
  test.

Do not promote competitive evidence, a heuristic, or a hypothesis to a direct
fact. Missing evidence is `unknown`, not zero and not a pass.

## Finding record

A finding must contain:

- stable finding ID;
- category and affected public resource;
- severity: `critical`, `high`, `medium`, `low`, or `info`;
- confidence: `confirmed`, `supported`, or `hypothesis`;
- evidence class, source, window or collection time, and exact observable fact;
- impact stated without promising rankings or traffic;
- concrete fix or next evidence-collection step;
- verification method;
- disposition: `repair`, `experiment`, `monitor`, `unknown`, or `not-applicable`;
- dependencies and automation eligibility.

Use `critical` only for direct, current failures that block indexing, break
canonical production behavior, expose unsafe data, or materially break a primary
user path. A low-confidence item cannot be a critical finding.

## Decision boundary

Classify work before editing:

- `repair`: restores an explicit invariant or fixes a reproducible defect. Safe
  repairs follow the same-cycle technical repair rules.
- `experiment`: changes otherwise valid behavior to improve a search or user
  outcome. It requires a baseline, hypothesis, observation window, and resource
  lock before implementation.
- `monitor`: no change is justified yet; collect another finalized window.
- `unknown`: evidence is insufficient or contradictory. State what observation
  would resolve it.
- `not-applicable`: the check does not apply to this site or page type.

Do not label a speculative title, content, schema, internal-link, or performance
change as a repair merely to bypass experiment controls.

## Experiment record

Every speculative change must have a durable record with:

- experiment ID and status;
- finding or opportunity that motivated it;
- hypothesis;
- one primary target metric and source;
- optional guardrail metrics;
- finalized baseline window and values;
- expected direction and a practically meaningful threshold;
- affected URL, template, query cluster, or other resource lock;
- implementation pull request and deployed commit;
- start time, finalization lag, minimum observation window, and earliest review
  date;
- rollback condition and method;
- known confounders;
- outcome: `won`, `lost`, `inconclusive`, or `aborted`, with the evaluation
  window and evidence.

A numeric threshold is not a guarantee. It defines what result would justify
keeping the change.

## Observation and resource locks

By default, only one speculative experiment may be active for a site. A site may
declare a different limit in `site.md`, but every active experiment still locks
its affected resources.

While an experiment is active or observing:

- do not make another speculative change to a locked URL, template, query
  cluster, navigation path, or measurement implementation;
- do not evaluate before the finalization lag and minimum observation window
  have elapsed;
- compare equivalent finalized windows and preserve metric semantics;
- treat an unchanged daily run as a valid result;
- record unrelated incidents, seasonality, releases, outages, and measurement
  changes as possible confounders.

A confirmed technical defect may override a lock. When it overlaps an active
experiment, repair the defect and mark the experiment `aborted` or
`inconclusive` rather than claiming a clean result.

## Comparison rules

- Never compare a partial period with a finalized period as equivalent.
- Do not mix Search Console clicks, GA4 sessions, and Cloudflare visits into one
  synthetic traffic number.
- Keep device, country, search type, and page/query dimensions stable when they
  materially affect the conclusion.
- Record schema drift, truncation, thresholding, sampling, missing rows, and API
  row limits.
- Use deterministic calculations for opportunity lists and changes; an agent may
  interpret the output but must not silently alter source values.

## Public-data boundary

Raw query rows, user-level analytics, IP addresses, cookies, credentials,
private account/property/zone/Drive identifiers, and full provider responses
remain outside Git. Public Markdown may contain source status, aggregate metrics,
public URLs, finding IDs, experiment definitions, decisions, pull requests,
commits, deployment evidence, and reviewed public-safe derived values.

When a detailed local analysis contains search queries, keep it ephemeral. Use a
public-safe mode that replaces query text with opaque keyed identifiers before
committing any derived artifact. A key used to make identifiers stable across
runs must be high entropy, supplied by the invoking environment, and never
committed.
