---
name: human-writing
description: |-
  Write or edit LaTeX prose in a formal, impersonal, scientific register that
  reads like a human author wrote it, not a language model — no first person,
  concrete referents instead of abstract placeholder nouns, varied sentence
  and paragraph length, no stock transitions or hedging filler, no
  restate-then-say padding. Writes technical content only from sources
  actually read, never from memory, and generates and embeds figures via the
  thesis-diagrams skill where they help. Use when writing or editing a .tex
  file, or any academic paper/thesis prose, regardless of section (abstract,
  related work, methods, discussion).
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  domain: academic-writing
---

## What I do

Write or revise scientific-paper/thesis prose in LaTeX (or markdown if specified) in a formal, impersonal
register that reads as a human author's writing rather than obviously
LLM-generated text.

## 0. What actually makes prose read as human

Specificity, not polish. LLM prose is recognisable because it is abstract,
evenly weighted, and uniformly hedged — not because of any single banned word.
Every rule below serves one of three goals: name concrete things, vary the
shape of the text, and let the emphasis be uneven.

Note the standing tension: formal impersonal academic register is inherently
low-variance, and low variance is exactly what automated detectors score
against. These rules reduce that signal but cannot remove it, and a detector
score is not the target — a reviewer's judgement is. Never trade correctness,
precision, or the field's register for a lower score.

## 1. Register (hard rules — these come first)

The default is impersonal. Do not use "I", "we", "our", "us", or "let us".
Recast with the passive, with an impersonal subject, or by making the artefact
itself the agent.

| Instead of | Write |
| --- | --- |
| we observe that X | it has been observed that X / X is observed |
| we show / we demonstrate | it is shown that / the results show that |
| we propose a method | a method is proposed |
| our experiments indicate | the experiments indicate |
| in this paper we describe | this paper describes |
| we can see from Fig. 2 | Fig. 2 shows |

Related constraints:

- Do not oscillate between voices. Once the impersonal register is set, hold
  it for the whole document, not just the current section.
- Passive voice is correct here and is not a defect to be "fixed". Do not
  rewrite impersonal constructions into the active first person for the sake
  of brevity or "directness".
- Exception: if the target venue's style guide or the surrounding existing
  text already uses first-person plural consistently, match the document.
  Match it silently; do not mix the two.
- Impersonal does not mean vague. Prefer a concrete agent to a hollow one:
  "the classifier misranks short queries", not "it can be observed that
  misranking occurs".

## 2. Lexical specificity (the highest-value rule)

Name the thing. Abstract placeholder nouns are the strongest LLM tell and the
one no rewriting tool can repair.

Generic nouns to replace wherever a concrete referent exists: *performance,
approach, method, framework, system, model, data, results, aspects, factors,
challenges, insights, capabilities, characteristics*.

- Not "the approach improves performance on the data" — but "beam search
  raises recall@10 by 4.2 points on the Farsi split".
- Not "several factors affect the results" — but "sequence length and
  tokenizer choice both shift the F1 by more than a point".
- Quantify where a number exists. Cite where a source exists. Name the
  dataset, the layer, the baseline, the metric, the unit.

Corollary: repeat the precise technical term rather than reaching for a
synonym. "The model … the architecture … the system …" for one referent is
elegant variation, and it reads synthetic. Terminological consistency is the
academic norm.

## 3. Verbs and nominalization

- Prefer plain verbs over noun-stacked constructions where precision allows:
  "the model converges after 40 epochs", not "convergence of the model is
  achieved at the point of the 40th epoch".
- This trades nominalization for a verb, not the impersonal voice for the
  first person. Both halves of the rule apply at once.

## 4. Rhythm, measurably

"Vary sentence length" is unfalsifiable, so make it checkable.

- Per paragraph of four sentences or more: at least one sentence under 12
  words and at least one over 30. Never a paragraph of uniformly 18–25 word
  sentences.
- Vary paragraph shape across a section. LLM prose settles into 4–5 sentence
  paragraphs throughout; real sections carry a two-sentence paragraph beside a
  nine-sentence one. At least one paragraph per section should be markedly
  shorter or longer than its neighbours.
