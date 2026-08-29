---
type: brain
project: Fruition OLE Harness
status: pilot content drafted (v1) — pending Avi/Thana/Josh review
last_updated: 2026-08-05
---

# AGENTS.md — the brain

> Every AI agent (Claude, Codex, Gemini, Grok, ...) reads this file first, via its
> runtime-specific entry file (`CLAUDE.md`, `GEMINI.md`, `.codex/config.md`, ...).
> This is the single source of routing rules, SOPs-in-brief, motion↔workspace
> mapping, and hard directives for the outbound engine. Edit this file once;
> every runtime stays in sync.

## 1. Hard directives (never violate)

1. **Dedupe on upload, always.** No lead enters a sequencer twice across
   campaigns or workspaces. Every upload path goes through
   `pipeline/dedup.py`, which reads `outbound-motions/_LEDGER.md` to know
   which workspaces/campaigns share a dedupe pool. Never hand-assemble a
   sequencer CSV that skips this step.
2. **Never commit `data/`, `exports/`, `.scratch/`, or `config/`.** These are
   gitignored on purpose (see `.gitignore`) — they hold lead data, PII, cost
   logs, credentials, and scratch artifacts. Do not `git add -f` them, and do
   not paste their contents into skills/, sops/, or knowledge/.
3. **Secrets via GitHub Secrets or Doppler only.** A credentials markdown/file
   in `config/` is a temporary local workaround, never a production path. Do
   not author new credential files under version-controlled paths.
4. **Same skeleton every motion.** Every folder under `outbound-motions/`
   contains exactly `icp/ research/ lists/ copy/ campaigns/ reporting/` — no
   ad hoc folders. Company-level offer/positioning lives in `knowledge/`, not
   duplicated per motion.
5. **Python for deterministic machinery, skills for judgment.** High-volume,
   repetitive work (cleaning, dedupe, enrichment of 50k+ leads) runs as
   scripts in `pipeline/`. ICP, copy, and segmentation are skills with human
   SOPs beside them — do not silently automate a judgment call that an SOP
   says needs review.
6. **Draft-v1 content is not launch-ready by default.** Every skill,
   `sops/` doc, and the `outbound-motions/anz-work-management/` content is
   currently a first-pass draft (see §8) — grounded in real source
   material, but unreviewed by Avi/Thana/Josh. Treat "it's written down"
   and "it's approved to use" as two different states; the gates in
   `sops/approval-gates.md` are what separates them.

## 2. Routing table (request type → skill)

| Request looks like... | Route to | Cites SOP(s) |
|---|---|---|
| "Set up / refresh a motion end-to-end" | `skills/fulfillment/` (orchestrates the rest) | all below |
| "Build/update the ICP or lead-fit rubric for X" | `skills/icp/` | `sops/lead-verification.md` |
| "Segment this cleaned list into buckets" | `skills/list-segmentation/` | `sops/lead-verification.md` |
| "Write/refresh sequence copy for a motion" | `skills/campaign-copy/` | `sops/persona-qa.md` |
| "Generate the weekly/monthly report" | `skills/campaign-reports/` | `sops/approval-gates.md` |
| "Clean/enrich/dedupe a raw list" | `pipeline/` scripts directly (no skill needed) | — |
| "Prep and launch an upload" | `pipeline/prepare_upload.py` (CSV) or `pipeline/launch_campaign.py` (direct API push) → **dedupe-on-upload** → `skills/fulfillment/` gate | `sops/approval-gates.md` |

`skills/fulfillment/` is the entry point for a full motion run: it calls
`icp` → pipeline scripts → `list-segmentation` → `campaign-copy` → upload →
`campaign-reports`, in that order, and stops at each gate defined in
`sops/approval-gates.md`.

## 3. Motion ↔ workspace mapping (placeholder)

The authoritative, current mapping lives in
`outbound-motions/_LEDGER.md` — treat that file as source of truth, not this
table.

**Correction (2026-08-05):** this table originally said the remaining 8
motions were "not yet scaffolded," implying greenfield. That's only true
of this *repo* — on the HeyReach side, **all 9 region×product combinations
already have live LinkedIn campaigns** (`V3 - {US,UK,ANZ} ({Service,CRM,WM})`,
all `IN_PROGRESS`, found via `HeyReachClient.get_campaigns()` — see
`knowledge/company/linkedin-messaging-foundation.md`). This repo's
`outbound-motions/` folders and `skills/` playbooks are new work; the
underlying campaigns Thana runs are not. Before scaffolding a new motion
folder, pull the real HeyReach account first and check whether it already
exists, the same way `anz-work-management` turned out to.

| Motion (region × product) | Repo folder status | HeyReach status |
|---|---|---|
| `anz-work-management` | pilot (first working slice) | **live** — `512925`, see `_LEDGER.md` |
| ANZ Service, ANZ CRM | not scaffolded in this repo | live — `512941`, `512937` |
| US Service, US CRM, US WM | not scaffolded in this repo | live — `512943`, `512940`, `512934` |
| UK Service, UK CRM, UK WM | not scaffolded in this repo | live — `512942`, `512939`, `512930` |

