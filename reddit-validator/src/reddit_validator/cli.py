"""Reddit Validator CLI."""
import asyncio
import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from reddit_validator.scraper import scan_subreddit, PainPoint
from reddit_validator.scorer import score_opportunity

app = typer.Typer()
console = Console()


@app.command()
def scan(
    subreddit: str = typer.Argument(..., help="Subreddit to scan (e.g., SaaS, startup)"),
    limit: int = typer.Option(50, "--limit", "-l", help="Number of posts to scan"),
    min_upvotes: int = typer.Option(5, "--min-upvotes", "-m", help="Minimum upvotes filter"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output JSON file"),
) -> None:
    """Scan a subreddit for SaaS pain points."""
    console.print(f"[bold blue]Scanning r/{subreddit}...[/]")
    
    points: list[PainPoint] = asyncio.run(scan_subreddit(subreddit, limit, min_upvotes))
    
    if not points:
        console.print("[yellow]No pain points found.[/]")
        return
    
    # Score each point
    results = []
    for p in points:
        score = score_opportunity(
            mention_count=p.upvotes,
            avg_sentiment_intensity=len(p.pain_keywords) / 5.0,
            competitor_count=0,  # Not detected in MVP
        )
        results.append({
            "subreddit": p.subreddit,
            "title": p.title,
            "url": p.url,
            "upvotes": p.upvotes,
            "pain_keywords": p.pain_keywords,
            "opportunity_score": score.score,
            "tier": score.tier,
        })
    
    # Display table
    table = Table(title=f"r/{subreddit} — Pain Points")
    table.add_column("Upvotes", style="cyan")
    table.add_column("Title", max_width=60)
    table.add_column("Score", style="green")
    table.add_column("Tier", style="bold")
    
    for r in results:
        table.add_row(
            str(r["upvotes"]),
            r["title"][:60],
            str(r["opportunity_score"]),
            r["tier"],
        )
    
    console.print(table)
    
    if output:
        with open(output, "w") as f:
            json.dump(results, f, indent=2)
        console.print(f"[green]Saved to {output}[/]")


if __name__ == "__main__":
    app()
