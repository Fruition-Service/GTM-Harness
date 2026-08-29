"""Shared HTTP helper: retry/backoff on 429s for the platform clients.

Not a general-purpose HTTP wrapper — just the one thing both
smartlead_client.py and heyreach_client.py need identically.
"""
from __future__ import annotations

import random
import time
from typing import Any

import requests

MAX_RETRIES = 5


def request_with_backoff(method: str, url: str, **kwargs: Any) -> requests.Response:
    """requests.request() with exponential backoff + jitter on HTTP 429.

    Honors a `Retry-After` header (seconds) when present, otherwise backs
    off 1s, 2s, 4s, 8s, 16s (+ up to 1s jitter). Raises on the final
    attempt via `raise_for_status()` if still failing.
    """
    for attempt in range(MAX_RETRIES):
        response = requests.request(method, url, **kwargs)
        if response.status_code != 429:
            return response

        retry_after = response.headers.get("Retry-After")
        delay = float(retry_after) if retry_after else (2**attempt) + random.random()
        if attempt < MAX_RETRIES - 1:
            time.sleep(delay)

    response.raise_for_status()
    return response
