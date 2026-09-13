"""x402 payment middleware."""
from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
import os

# Wallet address for payments: 0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c
PAYMENT_WALLET = os.getenv("PAYMENT_WALLET", "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c")
PAYMENT_CHAIN = os.getenv("PAYMENT_CHAIN", "base")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN", "USDC")

# Pricing tiers in USD (USDC on Base)
PRICING_TIERS: Dict[str, float] = {
    "signals": 0.05,
    "backtest": 0.50,
    "reconcile": 0.10,
}


def get_payment_requirement(resource: str) -> Dict:
    """Build x402 payment requirement object for a given resource."""
    amount = PRICING_TIERS.get(resource, 0.05)
    return {
        "payTo": PAYMENT_WALLET,
        "methods": [
            {
                "type": "eip155",
                "chainId": 8453,
                "currency": PAYMENT_TOKEN,
                "amount": str(int(amount * 1_000_000)),  # USDC has 6 decimals
            }
        ],
        "network": PAYMENT_CHAIN,
    }


class X402Middleware(BaseHTTPMiddleware):
    """x402 payment middleware for protected routes."""

    PROTECTED_PREFIXES = ("/signals", "/backtests", "/reconciliation")

    def __init__(self, app, pricing_override: Optional[Dict] = None):
        super().__init__(app)
        if pricing_override:
            PRICING_TIERS.update(pricing_override)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Always allow health, root, docs
        if path in ("/", "/health", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)

        # Check if path is protected
        is_protected = any(path.startswith(prefix) for prefix in self.PROTECTED_PREFIXES)

        if not is_protected:
            return await call_next(request)

        # Check for x402 payment headers
        x402_header = request.headers.get("x402-payment")
        wallet_address = request.headers.get("x402-wallet")
        signature = request.headers.get("x402-signature")

        if x402_header and wallet_address and signature:
            return await call_next(request)

        # Return x402 payment required
        # Determine which resource based on path
        resource = "signals"
        if path.startswith("/backtests"):
            resource = "backtest"
        elif path.startswith("/reconciliation"):
            resource = "reconcile"

        payment_req = get_payment_requirement(resource)
        response = JSONResponse(
            status_code=402,
            content={"error": "Payment Required", "payment": payment_req},
        )
        response.headers["X-Paywall"] = "x402"
        return response


# Dependency for route-level payment checks
def require_payment():
    """Dependency that raises 402 if no x402 payment headers present."""
    def _check(request: Request):
        x402 = request.headers.get("x402-payment")
        wallet = request.headers.get("x402-wallet")
        sig = request.headers.get("x402-signature")

        if not all([x402, wallet, sig]):
            raise HTTPException(status_code=402, detail="Payment Required")
        return True

    return _check
