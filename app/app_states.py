from typing import Optional

from core.rate_limiter import RateLimiter
from stores.base import RateLimitStore
from utils.config import Settings

settings: Optional[Settings] = None
store: Optional[RateLimitStore] = None
rate_limiter: Optional[RateLimiter] = None
