"""WebSocket connection manager for real-time scan updates."""
from __future__ import annotations

import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections keyed by scan_id.

    Each scan can have one active WebSocket connection at a time.
    Messages are sent as JSON payloads.
    """

    def __init__(self) -> None:
        self._connections: dict[str, WebSocket] = {}

    async def connect(self, scan_id: str, websocket: WebSocket) -> None:
        """Accept and register a WebSocket connection for a scan."""
        await websocket.accept()
        self._connections[scan_id] = websocket
        logger.info("WebSocket connected for scan %s", scan_id)

    def disconnect(self, scan_id: str) -> None:
        """Remove a WebSocket connection for a scan."""
        self._connections.pop(scan_id, None)
        logger.info("WebSocket disconnected for scan %s", scan_id)

    async def send_to_scan(self, scan_id: str, data: dict[str, Any]) -> None:
        """Send a JSON message to the WebSocket associated with a scan.

        Silently disconnects if the send fails (client gone).
        """
        websocket = self._connections.get(scan_id)
        if websocket is None:
            return

        try:
            await websocket.send_json(data)
        except Exception as exc:
            logger.warning(
                "Failed to send WebSocket message for scan %s: %s", scan_id, exc
            )
            self.disconnect(scan_id)

    async def broadcast(self, data: dict[str, Any]) -> None:
        """Send a JSON message to all connected WebSocket clients."""
        disconnected: list[str] = []
        for scan_id, websocket in self._connections.items():
            try:
                await websocket.send_json(data)
            except Exception:
                disconnected.append(scan_id)

        for scan_id in disconnected:
            self.disconnect(scan_id)

    @property
    def active_connections(self) -> int:
        """Return the number of active WebSocket connections."""
        return len(self._connections)


# Global singleton instance
ws_manager = ConnectionManager()
