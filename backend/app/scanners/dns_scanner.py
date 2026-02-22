"""DNS Scanner — resolves records, checks DNSSEC, propagation, ports, redirects."""
from __future__ import annotations

import asyncio
import logging
import socket
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import dns.asyncresolver
import dns.resolver
import httpx

from app.scanners.base import BaseScanner, ScanCallback

logger = logging.getLogger(__name__)

# Public DNS servers for propagation checks
PROPAGATION_SERVERS = {
    "Google": "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS": "208.67.222.222",
}

SCAN_PORTS = [80, 443, 8080, 8443]


class DNSScanner(BaseScanner):
    """Scan DNS records, DNSSEC, propagation, ports, HTTP→HTTPS redirect, IPv6."""

    name = "dns"

    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Execute all DNS sub-tests and report progress via callback."""
        hostname = urlparse(url).hostname or url.replace("https://", "").replace("http://", "").split("/")[0]
        results: dict[str, Any] = {"hostname": hostname, "checks": {}}

        # 1. Resolve DNS records
        results["checks"]["records"] = await self._resolve_records(hostname, callback)

        # 2. Resolution time
        results["checks"]["resolution_time"] = await self._measure_resolution_time(hostname, callback)

        # 3. DNSSEC
        results["checks"]["dnssec"] = await self._check_dnssec(hostname, callback)

        # 4. Propagation
        results["checks"]["propagation"] = await self._check_propagation(hostname, callback)

        # 5. Ping / latency
        results["checks"]["latency"] = await self._check_latency(hostname, callback)

        # 6. Port scan
        results["checks"]["ports"] = await self._scan_ports(hostname, callback)

        # 7. HTTP → HTTPS redirect
        results["checks"]["https_redirect"] = await self._check_https_redirect(hostname, callback)

        # 8. IPv6 support
        results["checks"]["ipv6"] = await self._check_ipv6(hostname, callback)

        # Calculate score
        score = self.calculate_score(results)
        grade = self.calculate_grade(score)
        results["score"] = score
        results["grade"] = grade

        return results

    # ── Sub-tests ──

    async def _resolve_records(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Resolve A, AAAA, MX, NS, TXT, SOA, CNAME records."""
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
        records: dict[str, list[str]] = {}

        for rtype in record_types:
            try:
                resolver = dns.asyncresolver.Resolver()
                resolver.timeout = 5
                resolver.lifetime = 5
                answers = await resolver.resolve(hostname, rtype)
                records[rtype] = [str(rdata) for rdata in answers]
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "success",
                    "message": f"{rtype} records found ({len(records[rtype])})",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except dns.resolver.NoAnswer:
                records[rtype] = []
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "info",
                    "message": f"No {rtype} records found",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except dns.resolver.NXDOMAIN:
                records[rtype] = []
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "error",
                    "message": f"Domain does not exist (NXDOMAIN) when querying {rtype}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except Exception as exc:
                records[rtype] = []
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "warning",
                    "message": f"Failed to resolve {rtype}: {exc}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

        return records

    async def _measure_resolution_time(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Measure how long DNS resolution takes."""
        try:
            resolver = dns.asyncresolver.Resolver()
            start = time.monotonic()
            await resolver.resolve(hostname, "A")
            elapsed_ms = round((time.monotonic() - start) * 1000, 2)
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "success",
                "message": f"DNS resolution time: {elapsed_ms}ms",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"resolution_ms": elapsed_ms}
        except Exception as exc:
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "error",
                "message": f"DNS resolution failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"resolution_ms": None, "error": str(exc)}

    async def _check_dnssec(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Check if DNSSEC is enabled for the domain."""
        try:
            resolver = dns.asyncresolver.Resolver()
            resolver.use_edns(0, dns.flags.DO, 4096)
            answer = await resolver.resolve(hostname, "A")
            has_dnssec = bool(answer.response.flags & dns.flags.AD)
            level = "success" if has_dnssec else "warning"
            msg = "DNSSEC is enabled" if has_dnssec else "DNSSEC is not enabled"
            await callback({
                "type": "log",
                "phase": "dns",
                "level": level,
                "message": msg,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"enabled": has_dnssec}
        except Exception as exc:
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "warning",
                "message": f"DNSSEC check failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"enabled": False, "error": str(exc)}

    async def _check_propagation(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Test DNS propagation across public resolvers."""
        propagation: dict[str, Any] = {}
        for name, server_ip in PROPAGATION_SERVERS.items():
            try:
                resolver = dns.asyncresolver.Resolver()
                resolver.nameservers = [server_ip]
                resolver.timeout = 5
                resolver.lifetime = 5
                answers = await resolver.resolve(hostname, "A")
                ips = [str(r) for r in answers]
                propagation[name] = {"resolved": True, "ips": ips}
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "success",
                    "message": f"Propagation OK on {name} DNS ({server_ip}): {', '.join(ips)}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except Exception as exc:
                propagation[name] = {"resolved": False, "error": str(exc)}
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "warning",
                    "message": f"Propagation failed on {name} DNS ({server_ip}): {exc}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        return propagation

    async def _check_latency(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Measure TCP connection latency (ping-like) to port 443 or 80."""
        for port in [443, 80]:
            try:
                start = time.monotonic()
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(hostname, port),
                    timeout=5.0,
                )
                latency_ms = round((time.monotonic() - start) * 1000, 2)
                writer.close()
                await writer.wait_closed()
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "success",
                    "message": f"TCP latency to port {port}: {latency_ms}ms",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"latency_ms": latency_ms, "port": port}
            except Exception:
                continue

        await callback({
            "type": "log",
            "phase": "dns",
            "level": "error",
            "message": "Could not measure latency (ports 443 and 80 unreachable)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return {"latency_ms": None}

    async def _scan_ports(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Check if common web ports are open."""
        port_results: dict[int, bool] = {}
        for port in SCAN_PORTS:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(hostname, port),
                    timeout=3.0,
                )
                writer.close()
                await writer.wait_closed()
                port_results[port] = True
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "success",
                    "message": f"Port {port} is open",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            except Exception:
                port_results[port] = False
                level = "error" if port == 443 else "info"
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": level,
                    "message": f"Port {port} is closed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        return port_results

    async def _check_https_redirect(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Check whether HTTP automatically redirects to HTTPS."""
        try:
            async with httpx.AsyncClient(follow_redirects=False, timeout=10) as client:
                response = await client.get(f"http://{hostname}")

            redirects = response.status_code in (301, 302, 307, 308)
            location = response.headers.get("location", "")
            to_https = location.startswith("https://")

            if redirects and to_https:
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "success",
                    "message": f"HTTP redirects to HTTPS ({response.status_code} → {location})",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"redirects": True, "to_https": True, "status_code": response.status_code}
            elif redirects:
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "warning",
                    "message": f"HTTP redirects but not to HTTPS ({location})",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"redirects": True, "to_https": False, "status_code": response.status_code}
            else:
                await callback({
                    "type": "log",
                    "phase": "dns",
                    "level": "warning",
                    "message": "No HTTP → HTTPS redirect detected",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"redirects": False, "to_https": False, "status_code": response.status_code}
        except Exception as exc:
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "warning",
                "message": f"HTTPS redirect check failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"redirects": False, "to_https": False, "error": str(exc)}

    async def _check_ipv6(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Check if the domain has AAAA (IPv6) records."""
        try:
            resolver = dns.asyncresolver.Resolver()
            answers = await resolver.resolve(hostname, "AAAA")
            ips = [str(r) for r in answers]
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "success",
                "message": f"IPv6 supported: {', '.join(ips)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"supported": True, "addresses": ips}
        except dns.resolver.NoAnswer:
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "warning",
                "message": "No IPv6 (AAAA) records found",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"supported": False, "addresses": []}
        except Exception as exc:
            await callback({
                "type": "log",
                "phase": "dns",
                "level": "warning",
                "message": f"IPv6 check failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"supported": False, "addresses": [], "error": str(exc)}

    # ── Scoring ──

    def calculate_score(self, results: dict[str, Any]) -> int:
        """Score from 100, deducting for missing capabilities."""
        score = 100
        checks = results.get("checks", {})

        # -30 if no A record
        records = checks.get("records", {})
        if not records.get("A"):
            score -= 30

        # -15 if no HTTPS redirect
        https_redirect = checks.get("https_redirect", {})
        if not https_redirect.get("to_https"):
            score -= 15

        # -20 if port 443 closed
        ports = checks.get("ports", {})
        if not ports.get(443):
            score -= 20

        # -5 if no IPv6
        ipv6 = checks.get("ipv6", {})
        if not ipv6.get("supported"):
            score -= 5

        # -10 if no DNSSEC
        dnssec = checks.get("dnssec", {})
        if not dnssec.get("enabled"):
            score -= 10

        return max(0, score)
