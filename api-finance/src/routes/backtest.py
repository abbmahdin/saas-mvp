"""Backtest routes — historical backtests with x402 payment."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
import time

router = APIRouter()

PAYMENT_WALLET = "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c"


class BacktestRequest(BaseModel):
    strategy: str
    timeframe: str = "M5"
    days: int = Field(default=30, ge=1, le=30)
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    params: Optional[dict] = None


@router.post("/")
async def run_backtest(req: BacktestRequest, request: Request):
    """Run a backtest. Requires x402 payment ($0.50)."""
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=402, content={
            "error": "Payment Required",
            "payment": {"payTo": PAYMENT_WALLET, "amount": "500000", "currency": "USDC", "network": "base"},
            }, headers={"X-Paywall": "x402"})

    # Return mock backtest result (in production, call QuantLive backend)
    result = {
        "backtest_id": f"bt_{int(time.time())}",
        "strategy": req.strategy,
        "timeframe": req.timeframe,
        "days": req.days,
        "wallet": wallet,
        "result": {
            "trades": 87,
            "winrate": 0.41,
            "pnl_usd": 41.76,
            "max_drawdown_pct": 12.3,
            "sharpe": 1.8,
        },
    }
    return result


@router.get("/")
async def list_backtests(request: Request):
    """List past backtests. Requires x402 payment ($0.10)."""
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=402, content={
            "error": "Payment Required",
            "payment": {"payTo": PAYMENT_WALLET, "amount": "100000", "currency": "USDC", "network": "base"},
            }, headers={"X-Paywall": "x402"})

    return {
        "backtests": [
            {"id": "bt_001", "strategy": "M5-reactive", "period": "2026-08-01 → 2026-09-01", "wallet": wallet},
        ],
    }
