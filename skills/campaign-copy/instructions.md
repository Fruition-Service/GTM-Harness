---
skill: campaign-copy
status: draft-v1
gate: sops/persona-qa.md
---

# campaign-copy

Drafts sequence copy from the ICP avatar + segmented list + past results,
runs spam checks, writes to `outbound-motions/<name>/copy/`.

> **Status:** draft v1. The framework and hooks below are grounded in
> `knowledge/company/sales-process-sop.md`'s SPIN discovery guide — the
> actual sequence text for a motion (see
> `outbound-motions/anz-work-management/copy/`) is a first pass to sharpen
> with real reply data, not final copy to run unreviewed.

## 1. Voice — calibrate against the discovery guide, not generic SDR copy

Every sequence should read like the consultant on a discovery call, not a
volume-outreach template. Concretely:

- **Diagnose before prescribing.** Open with an insight/reframe, not a
  feature pitch. Fruition's three validated reframes
  (`sales-process-sop.md`):
  1. "Most teams don't have a software problem — they have a
     work-scattered-across-ten-tools problem."
  2. "The teams that get real ROI aren't the ones with the biggest
     budget — they're the ones who fixed the process before they bought
     the tool."
  3. "Everyone wants AI. The ones who win start by finding where people
     repeat the same decision fifty times a week."
- **Make the pain concrete, not generic.** Pull from the Problem/
  Implication question bank in the discovery guide (bottlenecks, manual
  work nobody owns, things slipping through the cracks, cost in hours/
  missed deadlines) — but only claim what the buying signal actually
  supports. Don't assert a pain you have no evidence for.
- **One clear ask per email.** Mirror the discovery call's "always
  advance" rule — every step ends with a specific, low-friction next step
  (a question, not "let me know if you're interested").

## 2. Sequence architecture (starting template — tune per motion)

**Email (Smartlead), 4 steps:**

| Step | Delay | Purpose | Structure |
|---|---|---|---|
| 1 | Day 0 | Insight-led opener | Reframe → one-line pain hypothesis tied to their buying signal → single question CTA |
| 2 | +3 days | Proof / specificity | Name the cost of inaction in their terms (hours/deadlines/headcount) → light proof point → CTA |
| 3 | +5 days | Reframe the objection pre-emptively | Address the most likely objection for this persona (see §3) before they raise it → CTA |
| 4 | +7 days | Breakup | Short, no guilt-trip, leaves the door open, restates the one-line value prop |

**LinkedIn (HeyReach), for Tier A multi-touch accounts:** connection
request (no pitch, just a real reason to connect) → wait for acceptance →
message 1 mirrors email step 1's reframe → message 2 (if no reply) offers
a specific asset or insight, not "just checking in".

Adjust step count/timing per motion based on what
`skills/campaign-reports/` shows is working — this is a starting
hypothesis, not a fixed rule.

## 3. Objection pre-emption (use in step 3 or in follow-ups)

Straight from `sales-process-sop.md`'s objection quick-turns — adapt the
turn, don't quote it verbatim as if the prospect already objected:

| Likely objection | Reframe to use |
|---|---|
| "We could build this ourselves" | Time-cost framing: what's their team's time worth against their actual roadmap, vs. something deployed 600+ times already. |
| "Too expensive" | Anchor against the hours/cost already named in their world, not against Fruition's rate. |
| "Not the right time" | Priority-vs-budget distinction — the cost of the status quo doesn't pause either. |

## 4. Role-based variants (Tier A multi-contact accounts)

Per `skills/list-segmentation/` §3, write distinct variants per role, not
one email to three people:

- **Economic buyer:** lead with cost/ROI framing, Implication-stage
  language (headcount cost, scale risk).
  **Champion:** lead with the day-to-day pain, Problem-stage language
  (manual work, bottlenecks).
  **Influencer:** lead with the relief/quality-of-life angle,
  Need-payoff-stage language ("what would that free you up to do").

## 5. Proof points (use sparingly, always current)

Pull only from `knowledge/company/vision.md` /
`knowledge/company/sales-process-sop.md` — never invent a stat:

- monday.com Platinum Partner, Partner Summit Rising Star 2026
- "600+ deployments" (used in the objection quick-turn, sales SOP)
- Case studies — reference only if a real one exists for the motion's
  vertical; don't gesture at "case studies" generically if none apply.

## 6. House style (non-negotiable, per sales-process-sop.md §7)

Plain text only. No markdown bold/italics. No horizontal rule lines. No
excessive links (one CTA link max). This applies to every generated
sequence — it's the same rule human reps follow for client-facing drafts.

## 7. Output

`outbound-motions/<name>/copy/<sequence-name>.md` — one file per
sequence/variant, plus a `spam-check-results.md` log. Format each step
with step number, delay, subject (email only), and body.

## Gate

`sops/persona-qa.md` — every sequence reviewed before it's attached to a
live campaign.

## References

See `references/sources.md`.
