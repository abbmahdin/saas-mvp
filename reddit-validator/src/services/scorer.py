"""Scoring service for Reddit opportunity analysis."""
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class OpportunityScore:
    """Represents the scored opportunity for a subreddit."""
    volume_score: float
    intensity_score: float
    competition_score: float
    overall_score: float
    pains: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "volume_score": self.volume_score,
            "intensity_score": self.intensity_score,
            "competition_score": self.competition_score,
            "overall_score": self.overall_score,
            "pains": self.pains,
        }

    def to_markdown(self) -> str:
        """Generate a markdown report."""
        lines = [
            "# Opportunity Report",
            "",
            f"## Overall Score: {self.overall_score:.1f}/100",
            "",
            "### Score Breakdown",
            "",
            f"| Metric | Score |",
            f"|--------|-------|",
            f"| Volume | {self.volume_score:.1f} |",
            f"| Intensity | {self.intensity_score:.1f} |",
            f"| Competition | {self.competition_score:.1f} |",
            "",
            "### Pain Points Identified",
            "",
        ]
        for i, pain in enumerate(self.pains, 1):
            freq = pain.get("frequency", 0)
            desc = pain.get("description", "Unknown")
            lines.append(f"{i}. **{desc}** (frequency: {freq})")
        lines.append("")
        return "\n".join(lines)


def calculate_opportunity_score(
    pains: List[Dict[str, Any]],
    total_posts_scraped: int,
) -> OpportunityScore:
    """Calculate opportunity score from pain analysis.

    Args:
        pains: List of pain dicts with 'description', 'frequency', 'upvotes',
               optionally 'existing_solutions_mentioned'.
        total_posts_scraped: Total number of posts scraped from subreddit.

    Returns:
        OpportunityScore with volume, intensity, competition, and overall scores.
    """
    if not pains:
        return OpportunityScore(
            volume_score=0.0,
            intensity_score=0.0,
            competition_score=100.0,
            overall_score=30.0,
            pains=[],
        )

    total_frequency = sum(p.get("frequency", 0) for p in pains)
    total_upvotes = sum(p.get("upvotes", 0) for p in pains)
    total_solutions = sum(p.get("existing_solutions_mentioned", 0) for p in pains)

    # Volume: frequency of pain mentions relative to total posts scraped
    volume_score = min(100.0, (total_frequency / max(total_posts_scraped, 1)) * 200)

    # Intensity: average upvotes per pain mention (higher = more intense)
    avg_upvotes_per_mention = total_upvotes / max(total_frequency, 1)
    intensity_score = min(100.0, avg_upvotes_per_mention * 10)

    # Competition: inversely related to existing solutions mentioned
    # More solutions = lower opportunity
    competition_score = 100.0 / (1.0 + (total_solutions / 10.0))

    # Weighted overall score
    overall_score = (
        0.3 * volume_score
        + 0.4 * intensity_score
        + 0.3 * competition_score
    )

    return OpportunityScore(
        volume_score=round(volume_score, 2),
        intensity_score=round(intensity_score, 2),
        competition_score=round(competition_score, 2),
        overall_score=round(overall_score, 2),
        pains=pains,
    )