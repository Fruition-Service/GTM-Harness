#!/usr/bin/env python3
"""
check_integrations.py — read-only smoke test for the Smartlead/HeyReach/
AI Ark API clients. Confirms each configured key is valid and can actually
read data (not just that the client instantiates). Makes no writes — safe
to run any time, as often as you like.

Usage (must run as a module, from the repo root, so `pipeline` resolves):
    python3 -m pipeline.check_integrations
"""
from __future__ import annotations

import os

import pipeline.integrations  # noqa: F401  (loads config/.env if present)


def check_smartlead() -> None:
    if not os.environ.get("SMARTLEAD_API_KEY"):
        print("Smartlead: SKIPPED — SMARTLEAD_API_KEY not set (see config/.env.example)")
        return
    from pipeline.integrations.smartlead_client import SmartleadClient

    try:
        campaigns = SmartleadClient().get_campaigns()
        print(f"Smartlead: OK — key valid, {len(campaigns)} campaign(s) visible")
    except Exception as e:
        print(f"Smartlead: FAILED — {e}")


def check_heyreach() -> None:
    if not os.environ.get("HEYREACH_API_KEY"):
        print("HeyReach: SKIPPED — HEYREACH_API_KEY not set (see config/.env.example)")
        return
    from pipeline.integrations.heyreach_client import HeyReachClient

    try:
        client = HeyReachClient()
        client.check_api_key()
        campaigns = client.get_campaigns()
        lists = client.get_lists()
        print(
            f"HeyReach: OK — key valid, {campaigns['totalCount']} campaign(s), "
            f"{lists.get('totalCount', '?')} list(s) visible"
        )
    except Exception as e:
        print(f"HeyReach: FAILED — {e}")


def check_ai_ark() -> None:
    if not os.environ.get("AI_ARK_API_KEY"):
        print("AI Ark: SKIPPED — AI_ARK_API_KEY not set (see config/.env.example)")
        return
    from pipeline.integrations.ai_ark_client import AIArkClient

    try:
        credits = AIArkClient().get_credit()
        print(f"AI Ark: OK — key valid, {credits.get('total', '?')} credit(s) remaining")
    except Exception as e:
        print(f"AI Ark: FAILED — {e}")


def main() -> None:
    check_smartlead()
    check_heyreach()
    check_ai_ark()


if __name__ == "__main__":
    main()
