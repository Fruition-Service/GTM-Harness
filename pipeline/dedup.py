#!/usr/bin/env python3
"""
dedup.py — cross-campaign / cross-workspace dedupe.

Hard directive: **dedupe-on-upload, always**. No lead may enter a sequencer
twice across campaigns or workspaces (AGENTS.md §1.1). This script is the
enforcement point: it reads `outbound-motions/_LEDGER.md` to resolve which
dedupe pool a motion belongs to, then filters the incoming lead list
against a persistent local "already contacted" record for that pool —
leads that pass are appended to that record, so the next run (from this
motion or any other sharing the pool) won't re-contact them.

The contacted-record store is a local CSV under gitignored `data/` — not a
live Smartlead/HeyReach API check. That's a deliberate, documented
limitation: neither client currently exposes a fast "has this email been
contacted anywhere in the account" lookup (Smartlead's is scoped per
campaign, HeyReach's per campaign too) — see
knowledge/tool-docs/{smartlead,heyreach}.md. If this local store and the
platforms drift (e.g. someone uploads a CSV manually, bypassing this
script), that's a process gap to close, not something this script can
detect on its own.
"""
from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "outbound-motions" / "_LEDGER.md"
CONTACTED_STORE_DIR = REPO_ROOT / "data" / "dedupe"  # gitignored


def get_dedupe_pool(motion: str, ledger_path: Path = LEDGER_PATH) -> str:
    """Parse `_LEDGER.md`'s markdown table and return the `dedupe_pool`
    value for `motion`."""
    if not ledger_path.exists():
        raise FileNotFoundError(f"ledger not found at {ledger_path!r}")

    header_cols: list[str] | None = None
    for line in ledger_path.read_text().splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header_cols is None:
            if cells and cells[0].lower() == "motion":
                header_cols = [c.lower() for c in cells]
            continue
        if set(cells) == {"---"} or all(re.fullmatch(r"-+", c) for c in cells):
            continue  # markdown table separator row
        row_motion = cells[0].strip("`")
        if row_motion == motion:
            row = dict(zip(header_cols, cells))
            pool = row.get("dedupe_pool", "").strip("`")
            if not pool:
                raise ValueError(f"motion {motion!r} has no dedupe_pool set in {ledger_path!r}")
            return pool

    raise ValueError(f"motion {motion!r} not found in {ledger_path!r}")


def _contacted_store_path(pool: str) -> Path:
    return CONTACTED_STORE_DIR / f"{pool}.csv"


def load_contacted(pool: str) -> set[str]:
    path = _contacted_store_path(pool)
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as f:
        return {row["email"].strip().lower() for row in csv.DictReader(f) if row.get("email")}


def append_contacted(pool: str, emails: list[str], motion: str) -> None:
    path = _contacted_store_path(pool)
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "motion", "contacted_at"])
        if is_new:
            writer.writeheader()
        now = datetime.now(timezone.utc).isoformat()
        for email in emails:
            writer.writerow({"email": email, "motion": motion, "contacted_at": now})


def dedup(input_path: Path, output_path: Path, motion: str) -> Path:
    """Filter `input_path` against the dedupe pool for `motion` and write the
    deduped result to `output_path`. Leads that pass are recorded as
    contacted for future runs.

    Args:
        input_path: path to the cleaned/segmented leads CSV ready for upload.
        output_path: path to write the deduped CSV to.
        motion: motion slug used to resolve the shared dedupe pool via
            `_LEDGER.md`.

    Returns:
        Path to the deduped leads file written.
    """
    pool = get_dedupe_pool(motion)
    contacted = load_contacted(pool)

    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    seen_in_batch: set[str] = set()
    kept: list[dict[str, str]] = []
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if not email or email in contacted or email in seen_in_batch:
            continue
        seen_in_batch.add(email)
        kept.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept)

    append_contacted(pool, [row["email"].strip().lower() for row in kept], motion)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="leads CSV path, pre-dedupe")
    parser.add_argument("--output", type=Path, required=True, help="deduped leads CSV path")
    parser.add_argument("--motion", required=True, help="motion slug, e.g. anz-work-management")
    args = parser.parse_args()

    result_path = dedup(input_path=args.input, output_path=args.output, motion=args.motion)
    print(f"deduped leads written to {result_path}")


if __name__ == "__main__":
    main()
