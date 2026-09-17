"""Shared test fixtures for API Finance."""
import pytest
import sys
from pathlib import Path

# Ensure src is importable
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """x402 payment headers for authenticated requests."""
    return {
        "x402-wallet": "0xf8a2d3969bC89aC900D1C890F57feC60BEc9bB9c",
        "x402-signature": "test_sig_valid",
    }
