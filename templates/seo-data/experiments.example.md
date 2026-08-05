# SEO experiments

## Policy

- Maximum active speculative experiments: 1
- Default observation window: 28 finalized days
- Resource locks: URL, page template, query cluster, navigation path, schema surface, or measurement implementation
- Technical repair override: allowed, but an overlapping experiment becomes `aborted` or `inconclusive`
- Raw query rows: remain outside Git

A daily run does not need to start an experiment. Do not change a locked resource
again before the earliest review date. Compare equivalent finalized windows and
preserve provider metric semantics.

## Active experiments

No active experiment.

Use this record shape when starting one:

```text
### EXP-YYYYMMDD-01 — concise title

- Status: `proposed`
- Motivating finding: `FINDING-ID`
- Hypothesis: one falsifiable sentence
- Primary metric: source-native metric and provider
- Baseline window: YYYY-MM-DD to YYYY-MM-DD, finalized
- Baseline value: reviewed aggregate
- Expected effect: direction and practically meaningful threshold
- Guardrails: metrics and failure conditions
- Resource lock: exact URL, template, query cluster, or other surface
- Implementation pull request: not started
- Deployed commit: not deployed
- Start time: not started
- Finalization lag: use `site.md`
- Minimum observation window: use `site.md`
- Earliest review date: not scheduled
- Rollback: trigger and source-controlled method
- Confounders: none known
```

## Closed experiments

No closed experiment.

Move completed records here with status `won`, `lost`, `inconclusive`, or
`aborted`. Preserve the evaluation window, absolute and relative change,
guardrail result, confounders, decision, rollback when applicable, and released
resource lock.
