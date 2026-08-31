"""Agent sandbox isolation system."""

import sqlite3
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger


class AgentSandbox:
    """Isolated sandbox environment for each agent."""
    
    def __init__(self, agent_id: str, workspace_root: Path):
        """Initialize agent sandbox.
        
        Args:
            agent_id: Unique agent identifier
            workspace_root: Root workspace directory
        """
        self.agent_id = agent_id
        self.workspace_root = workspace_root
        self.sandbox_dir = workspace_root / "agents" / agent_id
        
        # Create directory structure
        self._setup_directories()
        logger.info(f"✅ Sandbox initialized for agent: {agent_id}")
    
    def _setup_directories(self) -> None:
        """Setup isolated directory structure."""
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        (self.sandbox_dir / "skills").mkdir(exist_ok=True)
        (self.sandbox_dir / "sandboxes").mkdir(exist_ok=True)
        (self.sandbox_dir / "memories").mkdir(exist_ok=True)
        (self.sandbox_dir / "data").mkdir(exist_ok=True)
        (self.sandbox_dir / "logs").mkdir(exist_ok=True)
    
    @property
    def db_path(self) -> Path:
        """Get isolated database path."""
        return self.sandbox_dir / "state.db"
    
    @property
    def skills_dir(self) -> Path:
        """Get isolated skills directory."""
        return self.sandbox_dir / "skills"
    
    @property
    def execution_dir(self) -> Path:
        """Get isolated execution directory."""
        return self.sandbox_dir / "sandboxes"
    
    @property
    def memories_dir(self) -> Path:
        """Get isolated memories directory."""
        return self.sandbox_dir / "memories"
    
    @property
    def data_dir(self) -> Path:
        """Get isolated data directory."""
        return self.sandbox_dir / "data"
    
    @property
    def logs_dir(self) -> Path:
        """Get isolated logs directory."""
        return self.sandbox_dir / "logs"
    
    def get_db_connection(self) -> sqlite3.Connection:
        """Get isolated database connection.
        
        Returns:
            SQLite connection for this agent
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.isolation_level = None
        return conn
    
    def init_db(self) -> None:
        """Initialize database schema."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data JSON
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                skill TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                result JSON,
                error TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS browser_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                action TEXT NOT NULL,
                url TEXT,
                status TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Database initialized for agent: {self.agent_id}")
    
    def clear(self) -> None:
        """Clear sandbox data (keeps structure)."""
        if self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)
        self._setup_directories()
        logger.warning(f"🗑️ Sandbox cleared for agent: {self.agent_id}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get sandbox information."""
        return {
            "agent_id": self.agent_id,
            "sandbox_dir": str(self.sandbox_dir),
            "db_path": str(self.db_path),
            "skills_dir": str(self.skills_dir),
            "data_dir": str(self.data_dir)
        }