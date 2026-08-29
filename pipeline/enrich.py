#!/usr/bin/env python3
"""
enrich.py — email finding and firmographic enrichment for a raw lead file.

When `AI_ARK_API_KEY` is set, rows with an `ai_ark_id` (from
`pipeline/source_leads.py`'s live-sourcing path) or a `linkedin_profile`
but no `email` get a real, verified email via AI Ark's single-person
export (`pipeline/integrations/ai_ark_client.py`, schema in
`knowledge/tool-docs/ai-ark.md`) — 1 credit per email found, 0 otherwise.
This calls the API once per row (rate-limited to stay under 5 req/s); for
very large batches, AI Ark's bulk async export
(`AIArkClient.export_people_with_email()`) would be more efficient — not
wired up here, since this pipeline processes files synchronously and that
endpoint is async/webhook-based.

Everything else — deriving a likely company website from a non-freemail
email domain, flagging what still needs a provider — runs regardless of
whether AI Ark is configured, as a local fallback.
"""
from __future__ import annotations

import argparse
import csv
import os
import time
from pathlib import Path

# Not an exhaustive list — good enough to avoid deriving a "company
# website" from a personal email address.
_FREEMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
    "aol.com", "protonmail.com", "live.com", "msn.com",
}

REQUIRED_FOR_ENRICHED = ("email", "company_name", "website", "linkedin_profile")


def _domain_from_email(email: str) -> str:
    return email.rsplit("@", 1)[-1].strip().lower() if "@" in email else ""


def _find_email_via_ai_ark(row: dict[str, str], client) -> dict[str, str]:
    """Mutates and returns `row` with `email` filled in if AI Ark finds
    one. Leaves `email` blank (not an error) on a 404 "no email found"."""
    import requests

    person_id = row.get("ai_ark_id") or None
    url = None if person_id else (row.get("linkedin_profile") or None)
    if not person_id and not url:
        return row
    try:
        result = client.export_single_person(person_id=person_id, url=url)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            return row  # "no email found" — a real, expected outcome, not an error
        raise
    outputs = ((result or {}).get("email") or {}).get("output") or []
    valid = [o for o in outputs if o.get("status") == "VALID" and o.get("address")]
    if valid:
        row["email"] = valid[0]["address"]
    elif outputs:
        row["email"] = outputs[0].get("address", "")  # best available, even if unverified
    return row


def enrich_row(row: dict[str, str]) -> dict[str, str]:
    row = dict(row)
    email = row.get("email", "")
    domain = _domain_from_email(email)

    if not row.get("website") and domain and domain not in _FREEMAIL_DOMAINS:
        row["website"] = f"https://{domain}"

    missing = [field for field in REQUIRED_FOR_ENRICHED if not row.get(field)]
    row["enrichment_status"] = "needs_provider:" + ",".join(missing) if missing else "complete"
    return row


def enrich(input_path: Path, output_path: Path) -> Path:
    """Enrich `input_path` (raw leads CSV) — real email-finding via AI Ark
    when configured, local best-effort derivation otherwise — and flag
    what still needs a real provider.

    Args:
        input_path: path to raw leads CSV (under gitignored `data/`).
        output_path: path to write the enriched CSV to.

    Returns:
        Path to the enriched leads file written.
    """
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if os.environ.get("AI_ARK_API_KEY"):
        from pipeline.integrations.ai_ark_client import AIArkClient

        client = AIArkClient()
        for row in rows:
            if not row.get("email") and (row.get("ai_ark_id") or row.get("linkedin_profile")):
                _find_email_via_ai_ark(row, client)
                time.sleep(0.25)  # stay under AI Ark's 5 req/s rate limit with margin

    rows = [enrich_row(row) for row in rows]

    # enrich_row() can add fields (website, enrichment_status) that weren't
    # in the original header — collect every key actually present so the
    # writer never chokes on a row with a field it doesn't know about.
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    incomplete = sum(1 for r in rows if r["enrichment_status"] != "complete")
    if incomplete:
        print(f"enrich: {incomplete}/{len(rows)} row(s) still need a real enrichment provider")

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="raw leads CSV path")
    parser.add_argument("--output", type=Path, required=True, help="enriched leads CSV path")
    args = parser.parse_args()

    enrich(input_path=args.input, output_path=args.output)


if __name__ == "__main__":
    main()
