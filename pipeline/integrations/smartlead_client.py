"""Smartlead API client.

Thin wrapper around the endpoints documented in
`knowledge/tool-docs/smartlead.md` — auth, request/response shapes, and
gotchas are explained there, not repeated here.

Usage:
    from pipeline.integrations.smartlead_client import SmartleadClient
    client = SmartleadClient()  # reads SMARTLEAD_API_KEY from the environment
    campaign = client.create_campaign(name="Q1 2026 ANZ Work Mgmt")
"""
from __future__ import annotations

import os
from typing import Any, Literal

from pipeline.integrations._http import request_with_backoff

BASE_URL = "https://server.smartlead.ai/api/v1"

CampaignStatus = Literal["START", "PAUSED", "STOPPED"]


class SmartleadClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL) -> None:
        self.api_key = api_key or os.environ.get("SMARTLEAD_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "SMARTLEAD_API_KEY not set. Copy config/.env.example to config/.env "
                "and fill it in, or export it via GitHub Secrets/Doppler in CI."
            )
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None,
                 json_body: dict[str, Any] | None = None) -> Any:
        params = {**(params or {}), "api_key": self.api_key}
        response = request_with_backoff(
            method, f"{self.base_url}{path}", params=params, json=json_body
        )
        response.raise_for_status()
        return response.json()

    # --- campaigns ---------------------------------------------------

    def get_campaigns(self, client_id: int | None = None, include_tags: bool = False) -> list[dict]:
        params: dict[str, Any] = {"include_tags": include_tags}
        if client_id is not None:
            params["client_id"] = client_id
        return self._request("GET", "/campaigns/", params=params)

    def get_campaign(self, campaign_id: int) -> dict:
        return self._request("GET", f"/campaigns/{campaign_id}")

    def get_campaign_performance(self, start_date: str, end_date: str,
                                  campaign_ids: list[int] | None = None,
                                  client_ids: list[int] | None = None) -> dict:
        """Per-campaign performance. `start_date`/`end_date` required,
        format YYYY-MM-DD. Confirmed live 2026-08-30: each item in
        `data.campaign_wise_performance` only has {id, campaign_name,
        sent, opened, replied, bounced} — no bounce_rate/reply_rate/
        unique_lead_count fields, despite what an earlier doc-page fetch
        claimed. Compute rates yourself from sent/bounced/replied — see
        knowledge/tool-docs/smartlead.md and pipeline/check_bounce_rate.py."""
        params: dict[str, Any] = {"start_date": start_date, "end_date": end_date}
        if campaign_ids is not None:
            params["campaign_ids"] = ",".join(str(c) for c in campaign_ids)
        if client_ids is not None:
            params["client_ids"] = ",".join(str(c) for c in client_ids)
        return self._request("GET", "/analytics/campaign/overall-stats", params=params)

    def create_campaign(self, name: str, client_id: int | None = None) -> dict:
        body: dict[str, Any] = {"name": name}
        if client_id is not None:
            body["client_id"] = client_id
        return self._request("POST", "/campaigns/create", json_body=body)

    def update_status(self, campaign_id: int, status: CampaignStatus) -> dict:
        return self._request(
            "POST", f"/campaigns/{campaign_id}/status", json_body={"status": status}
        )

    def update_sequences(self, campaign_id: int, sequences: list[dict]) -> dict:
        """`sequences` items: {id, seq_number, subject, email_body, seq_delay_details}.
        See knowledge/tool-docs/smartlead.md — cannot edit while campaign is ACTIVE.
        """
        return self._request(
            "POST", f"/campaigns/{campaign_id}/sequences", json_body={"sequences": sequences}
        )

    def add_email_accounts(self, campaign_id: int, email_account_ids: list[int]) -> dict:
        return self._request(
            "POST", f"/campaigns/{campaign_id}/email-accounts",
            json_body={"email_account_ids": email_account_ids},
        )

    def add_leads(self, campaign_id: int, lead_list: list[dict],
                   settings: dict[str, Any] | None = None) -> dict:
        """`lead_list` max 400 per call; each item needs at least `email`.
        Default settings keep dedupe-on-upload behavior — see
        knowledge/tool-docs/smartlead.md before overriding `settings`.
        """
        if len(lead_list) > 400:
            raise ValueError("Smartlead accepts at most 400 leads per add_leads() call")
        body: dict[str, Any] = {"lead_list": lead_list}
        if settings is not None:
            body["settings"] = settings
        return self._request("POST", f"/campaigns/{campaign_id}/leads", json_body=body)

    # --- webhooks / sentiment tagging (AGENTS.md §5 quick win) --------

    def create_webhook(self, webhook_url: str, campaign_id: int, name: str | None = None,
                        event_type_map: dict[str, bool] | None = None) -> dict:
        body: dict[str, Any] = {
            "webhook_url": webhook_url,
            "association_type": "campaign",
            "email_campaign_id": campaign_id,
        }
        if name is not None:
            body["name"] = name
        if event_type_map is not None:
            body["event_type_map"] = event_type_map
        return self._request("POST", "/webhook/create", json_body=body)

    def get_lead_categories(self) -> list[dict]:
        return self._request("GET", "/leads/fetch-categories")

    def update_lead_category(self, campaign_id: int, lead_id: int, category_id: int | None,
                              pause_lead: bool = False) -> dict:
        return self._request(
            "POST", f"/campaigns/{campaign_id}/leads/{lead_id}/category",
            json_body={"category_id": category_id, "pause_lead": pause_lead},
        )
