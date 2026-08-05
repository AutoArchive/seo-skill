# Contributing to the shared SEO skills

## Authorization

Modify this shared repository only when the user explicitly requests a change to
`AutoArchive/seo-skill`. Work on a consuming website, a submodule update, or a
daily SEO operation does not by itself authorize expanding or refactoring the
shared skills.

Do not close, edit, supersede, or merge another contributor's pull request unless
the user explicitly asks for that action.

## Incremental, minimum necessary scope

Every change to this shared repository must be incremental, independently
reviewable, and limited to the smallest change that satisfies the user's explicit
request. Preserve existing skill behavior and repository-wide operating contracts
unless changing that behavior is itself part of the request.

Before editing, identify:

1. the exact user request;
2. the directly affected skill or file;
3. the smallest change that satisfies the request;
4. the existing checks that are sufficient to validate it.

Adding or improving one capability does not authorize changing unrelated
scheduler cadence, daily-record retention, pull-request or closeout requirements,
analytics policy, consuming-repository layout, or other skills. Leave a separate
improvement out of the current pull request unless the user explicitly requests
it.

Avoid opportunistic refactors, new skills, new templates, new validators, new CI,
new schemas, terminology rewrites, or broad documentation synchronization unless
they are directly required by the user's request.

When one file can fix the issue, change one file. Update additional files only
when they would otherwise become factually incorrect or the requested feature
cannot work without them. When a requested change is genuinely large, split it
into independently useful phases that keep the current skills usable and
reversible after each phase.

## Consuming repositories

Website production changes must follow the incremental-change and blast-radius
policy in `$change-seo-site`: make the smallest independently deployable and
reversible change, preserve unrelated behavior, and verify affected and
representative unaffected pages.

Templates are examples, not automatically enforced schemas. Do not create a
shared validator or CI job to enforce consuming repositories' filenames,
headings, section order, or Markdown structure unless the user explicitly asks
for such enforcement.

When a current skill explicitly introduces a new requirement, consuming
repositories may add the minimum fields, files, or workflow changes needed to
follow it. Do not invent a permanent prohibition against future additions or
migrations.

A website change does not authorize editing this shared repository, and a shared
skill update does not authorize unrelated website changes.

## Validation and delivery

Use the repository's existing checks whenever possible. Do not add a new CI
workflow solely to validate one documentation change unless the user explicitly
requests it or the requested feature cannot be validated safely otherwise.

Deliver changes through a focused pull request. Review the final diff for
unrequested files, changed operating contracts, and scope expansion before
merge. Follow the repository's normal CI, self-review, and squash-merge process.
