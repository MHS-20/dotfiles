---
name: code-quality
description: "Apply on every task that writes, edits, refactors, or generates source code, in any language, not only when quality is mentioned explicitly. Enforces simple and elegant solutions, active code-smell detection, sensible use of design patterns, and concurrency and race-condition safety. This is the default engineering bar for every file touched, including small edits and quick fixes."
---

# Code Quality

## When this applies

Every time you write, edit, refactor, or generate code — new features, bug fixes, one-line changes, scripts, config-as-code. Don't wait to be asked about "quality"; treat this as the standing bar for anything that leaves your hands.

## The standard, in one sentence

Prefer the simplest correct solution, and make it easy for the next person — human or agent — to change safely.

## Before you write

- Read enough of the surrounding file/module to match its existing conventions (naming, error handling, structure) before adding to it.
- Prefer extending an existing pattern over inventing a new one. If the existing pattern is itself the problem, say so instead of quietly working around it (see the status-updates skill).

## Clean code checklist

Apply this while writing, not only when reviewing afterward:

- **Names** should make a comment unnecessary. If you have to explain what something is, rename it instead.
- **Functions do one thing.** If describing a function's job needs "and," split it.
- **Keep functions and files short enough to hold in your head.** If you can't summarize a function in one sentence, look for a split.
- **Minimize side effects.** Prefer functions that return a value over functions that mutate shared state.
- **Use guard clauses / early returns** instead of deeply nested conditionals.
- **No magic numbers or strings.** Give them a name.
- **Handle errors explicitly.** Never catch an exception and do nothing with it.
- **Comments explain why, not what.** If the code needs a comment to explain what it does, rewrite the code instead.
- **Delete dead code and unused variables/imports.** Don't comment them out "just in case."

## Simplify relentlessly

- Once the code works, re-read it and ask what you could delete and still have it work.
- Prefer the standard library or an existing project dependency over adding a new one.
- Don't add abstraction (interfaces, config flags, plugin points) for a need you're imagining. Build it when a second real use case actually shows up.
- If a change is meant to fix one bug, keep the diff scoped to that bug. Flag unrelated cleanup separately instead of folding it in silently.

## Code smells to watch for

- **Long function** — does too much; hard to name in one sentence.
- **Large class / god object** — knows or does too much.
- **Duplicate code** — the same logic in multiple places. Extract a shared function once it appears a third time.
- **Long parameter list** — more than three or four params usually means you need a struct or object instead.
- **Feature envy** — a function is more interested in another module's data than its own.
- **Shotgun surgery** — one conceptual change forces edits across many unrelated files.
- **Data clumps** — the same group of fields or parameters travels together everywhere; give it its own type.
- **Primitive obsession** — raw strings or numbers standing in for a real domain concept (an email, money, an ID).
- **Speculative generality** — unused hooks, parameters, or abstractions kept "for the future."
- **Message chains** — `a.b().c().d()`; hides dependencies and breaks if any link changes.
- **Mixed abstraction levels** — a single function mixing low-level detail with high-level orchestration.

## Design patterns: use with judgment

Reach for a named pattern to solve a recurring, real problem — not to look sophisticated. Be able to state the problem before naming the pattern.

- **Creational** — Factory / Abstract Factory (creation logic when the concrete type varies), Builder (staged construction of a complex object), Singleton (use sparingly; usually a sign of hidden global state — prefer passing a dependency explicitly).
- **Structural** — Adapter (bridge incompatible interfaces), Decorator (add behavior without subclassing), Facade (simplify a complex subsystem behind one entry point), Proxy (control or defer access to something).
- **Behavioral** — Strategy (swap an algorithm at runtime), Observer (broadcast state changes to listeners), Command (encapsulate an action as an object, e.g. for undo or queueing), State (behavior changes with internal state), Template Method (fixed skeleton, overridable steps), Chain of Responsibility (pass a request along a list of handlers).
- If you introduce a pattern, name it in a comment or your status update so the reasoning is visible ("Using Strategy here so X can be swapped without touching Y").
- Warning sign: if applying a pattern adds more code than it removes and there is only one real use case, don't use it.

## Concurrency and race conditions

- Identify any shared mutable state — module-level variables, shared caches, files, database rows, in-memory singletons — touched by more than one thread, process, or async task.
- Watch for check-then-act races (deciding based on a state that can change before you act on it), unsynchronized read-modify-write on shared counters, unsynchronized writes to shared collections, double-initialization of singletons, and lost updates from concurrent transactions.
- Prefer, in this order: (1) avoid sharing mutable state at all — pass data instead of sharing it; (2) use the language or platform's safe primitives — locks, atomics, channels, transactions with the right isolation level, optimistic concurrency with version checks; (3) hand-rolled locking only as a last resort, with the reasoning written down.
- For anything touching money, inventory, counters, or unique-ID generation, assume concurrent access will eventually happen even if today's caller is single-threaded.
- If you're not sure whether a resource can be accessed concurrently in this codebase, say so explicitly rather than assuming it's safe — see the never-guess skill.

## Before you report a change done

Pause and check:

- Would you be comfortable if a senior engineer read this diff line by line?
- Is there a simpler version that does the same thing?
- Did you introduce any of the smells above?
- Did you touch shared state without thinking through concurrency?

If the honest answer to any of these is no, fix it before reporting completion — or flag it explicitly as a known trade-off (see status-updates).

## Related skills

- **code-review** — a deeper, dedicated audit pass with a written report and a SOLID-principles check.
- **status-updates** — how to report a smell or trade-off you noticed but didn't fix.
- **never-guess** — what to do when you're not sure whether something is safe or correct.
