"""Skill executor - runs skills with proper context and error handling."""

from typing import Dict, Any, Optional
import importlib
from loguru import logger

from superopc.skills.base import BaseSkill
from superopc.core.agent.sandbox import AgentSandbox
from superopc.core.browser.daemon import BrowserManager
from superopc.core.models.provider import ModelProvider


class SkillExecutor:
    """Executes skills with proper isolation and context."""
    
    def __init__(
        self,
        browser_manager: BrowserManager,
        model_provider: ModelProvider
    ):
        """Initialize skill executor.
        
        Args:
            browser_manager: Browser manager instance
            model_provider: Model provider instance
        """
        self.browser = browser_manager
        self.models = model_provider
        self.loaded_skills: Dict[str, BaseSkill] = {}
        logger.info("⚙️  Skill executor initialized")
    
    async def execute_skill(
        self,
        agent_id: str,
        sandbox: AgentSandbox,
        skill_name: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a skill action.
        
        Args:
            agent_id: Agent identifier
            sandbox: Agent sandbox
            skill_name: Skill name
            action: Action to execute
            parameters: Action parameters
        
        Returns:
            Execution result
        """
        try:
            logger.info(f"🚀 Executing: {agent_id}/{skill_name}.{action}")
            
            # Load or get cached skill
            skill = await self._load_skill(
                skill_name,
                sandbox
            )
            
            if not skill:
                return {
                    "success": False,
                    "error": f"Skill not found: {skill_name}"
                }
            
            # Execute action
            result = await skill.execute(action, **parameters)
            
            logger.info(f"✅ Skill executed: {skill_name}.{action}")
            return result
        
        except Exception as e:
            logger.error(f"❌ Skill execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _load_skill(
        self,
        skill_name: str,
        sandbox: AgentSandbox
    ) -> Optional[BaseSkill]:
        """Load skill instance.
        
        Args:
            skill_name: Skill name
            sandbox: Agent sandbox
        
        Returns:
            Skill instance or None
        """
        # Check cache
        cache_key = f"{sandbox.agent_id}:{skill_name}"
        if cache_key in self.loaded_skills:
            return self.loaded_skills[cache_key]
        
        # Map skill names to modules
        skill_map = {
            "amazon_automation": "superopc.skills.ecommerce.amazon:AmazonSkill",
            "amazon_search": "superopc.skills.ecommerce.amazon:AmazonSkill",
            "amazon_details": "superopc.skills.ecommerce.amazon:AmazonSkill",
        }
        
        if skill_name not in skill_map:
            logger.warning(f"⚠️  Unknown skill: {skill_name}")
            return None
        
        # Parse module and class
        spec = skill_map[skill_name]
        module_path, class_name = spec.split(":")
        
        try:
            # Import module
            module = importlib.import_module(module_path)
            skill_class = getattr(module, class_name)
            
            # Instantiate skill
            skill = skill_class(
                browser_manager=self.browser,
                model_provider=self.models,
                sandbox=sandbox
            )
            
            # Cache
            self.loaded_skills[cache_key] = skill
            
            logger.info(f"✅ Loaded skill: {skill_name}")
            return skill
        
        except Exception as e:
            logger.error(f"❌ Failed to load skill: {e}")
            return None
    
    def unload_skill(self, agent_id: str, skill_name: str) -> bool:
        """Unload a skill from cache.
        
        Args:
            agent_id: Agent identifier
            skill_name: Skill name
        
        Returns:
            True if successful
        """
        cache_key = f"{agent_id}:{skill_name}"
        if cache_key in self.loaded_skills:
            del self.loaded_skills[cache_key]
            logger.info(f"✅ Unloaded skill: {skill_name}")
            return True
        return False