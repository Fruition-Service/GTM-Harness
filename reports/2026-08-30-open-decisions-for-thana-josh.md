---
type: handoff / decision request
audience: Thana, Josh
status: open — updated same day from the 2026-08-30 Avi/Thana/Yash team call
compiled: 2026-08-30
---

# Open decisions blocking this repo's next real step

> **Updated twice today.** First from the Fireflies transcript of the
> 2026-08-30 Avi/Thana/Yash call (#1 answered, #3 updated, #7/#8 new,
> #9 built). Then, later the same session, `SMARTLEAD_API_KEY` and
> `AI_ARK_API_KEY` both appeared in `config/.env` — both now confirmed
> live and working, resolving the "never checked" half of #3 and #4
> completely.

Eight things have come up while building this harness that only Thana or
Josh can actually resolve — this consolidates them into one list instead
of leaving them scattered across commit messages. **Nothing further
should be built on top of the unresolved ones below without an answer
first** — the risk is wasted work on a wrong assumption, not a technical
blocker.

## 1. Does this repo's pipeline connect to the 9 live HeyReach campaigns? — **answered: yes**

**Resolved by the 2026-08-30 call.** Thana, to Avi: "I have created the V3
campaigns for smart lead and yeah, they just need leads in... we also
need a lead refresh for heyreach." Josh/Avi frame the entire point of the
harness as taking lead-sourcing off Yash's plate given his capacity
constraints. This confirms the pipeline (AI Ark sourcing → `skills/icp/`
scoring → `skills/list-segmentation/` → dedupe → push) is meant to feed
these live campaigns, not run parallel to them.

**Next engineering step, fully unblocked now:** wire
`pipeline/launch_campaign.py` / `pipeline/dedup.py` against the real
campaign IDs — **all 9 confirmed for both platforms**, see
`outbound-motions/_LEDGER.md` (updated 2026-08-30 with real Smartlead
IDs, pulled live after the key was added — every "V3 Evergreen" campaign
is `DRAFTED`, exactly matching "just need leads in"). Validate this
repo's ICP rubric against real send data once volume exists.

## 2. US and UK HeyReach campaigns show zero activity — real problem or expected?

`reports/2026-08-14-heyreach-linkedin-performance-snapshot.md`: all 6
US/UK campaigns (Service, CRM, WM) show exactly zero connections/messages
in the pulled window, spot-checked back to June 1st to rule out a
date-window artifact. Only the 3 ANZ campaigns are active. Possible
causes this repo can't distinguish via the API alone: disconnected sender
accounts (`183013` US, `183170` UK), exhausted send limits, or campaigns
that were never actually started on the sending side.

**Ask Thana directly** — this is either an operational problem worth
fixing today, or a sign those campaigns aren't meant to be measured the
way this repo assumed.

## 3. Smartlead — ✅ resolved: key added, live, all 9 V3 campaign IDs confirmed

`SMARTLEAD_API_KEY` is now set and confirmed working (38 real campaigns
visible). Pulled the real IDs for all 9 "V3 Evergreen" campaigns — every
one is `DRAFTED` (created, zero sends), matching Thana's "just need leads
in" exactly. Full mapping in `outbound-motions/_LEDGER.md`. Also live-
tested `pipeline/check_bounce_rate.py` against 6 real campaigns — see #9,
which also caught and fixed a real doc error in the process.

**Nothing left open here** except the actual work: wiring leads into
these campaigns (#1) and understanding the paired `OOO - <region>`
campaigns' purpose (ask Thana — not guessed at in this repo).

## 4. AI Ark — ✅ key confirmed live; "is it the tool of choice" still open

`AI_ARK_API_KEY` is now set and confirmed working (30,000 credits, real
company search results). Tested a realistic query (ANZ, 25–2,000 staff,
construction industry) and got genuine construction companies back
(Clough, Metricon, Built, Coates) — the sourcing capability works. Also
caught two real filter-shape bugs while testing (see
`knowledge/tool-docs/ai-ark.md`'s "Verified live" section) — one of them
a silent-failure trap (`industries` accepting a request and returning
200 with completely unfiltered results, no error, if you don't use the
exact right shape).

**Still open:** is AI Ark actually the sourcing tool Thana wants this
repo to use day-to-day, or was the key added just to let this repo test
it? Worth a quick confirmation before building further sourcing workflow
on top of it.

## 5. Scraping — a real gap, not a decision this repo should make alone

`knowledge/frameworks/b2b-lead-sourcing.md` flags that this harness
covers 2 of the 3 standard lead-sourcing pillars (Database + Signals via
AI Ark) but has no Scraping capability. Worth a decision on whether
that's needed, and if so, which tool — not something to guess at and wire
without real docs, per how every other integration here was built.

## 6. CRM access — needed for the lookalike feedback loop to run on real data

`pipeline/find_lookalikes.py` (closed-won → similar-company sourcing) is
built and works, but `outbound-motions/anz-work-management/research/closed-won-seeds.md`
is an empty template — this repo has no monday.com CRM access, so there's
no real list of won deals to seed it with. Either someone manually
maintains that list, or a monday.com API integration gets researched and
built the same way AI Ark was.

## 7. "Clay documentation" — a real tool this repo has never touched

Per the call, Yash mentioned giving "the Clay documentation" to Claude to
prepare things, alongside Smartlead/HeyReach configuration. This repo has
**no `knowledge/tool-docs/clay.md` and no Clay client** — everything
built so far for sourcing/enrichment is AI Ark. Clay was explicitly named
in the original startup guide's tool list ("AI Arc, Clay, Smartlead, and
HeyReach") and in `knowledge/company/sales-process-sop.md` §2 ("Clay/n8n/
Instantly stack run by the Reachly team") — it was always in scope, just
never actually researched or wired here.

**Ask Yash:** was that Clay work done in a different session/context this
repo doesn't have visibility into, or is this still to do? If Clay is
genuinely a separate, actively-used tool (not just another name for AI
Ark), it needs the same treatment as the other three: real docs fetched,
`knowledge/tool-docs/clay.md` written, a client built — not guessed at.

## 8. "Deepline" — mentioned as a lead source, never researched here

Avi, describing the harness's ideal workflow: "go fetch the leads from
Deepline." This repo has never heard of Deepline before this call, and
has no documentation or integration for it — everything built for
sourcing uses AI Ark (`pipeline/integrations/ai_ark_client.py`).

**Ask Avi/Thana:** is Deepline a specific product Fruition should be
using (possibly AptAI Systems' own data platform, given the name matched
a folder in the reference GTM-harness screenshot Avi's team shared
earlier), or was it just an illustrative example in Avi's explanation of
how the harness generally works? Don't build against a guess here — same
rule as everything else in this repo.

## 9. Built and live-tested: the bounce-rate safety gate Thana described

Thana mentioned manually pausing V3 campaigns if bounce rate exceeds 2%
(checked via the Smartlead dashboard). That's now
`pipeline/check_bounce_rate.py` — defaults to report-only, `--auto-pause`
to actually pause via the API. **Run live (dry-run) against 6 real
campaigns once the key was added** — all healthy, 0.76%–1.57% bounce
rate, consistent with what Thana described.

**This live test caught a real documentation error worth knowing about:**
the Smartlead campaign-performance endpoint's response schema, as
originally fetched into `knowledge/tool-docs/smartlead.md`, claimed
fields (`bounce_rate`, `unique_lead_count`, `reply_rate`, etc.) that
**don't actually exist** in the real API response — only
`{sent, opened, replied, bounced}` come back. The doc and
`check_bounce_rate.py` are both corrected now (bounce rate computed as
`bounced/sent`). Flagging this because it's a reminder that even a
"verified" doc page fetch can be wrong — live-testing caught what a
second doc read wouldn't have.

Also worth knowing: Smartlead has a **built-in Insights tab** (AI Team →
Automations, same area as an AI Agent Thana already configured for
7-day-no-reply → push-to-HeyReach escalation) that's a free, native
alternative/complement to a custom dashboard — see
`skills/campaign-reports/instructions.md` §3a.

## 10. Recommended, not built: an "experiments" skill for automated variant testing

Thana asked whether the harness can create/modify campaigns itself —
new variants, ICP-driven copy — rather than her team hand-building each
test. Avi described his own team's weekly cycle (report → decide next
variant → a skill applies it with a change log → human approves) as the
model. This repo has the pieces (`skills/campaign-copy/`, the
`update_sequences`/`UpdateSequence` API calls, `skills/campaign-reports/`)
but no skill that closes that loop yet — scoped as a recommendation in
`skills/campaign-reports/instructions.md` §3b, not built, since the exact
workflow (what triggers a new variant, what the approval gate looks like)
needs Thana's input to spec properly rather than being guessed at.

## Recommended order to resolve these

**#1, #3, #4 are done.** Pipeline confirmed meant to feed the live
campaigns, both platforms' keys are live, all 9 Smartlead + 9 HeyReach
campaign IDs are in `outbound-motions/_LEDGER.md`. The actual next
engineering step is now genuinely just wiring
`pipeline/launch_campaign.py`/`pipeline/dedup.py` to push real leads into
the `DRAFTED` Smartlead campaigns and the `IN_PROGRESS` HeyReach ones.

**Still blocking, in priority order:**
1. **#2 — US/UK HeyReach zero activity.** Urgent, still needs Thana
   directly.
2. **#7 and #8 — Clay and "Deepline".** Quick clarifying answers needed
   before any new sourcing integration work, so effort doesn't go into
   AI Ark exclusively if either of these turns out to be the actual tool
   of choice.
3. **The `OOO - <region>` Smartlead campaigns' purpose** (new, from
   pulling real data) — ask before assuming what they're for.
4. **#5, #6, #10** stay lower-urgency — scraping tool choice, CRM access
   for lookalikes, and the experiments skill are all real but need more
   spec/decision before buildable.
