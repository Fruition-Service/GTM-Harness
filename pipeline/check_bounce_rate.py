#!/usr/bin/env python3
"""
check_bounce_rate.py — bounce-rate safety gate for Smartlead campaigns.

Encodes a policy Thana already runs manually (per the 2026-08-30 team
call): pause a campaign if its bounce rate exceeds 2%. Uses
SmartleadClient.get_campaign_performance(), computing bounce rate as
bounced / sent — the real response only has {sent, opened, replied,
bounced}, no bounce_rate or unique_lead_count field despite what an
earlier doc-page fetch claimed (corrected in knowledge/tool-docs/smartlead.md
after testing live 2026-08-30). This is bounced-per-email-sent, not
bounced-per-unique-lead — a looser number than the "ideal" definition,
but it's what the real API actually gives us.

**Defaults to report-only.** Pausing a live campaign is a real mutation
against a real account — this script never does that unless you pass
--auto-pause explicitly. Without it, exceeding-threshold campaigns are
printed as a warning for a human to act on.
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta

from pipeline.integrations.smartlead_client import SmartleadClient

DEFAULT_THRESHOLD_PCT = 2.0


def check_bounce_rates(start_date: str, end_date: str, campaign_ids: list[int] | None = None,
                        threshold_pct: float = DEFAULT_THRESHOLD_PCT, auto_pause: bool = False) -> list[dict]:
    """Returns one dict per campaign: {campaign_id, campaign_name, sent,
    bounced, bounce_rate_pct, exceeded, paused}. `paused` is only ever
    True if `auto_pause=True` was passed explicitly. Campaigns with 0
    sends get `bounce_rate_pct: None` (not 0 — nothing to divide by)."""
    client = SmartleadClient()
    result = client.get_campaign_performance(start_date, end_date, campaign_ids=campaign_ids)
    performance = (result.get("data") or {}).get("campaign_wise_performance") or []

    rows = []
    for c in performance:
        sent = c.get("sent") or 0
        bounced = c.get("bounced") or 0
        rate = round(bounced / sent * 100, 2) if sent > 0 else None
        exceeded = rate is not None and rate > threshold_pct
        paused = False
        if exceeded and auto_pause:
            client.update_status(c["id"], "PAUSED")
            paused = True
        rows.append({
            "campaign_id": c.get("id"),
            "campaign_name": c.get("campaign_name"),
            "sent": sent,
            "bounced": bounced,
            "bounce_rate_pct": rate,
            "exceeded": exceeded,
            "paused": paused,
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-date", default=(date.today() - timedelta(days=7)).isoformat(),
                         help="YYYY-MM-DD, default: 7 days ago")
    parser.add_argument("--end-date", default=date.today().isoformat(), help="YYYY-MM-DD, default: today")
    parser.add_argument("--campaign-ids", default=None, help="comma-separated campaign IDs; default: all")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD_PCT,
                         help=f"bounce rate %% threshold, default {DEFAULT_THRESHOLD_PCT}")
    parser.add_argument("--auto-pause", action="store_true",
                         help="actually pause exceeding campaigns via the API (default: report only)")
    args = parser.parse_args()

    campaign_ids = [int(c) for c in args.campaign_ids.split(",")] if args.campaign_ids else None
    rows = check_bounce_rates(args.start_date, args.end_date, campaign_ids=campaign_ids,
                               threshold_pct=args.threshold, auto_pause=args.auto_pause)

    if not rows:
        print("No campaign performance data returned for this window.")
        return

    for row in rows:
        flag = "⚠️ EXCEEDS THRESHOLD" if row["exceeded"] else "ok"
        paused_note = " — PAUSED" if row["paused"] else ""
        rate_display = f"{row['bounce_rate_pct']}%" if row["bounce_rate_pct"] is not None else "no sends in window"
        print(f"[{row['campaign_id']}] {row['campaign_name']!r}: bounce_rate={rate_display} "
              f"(sent={row['sent']}, bounced={row['bounced']}) — {flag}{paused_note}")

    exceeded = [r for r in rows if r["exceeded"]]
    if exceeded and not args.auto_pause:
        print(f"\n{len(exceeded)} campaign(s) exceed {args.threshold}% bounce rate. "
              "Re-run with --auto-pause to pause them, or pause manually.")


if __name__ == "__main__":
    main()
