"""Task scheduling system."""

from typing import Dict, Optional, Any, Callable
from datetime import datetime
from loguru import logger


class TaskScheduler:
    """Manages scheduled tasks and cron jobs."""
    
    def __init__(self):
        """Initialize task scheduler."""
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.workflows: Dict[str, Dict[str, Any]] = {}
        logger.info("⏰ Task scheduler initialized")
    
    def add_cron_task(
        self,
        task_id: str,
        agent_id: str,
        skill: str,
        action: str,
        cron_expression: str,
        parameters: Dict[str, Any]
    ) -> bool:
        """Add cron-based scheduled task.
        
        Args:
            task_id: Unique task ID
            agent_id: Agent to execute task
            skill: Skill name
            action: Action to execute
            cron_expression: Cron expression (e.g., "0 9 * * MON")
            parameters: Action parameters
        
        Returns:
            True if successful
        """
        try:
            self.tasks[task_id] = {
                "agent_id": agent_id,
                "skill": skill,
                "action": action,
                "cron": cron_expression,
                "parameters": parameters,
                "created_at": datetime.now(),
                "last_run": None,
                "next_run": None,
                "status": "scheduled"
            }
            
            logger.info(f"✅ Task scheduled: {task_id} ({cron_expression})")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to schedule task: {e}")
            return False
    
    def add_workflow(
        self,
        workflow_id: str,
        steps: list,
        cron_expression: str
    ) -> bool:
        """Add multi-step workflow.
        
        Args:
            workflow_id: Unique workflow ID
            steps: List of workflow steps
            cron_expression: Cron expression
        
        Returns:
            True if successful
        """
        try:
            self.workflows[workflow_id] = {
                "steps": steps,
                "cron": cron_expression,
                "created_at": datetime.now(),
                "last_run": None,
                "status": "scheduled"
            }
            
            logger.info(f"✅ Workflow scheduled: {workflow_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to schedule workflow: {e}")
            return False
    
    def list_tasks(self) -> Dict[str, Dict[str, Any]]:
        """List all scheduled tasks.
        
        Returns:
            Dictionary of tasks
        """
        return self.tasks.copy()
    
    def list_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List all workflows.
        
        Returns:
            Dictionary of workflows
        """
        return self.workflows.copy()
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task details.
        
        Args:
            task_id: Task ID
        
        Returns:
            Task details or None
        """
        return self.tasks.get(task_id)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a scheduled task.
        
        Args:
            task_id: Task ID
        
        Returns:
            True if successful
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            logger.info(f"✅ Task deleted: {task_id}")
            return True
        return False