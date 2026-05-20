"""
API module for FastAPI routers, schemas, and endpoint handlers.
Organized into endpoints, schemas (Pydantic models), and internal models.
"""

from backend.api.routers import router as api_router

__version__ = "1.0.0"

__all__ = ["api_router"]