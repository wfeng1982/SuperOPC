"""Agent management endpoints."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger

router = APIRouter(prefix="/api/agents", tags=["agents"])


class CreateAgentRequest(BaseModel):
    """Request to create agent."""
    agent_id: str
    name: str
    model_provider: str = "ollama"
    model_name: str = "mistral"
    skills: list[str] = []


@router.post("")
async def create_agent(req: CreateAgentRequest, request: Request):
    """Create a new agent."""
    manager = request.app.state.agent_manager
    
    try:
        sandbox = manager.create_agent(
            req.agent_id,
            req.dict()
        )
        return {
            "agent_id": req.agent_id,
            "status": "created",
            "sandbox": sandbox.get_info()
        }
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{agent_id}")
async def get_agent(agent_id: str, request: Request):
    """Get agent information."""
    manager = request.app.state.agent_manager
    info = manager.get_agent_info(agent_id)
    
    if not info:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return info


@router.get("")
async def list_agents(request: Request):
    """List all agents."""
    manager = request.app.state.agent_manager
    return {"agents": manager.list_agents()}


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, request: Request):
    """Delete an agent."""
    manager = request.app.state.agent_manager
    
    if manager.delete_agent(agent_id):
        return {"status": "deleted", "agent_id": agent_id}
    else:
        raise HTTPException(status_code=404, detail="Agent not found")