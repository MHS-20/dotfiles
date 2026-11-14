---
name: tech-brief
description: Research a tech topic (protocol, system, algorithm, standard, tool — e.g. OpenID Connect, Raft, TLS 1.3) from primary web sources and local books, and write a concrete, sourced guide deep enough to explain it in a technical interview, with figures screenshotted from the sources. Use when asked to research, study, write a guide/brief on, or prepare for an interview on a tech topic.
---

# Tech Brief

One guide per topic. Depth means real messages, field names and failure cases, not length. Every claim comes from a source read in this session.

## 0. Inputs
Ask for whatever is missing: the topic and its boundary, the interview target (backend, security, system design…), what the user already knows (skip that material), and the **Notion parent page** link.

No local copies. All working files (`questions.md`, `sources.md`, `notes.md`, `images/`, `guide.md`) go in `<scratchpad>/<slug>/`; the deliverable is the Notion page.

## 1. Questions first
Write `questions.md` with 15–30 questions an interviewer would ask about how the topic works, in three tiers: **core** (what it is, the problem it solves, the main flow), **mechanism** (why each step exists, what fails without it), **senior** (design trade-offs, attacks, alternatives). No how-to-use or configuration questions. Don't ask the user to approve them. These questions define the scope: material that answers none of them stays out, and research stops once each one has a sourced answer.

**Split check.** If the questions span more than one guide's worth (over ~30, or clearly separable parts such as OAuth 2.0 core vs. OIDC on top), propose a split into sub-topics and ask the user before writing anything. Each sub-topic becomes its own page.

## 2. Sources
List them in `sources.md`. Priority order:
1. The spec, RFC, original paper, official docs or source code. These are the authority.
2. Books in `~/Documents/Books` (see its `CLAUDE.md`). Find by title with `find ~/Documents/Books -iname '*.pdf' | grep -iE '<kw>'`, read the TOC with `pdftotext -l 20`, then read the relevant chapter with `pdftotext -f A -l B -layout`. If a book you know of would cover the topic and it isn't there, name the book and the chapter and ask the user to retrieve it. Carry on in the meantime.
3. At most 3 secondary sources (vendor engineering docs, OWASP/PortSwigger, a known practitioner). Use them for diagrams and pitfalls, never for normative claims. Skip SEO tutorials and listicles.

Read specs one section at a time and record section numbers.

## 3. Notes
In `notes.md`, organised per question: short verbatim extracts with section or page, plus concrete artefacts (HTTP requests and responses, JSON, claims, defaults, numbers). Mark anything without a source `TODO-source`. Such claims never reach the guide. A question is done once it has a primary or book source and one artefact.

## 4. Figures
```
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --list
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --pick 2,5 --name <slug>
uv run ~/.claude/skills/tech-brief/scripts/shot.py <url> <scratchpad>/<slug>/images --selector "<css>" --name <slug>
```
For PDFs, use `pdftoppm -png -r 144 -f N -l N [-x -y -W -H]`. View every image with Read. Drop blank, decorative or inaccurate ones. Prefer sequence or layout diagrams. Caption each one with its source and place it beside the text that walks through it. If no source figure shows a page's main mechanism, draw one (below). Otherwise don't.

**Drawn diagrams (TikZ).** Only for a structure, flow or comparison that is central to the page and that no source draws (e.g. key chains of several products side by side, which channel each protocol step uses). At most 1–2 per page, one idea each.
- Draw from `notes.md`, never from memory. Every box and arrow must match a source, and the caption cites those sources.
- Short labels only, no sentences inside the figure. Use numbered steps when order matters.
- `\documentclass[tikz,border=6pt]{standalone}` in `<scratchpad>/<slug>/fig/<name>.tex`, then `tectonic <name>.tex && pdftoppm -png -r 200 -singlefile <name>.pdf <name>`.
- View the PNG with Read and fix overlaps or clipping before using it.
- To add a figure to a page that's already pushed, use `scripts/insert_image.py <page-id> "<text of the block to insert after>" <png> "<caption>"`. That keeps the page's link.

## 5. Guide (`guide.md`)
The guide explains **how the thing works and why it is built that way**: the ideas, the trust model, the design decisions and what breaks without them. It is not a usage or configuration guide. Leave out endpoint paths, parameter catalogues, error codes, library/config advice and operational how-tos, unless one is the mechanism being explained.

Sections (skip any that don't apply):
1. **Problem**: what was broken before, concretely, and what the design has to achieve.
2. **Core idea**: the one or two insights the design rests on, in plain words.
3. **Model**: the parties, what each one knows or holds, and whom each trusts for what.
4. **How it works**: the mechanism step by step. Each step says what it achieves and what fails without it. Show at most one compact real message or data structure per idea, and only where seeing it makes the idea clearer.
5. **Design decisions**: the alternatives that were possible, why this one was chosen, and what it costs.
6. **Where it breaks**: attacks and limits, explained by the assumption each one violates.
7. **Relation to neighbours**: what problem each one solves differently.
8. **Interview answers**: a 30-second and a 2-minute explanation, then 3–6 sentences per question.
9. **Sources**.

Cite inline: `(RFC 7636 §4.4)`, `(*Book*, p. 214)`, `([site](url))`.

Rules:
- Explain mechanisms by their purpose. For each component: what problem it solves, what an attacker could do without it.
- Every non-obvious mechanism gets a small worked example with concrete values (from the spec where possible).
- Every "why" names a concrete failure. Not "PKCE improves security" but "without PKCE, an app that registered the same redirect scheme can intercept the code and redeem it (RFC 7636 §1)".
- Exact names where a name matters for the idea (`aud`, `nonce`, `state`), but no lists of fields for their own sake.
- No history, ecosystem lists or "benefits" sections unless a question needs them.
- Plain language, short paragraphs, tables for comparisons. Cut any sentence that can be deleted without losing information. Banned: metadiscourse ("it's worth noting", "the key insight"), self-narration ("this section covers"), drumbeat antitheses ("not X — it's Y"), invented taxonomies ("three pillars"), rating words and intensifiers (elegant, crucial, robust), maxims with nothing attached, appeals to consensus, verdict tails, and uniform hedging (state sourced claims flatly; when you hedge, give the reason).

## 6. Verify
Check that every claim traces to `notes.md` and no `TODO-source` remains, that example values match their sources, that every question is answered, and that every image has been viewed, credited and referenced.

## 7. Push and report
```
python3 ~/.claude/skills/tech-brief/scripts/push.py <parent-id> "<Topic>" <scratchpad>/<slug>/guide.md
```
This creates a child page under the parent and uploads the images in place (with `ntn`; see the `ntn` skill). For split topics, create one page per sub-topic. Then `ntn pages get <id> </dev/null` and check that the content and images arrived. If the push fails, report the error. Don't retry blindly.

Tell the user the Notion link, which questions are thin and why, and which book would deepen them.
