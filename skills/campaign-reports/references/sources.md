# Reference sources for campaign-reports/

- `reports/2026-08-14-heyreach-linkedin-performance-snapshot.md` and
  `outbound-motions/anz-work-management/reporting/2026-08-14-weekly-report.md`
  — first real reports produced against this skill's template
  (`instructions.md` §2), using `HeyReachClient.get_overall_stats()`.
  Worth reading before authoring v2 of this skill: they surface a real
  gap (no join to meeting-booked/won data) that the template should
  address, not just replicate.
- `knowledge/company/sales-process-sop.md` §8 (Definition of Done — Sales)
  — the real handoff point from outbound to sales (work order signed → CRM
  Won → kickoff booked). Outbound reporting should ideally track leads
  through to this point, not just replies/opens.
- `knowledge/company/delivery-sop.md` §8 (Delivery KPIs) — for context on
  the downstream metrics (utilisation, CSAT, case studies) that outbound
  quality is ultimately judged against.

- `knowledge/tool-docs/smartlead.md` — the sentiment-tagging webhook is now
  documented in full (`POST /webhook/create`, event types, lead
  categorization endpoints) and wired in `SmartleadClient`. What's left is
  the Make.com/n8n routing logic and mapping Smartlead's category IDs to
  the three controlled tags (information-request / book-meeting / positive).

<!-- TODO(Avi): use these when authoring the real report template and
     metrics, and when wiring the Smartlead sentiment-tagging quick win.
     Not yet incorporated — reference only. -->
