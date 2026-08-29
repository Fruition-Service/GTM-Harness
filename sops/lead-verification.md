---
sop: lead-verification
cited_by: [skills/icp, skills/list-segmentation]
status: draft-v1
owner: Thana (Reachly team) — review with Josh before treating as final
---

# Lead Verification (SOP)

Human checklist that gates a motion's ICP rubric and segmented lists before
they move downstream (rubric → `list-segmentation`; segmented list →
`campaign-copy`). This is the check that keeps `skills/icp/` and
`skills/list-segmentation/` from silently drifting off Fruition's actual
target market.

## Gate 1 — ICP rubric sign-off (before it's used to score any list)

1. **Target-market match.** Confirm the rubric's firmographic bounds match
   `knowledge/company/vision.md`: 25–25,000 staff, and the vertical list is
   drawn from {construction, manufacturing, professional services, NFP,
   government} unless there's a documented reason to test a new vertical.
2. **Signal sources are real.** Every buying signal in the rubric (recent
   hire, funding event, tool-stack indicator, etc.) must name where it's
   sourced from (AI Arc, Clay enrichment, LinkedIn Sales Navigator, etc.) —
   no signal that can't be traced to a real data source.
3. **Exclusions are explicit.** Confirm the exclusion list covers: existing
   Fruition/OG Labs/Senzo clients, active deals in any regional CRM board,
   competitors, and any account already in another motion's dedupe pool
   (`outbound-motions/_LEDGER.md`).
4. **Orange Bucket is separated.** Confirm existing monday.com accounts
   (Orange Bucket, per `knowledge/company/sales-process-sop.md` §5) are
   scored on a distinct path from net-new cold accounts, not blended into
   one rubric.

Sign-off: one person from the Reachly team + one Director spot-check
before the rubric is used to score a live list.

## Gate 2 — segmented list spot-check (before handoff to campaign-copy)

1. **Sample size:** pull a random 5% (minimum 20 records) of each bucket
   and manually verify firmographic fit against the ICP rubric.
2. **Data quality:** check for obviously malformed records (missing
   company name, placeholder emails, duplicate rows within the same
   upload) — these should have been caught by `pipeline/clean_normalize.py`
   and `pipeline/dedup.py`; if they weren't, that's a pipeline bug to
   report, not something to hand-fix in the list.
3. **Decision-maker seniority:** spot-check that contacts are the actual
   decision-makers/champions the ICP rubric targets, not arbitrary
   employees at a fit company.
4. **No fabricated or placeholder leads.** Every row must trace back to a
   real source-of-truth pull (AI Arc / Clay / manual research) — never
   synthetic or example data, in any environment, including test runs.

Sign-off: Reachly team member who ran the segmentation, before the list is
handed to `skills/campaign-copy/`.

## Escalation

If a rubric or list fails either gate, it goes back to `skills/icp/` or
`skills/list-segmentation/` for rework — it does not proceed with a
"we'll fix it in copy" workaround. Escalate to the sales rep attached to
the motion if the failure suggests the underlying ICP definition itself is
wrong, not just an execution error.
