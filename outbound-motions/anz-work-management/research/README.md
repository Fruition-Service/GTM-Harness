# research/ — anz-work-management

- [`source-register.md`](source-register.md) — where each buying signal
  comes from, its wiring status, the proof-catalog schema, and the QA
  checklist evidence must pass before it reaches copy. **Updated
  2026-08-14** — AI Ark is wired (was a stub before); most signals map to
  a real AI Ark filter now.
- [`closed-won-seeds.md`](closed-won-seeds.md) — seed domains for
  `pipeline/find_lookalikes.py`'s closed-won → lookalikes loop
  (`knowledge/frameworks/gtm-outbound-loop.md`). Template only, no CRM
  integration exists to populate it with real data yet.

No evidence entries exist in `source-register.md`'s proof catalog yet —
`pipeline/source_leads.py` is wired to AI Ark but hasn't been run with
real `--filters` for this motion. This folder holds schemas and sourcing
plans, not fabricated example data.
