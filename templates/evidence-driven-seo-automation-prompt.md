# Evidence-driven SEO automation prompt

Use this template when a consuming repository wants the audit-and-experiment loop
without replacing its existing daily prompt. Preserve that repository's own SEO
data filenames, headings, status vocabulary, and report format.

```text
Run one evidence-driven SEO operating cycle for <canonical-site>.

Read the complete repository instructions and every current file under
.github/seo-data/. Use the installed shared skills in this order when applicable:

1. $ensure-site-analytics — verify production measurement and ownership.
2. $collect-seo-data — collect repository, deployment, live-site, Search Console,
   analytics, and infrastructure evidence for exactly one canonical site.
3. $audit-seo-site — produce typed findings and classify each as repair,
   experiment, monitor, unknown, or not-applicable.
4. $change-seo-site — repair the highest-impact confirmed defect in the same
   cycle when it is safe and source-controlled.
5. $plan-seo-experiment — for an otherwise valid behavior, start at most one
   falsifiable experiment only when a finalized baseline and non-overlapping
   resource lock exist.

Operating rules:

- Missing evidence is unknown, not zero and not a pass.
- Keep raw query rows, credentials, user-level analytics, and private provider
  identifiers outside Git.
- Do not compare partial data with a finalized window.
- Do not combine Search Console clicks, GA4 sessions, and infrastructure visits
  into one synthetic traffic metric.
- Do not make a second speculative edit to a URL, template, query cluster,
  navigation path, schema surface, or measurement implementation locked by an
  active experiment.
- A confirmed technical defect may override a resource lock, but the overlapping
  experiment must become aborted or inconclusive.
- A no-op is a valid cycle when evidence is incomplete or an observation window
  is immature. Do not manufacture a content change merely to create a pull
  request.
- Preserve consumer-owned metadata layout. The shared example filenames are
  onboarding defaults, not a migration requirement.

For compatible Search Console CSV exports, derive opportunity candidates with:

python .github/seo-skills/scripts/analyze_gsc_exports.py \
  --query-csv <temporary-current-query.csv> \
  --page-csv <temporary-current-page.csv> \
  --prior-query-csv <temporary-prior-query.csv> \
  --prior-page-csv <temporary-prior-page.csv> \
  --query-page-csv <temporary-current-query-page.csv> \
  --output <temporary-gsc-analysis.json>

Use --public-safe only for a reviewed derived artifact. Supply a high-entropy
SEO_QUERY_ID_KEY outside Git when stable opaque query identifiers are needed
across runs.

Every repository change must use a fresh branch and a real pull request, wait for
required and expected CI, complete final self-review, squash-merge only when the
repository's policy permits it, verify the exact deployed commit and declared
public behavior, and close out durable metadata through the same lifecycle.

The final report must state evidence windows, limitations, findings and
confidence, the selected disposition, pull request and commit evidence when a
change shipped, active resource locks and earliest review date, and the exact
next observation. Never claim rankings, traffic, conversions, or AI citations
without mature source-native evidence.
```
