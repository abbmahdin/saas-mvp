"""Opportunity scorer for SaaS ideas extracted from Reddit."""
from dataclasses import dataclass
from typing import Literal

Tier = Literal["A", "B", "C"]


@dataclass
class OpportunityScore:
    """Score result for a potential SaaS opportunity."""
    score: float
    tier: Tier
    mention_count: int
    avg_intensity: float
    competitor_count: int


def score_opportunity(
    mention_count: int,
    avg_sentiment_intensity: float,
    competitor_count: int,
) -> OpportunityScore:
    """Score a SaaS opportunity based on Reddit signals.
    
    Algorithm:
    - Volume component (0-40): log-scaled mention count
    - Intensity component (0-40): sentiment intensity (pain/urgency)
    - Competition penalty (0-20): more competitors = lower score
    """
    import math
    
    # Volume: log-scaled, capped at 40
    volume = min(40.0, 10.0 * math.log1p(mention_count))
    
    # Intensity: linear 0-40
    intensity = max(0.0, min(40.0, avg_sentiment_intensity * 40.0))
    
    # Competition: inverse, capped at 20
    competition = max(0.0, 20.0 - (competitor_count * 2.0))
    
    score = volume + intensity + competition
    score = max(0.0, min(100.0, score))
    
    # Tier assignment
    if score >= 70:
        tier: Tier = "A"
    elif score >= 40:
        tier = "B"
    else:
        tier = "C"
    
    return OpportunityScore(
        score=round(score, 2),
        tier=tier,
        mention_count=mention_count,
        avg_intensity=avg_sentiment_intensity,
        competitor_count=competitor_count,
    )
