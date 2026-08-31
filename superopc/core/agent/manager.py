"""Agent lifecycle management."""

from pathlib import Path
from typing import Dict, Optional, Any
from loguru import logger

from superopc.core.agent.sandbox import AgentSandbox


class AgentManager:
    """Manages agent creation, lifecycle, and sandboxes."""
    
    def __init__(self, workspace_root: Path):
        """Initialize agent manager.
        
        Args:
            workspace_root: Root workspace directory
        """
        self.workspace_root = workspace_root
        self.sandboxes: Dict[str, AgentSandbox] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}
    
    def create_agent(
        self,
        agent_id: str,
        config: Dict[str, Any]
    ) -> AgentSandbox:
        """Create a new isolated agent.
        
        Args:
            agent_id: Unique agent identifier
            config: Agent configuration
        
        Returns:
            AgentSandbox instance
        """
        if agent_id in self.sandboxes:
            logger.warning(f"Agent {agent_id} already exists")
            return self.sandboxes[agent_id]
        
        # Create sandbox
        sandbox = AgentSandbox(agent_id, self.workspace_root)
        sandbox.init_db()
        
        self.sandboxes[agent_id] = sandbox
        self.agents[agent_id] = config
        
        logger.info(f"✅ Agent created: {agent_id}")
        return sandbox
    
    def get_agent_sandbox(self, agent_id: str) -> Optional[AgentSandbox]:
        """Get sandbox for specific agent.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            AgentSandbox or None if not found
        """
        if agent_id not in self.sandboxes:
            sandbox_path = self.workspace_root / "agents" / agent_id
            if sandbox_path.exists():
                self.sandboxes[agent_id] = AgentSandbox(agent_id, self.workspace_root)
            else:
                return None
        
        return self.sandboxes.get(agent_id)
    
    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all agents with their configurations.
        
        Returns:
            Dictionary of agent_id -> config
        """
        return self.agents.copy()
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent and its sandbox.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            True if successful
        """
        if agent_id in self.sandboxes:
            self.sandboxes[agent_id].clear()
            del self.sandboxes[agent_id]
        
        if agent_id in self.agents:
            del self.agents[agent_id]
        
        logger.info(f"✅ Agent deleted: {agent_id}")
        return True
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed agent information.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            Agent info or None
        """
        sandbox = self.get_agent_sandbox(agent_id)
        if not sandbox:
            return None
        
        return {
            "id": agent_id,
            "config": self.agents.get(agent_id),
            "sandbox": sandbox.get_info()
        }