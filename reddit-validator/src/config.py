"""Configuration settings for Reddit Validator."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Reddit API
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "reddit-validator/1.0"
    
    # LLM Provider
    llm_provider: str = "openai"  # "openai" or "anthropic"
    
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    
    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    
    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/reddit_validator"
    
    # App
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"


settings = Settings()