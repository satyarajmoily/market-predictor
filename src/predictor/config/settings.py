"""Configuration settings for the Market Predictor service."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    environment: str = Field(default="development", description="Environment name")
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    
    # Service settings
    service_name: str = Field(default="market-predictor", description="Service name")
    service_version: str = Field(default="0.1.0", description="Service version")
    
    # Model settings
    model_type: str = Field(default="dummy", description="Prediction model type")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    
    # Monitoring settings
    metrics_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    health_check_interval: int = Field(default=30, description="Health check interval")
    
    # Request timeout settings
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    max_concurrent_requests: int = Field(default=100, description="Max concurrent requests")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False
        extra = "forbid"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()