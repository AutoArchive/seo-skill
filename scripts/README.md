# Optional deterministic helpers

The scripts in this directory are optional. A skill or consuming repository may
use one when it replaces duplicated local logic, but the shared package does not
require consumers to run it, commit its output, or adopt a new CI or metadata
schema.

Keep site-specific content, deployment-provider, privacy, and editorial rules in
the consuming repository.

## `site_snapshot.py`

`site_snapshot.py` reads a static output directory and can perform selected
common checks for generated HTML, titles, H1 counts, canonical URLs, internal
links, sitemap coverage, required files, and required text. Every check is
opt-in.

```bash
python .github/seo-skills/scripts/site_snapshot.py \
  --root out \
  --base-url https://example.com \
  --sitemap sitemap.xml \
  --require-title \
  --require-one-h1 \
  --canonical same-route \
  --check-internal-links \
  --check-sitemap-coverage
```

Use `--output` to write a JSON snapshot. Supplying an earlier snapshot through
`--baseline` prints an incremental page and sitemap diff; `--diff-output` writes
that diff as Markdown.

```bash
python .github/seo-skills/scripts/site_snapshot.py \
  --root out \
  --base-url https://example.com \
  --sitemap sitemap.xml \
  --snapshot-only \
  --output /tmp/current-site.json \
  --baseline /tmp/previous-production-site.json \
  --diff-output /tmp/site-diff.md
```

A baseline should normally represent the last verified production output rather
than an unverified local build. Snapshots may remain temporary CI artifacts; the
shared package does not require committing them.
