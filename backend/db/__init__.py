"""
Database module for SQLAlchemy models and session management.
Exports Base, async session factory, and all ORM models.
"""

from backend.db.base import Base
from backend.db.session import get_db, AsyncSessionLocal

# Alias for backward compatibility
get_db_session = get_db

__all__ = [
    "Base",
    "get_db",
    "get_db_session",
    "AsyncSessionLocal",
]