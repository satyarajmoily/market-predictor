# Project Brief - Market Predictor

## Project Overview

**Market Predictor** is the core prediction engine in our autonomous trading system. It's a FastAPI-based service that provides Bitcoin price predictions and serves as the primary subject of monitoring and improvement by the market-programmer-agent.

## Core Purpose

- **Primary Function**: Expose REST APIs for Bitcoin price predictions
- **System Role**: Target system for autonomous improvement and monitoring
- **Business Value**: Provide reliable, fast, and accurate Bitcoin price predictions

## Key Responsibilities

1. **Prediction Service**: Expose REST APIs for Bitcoin price predictions
2. **Metrics Exposition**: Provide Prometheus-compatible metrics for monitoring
3. **Health Monitoring**: Implement comprehensive health checks and status endpoints
4. **Logging Integration**: Structure logs for Loki aggregation and analysis
5. **Model Management**: Handle prediction models, training, and inference
6. **Performance Optimization**: Maintain low-latency, high-availability prediction service

## System Architecture Context

```
[External Clients] → [Market Predictor] ← [Market Programmer Agent]
                           ↓
                    [Prometheus Metrics]
                           ↓
                      [Loki Logs]
```

The Market Predictor is the **target of autonomous improvement** - the agent monitors its performance, analyzes its logs, and creates PRs to enhance its capabilities.

## Milestone 1 Objectives

**Goal**: Establish a working FastAPI prediction server with core functionality

### Success Criteria:
- [x] Working FastAPI application with proper project structure ✅
- [x] Health endpoints: `/health`, `/status` ✅
- [x] Prometheus metrics: `/metrics` endpoint ✅ (NEW!)
- [x] Event-driven monitoring architecture ✅ (NEW!)
- [ ] Core API endpoints: `/predict`
- [ ] Basic prediction logic implementation (dummy model acceptable)
- [x] Docker containerization support ✅
- [ ] Comprehensive testing suite
- [x] API documentation via FastAPI/OpenAPI ✅

### Milestone 1 Phases:
1. **Phase 1.1**: Project Structure & Environment Setup ✅ COMPLETE
2. **Phase 1.2**: Prometheus Metrics & Event-Driven Architecture ✅ COMPLETE
3. **Phase 1.3**: Core API Endpoints (2-3 days) - NEXT
4. **Phase 1.4**: Basic Prediction Logic Implementation (3-4 days)
5. **Phase 1.5**: Local Testing & Validation (1-2 days)

## Technical Constraints

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **Deployment**: Docker containers
- **Monitoring**: Must support Prometheus metrics
- **API Design**: RESTful with proper HTTP status codes
- **Response Format**: JSON with Pydantic model validation

## Success Metrics

- API response time < 100ms for predictions
- 99% uptime during normal operation
- Comprehensive test coverage (>90%)
- Full API documentation coverage
- Docker deployment without manual configuration 