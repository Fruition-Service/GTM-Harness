"""HeyReach API client.

Thin wrapper around the endpoints documented in
`knowledge/tool-docs/heyreach.md` — auth, request/response shapes, and
gotchas (especially the DRAFT-campaign activation gap) are explained
there, not repeated here.

Usage:
    from pipeline.integrations.heyreach_client import HeyReachClient
    client = HeyReachClient()  # reads HEYREACH_API_KEY from the environment
    lst = client.create_empty_list(name="anz-work-management — segment A")
"""
from __future__ import annotations

import os
from typing import Any

from pipeline.integrations._http import request_with_backoff

BASE_URL = "https://api.heyreach.io/api/public"


class HeyReachClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL) -> None:
        self.api_key = api_key or os.environ.get("HEYREACH_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "HEYREACH_API_KEY not set. Copy config/.env.example to config/.env "
                "and fill it in, or export it via GitHub Secrets/Doppler in CI."
            )
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None,
                 json_body: dict[str, Any] | None = None) -> Any:
        headers = {"X-API-KEY": self.api_key}
        if method == "POST" and json_body is None:
            # HeyReach 415s on a bodyless POST (no Content-Type header) —
            # even endpoints with no real payload need an empty JSON object.
            json_body = {}
        response = request_with_backoff(
            method, f"{self.base_url}{path}", headers=headers, params=params, json=json_body
        )
        response.raise_for_status()
        return response.json() if response.content else None

    def check_api_key(self) -> Any:
        return self._request("GET", "/auth/CheckApiKey")

    # --- campaigns ---------------------------------------------------

    def get_campaigns(self, **filters: Any) -> Any:
        return self._request("POST", "/campaign/GetAll", json_body=filters)

    def get_campaign(self, campaign_id: int) -> Any:
        return self._request("GET", "/campaign/GetById", params={"campaignId": campaign_id})

    def get_campaign_sequence(self, campaign_id: int) -> Any:
        """Returns the live sequence tree (nodeType/payload/conditionalNode/
        unconditionalNode) for `campaign_id` — see
        knowledge/tool-docs/heyreach.md for the node schema."""
        return self._request("GET", "/campaign/GetCampaignSequence", params={"campaignId": campaign_id})

    def create_campaign(self, name: str, linked_in_user_list_id: int,
                         linked_in_account_ids: list[int],
                         schedule: dict[str, Any] | None = None,
                         sequence: dict[str, Any] | None = None,
                         **exclude_flags: bool) -> dict:
        """Creates a campaign in **DRAFT** status — see the gotcha section
        in knowledge/tool-docs/heyreach.md. There is no verified API call
        in this client to move it to active; that currently requires the
        HeyReach UI.
        """
        if not (1 <= len(linked_in_account_ids) <= 100):
            raise ValueError("linked_in_account_ids must have 1-100 items")
        body: dict[str, Any] = {
            "name": name,
            "linkedInUserListId": linked_in_user_list_id,
            "linkedInAccountIds": linked_in_account_ids,
            **exclude_flags,
        }
        if schedule is not None:
            body["schedule"] = schedule
        if sequence is not None:
            body["sequence"] = sequence
        return self._request("POST", "/campaign/Create", json_body=body)

    def update_sequence(self, campaign_id: int, sequence: dict[str, Any]) -> Any:
        return self._request(
            "POST", "/campaign/UpdateSequence",
            json_body={"campaignId": campaign_id, "sequence": sequence},
        )

    def update_accounts(self, campaign_id: int, linked_in_account_ids: list[int]) -> Any:
        """Replaces the entire sender list — accounts not in the new list
        are removed from the campaign."""
        return self._request(
            "POST", "/campaign/UpdateAccounts",
            json_body={"campaignId": campaign_id, "linkedInAccountIds": linked_in_account_ids},
        )

    def update_schedule(self, campaign_id: int, schedule: dict[str, Any]) -> Any:
        return self._request(
            "POST", "/campaign/UpdateSchedule",
            json_body={"campaignId": campaign_id, "schedule": schedule},
        )

    def pause_campaign(self, campaign_id: int) -> Any:
        return self._request("POST", "/campaign/Pause", params={"campaignId": campaign_id})

    def resume_campaign(self, campaign_id: int) -> Any:
        """Only works on an already-active, currently-paused campaign —
        rejects DRAFT. See the gotcha section in
        knowledge/tool-docs/heyreach.md."""
        return self._request("POST", "/campaign/Resume", params={"campaignId": campaign_id})

    def add_leads_to_campaign(self, campaign_id: int, account_lead_pairs: list[dict]) -> Any:
        """`account_lead_pairs` max 100 per call: [{linkedInAccountId, lead: {...}}].
        Requires the campaign to be ACTIVE/IN_PROGRESS — see
        knowledge/tool-docs/heyreach.md. Uses the V2 endpoint (V1 exists
        but is undeprecated-and-worse; prefer V2).
        """
        if len(account_lead_pairs) > 100:
            raise ValueError("HeyReach accepts at most 100 leads per add_leads_to_campaign() call")
        return self._request(
            "POST", "/campaign/AddLeadsToCampaignV2",
            json_body={"campaignId": campaign_id, "accountLeadPairs": account_lead_pairs},
        )

    # --- stats -----------------------------------------------------------

    def get_overall_stats(self, campaign_ids: list[int], account_ids: list[int]) -> Any:
        """Returns {byDayStats: {date: {...}}, overallStats: {...}} for the
        given campaigns/sender accounts. Both args are required by the API
        — there's no account-wide "all campaigns" call. Note the PascalCase
        body keys (`AccountIds`/`CampaignIds`) — inconsistent with every
        other HeyReach endpoint's camelCase, confirmed by testing, not a
        typo here."""
        return self._request(
            "POST", "/stats/GetOverallStats",
            json_body={"AccountIds": account_ids, "CampaignIds": campaign_ids},
        )

    # --- lists ---------------------------------------------------------

    def create_empty_list(self, name: str, list_type: str = "USER_LIST") -> Any:
        return self._request("POST", "/list/CreateEmptyList", json_body={"name": name, "type": list_type})

    def get_lists(self, **filters: Any) -> Any:
        return self._request("POST", "/list/GetAll", json_body=filters)
