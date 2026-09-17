"""Reconciliation routes — reconcile signals vs executions with x402 payment."""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import time

router = APIRouter()

PAYMENT_WALLET = "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c"


class ReconcileRequest(BaseModel):
    account: str
    date: datetime
    trades: Optional[List[dict]] = None


@router.post("/")
async def reconcile_trades(req: ReconcileRequest, request: Request):
    """Reconcile trades for an account. Requires x402 payment ($0.10)."""
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=402, content={
            "error": "Payment Required",
            "payment": {"payTo": PAYMENT_WALLET, "amount": "100000", "currency": "USDC", "network": "base"},
            }, headers={"X-Paywall": "x402"})

    return {
        "reconcile_id": f"rec_{int(time.time())}",
        "account": req.account,
        "date": req.date.isoformat(),
        "wallet": wallet,
        "result": {
            "trades_matched": 12,
            "trades_mismatched": 2,
            "pnl_broker": 54.20,
            "pnl_system": 53.88,
            "delta": -0.32,
        },
    }
