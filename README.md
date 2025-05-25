# Market Predictor - Bitcoin Price Prediction Server

## 🎯 Repository Responsibility

The **Market Predictor** is the core prediction engine in our autonomous trading system. This FastAPI-based service provides Bitcoin price predictions and serves as the **primary subject of monitoring and improvement** by the market-programmer-agent. 

### Core Responsibilities:
- **Prediction Service**: Expose REST APIs for Bitcoin price predictions
- **Metrics Exposition**: Provide Prometheus-compatible metrics for monitoring
- **Health Monitoring**: Implement comprehensive health checks and status endpoints
- **Logging Integration**: Structure logs for Loki aggregation and analysis
- **Model Management**: Handle prediction models, training, and inference
- **Performance Optimization**: Maintain low-latency, high-availability prediction service

### System Architecture Role:
```
[External Clients] → [Market Predictor] ← [Market Programmer Agent]
                           ↓
                    [Prometheus Metrics]
                           ↓
                      [Loki Logs]
```

The Market Predictor is the **target of autonomous improvement** - the agent monitors its performance, analyzes its logs, and creates PRs to enhance its capabilities.

---

## 🚀 Development Roadmap

### Milestone 1: Foundation - Basic Prediction Service
**Goal**: Establish a working FastAPI prediction server with core functionality

#### Phase 1.1: Project Structure & Environment Setup
**Duration**: 1-2 days
**Deliverables**:
- [ ] Python project structure with proper packaging
- [ ] Virtual environment configuration
- [ ] Basic requirements.txt with FastAPI dependencies
- [ ] Docker configuration for containerized deployment
- [ ] Environment variable management (.env support)

**Technical Implementation**:
```
market-predictor/
├── src/
│   ├── predictor/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models/              # Prediction models
│   │   ├── api/                 # API route handlers
│   │   ├── services/            # Business logic
│   │   └── config/              # Configuration management
├── tests/
├── docker/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**Key Files**:
- `src/predictor/main.py`: FastAPI application factory
- `src/predictor/config/settings.py`: Configuration management using Pydantic
- `requirements.txt`: Core dependencies (FastAPI, uvicorn, pydantic, requests)

#### Phase 1.2: Core API Endpoints
**Duration**: 2-3 days
**Deliverables**:
- [ ] `/predict` endpoint for Bitcoin price predictions
- [ ] `/health` endpoint for service health checks
- [ ] `/status` endpoint for detailed service status
- [ ] Pydantic models for request/response validation
- [ ] Error handling and HTTP status codes

**API Specification**:
```python
# Prediction Request Model
class PredictionRequest(BaseModel):
    timeframe: str = "1h"  # 1h, 4h, 1d
    data_points: Optional[int] = 100
    include_confidence: bool = True

# Prediction Response Model
class PredictionResponse(BaseModel):
    predicted_price: float
    confidence_score: float
    prediction_timestamp: datetime
    model_version: str
    timeframe: str
```

**Endpoints**:
- `POST /api/v1/predict` - Main prediction endpoint
- `GET /health` - Basic health check (returns 200 OK)
- `GET /status` - Detailed status (uptime, model info, last prediction)
- `GET /docs` - Auto-generated API documentation

#### Phase 1.3: Basic Prediction Logic Implementation
**Duration**: 3-4 days
**Deliverables**:
- [ ] Dummy prediction model (random walk, moving average)
- [ ] Model interface for future ML model integration
- [ ] Data validation and preprocessing
- [ ] Response caching mechanism
- [ ] Basic error handling for prediction failures

**Technical Implementation**:
```python
class PredictionModel:
    def predict(self, input_data: dict) -> PredictionResult:
        # Initial implementation: Simple moving average or random walk
        pass

class PredictionService:
    def __init__(self, model: PredictionModel):
        self.model = model
        self.cache = TTLCache(maxsize=100, ttl=300)  # 5-minute cache
    
    async def get_prediction(self, request: PredictionRequest) -> PredictionResponse:
        # Implement caching, validation, and prediction logic
        pass
```

#### Phase 1.4: Local Testing & Validation
**Duration**: 1-2 days
**Deliverables**:
- [ ] Unit tests for API endpoints
- [ ] Integration tests for prediction workflow
- [ ] Load testing with sample requests
- [ ] API documentation validation
- [ ] Local deployment verification

**Testing Strategy**:
- Unit tests: `pytest` for individual components
- Integration tests: `httpx` for API testing
- Load tests: Basic stress testing with `locust` or similar
- Docker testing: Verify containerized deployment

---

### Milestone 2: Monitoring Integration - Prometheus & Observability
**Goal**: Integrate comprehensive monitoring and metrics for autonomous agent consumption

#### Phase 2.1: Prometheus Metrics Implementation
**Duration**: 2-3 days
**Deliverables**:
- [ ] Prometheus client library integration
- [ ] Custom metrics for prediction service
- [ ] `/metrics` endpoint for Prometheus scraping
- [ ] Middleware for automatic request tracking
- [ ] Performance metrics collection

**Metrics Implementation**:
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Core Metrics
prediction_requests_total = Counter(
    'prediction_requests_total',
    'Total prediction requests',
    ['method', 'endpoint', 'status']
)

prediction_duration_seconds = Histogram(
    'prediction_duration_seconds',
    'Time spent on predictions',
    ['model_version']
)

prediction_confidence_score = Gauge(
    'prediction_confidence_current',
    'Current prediction confidence score'
)

model_last_updated = Gauge(
    'model_last_updated_timestamp',
    'Timestamp of last model update'
)
```

