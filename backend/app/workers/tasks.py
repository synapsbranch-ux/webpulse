import asyncio
import logging
from uuid import UUID

from app.workers.celery_app import celery_app
from app.core.database import async_session_maker
from app.models.scan import Scan, ScanStatus
from app.services.scan_orchestrator import ScanOrchestrator

logger = logging.getLogger(__name__)

async def run_scan_async(scan_id: str) -> None:
    """Async wrapper to run the scan orchestrator."""
    async with async_session_maker() as db:
        try:
            scan = await db.get(Scan, UUID(scan_id))
            if not scan:
                logger.error(f"Scan {scan_id} not found in database.")
                return
                
            orchestrator = ScanOrchestrator(db, scan)
            await orchestrator.run()
            
            # If scan completed successfully, trigger report generation
            if scan.status == ScanStatus.COMPLETED:
                logger.info(f"Scan {scan_id} completed. Triggering report generation task.")
                generate_report_task.delay(str(scan.id))
                
        except Exception as e:
            logger.error(f"Failed to execute orchestrator for scan {scan_id}: {e}", exc_info=True)


@celery_app.task(name="tasks.run_scan_task")
def run_scan_task(scan_id: str) -> None:
    """
    Celery task to run the full scan sequence.
    Triggers the async ScanOrchestrator inside a synchronous Celery task.
    """
    logger.info(f"Received scan task for ID {scan_id}")
    asyncio.run(run_scan_async(scan_id))


async def generate_report_async(scan_id: str) -> None:
    """Async wrapper to generate the report."""
    from app.services.report_service import ReportService
    async with async_session_maker() as db:
        try:
            report_service = ReportService(db)
            await report_service.generate_report(scan_id)
        except Exception as e:
            logger.error(f"Failed to generate report for scan {scan_id}: {e}", exc_info=True)


@celery_app.task(name="tasks.generate_report_task")
def generate_report_task(scan_id: str) -> None:
    """
    Celery task to generate AI report, PDF, and send email.
    """
    logger.info(f"Received report generation task for scan ID {scan_id}")
    asyncio.run(generate_report_async(scan_id))
