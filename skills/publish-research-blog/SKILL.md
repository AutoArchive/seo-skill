---
name: publish-research-blog
description: Deliver one evidence-backed long-form research blog from editorial question selection through deep research, accessible academic writing, pull request review, production deployment, and public verification. Use for recurring scholarly blog publication programs.
---

# Publish Research Blog

## Purpose

Coordinate one complete research-publication cycle. This skill connects:

1. the consuming site's editorial research program;
2. `$deep-research-blog` for multilingual evidence gathering and falsification;
3. `$write-readable-research-blog` for clear academic-style prose;
4. `$change-seo-site` for repository delivery, CI, self-review, squash merge,
   actual production deployment, and public verification.

The public product is one coherent article. Search logs, source matrices, model
transcripts, JSON records, and metadata updates may support the work but do not
replace it.

## Production topology gate

Before selecting or publishing content, verify that the consuming site's durable
instructions accurately identify the canonical hostname, actual production
provider, provider project or service, production source repository, production
branch, build command, output directory, and verification method.

When public content does not match the repository believed to be live, or when
multiple deployment paths exist, freeze publication and invoke the site's
bootstrap or production-topology audit. A generated branch, preview deployment,
passing repository workflow, `CNAME` file, or HTTP 200 response is not production
proof.

## Site context boundary

A site may use files such as `site.md`, `position.md`, `plan.md`,
`daily-task.md`, `status.md`, `block.md`, `promotion.md`, and daily records.
`site.md` can hold technical production, deployment, analytics, and verification
facts. `position.md` can hold mission, readers, research programs, editorial
boundaries, article form, language, and style. Site-specific content stays in the
consuming repository.

This list is guidance, not a structure enforced by the shared repository. If the
current pinned skill or the consuming site's own instructions explicitly require
a missing file or operating artifact, add it through a focused site-specific pull
request with only the minimum necessary change.

## Editorial program and topic selection

Read the site's editorial position, plan, and recent articles. A durable site may
organize work into several research programs, such as terminology history,
literary and media analysis, cross-language comparison, or repeated technical
experiments. These programs belong to the site, not this shared skill.

Select one narrow question that advances one program and fits into a larger chain
of articles. Prefer questions that:

- resolve a recurring confusion;
- reconstruct a missing history;
- distinguish terms that are often flattened together;
- compare how one object changes across languages or communities;
- explain a mechanism rather than merely describe a topic;
- test a model, search engine, translation system, or platform repeatedly with a
  reproducible method;
- create a prerequisite for later articles.

Check recent publication balance. Avoid publishing several articles in a row that
repeat the same thesis, source base, examples, or vocabulary with a different
title.

Before research, record internally:

- selected research program;
- exact question;
- connection to earlier and planned articles;
- intended new contribution;
- closest existing content and duplication risk;
- expected public URL and acceptance check.

## Research phase

Invoke `$deep-research-blog` completely.

The normal workflow is:

1. choose a sufficiently narrow question;
2. decompose it into Chinese, English, Japanese, other relevant-language, and
   counterargument query families;
3. search scholarly literature, primary material, institutional sources,
   archives, contemporaneous journalism, and relevant community history;
4. screen approximately 8–20 substantive sources;
5. deep-read approximately 3–8 load-bearing sources;
6. run a separate search intended to falsify the provisional thesis;
7. build an internal claim–evidence–counterevidence matrix;
8. verify bibliographic details and claim-level citation support;
9. hand a compact research packet to the writing phase.

The numbers are normal targets rather than permission to stop early. A disputed
or broad claim may require more evidence. A narrow archival article may use fewer
sources only when the primary evidence is unusually direct and the site-specific
rules allow it.

## Writing phase

Invoke `$write-readable-research-blog` completely.

The article should normally contain:

- informative title;
- abstract and keywords;
- direct opening answer;
- research question and scope;
- materials or method;
- sustained evidence-led argument;
- serious counterevidence or alternative explanation;
- clearly labeled original editorial synthesis;
- limitations;
- concise conclusion;
- claim-level citations and complete references.

Meet the consuming site's minimum length without using filler. Length is an
editorial floor, not evidence of quality.

Use collaborative affirmative prose. Let concrete materials drive the narrative,
show how comparisons produce judgments, and present competing interpretations
through their evidence positions. Collaboration comes from visible reasoning;
frequent “we” language and repeated rhetorical questions remain optional.

