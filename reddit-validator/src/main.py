"""Main FastAPI application for Reddit Validator."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.validate import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Reddit Validator",
    description="SaaS opportunity validation from Reddit pain points",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Reddit Validator API", "docs": "/docs"}