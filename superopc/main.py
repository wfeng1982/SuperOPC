"""Main entry point for SuperOPC."""

import asyncio
from pathlib import Path
from loguru import logger

from superopc.config import settings
from superopc.gateway.app import create_app
from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager


async def main():
    """Start SuperOPC application."""
    
    # Setup logging
    settings.log_dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        settings.log_dir / "superopc.log",
        level=settings.log_level,
        rotation="500 MB",
        retention="7 days"
    )
    
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Workspace: {settings.workspace_root}")
    
    # Initialize workspace
    settings.workspace_root.mkdir(parents=True, exist_ok=True)
    (settings.workspace_root / "agents").mkdir(exist_ok=True)
    (settings.workspace_root / "storage").mkdir(exist_ok=True)
    (settings.workspace_root / "models").mkdir(exist_ok=True)
    
    # Initialize managers
    agent_manager = AgentManager(settings.workspace_root)
    browser_manager = BrowserManager()
    
    logger.info("✅ Agent manager initialized")
    logger.info("✅ Browser manager initialized")
    
    # Create and run FastAPI app
    app = create_app(agent_manager, browser_manager)
    
    import uvicorn
    config = uvicorn.Config(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
    server = uvicorn.Server(config)
    
    logger.info(f"🚀 Starting server at http://{settings.host}:{settings.port}")
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())