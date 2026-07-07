---
name: commit-messages
description: |-
  Write Conventional Commit messages following this team's specific
  standard: header-only, past-tense mood, max 100 chars, optional scope,
  no commit body. Use whenever making a git commit in this repository, and
  whenever asked to write, review, or fix a commit message.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: git
---

## Format

```
<type>(<scope>): <short summary>
```

`(<scope>)` is optional — include it when the change is clearly localized to
one module/package/area (`fix(auth): ...`), omit it when the change is
cross-cutting or the repo doesn't use scopes.

### Types

| type       | use for                                                          |
|------------|-------------------------------------------------------------------|
| `feat`     | a new feature or capability                                       |
| `fix`      | a bug fix                                                         |
| `docs`     | documentation-only changes                                        |
| `style`    | formatting, whitespace, missing semicolons — no logic change      |
| `refactor` | code change that neither fixes a bug nor adds a feature           |
| `perf`     | a change that improves performance                                |
| `test`     | adding or correcting tests                                        |
| `build`    | build system or external dependency changes                       |
| `ci`       | CI configuration/scripts                                          |
| `chore`    | maintenance that doesn't fit the above (tooling, config, cleanup) |
| `revert`   | reverts a previous commit                                         |

If a change touches more than one type's worth of work, split it into
separate commits rather than picking one type to cover everything.

## Rules

- Subject line: max 100 characters total (including `type(scope):`),
  lowercase after the colon, no trailing period, single line — never wrap
  or add a newline in the header.
- Mood: past tense. "added feature", "fixed null check", "removed dead
  code" — not "add feature" / "fix null check".
- The header explains **what** changed, and **why** when the reason isn't
  obvious from the "what" alone (e.g. `fix: handled null response from
  payment gateway to stop checkout crash` beats a bare restatement of the
  diff).
- No commit body. Nothing after the header line — no blank line followed by
  paragraphs, no bullet list of changes.
- Breaking changes: since there's no body to host a `BREAKING CHANGE:`
  explanation, mark them with `!` right after the type/scope —
  `feat(api)!: removed legacy v1 endpoints` — and say what broke in the
  summary itself.
- Issue references: append as a trailing footer line, not prose in the
  header — `Closes #123` or `Refs #123` on its own line directly after the
  header. This is the one addition allowed beyond the header; it is a
  reference, not a body.
- One logical change per commit. Don't bundle unrelated files or multiple
  concerns into a single commit just to save time — see the atomic-commit
  rule this pairs with in `omni`.
- Never write a vague header like `fix: bug fix` or `chore: updates`. The
  summary must be specific enough that `git log --oneline` alone tells a
  reader what happened.

## Examples

```
feat(auth): added OAuth2 login flow

fix(payments): handled null response from payment gateway

refactor(query): extracted query builder into separate module

perf(search): reduced index lookup from O(n) to O(log n)

feat(api)!: removed legacy v1 endpoints

fix(cart): fixed quantity not resetting after checkout
Closes #482
```

## When to use me

Use for every commit made in this repository, and whenever asked to write,
review, or correct a commit message. If an existing commit in the repo
violates this format, don't silently imitate it — follow this standard for
new commits regardless of history.

## What I avoid

- Any text after the header (or header + single footer line).
- Imperative mood ("add", "fix") — this team uses past tense, not the
  common Conventional Commits default.
- Scopes invented for changes that aren't actually localized to one area.
- Combining multiple types of change into one commit to avoid writing two
  headers.
