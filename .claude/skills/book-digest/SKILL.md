---
name: book-digest
description: Condense a technical ebook (EPUB or PDF) one chapter at a time into a markdown digest built mostly from the book's own sentences, with active-recall questions, then push each chapter to a Notion page. Use when the user wants to summarize, condense, digest, or make study notes from a book or ebook, or when continuing a book digest ("next chapter").
---

# Book Digest

Turns a technical book into per-chapter study notes that keep the author's reasoning. Each digest is **continuous prose made of the book's own sentences**: important sentences copied verbatim and woven into coherent paragraphs, joined by short connecting text written by the model. It reads as one discourse, not as a series of quotes. Do not paraphrase what the author already says well. Model-written prose tends to be generic and vague, while the author's sentences carry the precision.

## 0. Before starting: collect inputs

Ask for anything missing and don't start until you have it:
- **Book file path** (EPUB or PDF).
- **Notion page link.** The digests go under this page. Required up front.
- **What the user already knows** about the subject. This sets how each chapter is triaged (step 2).
- Output directory. Default: `./<book-slug>/` next to the book file.

Check how Notion can be reached before doing any work:
1. If Notion MCP tools are available (e.g. `mcp__*notion*`), use them.
2. Otherwise use `scripts/push_notion.py`, which needs `NOTION_TOKEN` set to an internal integration token, with the target page shared with that integration (page `•••` → Connections). If it isn't set, tell the user how to set it up and stop.

## 1. Split the book into chapter files (once per book)

```
uv run ~/.claude/skills/book-digest/scripts/split_book.py <book> <outdir>/chapters [--ranges "1:Intro:1-14,2:Networking:15-48"]
```

- **EPUB**: splits automatically by the table of contents into `chapters/NN-title.md`.
- **PDF**: first run it without `--ranges`. That writes `chapters/_pages.txt` (full text with `=== PAGE n ===` markers). Read the book's table of contents from it, work out the PDF page ranges (printed page numbers are often offset from PDF page numbers, so check a chapter heading), then run it again with `--ranges`.
- Open two or three chapter files and check them: no chapter should be empty, merged with another, or cut in half. Code blocks and tables from PDFs often come out mangled. Note that, and use the file's context to reconstruct code in the digest when you are confident, marking it `[reconstructed]`.

The script also extracts the book's images into `<outdir>/images/` and puts `![alt](../images/name.png)` into the chapter files where each image appears (EPUB) or at the end of its page (PDF). `uv run` installs PyMuPDF automatically from the script's header (uv comes from `mise use -g uv`). PDF images are screenshots of their area on the page, so labels drawn on top of them are included.

Then write `<outdir>/plan.md`: one line per chapter with its triage label (step 2) and a status (`todo` / `done` / `pushed`). This file tracks progress between sessions.

## 2. Triage each chapter

Based on the TOC and what the user knows, give every chapter one label:
- **core**: the reason to read the book, or hard material. Recommend reading the original. The digest still gets made, but it's lighter: a "what to watch for" guide, the key passages, and the questions. It supports the reading instead of replacing it.
- **condense**: background, or partly known. Full digest at about 50–65% of the original length.
- **reference**: API lists, config options, appendices. A short cheat sheet (tables and lists) is enough.

Show the plan to the user and let them change labels before chapter 1.

## 3. Digest ONE chapter

Work on exactly one chapter file per turn. Read the whole chapter file (never work from memory of the book), write the digest, push it, then **stop** and report. Wait for the user to say "next" (or to name a chapter). Never batch several chapters.

### What to keep
- **Every concept, definition, trade-off, caveat, and limitation.**
- **The reasoning.** Keep the "X because Y" and "if you do A, B breaks", not just "use X".
- **The single best example per concept**, preferring the one with code or concrete numbers. Drop the rest.
- **Important sentences verbatim, woven into prose.** This is the default. Copy the author's sentences word for word and place them one after another in ordinary paragraphs, so the section reads as a coherent argument.
  - **No block quotes** (`>`) and **no `[…]`**, even for text taken from the book. To shorten, drop whole sentences; never trim inside one or change its words.
  - Keep the author's first person ("I've seen…", "In my opinion…") as it is; the paragraphs read as the author speaking.
  - Epigraphs and quoted laws (e.g. Conway's law) become a plain sentence: "Conway's law states that organizations which design systems…".
  - Hyphenation from PDF line breaks (`archi‐\ntecture`) is rejoined; that is not a change of words.
- **Code listings** that show a concept, verbatim, in fenced blocks with the language set.

### Images: include most of them
Include most of the chapter's figures in the digest. Diagrams, architecture drawings, screenshots, charts and tables drawn as images usually explain faster than any paragraph.
- **View each image with Read before deciding.** Leave out only decorative ones (logos, icons, author photos, chapter-opening art) and near-duplicates of a figure already included. Mark the dropped ones with `[omitted: figure 3.4, second variant of the same diagram]`.
- **PDF: crop each figure from the page, not from the raw extracted image.** The published figure shows the book's frame, a small white margin, and the caption when it is short:
  ```
  uv run ~/.claude/skills/book-digest/scripts/crop_figures.py <book.pdf> <outdir>/images <first-page> <last-page>
  ```
  Pass the chapter's PDF page range. It writes `images/fig-<chapter>-<n>.png`, named from the caption (`Figure 1-3` / `Figure 3.2` / `Fig. 3-2`), or `fig-p<page>-<i>.png` when no caption is found. It finds the frame even when the book draws it as separate lines, puts the caption inside the image when it is at most 2 lines, and keeps the margin clear of body text above and below. Images whose longer side is under 80pt (icons) are skipped. The script flags `(no frame)` and `(no caption)`; view those crops before using them. View a few of the others too.
- Put the image right after the passage that discusses it. When the caption is inside the image, the markdown caption is just the figure number: `![Figure 3.2](../images/fig-3-2.png)`, so Notion doesn't repeat it. When the caption was left out (too long, or none found), use `![Figure 3.2: <the book's caption, verbatim>](../images/fig-3-2.png)`. If the book has no caption, write a short factual one saying what the figure shows.
- **Diagrams the script missed.** PDFs often draw diagrams as vector graphics, which the script doesn't extract. If the text mentions a figure ("Figure 3.2", "as shown below") and there's no image near it, screenshot the page: `pdftoppm -png -r 144 -f N -l N book.pdf images/pN-full`. View the result, then crop to the figure with `pdftoppm -png -r 144 -f N -l N -x X -y Y -W W -H H -singlefile book.pdf images/pN-fig` (pixel values at 144 dpi). Include the frame, a small white margin and a short caption, as the script does. View the crop to check nothing is cut off. Do the same for PDF code listings or tables that came out as unreadable text.
- **EPUB**: if an image is SVG or another format Notion won't display, convert it to PNG (e.g. `rsvg-convert` or `magick`) and point the digest at the PNG.

### What to cut
- Extra examples of a concept already shown.
- Signposting ("as we'll see in chapter 7", "in this section we will…"), chapter intros and outros that repeat the headings, anecdotes, and marketing tone.
- Restatements. Keep whichever wording of the idea is clearest.
- Remove invented stories, tales, or anedocts about real persons and real companies, skip them or just write the meaning, the moral, or the lesson if it's important

Mark every cut that might matter so the user can go back to the book: `[omitted: two more examples of connection pooling, p. 142]` (page or section).

### Model-written text
Only between the book's sentences: a short phrase or sentence to connect them, define a term the author used earlier, or point out a link to another chapter. It sits in the same paragraph as the copied sentences, so the join reads naturally. If a connecting sentence says nothing the reader needs, delete it. Never summarize a passage you just gave.

### Chapter file format

Write it to `<outdir>/digest/NN-title.md` (the file name keeps the zero-padded `NN` so files sort; the title inside does not):

```markdown
# N. Chapter title

Triage: condense · Source: chapters/NN-title.md · pp. X–Y

## <Section heading from the book>

Verbatim sentence from the book. Another verbatim sentence that follows from it. A short connecting phrase, only if needed, leads into the next verbatim sentence.

A new paragraph of verbatim sentences for the next idea in the section.

![Figure N-M](../images/fig-N-M.png)

[omitted: …]

## 4. Push to Notion

