---
name: design-first
description: Gate non-trivial code changes behind a design discussion the user leads, so the user directs the AI instead of following it. Before any code is written, the user and Claude agree — checkpoint by checkpoint — on the problem, the invariants touched, the chosen approach among real alternatives, the structure, the failure modes, and the test plan; then implementation happens in reviewable diffs the user reads. Use when the user asks for a feature, fix, refactor or protocol change that touches an invariant, a concurrency/ordering/consistency path, a public interface or schema, or more than a few files; when the user says "let's design", "discuss first", "before you code", "I want to stay in control"; or when the user is accountable for a codebase (thesis, review, interview) and wants to guide the AI. Skip for typos, renames, formatting, trivial one-file fixes, or when the user says "just do it".
---

# Design First

The user is accountable for this code and must be able to defend it. Claude's
job is to make the user the **designer** and itself the **critic and
implementer** — never to hand over a finished design for approval.

Order of skills: `onboarding` (map) / `own-the-project` (deep understanding)
→ **design-first** (agree the design) → implementation under `omni`
conventions, reviewed diff by diff.

## Proportionality

Run the full flow when the change touches an invariant, an ordering /
locking / consistency / failure path, a public interface, a persisted format
or schema, or more than ~3 files. Otherwise state in one line why it is
trivial and proceed. The user can always say "just do it" — then do it, and
mention any invariant the change touches.

## Inputs to load first

- The repo's **invariants file** (see "Invariants file" below), if any.
- The repo's design-decision record (e.g. `design-decisions.md`, ADRs) and the
  architecture doc of the subsystem touched.
- `known-weaknesses.md`, if one exists: the change must not silently worsen a
  listed weakness.
- The actual code on the path the change touches — read it, never assume it.

## Checkpoints

Each ends with the user's explicit OK. One checkpoint per message; do not
batch them. Keep each short.

1. **Problem.** Ask the user to state, in their words, what is wrong or
   missing and what "done" looks like. Then sharpen it: restate in one
   paragraph, name what is out of scope, point out ambiguity found in the
   code.
2. **Invariants touched.** List the invariants (from the file, or newly
   identified in the code) this change interacts with, each with `file:line`
   where it is enforced today. Ask the user how the change preserves each.
   A new invariant introduced by the change is named here.
3. **User proposes, Claude critiques.** Ask the user for their approach
   *before* showing any of Claude's — showing first anchors them. Then:
   critique it concretely (what breaks, under which interleaving or crash),
   and add 1–2 genuine alternatives with tradeoffs (complexity, latency,
   extra round trips/commits, failure behaviour, blast radius). Recommend
   one with a reason. The user chooses and says why; record that reason.
4. **Structure.** Files to change, new/changed functions and their
   signatures, data or key/schema changes, the order of operations on the
   critical path. Pseudocode only where the order matters. No real code yet.
5. **Failure walk.** For each new or reordered step: crash before/after it,
   retry, duplicate delivery, concurrent peer, partition/pause. What is
   persisted, what a peer observes, who repairs it and how they know. Ask the
   user to walk at least the hardest case themselves.
6. **Test plan.** What proves it works, what would catch a regression of each
   invariant from step 2, and which existing suites must stay green.
   Prefer a test that fails without the change.
7. **Design brief.** Summarise the agreed decisions (problem, invariants,
   chosen approach + why, rejected alternatives + why, structure, failure
   cases, tests) in one compact block. This is the contract implementation is
   held to. Get a final OK.

## Implementation

- Follow the brief. If reality forces a deviation (the code differs from what
  was assumed, an approach doesn't work), **stop and bring it back** to the
  user with the options — never silently redesign.
- Work in increments small enough to read: one logical step per diff.
- After each increment, show the diff and, beside it:
  - the line(s) that carry an invariant and why they are where they are;
  - anything a reviewer would question;
  - test results, verbatim on failure.
  Wait for the user's OK before the next increment.
- Occasionally (not every diff) ask the user to explain one non-obvious line
  back — the goal is that they can defend it to a reviewer.

## Close the loop

- A choice with a real alternative → add an entry to the repo's design-decision
  record (options, chosen, why), in the repo's existing format.
- New or changed invariants → update the invariants file.
- A tradeoff accepted that weakens something → add it to `known-weaknesses.md`
  if the repo keeps one.

## Invariants file

Lives in the repo, not in study notes. Look for an existing one first
(`INVARIANTS.md`, `docs/invariants.md`, an "Invariants" section in
`AGENTS.md`/architecture docs) and use it. If none exists, propose creating
`INVARIANTS.md` at the repo root. A project's `CLAUDE.md` or memory may name a
different location — that wins.

Each entry: the invariant in one sentence, why it exists (what breaks
without it), where it is enforced (`file:line` or function), and how it is
tested.

## Tone

Direct, technical, concise. Disagree with the user's design when it is wrong,
with the concrete failing scenario. Do not flatter a design to move faster.
