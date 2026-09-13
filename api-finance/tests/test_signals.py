"""Tests for signal routes."""
import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.fixture
def client():
    from src.main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {
        "x402-wallet": "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c",
        "x402-signature": "test_sig_valid",
    }


def test_list_signals_requires_payment(client):
    """Listing signals without payment returns 402."""
    resp = client.get("/signals")
    assert resp.status_code == 402
    assert "payment" in resp.json()


def test_list_signals_with_payment(client, auth_headers):
    """Listing signals with valid x402 headers returns signals."""
    resp = client.get("/signals", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "signals" in data
    assert len(data["signals"]) >= 1
    assert data["signals"][0]["direction"] in ("BUY", "SELL")
    assert 0 <= data["signals"][0]["confidence"] <= 1.0


def test_get_signal_by_id_requires_payment(client):
    resp = client.get("/signals/sig_001")
    assert resp.status_code == 402


def test_get_signal_by_id_with_payment(client, auth_headers):
    resp = client.get("/signals/sig_001", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "sig_001"


def test_create_signal_requires_payment(client):
    resp = client.post("/signals", json={
        "id": "x", "timestamp": 1.0, "direction": "BUY", "price": 1.0,
        "stop_loss": 1.0, "confidence": 0.8, "source": "SMC", "reason": "test"
    })
    assert resp.status_code == 402


def test_create_signal_with_payment(client, auth_headers):
    signal = {
        "id": "sig_test", "timestamp": 1700000000.0,
        "direction": "BUY", "price": 3450.50,
        "stop_loss": 3445.0, "confidence": 0.85,
        "source": "SMC", "reason": "Order block confluence"
    }
    resp = client.post("/signals", json=signal, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["signal"]["id"] == "sig_test"


def test_signal_validation():
    """Signal confidence must be 0-1."""
    from src.routes.signals import Signal
    s = Signal(
        id="1", timestamp=1.0, direction="BUY", price=100.0,
        stop_loss=99.0, confidence=1.0, source="SMC", reason="test"
    )
    assert s.confidence == 1.0


def test_signal_direction_validation():
    """Signal direction must be BUY or SELL."""
    from src.routes.signals import Signal, SignalDirection
    s = Signal(
        id="1", timestamp=1.0, direction="BUY", price=100.0,
        stop_loss=99.0, confidence=0.5, source="SMC", reason="test"
    )
    assert s.direction == SignalDirection.BUY


def test_signal_confidence_range():
    """Signal confidence must be between 0 and 1."""
    from pydantic import ValidationError
    from src.routes.signals import Signal
    with pytest.raises(ValidationError):
        Signal(
            id="1", timestamp=1.0, direction="BUY", price=100.0,
            stop_loss=99.0, confidence=1.5, source="SMC", reason="test"
        )
