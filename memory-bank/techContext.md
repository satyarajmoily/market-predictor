# Technical Context - Market Predictor

## Technology Stack

### Core Technologies
- **Language**: Python 3.9+
- **Web Framework**: FastAPI 0.104+
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic V2
- **HTTP Client**: httpx (for external API calls)
- **Caching**: TTLCache or Redis (for production)

### Development Dependencies
- **Testing**: pytest, pytest-asyncio, httpx (for testing)
- **Code Quality**: black, isort, flake8, mypy
- **Documentation**: FastAPI auto-docs (OpenAPI/Swagger)
- **Development Server**: uvicorn with reload

### Monitoring & Observability
- **Metrics**: prometheus-client
- **Logging**: Python logging with JSON formatting
- **Health Checks**: Custom health check endpoints
- **Tracing**: OpenTelemetry (future consideration)

### Deployment Technologies
- **Containerization**: Docker
- **Base Image**: python:3.9-slim
- **Process Manager**: Uvicorn (single process for now)
- **Port**: 8000 (configurable)

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Docker (for containerized deployment)
- Git (for version control)

### Local Development Environment
```bash
# Clone repository
git clone <repository-url>
cd market-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run development server
uvicorn src.predictor.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Configuration
```bash
# .env file for local development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_HOST=0.0.0.0
API_PORT=8000
CACHE_TTL=300
MODEL_TYPE=dummy
```

### Docker Development
```bash
# Build development image
docker build -f docker/Dockerfile.dev -t market-predictor:dev .

# Run development container
docker run -p 8000:8000 --env-file .env market-predictor:dev

# Run with docker-compose
docker-compose -f docker/docker-compose.dev.yml up
```

## Dependencies

### Core Production Dependencies
```
fastapi>=0.104.0         # Web framework
uvicorn[standard]>=0.24.0 # ASGI server
pydantic>=2.0.0          # Data validation
pydantic-settings>=2.0.0 # Settings management
prometheus-client>=0.17.0 # Metrics collection
python-multipart>=0.0.6  # Form data parsing
```

### Development Dependencies
```
pytest>=7.4.0           # Testing framework
pytest-asyncio>=0.21.0  # Async testing support
httpx>=0.25.0           # HTTP client for testing
black>=23.0.0           # Code formatting
isort>=5.12.0           # Import sorting
flake8>=6.0.0           # Linting
mypy>=1.5.0             # Type checking
pre-commit>=3.4.0       # Git hooks
```

### Optional Dependencies
```
redis>=5.0.0            # Caching (production)
numpy>=1.24.0           # For ML models (future)
pandas>=2.0.0           # Data manipulation (future)
scikit-learn>=1.3.0     # ML models (future)
```

## Technical Constraints

### Performance Requirements
- **Response Time**: < 100ms for 95th percentile
- **Throughput**: Handle 1000+ concurrent requests
- **Memory Usage**: < 512MB under normal load
- **CPU Usage**: < 50% under normal load

### Scalability Constraints
- **Stateless Design**: No persistent state in application
- **Horizontal Scaling**: Support multiple instances behind load balancer
- **Resource Limits**: Work within container resource limits
- **Cache Coherency**: Handle cache invalidation across instances

### Security Requirements
- **Input Validation**: All inputs validated via Pydantic
- **No Authentication**: Service runs in trusted network (for now)
- **Rate Limiting**: Basic rate limiting to prevent abuse
- **Secure Defaults**: All configurations use secure defaults

### Monitoring Requirements
- **Prometheus Metrics**: Must expose /metrics endpoint
- **Structured Logging**: JSON format for log aggregation
- **Health Endpoints**: /health and /status endpoints required
- **Observability**: Full request/response tracing

## Development Workflow

### Code Quality Standards
```bash
# Pre-commit hooks
pre-commit install

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Testing
pytest tests/ -v --cov=src
```

### Git Workflow
- **Branch Naming**: feature/, bugfix/, hotfix/ prefixes
- **Commit Messages**: Conventional commit format
- **PR Requirements**: Tests pass, code review approved
- **Main Branch**: Protected, requires PR for changes

### Testing Strategy
```
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for API endpoints
├── performance/       # Load and performance tests
└── fixtures/          # Test data and fixtures
```

### Deployment Pipeline
1. **Development**: Local testing with hot reload
2. **Testing**: Automated tests in CI/CD
3. **Staging**: Container deployment for integration testing
4. **Production**: Orchestrated deployment with health checks

## Configuration Management

### Environment Variables
```python
class Settings(BaseSettings):
    # Application settings
    environment: str = "development"
    log_level: str = "INFO"
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Model settings
    model_type: str = "dummy"
    cache_ttl: int = 300
    
    # Monitoring settings
    metrics_enabled: bool = True
    health_check_interval: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

### Configuration Validation
- **Type Safety**: All settings validated at startup
- **Required Fields**: Fail fast if required config missing
- **Default Values**: Sensible defaults for all optional settings
- **Environment Overrides**: Environment variables override defaults

## Integration Points

### External Dependencies
- **None Currently**: Self-contained service for Milestone 1
- **Future**: Market data APIs, ML model services
- **Optional**: Redis for caching, external monitoring

### Service Discovery
- **Health Endpoints**: For load balancer health checks
- **Metrics Endpoint**: For Prometheus scraping
- **OpenAPI Schema**: For API documentation and client generation

### Monitoring Integration
- **Prometheus**: Metrics collection at /metrics
- **Loki**: Structured JSON logs (via external collector)
- **Health Checks**: Service health at /health and /status

## Future Technical Considerations

### Scalability Improvements
- **Redis Caching**: Distributed caching for multiple instances
- **Database Integration**: Persistent storage for historical data
- **Message Queues**: Async processing for heavy workloads
- **Load Balancing**: Multiple instances with session affinity

### Advanced Features
- **ML Model Integration**: Real machine learning models
- **Real-time Data**: WebSocket endpoints for live predictions
- **Authentication**: JWT or API key based authentication
- **Rate Limiting**: Advanced rate limiting with quotas

### Operational Improvements
- **Blue-Green Deployment**: Zero-downtime deployments
- **Circuit Breakers**: Resilience patterns for external dependencies
- **Distributed Tracing**: Full request tracing across services
- **Alerting**: Automated alerting based on metrics thresholds 