Create one child page per chapter under the user's page, titled `N. Chapter title` (e.g. `1. What Are Microservices?`, never `01.`), with the markdown file as its content.
- MCP: use the Notion tool that creates a page, with the given page as parent.
- Script: `python3 ~/.claude/skills/book-digest/scripts/push_notion.py <notion-page-url> <digest-file.md>`

The images go to Notion too, as image blocks at the same places as in the markdown:
- The script uploads every local `![…](path)` file through the Notion File Upload API and keeps the caption.
- The script centers each image at `IMAGE_WIDTH` (85%) of the page width by placing it in a three-column layout, since Notion's API has no image width setting.
- Headings map directly: `##`→heading 2, `###`→heading 3, `####`→heading 4 (all four render as real Notion headings). The `#` line is the page title.
- With MCP, check whether the tool can upload local files. If it only accepts image URLs, tell the user which images couldn't be pushed rather than dropping them silently.
- Open the page after pushing and check that the images appear.

Then set the chapter to `pushed` in `plan.md`. If the push fails, keep the local file, report the exact error, and don't retry blindly.

## 5. After the last chapter

Offer a one-page map of the whole book (`digest/00-book-map.md`): the main ideas per chapter in one or two lines each, with links between chapters. It's for reviewing months later, not for learning the book from.

## Writing rules for the model-written parts

Apply these to every sentence the model writes (connecting text, questions, answers, "what to watch for"). Sentences copied from the book stay as they are.

- Plain, simple language. Write for the user coming back to these notes because they forgot the material.
- Every sentence teaches something. No filler, and no restating the heading.
- No meta-commentary about the digest itself or the process ("this chapter covers…", "the author then explains…"). State the content directly.

### Avoid these traps
1. Metadiscourse (significance-announcing). The sentence's job is to tell you the next sentence matters, rather than just saying the thing. "X is worth stating plainly," "That is not a detail," "Y deserves a mention of its own." Diagnostic: delete it and no information is lost. This is the largest category and the most characteristic.
2. Aphoristic antithesis. The two-beat epigram, usually closing a paragraph: "not X. It is Y", "A does not disappear; it moves." One short punchy sentence after a long one, landing like a drumbeat. In moderation it's good prose; four per page reads as a machine that has learned cadence without having anything to be emphatic about.
3. Text self-narration. Prose describing the document's own rhetorical behaviour instead of the subject: "Chapter 9 states this before it states any result," "Chapter 6 is largely an argument about when it must be invoked."
4. Enumerated essence. "Two habits separate a model check from an ornament." A count plus an evaluative noun, presented as a discovered taxonomy. (Contrast "The protocol has two steps" — a count of actual countable things, which is fine.)
5. Connoisseur diction. Words that rate rather than describe: ornament, repays attention, worth holding onto, the interesting one, the awkward case. They position the author as a judge of the material.
Cutting across all five: unearned confidence — superlatives and totalising claims with nothing behind them ("the single largest reason a local filesystem feels fast").
6. Gnomic generalisations — the aphoristic maxim, or sententia in classical rhetoric: a timeless, subject-less, present-tense proposition offered as a general law rather than a claim about your system. Two markers make them detectable: an indefinite or universal subject ("A negative result…", "A checker never observed to fail…"), and a present-tense copula with no citation, no measurement, and no attachment to anything in the chapter. Related to the antithesis pattern, but distinct — antithesis is about shape, this is about epistemic posture. The register is the lecturer stating a principle rather than the author reporting work.
7. Consensus-appeal tag — a booster that props a claim up with imagined agreement ("nobody disputes it", "everyone agrees", "uncontroversially") instead of with evidence. It's dead weight when the evidence has just been given; appealing to unnamed consensus on top of it weakens rather than strengthens.

### Avoid counterfactual self-reference
An irrealis variant of text self-narration, with three things stacked in it:
1. Irrealis mood about the document itself: the text imagining an alternate version of itself that was never written ("these notes would be short if…").
2. Authorial persona intrusion: a wink at the reader that smuggles a speaker into an impersonal register without using "I".
3. Stakes-boosting: telling the reader the coming point is important instead of letting the content establish it.
