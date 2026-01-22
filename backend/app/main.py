"""FastAPI application main module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import etf, simulation
from app.core.config import settings
from app.db.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="ETF Investment Simulator Backend API",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(etf.router, prefix=settings.api_v1_prefix)
app.include_router(simulation.router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "ETF Investment Simulator API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
