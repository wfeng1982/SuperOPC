"""Configuration management for SuperOPC."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """SuperOPC configuration settings."""
    
    # Application
    app_name: str = "SuperOPC"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    
    # Workspace
    workspace_root: Path = Path.home() / ".superopc"
    
    # Browser
    browser_port: int = 12321
    browser_ws_port: int = 22321
    headless: bool = True
    
    # Database
    db_url: str = "sqlite:///superopc.db"
    db_echo: bool = False
    
    # Models
    default_model_provider: str = "ollama"
    default_model_name: str = "mistral"
    ollama_base_url: str = "http://localhost:11434"
    openai_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_dir: Path = Path.home() / ".superopc" / "logs"
    
    # Features
    enable_browser_automation: bool = True
    enable_rag: bool = True
    enable_scheduling: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()