"""LLM analyzer service for extracting pain points from Reddit posts."""
import json
import logging
from typing import List, Dict, Any

from src.config import settings

logger = logging.getLogger(__name__)


class LLMAnalyzerError(Exception):
    """Raised when LLM analysis fails."""
    pass


def _call_llm_unavailable(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Fallback when LLM is unavailable: return posts as-is with basic formatting."""
    logger.warning("LLM unavailable — returning raw posts without analysis")
    return [
        {
            "description": p.get("title", ""),
            "frequency": 1,
            "example_post": p.get("body", p.get("title", ""))[:200],
        }
        for p in posts[:10]
    ]


def _call_llm(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Call the configured LLM to analyze posts.
    Falls back to raw post extraction if LLM unavailable.
    """
    prompt = _build_prompt(posts)
    
    try:
        if settings.llm_provider == "anthropic":
            return _call_anthropic(prompt)
        else:
            return _call_openai(prompt)
    except Exception as e:
        logger.warning(f"LLM call failed ({e}), using fallback extraction")
        return _call_llm_unavailable(posts)


def _build_prompt(posts: List[Dict[str, Any]]) -> str:
    """Build the analysis prompt for the LLM."""
    posts_text = "\n\n".join(
        f"Title: {p.get('title', '')}\nBody: {p.get('body', '')}\nUpvotes: {p.get('score', 0)}"
        for p in posts
    )
    
    return f"""Analyze the following Reddit posts and extract recurring pain points.
For each pain point, provide:
- description: A concise description of the pain point
- frequency: How many times this pain appears (integer)
- example_post: A representative title or snippet

Return ONLY a JSON array of objects. No explanation, no markdown formatting.

Posts:
{posts_text}"""


def _call_openai(prompt: str) -> List[Dict[str, Any]]:
    """Call OpenAI-compatible API.
    
    Supports both OpenAI and OpenRouter (auto-detected by key prefix).
    """
    import openai
    
    api_key = settings.openai_api_key
    base_url = None
    model = settings.openai_model
    
    # Auto-detect OpenRouter by key prefix
    if api_key.startswith("sk-or-"):
        base_url = "https://openrouter.ai/api/v1"
    
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful analyst that extracts pain points from posts. Respond with valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    
    content = response.choices[0].message.content
    return _parse_llm_response(content)


def _call_anthropic(prompt: str) -> List[Dict[str, Any]]:
    """Call Anthropic API."""
    import anthropic
    
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=4096,
        system="You are a helpful analyst that extracts pain points from Reddit posts. Respond with valid JSON only.",
        messages=[{"role": "user", "content": prompt}],
    )
    
    content = response.content[0].text
    return _parse_llm_response(content)


def _parse_llm_response(content: str) -> List[Dict[str, Any]]:
    """Parse the LLM response into a list of pain dicts."""
    if not isinstance(content, str):
        raise LLMAnalyzerError(f"Expected string response, got {type(content)}")
    
    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1] if "\n" in content else content
        if content.endswith("```"):
            content = content[:-3]
    content = content.strip()
    
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise LLMAnalyzerError(f"Failed to parse LLM response as JSON: {e}")
    
    if not isinstance(data, list):
        raise LLMAnalyzerError(f"Expected JSON array, got {type(data).__name__}")
    
    # Validate and normalize each item
    pains = []
    for item in data:
        if not isinstance(item, dict):
            continue
        pain = {
            "description": str(item.get("description", "")),
            "frequency": int(item.get("frequency", 1)),
        }
        if "example_post" in item:
            pain["example_post"] = str(item["example_post"])
        pains.append(pain)
    
    return pains


def analyze_pains(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Analyze Reddit posts to extract pain points.
    
    Args:
        posts: List of post dicts with 'title', 'body', 'score'.
        
    Returns:
        List of pain point dicts with 'description', 'frequency', etc.
    """
    if not posts:
        return []

    # Call LLM to analyze posts
    try:
        pains = _call_llm(posts)
    except LLMAnalyzerError:
        raise
    except Exception as e:
        raise LLMAnalyzerError(f"LLM analysis failed: {e}")

    if not isinstance(pains, list):
        raise LLMAnalyzerError(
            f"Expected list from LLM, got {type(pains).__name__}"
        )

    return pains