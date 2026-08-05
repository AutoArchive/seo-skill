---
name: write-readable-research-blog
description: Turn a verified research packet into an accessible academic-style blog article. Use after deep research when the article must preserve evidence, counterarguments, citations, and original synthesis while remaining clear to non-specialist readers and avoiding repetitive self-negating or jargon-heavy prose.
---

# Write Readable Research Blog

## Purpose

Write a complete research article that a careful general reader can understand
and a future Agent can cite without losing the argument's context. The article
should carry the evidentiary discipline of an academic paper and the clarity,
pace, and concreteness of a strong long-form blog.

Invoke `$deep-research-blog` first. This skill does not repair weak research,
missing counterevidence, or unverified citations through confident prose.

## Core writing model

Use this sequence:

```text
precise question
→ direct answer
→ why the question is difficult
→ evidence and comparison
→ counterevidence and boundary conditions
→ original synthesis
→ implications and limitations
→ concise conclusion
```

A good article feels like one sustained explanation. It should not feel like a
research log, a stitched set of source summaries, a glossary, or a paper template
filled mechanically.

## Recommended article form

Adapt the structure to the question, but normally include:

1. **Title** — specific, informative, and searchable without becoming a keyword
   pile. Prefer a real question, distinction, mechanism, or finding.
2. **Abstract** — 150–300 Chinese characters summarizing the question, material,
   central answer, and original contribution in plain language.
3. **Keywords** — 4–8 terms that genuinely describe the argument.
4. **Opening answer** — answer the question within the first 2–4 paragraphs.
   Give readers the useful result before the literature tour.
5. **Question and scope** — define the object, period, languages, platforms, and
   exclusions. Explain why common treatments create confusion.
6. **Materials or method** — describe source selection, comparison, corpus,
   experiment, or interpretive method briefly and concretely.
7. **Main argument** — usually 3–6 sections, each advancing one subclaim through
   evidence, examples, and interpretation.
8. **Counterevidence or alternative readings** — present the strongest competing
   explanation and show how it changes the thesis.
9. **Editorial synthesis** — state the original insight, evidence combined,
   reasoning, scope, confidence, and revision conditions.
10. **Limitations** — identify missing archives, uneven languages, sampling
    limits, uncertain chronology, platform bias, or unavailable evidence.
11. **Conclusion** — answer the research question directly and state what the
    article changes in our understanding.
12. **References** — complete, consistently formatted, and limited to sources
    actually used.

Headings should describe the claim or problem in that section. Avoid a sequence
of empty labels such as “Background,” “Discussion,” and “Analysis” when a more
informative heading is available.

## Paragraph and sentence design

- Give each paragraph one main job.
- Put the paragraph's claim or question near the beginning.
- Follow abstract claims with a concrete example, source, quotation fragment,
  comparison, or observable consequence.
- Keep most paragraphs to 2–5 sentences. Use occasional shorter paragraphs for
  emphasis and longer paragraphs only when the reasoning requires continuity.
- Vary sentence length. Use short sentences to state findings and longer
  sentences to express qualified relationships.
- Prefer active verbs and concrete subjects: “研究者比较了……”, “平台把……分类为……”,
  “这个译法改变了……”.
- Introduce one specialist term at a time. Give its original-language form and a
  one-sentence explanation on first use.
- Translate necessary jargon into ordinary language immediately. If a term
  cannot be explained clearly, reconsider whether it is needed.
- Keep citations close to the claim they support. A citation cluster at the end
  of a long paragraph should not leave readers guessing which sentence it
  supports.

## Positive, direct argumentation

Chinese analytical prose often falls into a repetitive corrective rhythm:
“不是……而是……”, “并非……”, “不只是……”, “这并不意味着……”. These forms are useful
when a real logical contrast depends on negation. Repeated use makes the author
sound as if every paragraph is correcting an invisible opponent and gives the
article an automated, defensive cadence.

Default to positive formulations:

- “这个词的核心功能是……”
- “现有证据支持三点判断……”
- “在日本御宅文化语境中，它首先指向……”
- “中文传播增加了一个新的分类维度……”
- “两组研究的差异来自材料范围……”
- “这项结论适用于 2010 年后的平台语境……”
- “资料仍不足以确定最早用例……”

Use negation for evidence boundaries, factual correction, and explicit
non-equivalence. Do not use it as the default opening gesture.

### Self-negation style audit

During the final edit, search for patterns such as:

- `不是……而是……`
- `并非`
- `并不是`
- `不只是` / `不仅仅是`
- `这并不意味着`
- `不能简单地说`
- `与其说……不如说……`
- `并不能证明`

For a 5,000-character Chinese article, more than three rhetorical contrast
patterns usually signals a style problem. Rewrite excess cases as direct claims.
Keep additional instances only when removing the negation would weaken a precise
boundary or misstate the evidence. Avoid placing these constructions in adjacent
paragraphs.

The audit is qualitative rather than a mechanical ban. Sentences such as “现有
资料无法证明直接谱系” may be the most accurate scholarly wording and should
remain.

## Avoid automated academic mannerisms

