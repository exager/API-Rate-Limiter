class RateLimiterError(Exception):
    """Base class for rate limiter domain errors."""


class MissingAPIKeyError(RateLimiterError):
    """API key header is missing."""


class InvalidAPIKeyError(RateLimiterError):
    """API key is not recognized."""


class RateLimitExceededError(RateLimiterError):
    """Rate limit exceeded for the given API key."""
