---
name: ntn
description: Read and write the user's Notion workspace with the `ntn` CLI (pages get/create/edit, raw API calls, search, recursive page-tree dumps). Use whenever a task reads from or writes to Notion, a notion.so / app.notion.com link is given, or the user mentions their Notion notes.
---

# Using the `ntn` Notion CLI

## Hard rules
- **Never feed content through stdin.** `ntn` hangs on stdin. Always add `</dev/null` to every call and pass content with `--content=...`.
- **Use the `=` form: `--content="$(cat file.md)"`.** With a space (`--content "$(...)"`), content that starts with `---` (frontmatter) is parsed as a flag and the call fails with `unexpected argument`.
- Wrap calls in `timeout 60`–`120`.
- **`pages edit` replaces the whole page body.** Before editing, `get` the page. If it has child pages (`<page url=...>` lines), either keep those lines in the new content or create a child page instead (`--allow-deleting-content` is needed to drop them).

## IDs
A URL `https://app.notion.com/p/<workspace>/<Title-Slug>-<32hex>` → the page ID is the trailing 32-hex string. Dashed UUIDs also work.

## Commands
```bash
ntn pages get <id> </dev/null                        # Markdown + frontmatter (title)
ntn pages get <id> --json </dev/null                 # when the output is truncated
ntn pages edit <id> --content="$(cat f.md)" </dev/null
ntn pages create --parent page:<id> --content="$(printf -- '---\ntitle: T\n---\n'; cat f.md)" --plain </dev/null   # prints the new id
ntn api v1/blocks/<id>/children </dev/null           # raw blocks
ntn api v1/pages/<id> </dev/null                     # properties + parent
ntn api v1/search -X POST -d '{"query":"x","page_size":20}' </dev/null
```
Child pages appear in `get` output as `<page url="https://app.notion.com/p/<32hex>">Title</page>`.

## Recipes
- **Find where notes live**: search, then follow `parent.page_id` upward with `v1/pages/<id>`. Empty `results: []` from `blocks/children` means the page really is empty.
- **Dump a page tree**: recurse on the `<page url=...([0-9a-f]{32})">` matches with a small Python script (`subprocess.run([...], stdin=DEVNULL, timeout=120)`). Run independent trees in parallel. Write the dumps to the scratchpad.
- **Shrink a dump before reading**: remove image tags, long URLs, `<empty-block/>`, `<span ...>` tags and `~~strikethrough~~` with `sed`. That cuts the size by about 2–4×. Then list `title:` / `##` lines to map the structure, and read only the condensed sections.
- Markdown written with `edit`/`create` supports headings, nested lists, bold/italic and code blocks.

## Page font (Serif/Mono)
The public API cannot set a page's font. Generate a console script instead; it finds the pages itself, so no IDs are listed:
```bash
python3 -I ~/.claude/skills/ntn/scripts/page_font_js.py serif [<root-page-id-or-url>] [out.js]   # or default|mono
```
The JS walks the tree in the browser from the root (or, with no root, from the page open in that tab) through Notion's internal web API (`/api/v3/syncRecordValues`, following each block's `content`, sub-pages nested in toggles/columns included, databases skipped), then sets `format.page_font` with `saveTransactions`, skipping pages that already have the font. The user runs it: notion.so → F12 → Console → type `allow pasting` by hand → paste → Enter → reload. `DRY_RUN = true` in the file only lists what would change. Unofficial API: if it returns non-2xx, the format changed. The ID-listing version was verified on 2026-11-14 (290 pages); the self-walking version was not yet run by the user.

## Icons
`ntn api v1/pages/<id> -X PATCH -d '{"icon":{"type":"emoji","emoji":"📐"}}' </dev/null` (`{"icon":null}` removes it; `"cover"` works the same way).

## Block-level scripts (`~/.claude/skills/ntn/scripts/`)
Run with `python3 -I <script>`; each prints its usage when called without arguments. They wrap `ntn api` (stdin closed, timeouts set) for edits that `pages edit` (whole-page replace) and the MCP's `update_content` (fails on inline code and escaped quotes) handle badly. Prefer `--dry-run` first on pages you care about.

| Script | Does |
|---|---|
| `blocks.py <page>` | lists top-level blocks: `id type \| heading it falls under` |
| `replace_text.py <page> '[["old","new"],…]' [--regex] [--top-only] [--dry-run]` | find-and-replace in all blocks, nested blocks and table cells, keeping bold/code/links around the edit |
| `keep_headings.py <page> '<regex>' [--dry-run]` | deletes every top-level block not under a matching heading (`\(top\)` = before the first heading) |
| `merge_blocks.py <src> '<heading regex>' <target> [--out-dir D] [--dry-run]` | appends the blocks under matching headings (with nested children) to the end of target |
| `wait_populated.py <page> [timeout]` | waits until a `notion-duplicate-page` copy is readable |
| `reorder_children.py <parent> <spec> [--dry-run]` | puts child pages in a given order under given headings, via a temp page it trashes afterwards |

Recipes:
- **Split a page into parts**: `notion-duplicate-page` once per part, *one at a time* (`wait_populated.py` between them; concurrent duplicates of one page can leave an empty stub), then `keep_headings.py` on each copy, then set each title with `PATCH v1/pages/<id>` (the MCP's `properties` inside `update_content` is ignored). Existing text is never re-typed.
- **Append Markdown to an existing page** without `pages edit`: `ntn pages create` a scratch page with the new content, `merge_blocks.py <scratch> '<heading regex>' <target>`, then trash the scratch page.
- **Images**: the API cannot copy or create uploaded images, and `ntn files create` fails on the free plan. `merge_blocks.py` turns images into `IMGPLACEHOLDERn` paragraphs (downloading hosted ones to `imgN.png`). `ntn pages create` turns `![caption](X)` into an image with an empty URL, shown by the MCP's fetch as `<image>` followed by the caption. To attach a file: `notion-create-file-upload` (MCP) → `curl -X POST <upload_url> -H 'authorization: …' -F file=@fig.png` → `notion-update-page` `update_content` replacing `<image>\n<caption text start>` (or the placeholder paragraph) with `<image source="file-upload://<id>">…`. Escape underscores in `old_str` as `\_`.
- **New page with a title**: `ntn pages create` *without* frontmatter (frontmatter ends up as body blocks and leaves the title empty), then `ntn api v1/pages/<id> -X PATCH -d '{"properties":{"title":{"title":[{"text":{"content":"T"}}]}}}'`.
- **Delete a block**: `ntn api v1/blocks/<id> -X DELETE </dev/null`. Deleting a heading leaves the paragraphs after it; deleting a toggle removes its content. **Trash a page**: `PATCH v1/pages/<id>` with `{"in_trash": true}`.
