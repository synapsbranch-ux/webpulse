from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.scans import router as scans_router
from app.api.v1.reports import router as reports_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(scans_router, prefix="/scans", tags=["scans"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
