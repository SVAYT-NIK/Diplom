"""
Backend package for Energy Analytics System.
Provides FastAPI application, database models, services, and API endpoints.
"""

__version__ = "1.0.0"
__author__ = "Energy Analytics Team"

from backend.core import settings, get_logger
from backend.db import Base, get_db_session
from backend.main import create_app

__all__ = [
    "__version__",
    "create_app",
    "settings",
    "get_logger",
    "Base",
    "get_db_session",
]