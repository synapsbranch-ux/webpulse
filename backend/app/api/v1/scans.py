from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.scan import Scan
from app.models.scan_result import ScanResult
from app.schemas.scan import ScanCreate, ScanSchema
from app.workers.tasks import run_scan_task

router = APIRouter()

@router.post("", response_model=ScanSchema, status_code=status.HTTP_201_CREATED)
async def create_scan(
    scan_in: ScanCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Start a new scan for the given URL.
    Returns immediately with the Scan ID, the analysis runs in the background.
    """
    scan = Scan(
        user_id=current_user.id,
        url=str(scan_in.url)
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    
    # Trigger Celery Task
    run_scan_task.delay(str(scan.id))
    
    return scan

@router.get("", response_model=list[ScanSchema])
async def list_scans(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve all scans for the current user.
    """
    statement = select(Scan).where(Scan.user_id == current_user.id).offset(skip).limit(limit).order_by(Scan.created_at.desc())
    result = await db.execute(statement)
    scans = result.scalars().all()
    return scans

@router.get("/{scan_id}", response_model=ScanSchema)
async def get_scan(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get details of a specific scan by ID.
    """
    scan = await db.get(Scan, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return scan

@router.delete("/{scan_id}", response_model=dict)
async def delete_scan(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete a scan by ID.
    """
    scan = await db.get(Scan, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    await db.delete(scan)
    await db.commit()
    return {"message": "Scan deleted successfully"}

# A more specific query to grab results if the user needs them straight from API, 
# although Report usually aggregates this.
@router.get("/{scan_id}/results", response_model=list[dict])
async def get_scan_results(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get the detailed raw results of each module for a specific scan.
    """
    scan = await db.get(Scan, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    statement = select(ScanResult).where(ScanResult.scan_id == scan_id)
    result = await db.execute(statement)
    results = result.scalars().all()
    
    # We return raw dicts for simplicity in this endpoint as schemas could be complex
    return [{"module": r.module, "score": r.score, "grade": r.grade, "data": r.data, "issues": {"critical": r.issues_critical, "high": r.issues_high, "medium": r.issues_medium, "low": r.issues_low}} for r in results]
