# gtm-harness — Fruition OLE (Outbound Lead Engine)

One repo = one operating system for outbound. Centralizes AI Ark, Clay,
Smartlead, and HeyReach into a single command centre driven by Claude
Code / Codex / Gemini.

**Start here → [`AGENTS.md`](AGENTS.md).** It's the brain file every agent
runtime reads first (via `CLAUDE.md` / `GEMINI.md` / `.codex/config.md`):
routing rules, hard directives (dedupe-on-upload, no-commit-data, secrets
handling), and the motion↔workspace mapping.

## Layout

| Path | What it is |
|---|---|
| `AGENTS.md` | the brain — routing, directives, motion↔workspace map |
| `skills/` | reusable agent playbooks (icp, list-segmentation, campaign-copy, campaign-reports, fulfillment) |
| `sops/` | human-review docs the skills cite |
| `pipeline/` | deterministic Python scripts for sourcing/enriching/cleaning/deduping/uploading leads; `integrations/` has working Smartlead/HeyReach/AI Ark API clients |
| `outbound-motions/` | one folder per motion (region × product); `_LEDGER.md` is the routing table |
| `knowledge/` | evergreen reference (tool API docs incl. verified Smartlead/HeyReach/AI Ark schemas, frameworks, company docs) |
| `dashboard/` | optional web app over campaign/pipeline state |
| `reports/` | generated cross-motion reports |
| `config/`, `data/`, `exports/`, `.scratch/` | gitignored — never committed |

## Status

**Pilot content: draft v1, pending review.** Skills and SOPs now have real
first-draft content (ICP rubric, copy sequences, segmentation logic,
report template, approval gates) grounded in `knowledge/company/` — but
unreviewed by Avi/Thana/Josh and not yet validated against live send
data. See `AGENTS.md` §8 for exactly what's drafted vs. still open.

`pipeline/` is functionally implemented and integration-tested end-to-end
(source → enrich → clean → dedupe → personalize → upload-ready CSV).
`source_leads.py`/`enrich.py` call AI Ark live for real sourcing/email-
finding when `AI_ARK_API_KEY` is set, falling back to local file-based
consolidation/best-effort enrichment otherwise — see `AGENTS.md` §7.

**`anz-work-management` is not a from-scratch pilot.** Pulling the real
HeyReach account found this motion's campaign already live
(`512925 — "V3 - ANZ (WM)"`, `IN_PROGRESS`, real performance data in
`reports/2026-08-14-heyreach-linkedin-performance-snapshot.md`) — in fact
all 9 region×product combinations already have live HeyReach campaigns.
This repo's pipeline isn't currently wired to feed them; see
`outbound-motions/anz-work-management/campaigns/launch-plan.md` for the
open question to resolve with Thana before building further on top.

The Smartlead/HeyReach/AI Ark API clients (`pipeline/integrations/`) are
built and unit-tested; HeyReach is additionally confirmed against a real
account. Add real keys to `config/.env` (copy from `config/.env.example`)
and run `python3 -m pipeline.check_integrations` to verify each one. See
`AGENTS.md` §7.
