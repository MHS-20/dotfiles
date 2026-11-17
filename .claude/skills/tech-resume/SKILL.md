---
name: tech-resume
description: Write, rewrite, tailor or review a software-engineering resume (and the matching LinkedIn profile) for big-tech / startup applications. Use when the user asks to write or improve a resume/CV, rewrite bullets, tailor the resume to a job description, check ATS-friendliness, pick sections/order, or review a resume before applying.
---

# Tech resume writing

Sources: Harvard OCS "Resumes & Cover Letters" guide (2021), Tech Interview Handbook (techinterviewhandbook.org/resume), Aced/Exponent SWE resume guide (aced.io/blog/software-engineer-resume), the user's Notion "Resume Tips" page (Ashish – Big Tech Resume & LinkedIn, Farah Sharghi – Resume Secrets, Anthony D. Mays – Resume Tips). AlgoMaster and NeetCode had no fetchable resume article when this skill was written (2026-11-17).

## Local files
- `~/Work/Resume/resume-master.tex`: database of every project/bullet, never sent as is. One-page variants `~/Work/Resume/resume*.tex` are built from it (variant list and rules in `~/Work/Offers/CLAUDE.md`). Build with `tectonic`, check `pdfinfo <pdf> | grep Pages` = 1.
- Improve bullets in the master first, then propagate to the variants. Cover letters: use the `cover-letter` skill.

## The mindset
- A recruiter scans for **~7 seconds**, 200+ resumes a day, after an **ATS** filter. Optimise for both: keywords for the machine, instant clarity for the human.
- Hiring managers want a **safe hire**: look like someone who has *already done this job*. Vagueness, unexplained gaps and weak verbs read as risk.
- Show balance: **technical depth + business impact + leadership/soft skills** (cultural fit). Prove soft skills through bullets, never list them.
- Every line must earn its place. A few strong achievements beat many average ones.

## Workflow
1. **Collect inputs**: the current resume (ask for the file/text), the target job description(s), level (new grad / mid / senior). Never invent experience, numbers or skills — ask for the real metric, or mark `[METRIC?]` for the user to fill.
2. **Analyse the JD(s)** (3–5 for a role type, or the one target posting): extract and count recurring
   - technical skills, - soft skills, - product qualities ("-ilities": reliability, scalability, zero downtime, latency…).
   Frequency = priority. Mirror the posting's exact wording (and spell out abbreviations once: "Amazon Web Services (AWS)").
3. **Reflect / mine impact**: for each role, ask what was built, how, and the measurable result (latency, throughput, users, data size, cost, error rate, CI time, coverage, incidents, revenue, time saved). Indirect impact counts. Rough numbers are fine if honest.
4. **Write** bullets with the formula (below), sections in the right order, one page.
5. **Review** with the checklist at the end; report the remaining gaps (missing metrics, unmatched JD keywords) to the user.

## Bullet formula
Pick one, all equivalent:
- **XYZ (Google)**: "Accomplished **X**, as measured by **Y**, by doing **Z**."
- **Action-first (Aced)**: *Action verb* + *what you built/fixed* + *technical approach (tech named)* + *result in numbers*.
- Italian note from the user: *cosa hai fatto, come l'hai fatto, qual è stato il risultato.*

Rules:
- Start with a strong verb. Senior/ownership verbs: **led, owned, launched, spearheaded, designed, architected, drove, migrated, cut, shipped**. Never "responsible for", "helped", "supported", "worked on", "participated in".
- No pronouns at all (no "I", no "we"); a phrase, not a full sentence; drop articles where it still reads well. It must still be clearly *your* work: "Migrated the billing service out of the monolith", not "We migrated…". (The "I accomplished X" formula is a thinking template; strip the "I".)
- Specific, fact-based, plain: write to express, not impress; no flowery words, slang, narrative style.
- Vary verbs: never start several bullets in one role with the same verb.
- Name the technology inside the bullet (a skills list alone is just a claim); parentheses are fine: "(Kafka, Go)".
- 1–2 lines each (never >3), 3–5 bullets per role, strongest first, most recent roles get the most bullets.
- Results over duties.

Weak → strong (verbatim from Aced):
- "Worked on the payments backend" → "Cut payment API p99 latency from 800ms to 120ms by moving fraud checks to an async queue (Kafka, Go)"
- "Wrote unit tests" → "Caught 12 regressions before release with 40 integration tests for the checkout flow (pytest), now run on every deploy"
- "Built a chat app" → "Built a WebSocket chat service handling 10K concurrent connections on one node; load-tested with k6"
- "Built a distributed database using Java" → "Implemented Multi-Paxos from scratch, guaranteeing linearizability under partitions and 20% packet loss"
- "Maintained the CI pipeline" → "Cut CI time from 25 to 8 minutes by parallelizing the test suite"

