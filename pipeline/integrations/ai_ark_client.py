"""AI Ark API client (company/people search + email-finding enrichment).

Thin wrapper around the endpoints documented in
`knowledge/tool-docs/ai-ark.md` — auth, schemas, the two-step
search-then-export-with-email pattern, and credit metering are explained
there, not repeated here.

Usage:
    from pipeline.integrations.ai_ark_client import AIArkClient
    client = AIArkClient()  # reads AI_ARK_API_KEY from the environment
    companies = client.search_companies(account={"employeeSize": {...}})
"""
from __future__ import annotations

import os
from typing import Any, Literal

from pipeline.integrations._http import request_with_backoff

BASE_URL = "https://api.ai-ark.com/api/developer-portal"

ListType = Literal["people_id", "company_id"]
ListMode = Literal["APPEND", "REPLACE"]


class AIArkClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL) -> None:
        self.api_key = api_key or os.environ.get("AI_ARK_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "AI_ARK_API_KEY not set. Copy config/.env.example to config/.env "
                "and fill it in, or export it via GitHub Secrets/Doppler in CI."
            )
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None,
                 json_body: dict[str, Any] | None = None) -> Any:
        headers = {"X-TOKEN": self.api_key, "Content-Type": "application/json"}
        response = request_with_backoff(
            method, f"{self.base_url}{path}", headers=headers, params=params, json=json_body
        )
        response.raise_for_status()
        return response.json() if response.content else None

    # --- search ------------------------------------------------------

    def search_companies(self, page: int = 0, size: int = 10,
                          account: dict[str, Any] | None = None,
                          lookalike_domains: list[str] | None = None,
                          lists: dict[str, Any] | None = None) -> Any:
        """See knowledge/tool-docs/ai-ark.md for the full `account` filter
        surface (domain, industries, employeeSize, technology, naics, ...).
        Does not return email — see export_people_with_email()."""
        if lookalike_domains is not None and len(lookalike_domains) > 5:
            raise ValueError("AI Ark accepts at most 5 lookalikeDomains per call")
        body: dict[str, Any] = {"page": page, "size": size}
        if account is not None:
            body["account"] = account
        if lookalike_domains is not None:
            body["lookalikeDomains"] = lookalike_domains
        if lists is not None:
            body["lists"] = lists
        return self._request("POST", "/v1/companies", json_body=body)

    def search_people(self, page: int = 0, size: int = 10,
                       account: dict[str, Any] | None = None,
                       contact: dict[str, Any] | None = None,
                       lists: dict[str, Any] | None = None) -> Any:
        """See knowledge/tool-docs/ai-ark.md for the full `contact` filter
        surface (seniority, departmentAndFunction, experience, ...). Does
        not return email — see export_people_with_email() or
        export_single_person()."""
        body: dict[str, Any] = {"page": page, "size": size}
        if account is not None:
            body["account"] = account
        if contact is not None:
            body["contact"] = contact
        if lists is not None:
            body["lists"] = lists
        return self._request("POST", "/v1/people", json_body=body)

    # --- email finding / export ----------------------------------------

    def export_people_with_email(self, page: int = 0, size: int = 100,
                                  account: dict[str, Any] | None = None,
                                  contact: dict[str, Any] | None = None,
                                  webhook: str | None = None) -> Any:
        """Async bulk export with verified email-finding. `size` max
        10,000. Returns {trackId, statistics, state, ...} immediately —
        poll get_export_results()/get_export_statistics() or handle the
        webhook. Credit-metered: charged per found email."""
        if size > 10_000:
            raise ValueError("AI Ark export size is capped at 10,000")
        body: dict[str, Any] = {"page": page, "size": size}
        if account is not None:
            body["account"] = account
        if contact is not None:
            body["contact"] = contact
        if webhook is not None:
            body["webhook"] = webhook
        return self._request("POST", "/v1/people/export", json_body=body)

    def get_export_results(self, track_id: str, page: int = 0, size: int = 100) -> Any:
        """409 while still processing (not an error — poll again).
        403 means the submission was auto-refunded and isn't retrievable."""
        return self._request(
            "GET", f"/v1/people/export/{track_id}/inquiries", params={"page": page, "size": size}
        )

    def get_export_statistics(self, track_id: str) -> Any:
        return self._request("GET", f"/v1/people/export/{track_id}/statistics")

    def export_single_person(self, person_id: str | None = None, url: str | None = None) -> Any:
        """Real-time single-lead export. Exactly one of `person_id`
        (an AI Ark id from a prior search) or `url` (LinkedIn profile url)
        is required. 1 credit if an email is found, 0 otherwise."""
        if not person_id and not url:
            raise ValueError("export_single_person requires person_id or url")
        body: dict[str, Any] = {}
        if person_id:
            body["id"] = person_id
        if url:
            body["url"] = url
        return self._request("POST", "/v1/people/export/single", json_body=body)

    # --- lists (upstream exclude, not a replacement for pipeline/dedup.py) --

    def save_list(self, values: list[str], list_type: ListType | None = None,
                   list_id: str | None = None, mode: ListMode = "APPEND") -> Any:
        """`list_type` required when creating a new list (no `list_id`).
        See knowledge/tool-docs/ai-ark.md — this excludes by AI Ark's own
        internal id, not by email; it's a second, upstream dedupe layer,
        not a substitute for pipeline/dedup.py."""
        body: dict[str, Any] = {"values": values, "mode": mode}
        if list_id:
            body["id"] = list_id
        if list_type:
            body["type"] = list_type
        return self._request("POST", "/v1/lists", json_body=body)

    # --- account -------------------------------------------------------

    def get_credit(self) -> Any:
        return self._request("GET", "/v1/payments/credits")
