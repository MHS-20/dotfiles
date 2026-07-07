---
name: documentation-corpus
description: "Apply whenever a feature or fix is added and confirmed working, and whenever documentation is requested. Maintains a complete set of project documentation and keeps it in sync with the codebase: update the relevant docs in the same change as a verified fix or feature, never document unverified behavior as working, and fix stale docs encountered along the way even if unasked."
---

# Documentation Corpus

## When this applies

Any time you finish a feature or fix, any time you're asked to write or update documentation, and any time you notice existing docs are wrong while working on something else.

## Why this exists

Documentation describing old behavior is worse than no documentation — it actively misleads. This skill's job is to keep the docs both complete and true, not just present.

## The corpus

Maintain, and create if missing, a documentation set shaped like this. If the project already has its own docs layout or wiki, use that instead of imposing a second, competing structure — ask if it's genuinely unclear which one is authoritative (see never-guess).

```
docs/
  README.md       - index: what exists, and where to find it
  architecture.md - how the system fits together, major components, data flow
  setup.md        - how to install, run, and configure the project from zero
  api/            - one file per module or service, or a single api.md for small projects
  decisions/      - architecture decision records (ADRs), one file per significant decision
  changelog.md    - human-readable list of notable changes, newest first
```

## The core rule: docs move with verified code

- When you finish a change and have verified it works — tests pass, or you've manually confirmed the behavior — update the relevant doc(s) in that same change, not "later."
- Never document a fix or feature as complete or working before it's verified. If you need to write something down before verification, mark it clearly as a draft or TODO, and finalize it once confirmed.
- If a change makes an existing doc statement false, correct that statement directly — don't leave it standing and add a new, contradicting statement elsewhere.

## What to write, by change type

- **New feature** — what it does, how to use it (with an example), where it lives, any new config or environment variables.
- **Bug fix** — if the bug was documented behavior, correct that doc; if it reveals a gap that was never documented, add it. Add a changelog line either way.
- **Architecture-affecting change** (new service, new dependency, changed data flow) — update architecture.md, and add an ADR if the change involved a real trade-off. Add the ADR even if the choice seems obvious in hindsight; the point is recording *why*, for whoever reads it next.
- **Any decision made between multiple valid approaches** — write a short ADR: context, options considered, the choice, and why. This turns a one-time decision into a permanent record instead of something only mentioned once in a status update.

## Quality bar

- A short, correct doc beats a long, stale one.
- Every code example in the docs should actually run against the current code. If you change a signature, find and fix every example that calls it.
- Write for someone with no memory of this conversation — don't say "as discussed" or "as just changed"; say what the thing does now.
- Explain intent and usage, not a restatement of the code line by line — the same "why, not what" rule that applies to good comments applies here.

## Periodic audit

If you're working near docs that are wrong, outdated, or missing, fix them as part of the task and mention it in your status update, even if nobody asked. Treat stale docs you happen to encounter as a bug, not a footnote.

## Related skills

- **status-updates** — mention doc updates in your end-of-task summary.
- **never-guess** — don't document behavior you haven't actually verified.
- **code-review** — a review that changes behavior should trigger a documentation check.
