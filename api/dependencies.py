from fastapi import Header, HTTPException, status
from app import app_states
from core.rate_limiter import RateLimiter
from core.exceptions import (
    MissingAPIKeyError,
    InvalidAPIKeyError,
    RateLimitExceededError,
)

async def rate_limit_dependency(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    if app_states.rate_limiter is None:
        raise RuntimeError("Rate limiter not initialized")

    try:
        await app_states.rate_limiter.check(x_api_key)
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
