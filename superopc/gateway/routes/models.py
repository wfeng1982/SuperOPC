"""Model management endpoints."""

from fastapi import APIRouter, HTTPException, Request
from loguru import logger

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("/providers")
async def list_providers(request: Request):
    """List available model providers."""
    # Will be implemented with actual model provider
    return {
        "providers": [
            "ollama",
            "openai",
            "deepseek",
            "anthropic"
        ]
    }


@router.get("/providers/{provider}/models")
async def list_models(provider: str, request: Request):
    """List models for provider."""
    # Will be implemented with actual model provider
    return {
        "provider": provider,
        "models": []
    }