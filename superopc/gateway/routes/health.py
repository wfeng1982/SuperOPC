"""Health check endpoints."""

from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/")
async def root(request: Request):
    """Root endpoint."""
    return {
        "name": "SuperOPC",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }