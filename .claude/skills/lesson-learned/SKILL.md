---
name: lesson-learned
description: Write a recap of the general, reusable low-level/systems-programming knowledge surfaced in a technical Q&A or mentoring conversation (e.g. code-crafter stages, debugging sessions, concept explanations) — not a summary of the project or stage itself. Published as a page in the Notion Lessons knowledge base. Use when the user asks for a "recap," "summary of what I learned," "lesson learned," or wants their questions/doubts captured for later review.
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

## Diagrams
When a concept has structure or motion (memory layout, pointer relationships, a pipeline, state transitions, a request/response exchange), draw it. Follow the Diagrams section of `~/.claude/skills/_shared/style.md`.

## Style
Read `~/.claude/skills/_shared/style.md` before writing and follow it. Specific to this skill:
- Use a heading per concept, short paragraphs and code blocks where they help.
- The page must stand on its own: no need to re-open the original conversation.

## Output
Publish to Notion as described in the Publishing section of the shared style file: draft in `<scratchpad>/<slug>/lesson.md`, push it under the matching Lessons subject page, check it with `ntn pages get`, then delete the scratch folder. If the topic already has a page in Lessons, extend that page instead of creating a duplicate: check with `ntn api v1/search`. Give the user the Notion link.