## Format / layout
- One page (new grad, mid). Senior/staff: max 1.5–2 pages only if every line earns it.
- Single column, plain template, no photo, icons, skill bars/ratings, tables, headers/footers, symbols in headings. 0.5" margins, Arial/Calibri/Garamond (or LaTeX equivalent), ≥10 pt, minimal vertical whitespace.
- No photo, age, gender, marital status, references ("available on request" too). Don't start lines with dates. Be consistent: numerals vs words, bold/italics, capitalisation, date format.
- Bullets, not paragraphs. Consistent dates `MM/YYYY – MM/YYYY | Present`. Submit PDF named `Firstname-Lastname-Resume.pdf`.
- ATS test: copy the PDF text into a plain-text file — nothing missing, scrambled or garbled.

## Sections & order
- **New grad / <3 yrs**: Contact → (Summary) → Education → Skills → Experience → Projects (Projects above Experience if stronger) → Awards.
- **Experienced**: Contact → (Summary) → Experience → Skills → Projects (optional) → Education (one line).
- Skills may go near the top for fast recruiter scanning (Ashish).

Per section:
- **Contact**: name, phone, city/country, personal email, custom LinkedIn URL, GitHub (clean & pinned), portfolio, competitive-programming rank if strong. Never a work email/phone.
- **Summary**: optional. Use for career changers, a specialty, or to state the thesis the resume proves; ≤50 words, written last, no fluff. Otherwise spend the space on a bullet.
- **Experience**: `Company, Location | Title | dates`, reverse chronological. Focus on the last 5–7 years; condense older roles. Explain gaps/short stints briefly and honestly (one line), never leave them silent.
- **Skills**: grouped one-liners — `Languages: … | Frameworks: … | Databases: … | Cloud/Infra: … | Tools: …`. Only what you can be interviewed on; each should reappear in a bullet. No soft skills, no ratings, no Office/Word, no 30-item dumps.
- **Projects**: ≥2 hard ones you can defend in depth; stack beside the name, link to GitHub/demo only if clean/working, 2–3 bullets on the hardest problems. Strong signals: measurements/benchmarks, formal verification, chaos/fault-injection testing, production debugging, trade-offs, failure scenarios, real users (give the count).
- **Education**: degree, university, location, (expected) year; GPA only if ≥3.5/4 (or equivalent, e.g. ≥105/110 in Italy); one line of relevant coursework max; drop details after the first full-time job.
- **Awards**: `Year | quantified result | competition` ("2016 | Best product out of 50 teams | Facebook Hackathon"); only relevant ones.
- Drop hobbies and irrelevant skills.

## Tailoring per application
- Reorder/rewrite bullets to emphasise what the JD repeats (front-end role → front-end bullets first).
- Put JD keywords in Skills **and** in bullets, naturally; no stuffing, no skills you can't defend.
- Optionally check fit with a matcher (SkillSyncer, Jobscan, Resume Worded); treat the score as a hint.
- Don't apply to several different roles at the same company at once.
- Cover letter: rarely needed at big tech; for startups a short note on *why this role*, never a resume repeat, < 1 page.

## LinkedIn (keep in sync, can be more detailed than the resume)
- Custom URL; professional photo; headline = title + core skills + value (keywords, no clichés); keyword-rich About; ~5 key skills with endorsements; Featured/Projects with links; quantified experience; Open to Work; turn off share-profile-updates while editing; ask for referrals with a specific job link.

## Top 6 mistakes (Harvard OCS)
Spelling/grammar errors · missing email/phone · passive language instead of action verbs · hard to skim · no results shown · too long.

## Review checklist
- [ ] One page (or justified), single column, PDF, plain-text test passes
- [ ] Every bullet: strong verb, own action, tech named, measurable result, ≤2 lines
- [ ] No "responsible for / helped / worked on / we"
- [ ] Top JD keywords appear in Skills and bullets; abbreviations spelled out once
- [ ] Every skill listed is backed by a bullet/project and interview-defensible
- [ ] Section order matches level; recent roles dominate; gaps explained
- [ ] Mix of technical, business and leadership signals
- [ ] No typos, consistent dates/punctuation/tense (past for old roles, present for current)
- [ ] Links work (LinkedIn, GitHub, demos)

Output: when rewriting, show each changed bullet as *before → after*, list `[METRIC?]` placeholders the user must fill, and list JD keywords still missing.
