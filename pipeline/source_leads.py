#!/usr/bin/env python3
"""
source_leads.py — get raw leads for a motion, ready for pipeline/enrich.py.

Two paths:

1. **Live AI Ark sourcing** (used when `AI_ARK_API_KEY` is set *and*
   `--filters` is given): calls AI Ark's People Search
   (`pipeline/integrations/ai_ark_client.py`, schema in
   `knowledge/tool-docs/ai-ark.md`) and writes the matches — no email yet,
   that's `enrich.py`'s job (AI Ark's search endpoints don't return email;
   only its export endpoints do, and those cost credits per email found).
   `--filters` must be a JSON file with AI Ark's `account`/`contact`
   filter syntax — translating a motion's `icp/lead-fit-rubric.md` into
   that filter JSON is a human/skill judgment call
   (`skills/icp/instructions.md` §5), not something this script derives
   on its own.

2. **File-import fallback** (used otherwise): consolidates whatever CSV
   exports have been manually dropped into `data/<motion>/imports/`. This
   was the only path before AI Ark was wired up and remains useful for
   one-off manual pulls or other sourcing tools.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path
from typing import Any

RAW_FIELDNAMES = [
    "ai_ark_id", "first_name", "last_name", "email", "company_name",
    "title", "seniority", "department", "linkedin_profile", "location",
]


def _person_to_row(person: dict[str, Any]) -> dict[str, str]:
    profile = person.get("profile", {}) or {}
    company = person.get("company", {}) or {}
    department = person.get("department", {}) or {}
    link = person.get("link", {}) or {}
    location = person.get("location", {}) or {}
    return {
        "ai_ark_id": person.get("id", ""),
        "first_name": profile.get("first_name", ""),
        "last_name": profile.get("last_name", ""),
        "email": "",  # AI Ark search doesn't return email — see enrich.py
        "company_name": (company.get("summary", {}) or {}).get("name", ""),
        "title": profile.get("title", ""),
        "seniority": department.get("seniority", ""),
        "department": ",".join(department.get("departments", []) or []),
        "linkedin_profile": link.get("linkedin", ""),
        "location": location.get("default", ""),
    }


def source_leads_via_ai_ark(motion: str, out_dir: Path, filters: dict[str, Any],
                             target_size: int = 200) -> Path:
    """Source leads for `motion` live via AI Ark People Search.

    Args:
        motion: motion slug, e.g. "anz-work-management".
        out_dir: base output directory (expected under gitignored `data/`).
        filters: {"account": {...}, "contact": {...}} in AI Ark's filter
            syntax — see knowledge/tool-docs/ai-ark.md.
        target_size: total leads to fetch (paginated 100/page, AI Ark's max
            page size for search).

    Returns:
        Path to the raw leads file written.
    """
    from pipeline.integrations.ai_ark_client import AIArkClient

    client = AIArkClient()
    page_size = 100
    rows: list[dict[str, str]] = []
    page = 0
    while len(rows) < target_size:
        result = client.search_people(
            page=page, size=min(page_size, target_size - len(rows)),
            account=filters.get("account"), contact=filters.get("contact"),
        )
        content = result.get("content", [])
        if not content:
            break
        rows.extend(_person_to_row(p) for p in content)
        if page >= result.get("totalPages", 1) - 1:
            break
        page += 1
        time.sleep(0.25)  # stay under the 5 req/s rate limit with margin

    out_path = out_dir / motion / "raw" / "leads.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RAW_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"source_leads: sourced {len(rows)} lead(s) from AI Ark (no email yet — run enrich.py next)")
    return out_path


def source_leads_from_files(motion: str, out_dir: Path, import_dir: Path | None = None) -> Path:
    """Consolidate raw lead exports for `motion` into a single raw CSV.

    Args:
        motion: motion slug, e.g. "anz-work-management".
        out_dir: base output directory (expected under gitignored `data/`).
        import_dir: where to read source CSVs from. Defaults to
            `out_dir/<motion>/imports/` — drop manual AI Ark/Clay exports
            there before running this.

    Returns:
        Path to the raw leads file written (`out_dir/<motion>/raw/leads.csv`).
    """
    import_dir = import_dir or (out_dir / motion / "imports")
    if not import_dir.exists():
        raise FileNotFoundError(
            f"{import_dir} does not exist. Drop AI Ark/Clay CSV exports there before "
            "running source_leads.py, or set AI_ARK_API_KEY and pass --filters to source "
            "live instead (see knowledge/tool-docs/ai-ark.md)."
        )

    csv_files = sorted(import_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"no .csv files found in {import_dir}")

    fieldnames: list[str] = []
    all_rows: list[dict[str, str]] = []
    for csv_file in csv_files:
        with csv_file.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for name in reader.fieldnames or []:
                if name not in fieldnames:
                    fieldnames.append(name)
            all_rows.extend(reader)

    out_path = out_dir / motion / "raw" / "leads.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"source_leads: consolidated {len(all_rows)} row(s) from {len(csv_files)} file(s)")
    return out_path


def source_leads(motion: str, out_dir: Path, import_dir: Path | None = None,
                  filters: dict[str, Any] | None = None, target_size: int = 200) -> Path:
    """Dispatches to the AI Ark path if `filters` is given and
    `AI_ARK_API_KEY` is set, otherwise the file-import fallback. See the
    module docstring for why both paths exist.
    """
    if filters is not None and os.environ.get("AI_ARK_API_KEY"):
        return source_leads_via_ai_ark(motion, out_dir, filters, target_size)
    return source_leads_from_files(motion, out_dir, import_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--motion", required=True, help="motion slug, e.g. anz-work-management")
    parser.add_argument("--out-dir", type=Path, default=Path("data"), help="output directory (gitignored)")
    parser.add_argument("--import-dir", type=Path, default=None,
                         help="override the default data/<motion>/imports/ source directory (file-import path)")
    parser.add_argument("--filters", type=Path, default=None,
                         help="JSON file with AI Ark {account, contact} filters (live-sourcing path)")
    parser.add_argument("--target-size", type=int, default=200,
                         help="how many leads to fetch (live-sourcing path only)")
    args = parser.parse_args()

    filters = json.loads(args.filters.read_text()) if args.filters else None
    source_leads(motion=args.motion, out_dir=args.out_dir, import_dir=args.import_dir,
                 filters=filters, target_size=args.target_size)


if __name__ == "__main__":
    main()
