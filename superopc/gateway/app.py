"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from superopc.config import settings
from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager
from superopc.gateway import routes


def create_app(
    agent_manager: AgentManager,
    browser_manager: BrowserManager
) -> FastAPI:
    """Create FastAPI application.
    
    Args:
        agent_manager: Agent manager instance
        browser_manager: Browser manager instance
    
    Returns:
        FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI Agent platform for e-commerce automation",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Store managers in app state
    app.state.agent_manager = agent_manager
    app.state.browser_manager = browser_manager
    
    # Include routes
    app.include_router(routes.agents.router)
    app.include_router(routes.browser.router)
    app.include_router(routes.models.router)
    app.include_router(routes.health.router)
    
    @app.on_event("startup")
    async def startup():
        logger.info("🚀 SuperOPC startup")
    
    @app.on_event("shutdown")
    async def shutdown():
        logger.info("🛑 SuperOPC shutdown")
    
    return app