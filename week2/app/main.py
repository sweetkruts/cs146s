"""
Main FastAPI application with improved lifecycle management.

Implements proper startup/shutdown events, error handling, and
configuration management for the Action Item Extractor API.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import DatabaseError, init_db
from .routers import action_items, notes

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events properly, ensuring database
    initialization and cleanup.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} in {settings.environment} mode")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Initialize FastAPI app with lifespan management
app = FastAPI(
    title=settings.app_name,
    description="Extract and manage action items from free-form notes",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.debug,
)


# ============================================================================
# Error Handlers
# ============================================================================


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database-related errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed", "error_type": "DatabaseError"},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "error_type": "ValidationError"},
    )


# ============================================================================
# Routes
# ============================================================================


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the frontend HTML page."""
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }


# Include routers
app.include_router(notes.router)
app.include_router(action_items.router)


# Mount static files
static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")