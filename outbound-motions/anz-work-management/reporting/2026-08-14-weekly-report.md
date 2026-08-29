---
motion: anz-work-management
date: 2026-08-14
source: live pull via HeyReachClient.get_overall_stats() / get_campaign_sequence(), campaign 512925
status: real numbers — first report for this motion, built against skills/campaign-reports/instructions.md §2 template
---

# anz-work-management — weekly report — 2026-08-14

## Headline

HeyReach LinkedIn campaign `512925 ("V3 - ANZ (WM)")` is live and steady:
91 connection requests this week (flat vs. last week's 91), 4 replies (up
from 3), 1 auto-tagged "interested." No Smartlead/email-side data — not
checked yet (no API key at time of writing).

## Funnel

| Stage | This week | Last week | 2 weeks ago | Cumulative (~3wk window) |
|---|---:|---:|---:|---:|
| Connections sent | 91 | 91 | 131 | 313 |
| Connections accepted | 18 | 17 | 20 | 55 |
| Message threads started | 13 | 14 | 18 | 45 |
| Replied | 4 | 3 | 4 | 11 |
| Auto-tagged "interested" | 1 | 1 | 1 | 3 |
| Meeting booked | — not tracked by this repo — | | | |
| Work order signed | — not tracked by this repo — | | | |

**The last two rows are a real gap, not an oversight.** Per
`skills/campaign-reports/instructions.md` §1, the metric that actually
matters is funnel-through to a booked meeting / signed work order
(`knowledge/company/sales-process-sop.md` §8), not just replies. This
repo has no join between HeyReach's lead data and the CRM board that
would track that — closing that gap is the highest-value next step for
this skill, not a data-pull problem.

## By segment

Not available. `skills/list-segmentation/`'s Tier A/B/C buckets and the
ICP rubric (`icp/lead-fit-rubric.md`) were never actually used to build
the lead list feeding campaign `512925` — this repo's pipeline isn't
wired to it (see `campaigns/launch-plan.md`'s open question). The 313
leads contacted in this window came from wherever Thana's existing
process sources them, not from this repo.

## Sequence performance

Full sequence text: `knowledge/company/linkedin-messaging-foundation.md`
(WM track). From the numbers above:

- **Connection acceptance: 17.6%** over the full window — the lowest of
  the three ANZ product lines (Service 31.6%, CRM 22.7%, WM 17.6%; see
  `reports/2026-08-14-heyreach-linkedin-performance-snapshot.md`). The
  connection request itself carries no note across all three tracks, so
  this gap is about targeting or timing, not the (identical) request
  copy — worth investigating who's being targeted for WM specifically.
- **Reply rate: 24.4%** of started threads — in line with Service (24.0%)
  and CRM (27.5%). The 4-message structure is performing consistently
  regardless of which product it's pitching.
- **Auto-tagged "interested": 3 of 45 threads (~7%)** — lower than CRM's
  ~14%. Can't attribute this to copy vs. audience without more data;
  don't over-read a 3-lead sample.

## Issues / blockers

- **No pipeline connection.** This repo's ICP/segmentation/dedupe machinery
  has never touched the leads in this campaign. Until that's resolved
  with Thana, this report is descriptive only — it can't yet inform what
  this repo's `skills/` should change, because the skills aren't upstream
  of what's being measured.
- **No downstream conversion data.** See the Funnel section — reply/tag
  data exists, meeting/win data doesn't, in this repo.
- Smartlead side of this motion: unchecked.

## Next steps

1. Confirm with Thana whether/how this repo's pipeline should connect to
   campaign `512925`'s lead sourcing.
2. If a CRM join becomes available, wire actual meeting-booked/won data
   into future reports — that's the number that matters, not reply rate.
3. Investigate WM's lower connection-acceptance rate vs. Service/CRM —
   targeting question, not a copy question (request note is identical
   across all three).
