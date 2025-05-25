# System Patterns - Market Predictor

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Clients   │────│ Market Predictor │────│ Monitoring Stack│
│                 │    │   (FastAPI)     │    │ (Prometheus)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                       ┌─────────────────┐
                       │  Prediction     │
                       │    Models       │
                       └─────────────────┘
```

### Application Architecture
```
src/predictor/
├── main.py                 # FastAPI application factory
├── api/                    # API layer
│   ├── routes/            # Route handlers
│   ├── models/            # Pydantic request/response models
│   └── middleware/        # Custom middleware
├── services/              # Business logic layer
│   ├── prediction.py      # Prediction service
│   ├── health.py          # Health check service
│   └── metrics.py         # Metrics collection
├── models/                # Prediction models
│   ├── base.py           # Model interface
│   └── dummy.py          # Initial dummy model
└── config/               # Configuration
    ├── settings.py       # Pydantic settings
    └── logging.py        # Logging configuration
```

## Key Technical Decisions

### 1. Framework Choice: FastAPI
**Decision**: Use FastAPI as the web framework
**Reasoning**:
- **Performance**: High performance, comparable to NodeJS and Go
- **Type Safety**: Built-in Pydantic integration for request/response validation
- **Documentation**: Automatic OpenAPI/Swagger documentation generation
- **Async Support**: Native async/await support for high concurrency
- **Developer Experience**: Excellent IDE support and error messages

### 2. Configuration Management: Pydantic Settings
**Decision**: Use Pydantic Settings for configuration management
**Reasoning**:
- **Type Safety**: Automatic type validation and conversion
- **Environment Integration**: Seamless environment variable binding
- **Documentation**: Self-documenting configuration schema
- **Validation**: Built-in validation with clear error messages

### 3. Dependency Injection Pattern
**Decision**: Use FastAPI's dependency injection system
**Reasoning**:
- **Testability**: Easy to mock dependencies for testing
- **Modularity**: Clean separation of concerns
- **Lifecycle Management**: Automatic dependency lifecycle management
- **Configuration**: Centralized configuration injection

### 4. Response Caching Strategy
**Decision**: Implement TTL-based caching for prediction responses
**Reasoning**:
- **Performance**: Reduce computation for similar requests
- **Consistency**: Same inputs return same outputs within cache window
- **Resource Optimization**: Reduce model inference load
- **Scalability**: Handle burst traffic more effectively

## Design Patterns

### 1. Service Layer Pattern
```python
# Separation of concerns between API and business logic
class PredictionService:
    def __init__(self, model: PredictionModel, cache: Cache):
        self.model = model
        self.cache = cache
    
    async def get_prediction(self, request: PredictionRequest) -> PredictionResponse:
        # Business logic isolated from API concerns
        pass
```

### 2. Repository Pattern for Models
```python
# Abstract interface for prediction models
class PredictionModel(ABC):
    @abstractmethod
    async def predict(self, input_data: Dict) -> PredictionResult:
        pass
    
    @abstractmethod
    def get_model_info(self) -> ModelInfo:
        pass
```

### 3. Middleware Pattern for Cross-Cutting Concerns
```python
# Prometheus metrics collection
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    # Request processing
    response = await call_next(request)
    # Metrics collection
    return response
```

### 4. Factory Pattern for Application Creation
```python
# Application factory for different environments
def create_app(config: Settings) -> FastAPI:
    app = FastAPI(title="Market Predictor")
    
    # Configure middleware
    setup_middleware(app, config)
    
    # Register routes
    setup_routes(app)
    
    # Configure dependencies
    setup_dependencies(app, config)
    
    return app
```

## Component Relationships

### 1. API Layer Dependencies
```
API Routes → Services → Models
     ↓           ↓        ↓
Pydantic ← Validation ← Config
```

### 2. Service Layer Dependencies
```
PredictionService
    ├── PredictionModel (interface)
    ├── Cache (TTL-based)
    ├── MetricsCollector
    └── Logger
```

### 3. Monitoring Integration
```
FastAPI Middleware → Prometheus Metrics → /metrics endpoint
Application Logs → Structured JSON → Loki integration
Health Checks → Service Status → /health & /status endpoints
```

## Error Handling Patterns

### 1. Structured Error Responses
```python
class APIError(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict] = None
    timestamp: datetime
```

### 2. Exception Hierarchy
```
APIException (base)
├── ValidationException (400)
├── PredictionException (500)
├── ModelUnavailableException (503)
└── RateLimitException (429)
```

### 3. Error Recovery Strategy
- **Graceful Degradation**: Return cached predictions if model fails
- **Circuit Breaker**: Prevent cascade failures
- **Retry Logic**: Automatic retry for transient failures
- **Fallback Models**: Use simpler model if primary fails

## Performance Patterns

### 1. Async Processing
- **Non-blocking I/O**: All external calls use async/await
- **Connection Pooling**: Reuse connections for external services
- **Background Tasks**: Use FastAPI background tasks for logging

### 2. Caching Strategy
- **Response Caching**: TTL-based cache for prediction responses
- **Model Caching**: Keep models in memory for fast inference
- **Configuration Caching**: Cache settings to avoid repeated parsing

### 3. Resource Management
- **Memory Limits**: Set appropriate limits for model memory usage
- **Connection Limits**: Configure appropriate connection pool sizes
- **Timeout Handling**: Set reasonable timeouts for all external calls

## Security Patterns

### 1. Input Validation
- **Pydantic Models**: Automatic request validation
- **Sanitization**: Clean and validate all input data
- **Type Safety**: Enforce strict typing throughout

### 2. Health Check Security
- **Minimal Information**: Health endpoints expose minimal system info
- **No Sensitive Data**: Avoid exposing internal system details
- **Rate Limiting**: Prevent abuse of health endpoints

### 3. Monitoring Security
- **Metrics Sanitization**: Ensure no PII in metrics
- **Log Scrubbing**: Remove sensitive data from logs
- **Access Control**: Secure metrics endpoints appropriately 