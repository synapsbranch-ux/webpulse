"""SSL/TLS Scanner — certificate analysis, protocol checks, vulnerability detection."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import httpx
from sslyze import (
    Scanner,
    ServerScanRequest,
    ServerNetworkLocation,
    ScanCommand,
)
from sslyze.errors import ServerHostnameCouldNotBeResolved

from app.scanners.base import BaseScanner, ScanCallback

logger = logging.getLogger(__name__)


class SSLScanner(BaseScanner):
    """Analyse SSL/TLS certificates, protocols, cipher suites, and vulnerabilities."""

    name = "ssl"

    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Execute SSL/TLS scan using sslyze."""
        hostname = urlparse(url).hostname or url.replace("https://", "").replace("http://", "").split("/")[0]
        results: dict[str, Any] = {"hostname": hostname}

        await callback({
            "type": "log", "phase": "ssl", "level": "info",
            "message": f"Starting SSL/TLS scan for {hostname}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        try:
            server_location = ServerNetworkLocation(hostname=hostname, port=443)
            scan_request = ServerScanRequest(
                server_location=server_location,
                scan_commands={
                    ScanCommand.CERTIFICATE_INFO,
                    ScanCommand.SSL_2_0_CIPHER_SUITES,
                    ScanCommand.SSL_3_0_CIPHER_SUITES,
                    ScanCommand.TLS_1_0_CIPHER_SUITES,
                    ScanCommand.TLS_1_1_CIPHER_SUITES,
                    ScanCommand.TLS_1_2_CIPHER_SUITES,
                    ScanCommand.TLS_1_3_CIPHER_SUITES,
                    ScanCommand.HEARTBLEED,
                    ScanCommand.OPENSSL_CCS_INJECTION,
                    ScanCommand.TLS_COMPRESSION,
                },
            )
        except ServerHostnameCouldNotBeResolved:
            await callback({
                "type": "log", "phase": "ssl", "level": "error",
                "message": f"Hostname {hostname} could not be resolved",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            results["error"] = "Hostname could not be resolved"
            results["score"] = 0
            results["grade"] = "F"
            return results

        scanner = Scanner()
        scanner.queue_scans([scan_request])

        for server_scan_result in scanner.get_results():
            # Certificate info
            results["certificate"] = await self._extract_cert_info(
                server_scan_result, callback
            )

            # Protocol support
            results["protocols"] = await self._extract_protocols(
                server_scan_result, callback
            )

            # Cipher suites
            results["ciphers"] = await self._extract_ciphers(server_scan_result, callback)

            # Vulnerabilities
            results["vulnerabilities"] = await self._check_vulnerabilities(
                server_scan_result, callback
            )

        # HSTS header check
        results["hsts"] = await self._check_hsts(hostname, callback)

        score = self.calculate_score(results)
        grade = self._calculate_ssl_grade(results, score)
        results["score"] = score
        results["grade"] = grade

        return results

    async def _extract_cert_info(self, scan_result: Any, callback: ScanCallback) -> dict[str, Any]:
        """Extract certificate validity, chain, key size, and signature algorithm."""
        cert_info: dict[str, Any] = {}

        try:
            cert_result = scan_result.scan_result.certificate_info
            if cert_result.status.name == "ERROR_WHEN_RUNNING":
                await callback({
                    "type": "log", "phase": "ssl", "level": "error",
                    "message": "Certificate info scan failed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"error": "scan failed"}

            result = cert_result.result
            deployments = result.certificate_deployments

            if deployments:
                deployment = deployments[0]
                leaf_cert = deployment.received_certificate_chain[0]

                # Validity
                not_before = leaf_cert.not_valid_before_utc if hasattr(leaf_cert, 'not_valid_before_utc') else leaf_cert.not_valid_before
                not_after = leaf_cert.not_valid_after_utc if hasattr(leaf_cert, 'not_valid_after_utc') else leaf_cert.not_valid_after
                now = datetime.now(timezone.utc)

                # Ensure timezone-aware comparison
                if not_after.tzinfo is None:
                    from datetime import timezone as tz
                    not_after = not_after.replace(tzinfo=tz.utc)
                if not_before.tzinfo is None:
                    not_before = not_before.replace(tzinfo=timezone.utc)

                days_remaining = (not_after - now).days
                is_valid = now >= not_before and now <= not_after

                cert_info["not_before"] = not_before.isoformat()
                cert_info["not_after"] = not_after.isoformat()
                cert_info["days_remaining"] = days_remaining
                cert_info["is_valid"] = is_valid
                cert_info["subject"] = leaf_cert.subject.rfc4514_string()
                cert_info["issuer"] = leaf_cert.issuer.rfc4514_string()

                # Key size
                public_key = leaf_cert.public_key()
                cert_info["key_size"] = getattr(public_key, "key_size", None)

                # Signature algorithm
                cert_info["signature_algorithm"] = leaf_cert.signature_hash_algorithm.name if leaf_cert.signature_hash_algorithm else "unknown"

                # Chain length
                cert_info["chain_length"] = len(deployment.received_certificate_chain)

                # OCSP stapling
                cert_info["ocsp_stapling"] = deployment.ocsp_response is not None

                # Trust status
                cert_info["is_trusted"] = deployment.verified_certificate_chain is not None

                level = "success" if is_valid and days_remaining > 30 else "warning"
                await callback({
                    "type": "log", "phase": "ssl", "level": level,
                    "message": f"Certificate valid until {not_after.strftime('%Y-%m-%d')} ({days_remaining} days remaining)",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception as exc:
            logger.exception("Certificate info extraction failed")
            cert_info["error"] = str(exc)
            await callback({
                "type": "log", "phase": "ssl", "level": "error",
                "message": f"Certificate info extraction failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        return cert_info

    async def _extract_protocols(self, scan_result: Any, callback: ScanCallback) -> dict[str, bool]:
        """Determine which SSL/TLS protocol versions are supported."""
        protocols: dict[str, bool] = {}
        protocol_map = {
            "ssl_2_0_cipher_suites": "SSL 2.0",
            "ssl_3_0_cipher_suites": "SSL 3.0",
            "tls_1_0_cipher_suites": "TLS 1.0",
            "tls_1_1_cipher_suites": "TLS 1.1",
            "tls_1_2_cipher_suites": "TLS 1.2",
            "tls_1_3_cipher_suites": "TLS 1.3",
        }

        for attr_name, display_name in protocol_map.items():
            try:
                result_attr = getattr(scan_result.scan_result, attr_name, None)
                if result_attr and result_attr.status.name != "ERROR_WHEN_RUNNING":
                    accepted = result_attr.result.accepted_cipher_suites
                    is_supported = len(accepted) > 0
                    protocols[display_name] = is_supported

                    level = "success" if display_name in ("TLS 1.2", "TLS 1.3") else (
                        "warning" if is_supported else "success"
                    )
                    if display_name in ("SSL 2.0", "SSL 3.0") and is_supported:
                        level = "error"
                    elif display_name in ("TLS 1.0", "TLS 1.1") and is_supported:
                        level = "warning"

                    status_text = "supported" if is_supported else "not supported"
                    await callback({
                        "type": "log", "phase": "ssl", "level": level,
                        "message": f"{display_name}: {status_text}",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                else:
                    protocols[display_name] = False
            except Exception:
                protocols[display_name] = False

        return protocols

    async def _extract_ciphers(self, scan_result: Any, callback: ScanCallback) -> dict[str, list[str]]:
        """List accepted cipher suites for TLS 1.2 and TLS 1.3."""
        ciphers: dict[str, list[str]] = {}

        for version, attr_name in [("TLS 1.2", "tls_1_2_cipher_suites"), ("TLS 1.3", "tls_1_3_cipher_suites")]:
            try:
                result_attr = getattr(scan_result.scan_result, attr_name, None)
                if result_attr and result_attr.status.name != "ERROR_WHEN_RUNNING":
                    accepted = result_attr.result.accepted_cipher_suites
                    ciphers[version] = [cs.cipher_suite.name for cs in accepted]
                else:
                    ciphers[version] = []
            except Exception:
                ciphers[version] = []

        total = sum(len(v) for v in ciphers.values())
        await callback({
            "type": "log", "phase": "ssl", "level": "info",
            "message": f"Accepted cipher suites: {total} total",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return ciphers

    async def _check_vulnerabilities(self, scan_result: Any, callback: ScanCallback) -> dict[str, bool]:
        """Check for known SSL/TLS vulnerabilities."""
        vulns: dict[str, bool] = {}

        # Heartbleed
        try:
            hb = scan_result.scan_result.heartbleed
            if hb and hb.status.name != "ERROR_WHEN_RUNNING":
                vulns["heartbleed"] = hb.result.is_vulnerable_to_heartbleed
                level = "error" if vulns["heartbleed"] else "success"
                msg = "VULNERABLE to Heartbleed!" if vulns["heartbleed"] else "Not vulnerable to Heartbleed"
                await callback({
                    "type": "log", "phase": "ssl", "level": level,
                    "message": msg,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            vulns["heartbleed"] = False

        # OpenSSL CCS Injection
        try:
            ccs = scan_result.scan_result.openssl_ccs_injection
            if ccs and ccs.status.name != "ERROR_WHEN_RUNNING":
                vulns["ccs_injection"] = ccs.result.is_vulnerable_to_ccs_injection
                level = "error" if vulns["ccs_injection"] else "success"
                msg = "VULNERABLE to CCS Injection!" if vulns["ccs_injection"] else "Not vulnerable to CCS Injection"
                await callback({
                    "type": "log", "phase": "ssl", "level": level,
                    "message": msg,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            vulns["ccs_injection"] = False

        # TLS Compression (CRIME)
        try:
            comp = scan_result.scan_result.tls_compression
            if comp and comp.status.name != "ERROR_WHEN_RUNNING":
                vulns["compression"] = comp.result.supports_compression
                level = "warning" if vulns["compression"] else "success"
                msg = "TLS Compression enabled (CRIME risk)" if vulns["compression"] else "TLS Compression disabled"
                await callback({
                    "type": "log", "phase": "ssl", "level": level,
                    "message": msg,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        except Exception:
            vulns["compression"] = False

        return vulns

    async def _check_hsts(self, hostname: str, callback: ScanCallback) -> dict[str, Any]:
        """Check for HTTP Strict Transport Security header."""
        try:
            async with httpx.AsyncClient(verify=False, timeout=10) as client:
                response = await client.get(f"https://{hostname}")

            hsts_header = response.headers.get("strict-transport-security")
            if hsts_header:
                await callback({
                    "type": "log", "phase": "ssl", "level": "success",
                    "message": f"HSTS header present: {hsts_header}",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"present": True, "value": hsts_header}
            else:
                await callback({
                    "type": "log", "phase": "ssl", "level": "warning",
                    "message": "HSTS header not found",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                return {"present": False}
        except Exception as exc:
            await callback({
                "type": "log", "phase": "ssl", "level": "warning",
                "message": f"HSTS check failed: {exc}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return {"present": False, "error": str(exc)}

    # ── Scoring ──

    def calculate_score(self, results: dict[str, Any]) -> int:
        """Compute a 0-100 SSL score."""
        score = 100

        cert = results.get("certificate", {})
        protocols = results.get("protocols", {})
        vulns = results.get("vulnerabilities", {})
        hsts = results.get("hsts", {})

        # Certificate expired
        if not cert.get("is_valid", True):
            score -= 40

        # Certificate expiring soon (< 30 days)
        days = cert.get("days_remaining", 365)
        if isinstance(days, int) and days < 30:
            score -= 10

        # Weak key
        key_size = cert.get("key_size")
        if isinstance(key_size, int) and key_size < 2048:
            score -= 15

        # Old protocols
        if protocols.get("SSL 2.0"):
            score -= 20
        if protocols.get("SSL 3.0"):
            score -= 15
        if protocols.get("TLS 1.0"):
            score -= 10
        if protocols.get("TLS 1.1"):
            score -= 5

        # No modern protocols
        if not protocols.get("TLS 1.2") and not protocols.get("TLS 1.3"):
            score -= 20

        # Vulnerabilities
        if vulns.get("heartbleed"):
            score -= 25
        if vulns.get("ccs_injection"):
            score -= 20
        if vulns.get("compression"):
            score -= 5

        # No HSTS
        if not hsts.get("present"):
            score -= 5

        return max(0, score)

    def _calculate_ssl_grade(self, results: dict[str, Any], score: int) -> str:
        """Compute SSL-specific grade based on score and conditions."""
        cert = results.get("certificate", {})
        protocols = results.get("protocols", {})
        vulns = results.get("vulnerabilities", {})
        hsts = results.get("hsts", {})

        # F conditions
        if not cert.get("is_valid", True):
            return "F"
        if vulns.get("heartbleed") or vulns.get("ccs_injection"):
            return "D"
        if protocols.get("TLS 1.0"):
            return "C" if score >= 55 else "D"
        if protocols.get("TLS 1.1"):
            return "B" if score >= 70 else "C"

        # A+ conditions
        only_modern = (
            not protocols.get("SSL 2.0")
            and not protocols.get("SSL 3.0")
            and not protocols.get("TLS 1.0")
            and not protocols.get("TLS 1.1")
        )
        key_size = cert.get("key_size", 0) or 0
        no_vulns = not any(vulns.values())

        if only_modern and hsts.get("present") and no_vulns and key_size >= 2048 and score >= 95:
            return "A+"

        return self.calculate_grade(score)
