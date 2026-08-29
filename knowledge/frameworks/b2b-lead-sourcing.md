---
type: framework
status: draft-v1
source: benchmarked against a reference GTM-harness structure ("How we Run GTM at AptAI Systems"), adapted for Fruition's actual tooling
---

# B2B lead sourcing — the three pillars

A useful way to think about where leads come from, independent of any one
tool:

1. **Database** — structured company/people data behind an API, queried by
   firmographic/demographic filters (size, industry, title, seniority).
2. **Signals** — trigger events that indicate buying intent right now
   (recent hire, job posting, funding round, headcount growth) — the same
   database can often surface these, but it's a distinct *kind* of filter
   from static firmographics.
3. **Scraping** — pulling structured data out of unstructured web sources
   (job boards, company sites, review sites) that a database provider
   hasn't indexed.

## Where this harness stands on each pillar

| Pillar | Tool | Status |
|---|---|---|
| Database | AI Ark (`knowledge/tool-docs/ai-ark.md`) | **Wired.** `account.*` filters in `pipeline/integrations/ai_ark_client.py` — employee size, industry, NAICS, revenue, technology. |
| Signals | AI Ark | **Wired.** `account.metric` (headcount growth), `contact.experience` (recent title change) filters — same client, same endpoint. |
| Scraping | — | **Not wired. Open decision, not a gap to silently fill.** |

## The scraping gap — a real decision, not an oversight

The reference structure this was benchmarked against uses a scraping tool
(Firecrawl) as a third, independent lead-sourcing pillar alongside a
database and signals. This harness doesn't have an equivalent, and
**shouldn't get one without Thana/Josh choosing a tool** — adding an
unverified scraping integration here would repeat the exact mistake this
repo has avoided for every other integration (Smartlead, HeyReach, AI Ark
were only wired after real, fetched documentation existed, never guessed
at). If scraping becomes a priority:

1. Pick a tool (Firecrawl is a reasonable default given precedent
   elsewhere, but that's not this repo's call to make unilaterally).
2. Research its real API the same way `knowledge/tool-docs/ai-ark.md` was
   built — live docs, not memory.
3. Add `pipeline/integrations/<tool>_client.py` following the existing
   pattern (`_http.py` shared retry logic, `config/.env` key, wired into
   `check_integrations.py`).

Until then, **Database + Signals (AI Ark) cover this harness's sourcing**
— that's a real, working two-thirds of the framework, not a gap that
blocks anything currently planned.

## Used by

- `pipeline/source_leads.py` — the Database/Signals implementation.
- `skills/icp/instructions.md` §5 — signal sourcing notes.
- `outbound-motions/anz-work-management/research/source-register.md` —
  per-motion instantiation of which signal maps to which AI Ark filter.
