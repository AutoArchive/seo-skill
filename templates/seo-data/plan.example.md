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
- Every automated change uses a fresh branch and a real non-draft pull request.
- Required and expected CI must pass before the final automated self-review.
- A clean final review is followed by squash merge; human review is not needed.
- Site changes wait for the exact squash commit's production deployment and
  public verification.
- Post-merge evidence is recorded through a metadata-only closeout pull request
  that follows the same CI, self-review, and squash-merge rules.
- Normal operation does not require human approval.

Short-term fixes, one-off audits, and remediation backlogs belong in GitHub
issues, not in this durable plan.
