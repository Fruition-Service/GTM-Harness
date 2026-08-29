#!/usr/bin/env python3
"""
find_lookalikes.py — closes the GTM loop's "closed-won → lookalikes"
feedback path (knowledge/frameworks/gtm-outbound-loop.md).

Takes a small list of seed domains (closed-won accounts, or any accounts
that are a strong ICP fit) and uses AI Ark's lookalike company search
(`AIArkClient.search_companies(lookalike_domains=...)`, max 5 seeds per
call) to find similar companies. Writes:

1. A companies CSV, for human review.
2. A filters JSON in the shape `pipeline/source_leads.py --filters`
   expects, so the lookalike companies' domains can feed straight into a
   normal People Search pass — lookalike-sourced leads still go through
   the same ICP scoring as anything else (see
   knowledge/frameworks/gtm-outbound-loop.md — this is a sourcing signal,
   not a qualification shortcut).

Requires AI_ARK_API_KEY. Read-only against AI Ark (a search call), but
each call is credit-metered like any AI Ark search — check
`AIArkClient.get_credit()` / `pipeline/check_integrations.py` first if
credit budget matters.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from pipeline.integrations.ai_ark_client import AIArkClient

MAX_SEED_DOMAINS = 5


def find_lookalikes(seed_domains: list[str], size: int = 50) -> list[dict[str, Any]]:
    """Returns the raw AI Ark company results for the given seed domains."""
    if not seed_domains:
        raise ValueError("find_lookalikes requires at least one seed domain")
    if len(seed_domains) > MAX_SEED_DOMAINS:
        raise ValueError(f"AI Ark accepts at most {MAX_SEED_DOMAINS} seed domains per call")

    client = AIArkClient()
    result = client.search_companies(page=0, size=size, lookalike_domains=seed_domains)
    return result.get("content", [])


def write_lookalike_outputs(companies: list[dict[str, Any]], motion: str, out_dir: Path) -> tuple[Path, Path]:
    """Writes a companies CSV (for review) and a filters.json
    (`pipeline/source_leads.py --filters`-ready) from lookalike results.

    Returns:
        (companies_csv_path, filters_json_path)
    """
    out_base = out_dir / motion / "lookalikes"
    out_base.mkdir(parents=True, exist_ok=True)

    companies_path = out_base / "companies.csv"
    fieldnames = ["name", "domain", "linkedin", "industry", "employee_size", "location"]
    domains: list[str] = []
    with companies_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies:
            summary = company.get("summary", {}) or {}
            link = company.get("link", {}) or {}
            location = company.get("location", {}) or {}
            headquarter = (location.get("headquarter") or {}) if isinstance(location, dict) else {}
            domain = link.get("domain", "")
            if domain:
                domains.append(domain)
            writer.writerow({
                "name": summary.get("name", ""),
                "domain": domain,
                "linkedin": link.get("linkedin", ""),
                "industry": summary.get("industry", ""),
                "employee_size": summary.get("staff", ""),
                "location": headquarter.get("city", "") if isinstance(headquarter, dict) else "",
            })

    filters_path = out_base / "filters.json"
    filters = {"account": {"domain": {"any": {"include": domains}}}}
    filters_path.write_text(json.dumps(filters, indent=2))

    print(f"find_lookalikes: found {len(companies)} companies ({len(domains)} with a usable domain)")
    print(f"  → {companies_path}")
    print(f"  → {filters_path}  (feed to: python3 -m pipeline.source_leads --motion {motion} --filters {filters_path})")
    return companies_path, filters_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--motion", required=True, help="motion slug, e.g. anz-work-management")
    parser.add_argument("--seed-domains", required=True,
                         help=f"comma-separated seed domains (max {MAX_SEED_DOMAINS}), e.g. closed-won accounts")
    parser.add_argument("--size", type=int, default=50, help="how many lookalike companies to fetch")
    parser.add_argument("--out-dir", type=Path, default=Path("data"), help="output directory (gitignored)")
    args = parser.parse_args()

    seed_domains = [d.strip() for d in args.seed_domains.split(",") if d.strip()]
    companies = find_lookalikes(seed_domains, size=args.size)
    write_lookalike_outputs(companies, motion=args.motion, out_dir=args.out_dir)


if __name__ == "__main__":
    main()
