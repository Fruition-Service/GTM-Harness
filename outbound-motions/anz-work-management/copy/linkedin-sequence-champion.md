---
motion: anz-work-management
channel: heyreach (linkedin)
persona: champion (Ops Manager / PMO Lead / Head of Delivery)
status: draft-v1, superseded by a live campaign — see warning below
built_with: skills/campaign-copy/instructions.md
---

> ⚠️ **A live HeyReach campaign already exists for this motion**
> (`512925 — "V3 - ANZ (WM)"`, `IN_PROGRESS`) — this file was drafted
> without checking that first. The real, currently-running sequence is in
> `knowledge/company/linkedin-messaging-foundation.md`. Do not attach this
> file to `512925`; see `copy/README.md`'s reconciliation note.

# anz-work-management — LinkedIn Sequence — Champion variant

For Tier A accounts running the multi-touch model — LinkedIn runs
alongside, not instead of, the email sequence
(`email-sequence-champion.md`). Keep LinkedIn shorter than email; it's a
different register.

## Connection request

```
Hi {{first_name}} — came across {{company_name}} and your work in
{{vertical}}. Would love to connect and share a thought on project
visibility for teams your size.
```

## Message 1 — after acceptance

```
Thanks for connecting, {{first_name}}. Quick thought — most ops teams
don't have a software problem, they have a work-scattered-across-ten-tools
problem. Curious how {{company_name}} handles project status updates
today?
```

## Message 2 — if no reply after ~4 days

```
Following up, {{first_name}} — happy to send over how we've helped
similar {{vertical}} teams here in ANZ get to one source of truth for
project status. No pitch, just the framework we use. Interested?
```

## Sequence structure note (for `HeyReachClient` / `campaign/UpdateSequence`)

```
CONNECTION_REQUEST → (conditional: accepted) → MESSAGE (Message 1)
                   → (unconditional, +4 days) → MESSAGE (Message 2) → END
                   → (conditional: not accepted, no action) → END
```

See `knowledge/tool-docs/heyreach.md` for the actual `nodeType`/branching
schema this maps to when wired into a real campaign.
