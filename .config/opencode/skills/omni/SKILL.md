---
name: omni
description: |-
  Standing background conventions for every coding session, active
  regardless of which other skill is in use: header-only Conventional
  Commits with small/frequent commits, code quality judged by elegance,
  simplicity, and SOLID principles, keeping the user informed with plans
  and milestones, updating existing documentation in place alongside
  behavior changes, and never guessing a fact that can be looked up. Always
  applies during coding tasks.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  scope: always-on
---

## What I do

Bundle five conventions that apply to nearly every coding task, so they don't
need to be repeated per-skill.

## Commits

- Use Conventional Commits format for the header only: `type(scope): subject`.
  No commit body.
- Commit small and often: one logical change per commit. Don't bundle a
  refactor with a feature, and don't bundle multiple unrelated files into one
  commit. If a task naturally splits into steps, commit after each step
  rather than at the end.

## Code quality

- Favor elegance and simplicity: the simplest design that correctly solves
  the problem, not the cleverest one. If a change can be expressed with less
  code or fewer moving parts without losing clarity, prefer that version.
- Apply SOLID principles where they genuinely fit the codebase's existing
  paradigm — single responsibility, open/closed, Liskov substitution,
  interface segregation, dependency inversion — but don't force them onto a
  small script or a codebase that isn't organized that way. Judgment over
  dogma.
- Match the existing style/lint configuration exactly.
- Run the repo's linter, formatter, and type-checker before considering a
  change done — don't just eyeball it.
- Prefer the smallest correct diff over a broader rewrite unless a refactor
  was explicitly requested.

## Keep the user informed

- Before a multi-step or long-running task, state the plan in 2-4 bullet
  points.
- During execution, report at each meaningful milestone (not every file
  edit): what was done, what's next.
- Flag blockers immediately rather than silently working around them.

## Documentation corpus

- Whenever a change alters behavior, a public API, config, or setup steps,
  update the existing documentation that covers it, in the same commit as
  the code change — not as an afterthought.
- Update in place: find the doc(s) already describing the affected behavior
  and revise them. Don't propose new filenames, new doc files, or a
  changelog entry — work within whatever documentation structure the repo
  already has.

## Never guess

- If a fact needed to proceed (a file's contents, a function's signature, an
  env var's value, an external API's behavior) isn't already known with
  certainty, look it up: read the file, grep the repo, check the docs.
- If it truly can't be determined, stop and ask the user rather than
  proceeding on an assumption.
- State assumptions explicitly whenever one is unavoidable.

## When to use me

Always active during coding sessions in this repository, in addition to
whatever other skill is in use for the specific task at hand.
