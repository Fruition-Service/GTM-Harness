---
type: reference
source: Fruition Services — Project Delivery SOP
version: "1.0"
date: 2026-07
owner: Josh Jebathilak, Managing Director
source_systems: Company SOPs board (Sales to Delivery Process, Company Handbook), S-Project template, Collateral board, Delivery Bootcamp series (Fireflies)
---

# Fruition Services — Project Delivery SOP

Version 1.0 | July 2026 | Owner: Josh Jebathilak, Managing Director
Source systems: Company SOPs board (Sales to Delivery Process, Company
Handbook), S-Project template, Collateral board, Delivery Bootcamp series
(Fireflies)

## 1. Purpose

This SOP defines how Fruition delivers implementation projects from signed
work order through to closure and ongoing support. It applies to all
delivery staff across APAC, UK, and US, on all platforms (monday.com
primary; make.com, n8n, and integration work included).

Delivery principles:

- Always align scope before build. No full build without mock-up approval.
- Keep the client updated at every stage — no surprises.
- Document key decisions and changes on boards, not in email or Slack
  threads.
- Track time live and transparently.
- Escalate risk early. Raising a problem at 20% of hours is
  professionalism; discovering it at 90% is a crisis.

## 2. Delivery Lifecycle

**Presales → Kickoff → Discovery → Mock Up → Full Build → Testing (UAT) →
Training & Handover**

The internal project board (S-Project template) mirrors this as:
Requirements & Process Mapping → Build Solution Design → Review & Optimise
→ Automation & Integrations → Internal Training → Go Live.

### Hour-based milestones

Manage every project against utilisation checkpoints:

- **5% of hours** — handover complete (transcripts reviewed, kickoff
  booked)
- **20% of hours** — deliverables signed off by the client
- **50% of hours** — core solution complete; **notify the client of 50%
  utilisation and share the live Clockify report link**
- **80% of hours** — testing underway
- **Remaining** — end-user training, documentation, and support

## 3. Roles & Escalation

- **Sales rep** — owns scoping and handover; stays attached for expansion
  and escalation.
- **Delivery Manager / Project Lead** — owns solution design, client
  agreement, timeline, scope, and communication.
- **Implementation Consultant / technical consultants** — own the build,
  automations, and integrations.

Escalation path: mismatched expectations, scope disputes, or client
disengagement escalate first to the sales rep, then to the client's key
decision-maker. Do not be a people-pleaser — identify red flags (unclear
champion, low tech maturity, absent decision-makers, shifting priorities)
at kickoff and raise them immediately.

## 4. Stage-by-Stage Procedure

### Stage 1 — Handover (from Sales)

1. Respond promptly to the sales intro email; propose kickoff times same
   day.
2. Review all Fireflies transcripts (presales, discovery), the SOW/work
   order, and the project brief.
3. Start time tracking from the handover phase in Clockify.
4. Prepare the kickoff deck (Project Kick Off template; Advanced template
   for larger engagements).

### Stage 2 — Kickoff

1. Introduce team and roles; align on scope, timeline, deliverables, and
   success criteria.
2. Confirm communication channels and cadence (weekly check-ins as
   default).
3. Identify the champion, active users, and decision-makers — confirm who
   must attend discovery and who signs off.
4. **48-hour rule:** verify system access, account provisioning (correct
   plan/tier), and test any critical workflows at least 48 hours before
   every client meeting. A mis-provisioned account discovered mid-project
   causes expensive rework.
5. Send a post-kickoff follow-up email summarising decisions and next
   steps; schedule discovery.

### Stage 3 — Discovery & Solution Design

1. Choose the right format: high-level discovery for broad scope;
   workflow-specific sessions for complex builds. Tailor attendees
   accordingly.
2. Use the Five Ps framework (Problem, Process, People, Pain, Payoff), the
   CRM & Project / monday Service questionnaires, and process mapping
   templates.
3. Capture data structure, integration points, and reporting requirements —
   ask what the ideal dashboard looks like; that defines boards and
   fields.
4. Use Claude to draft solution designs and flowcharts from presales
   transcripts and the SOW; iterate the prompts to fill gaps before
   presenting.
5. Break the solution into concrete deliverables (forms, boards,
   dashboards, automations, integrations), distinguishing process boards
   from database/repository boards.
6. Document deliverables on the project plan and **get client sign-off on
   the approach (the 20% milestone)**. This document is the scope
   protection reference for the rest of the project.
7. Point the client at self-serve learning early (monday.com Academy, demo
   webinars, training boards) — especially for low tech-maturity teams.

### Stage 4 — Mock Up (MVP)

1. Build the initial solution/prototype with realistic dummy data so
   decision-makers can see themselves in it.
2. Review internally before any client presentation.
3. Present the MVP, gather feedback, and iterate.
4. **Obtain explicit mock-up approval before proceeding to full build.**
5. Combine MVP walkthroughs with early training touchpoints to build
   adoption momentum. Where useful, run the reverse demonstration: the
   client drives while the consultant guides.

### Stage 5 — Full Build

