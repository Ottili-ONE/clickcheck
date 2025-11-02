"""
Basic tests for ClickCheck SDK
"""
import sys

# Test imports first
try:
    from clickcheck import ClickCheckClient
    from clickcheck.exceptions import (
        ClickCheckError,
        ClickCheckAPIError,
        ClickCheckRateLimitError,
        ClickCheckInsufficientCreditsError,
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def test_imports():
    """Test that all modules can be imported."""
    assert ClickCheckClient is not None, "ClickCheckClient should be importable"
    assert ClickCheckError is not None, "ClickCheckError should be importable"
    assert ClickCheckAPIError is not None, "ClickCheckAPIError should be importable"
    assert ClickCheckRateLimitError is not None, "ClickCheckRateLimitError should be importable"
    assert ClickCheckInsufficientCreditsError is not None, "ClickCheckInsufficientCreditsError should be importable"


def test_client_initialization():
    """Test that client can be initialized."""
    client = ClickCheckClient(api_token="test_token")
    assert client.api_token == "test_token"
    assert client.base_url == "https://api.getclickcheck.com/api/v1"
    assert client.timeout == 120


def test_client_custom_base_url():
    """Test client with custom base URL."""
    client = ClickCheckClient(
        api_token="test_token",
        base_url="https://custom-url.com/api/v1"
    )
    assert client.base_url == "https://custom-url.com/api/v1"


def test_exception_hierarchy():
    """Test that exceptions follow correct inheritance."""
    assert issubclass(ClickCheckAPIError, ClickCheckError)
    assert issubclass(ClickCheckRateLimitError, ClickCheckError)
    assert issubclass(ClickCheckInsufficientCreditsError, ClickCheckError)


def test_api_error_with_status_code():
    """Test APIError with status code."""
    error = ClickCheckAPIError("Test error", status_code=404)
    assert error.status_code == 404
    assert str(error) == "Test error"


def test_rate_limit_error():
    """Test RateLimitError with all parameters."""
    error = ClickCheckRateLimitError(
        "Rate limit exceeded",
        retry_after=60,
        limit=100,
        remaining=0
    )
    assert error.retry_after == 60
    assert error.limit == 100
    assert error.remaining == 0

