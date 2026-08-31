"""Browser automation daemon."""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from loguru import logger


@dataclass
class BrowserSession:
    """Browser session management."""
    
    session_id: str
    agent_id: str
    created_at: datetime = field(default_factory=datetime.now)
    tabs: Dict[str, Any] = field(default_factory=lambda: {"main": None})
    locks: Dict[str, float] = field(default_factory=dict)
    page_semantics: Dict[str, Any] = field(default_factory=dict)
    state: str = "initialized"
    
    async def acquire_lock(
        self,
        domains: List[str],
        concurrency_policy: str = "domain"
    ) -> bool:
        """Acquire domain-level locks.
        
        Args:
            domains: List of domains to lock
            concurrency_policy: "domain" for mutual exclusion
        
        Returns:
            True if lock acquired
        """
        current_time = time.time()
        
        if concurrency_policy == "domain":
            # Check if domains are already locked
            for domain in domains:
                if domain in self.locks:
                    # Release old locks after 1 hour
                    if current_time - self.locks[domain] > 3600:
                        del self.locks[domain]
                    else:
                        logger.warning(
                            f"Domain {domain} already locked for session {self.session_id}"
                        )
                        return False
            
            # Acquire locks
            for domain in domains:
                self.locks[domain] = current_time
            
            logger.info(f"✅ Locks acquired for {domains} in session {self.session_id}")
            return True
        
        return True
    
    async def release_lock(
        self,
        close_browser: bool = False
    ) -> None:
        """Release locks.
        
        Args:
            close_browser: Whether to close browser
        """
        self.locks.clear()
        
        if close_browser:
            self.state = "closed"
        
        logger.info(f"✅ Locks released for session {self.session_id}")
    
    async def detect_page_state(self) -> Dict[str, Any]:
        """Detect current page state.
        
        Returns:
            Page state information
        """
        # Placeholder for actual page state detection
        return {
            "state": "ok",
            "confidence": 0.95,
            "reason": "Page loaded successfully",
            "suggested_action": "continue",
            "signals": [],
            "evidence": {}
        }
    
    async def request_help(
        self,
        title: str,
        prompt: str,
        timeout_ms: int = 300000
    ) -> Dict[str, Any]:
        """Request human intervention.
        
        Args:
            title: Help title
            prompt: Help prompt
            timeout_ms: Timeout in milliseconds
        
        Returns:
            Result of human intervention
        """
        return {
            "status": "waiting_for_user",
            "title": title,
            "prompt": prompt,
            "timeout_ms": timeout_ms,
            "created_at": datetime.now().isoformat()
        }


class BrowserManager:
    """Manages browser sessions and automation."""
    
    def __init__(self):
        """Initialize browser manager."""
        self.sessions: Dict[str, BrowserSession] = {}
        logger.info("🌐 Browser manager initialized")
    
    async def create_session(
        self,
        session_id: str,
        agent_id: str
    ) -> BrowserSession:
        """Create a new browser session.
        
        Args:
            session_id: Unique session ID
            agent_id: Associated agent ID
        
        Returns:
            BrowserSession instance
        """
        if session_id in self.sessions:
            logger.warning(f"Session {session_id} already exists")
            return self.sessions[session_id]
        
        session = BrowserSession(session_id=session_id, agent_id=agent_id)
        self.sessions[session_id] = session
        
        logger.info(f"✅ Browser session created: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[BrowserSession]:
        """Get browser session.
        
        Args:
            session_id: Session ID
        
        Returns:
            BrowserSession or None
        """
        return self.sessions.get(session_id)
    
    async def close_session(self, session_id: str) -> bool:
        """Close browser session.
        
        Args:
            session_id: Session ID
        
        Returns:
            True if successful
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            await session.release_lock(close_browser=True)
            del self.sessions[session_id]
            logger.info(f"✅ Session closed: {session_id}")
            return True
        
        return False
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions.
        
        Returns:
            List of session info
        """
        return [
            {
                "session_id": session.session_id,
                "agent_id": session.agent_id,
                "state": session.state,
                "created_at": session.created_at.isoformat(),
                "locked_domains": list(session.locks.keys())
            }
            for session in self.sessions.values()
        ]