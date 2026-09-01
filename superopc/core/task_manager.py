"""Task execution and result management."""

from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
import uuid
from loguru import logger


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Represents a task to be executed."""
    
    def __init__(
        self,
        agent_id: str,
        skill: str,
        action: str,
        parameters: Dict[str, Any]
    ):
        """Initialize task.
        
        Args:
            agent_id: Agent to execute task
            skill: Skill name
            action: Action to execute
            parameters: Action parameters
        """
        self.task_id = str(uuid.uuid4())
        self.agent_id = agent_id
        self.skill = skill
        self.action = action
        self.parameters = parameters
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary.
        
        Returns:
            Task as dictionary
        """
        return {
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "skill": self.skill,
            "action": self.action,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


class TaskManager:
    """Manages task execution and lifecycle."""
    
    def __init__(self):
        """Initialize task manager."""
        self.tasks: Dict[str, Task] = {}
        logger.info("📋 Task manager initialized")
    
    def create_task(
        self,
        agent_id: str,
        skill: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> Task:
        """Create a new task.
        
        Args:
            agent_id: Agent to execute task
            skill: Skill name
            action: Action to execute
            parameters: Action parameters
        
        Returns:
            Created task
        """
        task = Task(agent_id, skill, action, parameters)
        self.tasks[task.task_id] = task
        
        logger.info(f"✅ Task created: {task.task_id}")
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Task or None
        """
        return self.tasks.get(task_id)
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> bool:
        """Update task status.
        
        Args:
            task_id: Task identifier
            status: New status
            result: Execution result
            error: Error message
        
        Returns:
            True if successful
        """
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.status = status
        
        if status == TaskStatus.RUNNING:
            task.started_at = datetime.now()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            task.completed_at = datetime.now()
        
        if result:
            task.result = result
        if error:
            task.error = error
        
        logger.info(f"📊 Task {task_id} -> {status.value}")
        return True
    
    def list_tasks(
        self,
        agent_id: Optional[str] = None,
        status: Optional[TaskStatus] = None
    ) -> Dict[str, Task]:
        """List tasks with optional filtering.
        
        Args:
            agent_id: Filter by agent
            status: Filter by status
        
        Returns:
            Dictionary of tasks
        """
        results = {}
        
        for task_id, task in self.tasks.items():
            if agent_id and task.agent_id != agent_id:
                continue
            if status and task.status != status:
                continue
            results[task_id] = task
        
        return results