"""Base skill class."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from loguru import logger


class BaseSkill(ABC):
    """Base class for all skills."""
    
    name: str = "base_skill"
    description: str = "Base skill"
    version: str = "1.0.0"
    
    def __init__(self, browser_manager=None, model_provider=None, sandbox=None):
        """Initialize skill.
        
        Args:
            browser_manager: Browser manager instance
            model_provider: Model provider instance
            sandbox: Agent sandbox instance
        """
        self.browser = browser_manager
        self.models = model_provider
        self.sandbox = sandbox
        logger.info(f"✅ Skill initialized: {self.name} v{self.version}")
    
    @abstractmethod
    async def execute(self, action: str, **params) -> Dict[str, Any]:
        """Execute skill action.
        
        Args:
            action: Action name
            **params: Action parameters
        
        Returns:
            Action result
        """
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """Get skill information.
        
        Returns:
            Skill metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }