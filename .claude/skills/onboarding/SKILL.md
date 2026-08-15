---
name: explain-codebase
description: |-
  Give a prioritized reading path through a codebase — entry points, core
  domain logic, data layer, interfaces, config, and tests-as-documentation —
  so the user or another agent can make a correct architectural decision
  after reading 5-10 files, not the whole tree. Use when asked to explain the
  codebase, onboard someone to it, or provide architectural guidance before
  a patch.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: onboarding
---

## What I do

I map a repository to a short, ordered reading list, with one line per file
explaining what it does and why it matters for making changes — not a
paraphrase of its code, and not a tour of every file in the tree.

## Procedure

1. Read root-level orientation files first, if present, in this order:
   `README.md`, `AGENTS.md`/`CLAUDE.md`, `ARCHITECTURE.md`, the manifest
   (`package.json` / `pyproject.toml` / `Cargo.toml` or equivalent),
   `docker-compose.yml`.
2. Identify and list, in priority order:
   - **Entry point(s):** where execution starts (main, server bootstrap, CLI
     entry).
   - **Core domain logic:** the 2-4 files/modules encoding the actual business
     rules, not glue code.
   - **State/data layer:** schema definitions, models, migrations.
   - **Interfaces/contracts:** API route definitions, public exported types,
     shared interfaces between subsystems.
   - **Configuration surface:** env vars, config files, feature flags — these
     constrain what changes are safe.
   - **Tests that double as documentation:** the test file(s) that most
     clearly show intended behavior of the core logic.
3. For each file listed, give one line: what it does + why it matters for
   changes.
4. Explicitly flag dead ends: legacy code paths being phased out, and files
   that look central but are actually thin re-exports. These waste the most
   time if misjudged.
5. End with a short "if you are about to patch X, also check Y" map for the
   2-3 most common change types in this repo (e.g. "new API route → check
   middleware.ts for auth, and openapi.yaml for the contract").

## When to use me

Use before an architectural decision, before a non-trivial patch, or whenever
asked to explain or onboard onto a codebase. Do not use for narrow questions
about a single already-known file — just answer those directly.

## What I avoid

A file-by-file tour of the whole tree. Depth over coverage, always.
