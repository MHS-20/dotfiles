---
name: code-review
description: "Use this to run a deep, structured review of code and produce a written report, after implementing a feature or fix, before a merge, or whenever asked to review, check, audit, or give a second opinion on code. Looks for simplification opportunities and logic that looks wrong, and checks the code against all five SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion."
---

# Code Review

## When this applies

- After finishing an implementation, before telling the user it's done.
- Whenever asked to review, check, look over, audit, or give a second opinion on code.
- Before a merge or pull request, if the project has that workflow.

## What a review is for

A review is not a rubber stamp, and it's not nitpicking style for its own sake. It exists to catch what a careful second reader would catch: things that are wrong, things that are confusing, and things that are more complicated than they need to be. State clearly when you find nothing wrong — "no findings" is a legitimate, honest result.

## 1. Correctness and sense-check

- Does the code do what the surrounding comments, tests, or spec say it should do?
- Walk through at least one realistic input and one edge case (empty, null, zero, max, a second concurrent call) by hand.
- Flag anything that doesn't look right even if you can't immediately prove it's a bug: a name that doesn't match the behavior, a condition that looks inverted, a comment that contradicts the code next to it, an exception that's caught and silently ignored, a return value that's never used, a test that asserts something trivial instead of the actual behavior.
- Flag dead code, unreachable branches, and copy-pasted blocks that were only partly adapted to their new context.

## 2. Simplification

- For every function or module reviewed, ask whether it could be shorter or clearer without losing behavior.
- Look for logic that could collapse into one well-named function, a library call, or a built-in language feature instead of hand-rolled code.
- Look for unnecessary indirection: a wrapper that just calls one other function, an interface with a single implementation and no planned second one, a configuration option nobody ever sets differently.

## 3. SOLID principles

SOLID is five design principles for keeping code maintainable as it grows. Check the code against every one of them, even outside heavily object-oriented code — the underlying idea (separating concerns, depending on stable abstractions) still applies to modules and functions.

1. **Single Responsibility Principle (SRP)** — a class, module, or function should have only one reason to change. Check: can you describe what this unit does without using "and"? If a change to validation and a change to storage would both force an edit to the same unit, it has more than one responsibility.
2. **Open/Closed Principle (OCP)** — software should be open for extension but closed for modification: you should be able to add new behavior without rewriting existing, already-tested code. Check: does adding a new case (a new payment type, a new export format) mean editing a long if/else or switch chain, or can it be added alongside the existing code?
3. **Liskov Substitution Principle (LSP)** — objects of a subtype should be usable anywhere the base type is expected, without breaking correctness. Check: does any subclass or implementation override a method to throw, no-op, narrow the accepted inputs, or widen the outputs in a way the base type doesn't promise? That's a violation.
4. **Interface Segregation Principle (ISP)** — clients shouldn't be forced to depend on methods they don't use. Check: does an interface or base class force implementers to stub out methods they don't need? Prefer several small, focused interfaces over one broad one.
5. **Dependency Inversion Principle (DIP)** — high-level modules shouldn't depend on low-level modules; both should depend on abstractions, and abstractions shouldn't depend on details. Check: does core business logic import a concrete database, HTTP, or file-system client directly, making it hard to test or swap without editing the core logic? It should depend on an interface that the concrete implementation satisfies instead.

For every violation: name the principle, the exact location (file and function), the concrete cost (not just "this violates SRP" — explain what it actually makes harder, e.g. "every new export format requires editing this 400-line function"), and a suggested fix.

## 4. Concurrency spot-check

Re-check anything touching shared state against the concurrency guidance in the code-quality skill. A review is the second pair of eyes for this, not a replacement for thinking it through the first time.

## Report format

Always write the review up in this structure, even when a section has no findings:

```
# Code Review: <scope — file, PR, or feature name>

## Summary
2-4 sentences: overall state, and the single most important thing to fix, if anything.

## Findings
Ordered by severity — Blocking / Should fix / Consider:
- [Severity] file:line or function — what's wrong, why it matters, suggested fix.

## SOLID
Only list principles with an actual finding. For each: which principle, where, why it matters, suggested fix.

## Simplification opportunities
Concrete "replace X with Y" suggestions, not general style comments.

## Open questions
Anything you couldn't evaluate with confidence. State exactly what you'd need — a file, a spec, a running environment, a clarification — to resolve it. See the never-guess skill.
```

## What not to do in a review

- Don't rewrite the code as part of "reviewing" it unless asked. A review reports; a fix is a separate, explicit step — propose it and check before doing it if it's non-trivial (see status-updates).
- Don't invent a problem just to have something to say.
- Don't flag pure style preferences (tabs vs. spaces, quote style) unless they contradict a convention the project has already established for itself.

## Related skills

- **code-quality** — the standard you're reviewing the code against.
- **status-updates** — how to report findings and check before acting on them.
- **never-guess** — what belongs in "Open questions" instead of an assumption.
