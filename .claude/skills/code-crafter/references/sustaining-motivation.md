# Sustaining a long project

A staged curriculum's real failure mode is not a stage that's too hard. It's
week four, when the user stops showing up. Difficulty is rarely the cause;
the causes below are, and each has a structural fix. Reach for the fix, not
for encouragement — a pep talk about grit is the least useful thing to say to
someone telling you the work has become a chore.

Watch for the signals: sessions getting shorter, a gap of more than a week,
"I don't know why but X is more fun," asking to skip ahead, or asking Claude
to just write it.

## Diagnose before prescribing

The complaint "I can't find the motivation" is almost always one of four
distinct problems. Ask, or infer from what they describe — the fixes differ
and the wrong one makes things worse.

### 1. Context-reload cost

The tell: "it's daunting," "I have to remember too much before I can start,"
short sessions that never get going.

By stage 8 of a 25-stage project, sitting down means reconstructing a schema,
a protocol, three file locations and four past decisions before writing a
line. That cost is paid *every session* and it is pure waste. It is also the
single most common cause, and the most fixable.

**Fix: a context card.** Maintain `CONTEXT.md` in the project — one screen,
describing only the stage they're *in*, never the whole plan. Claude keeps it
current and opens each session from it. It should hold: where they are, the
one-paragraph why, a table of decisions already made and the reasoning behind
each (so they are never re-litigated), which files matter now and who owns
each, the order of work, and the commands. Nothing else.

### 2. The unit of work has grown

The tell: "LeetCode is more fun," "there's no complex context to understand
before doing stuff," nostalgia for the early stages.

Early stages are self-contained: one function, one test, a feedback loop of
seconds. Later stages span four components and "did it work?" costs a build,
a mount and squinting at debug output. The code didn't get less interesting —
the scaffolding needed to run one line of it did.

**Fix: extract the drill.** Every stage has a kernel of 30-60 lines where the
actual idea lives: the encoder, the alignment math, the extent arithmetic,
the CAS transaction, the generation guard. Pull it into a self-contained
exercise with a pure test file — no network, no daemon, no mount, runs in
under a second — and a `make drill` target. Then the integration (wiring it
into the running system) is a separate, shorter session where the hard
thinking is already done. This is the highest-leverage fix in this document
and it is worth doing pre-emptively, not just in response to a complaint.

Write drill tests as *contract* tests: assert the properties the design must
have, never the exact bytes or the exact structure, so the user's design
decisions remain theirs. Good drill tests are where the edge cases live —
truncation, sign extension, forward compatibility, aliasing, concurrency —
which is exactly the material they came for.

### 3. Writing by hand feels like typing, not learning

The tell: "I know I should write it once to learn it, but it's boring."

Sometimes accurate and sometimes not, and the difference matters. Deciding a
byte layout teaches something; typing the twelfth `PutUint32` does not.
Reasoning about a lock's failure modes teaches something; wiring an error
return through four layers does not.

**Fix: draw a line and name it.** The default line: *the user writes the
concurrency, ordering, protocol and low-level layout; Claude writes
serialization glue, plumbing, fixtures and scaffolding.*

**But do not assume where the line goes — ask.** It depends entirely on what
they want to become. Someone aiming at distributed systems may happily let
Claude write the byte layout; someone aiming at kernel and systems
programming wants exactly that byte layout and would be robbed by the same
offer. If Claude proposes a line and the user pushes back on which side
something belongs, they are right by definition — it's their goal. Move the
line and say so plainly rather than defending the original split.

### 4. Cadence mismatch

The tell: "I try to show up every day," alongside any of the above.

A daily 20-minute habit works for self-contained problems and fails for
projects with a context-reload cost, because the reload eats the session.
Suggest two longer sessions a week over seven short ones, and say explicitly
that a week off is not quitting. Guilt about a broken streak ends more
projects than difficulty does.

## Assisted mode

A user may ask to work with editor completions rather than writing
everything by hand. This is legitimate and usually better than the project
dying. Accept it, and install one guard.

**The failure mode to name out loud:** recognition and production are
different skills. Reading a completion and understanding it feels identical,
from the inside, to being able to write it — and the feeling arrives much
sooner than the ability. "I'll make sure I understand every line" does not
catch this, because they genuinely will understand every line as they read
it.

**The guard: keep production somewhere.** Completions for scaffolding, glue
and repetition; completions *off* for the stage's drill. Plus the memory
check below. That combination is what separates assisted development from a
build-along tutorial, which teaches far less than it feels like it does.

**The memory check.** At the end of a stage: close the editor, rewrite the
kernel function from scratch in a scratch file, five minutes. If it comes
out, they learned it. If it doesn't, they read it. Cheap enough that they'll
actually do it, and it is the only honest signal in an assisted workflow.

**A useful property of completions** worth pointing out: they are good at
boilerplate and unreliable at subtle bit manipulation, signedness, off-by-one
and concurrency — precisely the material a systems-focused user is here for.
Catching a confidently-wrong completion is real practice. Give them the rule:
if a completion looks right and you can't say *why* it's right, that's the
same as it being wrong.

Completions replace typing, not mentoring. A completion will never surface
the design space, push back on weak reasoning, or notice that today's layout
breaks stage 12. Claude still does all of that.

## Watch mode

Save-triggered review: Claude watches a file and wakes when the user saves,
seeing the diff since the last save. It gives them low-friction access to
explanations without breaking flow to compose a question.

**Scope it to exactly one file** — the one holding what they are currently
thinking about. Watching a directory or a repo means waking on formatter
runs, build output and unrelated edits: noise for them, cost for nothing. To
move the watch, stop the old one and start the new one; never run two.

**Markers** let them ask from inside the editor. They type a marker, save,
read the answer, delete the marker:

| Marker | Means |
|---|---|
| `// ?` | Explain this — what is this line doing, why is it like this. |
| `// ? <question>` | The same, specific: `// ? why big-endian here` |
| `// ??` | Stuck, next hint level. Repeating it pulls Claude down the hint ladder. |

Use the target language's line-comment syntax.

**Default to silence.** This is the part that matters, and the part that is
easy to get wrong. Commenting on every save preempts every moment of
productive struggle and turns the user into a passenger — worse than no watch
at all. Without a marker, speak only for:

- **A real bug** that would cost them an hour: a sign-extension slip, a
  truncating cast, a broken prefix boundary, a lost wakeup. Not style, not
  "this could be more elegant," and never a function they are visibly
  halfway through writing.
- **Stuck**: file unchanged for roughly ten minutes. One level-1 nudge, once,
  not on a loop.

**On a marker**, answer that question only. Don't review the rest of the
diff, and don't volunteer the next step. `// ??` still starts at hint level 1
the first time.

Say the token cost out loud once, and stop the watch when the session ends.

## When none of this is enough

If the user is systems- or kernel-bound and greenfield construction keeps
stalling, offer a different shape rather than more of the same: reading a
real codebase and writing small patches against it. Real kernel work is
mostly reading plus dense, carefully-reasoned diffs, not writing thousands of
lines of scaffolding. For some users that path reaches the same destination
and fits how they actually work. Offering it is not conceding failure.

The order of preference when a project is stalling: fix the structure, then
move the hand-written/generated line, then change the cadence, then change
the project's shape. Abandoning it is still better than a curriculum that
turns into an obligation — say so if it comes to that.
