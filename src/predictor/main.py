"""Main FastAPI application for Market Predictor service."""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from predictor.config.settings import get_settings
from predictor.models.health import DetailedStatus, HealthStatus

# Global variable to track application start time
app_start_time = time.time()

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])
SERVICE_HEALTH_CHECK = Counter('service_health_checks_total', 'Total health checks performed')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    settings = get_settings()
    print(f"🚀 Starting {settings.service_name} v{settings.service_version}")
    print(f"🌍 Environment: {settings.environment}")
    print(f"📡 API will be available at http://{settings.api_host}:{settings.api_port}")
    print(f"📊 Metrics available at /metrics")
    
    yield
    
    print(f"🛑 Shutting down {settings.service_name}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="Market Predictor",
        description="Bitcoin Price Prediction Service",
        version=settings.service_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health endpoints
    @app.get("/health", response_model=HealthStatus, tags=["Health"])
    async def health():
        """Health check endpoint for monitoring systems."""
        SERVICE_HEALTH_CHECK.inc()
        REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
        
        return HealthStatus(
            status="healthy",
            service=settings.service_name,
            version=settings.service_version
        )
    
    @app.get("/status", response_model=DetailedStatus, tags=["Health"])
    async def status():
        """Detailed status endpoint with comprehensive service information."""
        REQUEST_COUNT.labels(method="GET", endpoint="/status", status="200").inc()
        
        uptime = time.time() - app_start_time
        
        return DetailedStatus(
            status="healthy",
            service=settings.service_name,
            version=settings.service_version,
            uptime_seconds=uptime,
            components={
                "api": "healthy",
                "configuration": "healthy",
                "metrics": "healthy"
            },
            metadata={
                "environment": settings.environment,
                "model_type": "dummy",
                "cache_ttl": str(settings.cache_ttl),
                "metrics_enabled": str(settings.metrics_enabled)
            }
        )
    
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with service information."""
        return {
            "service": settings.service_name,
            "version": settings.service_version,
            "status": "running",
            "docs_url": "/docs",
            "health_url": "/health",
            "status_url": "/status"
        }
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    return app


# Create the FastAPI application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    from predictor.config.settings import get_settings
    
    settings = get_settings()
    uvicorn.run(
        "predictor.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )