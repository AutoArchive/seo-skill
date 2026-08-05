---
name: deep-research-blog
description: Research one narrow, durable question for a source-auditable long-form blog. Use before drafting an academic-style article that requires multilingual search, scholarly literature, primary sources, counterevidence, claim-to-source mapping, and a final citation audit.
---

# Deep Research Blog

## Purpose

Produce the research foundation for one original, durable article. The output of
this skill is a verified research packet and a defensible thesis, ready for
`$write-readable-research-blog`. It is not a generated long report, a search log,
a bibliography dump, or a lightly rewritten encyclopedia entry.

The research process should save future readers and Agents from repeating the
same expensive work: finding the right sources, distinguishing related concepts,
resolving contradictions, identifying historical and cultural scope, and tracing
which claims remain uncertain.

## Required context

Read the consuming site's existing content, editorial plan, newest research
articles, repository instructions, and current daily task. Preserve the site's
existing `.github/seo-data` layout. Topic programs, publication cadence, and
site-specific terminology belong in the consuming site's existing `plan.md` or
equivalent instructions, not in this shared skill.

When the production repository or deployment path is uncertain, stop content
work and invoke the site's bootstrap or production-topology audit first. Research
completion does not prove that an article has deployed.

## Research question gate

Select one question that is:

- narrow enough to answer in one coherent article;
- durable enough to remain useful beyond a news cycle;
- materially different from existing site content;
- answerable through evidence rather than opinion alone;
- connected to a larger research program in the site's editorial plan;
- likely to produce a useful distinction, historical reconstruction, causal
  explanation, comparison, or testable synthesis.

Reject topics that are merely broad categories, keyword variants, generic
introductions, listicles, or prompts whose only contribution is summary.

Write a one-paragraph research brief before searching. It must state:

- the exact question;
- the current provisional answer;
- the expected geographic, linguistic, platform, and historical scope;
- the closest existing article and the intended new contribution;
- what evidence could change the provisional answer.

## Multilingual query decomposition

Break the question into query families before opening sources. Use every
materially relevant language. For a Chinese topic with Japanese or English
history, this normally includes Chinese, English, and Japanese.

At minimum create query families for:

1. **Definitions and terminology** — official definitions, dictionaries,
   original-language spellings, historical labels, aliases, and contested uses.
2. **History and chronology** — first documented uses, platform transitions,
   publications, events, archives, and changes in meaning.
3. **Mechanisms and interpretation** — academic explanations, media systems,
   community practices, economics, politics, technology, and cultural transfer.
4. **Primary or contemporaneous evidence** — original texts, interviews,
   institutional documents, archived pages, platform material, catalogues, or
   contemporary reporting.
5. **Counterarguments and falsification** — contrary interpretations, negative
   cases, scope exceptions, later corrections, changed terminology, and sources
   that would weaken the provisional thesis.
6. **Translation and cross-cultural mismatch** — false friends, missing
   equivalents, shifts between self-label and external label, and differences in
   who or what a term classifies.

Do not rely on one language's search results to describe another language's
history or community.

## Source collection target

The normal first pass reads or screens 8–20 substantive sources. Deep-read the
3–8 sources that carry the main argument. Broader or disputed questions require
more.

A strong source set usually contains:

- at least three peer-reviewed articles or scholarly book chapters;
- at least one primary, institutional, archival, lexicographic, or
  contemporaneous source;
- current sources when present-day usage or policy is discussed;
- sources from more than one language when the argument crosses languages;
- at least one serious source that complicates or challenges the provisional
  thesis.

Classify every source before using it:

- peer-reviewed article;
- academic book or chapter;
- thesis or dissertation;
- preprint or working paper;
- institutional, legal, medical, archival, or lexicographic source;
- contemporaneous journalism;
- community or platform material;
- collaborative reference source;
- search lead only.

A search snippet, citation list, AI summary, repost, or abstract alone cannot
carry a substantive claim. A source may still be useful for discovery, but the
article must cite the underlying material.

## Reading protocol

For each potentially load-bearing source, record internally:

