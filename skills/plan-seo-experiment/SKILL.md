---
name: plan-seo-experiment
description: Plan, start, observe, and evaluate one falsifiable SEO experiment using finalized evidence, an explicit target metric, resource locks, guardrails, rollback, and a minimum observation window. Use for title, content, schema, internal-link, information-architecture, performance, or GEO changes that optimize otherwise valid behavior rather than repair a confirmed defect.
---

# Plan SEO Experiment

## Overview

Control speculative SEO work so scheduled agents do not repeatedly edit the same
page before search and analytics evidence can mature. Follow
[`../../references/evidence-and-experiment-contract.md`](../../references/evidence-and-experiment-contract.md).

This skill is not used for confirmed technical defects. Repairs follow
`$change-seo-site` immediately when safe.

## Required context

Read:

- `.github/seo-data/site.md`, `daily-task.md`, all other existing
  consumer-owned SEO-data files, and the newest daily reports;
- the site's declared durable experiment ledger when present; `experiments.md`
  is the recommended new-site filename, not a required migration target;
- current finalized evidence from `$collect-seo-data`;
- the finding or opportunity from `$audit-seo-site`;
- `$change-seo-site` and the shared delivery contract.

If no durable experiment ledger exists and the site is ready for experiments,
add the record in the most natural consumer-owned location. A new site may copy
`.github/seo-skills/templates/seo-data/experiments.example.md`; an existing site
must not rename or restructure its metadata merely to match that example. The
absence of the recommended filename is not a technical defect.

When a site adopts the recommended ledger shape, validate it before
implementation and again before closeout:

```bash
python .github/seo-skills/scripts/validate_experiment_ledger.py \
  --ledger .github/seo-data/experiments.md \
  --site .github/seo-data/site.md
```

This validator is opt-in. Do not apply it to a consumer-owned custom ledger
format without a site-specific adapter.

## Eligibility gate

A proposed change is eligible only when all are true:

- current behavior is valid and the work is genuinely an optimization;
- the motivating finding has explicit evidence and is not merely a generic SEO
  recommendation;
- a primary target metric and provider are available;
- the baseline window is finalized and comparable to the future evaluation
  window;
- the affected resources can be isolated;
- implementation and rollback are source-controlled and verifiable;
- no active experiment already locks an overlapping resource;
- the site's maximum active speculative experiment count would not be exceeded.

When these conditions are not met, record `monitor` or `unknown` rather than
forcing a change.

## Experiment states

Use only:

- `proposed`: complete design, not implemented;
- `active`: implementation is deployed and measurement has started;
- `observing`: deployed, but earliest review date has not arrived;
- `evaluating`: the observation window is mature and evidence is being compared;
- `won`: keep the change;
- `lost`: roll back or replace the change through a new controlled operation;
- `inconclusive`: release the lock without claiming success;
- `aborted`: interrupted by a defect, measurement change, rollback, or major
  confounder.

## Workflow

### 1. Check active work before proposing anything

Read the declared experiment ledger and identify active-like states: `active`,
`observing`, and `evaluating`. Enforce the site limit and every URL, template, query-cluster,
navigation, content, schema, and analytics resource lock.

If the relevant experiment is still observing, make no speculative site change.
Collect current evidence, record that the window is immature, and stop. A no-op
run is a correct result.

### 2. Define a falsifiable experiment

Create a stable ID such as `EXP-20260805-01` and record:

- motivating finding and affected resource;
- one-sentence hypothesis;
- primary target metric, provider, dimensions, and aggregation;
- finalized baseline start/end and value;
- expected direction and practically meaningful threshold;
- guardrail metrics and failure conditions;
- exact resource lock;
- implementation plan and smallest authoritative validation;
- rollback condition and method;
- finalization lag, minimum observation window, and earliest review date;
- known confounders.

Do not use rank, traffic, conversion, or AI citation promises as facts. The
threshold is a decision rule, not a forecast guarantee.

### 3. Persist the proposed record before editing

Add the complete proposed experiment to the consumer-owned experiment ledger
and today's existing-format report. Update the site's current-status record when
one exists with the proposed resource lock. Deliver this record through
a real pull request if it cannot be included atomically with a narrowly scoped
implementation pull request.

### 4. Implement one isolated change

Invoke `$change-seo-site` and identify the operation as an experiment rather than
a repair. Keep the diff limited to the declared resources. Preserve measurement,
record pre-change output, run CI, self-review, squash-merge, wait for the exact
deployment, and verify the declared changed behavior.

After deployment, update the record with the pull request, squash commit,
deployment, start time, status `observing`, and earliest review date through the
metadata closeout pull request.

### 5. Observe without interference

Until the earliest review date:

- collect normal source-native metrics;
- do not change the locked resources speculatively;
- do not repeatedly rewrite the same title, content, links, schema, or template;
- record outages, releases, seasonality, measurement changes, and other
  confounders;
- allow confirmed technical repairs, but mark the experiment aborted or
  inconclusive when causal interpretation is no longer credible.

### 6. Evaluate a mature window

Use equivalent finalized baseline and evaluation windows. Preserve source
semantics and relevant dimensions. Record absolute and relative changes, missing
data, confounders, guardrails, and whether the decision threshold was met.

Choose one outcome:

- `won`: retain the change and release the lock;
- `lost`: use `$change-seo-site` for the declared rollback, verify production,
  then release the lock;
- `inconclusive`: retain or revert based on guardrails and maintenance cost, but
  do not claim an SEO win;
- `aborted`: record why the test became uninterpretable.

Deliver the evaluation and any rollback through the normal PR, CI, self-review,
deployment, verification, and closeout lifecycle.

## Completion criteria

An experiment is complete only when its durable record includes the baseline,
hypothesis, target metric, resource lock, implementation and deployment
evidence, mature evaluation window, outcome, and released lock. An active
experiment without a mature window is ongoing, not incomplete daily work.
