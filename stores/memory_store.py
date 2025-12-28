from typing import Optional
from core.models import RateLimitState
from stores.base import RateLimitStore


class InMemoryRateLimitStore(RateLimitStore):
    def __init__(self) -> None:
        self._store: dict[str, RateLimitState] = {}

    def get_state(self, api_key: str) -> Optional[RateLimitState]:
        return self._store.get(api_key)

    def save_state(self, api_key: str, state: RateLimitState) -> None:
        self._store[api_key] = state

    def clear_state(self, api_key: str) -> None:
        self._store.pop(api_key, None)
