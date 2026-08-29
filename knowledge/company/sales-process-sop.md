---
type: reference
source: Fruition Services — Sales Process SOP
version: "1.0"
date: 2026-07
owner: Josh Jebathilak, Managing Director
source_systems: Fruition CRM workspace (monday.com), Company SOPs board, Collateral board, Fireflies
---

# Fruition Services — Sales Process SOP

Version 1.0 | July 2026 | Owner: Josh Jebathilak, Managing Director
Source systems: Fruition CRM workspace (monday.com), Company SOPs board,
Collateral board, Fireflies

## 1. Purpose & Positioning

This SOP defines how Fruition Services takes an opportunity from first
contact through to a signed work order and a clean handover into delivery.
It applies across all three entities (AU, US, UK) and all regional
pipelines.

Fruition sells outcomes, not hours. Our positioning is "process before
platform" — we design the operational system first, then implement the
technology. Every sales conversation should reflect this: we diagnose
before we prescribe, and we demo only against confirmed pain.

Key commercial facts:

- Default rate: $250/hr AUD (regional equivalents for UK/US engagements)
- Partner status: monday.com Platinum Partner; monday.com Partner Summit
  Rising Star 2026 (feature in all sales materials, alongside Senzo's
  Atlassian Rising Star 2026 where relevant)
- Target market: mid-market organisations (25–25,000 staff), with depth in
  construction, manufacturing, professional services, NFP, and government
- Presenter/author on all proposals: Josh Jebathilak

## 2. Lead Sources & Intake

1. **monday.com AE referrals** — the primary channel. Reps maintain active
   AE relationships (target: 50 LinkedIn connections/week during ramp,
   ongoing AE meeting cadence). All new-business or license-upgrade
   opportunities for AU must be registered via the Deal Registration Form
   (Collateral board — "License deal registration").
2. **Outbound (Reachly engine)** — Clay/n8n/Instantly stack run by the
   Reachly team (Thibault, Utkrusht, Thana), managed through the **Outbound
   Lead Engine (OLE) CRM board**. Outbound messaging is built on
   buying-signal hooks and competitive displacement positioning (notably vs
   Smartsheet and SimPro).
3. **Inbound** — website, LinkedIn content, Google reviews, case studies.
4. **Referral partners** — onboarded via the Referral System SOP (partner
   agreement signed, leads submitted through the Referrals board
   parent/sub-item structure). Internal referral bonus: $500 USD one-time
   if the referral becomes a client.
5. **Existing client expansion** — optimisation and phase-two work
   identified during delivery (see Orange Bucket, section 5).

All opportunities live in the regional CRM boards: Fruition CRM (APAC),
(UK), (NA), (SEA), (I&UAE), and (OLE) for outbound, with shared Contacts,
Accounts, and Activities boards. Every meeting is recorded in Fireflies —
transcripts are the raw material for proposals and delivery handover.

> **Harness note:** this confirms the `gtm-harness` repo *is* the system
> backing the OLE CRM board referenced above, owned by the Reachly team
> (Thibault, Utkrusht, Thana). See `AGENTS.md` §6.

## 3. The Core Sales Motion (New Business)

### Stage 1 — Initial Contact

Customer books a meeting (Calendly links on the Collateral board). Confirm
attendees, company context, and any AE involvement. Record the deal
registration if it's a monday.com license opportunity.

### Stage 2 — Discovery Meeting (30 minutes)

Follow this structure in order:

1. **Up-front contract** — agree the agenda, time, and what a good outcome
   looks like for both sides.
2. **Situation** — landscape, current state, why change now.
3. **Pain** — what's not working. Dig for specifics and quantify where
   possible.
4. **Short product demo** — only against the pain surfaced. No generic
   tours.
5. **Impact** — what happens if this doesn't get fixed.
6. **Need** — how soon it needs to be fixed.
7. **Range** — share indicative pricing to qualify budget early.
8. **Next steps** — book the deep dive workshop or targeted demo before
   leaving the call.

Use the Fruition Discovery Framework (Collateral board) and the Five Ps
lens — Problem, Process, People, Pain, Payoff — to structure questioning.

### Stage 3 — Deep Dive Workshop (60 minutes)

Process mapping session using the Process Mapping template deck. Map
current state → future state, identify the workflows in scope, the teams
involved, data/reporting requirements, and integrations (Xero, SimPro,
Fishbowl, etc.). Send the CRM & Project or monday Service questionnaire
ahead of the session where useful. Identify the client champion and key
decision-makers — this determines who must attend kickoff later.

### Stage 4 — Proposal

Generate via the fruition-proposal-generator skill from the Fireflies
discovery transcript. Standard output: branded .docx with cover page,
landscape & objective, workflow diagram, phase breakdown, deliverables
table, investment summary (AUD, $250/hr default), next steps, and the
Fruition intro page (Platinum tier + Rising Star 2026). Supporting
collateral: Industry Slides, Proposal Deck Template, AI Pricing Deck,
monday CRM + Xero Package deck, Construction Product Overview — select by
vertical. Present live wherever possible; never just email a proposal cold.

