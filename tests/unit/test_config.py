"""Unit tests for the backend."""

import pytest
from backend.core.config import Settings


def test_settings_default_values():
    """Test that Settings has correct default values."""
    settings = Settings()
    assert settings.project_name == "Energy Monitoring System"
    assert settings.debug is False


def test_settings_project_name():
    """Test custom project name."""
    settings = Settings(project_name="Custom Project")
    assert settings.project_name == "Custom Project"
