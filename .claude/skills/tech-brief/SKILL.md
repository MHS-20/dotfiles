---
name: tech-brief
description: Research a tech topic (protocol, system, algorithm, standard, tool — e.g. OpenID Connect, Raft, TLS 1.3) from primary web sources and local books, and write a sourced lesson explaining how it works and why it is built that way, with drawn and sourced diagrams, published to the user's Notion Lessons knowledge base. Use when asked to research, study, explain in depth, or write a guide/brief/lesson on a tech topic.
---

# Tech Brief

One researched lesson per topic, published to the Notion **Lessons** knowledge base. It is the counterpart of `lesson-learned`: that skill captures what the user learned by doing, this one researches what the user asks about. The reader is the user, coming back months later to re-learn the topic. Depth means real messages, data structures and failure cases, not length. Every claim comes from a source read in this session.

Read `~/.claude/skills/_shared/style.md` first. It defines the prose rules, publishing (Notion only, nothing local) and how to draw diagrams.

## 0. Inputs
Ask only for what is missing: the topic and its boundary, and what the user already knows (skip that material). The parent is the matching subject page under Lessons. Before writing, check that the topic doesn't already have a page (`ntn api v1/search`). If it does, extend or rewrite that page instead of creating a second one.

Working files (`questions.md`, `sources.md`, `notes.md`, `images/`, `fig/`, `guide.md`) go in `<scratchpad>/<slug>/` only.

## 1. Questions first
Write `questions.md` with 15–30 questions someone needs answered to understand how the topic works, in three tiers:
- **core**: what it is, the problem it solves, the main flow.
- **mechanism**: why each step exists and what fails without it.
- **design**: trade-offs, attacks, limits, alternatives.

Leave out how-to-use and configuration questions. Don't ask the user to approve the list. The questions define the scope: material that answers none of them stays out, and research stops once each one has a sourced answer.

**Split check.** If the questions span more than one lesson (over ~30, or clearly separable parts such as OAuth 2.0 core vs. OIDC on top), propose a split into sub-topics and ask the user before writing. Each sub-topic gets its own page.

## 2. Sources
List them in `sources.md`, in this priority order:
1. **Authoritative sources**: the spec, RFC, original paper, official docs or source code.
2. **Books** in `~/Documents/Books` (see its `CLAUDE.md`):
   - Find them by title with `find ~/Documents/Books -iname '*.pdf' | grep -iE '<kw>'`.
   - Read the TOC with `pdftotext -l 20`, then the relevant chapter with `pdftotext -f A -l B -layout`.
   - If a book you know of would cover the topic and it isn't there, name the book and the chapter and ask the user to get it. Keep working in the meantime.
3. **At most 3 secondary sources** (vendor engineering docs, OWASP/PortSwigger, a known practitioner). Use them for diagrams and pitfalls, never for normative claims. Skip SEO tutorials and listicles.

Read specs one section at a time and record section numbers.

## 3. Notes
In `notes.md`, organised per question, record:
- short verbatim extracts with their section or page;
- concrete artefacts: messages, data structures, defaults, numbers.

Mark anything without a source `TODO-source`. Such claims never reach the page. A question is done once it has a primary or book source and one artefact.

## 4. Figures
Every page whose topic has structure or motion gets at least one figure that shows the main mechanism. Figures come from two places.

**Drawn (TikZ)**, following the shared style file. This is the default when the mechanism is a flow, a layout, a key chain or a comparison.
- Draw from `notes.md`, never from memory. Every box and arrow must match a source.

**Screenshotted from a source**, when the source already has a clear diagram:
```
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --list
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --pick 2,5 --name <slug>
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --selector "<css>" --name <slug>
```
For PDFs, use `pdftoppm -png -r 144 -f N -l N [-x -y -W -H]`.

For both kinds: view every image with Read and drop blank, decorative or inaccurate ones. Caption each figure with what it shows (credit goes in the Sources list) and place it next to the text that walks through it.

## 5. The lesson (`guide.md`)
The lesson explains **how the thing works and why it is built that way**: the ideas, the trust model, the design decisions and what breaks without them. It is not a usage or configuration guide. Leave out endpoint paths, parameter catalogues, error codes, library/config advice and operational how-tos, unless one is the mechanism being explained.

Open with one or two sentences that say what the topic is, then use headings per concept. The order below fits most topics. Skip, merge or rename sections when the topic calls for it (an algorithm has no "parties").
1. **Problem**: what was broken before, concretely, and what the design has to achieve.
2. **Core idea**: the one or two insights the design rests on, in plain words.
3. **Model**: the parties, what each one knows or holds, and whom each trusts for what.
4. **How it works**: the mechanism step by step. Each step says what it achieves and what fails without it. Show at most one compact real message or data structure per idea, and only where seeing it makes the idea clearer.
5. **Design decisions**: the possible alternatives, why this one was chosen, and what it costs.
6. **Where it breaks**: attacks and limits, each explained by the assumption it violates.
7. **Relation to neighbours**: what problem each neighbouring design solves differently.
8. **Sources**.

No citations in the text or in figure captions, and no source list in the opening. The only place sources appear is the **Sources** list at the end, with section or page numbers (`RFC 7636 §4.4`, `*Book*, p. 214`) and the origin of each figure.

Rules:
- Explain each component by its purpose: what problem it solves, and what goes wrong without it.
- Every "why" names a concrete failure. Not "PKCE improves security" but "without PKCE, an app that registered the same redirect scheme can intercept the code and redeem it".
- Every non-obvious mechanism gets a small worked example with concrete values, taken from the spec where possible.
- Use exact names where a name matters for the idea (`aud`, `nonce`, `state`), but no field lists for their own sake.
- No history, ecosystem lists or "benefits" sections unless a question needs them.
- No interview framing: no elevator pitches and no "how to answer" sections.

## 6. Verify
Check that:
- every claim traces to `notes.md` and no `TODO-source` remains;
- example values match their sources;
- every question is answered in the page;
- every image has been viewed, credited and referenced;
- no banned pattern from the shared style file remains.

## 7. Publish and report
```
python3 ~/.claude/skills/tech-brief/scripts/push.py <subject-page-id> "<Topic>" <scratchpad>/<slug>/guide.md
```
Then run `ntn pages get <id> </dev/null`, check that the text and images arrived, and delete `<scratchpad>/<slug>/`. If the push fails, report the error and don't retry blindly.

Tell the user the Notion link, which questions are thin and why, and which book would deepen them.