### Stage 5 — Work Order & Signature

Follow the Work Order Creation SOP:

1. Send the Work Order Form (WOF) to the client.
2. When the submission lands on the Work Order board, complete the
   Statement of Work, link the Fruition CRM item, and verify mirror
   columns (Unit Value, Hours, Discount).
3. Classify as **One-off** or **Managed Service** (Managed Service uses the
   separate Managed Services Agreement template, currently populated
   manually and sent via DocuSign).
4. Send: use "Create Draft" for manual review (mandatory if SOW exceeds
   2,000 characters), otherwise set status to "Ready to send" for automatic
   DocuSign dispatch.
5. On signature, status auto-updates to Won and a new item is created on
   the Client Projects board.

### Stage 6 — Handover & Kickoff Booking

On Won:

- Assign the Delivery Manager and Implementation Consultant.
- Sales rep sends the intro-to-PM/kickoff email (template on Collateral
  board) introducing the delivery lead.
- Run the internal sales-to-delivery handover: delivery lead reviews all
  Fireflies transcripts (presales + discovery), the SOW, and the project
  brief before any client contact.
- Book the kickoff meeting. The sales rep remains attached to the account
  for escalation and expansion.

## 4. Qualification & Estimation Standards

- Qualify budget early with indicative ranges — do not run deep dives for
  unqualified prospects.
- Use the Sales Estimation board and the AE Help Request Form for scoping
  support on complex deals.
- Reference the Fruition/OG Labs Platform Analysis Cheat Sheet for
  multi-platform or competitive evaluations (monday.com, HubSpot, ClickUp,
  Atlassian, Zoho).
- Standard support attach on closing: recommend 10 hours/month for 3
  months then 5 hours/month for 3 months as rollout insurance — 6-month
  commitment secures a 10% discounted rate with unused hours carried
  forward.

## 5. Orange Bucket — Existing monday.com Users (Optimisation Motion)

For accounts already on monday.com (AE-referred optimisations, expansions):

1. What did you intend to solve by introducing monday.com?
2. On a scale of 1–10, how is your current setup going? Drill into the gap.
3. What's the key improvement since adopting it? What did you use before?
4. Which teams do you work closely with day to day, and what's their
   involvement?
5. Quick best-practice demo against their use case — show how we solve the
   pain.
6. Provide an estimate and/or options; ask which option fits best.
7. Book next steps and send the proposal.

## 6. Commissions & Incentives

- **Project sales commission:** 10% on new sales owned by the rep; 5% if
  supported or co-sold.
- **monday.com license commission:** 10% of Fruition's license commission,
  paid quarterly (reflecting monday.com's ~90-day payment terms to
  Fruition).
- **Referral bonus:** $500 USD one-time for successful client referrals.
- Related contribution bonuses: case study $200 USD; reusable solution
  template $150 USD (Loom + template/JSON + description, uploaded to the
  Fruition workspace).

## 7. Sales Team Standards

- Every client call runs through Fireflies. No exceptions — transcripts
  feed proposals, handover, and delivery.
- CRM hygiene is non-negotiable: correct stage, owner, value, hours, and
  linked account/contacts before any deal advances.
- New sales hires complete the Sales Onboarding Plan: tool access,
  monday.com and make.com certifications, listening to recorded discovery
  calls and AE pitches, AE connection targets, and first meetings booked in
  week one to four.
- Message drafts to clients and AEs: plain text, no markdown bold/italics,
  no horizontal rule lines.
