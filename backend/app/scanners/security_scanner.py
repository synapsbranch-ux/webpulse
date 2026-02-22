"""Security Scanner (DAST) — headers, cookies, CORS, info disclosure, mixed content."""
from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.scanners.base import BaseScanner, ScanCallback

logger = logging.getLogger(__name__)

# Required security headers and their severity if missing
SECURITY_HEADERS = {
    "Content-Security-Policy": {"severity": "high", "description": "Prevents XSS, clickjacking, and code injection attacks"},
    "X-Content-Type-Options": {"severity": "medium", "description": "Prevents MIME-type sniffing"},
    "X-Frame-Options": {"severity": "medium", "description": "Prevents clickjacking attacks"},
    "Strict-Transport-Security": {"severity": "high", "description": "Enforces HTTPS connections"},
    "Referrer-Policy": {"severity": "low", "description": "Controls referrer information sent with requests"},
    "Permissions-Policy": {"severity": "low", "description": "Controls browser feature permissions"},
    "X-XSS-Protection": {"severity": "low", "description": "Legacy XSS filter (deprecated but still useful)"},
}


class SecurityScanner(BaseScanner):
    """Perform Dynamic Application Security Testing (DAST) checks."""

    name = "security"

    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Execute all security checks against the target URL."""
        results: dict[str, Any] = {"url": url, "issues": []}

        try:
            async with httpx.AsyncClient(
                follow_redirects=True, timeout=15, verify=False
            ) as client:
                response = await client.get(url)
        except Exception as exc:
            await callback({
                "type": "log", "phase": "security", "level": "error",
                "message": f"Failed to fetch URL: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            results["error"] = str(exc)
            results["score"] = 0
            results["grade"] = "F"
            return results

        html = response.text
        headers = response.headers
        soup = BeautifulSoup(html, "lxml")

        # 1. Security headers
        await self._check_security_headers(headers, results, callback)

        # 2. Cookie flags
        await self._check_cookies(response, results, callback)

        # 3. CORS
        await self._check_cors(url, results, callback)

        # 4. Information disclosure
        await self._check_info_disclosure(headers, html, results, callback)

        # 5. Mixed content
        await self._check_mixed_content(url, soup, results, callback)

        # 6. Subresource Integrity (SRI)
        await self._check_sri(soup, url, results, callback)

        # 7. Directory listing
        await self._check_directory_listing(url, results, callback)

        score = self.calculate_score(results)
        grade = self.calculate_grade(score)
        results["score"] = score
        results["grade"] = grade

        return results

    async def _check_security_headers(
        self, headers: httpx.Headers, results: dict, callback: ScanCallback
    ) -> None:
        """Check for presence of recommended security headers."""
        results["headers"] = {}

        for header_name, info in SECURITY_HEADERS.items():
            value = headers.get(header_name.lower())
            present = value is not None
            results["headers"][header_name] = {
                "present": present,
                "value": value,
            }

            if present:
                await callback({
                    "type": "log", "phase": "security", "level": "success",
                    "message": f"Header {header_name} present: {value[:80] if value else ''}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            else:
                results["issues"].append({
                    "severity": info["severity"],
                    "category": "headers",
                    "issue": f"Missing {header_name} header",
                    "description": info["description"],
                    "solution": f"Add the {header_name} header to your server configuration",
                })
                await callback({
                    "type": "log", "phase": "security", "level": "warning",
                    "message": f"Missing security header: {header_name}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

    async def _check_cookies(
        self, response: httpx.Response, results: dict, callback: ScanCallback
    ) -> None:
        """Check cookie security flags (Secure, HttpOnly, SameSite)."""
        results["cookies"] = []
        raw_cookies = response.headers.get_list("set-cookie")

        if not raw_cookies:
            await callback({
                "type": "log", "phase": "security", "level": "info",
                "message": "No cookies set by the server",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return

        for cookie_str in raw_cookies:
            cookie_name = cookie_str.split("=")[0].strip()
            cookie_lower = cookie_str.lower()
            has_secure = "secure" in cookie_lower
            has_httponly = "httponly" in cookie_lower
            has_samesite = "samesite" in cookie_lower

            cookie_info = {
                "name": cookie_name,
                "secure": has_secure,
                "httponly": has_httponly,
                "samesite": has_samesite,
            }
            results["cookies"].append(cookie_info)

            if not has_secure:
                results["issues"].append({
                    "severity": "high",
                    "category": "cookies",
                    "issue": f"Cookie '{cookie_name}' missing Secure flag",
                    "description": "Cookie can be transmitted over unencrypted HTTP",
                    "solution": "Add the Secure flag to this cookie",
                })
            if not has_httponly:
                results["issues"].append({
                    "severity": "medium",
                    "category": "cookies",
                    "issue": f"Cookie '{cookie_name}' missing HttpOnly flag",
                    "description": "Cookie accessible via JavaScript (XSS risk)",
                    "solution": "Add the HttpOnly flag to this cookie",
                })
            if not has_samesite:
                results["issues"].append({
                    "severity": "medium",
                    "category": "cookies",
                    "issue": f"Cookie '{cookie_name}' missing SameSite attribute",
                    "description": "Cookie vulnerable to CSRF attacks",
                    "solution": "Add SameSite=Lax or SameSite=Strict to this cookie",
                })

            flags = []
            if has_secure:
                flags.append("Secure")
            if has_httponly:
                flags.append("HttpOnly")
            if has_samesite:
                flags.append("SameSite")
            level = "success" if all([has_secure, has_httponly, has_samesite]) else "warning"
            await callback({
                "type": "log", "phase": "security", "level": level,
                "message": f"Cookie '{cookie_name}': {', '.join(flags) if flags else 'No security flags'}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    async def _check_cors(self, url: str, results: dict, callback: ScanCallback) -> None:
        """Check CORS configuration for overly permissive settings."""
        try:
            async with httpx.AsyncClient(timeout=10, verify=False) as client:
                response = await client.options(
                    url, headers={"Origin": "https://evil.example.com"}
                )

            acao = response.headers.get("access-control-allow-origin")
            results["cors"] = {"allow_origin": acao}

            if acao == "*":
                results["issues"].append({
                    "severity": "high",
                    "category": "cors",
                    "issue": "CORS allows all origins (wildcard *)",
                    "description": "Any website can make authenticated requests to your API",
                    "solution": "Restrict Access-Control-Allow-Origin to specific trusted domains",
                })
                await callback({
                    "type": "log", "phase": "security", "level": "warning",
                    "message": "CORS: Wildcard (*) origin allowed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            elif acao == "https://evil.example.com":
                results["issues"].append({
                    "severity": "critical",
                    "category": "cors",
                    "issue": "CORS reflects arbitrary origins",
                    "description": "Server echoes back any Origin header, allowing any site to access resources",
                    "solution": "Validate Origin against a whitelist before reflecting it",
                })
                await callback({
                    "type": "log", "phase": "security", "level": "error",
                    "message": "CORS: Server reflects arbitrary origins (critical)",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            elif acao:
                await callback({
                    "type": "log", "phase": "security", "level": "success",
                    "message": f"CORS: Restricted to {acao}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            else:
                await callback({
                    "type": "log", "phase": "security", "level": "success",
                    "message": "CORS: No Access-Control-Allow-Origin header (restrictive)",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception as exc:
            results["cors"] = {"error": str(exc)}
            await callback({
                "type": "log", "phase": "security", "level": "info",
                "message": f"CORS check failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    async def _check_info_disclosure(
        self, headers: httpx.Headers, html: str, results: dict, callback: ScanCallback
    ) -> None:
        """Detect information disclosure through headers and response body."""
        results["info_disclosure"] = []

        # Server header
        server = headers.get("server")
        if server:
            results["info_disclosure"].append({"type": "Server header", "value": server})
            results["issues"].append({
                "severity": "low",
                "category": "info_disclosure",
                "issue": f"Server header reveals: {server}",
                "description": "Server type and version exposed to attackers",
                "solution": "Remove or genericize the Server header",
            })
            await callback({
                "type": "log", "phase": "security", "level": "warning",
                "message": f"Server header exposes: {server}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        # X-Powered-By header
        powered_by = headers.get("x-powered-by")
        if powered_by:
            results["info_disclosure"].append({"type": "X-Powered-By", "value": powered_by})
            results["issues"].append({
                "severity": "low",
                "category": "info_disclosure",
                "issue": f"X-Powered-By header reveals: {powered_by}",
                "description": "Technology stack exposed to attackers",
                "solution": "Remove the X-Powered-By header",
            })
            await callback({
                "type": "log", "phase": "security", "level": "warning",
                "message": f"X-Powered-By exposes: {powered_by}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        # Stack traces in body
        stack_trace_patterns = [
            r"Traceback \(most recent call last\)",
            r"at .+\.java:\d+",
            r"Exception in thread",
            r"Fatal error:.+on line \d+",
            r"<b>Warning</b>:",
            r"Stack trace:",
        ]
        for pattern in stack_trace_patterns:
            if re.search(pattern, html):
                results["info_disclosure"].append({"type": "Stack trace", "pattern": pattern})
                results["issues"].append({
                    "severity": "high",
                    "category": "info_disclosure",
                    "issue": "Stack trace or error details exposed in response",
                    "description": "Detailed error information can help attackers understand the application",
                    "solution": "Disable debug mode and use custom error pages in production",
                })
                await callback({
                    "type": "log", "phase": "security", "level": "error",
                    "message": "Stack trace or debug info detected in response body",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                break

        if not results["info_disclosure"]:
            await callback({
                "type": "log", "phase": "security", "level": "success",
                "message": "No information disclosure detected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    async def _check_mixed_content(
        self, url: str, soup: BeautifulSoup, results: dict, callback: ScanCallback
    ) -> None:
        """Detect HTTP resources loaded on an HTTPS page."""
        if not url.startswith("https://"):
            results["mixed_content"] = {"applicable": False}
            return

        mixed: list[dict[str, str]] = []

        for tag_name, attr in [("script", "src"), ("link", "href"), ("img", "src"), ("iframe", "src")]:
            for tag in soup.find_all(tag_name):
                resource_url = tag.get(attr, "")
                if resource_url.startswith("http://"):
                    mixed.append({"tag": tag_name, "url": resource_url[:200]})

        results["mixed_content"] = {"items": mixed, "count": len(mixed)}

        if mixed:
            results["issues"].append({
                "severity": "medium",
                "category": "mixed_content",
                "issue": f"{len(mixed)} mixed content resource(s) found",
                "description": "HTTP resources on HTTPS pages can be intercepted",
                "solution": "Load all resources over HTTPS",
            })
            await callback({
                "type": "log", "phase": "security", "level": "warning",
                "message": f"Mixed content: {len(mixed)} HTTP resource(s) on HTTPS page",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        else:
            await callback({
                "type": "log", "phase": "security", "level": "success",
                "message": "No mixed content detected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    async def _check_sri(
        self, soup: BeautifulSoup, url: str, results: dict, callback: ScanCallback
    ) -> None:
        """Check for Subresource Integrity on external scripts and stylesheets."""
        parsed = urlparse(url)
        site_domain = parsed.hostname or ""
        missing_sri: list[dict[str, str]] = []

        for tag in soup.find_all("script", src=True):
            src = tag.get("src", "")
            if src.startswith("http") and site_domain not in src:
                if not tag.get("integrity"):
                    missing_sri.append({"tag": "script", "src": src[:200]})

        for tag in soup.find_all("link", rel="stylesheet", href=True):
            href = tag.get("href", "")
            if href.startswith("http") and site_domain not in href:
                if not tag.get("integrity"):
                    missing_sri.append({"tag": "link", "href": href[:200]})

        results["sri"] = {"missing": missing_sri, "count": len(missing_sri)}

        if missing_sri:
            results["issues"].append({
                "severity": "medium",
                "category": "sri",
                "issue": f"{len(missing_sri)} external resource(s) without SRI",
                "description": "External resources without integrity checks can be tampered with",
                "solution": "Add integrity attributes to external script and stylesheet tags",
            })
            await callback({
                "type": "log", "phase": "security", "level": "warning",
                "message": f"SRI: {len(missing_sri)} external resource(s) missing integrity attribute",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        else:
            await callback({
                "type": "log", "phase": "security", "level": "success",
                "message": "All external resources have SRI or none are loaded",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    async def _check_directory_listing(
        self, url: str, results: dict, callback: ScanCallback
    ) -> None:
        """Test common directories for directory listing."""
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        test_paths = ["/", "/images/", "/assets/", "/uploads/", "/static/"]
        listing_found = False

        for path in test_paths:
            try:
                async with httpx.AsyncClient(timeout=5, verify=False) as client:
                    response = await client.get(f"{base}{path}")
                body = response.text.lower()
                if "index of" in body or "directory listing" in body:
                    listing_found = True
                    results["issues"].append({
                        "severity": "medium",
                        "category": "directory_listing",
                        "issue": f"Directory listing enabled at {path}",
                        "description": "Directory contents are visible to anyone",
                        "solution": "Disable directory listing in your web server configuration",
                    })
                    await callback({
                        "type": "log", "phase": "security", "level": "warning",
                        "message": f"Directory listing found at {path}",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
            except Exception:
                continue

        results["directory_listing"] = {"found": listing_found}
        if not listing_found:
            await callback({
                "type": "log", "phase": "security", "level": "success",
                "message": "No directory listing detected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    # ── Scoring ──

    def calculate_score(self, results: dict[str, Any]) -> int:
        """Score based on the number and severity of issues found."""
        score = 100
        severity_weights = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3,
            "info": 0,
        }

        for issue in results.get("issues", []):
            severity = issue.get("severity", "info")
            score -= severity_weights.get(severity, 0)

        return max(0, min(100, score))
