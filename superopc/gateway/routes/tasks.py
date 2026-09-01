"""Task execution endpoints."""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

from superopc.core.task_manager import TaskStatus

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class ExecuteTaskRequest(BaseModel):
    """Request to execute a task."""
    agent_id: str
    skill: str
    action: str
    parameters: Dict[str, Any] = {}


@router.post("")
async def execute_task(
    req: ExecuteTaskRequest,
    request: Request,
    background_tasks: BackgroundTasks
):
    """Execute a skill task."""
    agent_manager = request.app.state.agent_manager
    executor = request.app.state.skill_executor
    task_manager = request.app.state.task_manager
    
    try:
        # Verify agent exists
        agent_sandbox = agent_manager.get_agent_sandbox(req.agent_id)
        if not agent_sandbox:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Create task
        task = task_manager.create_task(
            agent_id=req.agent_id,
            skill=req.skill,
            action=req.action,
            parameters=req.parameters
        )
        
        # Execute in background
        background_tasks.add_task(
            _execute_task_background,
            task.task_id,
            req.agent_id,
            agent_sandbox,
            req.skill,
            req.action,
            req.parameters,
            executor,
            task_manager
        )
        
        return {
            "task_id": task.task_id,
            "status": "queued",
            "message": "Task queued for execution"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}")
async def get_task(task_id: str, request: Request):
    """Get task status and result."""
    task_manager = request.app.state.task_manager
    
    task = task_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task.to_dict()


@router.get("")
async def list_tasks(
    agent_id: Optional[str] = None,
    request: Request = None
):
    """List tasks with optional filtering."""
    task_manager = request.app.state.task_manager
    
    tasks = task_manager.list_tasks(agent_id=agent_id)
    return {
        "tasks": [task.to_dict() for task in tasks.values()]
    }


async def _execute_task_background(
    task_id: str,
    agent_id: str,
    sandbox: Any,
    skill: str,
    action: str,
    parameters: Dict[str, Any],
    executor: Any,
    task_manager: Any
) -> None:
    """Execute task in background."""
    try:
        task_manager.update_task_status(task_id, TaskStatus.RUNNING)
        
        # Execute skill
        result = await executor.execute_skill(
            agent_id=agent_id,
            sandbox=sandbox,
            skill_name=skill,
            action=action,
            parameters=parameters
        )
        
        if result.get("success"):
            task_manager.update_task_status(
                task_id,
                TaskStatus.COMPLETED,
                result=result
            )
        else:
            task_manager.update_task_status(
                task_id,
                TaskStatus.FAILED,
                error=result.get("error", "Unknown error")
            )
    
    except Exception as e:
        logger.error(f"Background task failed: {e}")
        task_manager.update_task_status(
            task_id,
            TaskStatus.FAILED,
            error=str(e)
        )