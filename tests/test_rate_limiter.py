import pytest
import asyncio
import time

from core.rate_limiter import RateLimiter
from core.exceptions import (
    MissingAPIKeyError,
    InvalidAPIKeyError,
    RateLimitExceededError,
)
from core.models import RateLimitState
from stores.memory_store import InMemoryRateLimitStore
from utils.config import RateLimitConfig


@pytest.mark.asyncio
async def test_allows_requests_under_limit():
    config = RateLimitConfig(
        requests_per_window=3,
        window_seconds=60,
        allowed_api_keys={"key1"},
    )
    store = InMemoryRateLimitStore()
    limiter = RateLimiter(config, store)

    await limiter.check("key1")
    await limiter.check("key1")
    await limiter.check("key1")


@pytest.mark.asyncio
async def test_blocks_when_limit_exceeded():
    config = RateLimitConfig(
        requests_per_window=2,
        window_seconds=60,
        allowed_api_keys={"key1"},
    )
    store = InMemoryRateLimitStore()
    limiter = RateLimiter(config, store)

    await limiter.check("key1")
    await limiter.check("key1")

    with pytest.raises(RateLimitExceededError):
        await limiter.check("key1")


@pytest.mark.asyncio
async def test_window_resets_after_expiry():
    config = RateLimitConfig(
        requests_per_window=1,
        window_seconds=1,
        allowed_api_keys={"key1"},
    )
    store = InMemoryRateLimitStore()
    limiter = RateLimiter(config, store)

    await limiter.check("key1")

    time.sleep(1.1)

    # Should be allowed again after window reset
    await limiter.check("key1")


@pytest.mark.asyncio
async def test_missing_api_key():
    config = RateLimitConfig(
        requests_per_window=1,
        window_seconds=60,
        allowed_api_keys={"key1"},
    )
    store = InMemoryRateLimitStore()
    limiter = RateLimiter(config, store)

    with pytest.raises(MissingAPIKeyError):
        await limiter.check(None)


@pytest.mark.asyncio
async def test_invalid_api_key():
    config = RateLimitConfig(
        requests_per_window=1,
        window_seconds=60,
        allowed_api_keys={"key1"},
    )
    store = InMemoryRateLimitStore()
    limiter = RateLimiter(config, store)

    with pytest.raises(InvalidAPIKeyError):
        await limiter.check("wrong")
