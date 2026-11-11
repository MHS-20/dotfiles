---
name: job-application
description: Find new job postings efficiently (LinkedIn guest API + Greenhouse/Lever/Ashby boards, deduped against tracker/seen-urls.txt), keep tracker/active.md and tracker/applied.md up to date, fill a job application form in the browser from the local profile/resume/letters, then, once the user confirms it is submitted, research the company and write a short brief with interview questions to submitted/. Use when the user asks to search for new jobs, apply to a job, fill an application, manage the tracker, or says an application was submitted.
---

# Job application

**Base directory:** `/home/sentinel/Work/Offers` (job-search HQ). Every relative path below (`tracker/…`, `submitted/…`, `letters/…`, `applicant_profile.md`, `files/…`, `../Resume/…`, `../Personal/…`) is relative to it; use absolute paths when working from another directory.

Follow the rules in `/home/sentinel/Work/Offers/CLAUDE.md` (one application at a time, never submit/consent/log in, ask for missing fields and add them to `applicant_profile.md`).

## 0. Tracker layout (never create new list files)

| File | Use |
|---|---|
| `tracker/active.md` | The only working list (~20–40 rows): found, not yet sent/skipped. Columns: Company, Role, City, YoE, Resume, Link, Found, Note. |
| `tracker/applied.md` | One row per sent application: Sent, Company, Role, Location, Resume, Brief link, Outcome (sent → OA / interview / offer / rejected / no reply after ~4 weeks). |
| `tracker/seen-urls.txt` | Every job URL/ID ever scanned. Dedupe against it; append every scanned ID. Never read by hand. |
| `tracker/archive/` | Frozen old lists. Only to look up a past skip reason. |

- **Apply:** move the row `active.md` → `applied.md`.
- **Skip:** delete the row from `active.md` (ID stays in `seen-urls.txt`).
- **Housekeeping on each scan:** drop `active.md` rows older than ~4 weeks never acted on.
- Before proposing a role, check its company against `applied.md` (the user does not want companies already applied to unless they ask) and the memory files (no Palantir, no observability-only/pure-ops roles).

## 0b. Finding new roles (efficient scan)

Use structured endpoints via `curl`/Python, not page-by-page browsing. Save intermediate JSON in the scratchpad; only the distilled picks go to `active.md`.

1. **LinkedIn guest search** (no login): `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<kw>&location=<loc>&f_E=1,2,3&f_TPR=r1209600&start=<0|25|50>`
   - `f_E` levels: 1 internship, 2 entry, 3 associate, 4 mid-senior. `f_TPR=r1209600` = last 14 days (r604800 = 7 days). `start` pages by 25.
   - Each card has `data-entity-urn="urn:li:jobPosting:<ID>"`, title (`base-search-card__title`), company (`base-search-card__subtitle`), location, `datetime`.
   - Scripts: `tracker/li_scan_backend.py` (backend keywords; current default) and `tracker/li_scan.py` (broader). Run: `python3 -I tracker/li_scan_backend.py tracker/seen-urls.txt <scratch>/out.json`. Edit `KWS`/`LOCS` in a scratch copy for other searches. 6 threads × ~700 queries is fine.
2. **Filter in code, then by eye:** `python3 -I tracker/filter_scan.py <scratch>/out.json > <scratch>/cand.txt` drops off-target titles (senior/lead, frontend/mobile/ML/data, test/embedded/PLC, devops/SRE/observability/sysadmin…), staffing agencies/consultancies, and companies already in `applied.md`. Extend its regexes when new agencies show up. Then keep only medium-to-high quality product/tech/finance companies by eye.
3. **Read the JD only for finalists:** `https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<ID>`; regex out "N+ years / anni / Jahre", "graduate", "no longer accepting". Fetch **sequentially with ~2.5 s sleep**: parallel fetches hit HTTP 429 after ~20 requests. Drop roles asking ≥3 YoE.
4. **Company ATS boards** (complete, structured; good for companies LinkedIn misses, e.g. Italian scale-ups):
   - Greenhouse `https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true`
   - Lever `https://api.lever.co/v0/postings/<slug>?mode=json`
   - Ashby `https://api.ashbyhq.com/posting-api/job-board/<slug>?includeCompensation=true` (shows pay band and deadline; check them)
   - Apply URLs: Greenhouse `job-boards.greenhouse.io/<slug>/jobs/<id>` (embedded forms: `boards.greenhouse.io/embed/job_app?for=<slug>&token=<id>`), Lever `<hostedUrl>/apply`, Ashby `<jobUrl>/application`.
5. **Finish:** append all scanned IDs to `seen-urls.txt` (with a `# scan <date>` header), add picks to `active.md` with Found date, report a short ranked list to the user (Italy first when the user asks for it).

Notes: `grep` on this machine is ugrep (rejects some long regexes); do text extraction in Python. Bologna/Emilia results are mostly agencies and industrial automation; Milan has most Italian backend roles.

## 1. Fill the form
1. Read the job post. Pick the resume variant and, if asked for, build the cover letter (see `CLAUDE.md`).
2. Fill the form from `applicant_profile.md`, `../Personal/*.md`, `trascript.pdf`.
3. Stop and hand over to the user to review and press Submit.

## 2. After the user confirms submission
1. Move the row from `tracker/active.md` to `tracker/applied.md` (date, resume, brief link, outcome `sent`).
2. Research the company (WebSearch/WebFetch): engineering blog (most popular + role-relevant posts), stack, products, open source, culture, new-grad onboarding. Stick to sources; no guessing.
3. Write `submitted/<YYYY-MM-DD>-<company>-<role-slug>.md` using the template below. Keep it short: bullets, ≤ ~40 lines total.

```markdown
# <Company> — <Role>

- **Location:** <city, country (hybrid/remote)>
- **Sent:** <YYYY-MM-DD>
- **Post:** <url>
- **Resume / letter:** <../Resume/resume-x.pdf> / <letters/... or none>

## Role
<1–2 lines: team, what you'd build, key requirements>

## Company
- **Products:** <what they sell, scale>
- **Stack:** <languages, infra, data tools; built in-house vs bought>
- **Open source:** <notable projects/contributions>
- **Culture:** <eng practices, values, work model>
- **Blog reads:** <2–3 posts: title — one-line takeaway (link)>

## Questions to ask
1. <specific, tied to a blog post or tool: why they built X instead of Y, its limits>
2. <stack/process decision: build vs buy, how decided>
3. <new-grad onboarding: first projects, ramp-up>
```

Questions must reference something concrete found in the research, not generic ones.
