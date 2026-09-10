---
name: overnight
description: Use when the user asks Claude to work autonomously for an extended unattended period (e.g. "overnight", "while I sleep", "run this on auto-loop", "I'll be away for hours") on a list of tasks such as running benchmarks, tests, migrations, or long builds. Covers how to keep going without stopping, poll long-running processes instead of blocking, use timeouts, avoid asking questions, protect correctness/no-regressions, and produce a minimal final report.
---

# Overnight Autonomous Work

Guidance for long unattended sessions where the user will not be present to
answer questions or read intermediate output. Optimize for: never stall,
never wait forever, protect correctness above all, and report briefly at
the end.

## Core rules

1. **Never stop and never wait for the user.** No clarifying questions. If a
   decision requires the user's judgment (ambiguous requirement, destructive
   action with unclear scope, conflicting instructions), **skip that specific
   item**, note it for the final report, and move on to the next task. Do not
   halt the whole session over one blocked item.

2. **Always poll, never block, on long-running commands.** Tests,
   benchmarks, builds, and other long processes must be launched
   asynchronously (background + poll) rather than run in a single blocking
   call:
   - Launch the process in the background (e.g. `command > log.txt 2>&1 &`
     or the equivalent async tool call) and capture its PID/handle.
   - Poll for completion on an interval (e.g. every 30-60s), checking the
     process status and tailing the log, instead of issuing one call that
     waits indefinitely.
   - Never issue a command with no timeout and no way to check progress.

3. **Always set a timeout / max wait per task.** Every benchmark, test run,
   or command gets an explicit ceiling (e.g. "abort/kill if >2h"). If a task
   hits its timeout:
   - Kill it, record it as timed-out/incomplete, and move to the next task.
   - Do not silently keep waiting past the budget.
   - Pick timeouts proportional to the task (a unit test suite vs. a
     multi-hour load test) — ask nothing, just make a reasonable estimate
     and move on.

4. **Correctness and consistency are the top priority, above completing
   more items.** Concretely:
   - Never merge/commit/report success on a change that introduces a
     regression, even if it means fewer tasks get finished.
   - Any correctness-critical checks the user names (tests, formal
     verification like TLA+ model checking, linearizability checkers like
     Porcupine, invariant checks, etc.) must pass before considering related
     work done. If one fails, stop advancing that line of work, record the
     failure, and move to the next independent task — don't paper over it
     or skip the check to save time.
   - When in doubt between "do more" and "don't risk breaking something",
     choose not to risk it.

5. **Work through the task list systematically.** Treat it like a queue:
   pick the next item, do it, record outcome (done / partial / skipped /
   failed + why), move on. Keep going until the list is exhausted or the
   overall session budget/timeout is hit.

6. **Commits, if requested:**
   - Follow the user's exact conventions (e.g. no author name/attribution
     added, amend instead of separate doc-only commits) precisely and
     consistently across the whole session.
   - Keep commit scope aligned with what the user described (e.g. don't
     invent unrelated changes).

7. **Be minimal during the run.** The user will not be reading output live.
   Don't narrate every step at length — just do the work. Save the detail
   for internal tracking, not chat output.

## Final report

At the end (list exhausted, or hard session timeout hit), produce **one
short report**, not a transcript of the session:
- What was completed (one line per item, or grouped if many).
- What was skipped or failed, and the one-line reason (blocked on a
  decision, timed out, correctness check failed, etc.).
- Any regression or correctness-check failure gets called out explicitly,
  even if brief — this is the one thing that must never be buried.
- No preamble, no step-by-step narration of how the session went. Just the
  results.

## Quick checklist before starting

- [ ] Task list enumerated and treated as a queue
- [ ] Every long-running command backgrounded + polled, not blocking
- [ ] Every long-running command has an explicit timeout
- [ ] No questions asked back to the user — ambiguous items skipped instead
- [ ] Correctness/formal-verification checks never skipped or weakened
- [ ] Commit conventions (if any) applied consistently
- [ ] Final output is a single brief report, not a running commentary
