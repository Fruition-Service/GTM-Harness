---
type: framework
status: draft-v1
source: benchmarked against a reference GTM-harness structure ("How we Run GTM at AptAI Systems"), adapted for Fruition's actual tooling and motion model
---

# The GTM / outbound loop

A three-stage loop that feeds back into itself:

```
Lead Sourcing  →  Outreach Messages  →  Reporting / Analytics
     ↑                                          |
     └──────────────────────────────────────────┘
              (closed-won → lookalikes)
```

## How each stage maps onto this harness

| Loop stage | What it covers | This harness's implementation |
|---|---|---|
| **Lead Sourcing** | List building, segmentation, scoring/tiering | `pipeline/source_leads.py` (AI Ark) → `pipeline/enrich.py` → `pipeline/clean_normalize.py` → `skills/list-segmentation/` |
| **Outreach Messages** | Sequencers, infra, copywriting/offers, multichannel, split tests | `skills/campaign-copy/` → `pipeline/dedup.py` → `pipeline/prepare_upload.py` / `pipeline/launch_campaign.py` → `pipeline/integrations/{smartlead,heyreach}_client.py` |
| **Reporting / Analytics** | Closed-won tracking, lookalikes, performance | `skills/campaign-reports/` → `pipeline/integrations/*_client.py` stats calls (e.g. `HeyReachClient.get_overall_stats()`) — see `reports/2026-08-14-heyreach-linkedin-performance-snapshot.md` for a worked example |

This is a close structural match to the pipeline this repo already had —
the loop framing doesn't require new folders, it's the same six pipeline
scripts and five skills already built.

## The feedback loop this harness was missing: closed-won → lookalikes

The one genuinely new capability worth adding: **feeding won deals back
into sourcing**, not just reporting on them. AI Ark's Company Search
already supports this — `lookalikeDomains` (max 5 seed domains per call)
finds companies similar to ones you give it
(`knowledge/tool-docs/ai-ark.md`). `pipeline/find_lookalikes.py` wraps
this: seed it with closed-won account domains, get back similar
companies, and hand those domains to `pipeline/source_leads.py --filters`
for a normal People Search pass.

**This is not a shortcut around ICP qualification.** Lookalike-sourced
companies still go through the same `skills/icp/` rubric and
`sops/lead-verification.md` gates as anything else — "looks like a
closed-won account" is a sourcing signal, not a scoring exemption. See
`skills/icp/instructions.md` §5 and
`skills/list-segmentation/instructions.md`.

**What's missing to actually run this loop today:** a real list of
closed-won accounts. This repo has no CRM API access (Fruition's regional
CRM boards live in monday.com, not queried anywhere in this repo) — see
`outbound-motions/anz-work-management/research/closed-won-seeds.md`,
which is a template, not data. Someone needs to either manually maintain
that list or this repo needs a monday.com CRM integration researched and
built the same way AI Ark was, before this loop runs on real data instead
of a placeholder.

## What this harness deliberately did *not* copy from the reference structure

Benchmarking surfaced a few patterns worth naming as **considered
rejections**, not oversights:

- **`clients/` instead of `outbound-motions/`.** The reference structure
  is client-services-shaped (one folder per client, with `kickoff/` and
  `handoff/` subfolders) — appropriate for an agency running GTM *as a
  service* for multiple clients. Fruition's OLE is the opposite: one
  company running outbound *for itself*, organized by motion
  (region × product), per the original startup guide. Renaming to
  `clients/` would import the wrong mental model. Fruition's actual
  per-client delivery process already exists and is documented in
  `knowledge/company/delivery-sop.md` — it's a different system from this
  one, correctly.
- **A `secrets/` folder.** However it's handled on the reference side,
  committing a folder literally named `secrets/` is worse practice than
  what this repo already does: `config/.env` (gitignored) +
  `config/.env.example` (tracked, blank) + GitHub Secrets/Doppler in CI,
  per `AGENTS.md` §1.3. Not adopting this.
- **A live, deployed dashboard.** The reference structure has a
  `vercel.json`, implying an actually-deployed app. This repo's
  `dashboard/` is intentionally still a placeholder — the original
  startup guide's sequencing (§7) is explicit: prove the first working
  slice before templatizing or adding a dashboard layer. Building one now
  would be ahead of where this harness actually is.

## Used by

- `pipeline/find_lookalikes.py`
- `skills/campaign-reports/instructions.md` — closed-won tracking is the
  input this loop needs; currently absent, see the gap noted above.
