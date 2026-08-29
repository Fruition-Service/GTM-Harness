---
skill: fulfillment
status: draft-v1
gate: sops/approval-gates.md (all gates)
---

# fulfillment

Orchestrates a full motion run end-to-end. This is the skill
`AGENTS.md` routes "set up / refresh a motion end-to-end" requests to.

> **Status:** draft v1 — the sequencing below is a reasonable first pass;
> the individual skills it calls are themselves draft-v1. Treat a full
> run as something a human watches closely, not something to leave
> unattended, until each stage has been through a few real cycles.

## The loop

```
1. icp            → outbound-motions/<name>/icp/{avatar.md, lead-fit-rubric.md}
2. pipeline/       → source_leads.py → enrich.py → clean_normalize.py
                     (raw → cleaned, enriched leads in data/, gitignored)
3. list-segmentation → outbound-motions/<name>/lists/*.csv
4. campaign-copy   → outbound-motions/<name>/copy/*.md
5. dedup + launch  → pipeline/dedup.py → pipeline/prepare_upload.py (CSV)
                     or pipeline/launch_campaign.py (direct API)
6. campaign-reports → outbound-motions/<name>/reporting/*.md
```

## Step-by-step

**1. ICP.** If `outbound-motions/<name>/icp/` is empty or stale (rubric
predates the last two report cycles' findings), run `skills/icp/` first.
If it's current, skip straight to step 2 — don't regenerate a rubric that
hasn't been invalidated by new data.

**2. Pipeline.** Run `pipeline/source_leads.py`, then `enrich.py`, then
`clean_normalize.py` in order. Each writes to `data/<motion>/`
(gitignored) — never to a tracked path. `source_leads.py` and
`enrich.py` currently read from local export files (see their docstrings)
rather than live AI Arc/enrichment APIs — confirm the export is fresh
before running.

**3. List segmentation.** Run `skills/list-segmentation/` against the
cleaned+enriched output, scored by the ICP rubric from step 1. **Gate:**
`sops/lead-verification.md` Gate 2 before proceeding.

**4. Copy.** Run `skills/campaign-copy/` against the segmented lists —
one pass per bucket/role per §4 of that skill. **Gate:**
`sops/persona-qa.md` before proceeding.

**5. Dedupe and launch.** Run `pipeline/dedup.py` against
`outbound-motions/_LEDGER.md` — this is non-negotiable
(`AGENTS.md` §1.1). Then either `prepare_upload.py` (manual CSV import) or
`launch_campaign.py` (direct API push) depending on the platform and
whether a campaign already exists. **HeyReach note:** if creating a new
campaign via API, it lands in DRAFT — confirm it's been activated (via the
UI, per `knowledge/tool-docs/heyreach.md`) before treating step 5 as
complete. **Gate:** `sops/approval-gates.md` Gate 4.

**6. Reports.** Run `skills/campaign-reports/` on a weekly cadence once
the campaign is live, not just at the end of the loop — this is ongoing,
not a one-time step. **Gate:** `sops/approval-gates.md` Gate 5 before
sharing outside the Reachly team.

## When to stop and ask a human

- Any gate fails (see `sops/approval-gates.md`) — return to the owning
  skill, don't patch around it.
- A pipeline script hits `NotImplementedError` or a missing API
  credential — that's a real gap, not something to route around silently.
- HeyReach campaign creation returns a DRAFT campaign with no clear
  activation path — stop and activate manually rather than guessing at an
  undocumented endpoint (`knowledge/tool-docs/heyreach.md`).
- Anything that would touch a lead already in another motion's dedupe pool
  — that's exactly what `pipeline/dedup.py` + `_LEDGER.md` exist to catch;
  if it's catching something, don't override it.

## References

See `references/sources.md`.
