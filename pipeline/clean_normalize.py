#!/usr/bin/env python3
"""
clean_normalize.py — company-name cleaning and field normalization/formatting
for an enriched lead file, ahead of dedupe and segmentation.

Pure string/data cleaning — no external API involved, so unlike
source_leads.py/enrich.py this is fully implemented, not a stub.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

# Legal-entity suffixes stripped for a normalized company_name_clean field
# (kept for fuzzy matching in dedup.py; the original company_name is
# preserved untouched for display/personalization).
_LEGAL_SUFFIXES = [
    r"\bpty\.?\s*ltd\.?\b", r"\bpty\b", r"\bltd\.?\b", r"\bllc\b",
    r"\binc\.?\b", r"\bcorp\.?\b", r"\bco\.?\b", r"\bplc\b", r"\bllp\b",
    r"\bgmbh\b", r"\bpvt\.?\s*ltd\.?\b",
]
_SUFFIX_RE = re.compile("|".join(_LEGAL_SUFFIXES), re.IGNORECASE)
_WHITESPACE_RE = re.compile(r"\s+")


def normalize_company_name(name: str) -> str:
    """Strip legal suffixes and collapse whitespace, for fuzzy matching —
    not for display (use the original company_name field for that)."""
    stripped = _SUFFIX_RE.sub("", name)
    stripped = re.sub(r"[^\w\s&-]", "", stripped)
    return _WHITESPACE_RE.sub(" ", stripped).strip().lower()


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_phone(phone: str) -> str:
    """Keep a leading + (international prefix), strip everything else
    non-numeric. Does not assume a specific country format."""
    if not phone:
        return ""
    has_plus = phone.strip().startswith("+")
    digits = re.sub(r"\D", "", phone)
    return f"+{digits}" if has_plus and digits else digits


def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = f"https://{url}"
    return url.rstrip("/").lower()


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    row = dict(row)
    if row.get("email"):
        row["email"] = normalize_email(row["email"])
    if row.get("company_name"):
        row["company_name"] = _WHITESPACE_RE.sub(" ", row["company_name"]).strip()
        row["company_name_clean"] = normalize_company_name(row["company_name"])
    if row.get("phone_number"):
        row["phone_number"] = normalize_phone(row["phone_number"])
    for url_field in ("website", "company_url", "linkedin_profile"):
        if row.get(url_field):
            row[url_field] = normalize_url(row[url_field])
    for name_field in ("first_name", "last_name"):
        if row.get(name_field):
            row[name_field] = _WHITESPACE_RE.sub(" ", row[name_field]).strip().title()
    return row


def clean_normalize(input_path: Path, output_path: Path) -> Path:
    """Clean and normalize `input_path` (enriched leads CSV).

    Args:
        input_path: path to enriched leads CSV (under gitignored `data/`).
        output_path: path to write the cleaned/normalized CSV to.

    Returns:
        Path to the cleaned leads file written.
    """
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        if "company_name_clean" not in fieldnames and "company_name" in fieldnames:
            fieldnames.append("company_name_clean")
        rows = [normalize_row(row) for row in reader]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="enriched leads CSV path")
    parser.add_argument("--output", type=Path, required=True, help="cleaned leads CSV path")
    args = parser.parse_args()

    clean_normalize(input_path=args.input, output_path=args.output)


if __name__ == "__main__":
    main()
