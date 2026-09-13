"""Validation routes for Reddit opportunity analysis."""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from src.services.reddit_scraper import scrape_subreddit, RedditScraperError
from src.services.llm_analyzer import analyze_pains, LLMAnalyzerError
from src.services.scorer import calculate_opportunity_score, OpportunityScore

logger = logging.getLogger(__name__)

router = APIRouter()


class ValidateRequest(BaseModel):
    """Request body for validation endpoint."""
    subreddit: str = Field(..., description="Subreddit name without r/")
    limit: int = Field(100, ge=1, le=500, description="Max posts to scrape")


class ValidateResponse(BaseModel):
    """Response from validation endpoint."""
    subreddit: str
    overall_score: float
    volume_score: float
    intensity_score: float
    competition_score: float
    pains: list
    report_markdown: str


def validate_subreddit(subreddit: str, limit: int = 100) -> dict:
    """Run full validation pipeline on a subreddit.
    
    Args:
        subreddit: Subreddit name without r/.
        limit: Max posts to scrape.
        
    Returns:
        Dict with scores, pains, and markdown report.
        
    Raises:
        RedditScraperError: If scraping fails.
        LLMAnalyzerError: If analysis fails.
    """
    # Step 1: Scrape posts
    logger.info(f"Scraping r/{subreddit} (limit={limit})")
    posts = scrape_subreddit(subreddit, limit=limit)
    
    if not posts:
        score = calculate_opportunity_score([], total_posts_scraped=0)
        return {
            "subreddit": subreddit,
            **score.to_dict(),
            "report_markdown": score.to_markdown(),
        }
    
    # Step 2: Analyze pains with LLM
    logger.info(f"Analyzing {len(posts)} posts for pain points")
    pains = analyze_pains(posts)
    
    # Step 3: Score the opportunity
    logger.info(f"Scoring opportunity from {len(pains)} pain points")
    score = calculate_opportunity_score(pains, total_posts_scraped=len(posts))
    
    return {
        "subreddit": subreddit,
        **score.to_dict(),
        "report_markdown": score.to_markdown(),
    }


@router.post("/validate", response_model=ValidateResponse)
async def validate_subreddit_endpoint(request: ValidateRequest):
    """Validate a subreddit for SaaS opportunities.
    
    Scrapes posts, analyzes pain points, and scores opportunity.
    """
    try:
        result = validate_subreddit(request.subreddit, limit=request.limit)
        return result
    except RedditScraperError as e:
        logger.error(f"Reddit scraper error: {e}")
        raise HTTPException(status_code=500, detail=f"Reddit scraping failed: {str(e)}")
    except LLMAnalyzerError as e:
        logger.error(f"LLM analyzer error: {e}")
        raise HTTPException(status_code=500, detail=f"LLM analysis failed: {str(e)}")
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