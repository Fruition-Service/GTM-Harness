---
type: reference
source: live pull via HeyReachClient.get_campaign_sequence(), HeyReach account
pulled: 2026-08-05
pulled_by: Claude Code, via pipeline/integrations/heyreach_client.py
---

# LinkedIn Messaging — Foundation (from Thana's live HeyReach sequences)

This is not a draft — every message below is copied verbatim from
**currently running** HeyReach campaigns, pulled live via
`HeyReachClient.get_campaign_sequence()`
(`GET /campaign/GetCampaignSequence?campaignId=...`). This is the real,
working LinkedIn messaging Thana has live across all three regions and
product lines. Treat this as the base pattern — `skills/campaign-copy/`
and any future LinkedIn sequence work should adapt from this, not
reinvent it.

## Source campaigns (V3 generation, all `IN_PROGRESS` at time of pull)

| Product | US | UK | ANZ |
|---|---|---|---|
| Service (monday Service / ticketing) | 512943 | 512942 | 512941 |
| CRM (monday CRM) | 512940 | 512939 | 512937 |
| WM (monday Work Management) | 512934 | 512930 | **512925** |

`512925 — "V3 - ANZ (WM)"` is the live campaign for exactly this repo's
pilot motion (`outbound-motions/anz-work-management/`) — see that
folder's README for the reconciliation note; the motion was drafted here
as "not yet launched" before this pull, which was wrong.

**Not pulled in this pass:** older `V2 -` and unversioned campaigns for
the same region/product combos, several of which are still `IN_PROGRESS`
(e.g. `449105 - V2 - UK/IRE (WM)`, `449085 - V2 - USC (WM)`). Same method
works on those — pull them the same way if a historical/legacy comparison
is useful.

## The shared structure (identical across all 9 campaigns)

```
VIEW_PROFILE (0h delay)
  → CONNECTION_REQUEST (3h delay, no note — see below)
      → [accepted] → MESSAGE 1 (1 day delay)
          → [replied] → END
          → [no reply] → MESSAGE 2 "bump" (1 day delay)
              → [replied] → END
              → [no reply] → MESSAGE 3 (5 day delay)
                  → [replied] → END
                  → [no reply] → MESSAGE 4 (10 day delay)
                      → [replied] → END
                      → [no reply] → END
      → [not accepted] → END (15 day delay — auto-withdraw)
```

**Connection request:** sent with **no note** — `messages: [""]`,
`fallbackMessage: ""`. Auto-withdrawn after 25 days if not accepted
(`toBeWithdrawnAfterDays: 25`). This is a deliberate choice already live
in production — a blank connection request rather than a pitchy note.
Don't "improve" this into a note without a real reason; it's the current
working baseline.

**Only Message 1 and the bump (Message 2) have A/B variants** (2 each,
except Service/CRM Message 1 which run 1 variant). Messages 3 and 4 run a
single variant each. HeyReach picks a variant per lead — this repo's
client doesn't currently expose which variant "won," so there's no
performance data backing which variant is stronger; that's a
`skills/campaign-reports/` gap worth closing.

**Regional localization:** content is identical between regions except UK
and ANZ use British/Australian spelling where US uses American spelling
(confirmed: "centralise" vs "centralize" in the Service track). This is
the only regional variation found — otherwise the exact same copy runs in
all three regions per product line. If a future motion needs actual
regional customization (not just spelling), that would be new work, not
something already covered.

## Service (monday Service / ticketing)

**Message 1** (+1 day after connect):
> Hi {FIRST_NAME}, thanks for connecting.
>
> We help support and customer success leaders centralise client requests
> and build visibility across the queue through monday Service.
>
> Came across your profile after a few similar builds we wrapped up
> recently.
>
> Curious to know what's been your go-to tool for ticketing?

*(US variant: "centralize" instead of "centralise", otherwise identical.)*

**Message 2 — bump** (+1 day, 2 variants):
> Just bumping my note from yesterday in case it slipped by. Would you be
> keen to see the centralised support queue we could build for your team?

> Just bumping my note from yesterday in case it slipped by. Happy to
> record a quick 2-minute video showing what a centralised support queue
> could look like for your team, if that's of interest?

