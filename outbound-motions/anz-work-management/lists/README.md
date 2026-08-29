# lists/ — anz-work-management

Segmented lead buckets, output of `skills/list-segmentation/` scoring the
cleaned+enriched lead list (from `pipeline/`) against
`icp/lead-fit-rubric.md`.

## Expected files once the pipeline runs

Per `skills/list-segmentation/instructions.md` §5:

- `tier-a.csv` — score 80-100, multi-persona treatment
- `tier-b.csv` — score 60-79, standard sequence
- `tier-c.csv` — score 40-59, lighter-touch/later batch
- `orange-bucket.csv` — existing monday.com accounts, routed via the
  7-question script instead of the numeric rubric
- `excluded.csv` — score <40, log only, never uploaded

Each row: `email, first_name, last_name, company_name, icp_score, segment,
role, vertical` at minimum.

**None of these files exist yet** — `pipeline/source_leads.py` has no live
data source wired (see `research/source-register.md`), so there's no real
lead list to segment. This README describes the target shape, not current
contents. Do not create these files with placeholder/example rows — an
empty `lists/` folder accurately reflects "pipeline not yet run," which is
more useful than fabricated data that looks real.
