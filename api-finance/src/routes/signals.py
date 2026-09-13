"""Signal routes — SMC/CVD XAUUSD signals with x402 payment."""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
import time

router = APIRouter()

PAYMENT_WALLET = "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c"


class SignalDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class SignalSource(str, Enum):
    SMC = "SMC"
    CVD = "CVD"
    MICRO = "MICRO"


class Signal(BaseModel):
    id: str
    timestamp: float
    direction: SignalDirection
    price: float = Field(..., description="Prix actuel de XAUUSD")
    stop_loss: float
    take_profit: Optional[float] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    source: SignalSource
    reason: str
    timeframe: str = "M5"


@router.get("/")
async def list_signals(request: Request):
    """List recent signals. Requires x402 payment ($0.05)."""
    # Check x402 headers
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        return _payment_required("signals")

    # Return mock signals (in production, query from DB or live bot)
    signals = _generate_mock_signals()
    return {"signals": signals, "wallet": wallet}


@router.get("/{signal_id}")
async def get_signal(signal_id: str, request: Request):
    """Get a specific signal by ID. Requires x402 payment ($0.05)."""
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        return _payment_required("signals")

    for s in _generate_mock_signals():
        if s["id"] == signal_id:
            return s

    raise HTTPException(status_code=404, detail="Signal not found")


@router.post("/")
async def create_signal(signal: Signal, request: Request):
    """Create a new signal. Requires x402 payment ($0.05)."""
    wallet = request.headers.get("x402-wallet")
    signature = request.headers.get("x402-signature")

    if not wallet or not signature:
        return _payment_required("signals")

    return {"message": "Signal created", "signal": signal.model_dump(), "wallet": wallet}


def _payment_required(resource: str):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=402,
        content={
            "error": "Payment Required",
            "payment": {
                "payTo": PAYMENT_WALLET,
                "methods": [{"type": "eip155", "chainId": 8453, "currency": "USDC", "amount": "50000"}],
                "network": "base",
            },
        },
        headers={"X-Paywall": "x402"},
    )


def _generate_mock_signals() -> List[dict]:
    """Generate mock signals for testing/demo."""
    return [
        {
            "id": "sig_001",
            "timestamp": time.time(),
            "direction": "BUY",
            "price": 3450.50,
            "stop_loss": 3445.0,
            "take_profit": 3458.0,
            "confidence": 0.85,
            "source": "SMC",
            "reason": "Order block confluence sur H4 + CVD divergence haussière M5",
            "timeframe": "M5",
        },
        {
            "id": "sig_002",
            "timestamp": time.time() - 300,
            "direction": "SELL",
            "price": 3448.20,
            "stop_loss": 3453.50,
            "confidence": 0.72,
            "source": "MICRO",
            "reason": "Range break baissier + M5 réactif sens SELL",
            "timeframe": "M5",
        },
    ]
