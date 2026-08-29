---
motion: anz-work-management
status: template — no real data yet
---

# anz-work-management — Closed-won seed accounts

Seed domains for `pipeline/find_lookalikes.py`
(`knowledge/frameworks/gtm-outbound-loop.md`'s closed-won → lookalikes
loop). Max 5 domains per lookalike search call.

**No rows exist here yet.** This repo has no CRM API access — Fruition's
regional CRM boards live in monday.com and aren't queried anywhere in
this repo (see `knowledge/company/sales-process-sop.md` §2 for where
they actually live). Populate this manually from real closed-won ANZ
Work Management deals, or wait until a monday.com integration exists.
**Do not fill this with placeholder/example company names** — an empty
table accurately reflects "no real data sourced yet," which is more
useful than fabricated rows that look real.

| Company | Domain | Won date | Notes |
|---|---|---|---|
| | | | |

## Usage

```
python3 -m pipeline.find_lookalikes \
  --motion anz-work-management \
  --seed-domains "domain1.com,domain2.com,domain3.com"
```

Writes `data/anz-work-management/lookalikes/{companies.csv,filters.json}`
(gitignored) — the `filters.json` is ready to feed into
`pipeline/source_leads.py --filters` for a People Search pass against the
lookalike companies found.