- All client-facing materials use Fruition purple (#5B2D8F) and feature
  Platinum tier + Rising Star 2026.

---

## THE FRUITION DISCOVERY GUIDE

**The 15-Question SPIN Playbook**

*Consultative discovery for multi-software, AI, and professional-services
engagements*

Built for implementation consultants who also sell. You are a consultant
first — discovery is diagnosis, not interrogation. But every diagnosis has
a purpose: a committed next step. Consultative core, tough edges.

### How to run a Fruition discovery call

1. **Diagnose before you prescribe.** Talk 30%, listen 70%. Earn the right
   to recommend before you pitch a single feature.
2. **Sell the cost of inaction.** Buyers decide emotionally (the pain) and
   justify logically (the ROI). Your job in discovery is to make the
   status quo expensive.
3. **Always advance the deal.** Never end a call without a booked next
   step, a date, and an owner. If it is a fit, say so and ask directly.

### Open with an insight, not a pitch

Lead with a point of view that reframes how they see the problem, then earn
the discovery. Three openers you can adapt:

- Most teams don't have a software problem — they have a
  work-scattered-across-ten-tools problem. The platform is never the fix;
  the workflow is.
- The teams that get real ROI aren't the ones with the biggest budget —
  they're the ones who fixed the process before they bought the tool.
  That's the work we do.
- Everyone wants AI. The ones who win start by finding where people repeat
  the same decision fifty times a week — that's where automation pays
  back, not the shiny stuff.

### The 15 questions

Move through the four stages in order. Situation sets context (keep it
light — do your homework first), Problem surfaces dissatisfaction,
Implication makes the pain expensive, and Need-payoff gets them selling the
value back to you.

#### Situation — set the baseline

*Map how work actually flows today. Keep these light; research what you
can in advance.*

| # | Question | Listen for |
|---|---|---|
| 1 | Walk me through how this process runs today, start to finish — who and what is involved at each step? | Handoffs, manual steps, where the process actually lives. |
| 2 | Which platforms are you running now — monday.com, CRM, spreadsheets, AI tools — and how well do they talk to each other? | Tool sprawl, integration gaps, duplicated data entry. |
| 3 | How is this work measured today, and who owns the number? | No visibility, gut-feel reporting, unclear ownership. |

#### Problem — surface the dissatisfaction

*Get them naming problems out loud. Dissatisfaction is the fuel for
everything that follows.*

| # | Question | Listen for |
|---|---|---|
| 4 | Where does this process break down or slow down most often? | Bottlenecks, recurring fire-drills. |
| 5 | What is the manual work nobody on the team wants to own? | Copy-paste, chasing updates, rebuilding reports. |
| 6 | When something slips through the cracks, how does that typically happen? | No single source of truth; reliance on memory and email. |
| 7 | How much of this still runs on spreadsheets, email threads, or people just knowing? | Key-person risk, ungoverned processes. |

#### Implication — make the pain expensive

*This is where the deal is won. Don't rush it — quantify the cost of the
problem before you talk solutions.*

| # | Question | Listen for |
|---|---|---|
| 8 | When that breakdown happens, what does it actually cost — hours, missed deadlines, revenue, or clients? | Quantifiable pain you can anchor ROI to. |
| 9 | How many people spend time on work that should be automated — and what is that in salary terms? | Headcount cost, opportunity cost. |
| 10 | If nothing changes, where does this leave the team as you grow over the next 12 months? | Pain that compounds with scale. |
| 11 | What is the downstream effect — on your clients, your reporting, or leadership's visibility? | Stakes beyond the immediate team; who else is affected. |

#### Need-payoff — let them sell themselves

*Shift to the upside. Get them describing the value of a fix in their own
words — you'll quote it back later.*

| # | Question | Listen for |
|---|---|---|
| 12 | If this ran itself and gave you clean, real-time data, what would that free your team to do? | Their vision of the fix — use their words later. |
| 13 | What would it be worth to get those hours back every week? | A value figure they have now said out loud. |
| 14 | If we fixed your single biggest pain first, how would that change the business case internally? | The wedge / phase-one they will champion. |
| 15 | Who else wins when this is solved — and who needs to see it to sign off? | Decision-makers, budget owner, your internal champion. |

### Close the discovery: always advance

- Play it back. Summarise their pain and its cost in their own words before
  you propose anything.
- Confirm fit out loud: "Based on what you've told me, this is exactly
  what we fix. Want to see what that looks like for your team?"
- Lock the next step. Book the calendar before you hang up — never "I'll
  send some info." A date and an owner, or it didn't happen.
- Follow up like a pro. Most deals take five or more touches. Persistence
  is service, not pressure.

### Objection quick-turns

Stay calm, isolate the real objection, and reframe with a question. Keep
control of the conversation.

| They say | You turn it |
|---|---|
| "We can build this ourselves." | You can. But should your best people spend six months building — and then owning forever — what we have deployed 600+ times? What is their time worth against your actual roadmap? |
| "It's too expensive." | Compared to what? Put it next to the hours you just told me you lose every week. The software is not the cost — the status quo is. |
| "Now isn't the right time." | Fair — is that priority or budget? The cost you described doesn't pause while we wait. Let's at least scope it so you can decide with numbers. |

**The method in one line: Insight → Situation → Problem → Implication →
Need-payoff → Advance.**

## 8. Definition of Done (Sales)

A deal is only "done" when: work order signed via DocuSign → CRM item at
Won with accurate value and hours → Client Projects item created → DM and
IC assigned → intro email sent → kickoff booked → transcripts and SOW
accessible to the delivery team.

---

## Why this is in the harness

This is the single most directly usable source document for outbound copy
and ICP work:

- **`skills/campaign-copy/`**: the three cold-open reframes, the
  Problem/Implication question bank, and the objection quick-turns
  translate almost directly into cold email hooks, subject lines, and
  breakup-sequence steps. The house style rule (§7 — plain text, no
  markdown bold/italics, no horizontal rules in client-facing drafts)
  should carry over to generated sequence copy.
- **`skills/icp/`**: §5 (Orange Bucket) gives a second, distinct
  qualification path for warm/existing monday.com accounts vs. net-new
  cold ICP fit — worth a separate scoring path or a separate motion
  variant rather than blending the two.
- **`skills/campaign-reports/`**: §8 (Definition of Done) is the real
  downstream event outbound should ultimately be measured against — not
  just replies/opens, but leads that make it to a signed work order.
- **`AGENTS.md` §6**: confirms this repo backs the OLE CRM board referenced
  in §2, owned by the Reachly team (Thibault, Utkrusht, Thana).
