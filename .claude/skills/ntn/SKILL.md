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
