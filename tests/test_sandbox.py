"""Tests for agent sandbox isolation."""

import pytest
from pathlib import Path
import tempfile
from superopc.core.agent.sandbox import AgentSandbox


@pytest.fixture
def temp_workspace():
    """Create temporary workspace."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_sandbox_creation(temp_workspace):
    """Test sandbox creation."""
    sandbox = AgentSandbox("test_agent", temp_workspace)
    
    assert sandbox.agent_id == "test_agent"
    assert sandbox.sandbox_dir.exists()
    assert sandbox.skills_dir.exists()
    assert sandbox.execution_dir.exists()


def test_database_isolation(temp_workspace):
    """Test database isolation."""
    sandbox1 = AgentSandbox("agent1", temp_workspace)
    sandbox2 = AgentSandbox("agent2", temp_workspace)
    
    sandbox1.init_db()
    sandbox2.init_db()
    
    assert sandbox1.db_path != sandbox2.db_path
    assert sandbox1.db_path.exists()
    assert sandbox2.db_path.exists()


def test_sandbox_info(temp_workspace):
    """Test sandbox info."""
    sandbox = AgentSandbox("test_agent", temp_workspace)
    info = sandbox.get_info()
    
    assert info["agent_id"] == "test_agent"
    assert "sandbox_dir" in info
    assert "db_path" in info