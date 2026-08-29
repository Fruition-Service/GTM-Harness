---
type: reference
source: https://api.smartlead.ai (official API reference)
retrieved: 2026-08-05
verified_by: direct fetch of listed pages; cross-checked base URL/auth across 3 independent pages
---

# Smartlead — API notes

## Base URL & auth

```
Base URL: https://server.smartlead.ai/api/v1
Auth:     API key as a query string parameter — ?api_key=YOUR_API_KEY
          (there is also a legacy /api/... path; use /api/v1/... )
```

No auth header — the key goes on every request as `api_key=...` in the
query string. Get your key from Smartlead → Settings → API Key.

`config/.env` (gitignored, see `.env.example`):
```
SMARTLEAD_API_KEY=...
```

## Rate limits

Per API key, across **all** endpoints combined (campaign + lead + analytics
calls all share one bucket):

| Tier | Per minute | Per hour | Burst |
|---|---|---|---|
| Standard | 60 | 1,000 | 10 req/sec |
| Pro | 120 | 3,000 | 20 req/sec |
| Enterprise | custom | custom | custom |

On `429`, response includes a `Retry-After` header (seconds) — respect it.
Otherwise back off exponentially (1s, 2s, 4s, 8s, 16s + jitter), max ~5
retries. `pipeline/integrations/smartlead_client.py` implements this.

## The endpoints that matter for "push/create campaigns directly"

These five are verified against the live docs (full request/response
schemas below) and are what `pipeline/integrations/smartlead_client.py`
wraps:

### 1. Create a campaign

```
POST /campaigns/create?api_key=...
Body: {"name": "Q1 2026 ANZ Work Mgmt", "client_id": 123}   # client_id optional
→ 200: {"ok": true, "id": 987, "name": "...", "created_at": "..."}
```

A new campaign is empty — no sequence, no senders, no leads yet. Populate
it with the calls below.

### 2. Set the sequence (subject/body/delay per step)

```
POST /campaigns/{campaign_id}/sequences?api_key=...
Body: {
  "sequences": [
    {
      "id": null,                          // null = new step, number = update existing
      "seq_number": 1,
      "subject": "Hello {{first_name}}",   // omit on follow-ups to keep it a reply-in-thread
      "email_body": "<p>Hi {{first_name}},</p>...",
      "seq_delay_details": {"delay_in_days": 0}
    }
  ]
}
→ 200: {"ok": true, "data": [{"id": 1001, "seq_number": 1, ...}]}
```

**Gotcha:** cannot modify sequences while the campaign is `ACTIVE`. Pause
first (`update-status` → `PAUSED`), edit, then resume (`START`).

### 3. Attach sender accounts

```
POST /campaigns/{campaign_id}/email-accounts?api_key=...
Body: {"email_account_ids": [456, 457, 458]}
→ 200: {"ok": true}
```

Email account IDs come from `GET /email-accounts/` (not yet wrapped in the
client — add if needed).

### 4. Add leads

```
POST /campaigns/{campaign_id}/leads?api_key=...
Body: {
  "lead_list": [                      // max 400 per call
    {
      "email": "jane@acme.com",       // required
      "first_name": "Jane", "last_name": "Doe",
      "company_name": "Acme", "phone_number": "...",
      "website": "...", "location": "...",
      "linkedin_profile": "...", "company_url": "...",
      "custom_fields": {"job_title": "COO"}   // max 200 keys
    }
  ],
  "settings": {
    "ignore_global_block_list": false,
    "ignore_unsubscribe_list": false,
    "ignore_duplicate_leads_in_other_campaign": false,   // leave false — dedupe-on-upload
    "ignore_community_bounce_list": false,
    "return_lead_ids": true
  }
}
→ 200: {"success": true, "added_count": N, "skipped_count": N, "lead_ids": [...], "message": "..."}
```

**Dedupe-on-upload directive:** keep `ignore_duplicate_leads_in_other_campaign:
false` (the default) unless a specific motion has an explicit, documented
reason to override it — that flag is Smartlead's own cross-campaign dedupe
check, and it should stay on by default per `AGENTS.md` §1.1. `pipeline/dedup.py`
should still run before this call; this flag is a second line of defense,
not a replacement.

### 5. Start / pause / stop

