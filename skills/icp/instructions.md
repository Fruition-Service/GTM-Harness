---
skill: icp
status: draft-v1
gate: sops/lead-verification.md (Gate 1)
---

# icp

Builds the ideal-customer-profile avatar and lead-fit scoring rubric for a
motion. Output goes to `outbound-motions/<name>/icp/` as two files:
`avatar.md` (narrative description) and `lead-fit-rubric.md` (scoring
table). Both are inputs to `skills/list-segmentation/`.

> **Status:** draft v1, written from `knowledge/company/vision.md` and
> `knowledge/company/sales-process-sop.md`. This is a first pass for Avi,
> Thana, and Josh to sharpen against real motion performance — not a
> finished rubric. Treat every weight and threshold below as a starting
> hypothesis, not gospel.

## 1. Baseline target market (applies to every motion unless overridden)

Pulled directly from `knowledge/company/vision.md` — don't re-derive this
per motion, just confirm the motion's region/product fits inside it:

- **Org size:** 25–25,000 staff (mid-market — too complex for
  out-of-the-box templates, too pragmatic for enterprise consulting
  theatre).
- **Verticals:** construction, manufacturing, professional services, NFP,
  government. A motion targeting outside this list needs an explicit
  reason documented in the motion's `icp/avatar.md`, not a silent
  expansion.
- **Platform signal:** currently on monday.com (Orange Bucket — see §4) or
  showing tool-sprawl pain that monday.com/the relevant platform solves
  (net-new).

## 2. Avatar template (`icp/avatar.md`)

For each motion, fill in:

```markdown
# <motion> — ICP Avatar

## Who they are
- Company size: <range within 25-25,000, narrowed for this motion>
- Vertical(s): <one or more from the baseline list, or justified exception>
- Region: <the motion's region>
- Department/buyer: <who owns the pain — Ops, PM office, Service delivery, etc.>

## The pain (use the SPIN Problem/Implication framing, not generic copy)
- What's broken today: <tool sprawl / manual reporting / no single source
  of truth — reference sales-process-sop.md's Problem-stage question bank>
- What it costs them: <hours, missed deadlines, key-person risk — Implication stage>
- Why now: <trigger — recent hire, funding, headcount growth, a bad
  quarter, a platform migration already underway>

## Buying signals (must each name a real source)
- <signal> — sourced via <AI Arc / Clay / Sales Navigator / etc.>
- <signal> — sourced via <...>

## Champion profile
- Title/seniority: <who typically champions this internally>
- What they care about: <tie back to Need-payoff stage — what they'd sell
  internally if this got fixed>

## Disqualifiers
- <e.g. already a Fruition/OG Labs/Senzo client>
- <e.g. company size outside band>
- <e.g. no budget authority at the seniority level being contacted>
```

## 3. Lead-fit rubric (`icp/lead-fit-rubric.md`)

Points-based, four weighted categories, 100 points total. Starting
weights — adjust per motion based on what `skills/list-segmentation/`
and `skills/campaign-reports/` show is actually predictive:

| Category | Weight | Scoring guidance |
|---|---|---|
| Firmographic fit | 35 | Full points if size + vertical exactly match §1; partial credit for adjacent verticals or edge-of-band size; zero if outside band entirely. |
| Buying signal strength | 30 | Full points for a recent (<90 day) trigger event (funding, leadership hire, headcount jump); partial for an older or weaker signal; zero for no identifiable trigger. |
| Champion accessibility | 20 | Full points if a named contact at the right seniority is identifiable and reachable; partial if only a generic company-level contact exists; zero if no path to a decision-maker. |
| Platform/tooling signal | 15 | Full points for confirmed monday.com usage (Orange Bucket) or explicit tool-sprawl evidence (job postings mentioning multiple disconnected tools, G2/Capterra reviews, etc.); partial for ambiguous signal; zero for none. |

**Bucket thresholds** (feeds `skills/list-segmentation/` directly):

- **80–100:** Tier A — highest priority, multi-touch/multi-persona motion.
- **60–79:** Tier B — standard sequence.
- **40–59:** Tier C — lighter-touch or nurture only.
- **<40:** excluded — does not enter the sequencer.

## 4. Orange Bucket (existing monday.com users) — separate path

Per `knowledge/company/sales-process-sop.md` §5, existing monday.com
accounts are qualified differently — the 7-question Orange Bucket script
(what did you intend to solve, how's it going 1–10, etc.) replaces cold
firmographic scoring. **Do not blend Orange Bucket leads into the cold
lead-fit rubric above** — score them qualitatively against those 7
questions instead, and flag them as `segment: orange-bucket` for
`list-segmentation` to route separately.

## 5. Signal sourcing notes

Every signal in the rubric must be traceable to a pipeline step:
`pipeline/source_leads.py` (raw pull) → `pipeline/enrich.py`
(firmographic/contact enrichment) → this rubric scores the enriched
record. If a signal can't currently be sourced by the pipeline as built,
don't put it in the rubric yet — flag it as a pipeline gap instead of
scoring on data you don't actually have.

## 6. Lookalike-sourced leads get no exemption

`pipeline/find_lookalikes.py` (`knowledge/frameworks/gtm-outbound-loop.md`)
can source leads from companies that resemble closed-won accounts.
"Resembles a closed-won account" is a sourcing signal, not a
qualification shortcut — lookalike-sourced leads go through this same
rubric like any other sourced lead, no separate fast-track tier.

## Gate

Every rubric and avatar goes through `sops/lead-verification.md` Gate 1
before it's used to score a live list — see that SOP for the checklist.

## References

See `references/sources.md`.
