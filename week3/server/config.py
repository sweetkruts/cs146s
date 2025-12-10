from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://127.0.0.1:8000/auth/callback"
    
    mcp_api_key: str
    
    log_level: str = "INFO"
    log_file: str = "mcp_server.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def validate_config(self) -> None:
        if not self.spotify_client_id or self.spotify_client_id == "your_spotify_client_id_here":
            raise ValueError("SPOTIFY_CLIENT_ID must be set in .env file")
        if not self.spotify_client_secret or self.spotify_client_secret == "your_spotify_client_secret_here":
            raise ValueError("SPOTIFY_CLIENT_SECRET must be set in .env file")
        if not self.mcp_api_key or self.mcp_api_key == "your_secure_random_key_here":
            raise ValueError("MCP_API_KEY must be set in .env file")

settings = Settings()

