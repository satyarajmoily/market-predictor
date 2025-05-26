"""Health check models for the Market Predictor service."""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class HealthStatus(BaseModel):
    """Basic health status response."""
    
    status: str = Field(..., description="Service health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


class DetailedStatus(BaseModel):
    """Detailed service status with components."""
    
    status: str = Field(..., description="Overall service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status check timestamp")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    components: Dict[str, str] = Field(default_factory=dict, description="Component health status")
    metadata: Optional[Dict[str, str]] = Field(default=None, description="Additional metadata")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    details: Optional[Dict] = Field(default=None, description="Additional error details")