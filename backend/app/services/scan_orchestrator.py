import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import Scan, ScanStatus, ScanResult
from app.websocket.manager import connection_manager
from app.scanners.dns_scanner import DNSScanner
from app.scanners.ssl_scanner import SSLScanner
from app.scanners.performance_scanner import PerformanceScanner
from app.scanners.security_scanner import SecurityScanner
from app.scanners.seo_scanner import SEOScanner

logger = logging.getLogger(__name__)

class ScanOrchestrator:
    """
    Orchestrates the execution of all scanners sequentially for a given Scan.
    Handles database state updates, WebSocket notifications, and error catching.
    """
    
    def __init__(self, db: AsyncSession, scan: Scan):
        self.db = db
        self.scan = scan
        self.scanners = [
            ("dns", DNSScanner()),
            ("ssl", SSLScanner()),
            ("performance", PerformanceScanner()),
            ("security", SecurityScanner()),
            ("seo", SEOScanner())
        ]
        
    async def _send_ws_message(self, message: dict) -> None:
        """Helper to send a message via WebSocket, catching and ignoring disconnection errors."""
        try:
            await connection_manager.send_to_scan(str(self.scan.id), message)
        except Exception as e:
            logger.warning(f"Failed to send WS message for scan {self.scan.id}: {e}")

    async def _save_scan_result(self, module_name: str, score: int, grade: str, data: dict, issues: dict) -> None:
        """Helper to save a ScanResult to the database."""
        result = ScanResult(
            scan_id=self.scan.id,
            module=module_name,
            score=score,
            grade=grade,
            data=data,
            issues_critical=issues.get("critical", 0),
            issues_high=issues.get("high", 0),
            issues_medium=issues.get("medium", 0),
            issues_low=issues.get("low", 0),
        )
        self.db.add(result)
        await self.db.commit()

    async def _update_scan_status(self, status: ScanStatus, current_phase: str | None = None, overall_score: int | None = None) -> None:
        """Helper to update the main Scan record."""
        self.scan.status = status
        if current_phase is not None:
            self.scan.current_phase = current_phase
        if overall_score is not None:
            self.scan.overall_score = overall_score
            
        if status == ScanStatus.COMPLETED or status == ScanStatus.FAILED:
            self.scan.completed_at = datetime.now(timezone.utc)
            if self.scan.started_at:
                self.scan.duration_seconds = int((self.scan.completed_at - self.scan.started_at).total_seconds())
                
        self.db.add(self.scan)
        await self.db.commit()

    async def run(self) -> None:
        """
        Executes all scanners sequentially.
        """
        try:
            logger.info(f"Starting orchestration for scan {self.scan.id} on {self.scan.url}")
            
            # Start scan
            self.scan.started_at = datetime.now(timezone.utc)
            await self._update_scan_status(ScanStatus.RUNNING, current_phase="starting")

            total_score = 0
            successful_modules = 0
            
            total_phases = len(self.scanners)

            for index, (module_name, scanner) in enumerate(self.scanners):
                try:
                    logger.info(f"[{self.scan.id}] Starting module: {module_name}")
                    
                    # Notify Phase Change
                    await self._update_scan_status(ScanStatus.RUNNING, current_phase=module_name)
                    await self._send_ws_message({
                        "type": "phase_change", 
                        "phase": module_name, 
                        "phase_index": index + 1, 
                        "total_phases": total_phases, 
                        "status": "running"
                    })

                    # Define callback for live updates
                    async def live_update_callback(event_type: str, data: dict) -> None:
                        message = {"type": event_type, "phase": module_name}
                        message.update(data)
                        await self._send_ws_message(message)

                    # Run Scanner
                    raw_results = await scanner.run(self.scan.url, live_update_callback)
                    
                    # Calculate Score and Grade
                    score = scanner.calculate_score(raw_results)
                    grade = scanner.calculate_grade(score)
                    
                    # Extract issues counts (pseudo logic, depends on scanner implementation)
                    # Scanners should ideally return an 'issues' dict in their raw_results
                    issues = raw_results.get("issues_summary", {"critical": 0, "high": 0, "medium": 0, "low": 0})

                    # Save result
                    await self._save_scan_result(module_name, score, grade, raw_results, issues)
                    
                    total_score += score
                    successful_modules += 1

                    # Notify Module Complete
                    await self._send_ws_message({
                        "type": "module_complete", 
                        "phase": module_name, 
                        "score": score, 
                        "grade": grade, 
                        "issues_count": issues
                    })
                    
                except Exception as e:
                    logger.error(f"[{self.scan.id}] Error in module {module_name}: {e}", exc_info=True)
                    # Notify Error via Log
                    await self._send_ws_message({
                        "type": "log", 
                        "phase": module_name, 
                        "level": "error", 
                        "message": f"Module failed: {str(e)}", 
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    # We continue to the next scanner (Graceful degradation)

            # Finalize Scan
            if successful_modules > 0:
                overall_score = total_score // successful_modules
                await self._update_scan_status(ScanStatus.COMPLETED, current_phase="completed", overall_score=overall_score)
                
                await self._send_ws_message({
                    "type": "scan_complete", 
                    "overall_score": overall_score, 
                    "duration_seconds": self.scan.duration_seconds, 
                    "report_generating": True
                })
                
                logger.info(f"Scan {self.scan.id} completed successfully with score {overall_score}")
                
            else:
                # All modules failed
                await self._update_scan_status(ScanStatus.FAILED, current_phase="failed", overall_score=0)
                await self._send_ws_message({
                    "type": "scan_complete", 
                    "overall_score": 0, 
                    "duration_seconds": self.scan.duration_seconds, 
                    "report_generating": False
                })
                logger.error(f"Scan {self.scan.id} failed: all modules failed.")

        except Exception as e:
            logger.error(f"Critical orchestration error for scan {self.scan.id}: {e}", exc_info=True)
            await self._update_scan_status(ScanStatus.FAILED, current_phase="failed")
            await self._send_ws_message({
                "type": "log", 
                "phase": "orchestrator", 
                "level": "error", 
                "message": "Critical orchestration failure.", 
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
