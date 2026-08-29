---
type: reference
source: https://documenter.getpostman.com/view/23808049/2sA2xb5F75 (Postman docs — JS-rendered, not directly scrapeable) + https://www.heyreach.io/blog/campaign-api (2026-04-21) + independent third-party API audits
retrieved: 2026-08-05
verified_by: web search cross-referencing HeyReach's own blog post against two independent third-party endpoint audits (bcharleson/heyreach-mcp, bcharleson/heyreach-cli)
---

# HeyReach — API notes

> **Note on sourcing:** the Postman documenter link you gave
> (`documenter.getpostman.com/view/23808049/2sA2xb5F75`) is a client-rendered
> SPA that returns an empty shell to a plain HTTP fetch — it can't be
> scraped directly. This doc is built from HeyReach's own API blog post
> (dated 2026-04-21) plus two independent third-party endpoint audits from
> mid-2026 that tested the live API. Treat the "confirmed" endpoints below
> as solid; treat the full index at the bottom as names-only, unverified.
> **Open the Postman link yourself and skim it before wiring real API keys
> in** — it's the primary source and may have moved since this was written.

## Base URL & auth

```
Base URL: https://api.heyreach.io/api/public
Auth:     header  X-API-KEY: YOUR_API_KEY
Test key: GET /auth/CheckApiKey
```

Get your key from HeyReach → Settings → API. Keys don't expire but can be
revoked.

`config/.env` (gitignored, see `.env.example`):
```
HEYREACH_API_KEY=...
```

## Rate limit

**300 requests/minute**, flat (no documented per-endpoint tiering like
Smartlead has).

## ⚠️ Known gotcha: campaign creation lands in DRAFT, and there's no clean documented way to activate it via API

This is the single most important thing to know before building against
this API:

1. `POST /campaign/Create` **does work** (added ~April 2026 — an older
   third-party audit from before that date found it 404ing, which is why
   you may see conflicting info online). It creates a fully-configured
   campaign, but the campaign comes back in **DRAFT** status.
2. `POST /campaign/Resume` — the obvious next call — **rejects DRAFT**
   campaigns. It's built for un-pausing an already-launched campaign, not
   activating a new one.
3. A `StartCampaign` endpoint reportedly exists and works, per an
   independent third-party API audit (dated 2026-05-04) — but it is
   **absent from HeyReach's own published docs, Postman collection, and
   Swagger UI**, so its exact path/request shape is unverified here. Do
   not guess at it in code.
4. There is **no documented endpoint to delete/cancel a campaign** either
   — cleanup is manual, in the UI.

**Practical implication for this harness:** `pipeline/integrations/heyreach_client.py`
implements `create_campaign()` honestly — it creates the DRAFT and returns
the `campaignId`, but does **not** pretend to activate it. Activating a
freshly-created campaign currently requires the HeyReach UI (or you can
try their support/Swagger to confirm `StartCampaign`'s real shape and add
it once verified). `resume_campaign()` is implemented only for the
already-active-then-paused case it's actually documented for.

## Verified live (2026-08-05, real API key)

`CheckApiKey`, `campaign/GetAll`, `campaign/GetCampaignSequence`,
`stats/GetOverallStats`, and `list/GetAll` were called against a real
account (28 real campaigns, 26 real lists, real performance numbers) and
confirmed working. Gotchas found only by doing this, not documented
anywhere:

1. **A bodyless POST gets `415 Unsupported Media Type`.**
   `requests.post(url, json=None)` sends no `Content-Type` header at all,
   which HeyReach rejects even for endpoints with no real parameters —
   you must send an explicit empty JSON object (`json={}`, not
   `json=None`). `HeyReachClient._request()` now defaults any POST's
   `json_body` to `{}` rather than `None` to handle this uniformly.
2. **`campaign/GetAll` is paginated with a low default page size** —
   `totalCount` in the response can be much larger than `len(items)`
   (observed: `totalCount: 28`, only 10 `items` returned by default). Use
   `offset`/`limit` params to page through (`skip`/`take` are silently
   ignored — confirmed by testing both). `HeyReachClient.get_campaigns()`
   passes through `**filters`, so call it as
   `get_campaigns(offset=10, limit=25)`; there's no auto-pagination
   helper yet, so a full-account pull needs a manual loop.

## Confirmed endpoints (schemas verified from HeyReach's own blog + cross-checked)

### Create a campaign

