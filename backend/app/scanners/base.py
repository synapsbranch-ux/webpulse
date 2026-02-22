"""Abstract base scanner defining the interface for all scan modules."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

# Type alias for the live-update callback used by scanners
ScanCallback = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class BaseScanner(ABC):
    """Base class that every scanner module must inherit from.

    Subclasses implement ``run()`` to perform the actual scan and call
    ``callback`` with live progress updates.  ``calculate_score`` and
    ``calculate_grade`` provide a uniform scoring system.
    """

    name: str = "base"

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"scanner.{self.name}")

    @abstractmethod
    async def run(self, url: str, callback: ScanCallback) -> dict[str, Any]:
        """Execute the scan against *url*.

        Args:
            url: The target URL to scan.
            callback: An async callable that receives a dict payload and
                      sends it to the client in real-time (e.g. via WebSocket).

        Returns:
            A dict containing the full scan results for this module.
        """
        ...

    @abstractmethod
    def calculate_score(self, results: dict[str, Any]) -> int:
        """Compute a 0-100 score from the raw scan results."""
        ...

    def calculate_grade(self, score: int) -> str:
        """Map a numeric score to a letter grade.

        95-100 → A+, 85-94 → A, 70-84 → B, 55-69 → C, 40-54 → D, <40 → F
        """
        if score >= 95:
            return "A+"
        if score >= 85:
            return "A"
        if score >= 70:
            return "B"
        if score >= 55:
            return "C"
        if score >= 40:
            return "D"
        return "F"
