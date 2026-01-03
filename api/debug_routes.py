from fastapi import APIRouter, Header, HTTPException, status

from stores.base import RateLimitStore
from core.models import RateLimitState
from app import app_states  

router = APIRouter(prefix="/debug")


@router.get("/rate-limit")
async def get_rate_limit_state(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    state = app_states.store.get_state(x_api_key)
    if hasattr(state, "__await__"):
        state = await state

    if state is None:
        return {
            "count": 0,
            "limit": app_states.settings.rate_limit.requests_per_window,
            "window_seconds": app_states.settings.rate_limit.window_seconds,
            "window_start": None,
        }

    return {
        "count": state.count,
        "limit": app_states.settings.rate_limit.requests_per_window,
        "window_seconds": app_states.settings.rate_limit.window_seconds,
        "window_start": state.window_start,
    }
