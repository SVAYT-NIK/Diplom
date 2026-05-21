"""
Core module for application configuration and utilities.
Exports settings, logging config, and common exceptions.
"""

from backend.core.config import Settings, get_settings

# Create settings instance for backward compatibility
settings = get_settings()

__all__ = [
    "settings",
    "Settings",
    "get_settings",
]