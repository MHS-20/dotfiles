---
name: reverse-interview
description: Prepare questions to interview the company back — assess a team's engineering standards, culture, manager, on-call, growth and company health — and interpret the answers. Use when the user asks what to ask at the end of an interview, wants to evaluate a company/team/offer, prepares a team-match or post-offer call, or asks whether a company is a good place to work.
---

# Reverse interviewing

Sources: Gergely Orosz, The Pragmatic Engineer — "Reverse interviewing" (2021/22) and "The Pragmatic Engineer Test" (12 questions); viraptor/reverse-interview (GitHub, CC BY-SA 4.0).

## When and with whom
- **During interview rounds** (the "any questions?" slot): 2–3 *safe but revealing* questions per interviewer, tailored to their role. Shows interest; avoid comp/PTO here.
- **After the final offer, before accepting** (the real reverse interview): you have leverage now. Order: **negotiate money first → reverse interview → decide.**
  - Ask the recruiter for 30-min 1:1s with: the **future manager**, the **most senior engineer** on the team, and **at least one future peer**. Frame it as "understanding the work, culture and career before deciding", not about the offer.
- Comp, benefits, PTO, visa/relocation, runway → recruiter/HR, not engineers.
- Practices differ per team: always ask about **the team you'd join**, not the company.

## Workflow
1. Research first (engineering blog, Glassdoor/Blind, Levels.fyi, layoffs news, funding, GitHub, recent launches); don't ask what's public. If the company has a brief in `~/Work/Offers/submitted/`, read it and append the questions there.
2. Pick **10–15 questions** (not the whole list) by the user's priorities and the stage; tailor wording to the company/interviewer.
3. Always follow up: **"what caused that?"**, **"how often?"**, **"can you give a recent example?"** — the signal is in the follow-ups and in pauses/deflection.
4. After the calls: score with the Pragmatic Engineer Test and the flags below; summarise for the user (strengths, red flags, unknowns, things to negotiate).

## Question bank

### The work and the team
- What were the last 3 projects the team shipped? (dig into one) Which are you proudest of?
- What's the biggest struggle right now, and why?
- Walk me through a typical week last month. What makes a good day vs a bad day? How often are bad days, and what causes them?
- What are you most excited about in the next 6 months? Open unsolved challenges?
- Who sets priorities? What happens on pushback ("can't be done in time") or a missed deadline?
- How are disagreements resolved? Tell me about a tough/toxic situation and how it was handled.
- Has anyone left the team recently, and why? What did new joiners struggle with?
- What would make me successful here? What's expected at 1 and 3 months?

### Engineering standards
- **Can you show me a recent non-trivial code review?** Look at: context in the description, tone, depth, who reviews, turnaround, tests included, CI running automatically.
- Life of a commit: from laptop to production — CI, staging, canaries, manual vs automatic deploy, rollback. How often do you deploy?
- Testing strategy and coverage; how long to set up the local environment?
- Monitoring/alerting/observability; infra as code; dependency and security-patch policy.
- Design docs / ADRs: who writes them, who reviews? Tech-debt time?
- Do engineers contribute to the roadmap? Do they talk directly with PMs/other teams, or only through managers?
- Code ownership: can I send a PR to another team's repo?

### On-call and incidents
- On-call rotation size, pages per week, night pages; is it paid?
- Is on-call health measured, and does fixing it beat feature work?
- Last incident: what happened, was the postmortem blameless, were action items done?

### Manager and growth
- Manager: what's your management style? How do you give feedback? Regular 1:1s? Are you (were you) an engineer?
- Peer: how supportive is the manager? What do they do well / could do better?
- Is there a career ladder with defined levels? Parallel IC/manager track?
- How do promotions and performance reviews work? Who was promoted last, and why?
- When did you last see someone grow a lot here, and how?
- Learning budget, conference time, mentorship, open-source policy?

### Company health and direction
- How does the company make money? Profitable? Runway / funding? (recruiter or senior people)
- Why is this role open? Growth or backfill? Why external vs internal?
- How often are there reorgs / priority shifts? Any layoffs recently, and how were they handled?
- 1-year plan; biggest competitive threat.

### Culture and logistics
- Why did you join, and why do you stay? Best and worst thing here? What would you change?
- Remote/hybrid policy and how strict; core hours; work-life balance in practice (late messages, weekend work).
- (Recruiter) Equity/bonus structure and typical payout, PTO, parental leave, relocation, visa support, hardware.

## Pragmatic Engineer Test (score per team, yes/no)
1. Equity or meaningful profit sharing for all engineers
2. Roadmap/backlog engineers contribute to
3. Engineers work directly with other ICs, not only via managers
4. Code review and testing are routine
5. CI, and CD or push-button deploy by engineers
6. Internal open source / clear code ownership
7. Healthy on-call, measured and prioritised
8. Technical managers
9. Career ladder (expected above ~10 engineers)
10. Parallel IC/manager tracks (above ~30)
11. Peer feedback / 360 / surveys acted on (2 of 3, above ~30)
12. Learning: budget, recognised time, mentorship (2 of 3)
Small startups (<20 eng) can lack 9–11 plausibly; that excuse fades with size.

## Flags
**Green**: concrete answers with examples; a real, polite, thorough code review shown; frequent safe deploys; measured on-call; recent specific promotion stories; departures explained candidly; engineers shape the roadmap; manager talks about your growth unprompted.

**Red**: "good day" = no fires; firefighting/constant pages/changing requirements; refusing to show a code review (~20% do); vague or evasive on turnover, runway, reorgs; can't name a hard situation; nobody promoted recently / no ladder at scale; everything routed through managers; deflecting technical questions to the recruiter; "we're like a family"; answers differ sharply between manager and peers.

## Output
- Pre-interview: a short, prioritised question list per person (manager / senior / peer / recruiter), 10–15 total, with a note on what a good vs bad answer looks like.
- Post-call: Test score, green/red flags with the evidence heard, open unknowns, and points worth raising in negotiation.
