# Human-only blockers

No human-only blockers.

The automation is authorized to perform all normal collection, repository,
branch, pull-request, CI-wait, self-review, squash-merge, deployment-wait,
verification, and closeout steps. Add an item here only when an external system
truly requires a human-only action or the required account permission does not
exist. Include the exact blocked action, evidence, impact, and minimal human
action needed. Remove resolved items in the next pull request.

Merged automation branch cleanup is best-effort hygiene. A connector without a
branch-deletion operation, or a harmless failure to delete an already-merged
head branch, is not a blocker and must not be recorded here.
