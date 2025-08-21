# Real-Time Explainable Credit Intelligence Platform

This repository contains a complete, end-to-end system that ingests multi-source data, computes adaptive creditworthiness scores with feature-level explainability, and presents results in an interactive analyst dashboard. It is designed for real-time operation, robust engineering, and clear transparency.

## Highlights
- High-throughput ingestion from structured (Yahoo Finance, World Bank) and unstructured (news RSS) sources
- Adaptive, online learning scoring engine (incremental SGD) with deterministic, feature-level contributions (no LLM)
- Explainability: per-score contribution breakdown, trend indicators (short- vs long-term), and event-aware reasoning (from structured + unstructured)
- Interactive React dashboard with trends, feature importance, filters, and alerts
- Dockerized with Compose for 1-command deployment; includes Postgres for persistence and a dedicated scheduler for automated refresh and retraining

## Architecture Overview
- backend (FastAPI): APIs, scoring service, explainability, alerts, SSE stream
- scheduler: periodic ingestion (structured + unstructured), feature engineering, incremental training, score publishing
- database (Postgres): issuers, raw events, features, scores, alerts, model metadata
- frontend (React + Vite): dashboard with trends, feature breakdown, events timeline, filters, comparisons

## Quickstart (Docker)
1. Copy env template and adjust as needed:
```bash
cp .env.example .env
```

2. Build and start:
```bash
docker compose up -d --build
```

3. Access services:
- API docs: http://localhost:8000/docs
- Dashboard: http://localhost:5173

## Local Development (optional)
- Backend: Python 3.10+
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Data Sources
- Structured: Yahoo Finance (prices/market features), World Bank (macro indicators)
- Unstructured: Company news via RSS (Google News/Company PR feeds)

Add your own sources easily under `backend/app/sources/`.

## Explainability
- Model: Online linear model (SGDRegressor with ElasticNet penalty) trained on a proxy risk target built from market volatility, drawdown, leverage, liquidity, macro stress, and recent sentiment
- Per-score contributions: coefficient × feature value; aggregated and displayed via API
- Trend indicators: EMA(7) vs EMA(30) on scores + feature trends

No LLM is used to generate explanations.

## Alerts
- Triggered on sudden score changes, volatility spikes, sentiment shocks, or data-quality anomalies
- Delivered via API and SSE stream for the dashboard

## MLOps
- Automated refresh and retraining via a dedicated scheduler container
- Fault tolerance: retries with exponential backoff, per-source circuit breakers, timeouts, and dead-letter tables
- Reproducible builds with Docker; deterministic model seeds

## Project Structure
```
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    sources/
    main.py
  requirements.txt
frontend/
  (React + Vite app)
Dockerfile.backend
Dockerfile.frontend
docker-compose.yml
.env.example
```

## Deployment
- Default stack uses Docker Compose (Postgres, backend API, scheduler, frontend)
- Can be deployed to any Docker-compatible host (AWS EC2, GCP, Azure, Render, Fly.io, etc.)

## Security
- Do not commit secrets; configure via environment variables
- SEC/EDGAR and similar sources may require a `User-Agent` string

## License
MIT

