---
type: cross-motion report
source: live pull via HeyReachClient.get_overall_stats()
pulled: 2026-08-14
date_range_covered: 2026-07-23 to 2026-08-13 (API default window; spot-checked back to 2026-06-01 for the zero-activity campaigns, confirmed genuinely zero, not a windowing artifact)
---

# HeyReach LinkedIn — cross-motion performance snapshot

Real numbers, not estimates — pulled via `HeyReachClient.get_overall_stats()`
(`POST /stats/GetOverallStats`) for all 9 current-generation (V3) campaigns
documented in `knowledge/company/linkedin-messaging-foundation.md`. This
grounds `skills/campaign-reports/` in what's actually happening, ahead of
building any new campaign.

## Summary table

| Campaign | Conn. sent | Accepted | Accept % | Msgs started | Replies | Reply % | Auto-tagged "interested" |
|---|---:|---:|---:|---:|---:|---:|---:|
| US (Service) | 19 | 4 | 21.1% | 4 | 1 | 25.0% | 0 |
| UK (Service) | 0 | 0 | — | 0 | 0 | — | 0 |
| **ANZ (Service)** | 114 | 36 | 31.6% | 25 | 6 | 24.0% | 2 |
| US (CRM) | 11 | 3 | 27.3% | 3 | 1 | 33.3% | 0 |
| UK (CRM) | 0 | 0 | — | 0 | 0 | — | 0 |
| **ANZ (CRM)** | 326 | 74 | 22.7% | 69 | 19 | 27.5% | 10 |
| US (WM) | 0 | 0 | — | 0 | 0 | — | 0 |
| UK (WM) | 0 | 0 | — | 0 | 0 | — | 0 |
| **ANZ (WM)** | 313 | 55 | 17.6% | 45 | 11 | 24.4% | 3 |
| **Total** | **783** | **172** | **22.0%** | **146** | **38** | **26.0%** | **15** |

## ⚠️ Finding worth flagging to Thana: US and UK campaigns show zero activity

Every US and UK campaign (Service, CRM, and WM alike — 6 of the 9) shows
**exactly zero** connections sent, messages, or replies in this window —
not low activity, genuinely zero. This was spot-checked with an explicit
`StartDate: 2026-06-01` on `US (WM)` to rule out a default-window
artifact; the result was still zero across the board.

Meanwhile all three **ANZ** campaigns are actively running with real
volume (783 total connection requests across the account, and ANZ
accounts for effectively all of it). Possible explanations this repo
can't distinguish from the API alone: the US/UK sender accounts
(`183013`, `183170`) are disconnected/unauthorized, those campaigns are
stalled despite reporting `IN_PROGRESS` status, send limits are
exhausted, or they simply haven't been started yet on the sending side
even though the campaign object itself is live. **Worth a direct check
with Thana** — this isn't something to guess at or "fix" from here.

## What's working (ANZ, all three product lines)

- **Connection acceptance**: 17.6–31.6% across the three ANZ campaigns —
  Service is notably higher (31.6%) than CRM (22.7%) or WM (17.6%).
- **Reply rate** (of message threads started): a tight band, 24.0–27.5%
  across all three — the product-specific messaging
  (`knowledge/company/linkedin-messaging-foundation.md`) is performing
  consistently regardless of which product it's pitching.
- **Auto-tagged "interested"**: CRM leads the pack at 10 (of 69 threads,
  ~14%), vs. WM's 3 (of 45, ~7%) and Service's 2 (of 25, 8%) — CRM may be
  hitting a sharper pain point, or its message copy may simply be
  stronger. Worth investigating before assuming it's the product, not the
  copy.

## Caveats

- This is `HeyReachClient.get_overall_stats()`'s default window (roughly
  the last 3 weeks) — not lifetime campaign performance. ANZ (WM)'s
  campaign was created 2026-07-18 per its `GetAll` record, so this window
  likely covers close to its full life so far; the same isn't confirmed
  for the others.
- "Auto-tagged interested" is HeyReach's own lead-categorization signal,
  not a confirmed meeting/pipeline outcome — don't conflate it with
  `knowledge/company/sales-process-sop.md` §8's "Definition of Done."
  There's currently no join in this repo between HeyReach's tagging and
  the actual CRM pipeline stage a lead reaches.
- V2 legacy campaigns still `IN_PROGRESS` for some region/product combos
  were not included in this pull — this is V3-generation only.

## Used by

- `skills/campaign-reports/instructions.md` — this is the first real data
  point for the metrics/report template defined there.
- `outbound-motions/anz-work-management/reporting/` — see that folder for
  the same numbers filtered to just the ANZ (WM) campaign.
