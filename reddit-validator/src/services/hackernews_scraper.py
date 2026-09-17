"""Hacker News scraper service for fetching pain points.

Replaced Reddit API (requires approval since 2026) with Hacker News API.
HN is free, no key needed, perfect for SaaS/startup pain point discovery.
"""
import logging
import urllib.request
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


class HackerNewsScraperError(Exception):
    pass


def fetch_story(story_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single HN story by ID."""
    url = f"{HN_API_BASE}/item/{story_id}.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        logger.warning(f"Failed to fetch story {story_id}: {e}")
        return None


def scrape_hackernews(
    query: str = "",
    limit: int = 100,
    min_score: int = 5,
    story_type: str = "top",  # top, new, best, ask, show, job
) -> List[Dict[str, Any]]:
    """Scrape Hacker News for pain points.
    
    Args:
        query: Filter stories by keywords (optional).
        limit: Maximum stories to return.
        min_score: Minimum score threshold.
        story_type: Type of stories (top/new/best/ask/show/job).
    
    Returns:
        List of story dicts with 'title', 'body', 'score', 'url', 'timestamp'.
    """
    try:
        # Get story IDs
        if story_type not in ("top", "new", "best", "ask", "show", "job"):
            story_type = "top"
        
        url = f"{HN_API_BASE}/{story_type}stories.json"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            story_ids = json.loads(resp.read().decode())
        
        stories = []
        for sid in story_ids[: limit * 3]:  # fetch extra to filter
            if len(stories) >= limit:
                break
            
            story = fetch_story(sid)
            if not story or story.get("type") != "story":
                continue
            
            score = story.get("score", 0)
            if score < min_score:
                continue
            
            title = story.get("title", "")
            
            # Filter by query if provided
            if query:
                keywords = [k.strip().lower() for k in query.split(",")]
                title_lower = title.lower()
                if not any(kw in title_lower for kw in keywords):
                    continue
            
            stories.append({
                "title": title,
                "body": story.get("text", ""),  # text field for Ask HN etc.
                "score": score,
                "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                "timestamp": datetime.fromtimestamp(story.get("time", 0)).isoformat(),
                "source": "hackernews",
            })
        
        logger.info(f"Scraped {len(stories)} stories from Hacker News (query={query!r})")
        return stories
        
    except urllib.error.URLError as e:
        raise HackerNewsScraperError(f"Hacker News API error: {e}")
    except Exception as e:
        logger.error(f"Failed to scrape HN: {e}")
        raise HackerNewsScraperError(f"Scraping failed: {e}")


def search_pain_points(
    niche: str = "saas",
    limit: int = 50,
    min_score: int = 5,
) -> List[Dict[str, Any]]:
    """Search HN for pain points in a specific niche.
    
    Combines multiple story types (top, ask, show) for comprehensive coverage.
    No keyword filtering — returns all stories, letting the LLM identify pain points.
    
    Args:
        niche: SaaS niche to search for (unused, kept for API compatibility).
        limit: Maximum results.
        min_score: Minimum score threshold.
    
    Returns:
        Deduplicated list of stories sorted by score.
    """
    all_stories: Dict[int, Dict[str, Any]] = {}
    
    for story_type in ["top", "ask"]:
        try:
            stories = scrape_hackernews(
                query="",
                limit=limit * 2,  # fetch extra for dedup
                min_score=min_score,
                story_type=story_type,
            )
            for s in stories:
                key = hash(s["title"])
                if key not in all_stories:
                    all_stories[key] = s
        except HackerNewsScraperError:
            continue
    
    results = list(all_stories.values())
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]