Limit or remove phrases that add ceremony without information:

- “值得注意的是”
- “需要指出的是”
- “众所周知”
- “显而易见”
- “毫无疑问”
- “从某种意义上说”
- “不可否认”
- “随着时代的发展”
- “在当今社会”
- repeated “本文认为 / 本文指出 / 本文试图”
- repeated “首先、其次、再次、最后” as the main organizing device

Replace them with the actual observation, evidence, or transition.

Bad:

> 值得注意的是，男娘这一概念并不是一个简单的身份标签，而是一种复杂的文化现象。

Better:

> “男娘”同时承担审美标签、角色分类和社群称呼三种功能；具体含义取决于使用者、平台和对象。

## Accessible academic tone

The desired tone is calm, precise, curious, and confident about evidence while
transparent about uncertainty.

Use:

- direct declarative sentences;
- concrete historical or textual examples;
- explicit transitions showing why the next section follows;
- calibrated claims such as “现有材料支持”, “在这一语料范围内”, “较强证据来自”,
  and “这一解释仍需更早档案验证”;
- short explanations of method and source quality;
- respectful distinctions among identity, expression, sexuality, performance,
  external labeling, and fictional genre.

Avoid:

- inflated claims of novelty or importance;
- moral verdicts standing in for analysis;
- unexplained theory names;
- long chains of abstract nouns;
- excessive parenthetical qualifications;
- rhetorical questions that the article never answers;
- treating one community, platform, country, or generation as internally uniform;
- assigning a sensitive identity to a real person through appearance or external
  labels;
- imitating journal opacity merely to look scholarly.

## Explain theory through its analytical work

When using a theoretical concept, explain what it helps the reader see.

Weak:

> 本文借鉴表演性理论、话语分析与跨文化翻译理论展开讨论。

Stronger:

> 本文把名称视为一种分类行动：它决定谁有权命名、对象被放进哪一类，以及读者随后会如何理解这个人或角色。这一视角帮助我们比较同一外表在中文、日文和英文语境中获得的不同社会位置。

Cite the theory when it materially shapes the argument. Do not decorate the
article with theories that never change the analysis.

## Source integration

Sources should enter the prose through claims and disagreements rather than
serial summaries.

Avoid:

> A 认为……。B 认为……。C 又认为……。

Prefer:

> 对大学女装比赛的研究显示，参与者能够借女性化表演扩展男性气质的边界；同一材料也记录了对女性身体的戏仿和等级化观看。两组现象同时出现，说明边界松动与旧有权力关系可以并存（作者，年份）。

When sources disagree:

1. state the shared question;
2. identify differences in corpus, period, language, platform, population, or
   method;
3. explain which conclusion each design can support;
4. show how the disagreement changes the article's thesis.

## Original synthesis paragraph

The original contribution deserves one clearly marked section or paragraph.
Use language such as:

> **编辑综合：** 综合上述材料，本文提出……

Then state:

- the finding;
- evidence combined;
- reasoning;
- scope;
- confidence;
- what evidence would revise it.

Do not present synthesis as settled scholarly consensus.

## Readability checks

Before finalizing, verify:

- a reader can find the answer within the opening screen or first several
  paragraphs;
- every section can be summarized in one plain sentence;
- no paragraph requires three unexplained specialist terms;
- examples appear wherever the argument becomes abstract;
- headings reveal the article's logic;
- tables and lists clarify comparisons rather than replace prose;
- the conclusion answers the same question posed at the beginning;
- the article still makes sense when citations are visually ignored;
- citations remain sufficient when the prose is checked claim by claim;
- the article sounds like one author reasoning, not a set of generated fragments.

Read the article aloud or simulate an oral reading. Rewrite sentences whose main
verb appears too late, whose subject is unclear, or whose qualifiers obscure the
finding.

## Final evidence and style audit

Complete two separate passes.

### Evidence pass

- Verify every factual and historical claim against the research packet.
- Check citation placement, bibliographic details, source type, and scope.
- Check quotations and paraphrases against copyright limits.
- Confirm that uncertainty, counterevidence, and limitations remain visible.
- Confirm that the original synthesis is labeled and not falsely attributed.

### Style pass

- Remove filler openings and ceremonial transitions.
- Rewrite excessive negative-antithesis constructions positively.
- Break overloaded sentences and paragraphs.
- Define jargon at first use.
- Replace abstract claims with examples where needed.
- Remove duplicated conclusions and source summaries.
- Make section openings state their contribution directly.
- Preserve nuance without surrounding every claim with defensive caveats.

## Completion criteria

The article is ready for repository delivery only when:

- it answers one precise question through a sustained argument;
- the opening gives a useful direct answer;
- research method and scope are understandable;
- evidence, counterevidence, original synthesis, limitations, and conclusion are
  present;
- claim-level citations and bibliography are complete;
- specialist concepts are explained in ordinary language;
- rhetorical self-negation and academic filler have been reduced;
- prose remains readable without sacrificing evidentiary boundaries;
- the article meets the consuming site's length, metadata, and editorial rules;
- the author has completed separate evidence and style audits.
