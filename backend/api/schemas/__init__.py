"""
Pydantic schemas for request/response validation.
Organized by domain: auth, metering, analytics, reports, common.
"""

from backend.api.schemas.common import BaseResponse, PaginatedResponse
from backend.api.schemas.auth import TokenData, UserCreate, UserLogin

__all__ = [
    "BaseResponse",
    "PaginatedResponse",
    "TokenData",
    "UserCreate",
    "UserLogin",
]