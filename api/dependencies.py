from fastapi import Header, HTTPException, status

from core.rate_limiter import RateLimiter
from core.exceptions import (
    MissingAPIKeyError,
    InvalidAPIKeyError,
    RateLimitExceededError,
)

# This will be injected from app startup
rate_limiter: RateLimiter | None = None


def set_rate_limiter(rl: RateLimiter) -> None:
    global rate_limiter
    rate_limiter = rl


async def rate_limit_dependency(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if rate_limiter is None:
        raise RuntimeError("Rate limiter not initialized")

    try:
        await rate_limiter.check(x_api_key)
    except MissingAPIKeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    except InvalidAPIKeyError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    except RateLimitExceededError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )
