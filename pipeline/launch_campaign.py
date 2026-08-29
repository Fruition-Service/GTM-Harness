#!/usr/bin/env python3
"""
launch_campaign.py — push a prepared, deduped lead list into Smartlead or
HeyReach directly via their APIs (as opposed to `prepare_upload.py`, which
assembles a CSV for manual/bulk import).

Must run *after* `pipeline/dedup.py` — this script does not dedupe itself,
per the dedupe-on-upload directive in AGENTS.md §1.1.

Requires SMARTLEAD_API_KEY / HEYREACH_API_KEY (see config/.env.example).
See knowledge/tool-docs/smartlead.md and knowledge/tool-docs/heyreach.md
for the underlying API shapes and known gotchas — especially the HeyReach
DRAFT-campaign activation gap, which this script does not attempt to work
around (see `_ensure_heyreach_campaign_active` below).

TODO(Avi/eng): sequence content (subject/body) and sender-account rotation
are business decisions this script deliberately does not make — see the
TODOs inline. This wires the plumbing; it doesn't author the campaign.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from pipeline.integrations.heyreach_client import HeyReachClient
from pipeline.integrations.smartlead_client import SmartleadClient

SMARTLEAD_BATCH_SIZE = 400
HEYREACH_BATCH_SIZE = 100


def _batched(rows: list[dict], size: int) -> list[list[dict]]:
    return [rows[i : i + size] for i in range(0, len(rows), size)]


def _read_leads(input_path: Path) -> list[dict[str, str]]:
    with input_path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def launch_smartlead(input_path: Path, campaign_id: int | None, campaign_name: str | None) -> int:
    """Add leads from `input_path` to a Smartlead campaign, creating one
    first if `campaign_id` isn't given. Returns the campaign id used.

    Expects CSV columns matching Smartlead's lead fields where present:
    email (required), first_name, last_name, company_name, phone_number,
    website, location, linkedin_profile, company_url. Any other columns
    are passed through as custom_fields.
    """
    client = SmartleadClient()
    rows = _read_leads(input_path)

    if campaign_id is None:
        if not campaign_name:
            raise ValueError("campaign_name required when campaign_id is not given")
        campaign = client.create_campaign(name=campaign_name)
        campaign_id = campaign["id"]
        # TODO(Avi): sequence content + sender accounts are not set here —
        # call client.update_sequences() / client.add_email_accounts()
        # with real copy/senders before starting the campaign.

    known_fields = {
        "email", "first_name", "last_name", "company_name", "phone_number",
        "website", "location", "linkedin_profile", "company_url",
    }
    for batch in _batched(rows, SMARTLEAD_BATCH_SIZE):
        lead_list = []
        for row in batch:
            lead: dict[str, Any] = {k: v for k, v in row.items() if k in known_fields and v}
            custom_fields = {k: v for k, v in row.items() if k not in known_fields and v}
            if custom_fields:
                lead["custom_fields"] = custom_fields
            lead_list.append(lead)
        client.add_leads(campaign_id, lead_list)

    return campaign_id


def launch_heyreach(input_path: Path, campaign_id: int, sender_account_id: int) -> int:
    """Add leads from `input_path` to an existing, ACTIVE HeyReach
    campaign. Does not create or activate campaigns — see the DRAFT gotcha
    in knowledge/tool-docs/heyreach.md; a campaign must already be active
    (created + activated via the UI, or via `HeyReachClient.create_campaign`
    + manual activation) before this will succeed.

    Expects a `profile_url` column (required by HeyReach) plus optional
    first_name/last_name/location/company_name/position/email columns.

    TODO(Avi/eng): `sender_account_id` is a single fixed sender for the
    whole batch. Real sender rotation across a pool of LinkedIn accounts
    is a business decision — not guessed here.
    """
    client = HeyReachClient()
    rows = _read_leads(input_path)

    field_map = {
        "profile_url": "profileUrl", "first_name": "firstName", "last_name": "lastName",
        "location": "location", "company_name": "companyName", "position": "position",
        "email": "emailAddress",
    }
    for batch in _batched(rows, HEYREACH_BATCH_SIZE):
        pairs = []
        for row in batch:
            if not row.get("profile_url"):
                raise ValueError(f"row missing required profile_url: {row!r}")
            lead = {field_map[k]: v for k, v in row.items() if k in field_map and v}
            pairs.append({"linkedInAccountId": sender_account_id, "lead": lead})
        client.add_leads_to_campaign(campaign_id, pairs)

    return campaign_id


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="deduped leads CSV path")
    parser.add_argument("--target", required=True, choices=["smartlead", "heyreach"])
    parser.add_argument("--campaign-id", type=int, default=None,
                         help="existing campaign id; required for heyreach, optional for smartlead")
    parser.add_argument("--campaign-name", default=None,
                         help="smartlead only: name for a new campaign if --campaign-id is omitted")
    parser.add_argument("--heyreach-sender-account-id", type=int, default=None,
                         help="heyreach only: LinkedIn sender account id to send from")
    args = parser.parse_args()

    if args.target == "smartlead":
        campaign_id = launch_smartlead(args.input, args.campaign_id, args.campaign_name)
    else:
        if args.campaign_id is None or args.heyreach_sender_account_id is None:
            parser.error("heyreach requires --campaign-id and --heyreach-sender-account-id")
        campaign_id = launch_heyreach(args.input, args.campaign_id, args.heyreach_sender_account_id)

    print(f"pushed leads from {args.input} to {args.target} campaign {campaign_id}")


if __name__ == "__main__":
    main()
