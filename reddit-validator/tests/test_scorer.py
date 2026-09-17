"""Tests for the opportunity scorer (RED → GREEN)."""
import pytest
from reddit_validator.scorer import score_opportunity, OpportunityScore


class TestScoreOpportunity:
    """Test scoring logic for SaaS opportunities."""

    def test_high_volume_high_intensity_scores_well(self):
        """High volume + high intensity should yield a strong score."""
        result = score_opportunity(
            mention_count=150,
            avg_sentiment_intensity=0.8,
            competitor_count=2,
        )
        assert isinstance(result, OpportunityScore)
        assert result.score > 60
        assert result.tier in ("A", "B")

    def test_low_volume_scores_poorly(self):
        """Low mention count should yield a weak score."""
        result = score_opportunity(
            mention_count=5,
            avg_sentiment_intensity=0.3,
            competitor_count=10,
        )
        assert result.score < 30
        assert result.tier == "C"

    def test_many_competitors_reduces_score(self):
        """More competitors should reduce the score."""
        few_comp = score_opportunity(100, 0.7, 1)
        many_comp = score_opportunity(100, 0.7, 20)
        assert few_comp.score > many_comp.score

    def test_score_bounds(self):
        """Score should always be between 0 and 100."""
        result = score_opportunity(0, 0.0, 0)
        assert 0 <= result.score <= 100

    def test_tier_assignment(self):
        """Tier should map correctly to score ranges."""
        a_tier = score_opportunity(200, 0.9, 1)
        assert a_tier.tier == "A"

        c_tier = score_opportunity(3, 0.2, 15)
        assert c_tier.tier == "C"
