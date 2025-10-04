"""
Application configuration management.

Centralizes all configuration settings with environment variable support
and sensible defaults. Supports different configurations for dev/test/prod.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


class Settings:
    """
    Application settings with environment variable support.
    
    Environment variables can override defaults (prefix: APP_).
    Example: APP_DATABASE_PATH=/custom/path/db.sqlite
    """

    def __init__(self) -> None:
        """Initialize settings from environment variables."""
        # Application
        self.app_name: str = os.getenv("APP_NAME", "Action Item Extractor")
        self.debug: bool = os.getenv("APP_DEBUG", "false").lower() in ("true", "1", "yes")
        self.environment: str = os.getenv("APP_ENVIRONMENT", "development")

        # Database
        self.database_path: Optional[str] = os.getenv("APP_DATABASE_PATH")
        
        # LLM Configuration
        self.ollama_model: str = os.getenv("APP_OLLAMA_MODEL", "llama3.1:8b")
        self.ollama_temperature: float = float(os.getenv("APP_OLLAMA_TEMPERATURE", "0.1"))
        
        # API Configuration
        self.api_prefix: str = os.getenv("APP_API_PREFIX", "")
        cors_origins_str = os.getenv("APP_CORS_ORIGINS", "*")
        self.cors_origins: list[str] = [
            origin.strip() for origin in cors_origins_str.split(",")
        ]

    def get_database_path(self) -> Path:
        """
        Get the database file path.
        
        Returns the configured path or default location in week2/data/app.db
        """
        if self.database_path:
            return Path(self.database_path)
        
        # Default: week2/data/app.db relative to app directory
        base_dir = Path(__file__).resolve().parent.parent
        return base_dir / "data" / "app.db"
    
    def get_data_dir(self) -> Path:
        """Get the data directory path."""
        return self.get_database_path().parent


# Global settings instance
settings = Settings()

