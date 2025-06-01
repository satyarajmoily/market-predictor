"""Configuration settings for the Market Predictor service."""

import os
from functools import lru_cache
from typing import Optional
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Application settings with environment variable support - ALL VALUES REQUIRED FROM .env"""
    
    def __init__(self, **kwargs):
        """Initialize settings and validate .env file exists"""
        # Find .env file in project root (works in Docker and local)
        env_file = Path(__file__).parent.parent.parent.parent / ".env"
        
        if not env_file.exists():
            raise FileNotFoundError(f"❌ CRITICAL: .env file not found at {env_file}")
        
        # Load environment variables
        load_dotenv(env_file)
        
        super().__init__(**kwargs)
        
        # Validate all required settings are present
        self._validate_required_settings()
    
    def _validate_required_settings(self):
        """Validate that all required settings are present in environment"""
        required_vars = [
            'ENVIRONMENT', 'LOG_LEVEL', 'API_HOST', 'API_PORT',
            'SERVICE_NAME', 'MODEL_TYPE', 'CACHE_TTL', 
            'METRICS_ENABLED', 'HEALTH_CHECK_INTERVAL',
            'REQUEST_TIMEOUT', 'MAX_CONCURRENT_REQUESTS'
        ]
        
        missing = []
        for var in required_vars:
            if os.getenv(var) is None:
                missing.append(var)
        
        if missing:
            raise ValueError(f"❌ REQUIRED: The following environment variables must be set in .env file: {', '.join(missing)}")
    
    # Application settings - NO DEFAULTS, ALL REQUIRED
    environment: str = Field(description="Environment name")
    log_level: str = Field(description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")
    
    # API settings - NO DEFAULTS, ALL REQUIRED  
    api_host: str = Field(description="API host")
    api_port: int = Field(description="API port")
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    
    # Service settings - NO DEFAULTS, ALL REQUIRED
    service_name: str = Field(description="Service name")
    service_version: str = Field(default="0.1.0", description="Service version")
    
    # Model settings - NO DEFAULTS, ALL REQUIRED
    model_type: str = Field(description="Prediction model type")
    cache_ttl: int = Field(description="Cache TTL in seconds")
    
    # Monitoring settings - NO DEFAULTS, ALL REQUIRED
    metrics_enabled: bool = Field(description="Enable Prometheus metrics")
    health_check_interval: int = Field(description="Health check interval")
    
    # Request timeout settings - NO DEFAULTS, ALL REQUIRED
    request_timeout: int = Field(description="Request timeout in seconds")
    max_concurrent_requests: int = Field(description="Max concurrent requests")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False
        extra = "forbid"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()