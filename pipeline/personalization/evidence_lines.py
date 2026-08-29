#!/usr/bin/env python3
"""
evidence_lines.py — generate evidence-based personalization lines (e.g.
recent hire, funding event) for each lead, sourced from the motion's
`research/` evidence catalog.

Reads `evidence.csv` from the motion's `research/` folder, matching the
schema documented in `outbound-motions/<name>/research/source-register.md`:
company, signal_type, signal_detail, source, source_url, sourced_date,
confidence. That file currently holds no real rows for any motion — see
research/source-register.md's QA checklist for why (no live sourcing
pipeline wired yet). This script is fully implemented and ready to run the
moment evidence.csv has real data; it does not fabricate a line when no
matching evidence exists for a lead (leaves personalization_line blank).
"""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path

from pipeline.clean_normalize import normalize_company_name

MAX_SIGNAL_AGE_DAYS = 90
LOW_CONFIDENCE = "low"

_TEMPLATES = {
    "hire": "Noticed {company_name} {signal_detail} recently — always a good "
            "moment to look at how project status gets tracked.",
    "job-posting": "Saw {company_name} is hiring for {signal_detail} — a role "
                   "that usually ends up owning exactly this kind of visibility problem.",
    "funding": "Congrats on {signal_detail} — worth flagging before the team "
               "scales past what a spreadsheet can track.",
    "headcount-growth": "With {signal_detail}, I'd guess project visibility is "
                         "getting harder to keep ad hoc.",
}
_DEFAULT_TEMPLATE = "Came across {signal_detail} at {company_name} — thought it was worth a note."


def _load_evidence(evidence_dir: Path) -> list[dict[str, str]]:
    evidence_path = evidence_dir / "evidence.csv"
    if not evidence_path.exists():
        return []
    with evidence_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _is_usable(evidence_row: dict[str, str]) -> bool:
    if evidence_row.get("confidence", "").strip().lower() == LOW_CONFIDENCE:
        return False
    sourced_date = evidence_row.get("sourced_date", "").strip()
    if not sourced_date:
        return False
    try:
        parsed = datetime.strptime(sourced_date, "%Y-%m-%d").date()
    except ValueError:
        return False
    return (date.today() - parsed).days <= MAX_SIGNAL_AGE_DAYS


def _best_evidence_by_company(evidence_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    """One evidence row per company: usable, then highest confidence, then most recent."""
    confidence_rank = {"high": 2, "medium": 1, "low": 0}
    best: dict[str, dict[str, str]] = {}
    for row in evidence_rows:
        if not _is_usable(row):
            continue
        key = normalize_company_name(row.get("company", ""))
        if not key:
            continue
        current = best.get(key)
        if current is None or (
            confidence_rank.get(row.get("confidence", "").lower(), 0)
            >= confidence_rank.get(current.get("confidence", "").lower(), 0)
            and row.get("sourced_date", "") >= current.get("sourced_date", "")
        ):
            best[key] = row
    return best


def render_line(evidence_row: dict[str, str]) -> str:
    template = _TEMPLATES.get(evidence_row.get("signal_type", ""), _DEFAULT_TEMPLATE)
    return template.format(
        company_name=evidence_row.get("company", ""),
        signal_detail=evidence_row.get("signal_detail", ""),
    )


def generate_evidence_lines(input_path: Path, evidence_dir: Path, output_path: Path) -> Path:
    """Generate a personalization line per lead in `input_path` using
    evidence from `evidence_dir` (a motion's `research/` folder).

    Args:
        input_path: path to the cleaned leads CSV.
        evidence_dir: path to `outbound-motions/<name>/research/`.
        output_path: path to write leads + personalization line CSV to.

    Returns:
        Path to the leads-with-personalization file written.
    """
    evidence_by_company = _best_evidence_by_company(_load_evidence(evidence_dir))

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for extra in ("personalization_line", "evidence_source", "evidence_source_url"):
            if extra not in fieldnames:
                fieldnames.append(extra)
        rows = list(reader)

    for row in rows:
        key = row.get("company_name_clean") or normalize_company_name(row.get("company_name", ""))
        evidence_row = evidence_by_company.get(key)
        if evidence_row:
            row["personalization_line"] = render_line(evidence_row)
            row["evidence_source"] = evidence_row.get("source", "")
            row["evidence_source_url"] = evidence_row.get("source_url", "")
        else:
            row.setdefault("personalization_line", "")
            row.setdefault("evidence_source", "")
            row.setdefault("evidence_source_url", "")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="cleaned leads CSV path")
    parser.add_argument("--evidence-dir", type=Path, required=True, help="motion research/ dir")
    parser.add_argument("--output", type=Path, required=True, help="output CSV path")
    args = parser.parse_args()

    generate_evidence_lines(input_path=args.input, evidence_dir=args.evidence_dir, output_path=args.output)


if __name__ == "__main__":
    main()
