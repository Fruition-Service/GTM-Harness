---
sop: approval-gates
cited_by: [skills/fulfillment, skills/campaign-reports]
status: draft-v1
owner: Thana (Reachly team) — review with Josh before treating as final
---

# Approval Gates (SOP)

The checkpoints a `skills/fulfillment/` run stops at, and who signs off at
each one. Modeled on the delivery SOP's "align scope before build, no
surprises" principle (`knowledge/company/delivery-sop.md` §1), applied to
outbound instead of client delivery.

| Gate | What's being approved | Owner | Cites |
|---|---|---|---|
| 1. ICP finalized | Rubric matches target market, signals are real, exclusions correct | Reachly team + 1 Director spot-check | `sops/lead-verification.md` Gate 1 |
| 2. List segmented | Bucket assignment spot-checked, no fabricated/malformed rows | Reachly team member who ran segmentation | `sops/lead-verification.md` Gate 2 |
| 3. Copy approved | Voice, claims, personalization, spam-check, compliance all pass | Reachly team member (persona QA) | `sops/persona-qa.md` |
| 4. Launch / upload | Dedupe confirmed, sender accounts attached, schedule set, campaign in correct state (Smartlead ACTIVE / HeyReach not stuck in DRAFT) | Reachly team member launching + sign-off from whoever owns the target account/workspace | — |
| 5. Report shared externally | Numbers reconciled against the platform dashboards, no unverified claims | Whoever compiled the report + Josh (if going to a Director-level audience) | — |

## Rules

- **No skipping gates under time pressure.** If a motion is behind
  schedule, escalate the timeline — don't skip Gate 1 or 3 to catch up.
  This mirrors the delivery SOP's "raising a problem at 20% of hours is
  professionalism; discovering it at 90% is a crisis" principle.
- **A failed gate returns to the owning skill**, not a manual patch. If
  copy fails persona QA, it goes back to `skills/campaign-copy/` for
  another pass, not a one-off manual edit that the skill never learns
  from.
- **Gate 4 is dedupe-on-upload's enforcement point.** `pipeline/dedup.py`
  must have run against the current `outbound-motions/_LEDGER.md` mapping
  before Gate 4 can pass — this is a hard directive
  (`AGENTS.md` §1.1), not a judgment call.
- **New motions inherit these gates unchanged.** Don't loosen approval
  gates to move faster on later motions once the pilot is proven — the
  gates exist independent of how many times the loop has run.
