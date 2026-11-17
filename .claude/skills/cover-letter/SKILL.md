---
name: cover-letter
description: Write, tailor or review a cover letter (or a short "why this company/role" note or motivation answer) for a software-engineering application. Use when the user asks for a cover letter, motivation letter, "why do you want to work here" text, or a review of one.
---

# Cover letters

Sources: Harvard OCS "Resumes & Cover Letters" (2021), Tech Interview Handbook, Aced/Exponent SWE guide, plus the user's conventions in `~/Work/Offers/CLAUDE.md`. For the resume itself use the `tech-resume` skill.

## Should there be one at all?
- Big tech: rarely read; write one only if the form asks or allows it and the role is a strong target.
- Startups, small companies, European/Italian companies, career pivots, explaining a gap or relocation/visa status: worth it.
- Never send a generic one. No letter beats a bad letter.

## Local workflow
1. Copy `~/Work/Offers/letters/cover-letter-template.tex` to `letters/<company>-<role>.tex`; fill the PER-APPLICATION block (company, role, team, city, recipient), pick `\SecondProject`, write `\WhyTeam` from **real research** on the team/product (engineering blog, talks, repos, recent launches). Look at existing letters in `letters/` for tone.
2. Facts only from `~/Work/Resume/resume-master.tex` and `~/Work/Personal/*.md` (stories). Never invent experience, numbers or motivation; ask the user if missing.
3. No `[...]` placeholder left. Work-authorisation line: EU/EEA/CH no sponsorship; UK needs a Skilled Worker visa.
4. Build with `tectonic`, confirm 1 page, same font/size as the resume.

## Structure (one page, ~250–400 words, 3–4 paragraphs)
- **Header**: date; recipient name + title + company (address optional). Address a specific person ("Dear Morgan Smith:"); find the hiring manager/recruiter if possible, else "Dear <Team> Hiring Team".
- **Opening**: who you are (one line), the exact role, where you found it / referral name. One summary sentence with up to **three reasons you fit**, mapped to the JD.
- **Middle (1–2 paragraphs)**: *why this company/team* (specific: product, technical problem, scale, a blog post — not "industry leader") and *why you*: 1–2 concrete examples (project/system, what you did, numbers) that match the JD's top requirements. Do not retell the resume; pick the evidence and connect it to their problems.
- **Closing**: reiterate interest and what you'd contribute, practical info if relevant (availability, location, work authorisation), thank them, say you look forward to discussing. "Sincerely," / "Best regards," + name.

## Style
- It is a writing sample and a marketing tool: confident, concrete, factual, active verbs.
- First person is fine, but don't start every sentence with "I"; put the reader/company in the sentence.
- No filler or flowery language: no "genuinely", "passionate", "I believe", "dynamic team", "I am writing to express my interest", no epigram-style closers.
- Reader's shoes: what convinces them you can do *this* job from day one (the "safe hire" signal)?
- Mirror JD keywords naturally; each claim backed by an example.

## Review checklist
- [ ] Named recipient, correct company/role everywhere (no leftover name from another letter)
- [ ] ≤1 page, same font as resume, PDF renders correctly
- [ ] Opening states role + 3 reasons; middle has company-specific "why" + 1–2 quantified examples; closing thanks + next step
- [ ] Nothing invented; no filler phrases; no resume rehash
- [ ] Spelling/grammar checked
