---
skill: list-segmentation
status: draft-v1
gate: sops/lead-verification.md (Gate 2)
---

# list-segmentation

Takes the cleaned, enriched, ICP-scored lead list (output of
`pipeline/clean_normalize.py` scored against `skills/icp/`'s rubric) and
splits it into buckets, written to `outbound-motions/<name>/lists/`.

> **Status:** draft v1. Bucket logic below implements the tiers defined in
> `skills/icp/instructions.md` §3 — if that rubric changes, this changes
> with it. Review with Avi/Thana before treating as final.

## 1. Primary split: cold vs. Orange Bucket

Before anything else, split on `segment` field from the ICP scoring pass:

- `segment: cold` → scored numerically, proceed to §2.
- `segment: orange-bucket` → existing monday.com accounts, bypass the
  numeric rubric entirely, route straight to a dedicated Orange Bucket
  list. These get the 7-question optimisation script
  (`knowledge/company/sales-process-sop.md` §5), not a cold sequence.

## 2. Cold-lead buckets (from the ICP lead-fit score)

| Bucket | Score range | Treatment |
|---|---|---|
| Tier A | 80–100 | Multi-persona (3 contacts/account per the signal-led motion model), highest send priority, first to launch. |
| Tier B | 60–79 | Standard single-persona sequence. |
| Tier C | 40–59 | Lighter-touch sequence (fewer steps, longer delays) or held for a later batch — don't burn full sequence capacity on marginal fit. |
| Excluded | <40 | Does not enter the sequencer. Log the exclusion reason (score + category) rather than silently dropping the row — useful for tuning the rubric later. |

## 3. Secondary segmentation (within a tier, for multi-contact motions)

For Tier A accounts running the multi-contact model (3 personas/account
per the startup guide), split by role so `campaign-copy` can write
role-specific variants rather than one generic sequence:

- **Economic buyer** (budget authority — Ops Director, GM, COO-level)
- **Champion** (day-to-day pain owner — PM lead, Ops Manager)
- **Influencer** (end user who feels the pain daily — team lead, coordinator)

Same account, three contacts, three copy variants — not the same email to
all three.

## 4. Vertical / product-line tagging

Tag every row with the motion's vertical and product line so
`skills/campaign-reports/` can break down performance later, and so the
list aligns with how campaigns actually get named downstream (see
`outbound-motions/<name>/campaigns/` for the naming convention). This
tagging is metadata on the row, not a new bucket dimension — don't
fragment Tier A/B/C further by vertical unless volume genuinely warrants
separate sequences per vertical.

## 5. Output format

Each bucket is a CSV under `outbound-motions/<name>/lists/`, e.g.:
`tier-a.csv`, `tier-b.csv`, `tier-c.csv`, `orange-bucket.csv`,
`excluded.csv` (log only, never uploaded). Every row carries:
`email, first_name, last_name, company_name, icp_score, segment, role,
vertical` at minimum — enough for `campaign-copy` and
`pipeline/prepare_upload.py` / `pipeline/launch_campaign.py` to consume
without re-deriving anything.

**Never fabricate rows here.** This skill only splits and tags leads that
already exist in the enriched input — it does not invent example leads,
including for demos or testing.

## Gate

`sops/lead-verification.md` Gate 2 — spot-check each bucket before handing
to `skills/campaign-copy/`.

## References

See `references/sources.md`.
