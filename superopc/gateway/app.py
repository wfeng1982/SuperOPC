"""Updated FastAPI app with full routing."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from superopc.config import settings
from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager
from superopc.core.executor import SkillExecutor
from superopc.core.task_manager import TaskManager
from superopc.core.models.provider import ModelProvider
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
        description="AI Agent platform for e-commerce automation with enterprise-grade browser automation and sandbox isolation",
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
    
    # Initialize managers and executors
    model_provider = ModelProvider()
    skill_executor = SkillExecutor(browser_manager, model_provider)
    task_manager = TaskManager()
    
    # Store in app state
    app.state.agent_manager = agent_manager
    app.state.browser_manager = browser_manager
    app.state.model_provider = model_provider
    app.state.skill_executor = skill_executor
    app.state.task_manager = task_manager
    
    # Include routes
    app.include_router(routes.agents.router)
    app.include_router(routes.browser.router)
    app.include_router(routes.models.router)
    app.include_router(routes.tasks.router)
    app.include_router(routes.skills.router)
    app.include_router(routes.health.router)
    
    @app.on_event("startup")
    async def startup():
        logger.info(f"🚀 {settings.app_name} v{settings.app_version} starting")
        logger.info(f"📍 Host: {settings.host}:{settings.port}")
        logger.info(f"💾 Workspace: {settings.workspace_root}")
    
    @app.on_event("shutdown")
    async def shutdown():
        logger.info("🛑 Application shutdown")
    
    return app