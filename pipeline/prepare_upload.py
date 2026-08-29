#!/usr/bin/env python3
"""
prepare_upload.py — assemble the final sequencer-ready CSV (Smartlead /
HeyReach column format) from the deduped, personalized lead list, for
manual/bulk CSV import. For pushing leads directly via API instead, see
`pipeline/launch_campaign.py` (uses `pipeline/integrations/`).

This is the last step before launch: it must run *after* `dedup.py` so the
dedupe-on-upload directive holds. Do not call this directly on a
pre-dedupe file.

Column names below match each platform's documented API field names
(knowledge/tool-docs/smartlead.md, heyreach.md) rather than a verified
bulk-CSV-import screen — this repo's research covered the APIs, not the
manual upload UI. Both platforms' import UIs let you map CSV columns to
fields by hand, so this should work as-is, but confirm against the actual
upload screen before assuming a fixed header contract.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

# CSV column (from the cleaned/personalized input) -> platform field name
_SMARTLEAD_FIELDS = {
    "email": "email",
    "first_name": "first_name",
    "last_name": "last_name",
    "company_name": "company_name",
    "phone_number": "phone_number",
    "website": "website",
    "location": "location",
    "linkedin_profile": "linkedin_profile",
    "company_url": "company_url",
}
_SMARTLEAD_REQUIRED = {"email"}

_HEYREACH_FIELDS = {
    "linkedin_profile": "profileUrl",
    "first_name": "firstName",
    "last_name": "lastName",
    "location": "location",
    "company_name": "companyName",
    "email": "emailAddress",
}
_HEYREACH_REQUIRED = {"linkedin_profile"}

_TARGET_FIELDS = {"smartlead": _SMARTLEAD_FIELDS, "heyreach": _HEYREACH_FIELDS}
_TARGET_REQUIRED = {"smartlead": _SMARTLEAD_REQUIRED, "heyreach": _HEYREACH_REQUIRED}


def prepare_upload(input_path: Path, output_path: Path, target: str) -> Path:
    """Assemble a sequencer-ready CSV from a deduped lead list.

    Rows missing the target platform's required field (email for
    Smartlead, linkedin_profile for HeyReach) are skipped, not silently
    included with a blank required field — that would just fail on
    upload, or worse, upload with a missing key identifier.

    Args:
        input_path: path to the deduped, personalized leads CSV.
        output_path: path to write the sequencer-ready CSV to.
        target: destination sequencer, one of "smartlead" | "heyreach".

    Returns:
        Path to the sequencer-ready CSV file written.
    """
    if target not in _TARGET_FIELDS:
        raise ValueError(f"unknown target {target!r}, expected 'smartlead' or 'heyreach'")

    field_map = _TARGET_FIELDS[target]
    required = _TARGET_REQUIRED[target]

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        source_fields = set(reader.fieldnames or [])
        active_map = {src: dst for src, dst in field_map.items() if src in source_fields}
        # personalization_line, if present, always carries through as the merge field
        if "personalization_line" in source_fields:
            active_map["personalization_line"] = "personalization_line"

        output_fields = list(dict.fromkeys(active_map.values()))
        skipped = 0
        rows_out = []
        for row in reader:
            if any(not row.get(req) for req in required):
                skipped += 1
                continue
            rows_out.append({dst: row.get(src, "") for src, dst in active_map.items()})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows_out)

    if skipped:
        print(f"prepare_upload: skipped {skipped} row(s) missing a required field for {target!r}")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="deduped leads CSV path")
    parser.add_argument("--output", type=Path, required=True, help="sequencer-ready CSV path")
    parser.add_argument("--target", required=True, choices=["smartlead", "heyreach"])
    args = parser.parse_args()

    result_path = prepare_upload(input_path=args.input, output_path=args.output, target=args.target)
    print(f"upload-ready CSV written to {result_path}")


if __name__ == "__main__":
    main()
