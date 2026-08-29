# Reference sources for icp/

- `knowledge/tool-docs/ai-ark.md` — the actual sourcing tool's filter
  surface should shape what the rubric scores on, not the other way
  around. `account.employeeSize`/`industries`/`naics` map to firmographic
  fit; `account.metric` (headcount growth) and `contact.experience` to
  buying-signal strength; `contact.seniority`/`departmentAndFunction` to
  champion accessibility; `account.technology` to the Orange Bucket /
  tool-sprawl check. Translating a rubric into AI Ark's actual filter JSON
  (for `pipeline/source_leads.py --filters`) is real work still to do per
  motion — see `outbound-motions/anz-work-management/research/source-register.md`.
- `knowledge/company/vision.md` — target market definition (mid-market,
  25–25,000 staff), verticals (construction, manufacturing, professional
  services, NFP, government), positioning ("process before platform").
- `knowledge/company/sales-process-sop.md` §5 (Orange Bucket) — a distinct
  qualification path for existing monday.com users vs. net-new cold ICP
  fit; likely a separate scoring path or motion variant, not a blend.
- `knowledge/company/sales-process-sop.md` (SPIN discovery guide, Situation
  stage) — the firmographic/process signals a discovery call probes for
  map directly onto candidate ICP scoring fields.

<!-- TODO(Avi): use these as source material when authoring the real ICP
     avatar + lead-fit rubric. Not yet incorporated into a rubric —
     reference only. -->
