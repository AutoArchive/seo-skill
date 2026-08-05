# SEO plan

## Purpose

State the durable, public-safe outcome this website should achieve for its
audience. Keep credentials, private business strategy, and personal information
out of this file.

## Success signals

- Define stable outcome metrics and review cadence.
- Explain which data source supports each signal.
- Preserve source-native semantics instead of inventing a blended score.

## Operating constraints

- Raw analytics stay outside Git.
- Every automated change uses the anonymous repository-local Git identity.
- Work is committed and pushed directly to the default branch; do not open PRs.
- Local validation and self-review happen before push; exact-commit CI must pass.
- Site changes wait for deployment success and public verification.
- Normal operation does not require human approval.

Short-term fixes, one-off audits, and remediation backlogs belong in GitHub
issues, not in this durable plan.
