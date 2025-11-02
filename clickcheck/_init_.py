"""
ClickCheck AI Python SDK
Official Python client for the ClickCheck AI API.
"""
from .client import ClickCheckClient
from .exceptions import ClickCheckError, ClickCheckAPIError, ClickCheckRateLimitError, ClickCheckInsufficientCreditsError

__version__ = "1.0.0"
__all__ = [
    "ClickCheckClient",
    "ClickCheckError",
    "ClickCheckAPIError",
    "ClickCheckRateLimitError",
    "ClickCheckInsufficientCreditsError",
]