```
POST /campaign/Create
Header: X-API-KEY: ...
Body (CreateCampaignApiInputDto):
{
  "name": "Q1 2026 ANZ Work Mgmt",       // required, 1-50 chars
  "linkedInUserListId": 123,              // required — must be an existing list of type USER_LIST
  "linkedInAccountIds": [456, 789],       // required, 1-100 sender account IDs
  "excludeContactedFromOtherCampaigns": false,
  "excludeHasOtherAccConversations": false,
  "excludeContactedFromSenderInOtherCampaign": false,
  "excludeListId": null,                  // optional, must differ from linkedInUserListId
  "schedule": { ... },                    // optional, see below; defaults Mon-Fri 09:00-17:00 UTC
  "sequence": { ... }                     // optional, see below
}
→ 200: {"campaignId": 12345}              // DRAFT status — see gotcha above
```

### Sequence structure (`sequence` field, and `POST /campaign/UpdateSequence`)

A tree of nodes (`PublicSequenceNodeDto`), each an action:

```
nodeType: CONNECTION_REQUEST | MESSAGE | INMAIL | VIEW_PROFILE | FOLLOW |
          LIKE_POST | FIND_EMAIL | CHECK_IS_CONNECTION |
          CHECK_IS_OPEN_PROFILE | SEND_LEAD_TO_INSTANTLY |
          SEND_LEAD_TO_SMARTLEAD | SEND_LEAD_TO_BISON | END
unconditionalNode: <next node>            // taken unconditionally, or when a branch condition is false
conditionalNode:   <next node>            // taken when a branch condition is true
actionDelay:      0-100
actionDelayUnit:  HOUR | DAY
payload:          {...}                   // varies by nodeType
externalReference: "..."                  // optional, max 100 chars, your own tracking id
```

Branching node types (`CONNECTION_REQUEST`, `CHECK_IS_CONNECTION`,
`CHECK_IS_OPEN_PROFILE`) require both `conditionalNode` and
`unconditionalNode`. Pure messaging nodes (`MESSAGE`, `INMAIL`) only
support `unconditionalNode`. Every path must terminate in an `END` node.

**Interesting for this harness:** `SEND_LEAD_TO_SMARTLEAD` is a native
node type — HeyReach can hand a lead off to a Smartlead campaign directly
as a sequence step, which is a plausible LinkedIn→email multi-channel
pattern worth considering for a motion later (not wired up here).

### Update sender accounts

```
POST /campaign/UpdateAccounts
Body: {"campaignId": 12345, "linkedInAccountIds": [456, 789]}
```
**Replaces** the entire sender list — any account not in the new array is
removed from the campaign.

### Update schedule

```
POST /campaign/UpdateSchedule
Body: {
  "campaignId": 12345,
  "schedule": {
    "dailyStartTime": "09:00:00", "dailyEndTime": "17:00:00",
    "timeZoneId": "Australia/Sydney",
    "enabledMonday": true, "enabledTuesday": true, ..., "enabledSunday": false,
    "startDate": "2026-08-10", "endDate": null
  }
}
```

### Pause / Resume (existing, already-active campaigns only)

```
POST /campaign/Pause?campaignId=12345
POST /campaign/Resume?campaignId=12345    // rejects DRAFT, see gotcha above
```

### Add leads to a campaign (requires an ACTIVE/IN_PROGRESS campaign)

```
POST /campaign/AddLeadsToCampaignV2       // prefer V2 over the undeprecated-but-older V1
Body: {
  "campaignId": 12345,
  "accountLeadPairs": [                   // max 100 per call
    {
      "linkedInAccountId": 456,           // which sender account contacts this lead
      "lead": {
        "profileUrl": "https://linkedin.com/in/jane-doe",   // minimum required field
        "firstName": "Jane", "lastName": "Doe",
        "location": "Sydney, Australia", "summary": "...",
        "companyName": "Acme", "position": "COO", "about": "...",
        "emailAddress": "jane@acme.com",
        "customUserFields": {"motion": "anz-work-management"}
      }
    }
  ]
}
→ 200: {"addedLeadsCount": N, "updatedLeadsCount": N, "failedLeadsCount": N}
```

Per-lead sender assignment (`linkedInAccountId`) means the caller decides
rotation, not HeyReach — `pipeline/launch_campaign.py` leaves the rotation
strategy as a TODO rather than guessing one.

### Get a campaign's live sequence — confirmed, not just documented

```
GET /campaign/GetCampaignSequence?campaignId=12345
→ 200: a single root node (usually VIEW_PROFILE), same PublicSequenceNodeDto
  shape as the `sequence` field in Create/UpdateSequence, but populated
  with real content. Real example (`payload` for a MESSAGE node):
  {
    "nodeType": "MESSAGE", "actionDelay": 1, "actionDelayUnit": "DAY",
    "payload": {
      "messages": ["variant A text...", "variant B text..."],  // HeyReach
                                                                 // A/B-tests between these
      "fallbackMessage": "..."   // used if variable substitution fails, or as
                                  // the single message when there's no A/B test
    },
    "conditionalNode": {...},    // taken on reply/acceptance
    "unconditionalNode": {...}   // taken on no reply/timeout
  }
```

