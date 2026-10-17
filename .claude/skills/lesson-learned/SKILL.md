---
name: lesson-learned
description: Write a recap of the general, reusable low-level/systems-programming knowledge surfaced in a technical Q&A or mentoring conversation (e.g. code-crafter stages, debugging sessions, concept explanations) — not a summary of the project or stage itself. Use when the user asks for a "recap," "summary of what I learned," "lesson learned," or wants their questions/doubts captured for later review.
---

# Recap Lesson Learned

Produce a recap of the **transferable systems-programming knowledge** a conversation surfaced — the kind of thing a good low-level programmer should just know, and that will come up again in some *other* project, in some *other* language, years from now. This is not a summary of the project, the stage, or what was built — it's the durable lesson underneath it, extracted and stripped of the specific context it happened to appear in.

The test for every sentence: **would this still be true and useful if the user had learned it while building a completely different project?** If a sentence only makes sense with reference to *this* codebase, this stage, this file, or this exercise's specific naming — it's boilerplate, not a lesson, and it doesn't belong.

## What goes in

- **General concepts** the conversation touched, named and explained the way a textbook or a senior engineer would explain them — e.g. "intrusive vs. non-intrusive data structures," "why pointer arithmetic is typed," "idempotency in mutation APIs," "macro hygiene," "sentinel nodes vs. NULL-checking." One topic can be as broad as "how the C preprocessor expands macros" or as narrow as "why you cast to `char *` before subtracting an `offsetof` byte count" — whichever is the actual reusable unit of knowledge.
- **The user's own questions, answered**, generalized and folded directly into the relevant topic — not as project-specific Q&A, but as the general principle their question was really about.
- **General advice / good practice for systems programming** that came up as relevant — naming/namespacing conventions, why certain bugs are made loud vs. silent by design, safety idioms, common pitfalls in the field — but only pieces the conversation actually touched, not a generic checklist.
- A minimal, illustrative code snippet is fine when a concept is easier to state in code than in prose — but keep it generic/example-shaped, not a pasted excerpt of the project's actual source.

## What stays out

- **Anything specific to the project, its stages, its file names, its variable/type names, or its curriculum** (e.g. don't write "in `list.h`," "stage 1," "the `ing_` prefix," "`ing_container_of`" as the running example) — translate it into the general concept it was an instance of.
- **A summary of what was built or what stage/task was completed.** That belongs in the project's own `progress.md` or notes, not in this recap.
- Redundant restatement of the same point under multiple headings.
- Wrong intermediate attempts, unless the *reason it was wrong* reveals a genuinely general misconception worth remembering.
- Meta-commentary about the conversation itself ("the user then asked...", "I explained that...") — write the explanation directly, not a narration of the dialogue.
- Material the user didn't ask about and that isn't load-bearing for what they did ask about.

## Visualize the moving parts

When a concept has structure or motion — memory layout, pointer relationships, data flowing through a pipeline, state transitions, a request/response exchange — draw it. Write a small standalone TikZ file (`\documentclass[tikz,border=4pt]{standalone}`), compile it with `tectonic <name>.tex`, convert to PNG if needed (e.g. `pdftoppm -png -r 200`), view the result to check it, and embed it in the recap (`![caption](figures/<name>.png)`), keeping the `.tex` source next to it.

- One idea per figure; label every box and arrow with the general concept, not project names.
- Show what moves and in what order: arrows, numbered steps, before/after panels.
- Skip it when the concept is purely verbal — a diagram must make something clearer, not decorate.

## Style

- Simple, plain language — assume the reader is the user, revisiting this because they forgot, not a stranger.
- Structure with headings per concept/topic, short paragraphs, code blocks where useful.
- Detailed enough to stand alone (no need to re-open the original conversation), but no filler — every sentence should teach something, not restate the heading.
- Default output is a markdown file in the current project directory (ask where, or use context clues like an existing `lesson.md`/`notes/` convention, if ambiguous) — write it with the Write tool, don't just print it into chat, unless the user explicitly asks to see it in chat first.


## Avoid this traps
1. Metadiscourse (significance-announcing). The sentence's job is to tell you the next sentence matters, rather than just saying the thing. "X is worth stating plainly," "That is not a detail," "Y deserves a mention of its own." Diagnostic: delete it and no information is lost. This is the largest category and the most characteristic.
2. Aphoristic antithesis. The two-beat epigram, usually closing a paragraph: "not X. It is Y", "A does not disappear; it moves." One short punchy sentence after a long one, landing like a drumbeat. In moderation it's good prose; four per page reads as a machine that has learned cadence without having anything to be emphatic about.
3. Text self-narration. Prose describing the document's own rhetorical behaviour instead of the subject: "Chapter 9 states this before it states any result," "Chapter 6 is largely an argument about when it must be invoked."
4. Enumerated essence. "Two habits separate a model check from an ornament." A count plus an evaluative noun, presented as a discovered taxonomy. (Contrast "The protocol has two steps" — a count of actual countable things, which is fine.)
5. Connoisseur diction. Words that rate rather than describe: ornament, repays attention, worth holding onto, the interesting one, the awkward case. They position the author as a judge of the material.
Cutting across all five: unearned confidence — superlatives and totalising claims with nothing behind them ("the single largest reason a local filesystem feels fast").
6. gnomic generalisations — the aphoristic maxim, or sententia in classical rhetoric: a timeless, subject-less, present-tense proposition offered as a general law rather than a claim about your system. Two markers make them detectable: an indefinite or universal subject ("A negative result…", "A checker never observed to fail…"), and a present-tense copula with no citation, no measurement, and no attachment to anything in the chapter. Related to the antithesis pattern, but distinct — antithesis is about shape, this is about epistemic posture. The register is the lecturer stating a principle rather than the author reporting work.
7. consensus-appeal tag — a booster that props a claim up with imagined agreement ("nobody disputes it", "everyone agrees", "uncontroversially") instead of with evidence. It's dead weight in a thesis specifically because you've just given the measurement; the numbers are the warrant, and appealing to unnamed consensus on top of them weakens rather than strengthens.


## Avoid counterfactual self-reference
Classification: counterfactual self-reference, an irrealis variant of the text self-narration family. Three things are stacked in it:
1. Irrealis mood about the document itself — the thesis imagining an alternate version of itself that was never written. Not a claim about GFS2, etcd, or QAttach; a claim about a hypothetical manuscript.
2. Authorial persona intrusion. "This thesis would be short" is a wink at the reader. It smuggles the author into an impersonal register without ever using "I" — the joke has a speaker even though the grammar doesn't name one.
3. Stakes-boosting. It tells the reader the coming failure is important instead of letting §4.5 establish it.


