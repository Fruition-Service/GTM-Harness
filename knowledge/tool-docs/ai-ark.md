---
type: reference
source: https://docs.ai-ark.com (llms.txt index + direct fetch of key reference pages)
retrieved: 2026-08-14
verified_by: llms.txt full endpoint index cross-checked against 6 individually-fetched reference pages; internally consistent (e.g. trackId flows between endpoints match)
---

# AI Ark — API notes

> **Name correction:** the original startup guide and this repo's earlier
> stub called this "AI Arc." The real product is **AI Ark**
> (`ai-ark.com` / `docs.ai-ark.com`) — a B2B company/people data and
> enrichment API. This file replaces the old `ai-arc.md` stub.

## Base URL & auth

```
Base URL: https://api.ai-ark.com/api/developer-portal
Auth:     header  X-TOKEN: YOUR_API_KEY
Required: header  Content-Type: application/json  (on every request)
```

Get your key from the AI Ark dashboard. `config/.env` (gitignored, see
`.env.example`):
```
AI_ARK_API_KEY=...
```

## Rate limits & credits

**5 requests/second, 300/minute, 18,000/hour** — stated per most
endpoints; export/email-finder endpoints additionally cap at **500
in-flight requests per token** (`400 too many pending requests` if
exceeded) with **10 concurrent** processed at once.

This is a **credit-metered** API, unlike Smartlead/HeyReach — check
`GET /v1/payments/credits` before running a large pull:
```
→ 200: {"total": 100}
```

## Verified live (2026-08-30, real API key)

`GET /v1/payments/credits` and `POST /v1/companies` (Company Search)
confirmed working against a real account. **Credit cost of search is
unconfirmed either way — don't assume it's free.** One single
before/after check showed no change, but roughly a dozen `search_companies()`
calls across this same testing session (30,000 → 29,997 credits) suggest
*something* cost 3 credits total — possibly search itself at a very small
rate, possibly unrelated account activity. Not enough evidence to state a
real number. If credit cost matters for a large sourcing run, check
`get_credit()` immediately before and after your own real call rather
than trusting either claim here.

Two real gotchas found only by testing, one worse than the other:

1. **A plain array for `location` gets `400 "request not readable"`.**
   Needs the `{"any": {"include": [...]}}` wrapper (like `domain`), not a
   bare array — this doc previously showed `location` as `[...]`, which
   is wrong and has been corrected below.
2. **`industries` silently returns unfiltered results if you don't use
   the full `{"mode": "SMART", ...}` shape — no error, just wrong
   results.** Tested directly: `{"industries": {"include": ["construction"]}}`
   returns `200` with 36,114 matches (clearly unfiltered — Redbubble,
   BaptistCare, a bank, a water utility, none construction). The correct
   shape, `{"industries": {"any": {"include": {"mode": "SMART", "content":
   ["construction"]}}}}`, returns `200` with 2,741 matches, genuinely
   construction companies (Clough, Metricon, Built, Coates — all real ANZ
   construction firms). **This is the more dangerous failure mode of the
   two** — a 400 is obvious, a silently-wrong 200 is not. Don't trust a
   filter is actually being applied just because the request succeeded;
   spot-check the results, especially for any field not yet confirmed
   here.

Given these two surprises on the two fields tested so far, treat every
other filter field in the surface below as **unverified until tested the
same way** — don't assume `{"any": {"include": [...]}}` is the universal
shape.

## The two-step pattern this API wants you to use

Search endpoints (`/v1/companies`, `/v1/people`) are synchronous and
**do not include email** — they return profile/company data plus (for
people) a `trackId`. Getting verified emails is a **separate,
credit-charged, async step**:

1. **Search** (`/v1/companies` or `/v1/people`) — find who matches your
   ICP. Free-ish (search itself), returns profiles + a `trackId`.
2. **Export with email** — either:
   - `POST /v1/people/export` — re-run the *same filters* as a bulk async
     export (up to 10,000 results, submit a `webhook` URL), **or**
   - `POST /v1/people/export/single` — export one specific person by `id`
     or LinkedIn `url` (real-time, 1 credit, 0 if no email found), **or**
   - `POST /v1/people/email-finder/{trackId}` (exact path per llms.txt:
     "Find Emails by Track ID") — resume email-finding on a search you
     already ran, using its `trackId`. **`trackId` is single-use and
     expires 6 hours after the original search.**
