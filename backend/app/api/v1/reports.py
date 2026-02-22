from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.scan import Scan
from app.models.report import Report
from app.schemas.report import ReportSchema
from app.services.email_service import EmailService

router = APIRouter()

@router.get("/{scan_id}", response_model=ReportSchema)
async def get_report(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the AI analysis/report JSON for a specific scan.
    """
    scan = await db.get(Scan, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    statement = select(Report).where(Report.scan_id == scan_id)
    result = await db.execute(statement)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not generated yet")
        
    return report

@router.get("/{scan_id}/download")
async def download_report_pdf(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Download the generated PDF report.
    """
    scan = await db.get(Scan, scan_id)
    if not scan or scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    statement = select(Report).where(Report.scan_id == scan_id)
    result = await db.execute(statement)
    report = result.scalar_one_or_none()
    
    if not report or not report.pdf_path:
        raise HTTPException(status_code=404, detail="PDF not found")
        
    return FileResponse(
        path=report.pdf_path, 
        filename=f"synapsbranch_report_{scan_id}.pdf",
        media_type="application/pdf"
    )

@router.post("/{scan_id}/email")
async def send_report_email_endpoint(
    scan_id: UUID,
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Manually trigger sending the report via email.
    """
    scan = await db.get(Scan, scan_id)
    if not scan or scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    statement = select(Report).where(Report.scan_id == scan_id)
    result = await db.execute(statement)
    report = result.scalar_one_or_none()
    
    if not report or not report.pdf_path:
        raise HTTPException(status_code=404, detail="Report not generated yet, wait a moment.")
    
    try:
        email_service = EmailService()
        await email_service.send_report_email(
            email=email,
            user_name=current_user.name or "Utilisateur",
            scan_url=scan.url,
            score=scan.overall_score or 0,
            pdf_path=report.pdf_path
        )
        
        # Update db to reflect email sent
        report.email_sent = True
        report.email_sent_at = select.func.now()
        db.add(report)
        await db.commit()
        
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
