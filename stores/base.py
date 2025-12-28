from abc import ABC, abstractmethod
from typing import Optional
from core.models import RateLimitState


class RateLimitStore(ABC):
    """Abstract interface for rate limit state storage."""

    @abstractmethod
    def get_state(self, api_key: str) -> Optional[RateLimitState]:
        """Retrieve rate limit state for an API key."""
        raise NotImplementedError

    @abstractmethod
    def save_state(self, api_key: str, state: RateLimitState) -> None:
        """Persist rate limit state for an API key."""
        raise NotImplementedError

    @abstractmethod
    def clear_state(self, api_key: str) -> None:
        """Clear rate limit state for an API key."""
        raise NotImplementedError