- full bibliographic identity;
- source type and publication status;
- language and geographic scope;
- historical period or data window;
- population, corpus, platform, or material studied;
- exact claims the source supports;
- exact claims it does not support;
- limitations identified by the authors;
- relevant quotations or page locations for private verification, while keeping
  published quotation length within copyright limits;
- relationship to other sources: independent, derivative, contradictory, or
  complementary.

Read enough original text to verify the claim. Do not transfer a claim from one
paper's literature review to the cited work without checking the cited work when
the claim is central.

## Internal claim–evidence–counterevidence matrix

Build a private working matrix before drafting. It may be a temporary table,
notes document, or structured outline, but it is research infrastructure rather
than the public article.

For every major claim, record:

- proposed claim;
- supporting sources;
- source independence;
- strongest contrary evidence or alternative explanation;
- geographic, linguistic, platform, and historical scope;
- confidence level;
- wording allowed by the evidence;
- evidence that would require revision.

Claims without adequate support must be narrowed, marked as inference, or
removed. A bibliography at the end of an article does not repair missing
claim-level support.

## Counterevidence pass

After forming an initial thesis, perform a separate search whose goal is to make
the thesis fail. Search for:

- earlier examples that challenge an origin story;
- communities that use the term differently;
- alternative causal explanations;
- evidence from another platform, country, language, class, or generation;
- findings that distinguish fictional categories from real-world identity;
- later revisions, retractions, legal changes, or updated terminology;
- methodological criticism of the strongest source;
- cases where translation changes the social meaning of the object described.

Revise the thesis when counterevidence narrows its scope. The final article
should present the strongest remaining claim, not defend the first idea chosen.

## Original synthesis requirement

Every article must contribute at least one synthesis that cannot be copied from a
single source. Good synthesis may:

- identify a recurring mechanism across several cases;
- explain why two literatures reach different conclusions;
- separate a word's etymology from the history of the practice it names;
- show how platform, audience, or translation changes a category;
- propose a typology grounded in multiple independent sources;
- connect a historical change to a measurable or observable shift;
- identify a boundary condition that resolves an apparent contradiction.

Record the synthesis internally with:

- evidence combined;
- reasoning steps;
- scope and confidence;
- plausible competing explanations;
- future evidence that would require revision.

The article must label this as editorial synthesis or inference. It must not
attribute the synthesis to a source that did not make it.

## Research packet handoff

Before invoking `$write-readable-research-blog`, produce a compact internal
packet containing:

- final research question;
- one-sentence answer;
- thesis and 3–6 supporting subclaims;
- scope and explicit exclusions;
- source inventory by type and language;
- claim–evidence–counterevidence matrix;
- chronology or comparison table when useful;
- original synthesis and revision conditions;
- unresolved questions and limitations;
- verified bibliography entries;
- candidate article structure.

Do not publish the raw packet as the article. The public output must be a
coherent argument written for readers.

## Citation audit

Before research is considered complete:

1. Check every non-common-knowledge historical, empirical, legal, medical,
   demographic, etymological, chronological, and current-usage claim.
2. Confirm that the cited source supports the adjacent claim and the claimed
   scope.
3. Confirm names, titles, dates, page locations, DOI or stable URLs, and
   publication status.
4. Distinguish peer-reviewed work, books, theses, preprints, journalism,
   dictionaries, community material, and collaborative references in the prose
   when the distinction matters.
5. Remove citations included only to make the bibliography look larger.
6. Check source independence and avoid counting multiple retellings of one claim
   as multiple confirmations.
7. Mark remaining uncertainty directly and proportionally.

## Completion criteria

Research is ready for writing only when:

- the question is narrow and the new contribution is explicit;
- materially relevant languages were searched;
- the source set meets the site's quality threshold;
- the most important sources were read beyond snippets or abstracts;
- claim-level support has been mapped;
- a separate counterevidence search changed or confirmed the thesis;
- at least one original synthesis is defensible and clearly scoped;
- the bibliography and citation details are verified;
- unresolved uncertainty is documented;
- the packet can support one coherent article without filler.
