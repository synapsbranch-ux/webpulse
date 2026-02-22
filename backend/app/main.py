from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Plateforme d'analyse web automatisée",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI → http://localhost:8000/docs
    redoc_url="/redoc",       # ReDoc → http://localhost:8000/redoc
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "WebPulse API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}