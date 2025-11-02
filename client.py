"""
ClickCheck API Client
Main client class for interacting with the ClickCheck AI API.
"""
import requests
from typing import Optional, Dict, Any
from .exceptions import (
    ClickCheckError,
    ClickCheckAPIError,
    ClickCheckRateLimitError,
    ClickCheckInsufficientCreditsError,
)


class ClickCheckClient:
    """
    Client for interacting with the ClickCheck AI API.
    
    Usage:
        >>> from clickcheck import ClickCheckClient
        >>> client = ClickCheckClient(api_token="your_api_token")
        >>> result = client.scan_url("https://example.com")
        >>> print(f"Status: {result['status']}, Score: {result['score']}")
    """
    
    BASE_URL = "https://api.getclickcheck.com/api/v1"
    
    def __init__(
        self,
        api_token: str,
        base_url: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize ClickCheck API client.
        
        Args:
            api_token: Your API token (get it from https://getclickcheck.com/api-tokens)
            base_url: Optional custom base URL (defaults to production)
            timeout: Request timeout in seconds (default: 120)
        """
        self.api_token = api_token
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an API request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/scans/analyze")
            **kwargs: Additional arguments for requests
        
        Returns:
            JSON response as dictionary
        
        Raises:
            ClickCheckError: Base exception for all ClickCheck errors
            ClickCheckAPIError: API returned an error
            ClickCheckRateLimitError: Rate limit exceeded
            ClickCheckInsufficientCreditsError: Insufficient credits
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "60")
                limit = response.headers.get("X-RateLimit-Limit", "unknown")
                remaining = response.headers.get("X-RateLimit-Remaining", "0")
                raise ClickCheckRateLimitError(
                    f"Rate limit exceeded. Limit: {limit}/minute, Remaining: {remaining}. "
                    f"Retry after {retry_after} seconds.",
                    retry_after=int(retry_after),
                    limit=int(limit) if limit != "unknown" else None,
                    remaining=int(remaining) if remaining != "0" else 0,
                )
            
            # Handle insufficient credits
            if response.status_code == 402:
                error_data = response.json() if response.content else {}
                detail = error_data.get("detail", "Insufficient credits")
                raise ClickCheckInsufficientCreditsError(detail)
            
            # Handle other errors
            if not response.ok:
                try:
                    error_data = response.json()
                    detail = error_data.get("detail", f"HTTP {response.status_code}")
                except:
                    detail = f"HTTP {response.status_code}: {response.text[:200]}"
                raise ClickCheckAPIError(detail, status_code=response.status_code)
            
            return response.json()
            
        except (ClickCheckRateLimitError, ClickCheckInsufficientCreditsError, ClickCheckAPIError):
            raise
        except requests.exceptions.Timeout:
            raise ClickCheckError("Request timed out")
        except requests.exceptions.RequestException as e:
            raise ClickCheckError(f"Network error: {str(e)}")
    
    def scan_url(self, url: str, evaluation_mode: str = "default") -> Dict[str, Any]:
        """
        Analyze a URL for privacy and security risks.
        
        Args:
            url: URL to analyze (must start with http:// or https://)
            evaluation_mode: Evaluation mode ("default", "strikt", or "grosszuegig")
                - default: Balanced evaluation (recommended)
                - strikt: Very critical, finds all risks
                - grosszuegig: Optimistic, minimizes concerns
        
        Returns:
            Dictionary with scan results:
            {
                "id": int,
                "url": str,
                "domain": str,
                "status": "SAFE" | "CAUTION" | "UNSAFE",
                "score": float (0.0-1.0),
                "summary": str,
                "ai_analysis": dict,
                "privacy_document_url": str | None,
                "virustotal_data": dict | None,
                "virustotal_risk": float | None,
                "created_at": str (ISO format),
                "credits_used": float
            }
        
        Raises:
            ClickCheckError: Base exception
            ClickCheckAPIError: API error
            ClickCheckRateLimitError: Rate limit exceeded
            ClickCheckInsufficientCreditsError: Insufficient credits
        """
        if evaluation_mode not in ["default", "strikt", "grosszuegig"]:
            raise ValueError(f"Invalid evaluation_mode: {evaluation_mode}. Must be 'default', 'strikt', or 'grosszuegig'")
        
        return self._request(
            "POST",
            "/scans/analyze",
            json={
                "url": url,
                "evaluation_mode": evaluation_mode
            }
        )
    
    def check_blacklist(self, domain: str, url: Optional[str] = None) -> Dict[str, Any]:
        """
        Check if a domain is in the ClickCheck blacklist.
        
        Requires PRO or BUSINESS subscription.
        
        Args:
            domain: Domain to check (e.g., "example.com")
            url: Optional URL to check (more specific)
        
        Returns:
            Dictionary with blacklist status:
            {
                "blacklisted": bool,
                "domain": str,
                "severity": str | None,
                "reason": str | None,
                "first_detected": str | None,
                "report_count": int | None
            }
        """
        params = {"domain": domain}
        if url:
            params["url"] = url
        
        return self._request("GET", "/check", params=params)
    
    def report_blacklist(
        self,
        domain: str,
        url: Optional[str] = None,
        reason: Optional[str] = None,
        evidence: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Report a domain to the blacklist.
        
        If the report is accepted (verified and added), you receive 0.001€ (1 credit) as reward.
        
        Args:
            domain: Domain to report (e.g., "malicious-site.com")
            url: Optional specific URL
            reason: Optional reason for reporting
            evidence: Optional evidence or description
        
        Returns:
            Dictionary with report result:
            {
                "id": int,
                "domain": str,
                "status": "pending" | "verified" | "rejected",
                "reward_credits": float | None (0.001 if accepted),
                "message": str,
                "created_at": str (ISO format)
            }
        """
        return self._request(
            "POST",
            "/blacklist/report",
            json={
                "domain": domain,
                "url": url,
                "reason": reason,
                "evidence": evidence
            }
        )
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get current API token balance and usage.
        
        Returns:
            Dictionary with balance information:
            {
                "balance_credits": float,
                "total_used_credits": float,
                "token_name": str,
                "last_used": str | None (ISO format)
            }
        """
        return self._request("GET", "/balance")

