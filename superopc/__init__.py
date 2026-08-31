"""SuperOPC - Open-source AI Agent platform for e-commerce automation."""

__version__ = "0.1.0"
__author__ = "SuperOPC Contributors"

from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager
from superopc.core.models.provider import ModelProvider

__all__ = [
    "AgentManager",
    "BrowserManager",
    "ModelProvider",
]