Smartlead side of all of the above: unknown, not checked programmatically
(`SMARTLEAD_API_KEY` still unset) — **but confirmed by Thana on the
2026-08-30 call that the V3 Smartlead campaigns exist and are empty,
waiting for leads.** Also confirmed on that same call: this repo's
pipeline is meant to feed these live campaigns, not run separately from
them — see `reports/2026-08-30-open-decisions-for-thana-josh.md` #1. Pull
the real Smartlead IDs the moment the key is set, the same way the
HeyReach ones were found.

## 4. First working slice

Per the startup guide (§7): do not build all nine motions at once. Prove the
full loop (ICP → list → copy → dedupe → upload → report) on
`outbound-motions/anz-work-management/` first. Only templatize to the rest of
the 3×3 matrix once that slice runs cleanly end-to-end.

## 5. Quick wins (run alongside the pilot)

- **Smartlead sentiment tagging** via webhook → Make.com/n8n, tagging
  replies `information-request` / `book-meeting` / `positive`. Interim:
  "any reply" notification so nothing is missed until tagging is live.
  The exact endpoint (`POST /webhook/create`, event types, lead
  categorization calls) is now documented in
  `knowledge/tool-docs/smartlead.md` and wired in
  `SmartleadClient.create_webhook()` / `.update_lead_category()` — the
  Make.com/n8n routing logic and the mapping from Smartlead's default
  category IDs to the three controlled tags is still TODO.
- **Slack notification on positive replies** to close the 5–10 minute
  response window. Not yet wired up — downstream of the webhook above.

## 6. Company context

Company-wide reference docs live in `knowledge/company/`:

- `vision.md` — Director Vision Statement: positioning ("process before
  platform"), target market (mid-market, 25–25,000 staff; construction,
  manufacturing, professional services, NFP, government).
- `sales-process-sop.md` — Sales Process SOP. **Confirms this repo is the
  system backing the "Outbound Lead Engine (OLE)" CRM board** referenced
  there (§2), owned by the Reachly team (Thibault, Utkrusht, Thana) on the
  Clay/n8n/Instantly stack. Also the primary source for `skills/icp/` and
  `skills/campaign-copy/` — the SPIN discovery framework, cold-open
  reframes, and objection handling.
- `delivery-sop.md` — Project Delivery SOP: the process downstream of a won
  deal. Relevant to `skills/campaign-reports/` for what outbound is
  ultimately judged against (§8 Delivery KPIs), not just reply/open rates.

Each skill folder still has a `references/sources.md` pointing at the
specific sections to draw from — kept even now that draft-v1 rubrics/
frameworks exist (§8), since they're what a future revision should
re-derive from if the drafts need rework.

## 7. API integrations (Smartlead, HeyReach, AI Ark)

`pipeline/integrations/` has working API clients for all three external
services — `smartlead_client.py`, `heyreach_client.py`, and
`ai_ark_client.py`. Full endpoint docs (auth, schemas, rate limits, known
gotchas) live in `knowledge/tool-docs/{smartlead,heyreach,ai-ark}.md`;
read those before extending the clients, don't re-derive from memory.
**Naming note:** the sourcing tool is **AI Ark** (`ai-ark.com`), not
"AI Arc" as the original startup guide and this repo's earlier stub had
it — corrected 2026-08-14.

Smartlead and HeyReach are confirmed working against real accounts
(HeyReach with a live key at time of writing; Smartlead client built and
unit-tested but never called with a real key — no `SMARTLEAD_API_KEY` was
available). **AI Ark is built and unit-tested against its documented
response schemas, but has never been called with a real key either** — no
`AI_ARK_API_KEY` was available when it was wired up. Run
`python3 -m pipeline.check_integrations` once each key is added; it now
checks all three.

**Setup:** copy `config/.env.example` to `config/.env` and fill in
`SMARTLEAD_API_KEY` / `HEYREACH_API_KEY` / `AI_ARK_API_KEY` (gitignored —
never commit the real file). In CI, set these via GitHub Secrets/Doppler
instead, per §1.3. `pip install -r requirements.txt` for `requests` +
`python-dotenv` (no new dependency for AI Ark — same `requests`-based
client pattern as the other two).

AI Ark is credit-metered (not just rate-limited like the other two) —
`AIArkClient.get_credit()` / `check_integrations.py` shows remaining
balance. `pipeline/source_leads.py` and `pipeline/enrich.py` now call it
live when `AI_ARK_API_KEY` is set (source_leads additionally needs
`--filters`, a JSON file translating a motion's ICP rubric into AI Ark's
filter syntax — a human/skill judgment call, not auto-derived); both fall
back to their original file-based behavior otherwise. See
`knowledge/tool-docs/ai-ark.md` for the two-step search-then-export
pattern this is built around.

`pipeline/launch_campaign.py` pushes a deduped lead CSV directly into a
campaign via API (as an alternative to `prepare_upload.py`'s CSV-assembly
path). **Read this before using it on HeyReach:** a campaign created via
`HeyReachClient.create_campaign()` lands in DRAFT status, and there is
currently no verified API call in this client to activate it — that gap is
documented in `knowledge/tool-docs/heyreach.md` and is not silently
papered over. Smartlead has no equivalent gap — `update_status(..., "START")`
works as documented.

**`pipeline/check_bounce_rate.py`** (added 2026-08-30) encodes Thana's
existing manual policy — pause a Smartlead campaign above 2% bounce rate
— via the newly-confirmed `SmartleadClient.get_campaign_performance()`.
Defaults to report-only; `--auto-pause` is required to actually mutate a
live campaign. Unit-tested against mock data, never run live (needs
`SMARTLEAD_API_KEY`).

Neither client's higher-level orchestration (sequence copy, sender
rotation, which existing campaign to target) is decided here — those are
`skills/campaign-copy/` and `skills/fulfillment/` judgment calls, left as
TODOs in `launch_campaign.py`.

## 8. Pilot content status (draft v1 — read before treating anything as final)

Everything below was written in one pass, grounded in
`knowledge/company/` and the real HeyReach account data pulled via
`pipeline/check_integrations.py` — not fabricated, but also not yet
proven against real send data. **Original guide directive:** skills/SOPs
were meant to be authored collaboratively with Avi over the engagement,
not generated blind — this pass exists because the repo owner explicitly
requested full drafts now. Treat it as a strong starting point for that
collaboration, not a substitute for it.

**Written and populated:**
- `skills/{icp,list-segmentation,campaign-copy,campaign-reports,fulfillment}/instructions.md`
- `sops/{lead-verification,persona-qa,approval-gates}.md`
- `outbound-motions/anz-work-management/{icp,research,lists,campaigns,reporting}/`
  — frameworks and templates; `lists/`, `reporting/` intentionally hold no
  data yet (nothing to segment/report on until the pipeline has a real
  lead source)
- `outbound-motions/anz-work-management/copy/` — one complete champion-persona
  sequence per channel (email + LinkedIn); economic-buyer/influencer
  variants still TODO
- `pipeline/{clean_normalize,dedup,personalization/evidence_lines,prepare_upload}.py`
  — fully implemented and integration-tested (chained end-to-end: raw →
  enriched → cleaned → deduped → personalized → upload-ready CSV)
- `pipeline/{source_leads,enrich}.py` — **updated 2026-08-14**: now call
  AI Ark live (`pipeline/integrations/ai_ark_client.py`) when
  `AI_ARK_API_KEY` is set, falling back to the original file-based
  consolidation/best-effort enrichment otherwise. Unit-tested against AI
  Ark's documented response schemas; never called with a real key (none
  was available). See §7.

**Correction (2026-08-14):** the line above used to say no campaign had
been created for this motion. Wrong — see §3: HeyReach campaign `512925`
is live and has real performance data
(`reports/2026-08-14-heyreach-linkedin-performance-snapshot.md`). What's
still true: this repo's ICP rubric, segmentation, and copy have not been
validated against that live send data, because this repo's pipeline isn't
actually feeding that campaign (open question in `campaigns/launch-plan.md`).
Smartlead side: still unchecked either way.

**Before this goes live:** run it through the gates in
`sops/approval-gates.md`, same as any other motion — nothing here is
exempt from review just because an agent wrote the first draft instead of
a human.

## 9. GTM frameworks & the lookalike loop

`knowledge/frameworks/` (previously an empty stub) now has two real docs,
benchmarked against a reference GTM-harness structure the repo owner
shared and adapted for Fruition's actual tooling and motion model:

- `b2b-lead-sourcing.md` — the Database/Signals/Scraping framework. This
  harness covers Database + Signals via AI Ark; Scraping is flagged as a
  genuine open decision (needs a tool choice from Thana/Josh + real
  research the same way AI Ark was), not silently skipped.
- `gtm-outbound-loop.md` — maps Lead Sourcing → Outreach → Reporting onto
  this repo's existing skills/pipeline (no restructuring needed, it
  already matched), and adds the one real missing piece: a **closed-won →
  lookalikes feedback loop** via `pipeline/find_lookalikes.py`, using AI
  Ark's `lookalikeDomains` search. Lookalike-sourced leads get no
  qualification shortcut — see `skills/icp/instructions.md` §6.
- That same doc also records **three patterns deliberately not adopted**
  from the benchmark: a `clients/`-per-customer structure (wrong model —
  this repo is one company's own motion-based outbound, not
  agency-for-hire), a committed `secrets/` folder (worse than this repo's
  existing `config/.env` + Secrets/Doppler pattern), and a live deployed
  dashboard (premature — the startup guide's §7 sequencing says prove the
  pilot slice first).

**Real gap this loop currently has:** no CRM integration exists, so
`outbound-motions/anz-work-management/research/closed-won-seeds.md` (the
seed-domain list `find_lookalikes.py` needs) is a template with no real
rows — Fruition's regional CRM boards live in monday.com and aren't
queried anywhere in this repo yet.