1. Build final workflows, boards, automations, and integrations
   iteratively with regular client feedback loops.
2. Conduct internal QA before each client review.
3. Log automations in the Automation Log; document integration
   architecture as you go.
4. Maintain live Clockify tracking and trigger the 50% utilisation
   notification.

### Stage 6 — Testing / UAT

1. Agree test users up front — champions and active users, not bystanders.
2. Build testing scenarios on a board (Testing Guide template) for larger
   projects; track user participation and feedback.
3. Run all issues and change requests through the Issue/Change Log board —
   never manage defects via email or Slack.
4. Resolve issues, confirm the solution meets the signed-off requirements,
   and confirm rollout readiness.

### Stage 7 — Training, Handover & Go-Live

1. Deliver admin training and end-user training as separate tracks
   (Account Governance/Admin training reference available).
2. Produce documentation proportionate to the engagement — Guidde for
   step-by-step playbooks, Loom for walkthroughs. Do not over-invest in
   documentation the client hasn't asked for.
3. Final walkthrough and sign-off; hand over to the client team or
   Fruition managed services.

## 5. Scope Management

Known scope-creep patterns to watch for: additional teams, workflow
extensions, feature customisation, extra reporting, new integrations,
additional training, rebuilds, third-party apps, and shifting priorities or
champions.

Controls:

- The signed-off deliverables document is the single source of truth for
  scope.
- Explicitly exclude ambiguous items (e.g. data migration responsibility)
  in writing during solution design.
- All change requests go through the change request log/form with hours
  impact assessed before commitment.
- Small goodwill items are fine; patterns of "just one more thing" get a
  scope conversation with the sales rep involved.

## 6. Closure

1. Prepare the **Project Closure Deck**: deliverables overview, team,
   benefits realised (use AI analysis of call transcripts to articulate
   benefits), go-live readiness, roadblocks resolved, and the Clockify
   report (hours utilised vs allocated).
2. Present **Phase 2 recommendations** — additional workflows,
   integrations, or optimisations identified during delivery.
3. Define support channels clearly: monday.com support for platform bugs;
   Fruition for custom work.
4. Offer **managed services**: 5–10 hours/month maintenance packages.
   Standard rollout-insurance offer: 10 hrs/month for 3 months then 5
   hrs/month for 3 months; 6-month commitment earns a 10% discount with
   unused hours carried forward. Invoicing: monthly invoices for $2,000+
   arrangements, block-hour packages below that.
5. Collect feedback in priority order: **case study first** (most
   valuable — $200 USD contributor bonus), then Google review, then CSAT.
   Do not request public feedback on a project that didn't go well.
6. Complete the CRM/Salesforce project closure with required fields, file
   uploads, and CSAT survey. Close the project item on the Fruition
   Projects board.

## 7. Professional Standards (Company Handbook)

- **Response times:** meet the handbook's internal and external
  response-time protocols; acknowledge client messages promptly even if
  the full answer comes later.
- **Leave:** schedule planned leave with project coverage arranged in
  advance; follow the unplanned-leave notification process so no client is
  left waiting.
- **Time tracking:** live and accurate in Clockify, always. Utilisation
  reporting and the weekly project-hours report (over-scope and within-25%
  flags by region) depend on it.
- **Risk:** escalate early — clients must never be surprised by a problem
  we saw coming.
- **Quality:** internal review before anything reaches a client; test
  workflows before demos.
- The handbook's twelve team commitments apply to all delivery work.

## 8. Delivery KPIs

Tracked live on the Fruition Projects board and reviewed at team huddles:

- Projects completed and completion rate
- Client health scores (positive health %)
- Hour utilisation vs scope (flagged weekly: over-hours and within 25% of
  over)
- CSAT, case studies, and Google reviews generated

## 9. Collateral Index (Delivery)

Kickoff decks (standard + advanced) · Discovery questionnaires (CRM &
Project, monday Service) · Process Mapping deck · Implementation stacks
(Basic + Advanced project plan apps) · Training boards & bootcamp decks ·
Testing Guide board · Issue/Change Log board · Guidde playbooks · Admin
Access Guide · Sample handover documentation (monday Docs) · Project
Closure Deck · Closing-up email with support offer · Case Study form ·
Google review link. All live on the Collateral board, tagged by phase.

---

## Why this is in the harness

This is downstream of outbound — it's what a lead becomes after the sales
SOP's "Definition of Done" — but it's still relevant reference material:

- **`skills/campaign-reports/`**: §8 (Delivery KPIs) is the ultimate metric
  outbound quality is judged against (utilisation, CSAT, case studies), not
  just reply/open rates. Useful context when framing what a "good" outbound
  motion looks like beyond top-of-funnel numbers.
- **`skills/campaign-copy/`**: the managed-services offer (§6.4 — 10
  hrs/month rollout insurance) and the "600+ deployments" / case-study
  proof points referenced in the sales SOP originate from this delivery
  motion — good source material for later-sequence proof points.
- **`AGENTS.md` §6**: general company-process context for any agent
  reasoning about what happens after a motion's leads convert.