3. **Poll or wait for webhook** — export/email-finder jobs return
   `{trackId, state: "PENDING", statistics: {total, found}}` immediately;
   poll `GET /v1/people/export/{trackId}/inquiries` (paginated results) or
   `.../statistics` for progress, or just handle the webhook POST.

**All emails are verified in real time by BounceBan** (their words) —
both SMTP and CATCH_ALL results. Charged 0 credits if no valid email is
found, on the export-with-email and single-export endpoints.

**Clay-compatible v2 variants exist** for two endpoints
(`/v2/people/mobile-phone-finder`, `/v2/people/export/single`) that
return **HTTP 200 with `{status, error, data: null}`** on a not-found,
instead of v1's `404` — use v2 if consuming this from something that
chokes on 404s (Clay does; a Python client doesn't need to care either
way, `HeyReachClient`/`SmartleadClient`-style `raise_for_status()` handles
v1's 404 fine).

## Company Search

```
POST /v1/companies
Body: {
  "page": 0, "size": 10,                    // required; size max 100
  "account": {
    "domain": {"any": {"include": ["acme.com"]}},
    "industries": {"any": {"include": {"mode": "SMART", "content": ["construction"]}}},
    "location": {"any": {"include": ["Australia"]}},
    "employeeSize": {"type": "RANGE", "range": [{"start": 25, "end": 2000}]},
    "type": [...], "foundedYear": {...}, "revenue": [...], "technology": [...],
    "naics": [...], "keyword": {...}, "funding": {...}
    // full filter surface: domain, linkedin, url, name, socialMediaLink,
    // phoneNumber, industries, location, productAndServices, socialMedia,
    // type, foundedYear, employeeSize, revenue, language, geoLocation,
    // keyword, funding, metric (headcount growth), technology, naics
  },
  "lookalikeDomains": ["acme.com"],           // optional, max 5 — "find companies like this one"
  "lists": {"company_id": {"exclude": ["<list-id>"]}}   // optional, exclude by list
}
→ 200: {"content": [ {id, summary: {name, legal_name, description, founded_year,
         type, industry, staff, logo}, link: {website, domain, linkedin, twitter,
         crunchbase}, contact: {email, phone}, financial: {funding: {rounds: [...]}},
         location: {headquarter, locations: [...]}, technologies: [{name, category}],
         industries, keywords, languages, sic, naics, last_updated} ],
        pageable, totalElements, totalPages, first, last, empty}
```

**Directly maps to `skills/icp/instructions.md`'s lead-fit rubric**:
`employeeSize` → firmographic fit band (25–2,000 for `anz-work-management`,
per `icp/lead-fit-rubric.md`); `industries`/`naics` → vertical match;
`metric` (headcount growth) → the "recent headcount growth" buying
signal; `technology` → the "confirmed monday.com usage" Orange Bucket
check (search `technology` for monday.com and route matches separately
per `skills/list-segmentation/instructions.md` §1) or the "tool-sprawl"
signal if it finds competing/adjacent tools instead.

## People Search

```
POST /v1/people
Body: {
  "page": 0, "size": 10,
  "account": { ... same AccountFilter as Company Search ... },
  "contact": {
    "seniority": {"any": {"include": ["founder", "vp", "director"]}},
    "departmentAndFunction": {...},           // e.g. Operations, Project Management
    "experience": {"current": {"title": {...}}},
    "location": {"any": {"include": ["Australia"]}},   // same {any:{include:[...]}} wrapper as Company Search, not a plain array
    "fullName": {"any": {"include": {"mode": "SMART", "content": ["..."]}}}
    // full filter surface: fullName, socialMediaLink, company (latest/
    // current/previous), seniority, location, linkedin, departmentAndFunction,
    // skill, certification, keyword, socialMedia, language, education,
    // profileBadge, socialMediaFollower, experience
  }
}
→ 200: {"content": [ {id, identifier, profile: {first_name, last_name, full_name,
         headline, title, ...}, link: {linkedin, twitter, github, facebook},
         location, industry, educations, certifications, position_groups
         (employment history), skills, member_badges, company: {...full company
         object...}, department: {departments, sub_departments, functions, seniority},
         statistics: {network: {followers_count, connections_count}}, last_updated} ],
        pageable, totalElements, totalPages, trackId, ...}
```

**No email in this response** — see "two-step pattern" above.
`department.seniority` and `department.functions` are what
`skills/icp/instructions.md`'s "Champion accessibility" rubric category
and the economic-buyer/champion/influencer role split
(`skills/campaign-copy/instructions.md` §4) should filter on.

## Export people with email (the bulk-sourcing endpoint)

```
POST /v1/people/export
Body: {
  "account": {...}, "contact": {...},   // same filters as People Search
  "page": 0, "size": 2000,               // size max 10,000 for exports
  "webhook": "https://your-endpoint/ai-ark-callback"   // optional
}
→ 200: {"trackId": "...", "statistics": {"total": N, "found": N},
        "webhook": {"state": "PENDING", "retry": null}, "state": "...", "description": null}
```

Then poll:
```
GET /v1/people/export/{trackId}/inquiries?page=0&size=100
→ paginated results; each item has an `email: {state: "DONE"|"PROCESSING",
  output: [{address, verification/MX details}]}` block once processing completes
GET /v1/people/export/{trackId}/statistics
→ {"total": N, "found": N, "state": "..."}  (poll until state is terminal)
```

**409** on results/statistics = still processing, not an error to
surface. **403** = the submission was auto-refunded (charged but never
delivered within the 10-hour window) — not retrievable, resubmit.
**Auto-refund is automatic**, not something this client needs to trigger.

This endpoint is the real replacement for `pipeline/source_leads.py`'s
current file-based "drop a CSV in `data/<motion>/imports/`" stand-in —
see `pipeline/integrations/ai_ark_client.py`.

## Single-person export (real-time, for one lead at a time)

```
POST /v1/people/export/single
Body: {"id": "<ai-ark-uuid-from-a-prior-search>"}   // or {"url": "<linkedin-profile-url>"}
→ 200: real-time result with email; 404 if no email found
→ v2 (Clay-compatible): POST /v2/people/export/single — 200 with
  {status, error, data: null} instead of 404 on not-found
```
1 credit per call, 0 if no email found. Useful for
`pipeline/personalization/evidence_lines.py`-adjacent single-lead
enrichment rather than a full re-export.

## Exclude lists (relevant to dedupe-on-upload)

```
POST /v1/lists
Body: {"id": "<optional, to update>", "type": "people_id" | "company_id",
       "values": ["<ai-ark-id>", ...], "mode": "APPEND" | "REPLACE"}
→ 200: {"id": "...", "workspace": "...", "type": "...", "values": [...], "created": <epoch ms>}
```
Max **50 lists/day**, **10,000 items/list**, lists **expire after 24
hours**. Reference a list's `id` in Company/People Search's
`lists.{people_id,company_id}.exclude` to skip already-known records.

**Important limitation for this harness:** lists exclude by **AI Ark's
own internal `id`** (a UUID per person/company), **not by email**. This
doesn't directly replace `pipeline/dedup.py`'s email-based "contacted"
ledger (`outbound-motions/_LEDGER.md`'s dedupe pools) — the two operate
on different keys. It's still useful as a *second, upstream* dedupe layer
(skip re-searching people you've already exported this month) but
`pipeline/dedup.py`'s email-based check remains the authoritative
dedupe-on-upload enforcement point per `AGENTS.md` §1.1. Don't treat AI
Ark list-exclusion as sufficient on its own.

## Other endpoints (documented in the llms.txt index, not individually fetched)

- `POST /v1/people/mobile-phone-finder` (+ `/v2/...` Clay-compatible
  variant) — phone enrichment; 5 credits if found, 0 if not.
- `POST /v1/people/analysis` — "Personality Analysis API" from public
  profile data.
- `POST /v1/people/reverse-lookup` — find a person from an email/phone
  (`kind`: CONTACT, `search`: the value).
- Submission-history endpoints: `GET .../export/submissions`,
  `GET .../email-finder/submissions` — list your own past export/
  email-finder jobs with refund status.
- Webhook resend endpoints for both export and email-finder flows.
- `docs.ai-ark.com/reference/mcp` — AI Ark also exposes an MCP server, if
  a future agent runtime here wants to call it directly rather than
  through `pipeline/`.

## Used by

- `pipeline/integrations/ai_ark_client.py` — wraps Company Search, People
  Search, Export-with-email (+ polling), and Fetch Credit.
- `pipeline/source_leads.py` — now calls this API for company+people
  discovery when `AI_ARK_API_KEY` is set, falling back to the file-import
  path documented there when it isn't.
- `pipeline/enrich.py` — the local best-effort logic stays as a fallback;
  when a real AI Ark export result is available it takes precedence (real
  verified email > guessed-from-domain website).