For `CONNECTION_REQUEST` nodes specifically, `payload` also carries
`toBeWithdrawnAfterDays` (confirmed real value: `25` — auto-withdraws an
unaccepted request after that many days). A blank `messages: [""]` +
`fallbackMessage: ""` is valid — it means "send the connection request
with no note," not a bug.

This is genuinely useful for pulling **real, currently-running** sequences
to document or reuse — see `knowledge/company/linkedin-messaging-foundation.md`
for a full worked example pulled this way across 9 live campaigns.
`HeyReachClient.get_campaign_sequence(campaign_id)` wraps this.

### Get campaign performance stats — confirmed, not just documented

```
POST /stats/GetOverallStats
Body: {"AccountIds": [456, 789], "CampaignIds": [12345]}   // note PascalCase — inconsistent
                                                             // with every other endpoint's
                                                             // camelCase, confirmed by testing
→ 200: {
  "byDayStats": {"2026-07-23T00:00:00Z": {...daily metrics...}, ...},
  "overallStats": {
    "profileViews": N, "connectionsSent": N, "connectionsAccepted": N,
    "connectionAcceptanceRate": 0.0-1.0,
    "messagesSent": N, "totalMessageStarted": N, "totalMessageReplies": N,
    "messageReplyRate": 0.0-1.0,
    "inmailMessagesSent": N, "totalInmailStarted": N, "totalInmailReplies": N,
    "inMailReplyRate": 0.0-1.0,
    "uniqueLeadsContacted": N,
    "autoTaggedInterested": N, "totalAutoTagged": N, "autoTaggedInterestedRate": 0.0-1.0
  }
}
```

**Both `AccountIds` and `CampaignIds` are required** — a bare `{}` 400s
with a validation error naming both fields; there's no account-wide "all
campaigns" call. Optional `StartDate`/`EndDate` (ISO date strings) narrow
the window — without them, the API defaults to roughly the trailing 3
weeks (confirmed: default window started 2026-07-23 when queried on
2026-08-14). Passing an explicit earlier `StartDate` on a
genuinely-inactive campaign returned a still-zero result, confirming the
default window isn't hiding older activity.

`autoTaggedInterested`/`totalAutoTagged` is HeyReach's own auto-tagging
signal (separate from anything Smartlead-side) — don't conflate this with
a confirmed sales-qualified lead; see
`reports/2026-08-14-heyreach-linkedin-performance-snapshot.md` for a
worked example and its caveats. `HeyReachClient.get_overall_stats()`
wraps this.

### Lists

```
POST /list/CreateEmptyList
Body: {"name": "anz-work-management — segment A", "type": "USER_LIST"}
→ 200: {"listId": ...}

POST /list/GetAll
```

Leads must live in a `USER_LIST` before `campaign/Create` can reference it
via `linkedInUserListId` — list creation/population is a prerequisite
step, not optional.

## Full endpoint index (names only, corroborated across two third-party audits + a Postman-doc mirror — treat as unverified until you open the Postman link yourself)

- **auth** — CheckApiKey (GET)
- **campaign** — GetAll, GetById, Create, UpdateSettings, UpdateSequence,
  UpdateAccounts, UpdateSchedule, GetCampaignSequence, Pause, Resume,
  AddLeadsToCampaignV2 (and an older V1, undeprecated — prefer V2)
- **lead** — GetLead (POST, requires `profileUrl`)
- **list** — GetAll, CreateEmptyList, GetById(?), AddLeadsToList,
  list-leads-in-list, list-companies-in-list
- **inbox** — GetConversationsV2, get single conversation, send message
- **stats** — GetOverallStats
- **MyNetwork** — GetMyNetworkForSender (requires `senderId`)
- **webhooks** — create, get, list, update, delete (event-driven —
  candidate for a HeyReach-side equivalent of the Smartlead
  sentiment-tagging quick win, not yet explored)
- **LinkedIn accounts** — list connected sender accounts

Known documentation gaps as of the mid-2026 third-party audits (worth
re-checking periodically, not re-litigating in code): Swagger UI has a
redirect loop between `/swagger` and `/swagger/`; no campaign
delete/cancel endpoint; campaigns silently auto-pause when their lead list
empties (misleading "success" responses); V1/V2 lead-adding endpoints
coexist without deprecation markers.

## Used by

- `pipeline/integrations/heyreach_client.py` — wraps the confirmed calls
  above. `create_campaign()` is honest about leaving the campaign in
  DRAFT; there is no `start_campaign()` — see the gotcha section.
- `pipeline/launch_campaign.py` — orchestrates list creation → campaign
  create → sequence/accounts/schedule → add leads for a motion.
