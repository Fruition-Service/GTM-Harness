# knowledge/

Evergreen reference material: tool API docs (`tool-docs/`), frameworks the
skills cite (`frameworks/`), and company-level offer/positioning
(`company/`, shared across all motions, not duplicated per motion).

## tool-docs/

- [`smartlead.md`](tool-docs/smartlead.md) — auth, rate limits, verified
  request/response schemas for create/sequence/leads/status/webhooks, plus
  a full endpoint-name index. Backs `pipeline/integrations/smartlead_client.py`.
- [`heyreach.md`](tool-docs/heyreach.md) — auth, rate limits, verified
  schemas, and a documented gotcha: campaigns created via API land in
  DRAFT with no verified API activation path. Backs
  `pipeline/integrations/heyreach_client.py`.
- [`ai-ark.md`](tool-docs/ai-ark.md) — company/people search + verified
  email-finding. Corrects the product name (was documented as "AI Arc" —
  it's actually **AI Ark**). Auth, credit metering, the two-step
  search-then-export-with-email pattern, and a note on its list-exclude
  feature vs. `pipeline/dedup.py`'s email-based dedupe. Backs
  `pipeline/integrations/ai_ark_client.py`.

See `AGENTS.md` §7 for how these clients fit into the pipeline.

## company/

- [`vision.md`](company/vision.md) — Director Vision Statement: positioning
  ("process before platform"), target market, where the business is
  headed.
- [`sales-process-sop.md`](company/sales-process-sop.md) — Sales Process
  SOP: confirms this repo backs the "Outbound Lead Engine (OLE)" CRM board
  it references; includes the SPIN discovery framework and objection
  handling that `skills/campaign-copy/` and `skills/icp/` should draw on.
- [`delivery-sop.md`](company/delivery-sop.md) — Project Delivery SOP:
  what happens after a lead converts; relevant to `skills/campaign-reports/`
  for framing what outbound is ultimately judged against.
- [`linkedin-messaging-foundation.md`](company/linkedin-messaging-foundation.md)
  — **not a draft** — the real, live LinkedIn sequences pulled directly
  from Thana's running HeyReach campaigns (all 3 regions × 3 products).
  The base pattern `skills/campaign-copy/` should reskin, not reinvent.

See each skill's `references/sources.md` for the specific pointers into
these docs.
