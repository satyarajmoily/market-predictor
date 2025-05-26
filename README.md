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

## 🚀 Quick Start

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd market-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run development server
python -m uvicorn src.predictor.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Setup

```bash
# Build and run with Docker Compose
cd docker
docker-compose up --build

# Or build manually
docker build -f docker/Dockerfile -t market-predictor .
docker run -p 8000:8000 --env-file .env market-predictor
```

### API Endpoints

Once running, the service provides:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Detailed Status**: http://localhost:8000/status
- **Prometheus Metrics**: http://localhost:8000/metrics ⚡ NEW!
- **Root Info**: http://localhost:8000/

---

## 📁 Project Structure

```
market-predictor/
├── src/
│   └── predictor/
│       ├── __init__.py
│       ├── main.py              # FastAPI app entry point
│       ├── api/                 # API route handlers
│       ├── services/            # Business logic
│       ├── models/              # Pydantic models
│       │   └── health.py        # Health check models
│       └── config/
│           └── settings.py      # Configuration management
├── tests/                       # Test suite
├── docker/
│   ├── Dockerfile              # Production container
│   └── docker-compose.yml      # Development environment
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── .env.example                # Environment template
└── memory-bank/                # Project documentation
```

---

## 🔧 Configuration

The service uses Pydantic Settings for configuration management. Environment variables can be set in `.env` file:

```bash
# Environment Configuration
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DEBUG=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Service Configuration
SERVICE_NAME=market-predictor
SERVICE_VERSION=0.1.0

# Model Configuration
MODEL_TYPE=dummy
CACHE_TTL=300

# Monitoring Configuration
METRICS_ENABLED=true
HEALTH_CHECK_INTERVAL=30
```

---

## 🧪 Testing

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src/predictor --cov-report=html

# Run linting
flake8 src/ tests/
black src/ tests/
mypy src/
```

---

## 📊 Current Status: Phase 1.2 Complete ✅ (Prometheus Metrics)

### ✅ Completed Features:
- **Project Structure**: Complete Python package with proper structure
- **FastAPI Application**: Working web service with health endpoints
- **Configuration Management**: Pydantic settings with environment variables
- **Docker Support**: Containerization with development environment
- **Health Endpoints**: `/health` and `/status` endpoints functional
- **⚡ Prometheus Metrics**: `/metrics` endpoint with HTTP request counters and duration histograms
- **⚡ Event-Driven Architecture**: Professional monitoring stack with Prometheus + Alertmanager
- **⚡ Alert Rules**: Production-ready alerts for service monitoring
- **Development Environment**: Ready for local development

### 🔜 Next Steps (Phase 1.3):
- Implement `/predict` endpoint for Bitcoin price predictions
- Add request/response validation with Pydantic models
- Create prediction service with caching
- Implement proper error handling and HTTP status codes

---

## 🚦 Agent Integration Points

The Market Predictor is designed to be monitored and improved by the Market Programmer Agent:

### Event-Driven Monitoring (Professional Architecture) ⚡
- `GET /health` - Basic health status for agent monitoring
- `GET /status` - Detailed status for agent analysis (includes uptime, components)
- `GET /metrics` - ✅ Prometheus-formatted metrics (HTTP counters, durations, health checks)
- **Alert Rules** - ✅ Production-ready alerts for service issues
- **Alertmanager** - ✅ Routes alerts to Market Programmer Agent webhooks

### Agent Integration Architecture
```
Prometheus → Alert Rules → Alertmanager → Agent Webhooks → AI Analysis
     ↑                                                           ↓
Market Predictor /metrics                               Intelligent Actions
```

### Future Integration (Later Phases)
- **Structured JSON logs** for easy parsing
- **API versioning** to prevent breaking changes
- **GitHub Actions** respond to agent-created PRs

---

## 📈 Development Roadmap

### Milestone 1: Foundation (Current)
- **Phase 1.1**: ✅ Project Structure & Environment Setup
- **Phase 1.2**: ✅ Prometheus Metrics & Event-Driven Architecture ⚡
- **Phase 1.3**: 🔄 Core API Endpoints (`/predict`, error handling)
- **Phase 1.4**: ⏳ Basic Prediction Logic Implementation
- **Phase 1.5**: ⏳ Local Testing & Validation

### Future Milestones
- **Milestone 2**: Prediction Service Implementation
- **Milestone 3**: Logging & Observability (Loki integration)
- **Milestone 4**: Production Readiness (CI/CD & deployment)

---

## 🤝 Contributing

This repository is part of an autonomous trading system where the Market Programmer Agent will make most code improvements. However, manual contributions are welcome:

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** changes with comprehensive tests
4. **Ensure** all health endpoints remain functional
5. **Submit** a pull request with detailed description

### Development Guidelines
- Maintain **high test coverage** (>90%)
- Include **proper health checks** for agent monitoring
- Follow **FastAPI best practices**
- Document **API changes** thoroughly

---

## 📝 License

MIT License - This project is part of the Autonomous Trading Builder system.