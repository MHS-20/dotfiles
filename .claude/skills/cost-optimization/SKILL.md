---
name: optimize-usage
description: |-
  Recommend the cheapest model/effort combination (deepseek-flash or deepseek-pro,
  effort low/medium/high) that will still get a task right on the first try.
  Use proactively before starting any new task that has not been pinned to a
  model, and whenever the user asks "which model should I use" or "how much
  effort does this need".
license: MIT
compatibility: opencode
metadata:
  models:
    - deepseek-flash
    - deepseek-pro
  audience: developers
---

## What I do

Given a task description, I pick one model (`deepseek-flash` or `deepseek-pro`)
and one effort level (`low`, `medium`, `high`) — the cheapest combination that
will still succeed on the first attempt. A retry after under-provisioning costs
more than over-provisioning once, so ties round up a tier.

## Decision procedure

Answer in order, stop at the first match:

1. Does the task require holding more than ~3 files of context at once, or
   reasoning about interactions between subsystems (e.g. "why does X break Y")?
   → `deepseek-pro`, effort `high`.
2. Is it a refactor, bug fix, or feature touching 2-5 files with clear existing
   patterns to follow? → `deepseek-pro`, effort `medium`.
3. Is it single-file, mechanical, or has an unambiguous spec (rename,
   boilerplate, CRUD endpoint, test for an existing pattern, formatting/typing
   fixes)? → `deepseek-flash`, effort `low`.
4. Is it a one-line change, a lookup, or a question about code already in
   context? → `deepseek-flash`, effort `low`.

## Escalation rule

If `deepseek-flash` output fails tests, contradicts existing codebase
conventions, or needs a second correction pass, stop iterating on `flash` and
re-run the same task on `deepseek-pro` instead. Report the escalation in one
sentence, e.g. "flash struggled with X, retrying on pro."

## When to use me

Use before kicking off any task that hasn't already been assigned a model, or
whenever explicitly asked to recommend one. Do not use for tasks already
mid-flight on a chosen model unless they've just failed (see escalation rule).

## Output format

```
model: <deepseek-flash|deepseek-pro>
effort: <low|medium|high>
why: <one sentence>
```

Always commit to one recommendation — never answer "it depends" as the final
word. Mention a runner-up only if it's genuinely close.
