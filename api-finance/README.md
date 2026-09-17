# API Données Financières Curatées

## Objectif
Endpoint unique : signaux SMC/CVD nettoyés XAUUSD (pipeline QuantLive) → JSON normalisé, historique 2+ ans, rate-limited, clés API par client.

## Stack
- **Language** : Python
- **Framework** : FastAPI
- **DB** : PostgreSQL (candles QuantLive)
- **Deploy** : Docker + docker-compose
- **Scheduler** : n8n
- **Payments** : x402 (USDC sur Base) — signaux $0.05, backtests $0.50

## Structure

```
api-finance/
├── src/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── routes/
│   │   ├── signals.py   # GET /signals/xauusd
│   │   ├── candles.py   # GET /candles/xauusd
│   │   └── backtest.py  # POST /backtest
│   ├── models/
│   │   └── signal.py
│   └── middleware/
│       └── x402.py      # Paiement par requête
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── data/                # CSV historiques
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Endpoints (MVP)

| Méthode | Route | Prix | Description |
|---------|-------|------|-------------|
| GET | `/health` | free | Health check |
| GET | `/candles/xauusd?from=&to=&tf=` | free (rate-limited) | Candlesticks historiques |
| GET | `/signals/xauusd` | $0.05 | Signal SMC/CVD actuel |
| POST | `/backtest` | $0.50 | Backtest walk-forward |

## Setup local

```bash
cd ~/saas-mvp/api-finance
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./docker-compose up -d postgres
pytest -v  # TDD — tests d'abord
```

## Status

- ⏳ À démarrer — réutilise la logique de QuantLive (`app/micro/regime.py`, `app/micro/gates.py`)