- Vary sentence openings across a section, not merely between adjacent
  sentences. Use all four types: subject-first, prepositional or adverbial
  phrase first, subordinate clause first, and citation-first
  (`\citet{smith2021} showed that ...`). Subject-first should not exceed
  roughly half the sentences in a section; LLM defaults sit near 80%.

## 5. Structure and transitions

- Do not open paragraphs with "Furthermore," "Moreover," "Additionally,"
  "It is worth noting that," or "This highlights." Vary or drop transitions;
  not every paragraph needs one.
- Do not force perfect parallelism across a list of claims. A slightly uneven
  list ("first, X; second, Y, which also implies Z; finally W") reads more
  human than a rigid enumeration.
- No em-dash-heavy staccato style, no rhetorical questions, no rule-of-three
  flourishes ("robust, scalable, and efficient").
- Do not summarize what a section will say and then say it ("In this section
  we will discuss X. X is..."). Say it.

## 6. Filler and calibrated hedging

- Avoid stock hedging/inflation pairs: "not only... but also," "plays a
  crucial role," "serves as a testament to," "underscores the importance of,"
  "in the realm of," "it is important to note."
- Hedge asymmetrically. Uniform mid-strength hedging on every sentence is a
  strong synthetic signal. A well-supported result is stated flatly ("accuracy
  drops by 6 points"); a genuinely uncertain one is hedged hard *and the
  reason is named* ("with only 40 held-out examples per class, this gap may
  not be stable"). Nothing in between by default.
- "It has been observed that" is the register-correct form of a claim, but it
  is still a phrase — do not open three consecutive sentences with it. Vary
  between passive, impersonal subject, and artefact-as-agent.

## 7. Permitted imperfection

Over-polish is itself a tell. Real papers are allowed to:

- weight claims unevenly, spending three sentences on one finding and half a
  clause on another of nominally equal importance;
- leave a minor observation unelaborated rather than closing every loop;
- use the slightly awkward phrase that is the field's actual idiom, in
  preference to the smoother generic alternative;
- repeat a term rather than vary it (see §2).

Do not manufacture flaws — see §9. This section permits leaving natural
unevenness in place; it does not license introducing errors.

## 8. Section-specific guidance

**Abstract.** Highest-density synthetic writing in most papers. No
scene-setting first sentence about the importance of the field. Open with the
problem or the contribution. Include at least one concrete number.

**Related work.** The worst offender. Do not write a per-paper list ("X et al.
proposed A. Y et al. proposed B."). Group by idea or by shared limitation, put
several citations behind one claim where they support it, and take a stance
toward the prior work — what it did not settle, where it disagrees with
another line, why it does not transfer to this setting. A related-work section
with no stance reads as a summarisation task, because that is what it is.

**Methods.** Specificity is cheap here and its absence is conspicuous: state
versions, hyperparameters, hardware, and seeds rather than "standard settings".

**Discussion / limitations.** Name real limitations with their mechanism, not
a generic list. "Future work" should follow from something in the paper, not
be a list of adjacent topics.

## 9. Citations and equations

Keep citations and equations where a domain author would place them. Do not
add a sentence restating an equation in words unless the field's convention
calls for it.

## 10. Sourcing — never write technical content from memory

Prose about a system, protocol, algorithm, or prior result must be written
from the actual document, open in front of you. Recalled detail is the single
most damaging failure mode in a thesis: a plausible-sounding wrong claim about
GFS2's locking or Corosync's membership protocol survives review far longer
than a stylistic tell, and it is the kind of error an examiner catches.

Procedure, in order:

1. **Look for the source locally first.** Check the project's `refs/`,
   `papers/`, `docs/`, or bibliography directory, and the `.bib` file, for the
   paper, RFC, man page, or specification. Read the relevant section.
2. **If it is not there, retrieve it** — the paper from its publisher or
   arXiv, the RFC, the project's official documentation, the man page
   (`man gfs2`, `man corosync.conf`), or the source repository. Save it into
   the project's references directory so the next session does not re-fetch.
3. **If it cannot be retrieved, stop and ask.** Say exactly which document is
   needed and for which claim. Do not fill the gap with recollection, and do
   not quietly soften the sentence into vagueness to avoid needing the source.
4. **Write the claim only after reading it**, and cite the specific section,
   figure, or page — not merely the work as a whole.

Look it up every time. Whenever the text describes something real (a
protocol, a kernel interface, a library contract, the project's own code),
open the source for that claim before writing it, even when the claim seems
familiar or is already in the draft. This applies to rewording too: an
existing sentence is not evidence. Re-verify every claim you carry over,
because the draft may predate the code.

For the project's own system, the code is the primary source, not its docs:

- Read the function that implements the behaviour, not just its doc comment.
  Docs, comments and earlier chapters drift. Check `git log` on the relevant
  files for recent changes that may have made a statement false.
- Where the code and the docs disagree, write what the code does, and report
  the discrepancy to the user so the doc or comment can be fixed.
- Take constants and defaults from where they are defined (intervals, sizes,
  caps, timeouts, key formats), not from prose that quotes them.
- When the code relies on an external contract (a libfuse header, a POSIX
  page, an RFC), read that contract as well, and cite it rather than the
  code comment that paraphrases it.

Additional constraints:

- Every non-obvious technical assertion carries a citation to something that
  was actually read in this session or is verifiably in the project's
  references. No citation is added to a work that has not been opened.
- Do not invent bibliography entries, DOIs, page numbers, section numbers, or
  quotations. A `\cite{}` key must exist in the `.bib`.
- Version matters. State the version or release the described behaviour
  belongs to when it has changed across versions, and confirm it in the
  document rather than assuming the current one.
- Prefer the primary source: the specification, the original paper, or the
  code, over a survey's summary of it or a blog restatement.
- Where the source is genuinely ambiguous or silent, say so in the text and
  attribute the uncertainty to the source — do not resolve it by guessing.
- When measurements or behaviour come from this project's own experiments
  rather than the literature, keep that boundary explicit; never blend a
  measured result and a cited one into one unattributed sentence.

This section outranks every stylistic rule above. A well-cadenced sentence
that misstates the source is worse than an awkward one that is correct.

## 11. Figures

A diagram is warranted when the text is describing a structure, a flow, a
state machine, a layering, or a timeline — anything where a reader would
otherwise have to reconstruct a picture from a paragraph. It is not warranted
as decoration, and a figure that merely restates a sentence should be cut.

When one is warranted, generate it with the `thesis-diagrams` skill rather
than describing it and moving on:

- Author the figure as a TikZ source under `figures/`, compile it with
  `figc`, and view the rendered PNG before considering it done.
- Include the compiled **PDF**:
  `\includegraphics[width=\linewidth]{figures/out/<name>}`, inside a
  `figure` environment with a `\caption` and a `\label`.
- Reference every figure from the prose by its label (`Fig.~\ref{fig:x}
  shows ...`). An uncited floating figure is a defect.
- Captions follow the same register rules as the body: impersonal, concrete,
  no first person. A caption states what the figure shows and what to notice
  in it; it is not a title fragment, and it is not a restatement of the
  paragraph.
- Figures depicting a system described in an external document are subject to
  §10 — draw the architecture from the specification or paper, not from
  recollection of it.
- Keep the palette and node styles consistent with the thesis's other
  figures, per the `thesis-diagrams` template.

Prefer drawing over describing: when a mechanism has moving parts (data
flowing between components, state changing across steps, memory layout, a
protocol exchange), a TikZ figure compiled with `tectonic` (directly, or via
`figc`) usually explains it faster than a paragraph. Use arrows, grouping,
and step numbers to show what moves and in what order, and one figure per
idea rather than one dense figure for everything.

Offer the figure when the prose would benefit; do not silently insert
unrequested figures into an editing task on existing text.

## 12. Prohibited "humanizing" tricks

Never attempt to lower a detector score by degrading the text. Specifically:
no deliberate typos or grammatical errors, no injected filler or redundancy,
no synonym-swapping for its own sake, no random punctuation variation, no
homoglyph or invisible-character insertion. These damage the paper, are
visible to reviewers and copy-editors, and constitute misrepresentation of the
text. The legitimate route is §2 and §4: real specificity and real variation.

## 13. Avoid these traps
1. Metadiscourse (significance-announcing). The sentence's job is to tell you the next sentence matters, rather than just saying the thing. "X is worth stating plainly," "That is not a detail," "Y deserves a mention of its own." Diagnostic: delete it and no information is lost. This is the largest category and the most characteristic. It often sits at the start of a paragraph as a stakes-raising opener: "\etcfs takes that literally.", "The cost is stated as plainly.", "One detail of trimming is easy to get wrong in a first implementation and hard to find later.", "The decisive point is that…", "The single most important structural fact about X is that…", "Two rows deserve comment." Fix: delete the opener and start with the claim ("The decisive point is that X needs etcd anyway" → "X needs etcd anyway").
2. Aphoristic antithesis. The two-beat epigram, usually closing a paragraph: "not X. It is Y", "A does not disappear; it moves." One short punchy sentence after a long one, landing like a drumbeat. In moderation it's good prose; four per page reads as a machine that has learned cadence without having anything to be emphatic about.
3. Text self-narration. Prose describing the document's own rhetorical behaviour instead of the subject: "Chapter 9 states this before it states any result," "Chapter 6 is largely an argument about when it must be invoked." Includes cross-reference chaining, where a sentence exists only to link to another part of the document and characterise it: "Chapter 4 ended on an asymmetry.", "Figure 5.1 is the figure the rest of the thesis refers back to.", "Section 5.4 argues why that boundary is where it is.", "the design question this chapter answers", "Chapter 12 treats that as the standing liability it is.", section intros listing what the subsections will do, and a chapter's closing paragraph previewing the next chapter. Cut them. A bare pointer attached to content ("\cref{ch:evaluation} shows the measurements") is fine.
4. Enumerated essence. "Two habits separate a model check from an ornament." A count plus an evaluative noun, presented as a discovered taxonomy. (Contrast "The protocol has two steps" — a count of actual countable things, which is fine.)
5. Connoisseur diction. Words that rate rather than describe: ornament, repays attention, worth holding onto, the interesting one, the awkward case. They position the author as a judge of the material.
Cutting across all five: unearned confidence — superlatives and totalising claims with nothing behind them ("the single largest reason a local filesystem feels fast").
6. gnomic generalisations — the aphoristic maxim, or sententia in classical rhetoric: a timeless, subject-less, present-tense proposition offered as a general law rather than a claim about your system. Two markers make them detectable: an indefinite or universal subject ("A negative result…", "A checker never observed to fail…"), and a present-tense copula with no citation, no measurement, and no attachment to anything in the chapter. Related to the antithesis pattern, but distinct — antithesis is about shape, this is about epistemic posture. The register is the lecturer stating a principle rather than the author reporting work.
7. Consensus-appeal tag — a booster that props a claim up with imagined agreement ("nobody disputes it", "everyone agrees", "uncontroversially") instead of with evidence. It's dead weight in a thesis specifically because you've just given the measurement; the numbers are the warrant, and appealing to unnamed consensus on top of them weakens rather than strengthens.
8. Verdict tails. A clause or trailing sentence appended to a claim that is already complete, grading it instead of adding a fact: "…rather than incidental benefits of it", "…and it is load-bearing rather than incidental", "the table is the inversion stated as a data layout", "a filesystem enforcing something other than what `ls -l` displays is a worse failure than one that enforces nothing of its own", "One store means one answer.", "and none of them is closable by tuning", "the cost is reported rather than argued away". Related to antithesis and gnomic maxims, but identified by position: it comes after the information, and cutting it at the last comma or full stop leaves the claim intact. Cut it there.
9. Inflated wording. Where a plain word says the same thing, use it. Watch for dramatised verbs ("measures what it costs" → "shows the measurements"; "never learn that consensus got slower; writes feel all of it" → "send nothing to etcd, while every write waits for a commit"), inflated necessity ("ownership has to be a key" → "ownership is a key"), and intensifiers that add no information: exactly, precisely, genuinely, entirely, "at all", "the clearest example", "one interesting way".

When revising existing prose against rules 1–9, change the framing only. Keep every technical claim, number, citation and cross-reference target that carries content. Most of these fixes are deletions; a sentence gets reworded only when deleting the framing would leave a fragment.

## 14 Avoid counterfactual self-reference
Classification: counterfactual self-reference, an irrealis variant of the text self-narration family. Three things are stacked in it:
1. Irrealis mood about the document itself — the thesis imagining an alternate version of itself that was never written. Not a claim about GFS2, etcd, or QAttach; a claim about a hypothetical manuscript.
2. Authorial persona intrusion. "This thesis would be short" is a wink at the reader. It smuggles the author into an impersonal register without ever using "I" — the joke has a speaker even though the grammar doesn't name one.
3. Stakes-boosting. It tells the reader the coming failure is important instead of letting §4.5 establish it.

## 15. Clarity: explain before arguing

The traps in §13 and §14 are about framing. This section is about sentences that are correct but hard to follow. The register stays formal and impersonal throughout, and clarity never justifies dropping precision.

1. Define a term before relying on it. Before using a technical term (extent, logical block, generation, arena), check the earlier chapters and sections for a definition. If there is none, add a one- or two-sentence definition where the term first carries weight, usually in the background chapter, and let later chapters add only what is specific to the system. A later definition does not excuse earlier uses.
2. One term per concept. When the background chapter names something ("logical block size"), later chapters use the same name. Do not switch to a near-synonym ("sector", "block boundary") in the same argument, and never use two of them in one sentence.
3. One idea per sentence. If a sentence joins two separate justifications with a semicolon or with "and", such as why something is needed and why it goes one way rather than the other, split it. Nested clauses, stacked participles and appositives inside appositives are split the same way. Long sentences are fine when they carry one line of reasoning.
4. State the mechanism, then its consequence. Say what the system does ("free space is the unclaimed arenas plus this node's own slack") before the property that follows from it ("so the figure is never too high"). A property stated without its mechanism reads as a slogan.
5. Say what goes wrong, concretely. When an alternative is rejected, name the observable failure: data reads back as zeroes, `write` fails with `ENOSPC` while `df` shows room, access differs from the mode bits `ls -l` shows. "A worse failure", "inconsistent" and "diverge" alone are not enough.
6. Use a small worked example for non-obvious mechanisms. For ordering, splitting, rounding, or any interaction between two records or two nodes, give concrete values: extent A covers bytes 0–100 with sequence 5, write B covers 40–60 with sequence 7. Keep it to a few sentences with real-looking numbers and name the outcome. Use examples sparingly: one for each mechanism that needs it, not one per paragraph.
7. Make every referent resolvable. Name the thing a sentence depends on: "a stamp" becomes "the generation and writer fields of an extent"; "ranked by their own keys" becomes "ordered by the chunk number in the key". If a data format matters to the argument (field order, separator, parsing rule), state it.
8. Headings and topic sentences say what the paragraph covers, not how interesting it is ("Three of the six fields exist because…", not "Three of the six fields repay attention").
9. Open with what and why. A chapter or section starts by saying what it
   covers and why the reader needs it, in concrete terms: what an application
   observes, what problem the mechanism solves. Do not start with a detail.
   This is content, not self-narration: "an application sees the filesystem
   only through stat, read and rename; this design decides what they return"
   rather than "this section discusses semantics".
10. Check the background exists. Before relying on a concept the reader may
    not know (hard links, unlink-while-open, readdir offsets, the scrubber,
    serializable versus linearizable reads), search the earlier chapters. If
    it is missing, add a short background subsection in the background or
    architecture chapter, or a one-sentence definition at first use, and point
    to it.
11. The heading must match everything under it. If a subsection holds
    material about something else (a rule about the snapshot under "Flush
    before yield", a create race inside a paragraph about flushes), move it
    or rename the subsection. Unrelated points never share a paragraph.
12. Several rules or cases go in a list, or in one paragraph each with a
    short bold lead naming the case. Never chain three or more rules into one
    paragraph of semicolons.
13. Cross-references point where the thing is actually explained. Before
    writing \cref{...}, open the target and confirm it covers the claim.
    Point the reader to the explanation, not to a passing mention of it.
14. State limitations as limitations. When the system does not meet a
    contract (a spec, a library requirement, POSIX), say so plainly, name
    the case in which it fails, and give the concrete consequence. Do not
    soften it by citing a permission the spec does not grant.
15. Figures carry structure, the text carries explanation. Keep prose out of
    figures: no paragraphs inside them and no summarising footers, only a
    short label per element. Captions are two or three sentences: what is
    shown, how to read it (line styles, numbering), what to notice. Long
    reasoning belongs in a paragraph of its own that walks through the
    figure, using the figure's step numbers. Every element in a figure must
    match the code, including transitions and the lane an action sits on.
    Check layout overlaps in the rendered PNG.
16. Explain the current design by its reasons, never by its history. When a
    choice needs justifying, state the problem it solves and what the
    alternative would do wrong, in the present tense ("a per-lock lease would
    add two commits to every write"), not how the design got there ("the
    per-lock lease used to cost two commits"). §16 has the full rule.

Check these against the source (§10). A worked example has to follow the real behaviour: every number and outcome in it must be something the code or documentation actually produces.

## 16. Current design, not its history

Describe the system as it is. The problems that shaped a design and the reasons for it stay; the timeline does not.

- Keep: the alternative that was rejected and its concrete failure, stated in the present tense ("interleaving the fields would shift every later offset and make whole-second records unreadable"; "scanning the whole prefix would hand out offsets inside a peer's arena").
- Drop: "earlier versions did X, now Y", "used to", "originally", "initially", "no longer", "until it was fixed", "was corrected", "since the change", dates of changes, and remarks that a previous version of the code or the docs was wrong.
- Rewrite "X broke, so it was changed to Y" as "Y, because X would fail in this way". If removing the history leaves a design choice without a reason, restore the reason in the present tense rather than leaving the choice unexplained.
- Measurements stay. A measured failure of the rejected alternative is evidence, reported as a measurement of that alternative, not as an episode in the project's past.

## Self-check before returning text

Run these mechanically:

1. Grep for `\bI\b`, `\bwe\b`, `\bour\b`, `\bus\b`, "let us". Every hit is
   recast, or justified by the §1 venue exception.
2. Grep for the generic nouns listed in §2. For each hit, confirm no concrete
   referent, number, or name was available.
3. Sentence-length spread: for each multi-sentence paragraph, confirm the
   under-12 and over-30 word sentences required by §4.
4. Opening-type histogram: count subject-first openings per section; if above
   roughly half, recast some as citation-first or phrase-first.
5. Paragraph lengths across the section are not all within one sentence of
   each other.
6. Deletion test: any sentence that could be removed without losing content is
   padding — cut it.
7. Framing sweep (§13): check each paragraph's first and last sentence for a
   stakes-raising opener or a verdict tail, and check every sentence naming a
   chapter, section or figure for self-narration. Cut what fails the deletion test.
8. Clarity pass (§15): every technical term is defined before it carries
   weight; one name per concept; no sentence carries two separate arguments;
   every rejected alternative names its concrete failure; non-obvious
   mechanisms have a worked example that matches the source.
9. Hedging is asymmetric, not uniform (§6), and every hedge names its reason.
10. Every technical claim traces to a document actually read (§10); every
   `\cite{}` key resolves in the `.bib`; nothing was written from memory.
11. Every figure is compiled, viewed, captioned, labelled, and referenced from
   the prose (§11).
12. History sweep (§16): grep for used to|originally|initially|no longer|until it
   was|was fixed|was corrected|previous(ly)?|earlier version|older|now ; each hit
   is recast as the present design plus its reason.
13. Source sweep (§10): for each claim about the project's system, name
    the file or function it was checked against in this session. Claims
    taken only from docs or the existing draft are re-checked in code.
14. Structure sweep (§15.9–15.16): every section opens with what and why;
    every term has background; every heading matches its content; every
    \cref target covers the claim; figures hold no prose and captions are
    at most three sentences; design choices are justified by reasons, not
    history.

## When to use me

Any writing or editing task inside a `.tex` file, or any request for
academic/thesis/paper prose, in any section. Do not apply these rules to code
comments, commit messages, or non-academic documentation.
