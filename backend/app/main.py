import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.api.v1.router import api_router
from app.websocket.manager import ws_manager

# Note: We rely on Alembic for DB migrations, 
# but we could optionally create tables here if desired.

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure static dirs exist
    import os
    os.makedirs("static/reports", exist_ok=True)
    logger.info("Starting up Synapsbranch backend...")
    yield
    # Shutdown
    logger.info("Shutting down Synapsbranch backend...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Synapsbranch web analysis platform.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS configuration
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

import os
os.makedirs("static/reports", exist_ok=True)

# Static files for PDF reports
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket Route
@app.websocket("/ws/scan/{scan_id}")
async def websocket_endpoint(websocket, scan_id: str):
    await ws_manager.connect(scan_id, websocket)

# Healthcheck
@app.get("/", tags=["Health"])
async def root():
    return {
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
        "status": "online"
    }

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}