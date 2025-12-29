import time
import logging
from typing import Union

from core.models import RateLimitState
from core.exceptions import (
    MissingAPIKeyError,
    InvalidAPIKeyError,
    RateLimitExceededError,
)
from utils.config import RateLimitConfig
from stores.base import RateLimitStore

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(
        self,
        config: RateLimitConfig,
        store: RateLimitStore,
    ) -> None:
        self._config = config
        self._store = store

    async def check(self, api_key: str) -> None:
        '''
        Enforce rate limiting for a given API key.
        Raises domain exceptions on failure.
        '''

        if not api_key:
            logger.warning("Missing API key")
            raise MissingAPIKeyError()

        if api_key not in self._config.allowed_api_keys:
            logger.warning("Invalid API key attempted: %s", api_key)
            raise InvalidAPIKeyError()

        state = await self._get_state(api_key)

        if state is None:
            state = RateLimitState()
            logger.info("Initializing rate limit state for key=%s", api_key)

        # Check window expiration
        if state.is_window_expired(self._config.window_seconds):
            logger.info(
                "Rate limit window expired for key=%s, resetting state", api_key
            )
            state.count = 0
            state.window_start = time.time()

        state.count += 1

        logger.debug(
            "Rate limit check key=%s count=%d",
            api_key,
            state.count,
        )

        if state.count > self._config.requests_per_window:
            logger.warning(
                "Rate limit exceeded key=%s count=%d limit=%d",
                api_key,
                state.count,
                self._config.requests_per_window,
            )
            await self._save_state(api_key, state)
            raise RateLimitExceededError()

        await self._save_state(api_key, state)

    async def _get_state(self, api_key: str) -> RateLimitState | None:
        result = self._store.get_state(api_key)
        if hasattr(result, "__await__"):
            return await result
        return result

    async def _save_state(self, api_key: str, state: RateLimitState) -> None:
        result = self._store.save_state(api_key, state)
        if hasattr(result, "__await__"):
            await result
