"""Tests for the LLM analyzer service."""
import pytest
from unittest.mock import patch, MagicMock
from src.services.llm_analyzer import analyze_pains, LLMAnalyzerError


class TestAnalyzePains:
    """Test suite for analyze_pains function."""

    def test_basic_analysis_returns_list_of_pains(self):
        """Valid input should return a list of pain dicts."""
        posts = [
            {"title": "I hate time management", "body": "It takes too much time", "score": 50},
            {"title": "Project tracking is painful", "body": "I lose track of everything", "score": 30},
        ]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.return_value = [
                {"description": "Time management difficulties", "frequency": 1, "example_post": "I hate time management"},
                {"description": "Project tracking issues", "frequency": 1, "example_post": "Project tracking is painful"},
            ]
            result = analyze_pains(posts)

        assert isinstance(result, list)
        assert len(result) == 2

    def test_empty_posts_returns_empty_list(self):
        """Empty posts input should return empty pains list."""
        result = analyze_pains([])
        assert result == []

    def test_llm_output_parsed_correctly(self):
        """Valid LLM JSON output should be parsed into pain objects."""
        posts = [{"title": "Help with invoicing", "body": "I can't track my invoices", "score": 100}]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.return_value = [
                {"description": "Invoice tracking difficulties", "frequency": 3, "example_post": "Help with invoicing"},
            ]
            result = analyze_pains(posts)

        assert result[0]["description"] == "Invoice tracking difficulties"
        assert result[0]["frequency"] == 3

    def test_llm_error_raises_exception(self):
        """LLM failures should raise LLMAnalyzerError."""
        posts = [{"title": "test", "body": "test", "score": 1}]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.side_effect = Exception("API timeout")
            with pytest.raises(LLMAnalyzerError):
                analyze_pains(posts)

    def test_posts_with_high_upvotes_weighted_higher(self):
        """Posts with more upvotes should carry more weight in analysis."""
        posts = [
            {"title": "Minor issue", "body": "Slight inconvenience", "score": 5},
            {"title": "MAJOR PAIN POINT", "body": "THIS IS UNBEARABLE", "score": 500},
        ]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.return_value = [
                {"description": "MAJOR PAIN POINT", "frequency": 5, "example_post": "MAJOR PAIN POINT"},
                {"description": "Minor issue", "frequency": 1, "example_post": "Minor issue"},
            ]
            result = analyze_pains(posts)

        # High upvote pain should be first or prominent
        assert result[0]["description"] == "MAJOR PAIN POINT"

    def test_handles_malformed_llm_output_gracefully(self):
        """Malformed LLM output should not crash the system."""
        posts = [{"title": "test", "body": "test body", "score": 10}]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.return_value = "not a list"  # type: ignore
            with pytest.raises(LLMAnalyzerError):
                analyze_pains(posts)

    def test_large_post_list_passed_to_llm(self):
        """Many posts should be batched and passed to LLM correctly."""
        posts = [{"title": f"Post {i}", "body": f"Body {i}", "score": i} for i in range(50)]

        with patch("src.services.llm_analyzer._call_llm") as mock_llm:
            mock_llm.return_value = [{"description": "Aggregated pain", "frequency": 10}]
            result = analyze_pains(posts)

            # Should have called LLM with posts data
            call_args = mock_llm.call_args
            assert call_args is not None
            assert len(call_args[0][0]) == 50


class TestLLMAnalyzerError:
    """Test LLMAnalyzerError exception."""

    def test_error_message_preserved(self):
        """Error message should be accessible."""
        err = LLMAnalyzerError("test error")
        assert str(err) == "test error"

    def test_inherits_from_exception(self):
        """Should be catchable as Exception."""
        with pytest.raises(Exception):
            raise LLMAnalyzerError("test")


class TestCallLLM:
    """Test _call_llm helper function."""

    @patch("openai.OpenAI")
    def test_openai_call_returns_parsed_json(self, mock_openai_cls):
        """OpenAI-compatible call should return parsed JSON."""
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='[{"description": "pain"}]'))]
        )
        mock_openai_cls.return_value = mock_client

        with patch("src.services.llm_analyzer.settings") as mock_settings:
            mock_settings.llm_provider = "openai"
            mock_settings.openai_api_key = "test-key"
            mock_settings.openai_model = "gpt-4o-mini"

            from src.services.llm_analyzer import _call_llm
            result = _call_llm([{"title": "test"}])

        assert isinstance(result, list)
        assert result[0]["description"] == "pain"

    @patch("anthropic.Anthropic")
    def test_anthropic_call_returns_parsed_json(self, mock_anthropic_cls):
        """Anthropic call should return parsed JSON."""
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text='[{"description": "pain"}]')]
        )
        mock_anthropic_cls.return_value = mock_client

        with patch("src.services.llm_analyzer.settings") as mock_settings:
            mock_settings.llm_provider = "anthropic"
            mock_settings.anthropic_api_key = "test-key"
            mock_settings.anthropic_model = "claude-sonnet-4-20250514"

            from src.services.llm_analyzer import _call_llm
            result = _call_llm([{"title": "test"}])

        assert isinstance(result, list)
        assert result[0]["description"] == "pain"