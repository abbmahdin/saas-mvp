"""Tests for the Reddit scraper service."""
import pytest
from unittest.mock import patch, MagicMock, call
from src.services.reddit_scraper import scrape_subreddit, RedditScraperError


class TestScrapeSubreddit:
    """Test suite for scrape_subreddit function."""

    def test_basic_scrape_returns_posts_list(self):
        """Valid scrape should return list of post dicts."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit

            mock_post1 = MagicMock()
            mock_post1.title = "I need help with invoicing"
            mock_post1.selftext = "I can't manage my invoices properly"
            mock_post1.score = 50

            mock_post2 = MagicMock()
            mock_post2.title = "Project management pain"
            mock_post2.selftext = "Tracking projects is hard"
            mock_post2.score = 30

            mock_subreddit.hot.return_value = [mock_post1, mock_post2]
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test", limit=2)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "I need help with invoicing"

    def test_post_structure_has_required_fields(self):
        """Each post should have title, body, score."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit

            mock_post = MagicMock()
            mock_post.title = "Test"
            mock_post.selftext = "Body text"
            mock_post.score = 10

            mock_subreddit.hot.return_value = [mock_post]
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test", limit=1)

        assert "title" in result[0]
        assert "body" in result[0]
        assert "score" in result[0]

    def test_empty_subreddit_returns_empty_list(self):
        """Subreddit with no posts returns empty list."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit
            mock_subreddit.hot.return_value = []
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test", limit=10)

        assert result == []

    def test_limit_parameter_respected(self):
        """Limit parameter should cap the number of posts returned."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit

            posts = []
            for i in range(50):
                p = MagicMock()
                p.title = f"Post {i}"
                p.selftext = f"Body {i}"
                p.score = i
                posts.append(p)

            # Mock hot() to respect the limit parameter
            def mock_hot(limit=None):
                return posts[:limit] if limit else posts

            mock_subreddit.hot.side_effect = mock_hot
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test", limit=5)

        assert len(result) == 5

    def test_praw_error_raises_reddit_scraper_error(self):
        """PRAW errors should raise RedditScraperError."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit_cls.side_effect = Exception("Invalid credentials")
            with pytest.raises(RedditScraperError):
                scrape_subreddit("test")

    def test_selftext_empty_string_handled(self):
        """Posts with empty selftext should have empty body."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit

            mock_post = MagicMock()
            mock_post.title = "Image post"
            mock_post.selftext = ""
            mock_post.score = 5

            mock_subreddit.hot.return_value = [mock_post]
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test", limit=1)

        assert result[0]["body"] == ""

    def test_default_limit_is_100(self):
        """Default limit should be 100."""
        with patch("praw.Reddit") as mock_reddit_cls:
            mock_reddit = MagicMock()
            mock_subreddit = MagicMock()
            mock_reddit.subreddit.return_value = mock_subreddit

            posts = []
            for i in range(150):
                p = MagicMock()
                p.title = f"Post {i}"
                p.selftext = f"Body {i}"
                p.score = i
                posts.append(p)

            def mock_hot(limit=None):
                return posts[:limit] if limit else posts

            mock_subreddit.hot.side_effect = mock_hot
            mock_reddit_cls.return_value = mock_reddit

            result = scrape_subreddit("test")

        assert len(result) == 100


class TestRedditScraperError:
    """Test RedditScraperError exception."""

    def test_error_message_preserved(self):
        """Error message should be accessible."""
        err = RedditScraperError("test error")
        assert str(err) == "test error"

    def test_inherits_from_exception(self):
        """Should be catchable as Exception."""
        with pytest.raises(Exception):
            raise RedditScraperError("test")
