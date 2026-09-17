"""FastAPI application for API Finance."""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from uuid import uuid4
import time

# Pricing tiers in USD (USDC on Base)
PRICING = {
    "signals": 0.05,       # $0.05 per signal request
    "backtest": 0.50,      # $0.50 per backtest (up to 30 days)
    "reconcile": 0.10,     # $0.10 per reconciliation request
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    print("API Finance starting up...")
    yield
    print("API Finance shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="API Finance",
        description="SMC/CVD XAUUSD Signals, Backtests & Reconciliation with x402 payments",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Prometheus metrics
    from src.metrics import setup_metrics
    setup_metrics(app)

    from src.routes.signals import router as signals_router
    from src.routes.backtest import router as backtest_router
    from src.routes.reconcile import router as reconcile_router

    app.include_router(signals_router, prefix="/signals", tags=["signals"])
    app.include_router(backtest_router, prefix="/backtests", tags=["backtests"])
    app.include_router(reconcile_router, prefix="/reconciliation", tags=["reconciliation"])

    @app.get("/", tags=["root"])
    async def root():
        return {
            "name": "API Finance",
            "version": "0.1.0",
            "description": "SMC/CVD XAUUSD Signals, Backtests & Reconciliation",
            "endpoints": {
                "signals": "/signals",
                "backtests": "/backtests",
                "reconciliation": "/reconciliation",
                "health": "/health",
            },
        }

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "service": "api-finance"}

    return app


app = create_app()
