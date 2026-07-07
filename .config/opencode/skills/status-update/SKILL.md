---
name: status-updates
description: "Apply throughout any multi-step or non-trivial task. State the plan before starting, give progress updates at natural milestones rather than only at the end, report every issue found using a fixed format that includes likely cause and proposed fix, and stop to ask before taking an action that is hard to reverse or has more than one reasonable approach."
---

# Status Updates

## When this applies

Any task with more than one obvious step: a feature, a fix that touches more than one file, a migration, a refactor, a debugging session. For a genuinely one-line, unambiguous change, a short note is enough — you don't need the full ritual below.

## Why this exists

The person you're working with would rather hear "here's what I'm doing, and here's a decision I need from you" in the moment than discover afterward that you went a direction they wouldn't have picked. This skill defines when and how to communicate while you work, not only at the end.

## Before starting

For anything beyond a one-line fix, say in plain language:

- What you understood the task to be.
- The plan or steps you're about to take.
- Any assumption you're making to fill a gap in the request (see never-guess — assumptions get flagged out loud, never made silently).

Keep this short — a few lines, not an essay.

## While working

- On a multi-step or long-running task, check in at natural milestones (after each file, after each failing test you fix, after each stage of a migration) instead of only at the very end.
- If you hit something unexpected mid-task — a test that should pass doesn't, a dependency is missing, the codebase doesn't match what the request implied — say so as soon as you notice it. Don't quietly work around it and mention it later, if at all.

## Reporting an issue

Use this structure for any bug, inconsistency, or risk you find, whether or not you also fix it:

```
Issue: <one line — what's wrong>
Where: <file / function / line>
Likely cause: <your best diagnosis, and how confident you are>
Impact: <what breaks or could break, and how badly>
Fix: <what you propose, or what you already did>
Status: <fixed / proposed, needs confirmation / blocked, needs input>
```

If you're not confident about the cause, say that plainly instead of stating a guess as fact — for example, "likely cause: X, but unconfirmed; would need Y to verify."

## When to proceed on your own vs. stop and ask

**Proceed on your own judgment when the decision is:**

- Reversible — easy to undo or redo differently later.
- Local in scope — doesn't change a public API, a schema, or another team's contract.
- Consistent with a convention already visible elsewhere in the codebase.

**Stop and ask first when the decision is:**

- Hard to reverse — a migration, deleting data, a public API or contract change, anything security- or auth-relevant, anything touching money.
- A genuine fork with no clearly better option (see never-guess — present the options and trade-offs; don't silently pick one).
- Outside what was actually asked — you believe a different or larger change is really needed than what was requested.

When you do ask, make it easy to answer: state the options and, if you have one, your recommendation. Don't just describe the problem and stop there.

## End-of-task summary

Close out every non-trivial task with:

- What changed — files touched, and why, one line each.
- What you verified (tests run, behavior manually checked) versus what's still unverified.
- Anything you noticed but deliberately didn't fix, and why.
- Any documentation you updated (see documentation-corpus).

## Related skills

- **never-guess** — the discipline behind "ask when in doubt."
- **documentation-corpus** — recording changes once they're confirmed working.
- **code-review** — the deep-dive version of issue reporting, for a dedicated audit.