```
POST /campaigns/{campaign_id}/status?api_key=...
Body: {"status": "START"}    # NOT "ACTIVE" — use START to launch/resume
      {"status": "PAUSED"}   # temporary
      {"status": "STOPPED"}  # permanent, irreversible
```

## Sentiment-tagging webhook (the AGENTS.md §5 quick win)

```
POST /webhook/create?api_key=...     # note: singular "webhook", not "webhooks"
Body: {
  "name": "Reply Notifications",
  "webhook_url": "https://<make.com-or-n8n-endpoint>",
  "association_type": "campaign",     // or "client" / "user" for broader scope
  "email_campaign_id": 987,           // required when association_type=campaign
  "event_type_map": {"EMAIL_REPLY": true, "EMAIL_OPEN": true}
}
→ 200: {"ok": true, "id": 456, "webhook_url": "..."}
```

Available event types: `EMAIL_SENT`, `FIRST_EMAIL_SENT`, `EMAIL_OPEN`,
`EMAIL_LINK_CLICK`, `EMAIL_REPLY`, `EMAIL_BOUNCE`, `LEAD_UNSUBSCRIBED`,
`LEAD_CATEGORY_UPDATED`, `CAMPAIGN_STATUS_CHANGED`, `UNTRACKED_REPLIES`,
`MANUAL_STEP_REACHED`.

For the interim "any reply" notification (before controlled tags
information-request / book-meeting / positive are wired up), just fire on
`EMAIL_REPLY` and route to Slack via Make.com/n8n.

To actually apply the controlled tags, use lead categorization:

```
GET  /leads/fetch-categories?api_key=...
→ [{"id": 1, "name": "Interested", "sentiment_type": "positive"}, ...]
     # global categories have low IDs; custom categories you create get higher IDs.
     # Smartlead ships defaults like "Interested"/"Not Interested"/"Meeting Booked" —
     # confirm the exact IDs in your account (fetch-categories) before hardcoding.

POST /campaigns/{campaign_id}/leads/{lead_id}/category?api_key=...
Body: {"category_id": 1, "pause_lead": false}
```

## Campaign performance / bounce rate (verified live 2026-08-30 against a real account — corrected from an earlier doc-page fetch that was wrong)

```
GET /analytics/campaign/overall-stats?api_key=...
Query: start_date=YYYY-MM-DD, end_date=YYYY-MM-DD (both required),
       campaign_ids=1,2,3 (optional), client_ids=... (optional)
→ 200: {"ok": true, "data": {"campaign_wise_performance": [
    {"id": 123, "campaign_name": "...", "sent": N, "opened": N,
     "replied": N, "bounced": N}
  ]}}
```

