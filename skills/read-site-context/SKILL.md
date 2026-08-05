---
name: read-site-context
description: Resolve a consuming website's technical and editorial sources of truth before research, writing, SEO, product, or deployment work. Use when a repository may separate technical facts in site.md from mission, audience, content programs, and style in an optional position.md, while preserving backward compatibility with existing SEO-data layouts.
---

# Read Site Context

## Purpose

Build a reliable context map before changing or publishing anything. This skill keeps production facts separate from editorial identity while preserving each consuming repository's existing `.github/seo-data` structure.

Invoke it before `$deep-research-blog`, `$write-readable-research-blog`, `$publish-research-blog`, or any `$change-seo-site` operation whose correctness depends on audience, positioning, content scope, writing style, provider, build, analytics, or public acceptance.

Read [`../../references/site-position-boundary.md`](../../references/site-position-boundary.md) completely.

## Context roles

### Technical source of truth

Use the consuming repository's existing `site.md` for durable technical and operational facts, including the canonical domain, repository, production provider, project or service, production branch, build command, output directory, deployment trigger, analytics, URL reporting, evidence routes, public verification, security boundaries, and rollback facts.

Editorial prose must not override technical facts recorded in `site.md`.

### Editorial source of truth

When an existing `position.md` is present, use it for durable site-specific editorial identity:

- mission and intended public value;
- target readers and user needs;
- research or content programs;
- editorial scope and exclusions;
- sensitive-topic boundaries;
- article form, citation expectations, language, tone, and style;
- product or publication positioning.

The actual contents of `position.md` belong only in the consuming repository. Never copy one site's topics, audiences, labels, or style rules into this shared skill repository.

When `position.md` is absent, use the site's existing editorial plan, repository instructions, content guide, product document, or equivalent durable file. Absence alone is not permission to create or require a new file.

### Execution and current state

- `daily-task.md` governs the current operating workflow and skill sequence.
- `plan.md` normally governs current priorities, sequencing, experiments, and backlog.
- `status.md`, blocker records, incident records, and daily reports govern current evidence and history.

These are recommended semantic roles rather than a mandatory filename or heading schema.

## Backward-compatible behavior

- Preserve all existing `.github/seo-data` filenames, headings, titles, section order, and prose unless the site owner or consuming repository explicitly authorizes a change.
- Do not require `position.md` in validators or shared templates.
- Do not create `position.md` merely because the shared skill supports it.
- A submodule update must not make an established consuming repository invalid solely because it has no `position.md`.
- When a site owner explicitly requests a technical/editorial split, implement it through a focused consuming-repository pull request and keep site-specific content outside this submodule.

## Read sequence

1. Read current explicit site-owner instructions and repository-level instructions.
2. Read `site.md` completely and extract the technical production map.
3. Read `position.md` when it exists; otherwise identify the existing editorial equivalent.
4. Read `daily-task.md`, `plan.md`, current status, blockers, incidents, and recent daily records.
5. Compare these sources for contradictions, staleness, and accidental duplication.
6. Produce an internal context map before beginning the requested task.

The context map should identify:

- technical source of truth;
- editorial source of truth;
- current execution contract;
- current priorities;
- production and analytics acceptance rules;
- audience, scope, and style constraints relevant to the task;
- conflicts or missing evidence that affect safe execution.

## Conflict handling

Use this precedence:

1. explicit current site-owner instruction;
2. verified technical facts in `site.md` for production and analytics;
3. `position.md` or the editorial equivalent for mission, audience, content, and style;
4. `daily-task.md` for execution;
5. `plan.md` for current sequencing;
6. status, incidents, and daily records for current evidence.

When two files conflict on a material fact, freeze only the affected mutation. Record the contradiction and resolve it through a focused consuming-repository pull request. Do not guess the production provider, source repository, audience, editorial scope, language policy, or publication standard.

## Task-specific use

### Research and writing

Read the editorial source before selecting a topic, defining scope, choosing terminology, setting article form, or applying a language style. Read `site.md` for the canonical domain, repository delivery, analytics, and deployment acceptance.

### SEO and content changes

Use editorial position to preserve page purpose, audience, tone, sensitive-topic policy, and content boundaries. Use `site.md` to preserve canonical ownership, deployment, analytics, and runtime behavior.

### Technical and deployment changes

Use `site.md` and authenticated provider evidence. Editorial documents cannot establish a production provider or authorize a migration.

## Completion criteria

This context step is complete when:

- the technical and editorial sources of truth are identified;
- optional `position.md` is used when present without being forced when absent;
- site-specific content remains in the consuming repository;
- current task constraints are summarized internally;
- material contradictions are either resolved or truthfully block the affected mutation;
- no shared-schema migration has been introduced.
