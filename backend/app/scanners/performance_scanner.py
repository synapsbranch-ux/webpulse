"""Performance Scanner — load testing with Locust in headless/library mode."""
from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any

import httpx

from app.scanners.base import BaseScanner, ScanCallback

logger = logging.getLogger(__name__)

# Load test tiers: (num_users, duration_seconds, spawn_rate)
LOAD_TIERS = [
    {"users": 1, "duration": 30, "spawn_rate": 1},
    {"users": 50, "duration": 60, "spawn_rate": 10},
    {"users": 100, "duration": 60, "spawn_rate": 20},
    {"users": 500, "duration": 90, "spawn_rate": 50},
    {"users": 1000, "duration": 120, "spawn_rate": 100},
]


class PerformanceScanner(BaseScanner):
    """Load-test a URL with escalating concurrency tiers and collect response metrics."""

    name = "performance"

    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Run 5-tier load test against the URL, reporting live metrics."""
        results: dict[str, Any] = {"url": url, "levels": []}

        for tier_index, tier in enumerate(LOAD_TIERS):
            num_users = tier["users"]
            duration = tier["duration"]
            spawn_rate = tier["spawn_rate"]

            await callback({
                "type": "progress",
                "phase": "performance",
                "progress_percent": int((tier_index / len(LOAD_TIERS)) * 100),
                "message": f"Starting tier {tier_index + 1}/5 — {num_users} users for {duration}s",
                "live_metrics": {},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

            tier_result = await self._run_tier(
                url, num_users, duration, spawn_rate, tier_index, callback
            )
            results["levels"].append(tier_result)

            # Tier summary callback
            await callback({
                "type": "log",
                "phase": "performance",
                "level": "success",
                "message": (
                    f"Tier {tier_index + 1} complete — "
                    f"avg: {tier_result['avg_response_time']:.0f}ms, "
                    f"p95: {tier_result['p95']:.0f}ms, "
                    f"throughput: {tier_result['throughput']:.1f} req/s, "
                    f"error_rate: {tier_result['error_rate']:.1f}%"
                ),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        score = self.calculate_score(results)
        grade = self.calculate_grade(score)
        results["score"] = score
        results["grade"] = grade

        return results

    async def _run_tier(
        self,
        url: str,
        num_users: int,
        duration: int,
        spawn_rate: int,
        tier_index: int,
        callback: ScanCallback,
    ) -> dict[str, Any]:
        """Execute a single load tier by sending concurrent requests and measuring metrics."""
        response_times: list[float] = []
        errors: int = 0
        total_requests: int = 0
        total_bytes: int = 0
        ttfb_values: list[float] = []

        start_time = time.monotonic()
        report_interval = 2.0  # seconds between live metric reports
        last_report = start_time

        # Gradually ramp up to num_users
        active_tasks: list[asyncio.Task] = []
        users_spawned = 0

        async def _user_loop(user_id: int) -> None:
            """Simulate a single user making sequential requests."""
            nonlocal errors, total_requests, total_bytes
            while time.monotonic() - start_time < duration:
                req_start = time.monotonic()
                try:
                    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                        response = await client.get(url)
                    elapsed = (time.monotonic() - req_start) * 1000  # ms
                    response_times.append(elapsed)
                    ttfb_values.append(elapsed)  # Simplified: using total time as TTFB
                    total_bytes += len(response.content)
                    total_requests += 1

                    if response.status_code >= 400:
                        errors += 1
                except Exception:
                    errors += 1
                    total_requests += 1
                    elapsed = (time.monotonic() - req_start) * 1000
                    response_times.append(elapsed)

                # Small delay between requests per user
                await asyncio.sleep(0.1)

        # Spawn users gradually
        spawn_interval = 1.0 / max(spawn_rate, 1)
        for i in range(num_users):
            task = asyncio.create_task(_user_loop(i))
            active_tasks.append(task)
            users_spawned += 1

            # Send live metrics every 2 seconds
            now = time.monotonic()
            if now - last_report >= report_interval and response_times:
                sorted_times = sorted(response_times)
                n = len(sorted_times)
                elapsed_total = now - start_time

                live = {
                    "active_users": users_spawned,
                    "total_requests": total_requests,
                    "avg_response_time": sum(sorted_times) / n,
                    "p50": sorted_times[int(n * 0.5)] if n > 0 else 0,
                    "p95": sorted_times[int(n * 0.95)] if n > 0 else 0,
                    "throughput": total_requests / max(elapsed_total, 0.01),
                    "error_rate": (errors / max(total_requests, 1)) * 100,
                }
                await callback({
                    "type": "progress",
                    "phase": "performance",
                    "progress_percent": int(
                        ((tier_index + (now - start_time) / duration) / len(LOAD_TIERS)) * 100
                    ),
                    "message": f"Testing {users_spawned} users — {int(now - start_time)}s elapsed",
                    "live_metrics": live,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                last_report = now

            if i < num_users - 1:
                await asyncio.sleep(spawn_interval)

        # Wait for remaining duration
        remaining = duration - (time.monotonic() - start_time)
        if remaining > 0:
            # Send live metrics during the remaining time
            while remaining > 0:
                wait_time = min(report_interval, remaining)
                await asyncio.sleep(wait_time)
                remaining = duration - (time.monotonic() - start_time)

                if response_times:
                    sorted_times = sorted(response_times)
                    n = len(sorted_times)
                    elapsed_total = time.monotonic() - start_time

                    live = {
                        "active_users": num_users,
                        "total_requests": total_requests,
                        "avg_response_time": sum(sorted_times) / n,
                        "p50": sorted_times[int(n * 0.5)] if n > 0 else 0,
                        "p95": sorted_times[int(n * 0.95)] if n > 0 else 0,
                        "throughput": total_requests / max(elapsed_total, 0.01),
                        "error_rate": (errors / max(total_requests, 1)) * 100,
                    }
                    await callback({
                        "type": "progress",
                        "phase": "performance",
                        "progress_percent": int(
                            ((tier_index + (time.monotonic() - start_time) / duration) / len(LOAD_TIERS)) * 100
                        ),
                        "message": f"Testing {num_users} users — {int(time.monotonic() - start_time)}s elapsed",
                        "live_metrics": live,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })

        # Cancel all user tasks
        for task in active_tasks:
            task.cancel()
        await asyncio.gather(*active_tasks, return_exceptions=True)

        # Compute final metrics
        elapsed_total = time.monotonic() - start_time
        sorted_times = sorted(response_times) if response_times else [0]
        n = len(sorted_times)

        return {
            "users": num_users,
            "duration": round(elapsed_total, 1),
            "spawn_rate": spawn_rate,
            "total_requests": total_requests,
            "avg_response_time": round(sum(sorted_times) / max(n, 1), 2),
            "p50": round(sorted_times[int(n * 0.5)] if n > 0 else 0, 2),
            "p95": round(sorted_times[int(n * 0.95)] if n > 0 else 0, 2),
            "p99": round(sorted_times[int(n * 0.99)] if n > 0 else 0, 2),
            "throughput": round(total_requests / max(elapsed_total, 0.01), 2),
            "error_rate": round((errors / max(total_requests, 1)) * 100, 2),
            "success_rate": round(((total_requests - errors) / max(total_requests, 1)) * 100, 2),
            "ttfb": round(sum(ttfb_values) / max(len(ttfb_values), 1), 2),
            "data_rate_kb": round(total_bytes / 1024 / max(elapsed_total, 0.01), 2),
            "active_connections": num_users,
            "network_errors": errors,
        }

    def calculate_score(self, results: dict[str, Any]) -> int:
        """Score performance based on response times and error rates across tiers."""
        score = 100
        levels = results.get("levels", [])

        if not levels:
            return 0

        # Score based on first tier (1 user — baseline)
        if levels[0]["avg_response_time"] > 2000:
            score -= 20
        elif levels[0]["avg_response_time"] > 1000:
            score -= 10
        elif levels[0]["avg_response_time"] > 500:
            score -= 5

        # Score based on error rates across tiers
        for level in levels:
            if level["error_rate"] > 50:
                score -= 15
            elif level["error_rate"] > 20:
                score -= 10
            elif level["error_rate"] > 5:
                score -= 5

        # Score based on p95 at highest tier
        if len(levels) >= 5:
            high_tier = levels[-1]
            if high_tier["p95"] > 10000:
                score -= 15
            elif high_tier["p95"] > 5000:
                score -= 10
            elif high_tier["p95"] > 3000:
                score -= 5

        # Score based on throughput degradation
        if len(levels) >= 2:
            baseline_throughput = levels[0]["throughput"] if levels[0]["throughput"] > 0 else 1
            for level in levels[1:]:
                per_user_throughput = level["throughput"] / max(level["users"], 1)
                baseline_per_user = baseline_throughput / 1
                if per_user_throughput < baseline_per_user * 0.1:
                    score -= 5

        return max(0, min(100, score))
