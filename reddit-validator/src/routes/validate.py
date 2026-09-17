"""Validation routes for SaaS opportunity analysis.

Uses Hacker News API instead of Reddit (Reddit closed self-service API access in 2026).
HN is free, no key needed, perfect for startup/SaaS pain point discovery.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.services.hackernews_scraper import scrape_hackernews, search_pain_points, HackerNewsScraperError
from src.services.reddit_scraper import scrape_subreddit, RedditScraperError
from src.services.llm_analyzer import analyze_pains, LLMAnalyzerError
from src.services.scorer import calculate_opportunity_score, OpportunityScore

logger = logging.getLogger(__name__)

router = APIRouter()


class ValidateRequest(BaseModel):
    """Request body for validation endpoint."""
    subreddit: str = Field("", description="Optional: subreddit name (if empty, uses HN)")
    limit: int = Field(100, ge=1, le=500, description="Max posts/stories to analyze")
    source: str = Field("hackernews", description="Data source: hackernews or reddit")
    query: str = Field("", description="Optional: filter by keywords (comma-separated)")


class ValidateResponse(BaseModel):
    """Response from validation endpoint."""
    source: str
    overall_score: float
    volume_score: float
    intensity_score: float
    competition_score: float
    pains: list
    report_markdown: str


def validate_source(source: str, query: str = "", limit: int = 100, subreddit: str = "") -> dict:
    """Run full validation pipeline on a source.
    
    Args:
        source: 'hackernews' or 'reddit'.
        query: Optional keyword filter.
        limit: Max items to scrape.
        subreddit: Subreddit name (for reddit source only).
    
    Returns:
        Dict with scores, pains, and markdown report.
    """
    # Step 1: Scrape
    logger.info(f"Scraping from {source} (query={query!r}, limit={limit})")
    
    if source == "reddit":
        if not subreddit:
            raise ValueError("subreddit required for reddit source")
        try:
            posts = scrape_subreddit(subreddit, limit=limit)
        except RedditScraperError as e:
            raise HTTPException(status_code=500, detail=f"Reddit scraping failed: {e}")
    else:  # hackernews
        try:
            if query:
                posts = scrape_hackernews(query=query, limit=limit)
            else:
                posts = search_pain_points(niche="saas", limit=limit)
        except HackerNewsScraperError as e:
            raise HTTPException(status_code=500, detail=f"Hacker News scraping failed: {e}")
    
    if not posts:
        score = calculate_opportunity_score([], total_posts_scraped=0)
        return {
            "source": source,
            **score.to_dict(),
            "report_markdown": score.to_markdown(),
        }
    
    # Step 2: Analyze pains with LLM (or fallback if unavailable)
    logger.info(f"Analyzing {len(posts)} posts for pain points")
    try:
        pains = analyze_pains(posts)
        llm_used = True
    except LLMAnalyzerError:
        logger.warning("LLM analyzer failed, using raw posts")
        pains = [{"description": p.get("title", ""), "frequency": 1} for p in posts[:10]]
        llm_used = False
    
    # Step 3: Score the opportunity
    logger.info(f"Scoring opportunity from {len(pains)} pain points")
    score = calculate_opportunity_score(pains, total_posts_scraped=len(posts))
    
    return {
        "source": source,
        "llm_used": llm_used,
        **score.to_dict(),
        "report_markdown": score.to_markdown(),
    }


@router.post("/validate", response_model=ValidateResponse)
async def validate_endpoint(request: ValidateRequest):
    """Validate a niche for SaaS opportunities.
    
    Supports:
    - Hacker News (default, free, no key needed)
    - Reddit (requires API keys, may not work)
    """
    try:
        result = validate_source(
            source=request.source,
            query=request.query,
            limit=request.limit,
            subreddit=request.subreddit,
        )
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.get("/ready")
async def ready_check():
    """Readiness check endpoint."""
    return {"status": "ready"}
