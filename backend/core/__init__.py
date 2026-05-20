"""
Core module for application configuration and utilities.
Exports settings, logging config, and common exceptions.
"""

from backend.core.config import settings, Settings
from backend.core.logging import get_logger
from backend.core.exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
)

__all__ = [
    "settings",
    "Settings",
    "get_logger",
    "AppException",
    "BadRequestException",
    "NotFoundException",
    "UnauthorizedException",
    "ForbiddenException",
]