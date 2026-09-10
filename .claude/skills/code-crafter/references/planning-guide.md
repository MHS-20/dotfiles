# Planning Guide: turning a project into a staged curriculum

Read this fully before writing `stages.md`. It covers how to find the target's
learning-critical path, how to size and order stages, and exactly what to put
in the plan.

## 1. Classify the target

- **Reference-implementation-backed** (e.g. "build my own Redis," "build my
  own git"): a real, well-known codebase exists that the user can be pointed
  at line-by-line. Prefer citing *that* project's actual source.
- **Spec-backed, no single reference impl** (e.g. "build an HTTP/1.1 server,"
  "build a BitTorrent client"): there's an RFC/spec but no single canonical
  codebase to cite. Reference the spec section number instead of code lines.
- **Open-ended / user's own design** (e.g. "build a job-queue system like the
  one at my company"): no external reference at all. Stages cite the design
  document Claude and the user produce together instead of external lines.

Ask which bucket applies if it's not obvious — it changes what "reference
lines" means in every stage entry.

## 2. Find the learning-critical path

If there's a reference implementation, don't stage the whole thing — most
real codebases are >80% plumbing. Read the entrypoint and follow the main
execution path, then classify each component:

- **Core / worth building by hand**: anything embodying a genuinely
  interesting idea the user came here to learn — a parser, a wire protocol,
  a data structure, a concurrency primitive, an algorithm, a consistency
  protocol, an eviction policy, a diffing algorithm, etc.
- **Boilerplate / should be scaffolded**: CLI argument parsing, logging
  setup, config file loading, project/package scaffolding, dependency
  wiring, generic error-handling glue, build scripts, most test-harness
  code.
- **Judgment calls**: things like "socket accept loop" are usually
  boilerplate the first time they appear, but become a legitimate stage the
  moment concurrency, backpressure, or connection lifecycle management is
  the actual lesson (e.g., "handle multiple concurrent clients" is a fine
  stage in a Redis-clone curriculum even though a bare accept loop wouldn't
  be).

A useful test: *would writing this by hand teach the user something they
came here to learn?* If yes, it's a stage. If it's just necessary friction
to get to the interesting part, scaffold it.

Use whatever repo-reading tools are available (viewing files, grep/search,
git blame/log for history and commit boundaries — real projects' own commit
history is often a decent hint at natural staging boundaries) to build this
map before designing stages.

## 3. Stage sizing

Target: **a stage should take a focused person roughly 30-90 minutes**,
produce a visible, testable result (a passing test, a command that now
prints the right thing, a new client behavior that works end-to-end), and
touch **one primary new concept** (occasionally two if they're inseparable).

Signs a stage is **too big** — split it:
- It requires holding more than ~3 new concepts in your head simultaneously.
- The natural verification step only happens at the very end, so the user
  gets zero feedback for 90+ minutes (bad — split so each half is
  independently verifiable).
- The reference implementation's own commit history shows this landing over
  many separate commits by its original authors.
- It mixes "get the plumbing right" with "get the interesting algorithm
  right" — separate those into two stages where feasible.

Signs a stage is **too small** — merge it:
- It's pure boilerplate with no real decision or new concept (should've been
  scaffolded, not staged).
- It would take under ~10 minutes even including reading the context.
- It's a trivial extension of the immediately preceding stage with no new
  idea (e.g., "now also handle the DELETE command" right after "handle the
  GET command" using identical logic shape — fold these into one stage with
  multiple sub-tasks instead of two stages).

Calibrate to the scope the user chose in the bootstrap step: a
weekend-sized MVP might be 6-10 stages; a multi-week project might be
25-40+. When in doubt, err smaller and more numerous — momentum and
frequent wins matter more than fewer, chunkier stages.

## 4. Ordering

- Strict dependency order: a stage may only assume things built in earlier
  stages exist.
- Prefer an order that keeps something runnable and testable after every
  single stage, even in a minimal way (e.g., "server starts and responds to
  one hardcoded command" before "server parses arbitrary commands").
- Front-load the stage that teaches the central metaphor or data structure
  of the whole project if possible — it pays off in every later stage.
- Save cross-cutting concerns (persistence, replication, concurrency
  hardening, performance) for after the single-threaded/happy-path version
  works, unless the user specifically said the concurrency/distributed
  aspect *is* the point of the project.

## 5. What each stage entry needs

Follow `stages_template.md` for exact formatting. Every stage needs:

- **Title & number.**
- **Concept(s) introduced** — one line, plain language.
- **Why it matters** — a few sentences of real-world context: what breaks or
  is impossible without this piece, what systems use this idea elsewhere.
- **Reference pointer** — for reference-backed targets: `repo/path/file.ext`
  with a line range (get exact ranges by reading the file, don't guess). For
  spec-backed targets: the RFC/spec section number and title. For open-ended
  targets: reference the shared design doc section.
- **Task description** — precise, unambiguous statement of what the user's
  code must do, phrased as behavior/contract, not as a step-by-step
  implementation recipe (that would pre-empt their own design work).
- **Interface/contract** — the exact function signature(s), data
  structure(s), or protocol message shape(s) the surrounding boilerplate
  expects them to produce, so their code plugs in cleanly.
- **Verification** — an exact command to run (a test file, a CLI
  invocation, a curl command) and what success looks like.
- **Suggested design questions** — for stages with a genuine design
  decision, 2-3 questions to prompt exploration (used by mentor mode, not
  answered here).
- **Hints** — write all four ladder levels up front (see
  `mentoring-playbook.md` for the ladder definition) so mentor mode doesn't
  have to invent them live and risk inconsistency across sessions.
- **Estimated time** and **difficulty** (light/medium/heavy) relative to the
  rest of the curriculum.

## 6. Scaffolding rules

When generating the boilerplate repo:

- Every stage's task surface should be a clearly marked stub: a function
  raising `NotImplementedError`/`todo!()`/equivalent, or a clearly commented
  gap, matching the contract documented in that stage's entry exactly.
- Include whatever test harness or runner is idiomatic for the language so
  "verification" in each stage entry is a real, runnable command from day
  one — even stage 1.
- Do not implement any core-path logic "just to get things running," even
  partially. If the scaffolding needs the stubbed function to return
  *something* to compile/run, return an obviously-wrong placeholder (e.g.
  `null`, an empty struct, an error) rather than a plausible-looking partial
  implementation — a partial implementation can quietly do some of the
  user's thinking for them.
- Set up version control (a git repo) if not already present, with the
  scaffold as an initial commit, so each finished stage can become its own
  commit — this gives the user a clean diff of exactly what they wrote per
  stage, and a natural rollback point if a stage goes sideways.

## 7. `progress.md` format

Keep it simple — a checklist mirroring `stages.md` titles, e.g.:

```markdown
# Progress

- [x] Stage 1: TCP echo server
- [ ] Stage 2: RESP protocol parser
- [ ] Stage 3: PING/ECHO commands
...

## Notes
(free-form space for the user's own running notes/questions)
```

Update the checkbox the moment a stage's verification passes.
