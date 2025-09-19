"""
Application settings module.

This module handles all application configuration including environment variables,
database settings, JWT secrets, and other application-wide settings.
It provides a centralized way to manage configuration across different environments
(development, staging, production) using Pydantic settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database Configuration
    database_url: str = Field(..., env="DATABASE_URL")
    
    # JWT Configuration
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Application Configuration
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    api_v1_str: str = Field(default="/api/v1", env="API_V1_STR")
    
    # CORS Configuration
    allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        env="ALLOWED_ORIGINS"
    )
    
    # Email Configuration (for future use)
    smtp_host: Optional[str] = Field(default=None, env="SMTP_HOST")
    smtp_port: Optional[int] = Field(default=None, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # Redis Configuration (for future use)
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
