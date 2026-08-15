---
name: human-writing-latex
description: |-
  Write or edit LaTeX prose in a formal, impersonal, scientific register that
  reads like a human author wrote it, not a language model — varied sentence
  length, no stock transitions or hedging filler, no restate-then-say
  padding. Use when writing or editing a .tex file, or any academic
  paper/thesis prose, regardless of section (abstract, related work,
  methods, discussion).
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  domain: academic-writing
---

## What I do

Write or revise scientific-paper/thesis prose in LaTeX so it reads as a human
author's formal, impersonal writing rather than obviously LLM-generated text,
while keeping the field's expected register.

## Rules

- Vary sentence length deliberately. Follow a long, subordinate-clause-heavy
  sentence with a short one. Do not settle into a uniform rhythm of
  medium-length sentences — that cadence is the most obvious tell.
- Do not open paragraphs with "Furthermore," "Moreover," "Additionally,"
  "It is worth noting that," or "This highlights." Vary or drop transitions;
  not every paragraph needs one.
- Avoid stock hedging/inflation pairs: "not only... but also," "plays a
  crucial role," "serves as a testament to," "underscores the importance of,"
  "in the realm of," "it is important to note." These read as filler in a
  paper and reviewers notice them.
- Prefer plain verbs over nominalizations where it doesn't cost precision
  ("we show" over "this demonstrates the fact that").
- Keep the register impersonal/formal: passive voice or first-person plural
  ("we observe", "it is shown that") as the field's convention dictates —
  but do not oscillate between "I," "we," and passive within one section.
- Do not force perfect parallelism across a list of claims. A slightly uneven
  list ("first, X; second, Y, which also implies Z; finally W") reads more
  human than a rigid enumeration.
- Do not over-hedge every claim ("may potentially suggest a possible
  correlation"). State results plainly; reserve hedging for genuine
  uncertainty, and name the reason for the uncertainty rather than using a
  generic qualifier.
- No em-dash-heavy staccato style, no rhetorical questions, no rule-of-three
  flourishes ("robust, scalable, and efficient"). These are creative-writing
  habits, out of place in a paper.
- Do not summarize what a section will say and then say it ("In this section
  we will discuss X. X is..."). Just say it.
- Keep citations and equations where a domain author would place them. Do not
  add a sentence restating an equation in words unless the field's convention
  calls for it.

## Self-check before returning text

Read the draft back and ask whether any sentence could be deleted without
losing content. LLM prose often pads with a sentence restating the previous
claim — cut those.

## When to use me

Use for any writing or editing task inside a `.tex` file, or any request for
academic/thesis/paper prose, in any section. Do not apply these rules to
code comments, commit messages, or non-academic documentation.
