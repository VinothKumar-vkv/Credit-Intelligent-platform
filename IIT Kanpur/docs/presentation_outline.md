# Presentation Outline (5–7 minutes)

1. Problem & Requirements (30s)
- Real-time explainable credit intelligence; multi-source ingest; adaptive scoring; transparent explanations; interactive dashboard; deployment.

2. Architecture (45s)
- Diagram: Ingestion (Yahoo, World Bank, RSS) -> Feature Store -> Online Scoring (SGD) -> Explainability -> Postgres -> API (FastAPI) -> Dashboard (React) -> Alerts.

3. Data Engineering (60s)
- Structured: Yahoo Finance, World Bank. Unstructured: RSS + VADER sentiment.
- Cleaning, normalization, retries/backoffs, circuit breakers, dead-letter strategy.
- Near-real-time scheduler; incremental updates.

4. Model & Explainability (75s)
- Online linear model (SGDRegressor) with feature standardization.
- Target proxy design (volatility, drawdown, momentum, macro stress) and rationale.
- Deterministic feature contributions (coef × standardized feature), trend EMA(7)/EMA(30).
- No LLM explanations; purely model-derived, auditable.

5. Dashboard UX (60s)
- Issuer list, score trends, feature contributions, recent events, filters.
- Alerts for sudden changes.

6. Deployment & Ops (45s)
- Dockerized services; Render config with web (API), worker (scheduler), static (frontend).
- Env-based configuration; Postgres managed DB; scalability.

7. Innovation & Extensions (45s)
- Add sector indices, shipping/energy data; text embeddings for events clustering; anomaly detection; agency rating comparison; SSE alert streaming.

8. Results & Demo (45s)
- Show live dashboard; issuer trend; explanation and recent events; trigger a manual refresh.

9. Close (15s)
- Summary, trade-offs, roadmap.
