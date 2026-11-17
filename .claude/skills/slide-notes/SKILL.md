---
name: slide-notes
description: Turn university lecture slide decks (PDF) into structured study notes on Notion, one sub-page per deck/topic, with prose, nested bullets, examples, tables and cropped screenshots of diagrams. Use when the user asks to write summaries, lecture notes, or "appunti" from slides/PDFs in a course folder (e.g. ~/Unibo/...) into a Notion course page.
---

# Slide decks → Notion lecture notes

## Goal
For each slide deck that has no notes yet, create one Notion sub-page under the course page, so the course page covers all the material. Notes should be useful for studying: they are a condensed version of the slides, not a transcription.

## 1. Scope the work
- List the course folder (`find <dir> -type f`). Get page counts with `pdfinfo`.
- Find the Notion course page (the user's link, or `notion-search`). Fetch it and list its existing child pages. **Skip decks that already have a page**; tell the user which ones you assumed were already covered.
- Skip by default: exercise decks and solutions ("Esercitazioni", "autoVal", exam tests), the course-presentation deck, and schemas or datasets with no content. Lab decks count as content: summarize the concepts and worked examples, not the exercise prompts.
- Fetch one existing sibling page and copy its **language** (Italian notes stay Italian) and tone.
- State the plan (which pages, which decks) before writing.

## 2. Read the decks
```bash
pdftotext -layout deck.pdf - | awk 'BEGIN{p=1} /\f/{p++; print "--- p" p} {gsub(/ {2,}/," "); if($0!~/^ *$/) print}' > deck.c
```
- The page markers (`--- pN`) map text to PDF pages, which you need for screenshots.
- Some decks put 2 slides on each PDF page (handout layout). Check one rendered page before you crop.
- Large files: read them in parts. Drop exercise lines with grep before reading.

## 3. Screenshots: diagrams only
- Screenshot **only diagrams, figures, charts, architecture drawings, or important visual tables**. Never screenshot a slide that is mostly text or code: write that content as markdown instead.
- Render candidates at low dpi and review several at once:
  `pdftoppm -png -r 60 -f N -l N -singlefile deck.pdf out` and then `magick montage a.png b.png -tile 3x2 -geometry +4+4 mont.png` (view it with Read).
- **Crop to the figure** at high dpi with `pdftoppm -r 150..200 -x X -y Y -W W -H H`, adding a **generous margin** (about 10px at 40 dpi, i.e. ~3% of the slide, on every side) so nothing on the border gets cut. Coordinates are in pixels at that dpi, so a coordinate measured at 60 dpi scales by 200/60. Check the crops in a montage before uploading.
- Aim for about 2–10 images per page. A deck with no real diagrams gets no images.
- Upload: call `notion-create-file-upload` with the filename, then
  `curl -s -X POST "<upload_url>" -H "authorization: Bearer <token>" -F "file=@img.png"` → status `uploaded`.
  Several create-file-upload calls can run in parallel; do the curls in one Bash call. Upload URLs expire after about an hour, so upload right after creating them.
- Embed with `<image source="file-upload://<id>" />`.

## 4. Writing format
- **Headings: use `##` (H2) for the main numbered sections and `###` (H3) for subsections. Avoid `#` (H1). Never use a bold-only line as a title**: if a line would be a bold label on its own line, make it an H3. Bold inside a sentence is fine.
- Mix short **prose paragraphs** (context, why something matters) with **bullets and sub-bullets** (properties, pros/cons, lists).
- Use ✅ / ❌ for advantages and drawbacks, ⚠️ for common pitfalls.
- Use **tables** for comparisons (A vs B, cardinalities, tools).
- Put **examples** in code blocks with a language (`sql`, `javascript`, `json`), labelled *Esempio* / *Example*. Keep the slides' own examples; leave out exercises and their solutions.
- Condense: remove repetition, slide boilerplate, author/page footers and resource URLs. Don't add "[omessi]" / "omitted" markers.
- Base everything on the slides; don't add facts that aren't in them.
- End with a 1-line reading reference if the deck gives one.

## 5. Create and fix pages
- Create pages with `notion-create-pages` (parent = course page, `allow_async: false`), one per deck. Put the title in properties, not in the content.
- Small fixes: `notion-update-page` `update_content` with old_str copied from the **fetched** form (headings look like `### <b>Title</b>`, bold looks like `<b>x</b>`).
- **Image blocks can't be matched by update_content.** To remove or replace an image, fetch the page and `replace_content` the whole body, keeping the existing `notion-file-block://...` sources verbatim and adding `file-upload://` for new images.

## 6. Report
Give a table of the pages created (link, source deck, which diagrams are included) and list what was skipped and why, including any decks you assumed were already covered.