**⚠️ An earlier fetch of this endpoint's doc page (2026-08-14) claimed
additional fields — `open_rate`, `reply_rate`, `bounce_rate`,
`positive_reply_rate`, `positive_replied`, `unique_lead_count`,
`unique_open_count`. Tested live against 6 real campaigns on 2026-08-30:
none of those fields exist. Only `id, campaign_name, sent, opened,
replied, bounced` come back**, every time, no exceptions. Whatever page
was fetched either described a different/newer API version or was
summarized wrong — this is the confirmed, real shape as of 2026-08-30.
Also observed: `opened` was `0` on every campaign checked, real or not
(possibly open-tracking disabled account-wide, or blocked by mail
providers' privacy features — not confirmed either way).

**No `bounce_rate` or `unique_lead_count` field means you compute bounce
rate yourself** — `pipeline/check_bounce_rate.py` uses `bounced / sent`
(per email sent, not per unique lead — a looser number than the "ideal"
per-lead definition, but it's what the real data supports).

This backs Thana's manually-run bounce-rate safety gate (per the
2026-08-30 team call): pause a campaign if bounce rate exceeds 2%, which
she was doing by eyeballing the Smartlead dashboard.
`SmartleadClient.get_campaign_performance()` +
`pipeline/check_bounce_rate.py` encode that same policy as a script —
tested live, dry-run, against the real account the same day.

## Full endpoint index (names only, by category)

Confirmed to exist via the live sitemap (`api.smartlead.ai/sitemap.xml`).
Only the endpoints detailed above have been fetched and verified in full;
everything else below is a name/path only — fetch the specific
`/api-reference/<category>/<slug>` page before building against it.

- **campaigns** — get-all, get-by-id, create, delete, duplicate,
  update-status, update-settings, update-schedule, statistics,
  get-analytics, get-analytics-by-date, get-sequences, update-sequences,
  create-subsequence, get-email-accounts, add-email-accounts,
  remove-email-accounts, get-leads, add-leads, get-lead-by-id,
  update-lead, update-lead-category, update-lead-email-account,
  delete-lead, pause-lead, resume-lead, mark-lead-complete,
  unsubscribe-lead, get-lead-history, get-leads-history-bulk,
  all-leads-activities, export-leads, send-test-email, forward-email,
  reply-email-thread, get-webhooks, save-webhooks, delete-webhook,
  get-webhook-summary, retrigger-webhooks, update-team-member
- **campaign-statistics** — top-level, top-level-by-date, get-by-id,
  get-by-date-range, lead-statistics, mailbox-statistics
- **leads** — get-by-campaign, get-by-email, add-to-campaign, update,
  delete, pause, resume, unsubscribe, categories, activities, export
- **lead-lists** — get-all, get-by-id, create, update, delete,
  import-leads, push-to-campaign, push-between-lists, assign-tags
- **lead-tags / lead-notes / lead-tasks** — create, get-all,
  add-to-lead / remove-from-lead
- **email-accounts** — get-all, get-by-id, add-smtp, add-oauth, update,
  delete, suspend, unsuspend, warmup-settings, warmup-stats, tags
- **email-account-tags** — get-all, create, create-new, assign, remove
- **clients** — get-all, create, update, api-keys
- **webhooks** (account-level, distinct from per-campaign webhooks above)
  — get, create, update, delete, events
- **inbox** (Unibox) — get-unread/-sent/-archived/-important/-scheduled/
  -snoozed/-untracked/-assigned/-views/-messages/-by-id, mark-read, reply,
  reply-status, forward, set-reminder, get-reminders, create-note,
  create-task, update-category, update-team-member, update-revenue,
  push-to-subsequence, resume-lead, block-domains
- **analytics** (agency/reporting rollups) — overview, campaign-list,
  campaign-performance, campaign-response-stats, campaign-status-stats,
  client-list, client-performance, month-wise-client-count, lead-stats,
  lead-category-response, lead-to-reply-time, leads-for-first-reply,
  followup-reply-rate, mailbox-health, domain-wise-health,
  email-wise-health, provider-performance, day-wise-stats,
  day-wise-sent-time, day-wise-positive-reply,
  day-wise-positive-sent-time, team-board-stats,
  how-metrics-are-calculated
- **smart-delivery** (inbox placement testing) — folders, tests
  (manual/automated, list/stop/delete), sender-list/-report,
  domain-blacklist, ip-blacklist-count, ip-details, spf-details,
  dkim-details, rdns-report, provider-report, provider-ids,
  spam-filter-report, geo-report, schedule-history, reply-headers,
  mailbox-count, mailbox-summary, test-details, test-email-content
- **smart-prospect** (built-in lead finder) — search/get/fetch-contacts,
  review-contacts, update-fetched-lead, saved-searches, recent-searches,
  fetched-searches, search-analytics, reply-analytics, and filter-option
  lookups (industries, departments, job-title, levels, company, domain,
  countries, states, cities, revenue, head-counts, keywords,
  sub-industries)
- **smart-senders** (domain/mailbox provisioning) — search-domain,
  domain-list, get-vendors, place-order, order-details, auto-generate,
  get-otp
- **utilities** — send-single-email, domain-block-list

Guides worth reading before building further: `guides/campaign-setup`,
`guides/email-warmup`, `guides/webhook-integration`, `guides/error-handling`,
`guides/best-practices`. Core concept pages: `core/campaigns`,
`core/leads`, `core/email-accounts`, `core/sequences`, `core/webhooks`.

## Used by

- `pipeline/integrations/smartlead_client.py` — the wrapper implementing
  the five calls above plus webhook creation and lead categorization.
- `pipeline/launch_campaign.py` — orchestrates create → sequence → senders
  → leads → start for a motion.
- `skills/campaign-reports/` — see `references/sources.md`; the
  sentiment-tagging webhook is the quick win from `AGENTS.md` §5.