Author-written titles, descriptions, abstracts, headings, body text, captions,
callouts, synthesis, limitations, and conclusions must contain zero negative or
defensive constructions. Run the literal and semantic audits defined by
`$write-readable-research-blog`. Rewrite every denial, correction-first sentence,
disclaimer, anticipated objection, and self-protective caveat as a direct positive
statement of evidence, scope, relationship, chronology, confidence, or open
question. Source-accurate quotations, official titles, proper names, code, and
bibliographic entries retain their original wording.

## Article review packet

Before repository delivery, prepare a concise internal review packet containing:

- research program and question;
- one-sentence answer;
- article thesis and original synthesis;
- main-text character or word count according to site rules;
- source count by type and language;
- peer-reviewed, primary, archival, institutional, and weaker-source breakdown;
- strongest counterevidence and how it changed the thesis;
- known limitations;
- duplication check result;
- evidence-audit result;
- collaborative-language audit result;
- zero-negation literal scan result;
- defensive-language semantic review result;
- target source path, generated URL, canonical URL, and production acceptance
  check.

Use this packet to write the pull-request description and perform the post-CI
from-scratch domain review. Do not publish private notes or copyrighted source
excerpts.

## Repository delivery

Invoke `$change-seo-site` for the actual repository change.

The main pull request must include the article and only closely related site
changes. A recurring publication program may also update or add the site-owned
operating record explicitly required for the current publication cycle.

The pull-request body must state:

- research question and program;
- central answer and original contribution;
- main-text length;
- source composition and languages;
- counterevidence and limitations;
- article path, generated URL, canonical URL, and navigation path;
- validation performed;
- production provider and exact acceptance check;
- submodule update status when applicable.

Run the consuming repository's authoritative checks. Where available, check:

- front matter and real publication date;
- minimum main-text length;
- required article sections;
- citation and reference presence;
- broken internal and external links;
- Hugo or application production build;
- generated article path and canonical;
- structured data and social metadata;
- sitemap and internal navigation;
- invalid dates or placeholder content;
- duplicate title, slug, or substantially duplicated body.

## CI and domain-specific final review

Use `$deliver-github-pr` through `$change-seo-site` for complete expected CI and
the common from-scratch final review. During that post-CI review, also restart
the article review from the original research question and perform two separate
domain passes:

### Evidence review

- Every load-bearing factual claim has adequate support.
- Citations support adjacent claims and claimed scope.
- Source types and publication status are represented accurately.
- Counterevidence is serious rather than token opposition.
- Original synthesis is labeled and not falsely attributed.
- Quotations and paraphrases respect copyright limits.
- Sensitive identity, medical, legal, minors, and adult-subculture claims use
  strong sources and narrow wording.

### Writing review

- The opening gives a direct answer.
- Section order follows the argument.
- Paragraphs have clear jobs and concrete examples.
- Specialist vocabulary is explained.
- The reader can follow the materials and inferential path.
- Competing interpretations appear through their evidence positions.
- Every author-written field passes the zero-negation literal scan.
- Every defensive construction has become a positive statement of evidence,
  scope, relationship, chronology, confidence, or open question.
- The conclusion answers the original question.
- The article reads as one authored argument rather than stitched summaries.

Fix every issue on the same branch, wait for complete CI again, restart the
common review from the original request, and repeat both article passes.

## Merge, production, and public verification

After `$deliver-github-pr` returns a squash commit through `$change-seo-site`,
identify the deployment produced by the actual production provider for that
exact commit.

Verify the canonical public hostname independently. At minimum confirm:

- the expected article URL is reachable;
- title, date, body, citations, and references are present;
- canonical points to the intended URL;
- the article is discoverable through the intended internal navigation and
  sitemap;
- the public output corresponds to the exact source commit through an immutable
  marker or another site-approved evidence method;
- the response is production rather than preview, generated branch, legacy host,
  or stale CDN content.

A source file in the repository, generated file in a deployment branch, passing
workflow, or HTTP 200 alone does not complete publication.

Complete the consuming site's closeout process, adding only records explicitly
required by the current skill or site instructions.

## Completion criteria

A research-publication cycle is complete only when:

- one narrow question advanced a site-defined research program;
- multilingual deep research and a falsification pass were completed;
- the article contains a defensible original synthesis;
- evidence and style audits passed;
- the article meets site-specific length and structure rules without filler;
- the article uses collaborative reasoning and zero author-written negative or
  defensive constructions;
- a real pull request passed all expected CI, a common from-scratch review, and
  both complete article review passes;
- the pull request was squash-merged;
- the exact commit deployed through the actual production provider;
- the canonical public article was independently verified;
- the site's status or closeout record contains truthful delivery evidence.
