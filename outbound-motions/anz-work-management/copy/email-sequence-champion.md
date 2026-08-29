---
motion: anz-work-management
channel: smartlead (email)
persona: champion (Ops Manager / PMO Lead / Head of Delivery)
status: draft-v1 — NOT sent, pending sops/persona-qa.md review
built_with: skills/campaign-copy/instructions.md
---

# anz-work-management — Email Sequence — Champion variant

Merge fields used: `{{first_name}}`, `{{company_name}}`, `{{vertical}}`,
`{{sender_first_name}}`. All must resolve from the segmented list
(`lists/tier-a.csv` etc.) before this goes live — see
`sops/persona-qa.md` item 3.

## Step 1 — Day 0 — insight-led opener

**Subject:** quick thought on {{company_name}}'s project visibility

```
Hi {{first_name}},

Most ops teams don't have a software problem — they have a
work-scattered-across-ten-tools problem. The platform is never the fix;
the workflow is.

I'd guess {{company_name}} runs projects across a mix of spreadsheets,
email threads, and a bit of "ask so-and-so" — that's the norm for most
teams your size in this space.

Curious — when a project's status changes, how does everyone actually
find out?

{{sender_first_name}}
```

## Step 2 — Day 3 — cost of inaction + proof

**Subject:** re: quick thought on {{company_name}}'s project visibility

```
Hi {{first_name}},

Following up — the teams that get real ROI from a platform change aren't
the ones with the biggest budget. They're the ones who fixed the process
before they bought the tool. That's the work we do.

We're a monday.com Platinum Partner (Partner Summit Rising Star 2026),
and we've built exactly this — one source of truth for project status,
automated reporting instead of manual chasing — for 600+ teams, several
in construction and professional services here in ANZ.

Worth 15 minutes to see what that looks like for a team {{company_name}}'s
size?

{{sender_first_name}}
```

## Step 3 — Day 8 — pre-empt the likely objection

**Subject:** before you say "we'll sort this internally"

```
Hi {{first_name}},

If the plan is to fix this internally at some point — fair. But it's
worth asking what your team's time is actually worth against your real
roadmap, versus a workflow we've already deployed 600+ times.

And if it's a timing thing — the hours lost to status-chasing and rework
don't pause while it's "not the right time." Happy to just scope it so
there's a real number to weigh, no pressure either way.

{{sender_first_name}}
```

## Step 4 — Day 15 — breakup

**Subject:** closing the loop

```
Hi {{first_name}},

I'll leave this here — if project visibility becomes a priority later,
happy to pick it back up. In short: we help ops teams replace
spreadsheet-and-email project tracking with one source of truth, without
the internal build project.

All the best,
{{sender_first_name}}
```

## Other role variants (Tier A multi-contact accounts)

Full sequences not yet written for these — same 4-step structure and
timing, different opening framing per
`skills/campaign-copy/instructions.md` §4:

- **Economic buyer (GM/COO):** open with cost/scale framing instead of the
  workflow reframe — e.g. "What does status-chasing actually cost you
  across a team of {{headcount}}, in hours a month?" — lead with
  Implication-stage language, not Problem-stage.
- **Influencer (PM/Coordinator):** open with the relief angle — "What
  would you do with the hours you're not spending re-chasing updates?" —
  Need-payoff framing.

TODO(Avi/Thana): write these two in full before launching Tier A
multi-contact sends — right now only the champion variant is complete.