**Key Metrics Categories**:
- **Request Metrics**: Count, duration, status codes
- **Prediction Metrics**: Confidence scores, model performance
- **System Metrics**: Memory usage, CPU, response times
- **Business Metrics**: Prediction accuracy, model drift

#### Phase 2.2: Advanced Instrumentation
**Duration**: 2-3 days
**Deliverables**:
- [ ] FastAPI middleware for automatic instrumentation
- [ ] Custom business logic metrics
- [ ] Resource utilization tracking
- [ ] Model performance metrics
- [ ] Alert-ready metric thresholds

**Implementation Details**:
```python
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    # Record metrics
    prediction_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    prediction_duration_seconds.labels(
        model_version=get_current_model_version()
    ).observe(time.time() - start_time)
    
    return response
```

#### Phase 2.3: Health Check Enhancement
**Duration**: 1-2 days
**Deliverables**:
- [ ] Comprehensive health check system
- [ ] Dependency health verification
- [ ] Performance benchmark validation
- [ ] Graceful degradation indicators
- [ ] Health status metrics

**Health Check Categories**:
- **Service Health**: API responsiveness, memory usage
- **Model Health**: Model availability, last training date
- **Data Health**: Input validation, data freshness
- **External Dependencies**: Database, external APIs

---

### Milestone 3: Logging & Observability - Loki Integration
**Goal**: Implement structured logging for autonomous analysis by the programmer agent

#### Phase 3.1: Structured Logging Implementation
**Duration**: 2-3 days
**Deliverables**:
- [ ] JSON-structured logging with Python logging
- [ ] Log correlation IDs for request tracing
- [ ] Different log levels and categories
- [ ] Log sanitization for sensitive data
- [ ] Performance-optimized logging

**Logging Structure**:
```python
import structlog

logger = structlog.get_logger()

# Structured log example
logger.info(
    "prediction_completed",
    request_id=request_id,
    user_id=user_id,
    model_version="v1.2.3",
    prediction_value=1234.56,
    confidence_score=0.85,
    processing_time_ms=125,
    input_features=feature_count
)
```

**Log Categories**:
- **Request Logs**: API calls, parameters, responses
- **Prediction Logs**: Model inputs, outputs, confidence
- **Error Logs**: Exceptions, stack traces, error context
- **Performance Logs**: Timing, resource usage, bottlenecks
- **Security Logs**: Authentication, authorization events

#### Phase 3.2: Loki Integration & Log Shipping
**Duration**: 2-3 days
**Deliverables**:
- [ ] Promtail configuration for log shipping
- [ ] Log labels for Loki querying
- [ ] Log retention policies
- [ ] Log parsing and filtering rules
- [ ] Dashboard-ready log format

**Promtail Configuration**:
```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: predictor
    static_configs:
      - targets:
          - localhost
        labels:
          job: predictor
          service: market-predictor
          __path__: /var/log/predictor/*.log
```

#### Phase 3.3: Error Tracking & Diagnostics
**Duration**: 1-2 days
**Deliverables**:
- [ ] Exception tracking and categorization
- [ ] Stack trace logging with context
- [ ] Error rate monitoring
- [ ] Diagnostic information collection
- [ ] Recovery attempt logging

---

### Milestone 4: Production Readiness - CI/CD & Deployment
**Goal**: Prepare the service for autonomous deployment and updates

#### Phase 4.1: CI/CD Pipeline Setup
**Duration**: 3-4 days
**Deliverables**:
- [ ] GitHub Actions workflow for testing
- [ ] Automated testing on PR creation
- [ ] Docker image building and publishing
- [ ] Deployment automation
- [ ] Rollback capabilities

**GitHub Actions Workflow**:
```yaml
name: Market Predictor CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src/predictor tests/
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: |
          # Deployment script
```

#### Phase 4.2: Model Management & Versioning
**Duration**: 2-3 days
**Deliverables**:
- [ ] Model versioning system
- [ ] Model artifact storage
- [ ] A/B testing framework for models
- [ ] Model rollback capabilities
- [ ] Performance comparison tracking

#### Phase 4.3: Configuration Management
**Duration**: 1-2 days
**Deliverables**:
- [ ] Environment-specific configurations
- [ ] Secret management integration
- [ ] Feature flags for A/B testing
- [ ] Runtime configuration updates
- [ ] Configuration validation

---

### Milestone 5: Enhanced Prediction Capabilities
**Goal**: Implement advanced prediction features and model improvements

