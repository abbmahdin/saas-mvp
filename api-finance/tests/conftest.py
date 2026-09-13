"""Tests conftest."""
import pytest
from pathlib import Path

@pytest.fixture
def sample_candle():
    return {
        "ts": 1234567890,
        "open": 3400.5,
        "high": 3401.0,
        "low": 3399.0,
        "close": 3400.2,
        "volume": 1500,
    }
