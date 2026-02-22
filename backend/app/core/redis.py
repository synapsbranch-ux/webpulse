"""Redis client configuration and rate limiting utilities."""
from __future__ import annotations

import logging
from typing import Optional

import redis.asyncio as aioredis

from app.config import settings

logger = logging.getLogger(__name__)

# Module-level Redis client (initialized via init_redis)
_redis_client: Optional[aioredis.Redis] = None


async def init_redis() -> aioredis.Redis:
    """Initialize the async Redis client. Call once at application startup."""
    global _redis_client
    _redis_client = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )
    # Verify connection
    await _redis_client.ping()
    logger.info("Redis connection established at %s", settings.REDIS_URL)
    return _redis_client


async def get_redis() -> aioredis.Redis:
    """Return the active Redis client. Raises if not initialized."""
    if _redis_client is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis_client


async def close_redis() -> None:
    """Gracefully close the Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")


async def check_rate_limit(
    key: str,
    max_attempts: int = 5,
    window_seconds: int = 60,
) -> bool:
    """Check and enforce rate limiting using a sliding window counter.

    Args:
        key: Unique identifier for the rate limit bucket (e.g. "login:user@example.com").
        max_attempts: Maximum number of attempts allowed within the window.
        window_seconds: Time window in seconds.

    Returns:
        True if the request is allowed, False if rate-limited.
    """
    client = await get_redis()
    full_key = f"rate_limit:{key}"

    current = await client.get(full_key)
    if current is not None and int(current) >= max_attempts:
        logger.warning("Rate limit exceeded for key=%s (count=%s)", key, current)
        return False

    pipe = client.pipeline()
    pipe.incr(full_key)
    pipe.expire(full_key, window_seconds)
    await pipe.execute()
    return True
