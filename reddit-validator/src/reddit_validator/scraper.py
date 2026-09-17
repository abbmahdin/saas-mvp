"""Reddit pain-point scraper (MVP: subreddit scan → JSON output)."""
import httpx
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PainPoint:
    """A pain point extracted from a Reddit post."""
    subreddit: str
    title: str
    url: str
    upvotes: int
    comment_count: int
    pain_keywords: list[str]


PAIN_KEYWORDS = [
    "annoyed", "frustrated", "wish there was", "alternative to",
    "too expensive", "doesn't work", "waste of time", "sucks",
    "terrible", "garbage", "broken", "pain point", "struggle with",
    "any tool for", "looking for", "recommend a tool",
]


async def scan_subreddit(
    subreddit: str,
    limit: int = 50,
    min_upvotes: int = 5,
) -> list[PainPoint]:
    """Scan a subreddit for pain-point posts.
    
    Uses Reddit's public JSON API (no auth required for read-only).
    """
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {"User-Agent": "reddit-validator/0.1 (research tool)"}
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    
    points = []
    for post in data.get("data", {}).get("children", []):
        post_data = post.get("data", {})
        title = post_data.get("title", "").lower()
        
        # Check for pain keywords
        found_keywords = [kw for kw in PAIN_KEYWORDS if kw in title]
        if not found_keywords:
            continue
        
        upvotes = post_data.get("ups", 0)
        if upvotes < min_upvotes:
            continue
        
        points.append(PainPoint(
            subreddit=subreddit,
            title=post_data.get("title", ""),
            url=f"https://reddit.com{post_data.get('permalink', '')}",
            upvotes=upvotes,
            comment_count=post_data.get("num_comments", 0),
            pain_keywords=found_keywords,
        ))
    
    return sorted(points, key=lambda p: p.upvotes, reverse=True)
