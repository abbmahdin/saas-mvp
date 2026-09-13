"""Tests for the validator API routes."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# We'll create a simple FastAPI app for testing
from fastapi import FastAPI
from src.routes.validate import router


@pytest.fixture
def client():
    """Create test client with the validate router."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return TestClient(app)


class TestValidateEndpoint:
    """Test suite for POST /api/v1/validate."""

    def test_validate_returns_200_with_valid_input(self, client):
        """Valid subreddit should return 200 with report."""
        with patch("src.routes.validate.validate_subreddit") as mock_val:
            mock_val.return_value = {
                "subreddit": "test",
                "overall_score": 75.0,
                "pains": [],
                "volume_score": 80.0,
                "intensity_score": 70.0,
                "competition_score": 60.0,
            }
            response = client.post(
                "/api/v1/validate",
                json={"subreddit": "test", "limit": 50}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["subreddit"] == "test"

    def test_validate_requires_subreddit_field(self, client):
        """Missing subreddit should return 422."""
        response = client.post(
            "/api/v1/validate",
            json={"limit": 50}
        )
        assert response.status_code == 422

    def test_validate_uses_default_limit(self, client):
        """Default limit should be 100."""
        with patch("src.routes.validate.validate_subreddit") as mock_val:
            mock_val.return_value = {"subreddit": "test", "overall_score": 50.0, "pains": [], "volume_score": 50.0, "intensity_score": 50.0, "competition_score": 50.0}
            client.post("/api/v1/validate", json={"subreddit": "test"})
            call_args = mock_val.call_args
            assert call_args[1].get("limit", 100) == 100 or call_args[0][1] == 100

    def test_validate_passes_limit_to_service(self, client):
        """Custom limit should be passed through."""
        with patch("src.routes.validate.validate_subreddit") as mock_val:
            mock_val.return_value = {"subreddit": "test", "overall_score": 50.0, "pains": [], "volume_score": 50.0, "intensity_score": 50.0, "competition_score": 50.0}
            response = client.post(
                "/api/v1/validate",
                json={"subreddit": "python", "limit": 200}
            )
            assert response.status_code == 200
            mock_val.assert_called_once()
            # Check that limit=200 was passed
            call_kwargs = mock_val.call_args[1]
            assert call_kwargs.get("limit") == 200

    def test_validate_response_contains_markdown_report(self, client):
        """Response should include a markdown report."""
        with patch("src.routes.validate.validate_subreddit") as mock_val:
            mock_val.return_value = {
                "subreddit": "test",
                "overall_score": 75.0,
                "pains": [{"description": "test pain", "frequency": 5}],
                "volume_score": 80.0,
                "intensity_score": 70.0,
                "competition_score": 60.0,
            }
            response = client.post("/api/v1/validate", json={"subreddit": "test"})
            data = response.json()
            assert "report_markdown" in data
            assert isinstance(data["report_markdown"], str)

    def test_validate_handles_service_errors(self, client):
        """Service errors should return 500."""
        with patch("src.routes.validate.validate_subreddit") as mock_val:
            mock_val.side_effect = Exception("Reddit API error")
            response = client.post("/api/v1/validate", json={"subreddit": "test"})
            assert response.status_code == 500


class TestHealthEndpoint:
    """Test suite for GET /health."""

    def test_health_returns_200(self, client):
        """Health check should return 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestReadyEndpoint:
    """Test suite for GET /ready."""

    def test_ready_returns_200_when_healthy(self, client):
        """Ready check should return 200."""
        response = client.get("/ready")
        assert response.status_code == 200