**Message 3** (+5 days):
> No worries if you've been heads-down, {first_name}. For context, the
> latest team like yours we worked with had client requests scattered
> across email and Slack, and we centralised them with a build in 3
> weeks.
>
> I could spin up a custom monday Service portal for your team, ticket
> intake, automated routing and queue visibility, ready to click through.
> Worth a quick look?

**Message 4** (+10 days):
> Hi {FIRST_NAME}, here's a quick walkthrough of our process:
> https://www.fruitionservices.io/post/monday-service-use-cases
>
> Is there someone else on your team I should be talking to about this?
>
> Otherwise glad to be connected.

## CRM (monday CRM)

**Message 1** (+1 day after connect, 1 variant):
> Hi {FIRST_NAME}, thanks for connecting.
>
> We help sales leaders get cleaner pipeline data and clearer visibility
> across deals through monday CRM.
>
> Came across your profile after a few similar builds we wrapped up
> recently.
>
> Curious to know what's been your go-to CRM tool?

**Message 2 — bump** (+1 day, 2 variants):
> Just bumping my note from yesterday in case it slipped by. Would you be
> keen to see the pipeline visibility system we could build for your
> team?

> Just bumping my note from yesterday in case it slipped by. Happy to
> record a quick 2-minute video showing what cleaner pipeline visibility
> could look like for your team, if that's of interest?

**Message 3** (+5 days):
> No worries if you've been heads-down, {first_name}. For context, the
> latest team like yours we worked with had messy pipeline data and
> inconsistent deal logging, and we cleaned it up with a build in 4
> weeks.
>
> I could spin up a custom monday CRM for your team, deal stages,
> automations, and pipeline reporting, ready to click through. Worth a
> quick look?

**Message 4** (+10 days):
> Hi {FIRST_NAME}, here's a quick walkthrough of our process:
> https://www.fruitionservices.io/post/monday-crm-contact-management-tutorial
>
> Is there someone else on your team I should be talking to about this?
>
> Otherwise glad to be connected.

## WM (monday Work Management) — the pilot motion's actual live copy

**Message 1** (+1 day after connect, 2 variants):
> Hi {FIRST_NAME}, thanks for connecting.
>
> We help operations and project leaders build visibility across
> projects, milestones and team dependencies through monday.com
>
> Came across your profile after a few similar builds we wrapped up
> recently.
>
> Curious to know what's been your go-to tool for project management?

> Hi {FIRST_NAME}, thanks for connecting.
>
> We help operations and project leaders build visibility across
> projects, milestones and team dependencies through monday.com
>
> Came across your profile while looking at companies at a similar growth
> stage to ones we've worked with.
>
> Curious to know what's been your go-to tool for project management?

**Message 2 — bump** (+1 day, 2 variants):
> Just bumping my note from yesterday in case it slipped by. Would you be
> keen to see the project visibility system we could build for your
> team?

> Just bumping my note from yesterday in case it slipped by. Happy to
> record a quick 2-minute video showing what that project visibility
> could look like for your team, if that's of interest?

**Message 3** (+5 days):
> No worries if you've been heads-down, {first_name}. For context, the
> last team like yours we worked with had project delays and task
> tracking slipping, and we sorted it with a build in 3 weeks.
>
> I could spin up a custom monday demo environment for your team, project
> pipeline, task tracking and capacity, ready to click through. Worth a
> quick look?

**Message 4** (+10 days):
> Hi {FIRST_NAME}, here's a quick walkthrough of our process:
> https://www.fruitionservices.io/post/monday-project-portfolio-management-setup
>
> Is there someone else on your team I should be talking to about this?
>
> Otherwise glad to be connected.

## Pattern worth naming (for future product lines / motions)

Every track follows the same beat, just re-skinned per product:

1. **Message 1** — thanks for connecting, one-line value prop framed
   around the product's core visibility problem, soft question CTA.
2. **Message 2** — pure bump, references "yesterday," offers a choice
   between seeing the system or a 2-minute video.
3. **Message 3** — "no worries if heads-down" opener, a specific
   composite pain + build-timeframe proof point, offers a concrete demo.
4. **Message 4** — links to a real case-study/tutorial page on
   fruitionservices.io, asks for a redirect to the right person, low-key
   sign-off.

If a future motion needs a new product-line track, this is the template
to reskin, not `outbound-motions/*/copy/`'s independently-drafted
sequences (see the reconciliation note in
`outbound-motions/anz-work-management/copy/README.md`).
