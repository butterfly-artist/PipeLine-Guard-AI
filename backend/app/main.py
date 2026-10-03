from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api import health, analyze, profile, rules

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["Health"])
app.include_router(analyze.router, prefix=settings.api_v1_prefix, tags=["Analysis"])
app.include_router(profile.router, prefix=settings.api_v1_prefix, tags=["Profiling"])
app.include_router(rules.router, prefix=settings.api_v1_prefix, tags=["Rules"])


@app.get("/")
def root():
    return {
        "message": "Welcome to PipeGuard AI API",
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health",
        "demo": f"{settings.api_v1_prefix}/demo"
    }
