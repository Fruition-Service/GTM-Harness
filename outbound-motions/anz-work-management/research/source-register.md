---
motion: anz-work-management
status: draft-v1
---

# anz-work-management — Source Register

Where each buying signal in `icp/lead-fit-rubric.md` actually comes from,
and its reliability. This is the register `pipeline/source_leads.py` and
`pipeline/enrich.py` should be pointed at — populate the "status" column
as each source actually gets wired up. **No evidence entries in this
folder should ever be fabricated or placeholder** — this file records
where evidence comes from, not the evidence itself.

| Signal | Source | Status | Notes |
|---|---|---|---|
| Recent Ops/PM hire | AI Ark | **Wired** — `pipeline/source_leads.py` via `AIArkClient.search_people(contact={"experience": ...})`, once real `--filters` JSON exists for this motion | Corrected name (was "AI Arc"); see `knowledge/tool-docs/ai-ark.md` |
| Active PM/Ops job posting | AI Ark | Not wired | AI Ark's `metric`/`keyword` filters may cover this — not confirmed; check `knowledge/tool-docs/ai-ark.md`'s Company Search filter surface before assuming |
| Headcount growth (6-12mo) | AI Ark | **Wired (untested)** — `account.metric` (headcount growth) filter in Company/People Search, see `knowledge/tool-docs/ai-ark.md` | Filter exists per docs; not yet exercised against a real motion's rubric |
| Named champion contact | AI Ark People Search | **Wired** — `contact.seniority`/`contact.departmentAndFunction` filters, `pipeline/source_leads.py` | |
| Monday.com usage confirmation | AI Ark | **Wired (untested)** — `account.technology` filter can search for "monday.com" as a detected technology | Feeds the Orange Bucket routing check; whether AI Ark's technology detection actually catches monday.com specifically is unconfirmed |
| Company firmographics (size, vertical) | AI Ark Company/People Search | **Wired** — `account.employeeSize`, `account.industries`, `account.naics` | |
| Verified email | AI Ark | **Wired** — `pipeline/enrich.py` via `AIArkClient.export_single_person()`, real-time, credit-metered | Replaces the local domain-guessing fallback when `AI_ARK_API_KEY` is set |

**Wired but not yet live-tested end-to-end:** no `AI_ARK_API_KEY` was
available when this was written — the client and pipeline wiring are
built and unit-tested against the documented response schemas
(`knowledge/tool-docs/ai-ark.md`), but never called with a real key. Run
`python3 -m pipeline.check_integrations` once a key is added (that script
should be extended to check AI Ark too — currently only checks
Smartlead/HeyReach).

## Proof catalog (for personalization lines)

`pipeline/personalization/evidence_lines.py` reads per-lead evidence from
here once sourcing is live. Structure for each entry, when real:

```
company: <name>
signal_type: <hire | funding | job-posting | headcount-growth | other>
signal_detail: <specific, factual — e.g. "hired Ops Manager, June 2026">
source: <where this was found>
source_url: <link, if public>
sourced_date: <YYYY-MM-DD>
confidence: <high | medium | low>
```

No rows exist here yet — this is the schema, not data. Do not fill this
file with example/placeholder companies; leave it empty until
`pipeline/source_leads.py` produces real evidence.

## QA checklist for evidence before it reaches copy

1. Is the signal specific and factual, not inferred/guessed?
2. Is it recent enough to still be true (<90 days for hire/job-posting
   signals, per `icp/lead-fit-rubric.md`)?
3. Does the source URL (if any) actually support the claim?
4. Would this line survive the prospect Googling it themselves?

If any answer is no, the evidence doesn't go into a personalization line —
`skills/campaign-copy/` falls back to a generic-but-honest opener instead
of a specific-but-shaky one.
