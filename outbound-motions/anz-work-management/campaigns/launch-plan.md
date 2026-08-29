---
motion: anz-work-management
status: **HeyReach side is already live** — corrected 2026-08-05, see below
---

# anz-work-management — Launch Plan

## Correction (2026-08-05)

This file originally said the motion "hasn't launched" and proposed a
`V4 - ANZ (Work Management)` naming placeholder. That was wrong. Pulling
the real HeyReach account (`HeyReachClient.get_campaigns()` /
`get_campaign_sequence()`) found campaign **`512925 — "V3 - ANZ (WM)"`,
status `IN_PROGRESS`** — Thana already has this motion's LinkedIn side
running in production. The actual live sequence is now documented in
`knowledge/company/linkedin-messaging-foundation.md`; the
`copy/linkedin-sequence-champion.md` drafted earlier in this repo is a
separate, independently-written hypothesis that was never checked against
the real thing — see `copy/README.md` for the reconciliation note.

**What's still genuinely open:**
- Smartlead side — not checked (`SMARTLEAD_API_KEY` wasn't set when this
  repo last pulled). Run `python3 -m pipeline.check_integrations` once it
  is, then check for an existing Smartlead campaign the same way this
  HeyReach one was found, before assuming email-side needs to be built
  from scratch.
- Whether this repo's ICP rubric / segmentation / dedupe pool are actually
  the ones driving leads into campaign `512925`, or whether Thana is
  sourcing leads some other way this repo doesn't yet touch. **Ask Thana**
  before assuming this repo's pipeline is upstream of the live campaign —
  it currently isn't wired to push into it.

## Naming convention (confirmed, not just observed)

`V<n> - <Region> (<Product>)`, product abbreviated (`Service`, `CRM`,
`WM`). Current generation is **V3** across all 9 region×product
combinations that are live — see
`knowledge/company/linkedin-messaging-foundation.md`'s source table.
Several `V2 -` campaigns are also still `IN_PROGRESS` for some combos
(legacy, being phased out per-region as V3 rolls out) — don't confuse
those with the current generation.

## HeyReach: already provisioned — do not re-create

- [x] Campaign exists — `512925`, `IN_PROGRESS`, sequence documented in
      `knowledge/company/linkedin-messaging-foundation.md` (the WM track).
      **Do not call `HeyReachClient.create_campaign()` for this
      motion/region/product — it would create a duplicate alongside the
      real one.**
- [ ] Confirm whether this repo's `skills/list-segmentation/` output is
      meant to feed `512925` via `AddLeadsToCampaignV2`, or whether Thana
      runs lead sourcing for it separately — **ask before wiring
      `pipeline/launch_campaign.py` against this campaign ID.**
- [ ] `outbound-motions/_LEDGER.md` — updated with `512925` (done,
      2026-08-05).

## Smartlead: unknown — check before assuming greenfield

- [ ] Set `SMARTLEAD_API_KEY`, run `python3 -m pipeline.check_integrations`,
      then `SmartleadClient().get_campaigns()` and look for the ANZ/WM
      equivalent before assuming `create_campaign()` is the right first
      move.

## Remaining provisioning gaps (whichever platform turns out to need them)

- [ ] Sender accounts / schedule / timezone — for HeyReach, `512925`'s
      current senders are account IDs `183384` and `177663` (from
      `get_campaigns()`); schedule wasn't pulled in this pass — fetch via
      `GetCampaignSequence`'s sibling schedule endpoint if it becomes
      relevant.
- [ ] Dedupe pool (`anz`, per `_LEDGER.md`) — still applies once this
      repo's pipeline is actually feeding either platform.

## Status

**HeyReach: live, pre-existing, not created by this repo.** Smartlead:
unknown. This motion is not a from-scratch launch — it's partially already
running, and the immediate next step is figuring out how this repo's
pipeline relates to what's already live, not provisioning a new campaign.
