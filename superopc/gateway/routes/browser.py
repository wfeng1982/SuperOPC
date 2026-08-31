"""Browser automation endpoints."""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from loguru import logger

router = APIRouter(prefix="/api/browser", tags=["browser"])


class CreateSessionRequest(BaseModel):
    """Request to create browser session."""
    session_id: str
    agent_id: str


class AcquireLockRequest(BaseModel):
    """Request to acquire domain lock."""
    domains: List[str]
    concurrency_policy: str = "domain"


@router.post("/sessions")
async def create_session(req: CreateSessionRequest, request: Request):
    """Create browser session."""
    manager = request.app.state.browser_manager
    
    try:
        session = await manager.create_session(req.session_id, req.agent_id)
        return {
            "session_id": req.session_id,
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions")
async def list_sessions(request: Request):
    """List active browser sessions."""
    manager = request.app.state.browser_manager
    return {"sessions": manager.list_sessions()}


@router.post("/sessions/{session_id}/lock")
async def acquire_lock(
    session_id: str,
    req: AcquireLockRequest,
    request: Request
):
    """Acquire domain locks for session."""
    manager = request.app.state.browser_manager
    session = manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    acquired = await session.acquire_lock(
        req.domains,
        req.concurrency_policy
    )
    
    return {
        "session_id": session_id,
        "acquired": acquired,
        "domains": req.domains
    }


@router.post("/sessions/{session_id}/unlock")
async def release_lock(
    session_id: str,
    close_browser: bool = False,
    request: Request = None
):
    """Release domain locks for session."""
    manager = request.app.state.browser_manager
    session = manager.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await session.release_lock(close_browser)
    
    return {
        "session_id": session_id,
        "status": "unlocked"
    }


@router.delete("/sessions/{session_id}")
async def close_session(session_id: str, request: Request):
    """Close browser session."""
    manager = request.app.state.browser_manager
    
    if await manager.close_session(session_id):
        return {"status": "closed", "session_id": session_id}
    else:
        raise HTTPException(status_code=404, detail="Session not found")