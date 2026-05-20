"""
Internal API models for database interaction and domain logic.
These are distinct from Pydantic schemas and ORM models.
"""

from backend.api.models.common import TimestampMixin, SoftDeleteMixin

__all__ = ["TimestampMixin", "SoftDeleteMixin"]