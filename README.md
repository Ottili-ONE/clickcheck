# ClickCheck Python SDK

[![PyPI version](https://badge.fury.io/py/clickcheck.svg)](https://badge.fury.io/py/clickcheck)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [ClickCheck AI API](https://getclickcheck.com) - Analyze website privacy and security risks programmatically.

## Features

- 🔍 **URL Scanning**: Analyze websites for privacy and security risks
- 🚫 **Blacklist Check**: Check if domains are in the ClickCheck blacklist
- 📊 **Blacklist Reporting**: Report malicious domains and earn rewards (0.001€ per accepted report)
- 💰 **Credit-based**: Pay-as-you-go with affordable pricing (0.012€ per scan)
- ⚡ **Rate Limiting**: Different limits based on your plan (FREE: 10/min, PRO: 60/min, BUSINESS: 300/min)

## Installation

```bash
pip install clickcheck
```

## Quick Start

```python
from clickcheck import ClickCheckClient

# Initialize client with your API token
client = ClickCheckClient(api_token="your_api_token_here")

# Scan a URL
result = client.scan_url("https://example.com")
print(f"Status: {result['status']}")  # SAFE, CAUTION, or UNSAFE
print(f"Risk Score: {result['score']}")  # 0.0 (safe) to 1.0 (unsafe)
print(f"Summary: {result['summary']}")

# Check blacklist
blacklist_check = client.check_blacklist("suspicious-site.com")
if blacklist_check['blacklisted']:
    print(f"⚠️ Domain is blacklisted: {blacklist_check['reason']}")

# Report a malicious domain (earn 0.001€ reward if accepted!)
report = client.report_blacklist(
    domain="malicious-site.com",
    reason="Phishing website",
    evidence="Received phishing email from this domain"
)
if report['reward_credits']:
    print(f"✅ Report accepted! You earned {report['reward_credits']:.3f}€")

# Check your balance
balance = client.get_balance()
print(f"Balance: {balance['balance_credits']:.4f}€")
```

## Authentication

Get your API token from [https://getclickcheck.com/api-tokens](https://getclickcheck.com/api-tokens)

1. Log in to your ClickCheck account
2. Go to API Tokens section
3. Create a new token (BUSINESS plan required)
4. Copy the token (shown only once!)

## API Reference

### `ClickCheckClient(api_token, base_url=None, timeout=120)`

Initialize the client.

**Parameters:**
- `api_token` (str): Your API token
- `base_url` (str, optional): Custom API base URL (defaults to production)
- `timeout` (int): Request timeout in seconds (default: 120)

### `scan_url(url, evaluation_mode="default")`

Analyze a URL for privacy and security risks.

**Parameters:**
- `url` (str): URL to analyze (must start with http:// or https://)
- `evaluation_mode` (str): Evaluation mode:
  - `"default"`: Balanced evaluation (recommended)
  - `"strikt"`: Very critical, finds all risks
  - `"grosszuegig"`: Optimistic, minimizes concerns

**Returns:**
```python
{
    "id": int,
    "url": str,
    "domain": str,
    "status": "SAFE" | "CAUTION" | "UNSAFE",
    "score": float,  # 0.0 (safe) to 1.0 (unsafe)
    "summary": str,
    "ai_analysis": dict,
    "privacy_document_url": str | None,
    "virustotal_data": dict | None,
    "virustotal_risk": float | None,
    "created_at": str,  # ISO format
    "credits_used": float
}
```

### `check_blacklist(domain, url=None)`

Check if a domain is in the ClickCheck blacklist. Requires PRO or BUSINESS subscription.

**Parameters:**
- `domain` (str): Domain to check (e.g., "example.com")
- `url` (str, optional): Specific URL to check

**Returns:**
```python
{
    "blacklisted": bool,
    "domain": str,
    "severity": str | None,
    "reason": str | None,
    "first_detected": str | None,
    "report_count": int | None
}
```

### `report_blacklist(domain, url=None, reason=None, evidence=None)`

Report a domain to the blacklist. If accepted, you receive 0.001€ (1 credit) as reward.

**Parameters:**
- `domain` (str): Domain to report
- `url` (str, optional): Specific URL
- `reason` (str, optional): Reason for reporting
- `evidence` (str, optional): Evidence or description

**Returns:**
```python
{
    "id": int,
    "domain": str,
    "status": "pending" | "verified" | "rejected",
    "reward_credits": float | None,  # 0.001 if accepted
    "message": str,
    "created_at": str  # ISO format
}
```

### `get_balance()`

Get current API token balance and usage statistics.

**Returns:**
```python
{
    "balance_credits": float,
    "total_used_credits": float,
    "token_name": str,
    "last_used": str | None  # ISO format
}
```

## Error Handling

The SDK provides custom exceptions for better error handling:

```python
from clickcheck import (
    ClickCheckClient,
    ClickCheckError,
    ClickCheckAPIError,
    ClickCheckRateLimitError,
    ClickCheckInsufficientCreditsError
)

client = ClickCheckClient(api_token="your_token")

try:
    result = client.scan_url("https://example.com")
except ClickCheckRateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
    print(f"Limit: {e.limit}/minute, Remaining: {e.remaining}")
except ClickCheckInsufficientCreditsError:
    print("Insufficient credits. Please top up your balance.")
except ClickCheckAPIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
except ClickCheckError as e:
    print(f"Error: {e}")
```

## Pricing

- **Scan Cost**: 0.012€ per scan (reduced from 0.032€)
- **Reward**: 0.001€ per accepted blacklist report

## Rate Limits

Rate limits are based on your subscription plan:

- **FREE**: 10 requests/minute
- **PRO**: 60 requests/minute
- **BUSINESS**: 300 requests/minute (highest)

When rate limited, the SDK raises `ClickCheckRateLimitError` with retry information.

## Requirements

- Python 3.8+
- `requests>=2.31.0`

## Documentation

Full API documentation: [https://docs.getclickcheck.com](https://docs.getclickcheck.com)

## Support

- Website: [https://getclickcheck.com](https://getclickcheck.com)
- Documentation: [https://docs.getclickcheck.com](https://docs.getclickcheck.com)
- Issues: [GitHub Issues](https://github.com/Ottili-ONE/clickcheck/issues)

## License

MIT License - see LICENSE file for details.

## Changelog

### 1.0.0 (2024)
- Initial release
- URL scanning functionality
- Blacklist check and reporting
- Credit-based pricing (0.012€ per scan)
- Rate limiting based on subscription plan
- Reward system for accepted blacklist reports (0.001€)

