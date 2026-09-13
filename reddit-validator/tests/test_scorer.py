"""Tests for the opportunity scorer."""
import pytest
from src.services.scorer import calculate_opportunity_score, OpportunityScore


class TestCalculateOpportunityScore:
    """Test suite for calculate_opportunity_score function."""

    def test_basic_scoring_returns_correct_structure(self):
        """Test that scoring returns an OpportunityScore with all fields."""
        pains = [
            {"description": "I struggle with time tracking", "frequency": 5, "upvotes": 50},
            {"description": "Project management is overwhelming", "frequency": 3, "upvotes": 30},
        ]
        result = calculate_opportunity_score(pains, total_posts_scraped=100)

        assert isinstance(result, OpportunityScore)
        assert hasattr(result, "volume_score")
        assert hasattr(result, "intensity_score")
        assert hasattr(result, "competition_score")
        assert hasattr(result, "overall_score")
        assert hasattr(result, "pains")

    def test_higher_frequency_increases_volume_score(self):
        """Higher frequency of mentions should increase volume score."""
        high_freq_pains = [
            {"description": "X pain", "frequency": 20, "upvotes": 200},
        ]
        low_freq_pains = [
            {"description": "Y pain", "frequency": 1, "upvotes": 10},
        ]

        high_score = calculate_opportunity_score(high_freq_pains, total_posts_scraped=100)
        low_score = calculate_opportunity_score(low_freq_pains, total_posts_scraped=100)

        assert high_score.volume_score > low_score.volume_score

    def test_higher_upvotes_increases_intensity_score(self):
        """More upvotes on pain posts indicates higher intensity."""
        high_intensity = [
            {"description": "Pain A", "frequency": 5, "upvotes": 500},
        ]
        low_intensity = [
            {"description": "Pain B", "frequency": 5, "upvotes": 5},
        ]

        high_score = calculate_opportunity_score(high_intensity, total_posts_scraped=100)
        low_score = calculate_opportunity_score(low_intensity, total_posts_scraped=100)

        assert high_score.intensity_score > low_score.intensity_score

    def test_more_total_posts_reduces_volume_score(self):
        """Pain mentions in a larger pool of posts means lower relative volume."""
        pains = [{"description": "Same pain", "frequency": 5, "upvotes": 50}]

        small_pool = calculate_opportunity_score(pains, total_posts_scraped=50)
        large_pool = calculate_opportunity_score(pains, total_posts_scraped=5000)

        assert small_pool.volume_score > large_pool.volume_score

    def test_competition_penalty_reduces_score(self):
        """Existing solutions mentioned in posts should reduce competition score."""
        pains_with_competition = [
            {"description": "Pain with many solutions", "frequency": 5, "upvotes": 50, "existing_solutions_mentioned": 10},
        ]
        pains_no_competition = [
            {"description": "Pain with no solutions", "frequency": 5, "upvotes": 50, "existing_solutions_mentioned": 0},
        ]

        comp_score = calculate_opportunity_score(pains_with_competition, total_posts_scraped=100)
        no_comp_score = calculate_opportunity_score(pains_no_competition, total_posts_scraped=100)

        assert comp_score.competition_score < no_comp_score.competition_score

    def test_overall_score_is_weighted_average(self):
        """Overall score should combine volume, intensity, and competition."""
        pains = [{"description": "Test pain", "frequency": 10, "upvotes": 100}]
        result = calculate_opportunity_score(pains, total_posts_scraped=100)

        # Weights: volume=0.3, intensity=0.4, competition=0.3
        expected = 0.3 * result.volume_score + 0.4 * result.intensity_score + 0.3 * result.competition_score
        assert abs(result.overall_score - expected) < 0.01

    def test_empty_pains_list_returns_zero_scores(self):
        """No pains found should result in zero scores."""
        result = calculate_opportunity_score([], total_posts_scraped=100)

        assert result.volume_score == 0
        assert result.intensity_score == 0
        assert result.competition_score == 100  # No competition if no pains
        assert result.overall_score == 30.0  # Only competition contributes

    def test_scores_are_normalized_0_to_100(self):
        """All scores must be between 0 and 100."""
        pains = [
            {"description": "A", "frequency": 50, "upvotes": 1000, "existing_solutions_mentioned": 0},
            {"description": "B", "frequency": 1, "upvotes": 1, "existing_solutions_mentioned": 100},
        ]
        result = calculate_opportunity_score(pains, total_posts_scraped=50)

        for score_val in [result.volume_score, result.intensity_score, result.competition_score, result.overall_score]:
            assert 0 <= score_val <= 100

    def test_pains_output_matches_input(self):
        """Output pains should include enriched data from scoring."""
        pains = [{"description": "Time tracking", "frequency": 5, "upvotes": 50}]
        result = calculate_opportunity_score(pains, total_posts_scraped=100)

        assert len(result.pains) == 1
        assert result.pains[0]["description"] == "Time tracking"

    def test_multiple_pains_aggregate_correctly(self):
        """Multiple pains should aggregate their metrics for scoring."""
        pains = [
            {"description": "Pain 1", "frequency": 10, "upvotes": 100},
            {"description": "Pain 2", "frequency": 20, "upvotes": 200},
            {"description": "Pain 3", "frequency": 30, "upvotes": 300},
        ]
        result = calculate_opportunity_score(pains, total_posts_scraped=100)

        # Total frequency = 60, should yield a high volume score
        assert result.volume_score > 50
        assert result.intensity_score > 50


class TestOpportunityScore:
    """Test the OpportunityScore dataclass."""

    def test_to_dict_returns_serializable(self):
        """to_dict should return a JSON-serializable dict."""
        score = OpportunityScore(
            volume_score=75.0,
            intensity_score=80.0,
            competition_score=60.0,
            overall_score=72.0,
            pains=[{"description": "test"}],
        )
        d = score.to_dict()
        assert isinstance(d, dict)
        assert d["volume_score"] == 75.0
        assert d["overall_score"] == 72.0

    def test_to_markdown_returns_string(self):
        """to_markdown should generate a markdown report."""
        score = OpportunityScore(
            volume_score=75.0,
            intensity_score=80.0,
            competition_score=60.0,
            overall_score=72.0,
            pains=[{"description": "test pain", "frequency": 5}],
        )
        md = score.to_markdown()
        assert isinstance(md, str)
        assert "# Opportunity Report" in md
        assert "72.0" in md