#### Phase 5.1: Advanced Prediction Models
**Duration**: 1-2 weeks
**Deliverables**:
- [ ] Multiple prediction algorithms (LSTM, ARIMA, Prophet)
- [ ] Ensemble model predictions
- [ ] Feature engineering pipeline
- [ ] Model training automation
- [ ] Hyperparameter optimization

#### Phase 5.2: Real-time Data Integration
**Duration**: 1 week
**Deliverables**:
- [ ] Live market data feeds
- [ ] Data preprocessing pipelines
- [ ] Real-time prediction updates
- [ ] Data quality monitoring
- [ ] Streaming data handling

#### Phase 5.3: Performance Optimization
**Duration**: 3-5 days
**Deliverables**:
- [ ] Prediction caching strategies
- [ ] Database optimization
- [ ] API response time optimization
- [ ] Resource usage optimization
- [ ] Scalability improvements

---

### Milestone 6: Production Hardening & Resilience
**Goal**: Ensure production-grade reliability and performance

#### Phase 6.1: Security Implementation
**Duration**: 3-4 days
**Deliverables**:
- [ ] API authentication and authorization
- [ ] Rate limiting and throttling
- [ ] Input validation and sanitization
- [ ] Security headers and CORS
- [ ] Vulnerability scanning integration

#### Phase 6.2: Reliability & Fault Tolerance
**Duration**: 3-4 days
**Deliverables**:
- [ ] Circuit breaker patterns
- [ ] Retry mechanisms with exponential backoff
- [ ] Graceful degradation
- [ ] Health check improvements
- [ ] Disaster recovery procedures

#### Phase 6.3: Monitoring & Alerting Enhancement
**Duration**: 2-3 days
**Deliverables**:
- [ ] SLA-based monitoring
- [ ] Predictive alerting
- [ ] Performance benchmarking
- [ ] Capacity planning metrics
- [ ] Business KPI tracking

---

## 🔧 Technical Stack

### Core Technologies
- **Framework**: FastAPI 0.104+
- **Python**: 3.11+
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **Testing**: Pytest, httpx

### Monitoring & Observability
- **Metrics**: Prometheus (prometheus-client)
- **Logging**: Structlog, JSON formatting
- **Log Aggregation**: Compatible with Loki/Promtail
- **Health Checks**: Custom health check framework

### Data & ML
- **Data Processing**: Pandas, NumPy
- **ML Libraries**: Scikit-learn, TensorFlow/PyTorch
- **Time Series**: Prophet, ARIMA models
- **Feature Engineering**: Custom pipeline framework

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Deployment**: Oracle Cloud Infrastructure (Always Free)
- **CI/CD**: GitHub Actions
- **Database**: PostgreSQL (for model storage)

---

## 🚦 Agent Integration Points

The Market Predictor is designed to be monitored and improved by the Market Programmer Agent:

### Metrics Endpoints for Agent Monitoring
- `GET /metrics` - Prometheus-formatted metrics
- `GET /health` - Health status for agent monitoring
- `GET /status` - Detailed status for agent analysis

### Log Integration for Agent Analysis
- **Structured JSON logs** for easy parsing
- **Error categorization** for agent classification
- **Performance metrics** in logs for trend analysis
- **Request tracing** for debugging assistance

### API Stability for Agent Operations
- **Versioned APIs** to prevent breaking changes
- **Backward compatibility** during agent-driven updates
- **Feature flags** for safe A/B testing
- **Graceful degradation** during maintenance

### Deployment Integration
- **GitHub Actions** respond to agent-created PRs
- **Automated testing** validates agent-proposed changes
- **Rollback capabilities** for failed agent deployments
- **Status webhooks** notify agent of deployment results

---

## 📊 Success Metrics

### Performance KPIs
- **Response Time**: < 100ms for predictions
- **Availability**: > 99.9% uptime
- **Throughput**: > 1000 requests/minute
- **Error Rate**: < 0.1% of requests

### Prediction Quality
- **Accuracy**: Continuously improving prediction accuracy
- **Confidence**: Reliable confidence scoring
- **Model Performance**: Regular model evaluation metrics
- **Data Quality**: Real-time data validation

### Autonomous Operation
- **Agent Compatibility**: Seamless integration with programmer agent
- **Monitoring Coverage**: 100% observability for agent analysis
- **Deployment Success**: Successful agent-driven deployments
- **Self-Healing**: Automatic recovery from common issues

---

## 🤝 Contributing

This repository is part of an autonomous trading system where the Market Programmer Agent will make most code improvements. However, manual contributions are welcome:

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** changes with comprehensive tests
4. **Ensure** all metrics and logging are properly instrumented
5. **Submit** a pull request with detailed description

### Development Guidelines
- Maintain **high test coverage** (>90%)
- Include **proper logging** for agent analysis
- Add **appropriate metrics** for monitoring
- Follow **FastAPI best practices**
- Document **API changes** thoroughly

---

## 📝 License

MIT License - This project is part of the Autonomous Trading Builder system.