from pydantic import BaseModel, Field
from typing import Optional
import time

# Rate limit runtime state
class RateLimitState(BaseModel):
    count: int = Field(default=0, ge=0)
    window_start: float = Field(default_factory=lambda: time.time())

    def is_window_expired(self, window_seconds: int) -> bool:
        return (time.time() - self.window_start) >= window_seconds


# Success response model
class ResourceResponse(BaseModel):
    message: str
    timestamp: float = Field(default_factory=lambda: time.time())

# Error response model
class ErrorResponse(BaseModel):
    error: str
    detail: str
