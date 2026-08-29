---
skill: campaign-reports
status: draft-v1
gate: sops/approval-gates.md (Gate 5)
---

# campaign-reports

Turns campaign analytics into an internal report, written to
`outbound-motions/<name>/reporting/` and rolled up into `reports/`.

> **Status:** draft v1. Metric definitions below are grounded in
> `knowledge/company/sales-process-sop.md` §8 and
> `knowledge/company/delivery-sop.md` §8 — sharpen the cadence/format with
> Thana and Josh once real campaign data exists to report on.

## 0. Reporting philosophy (per Avi, 2026-08-30 team call)

**Agile, not exhaustive.** Reports should be built around the weekly
experiment cycle Avi's own team runs (report Friday afternoon → decide
next week's test → apply it Monday), not a long-winded dump of every
metric. Concretely: **what did we test, what happened, what's the delta
from where we want to be, what are we testing next** — that structure,
every time. "If it's a very big, long-winded report on everything, no one
reads it" — pull exactly what's needed, not everything available.

## 1. Metrics to pull, and where from

**Top-of-funnel (per platform, per campaign):**
- Sent, opened, replied, bounced — Smartlead:
  `SmartleadClient.get_campaign_performance()` (confirmed schema,
  `knowledge/tool-docs/smartlead.md` — note `bounce_rate` is per unique
  lead, not per email sent); HeyReach: `HeyReachClient.get_overall_stats()`
  (confirmed, `knowledge/tool-docs/heyreach.md`).
- **Bounce-rate safety gate:** `pipeline/check_bounce_rate.py` encodes
  Thana's existing manual policy — pause a campaign above 2% bounce rate.
  Report on whether any campaign is approaching or has hit that
  threshold; don't wait for the weekly report to be the only place this
  gets checked (run it more often, ideally daily, once automated).
- Reply sentiment breakdown (positive/neutral/negative) — Smartlead
  `analytics/campaign-response-stats`, once lead categorization
  (`knowledge/tool-docs/smartlead.md`) is wired.

**The metric that actually matters — funnel-through, not just opens:**
Per `sales-process-sop.md` §8 (Definition of Done — Sales), track leads
through to: reply → booked meeting (Stage 1 Initial Contact) → work order
signed (Won). Reply/open rates are leading indicators; this is the number
that justifies the motion's existence. Pull booked-meeting and Won status
from the relevant regional CRM board, joined back to the originating
outbound lead — this join doesn't exist yet as a pipeline step; flag it as
a gap rather than reporting reply rate alone as if it were the whole
story.

**Downstream context (not this skill's job to hit, but worth knowing):**
`delivery-sop.md` §8 KPIs — utilisation, CSAT, case studies — are what
outbound quality is ultimately judged against, several steps past this
report. Reference, don't chase.

## 2. Report structure

Shaped around the experiment cycle (§0), not a generic metrics dump:

```markdown
# <motion> — weekly report — <date>

## What we tested this week
<the specific variant/change that was live — sequence step, ICP tweak,
new segment. If nothing changed, say so; don't pad.>

## What happened
| Stage | This week | Last week | Delta | Cumulative (motion to date) |
|---|---|---|---|---|
| Contacted | | | | |
| Replied | | | | |
| Positive reply | | | | |
| Meeting booked | | | | |
| Work order signed | | | | |

Bounce rate: <X%> (threshold: 2%, see `pipeline/check_bounce_rate.py`)

## By segment (Tier A / B / C, cold vs Orange Bucket)
<funnel breakdown per skills/list-segmentation/ bucket — which segment is
actually converting, not just which has volume>

## Sequence performance
<which step/variant (skills/campaign-copy/ output) is driving replies —
this is what decides next week's experiment>

## Issues / blockers
<anything from pipeline/dedup.py exclusions, platform API errors, bounce
rate approaching threshold, gates that failed and sent something back
for rework>

## What we're testing next week
<the specific next variant, and why — tie it back to what "What happened"
showed. This is the section the whole report exists to produce.>
```

## 3. Sentiment-tagging quick win (AGENTS.md §5)

Once wired: Smartlead webhook (`POST /webhook/create`, `EMAIL_REPLY` event)
→ Make.com/n8n → apply one of the three controlled tags
(information-request / book-meeting / positive) via
`update-lead-category` → Slack notification on `positive` to close the
5–10 minute response window. Until the controlled-tag mapping exists, the
interim is "any reply" → Slack, so nothing gets missed. This report should
note which mode (interim vs. full tagging) was live for the period it
covers, since that changes what the sentiment numbers mean.

## 3a. Native platform automations worth knowing about (not duplicating)

Per the 2026-08-30 call, Smartlead has two built-in features worth
checking before this repo builds an equivalent from scratch:

- **AI Agent automation** (Smartlead UI → AI Team → Automations): Thana
  has one configured to push a lead to HeyReach if it doesn't reply
  within 7 days on email — a native cross-platform escalation, not
  something `pipeline/` needs to replicate via API.
- **Insights tab** (same area): a built-in reply/bounce-rate dashboard,
  free on Thana's plan. Worth cross-checking this repo's pulled numbers
  against it rather than assuming API and UI ever drift silently.

## 3b. Recommended next build: an "experiments" skill (not built yet)

Thana asked, on the same call, whether the harness can create/modify
campaigns itself — new variants, dynamic ICP-driven copy — rather than
her team hand-building each test. Avi's own team runs this as a named
weekly cycle (this is where §0's philosophy comes from): decide the
variant → a skill applies the change (new sequence variant, updated
targeting) with a full change log → human approves → tracked the
following week. This harness has the pieces
(`skills/campaign-copy/`, `pipeline/integrations/*_client.py`'s
`update_sequences`/`UpdateSequence` calls, this skill's reporting) but
not yet a skill that closes the loop end-to-end automatically. Worth
scoping as its own skill (`skills/experiments/`?) rather than folding
into this one — flagged here since the reporting cycle is what would
feed it.

## 4. Rules

- **Numbers before narrative.** Pull real numbers from the platform APIs
  before writing any qualitative summary — don't estimate or round from
  memory.
- **Reconcile before sharing externally.** Per `sops/approval-gates.md`
  Gate 5, any report going to a Director-level audience gets checked
  against the platform dashboards directly, not just the API pull, in
  case of API lag or a miscounted join.

## References

See `references/sources.md`.
