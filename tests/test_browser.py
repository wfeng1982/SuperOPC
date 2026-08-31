"""Tests for browser automation."""

import pytest
import asyncio
from superopc.core.browser.daemon import BrowserManager, BrowserSession


@pytest.mark.asyncio
async def test_session_creation():
    """Test browser session creation."""
    manager = BrowserManager()
    session = await manager.create_session("session_1", "agent_1")
    
    assert session.session_id == "session_1"
    assert session.agent_id == "agent_1"
    assert session.state == "initialized"


@pytest.mark.asyncio
async def test_domain_locking():
    """Test domain-level locking."""
    session = BrowserSession("session_1", "agent_1")
    
    # Acquire lock
    acquired = await session.acquire_lock(["amazon.com"], "domain")
    assert acquired is True
    assert "amazon.com" in session.locks
    
    # Try to acquire same lock again
    acquired2 = await session.acquire_lock(["amazon.com"], "domain")
    assert acquired2 is False
    
    # Release lock
    await session.release_lock()
    assert len(session.locks) == 0


@pytest.mark.asyncio
async def test_page_state_detection():
    """Test page state detection."""
    session = BrowserSession("session_1", "agent_1")
    state = await session.detect_page_state()
    
    assert state["state"] == "ok"
    assert state["confidence"] > 0