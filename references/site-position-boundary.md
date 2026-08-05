# Site and editorial-position boundary

Shared skills must keep technical production facts separate from site-specific editorial identity when the consuming repository supports that separation.

## `site.md`: technical source of truth

Use the consuming repository's existing `site.md` for durable operational facts such as:

- canonical domain, languages, and timezone;
- source repository, default branch, submodules, and merge policy;
- production provider, project or service, production branch, build command,
  output directory, deployment trigger, and verification method;
- analytics providers, URL reporting policy, evidence routes, and public-data
  boundaries;
- DNS, edge, cache, runtime, security, and rollback facts when the site records
  them there.

Content, research, branding, or tone decisions must not silently redefine these technical facts.

## `position.md`: optional site-owned editorial contract

A consuming repository may use an existing `position.md` for durable editorial and product identity, including:

- mission and intended public value;
- target readers and user needs;
- content or research programs;
- editorial scope, exclusions, and sensitive-topic boundaries;
- article form, citation expectations, language, tone, and style;
- product positioning and the relationship among content types.

`position.md` is site-specific. Its actual topics, audiences, terminology, voice, and policies belong only in the consuming repository. Never hard-code one site's position into this shared submodule.

## Other site-owned files

- `plan.md` normally contains current priorities, sequence, experiments, and backlog.
- `daily-task.md` orchestrates execution and invokes shared skills.
- `status.md`, blocker records, incident records, and daily reports contain current evidence and history.

These roles are recommendations, not a mandatory shared schema.

## Backward compatibility

The shared skill must not require every existing consumer to add `position.md` or reorganize `.github/seo-data`.

- When `position.md` exists, content, research, writing, branding, navigation, and product-positioning work must read and preserve it.
- When it does not exist, read the site's existing editorial plan, repository instructions, content guidelines, or equivalent durable file.
- Create or split out `position.md` only when the site owner or consuming repository explicitly authorizes that change.
- A submodule update alone must never trigger a file migration, rename, heading change, or validator failure.

## Conflict resolution

- Explicit current site-owner instructions take precedence.
- `site.md` governs technical production facts.
- `position.md` or the site's equivalent editorial contract governs editorial identity and writing style.
- `daily-task.md` governs the current execution workflow.
- `plan.md` governs current sequencing rather than permanent identity.

When two site-owned files conflict, stop the affected mutation, report the contradiction, and resolve it through a focused consuming-repository pull request. Do not guess which production provider, editorial policy, or audience is intended.
