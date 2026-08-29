---
type: ledger
status: workspace IDs confirmed for all 9 (both platforms); only anz-work-management has a scaffolded repo folder
last_updated: 2026-08-30
---

# _LEDGER.md — motion ↔ workspace routing table

Source of truth for which tool workspaces/keys back each motion, and which
motions share a **dedupe pool** (`pipeline/dedup.py` reads this file).
Motions in the same dedupe-pool group must never let a lead upload twice
across their workspaces.

All motions currently share one Smartlead/HeyReach account, so
`smartlead_key_ref` / `heyreach_key_ref` point at the single
`SMARTLEAD_API_KEY` / `HEYREACH_API_KEY` env vars (see
`config/.env.example`, `knowledge/tool-docs/smartlead.md`,
`knowledge/tool-docs/heyreach.md`). If/when a motion gets its own
sub-account or workspace-scoped key, give it its own ref here rather than
overloading the shared one.

**Per the 2026-08-30 team call, this repo's pipeline is confirmed to be
meant to feed these campaigns** (see
`reports/2026-08-30-open-decisions-for-thana-josh.md` #1) — connecting
`pipeline/launch_campaign.py` / `pipeline/dedup.py` to the real IDs below
is the next engineering step, not building a parallel system.

**Smartlead status:** all 9 "V3 Evergreen" campaigns exist and are
`DRAFTED` (created, not started, zero sends) — exactly matching Thana's
"just need leads in." Each also has a paired `OOO - <region>` campaign
(same status) — purpose not confirmed, likely an out-of-office/backup
sequence; ask before assuming.

**HeyReach status:** all 9 exist and are `IN_PROGRESS`, but only the 3
ANZ campaigns show real send activity — US and UK show zero across the
board (`reports/2026-08-14-heyreach-linkedin-performance-snapshot.md`,
open question #2 in the decisions doc).

| motion | region | product | smartlead_campaign_id | smartlead_status | heyreach_campaign_id | heyreach_status | dedupe_pool |
|---|---|---|---|---|---|---|---|
| `anz-work-management` | ANZ | Work Management | `3808735` (OOO: `3808736`) | DRAFTED | `512925` | IN_PROGRESS, active | `anz` |
| *(unscaffolded)* | ANZ | CRM | `3819250` (OOO: `3819251`) | DRAFTED | `512937` | IN_PROGRESS, active | `anz` |
| *(unscaffolded)* | ANZ | Service | `3841339` (OOO: `3841340`) | DRAFTED | `512941` | IN_PROGRESS, active | `anz` |
| *(unscaffolded)* | US | Work Management | `3808803` (OOO: `3808804`) | DRAFTED | `512934` | IN_PROGRESS, **zero activity** | `us` |
| *(unscaffolded)* | US | CRM | `3819571` (OOO: `3819572`) | DRAFTED | `512940` | IN_PROGRESS, **zero activity** | `us` |
| *(unscaffolded)* | US | Service | `3841369` (OOO: `3841370`) | DRAFTED | `512943` | IN_PROGRESS, **zero activity** | `us` |
| *(unscaffolded)* | UK | Work Management | `3808794` (OOO: `3808795`) | DRAFTED | `512930` | IN_PROGRESS, **zero activity** | `uk` |
| *(unscaffolded)* | UK | CRM | `3819443` (OOO: `3819444`) | DRAFTED | `512939` | IN_PROGRESS, **zero activity** | `uk` |
| *(unscaffolded)* | UK | Service | `3841366` (OOO: `3841367`) | DRAFTED | `512942` | IN_PROGRESS, **zero activity** | `uk` |

`smartlead_key_ref` / `heyreach_key_ref` for every row above:
`SMARTLEAD_API_KEY` / `HEYREACH_API_KEY` (shared account, see note above).

**Dedupe pools split by region** (`anz`/`us`/`uk`), not one shared pool —
each region's 3 product-line campaigns (WM/CRM/Service) target the same
underlying company/contact universe more than they overlap across
regions. Revisit this if that assumption turns out wrong once real send
volume exists.

<!--
TODO(Yash): 8 of these 9 motions have confirmed workspace IDs above but no
outbound-motions/<name>/ folder yet — scaffold them following
outbound-motions/anz-work-management/'s structure when ready, using
knowledge/company/linkedin-messaging-foundation.md's per-product-line
messaging as the starting copy (already confirmed live and working for
all 3 product lines, just needs the per-region localization noted there).
-->
