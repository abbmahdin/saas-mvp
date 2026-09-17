"""Reddit scraper service for fetching posts from subreddits."""
import logging
from typing import List, Dict, Any

from src.config import settings

logger = logging.getLogger(__name__)


class RedditScraperError(Exception):
    """Raised when Reddit scraping fails."""
    pass


def scrape_subreddit(subreddit_name: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Scrape posts from a subreddit.
    
    Args:
        subreddit_name: Name of the subreddit (without r/).
        limit: Maximum number of posts to fetch (default 100).
        
    Returns:
        List of post dicts with 'title', 'body', 'score'.
        
    Raises:
        RedditScraperError: If scraping fails.
    """
    try:
        import praw
    except ImportError:
        raise RedditScraperError("praw package is not installed")
    
    try:
        reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )
        
        subreddit = reddit.subreddit(subreddit_name)
        
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append({
                "title": post.title,
                "body": post.selftext,
                "score": post.score,
            })
        
        logger.info(f"Scraped {len(posts)} posts from r/{subreddit_name}")
        return posts
        
    except RedditScraperError:
        raise
    except Exception as e:
        logger.error(f"Failed to scrape r/{subreddit_name}: {e}")
        raise RedditScraperError(f"Reddit scraping failed: {e}")