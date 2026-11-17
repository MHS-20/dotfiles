---
name: behavioral-stories
description: Write, update and review the user's behavioral interview material (STAR stories and personal-question answers) in ~/Work/Personal, mirrored to Notion. Use when the user has a new experience to turn into a story, wants to add or fix a story or a personal answer, map stories to questions or to a company's values (e.g. Amazon's Leadership Principles), find gaps in coverage, or prepare these for an interview at a specific company.
---

# Behavioral stories and personal answers

The material is for recall in an interview. It is not a script. Short, structured and easy to remember beats complete.

## Files

Local, in `~/Work/Personal/`, each mirrored to a Notion page under **Behavioral Interview** (`3726da3fac8580158cffc81be1ab2a83`):

| File | Notion page | Content |
|---|---|---|
| `stories-core.md` | `3c96da3fac858075b6c2f4e5bbf97f47` | Main STAR stories + the core cheat sheet |
| `stories-secondary.md` | `4176da3fac85819780dec98f625c27fb` | Backup stories + their cheat sheet |
| `personal-core.md` | `29e6da3fac8580cab1fad1dc91b7436a` | Frequent personal questions |
| `personal-secondary.md` | `4176da3fac85818aa34acd863dc0b2fb` | Less frequent personal questions |
| `personal-questions-list.md` | `3cc6da3fac8580508d3cc8ce9f1a0efc` | Personal questions list |
| `stories-question-list.md` | `3c76da3fac85804b95e1ef32fff44c01` | Common behavioral questions by category |

Use the `ntn` skill for Notion.

## Story format

Title: `## Project: Short title` in core, `### Project: Short title` in secondary.

Core:
```
## HabitQuest: Making the build easy for everyone
**Customer Obsession** · Invent and Simplify

- **S:** one line of context.
- **T:** what had to be achieved, or the problem.
- **A:**
  - 2–4 short bullets: the decisions *I* made.
- **R:** the outcome with its number or concrete effect, plus the lesson if there is one.
```

Secondary: one `**Use for:** question · competency` line, then `**S/T:**`, `**A:**`, `**R:**`, each one or two lines.

Rules:
- Each bullet gives the idea, not a sentence to recite. Keep the numbers, results and impact. Cut everything else.
- First person, plain words, no filler, no slogans.
- **One story per question.** A story may answer several questions. A question never has two competing stories; a backup is labelled "(backup for the X story)".
- Never number questions or stories. Refer to them by question wording or story title.
- A story goes into core only if the user says so. Ask; secondary is the default.

## Cheat sheets

Each story file starts with `## Cheat sheet`: a `| Question | LP | Story |` table (the LP column holds the competency; Amazon's Leadership Principle names are used because they cover what most companies assess), with questions joined by ` · `. Update it whenever a story is added, renamed, moved or remapped, and check that no question appears for two stories.

## Personal answers

- `### Question` followed by 3–5 short bullets of talking points, not a playbook.
- They are personal: they don't need a story anchor for every point. They must sound like the user. When an answer is vague or doesn't feel like theirs, **ask the user open questions, let them answer roughly, then rephrase** their words into bullets. Don't invent opinions.
- Each idea lives in one answer only. Don't list all the from-scratch projects; "I build things from scratch to understand the internals" is enough.
- The motivation is growth: a challenging environment, a very high bar, very large scale. Cloud and infrastructure are a supporting point.
- Weaknesses: one real weakness plus what they're doing about it. When the user is unsure, offer 2–3 options to pick from, and only accept one that's true today.

## Quality checklist (from interview-prep guides)

Use it when reviewing a story, but keep the short format: each item is one bullet or one clause, not a new section.

- **Situation and Task stay short.** Too much setup is the most common STAR mistake. Spend the words on Action and Result.
- **Action is the core.** 2–4 bullets saying what *I* did, using "I" and not "we". Name the alternative considered and why it was rejected, when there was one.
- **Result leads with the main outcome**, quantified if possible. Fail-the-test result: "the project was a success".
- **End with a reflection/learning line** for failure, mistake and conflict stories: what changed afterwards, or what I'd do differently. Interviewers often ask for it.
- **Conflict stories:** a professional disagreement (design, scope, quality, priorities), never a personality clash. Show the other side as reasonable, bring evidence, and include a concession or what it cost. Try the peer level before escalating. Avoid a clean "we talked and aligned".
- **Learning-fast stories:** tied to shipping something. Say how I learned (docs, a small prototype, a person), include one point of friction, and ideally a step where I passed the knowledge on.
- **Be ready for follow-ups:** for each story know why that decision, what the alternatives were, when I'd escalate, and what I'd change. Answers must hold up to two or three of these.
- **Tell me about yourself:** 60–90 seconds, present → past → future. Lead with the most relevant work, pick 1–2 highlights with a number, end by linking to the role. Not a chronological résumé.
- **Why this company:** two or three specific reasons (one about the company/product/team, one about the role), researched before each interview. It should not work if pasted into another application.
- Talk from bullet points, don't memorise scripts, and practise aloud.

Sources: Tech Interview Handbook (behavioral interview, self-introduction, question list) and AlgoMaster's behavioral course (story bank, tell me about yourself, why this company, conflict, learning new tech).

## Preparing for a specific company

The story bank stays general. Per company, only the mapping and a few answers change:

- Read the company's published values or principles and the job description. Map the existing stories to them in the chat or a short note; don't rewrite the stories.
- Look for value areas with no story and ask the user for one.
- Rewrite "Why this company?" and the last line of "Tell me about yourself" for that company and team.
- Check which questions the company is known to ask (e.g. the Tech Interview Handbook question list), and confirm each one has a story or answer.

### Amazon

- Every behavioral question targets one of the 16 Leadership Principles. Each interviewer usually covers one or two, and they compare notes afterwards, so avoid telling the same story twice in one loop.
- Most frequent for new grads: Customer Obsession, Ownership, Dive Deep, Learn and Be Curious, Deliver Results, Bias for Action, Earn Trust. Then Insist on the Highest Standards, Invent and Simplify, Have Backbone; Disagree and Commit, Are Right, A Lot.
- Expect several "why" and "how did you know" follow-ups on each story. Data and the user's own decisions matter most.
- These are public prep-site observations, not official Amazon policy. Say so if the user asks.

## Adding a new experience

1. Ask for: context, what the user did and decided, the outcome, and any number. One round of questions; rough answers are fine.
2. Ask for a missing result instead of inventing one. If none exists, use the honest outcome and say so.
3. Pick the question and competency it answers most cleanly. If it overlaps an existing story, say so and propose which one wins.
4. Write it in the format above, update the cheat sheet, then sync Notion.

## Facts and honesty

- Check any claim about a project against its source before writing it: repo README and docs, `git log`, or the code. EtcFS lives in `~/Work/EtcFS` (numbers from `etcfs/README.md` and `etcfs-docs/`). Other projects are on GitHub under `MHS-20` / `Basigli` / `g-mainardi`, and can be cloned to `/tmp/repos`.
- Never invent results, numbers or reasons. If something can't be verified, mark it for the user to confirm.
- Only write what the user can defend through two or three follow-up questions. If a claim is true but the user doesn't know its details, flag it.
- Refer to teammates by role. Use neutral wording for the user in third-person lines ("owns what is given", not "he/she").

## Syncing with Notion

- The user edits Notion directly. **Before every update**, fetch the page, normalise tabs to two spaces, and apply the same edits to the Notion text and to the local file. Never overwrite Notion with the local file without checking for differences first.
- Bring the user's Notion edits back into the local file.
- Struck-out (`~~`) stories stay in Notion; drop them locally.
- `ntn pages edit` replaces the whole body. Drop the local `# Title` line, since the page has its own title.
