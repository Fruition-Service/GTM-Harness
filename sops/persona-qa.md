---
sop: persona-qa
cited_by: [skills/campaign-copy]
status: draft-v1
owner: Thana (Reachly team) — review with Josh before treating as final
---

# Persona QA (SOP)

Human checklist for outbound copy before it goes live in a sequencer
(Smartlead or HeyReach). Gates `skills/campaign-copy/` output.

## Checklist (every sequence, every variant)

1. **Voice match.** Copy sounds like `knowledge/company/sales-process-sop.md`'s
   discovery guide — consultative, diagnosis-before-prescription, not a
   generic SDR template. Re-read the three cold-open reframes and the
   objection quick-turns in that doc as the calibration reference.
2. **Claims are substantiated.** Any stat or claim ("600+ deployments",
   "Platinum Partner", case-study references) must trace to
   `knowledge/company/vision.md` or a real, current data point — never
   invented or rounded up for effect.
3. **Personalization fields resolve.** Every `{{merge_field}}` has a real
   source column in the prepared lead list; no sequence ships with a
   merge field that will silently render blank or literal `{{...}}` text.
4. **House style.** Per `sales-process-sop.md` §7: plain text, no markdown
   bold/italics, no horizontal rule lines. This applies to generated
   sequence copy exactly as it does to human-written client messages.
5. **Spam-check passed.** Run the copy through the sequencer's spam-check
   (Smartlead has one built in) or an equivalent tool before scheduling.
   Flag: excessive links, ALL CAPS subject lines, spam-trigger phrases
   ("free", "guarantee", "act now"), missing unsubscribe footer.
6. **Compliance footer present.** Unsubscribe/opt-out language on every
   sequence, per platform requirements and general anti-spam law
   (CAN-SPAM / Australian Spam Act / UK PECR depending on region).
7. **No overclaiming vs. the signed offer.** Copy doesn't promise anything
   outside what Fruition can actually deliver (scope, timeline, price) —
   cross-check against `knowledge/company/sales-process-sop.md` §1 default
   rate and positioning if pricing language is used at all (usually it
   shouldn't be, this early in the funnel).

## Sign-off

One Reachly team member reviews every new sequence before it's attached to
a live campaign (`campaigns/update-sequences` on Smartlead,
`campaign/UpdateSequence` on HeyReach). Re-review is required any time
copy is meaningfully edited, not just on first creation.
