"""
ClickCheck API Exceptions
Custom exceptions for the ClickCheck API client.
"""
from typing import Optional


class ClickCheckError(Exception):
    """Base exception for all ClickCheck errors."""
    pass


class ClickCheckAPIError(ClickCheckError):
    """API returned an error."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class ClickCheckRateLimitError(ClickCheckError):
    """Rate limit exceeded."""
    
    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None
    ):
        super().__init__(message)
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining


class ClickCheckInsufficientCreditsError(ClickCheckError):
    """Insufficient credits to perform the operation."""
    pass

