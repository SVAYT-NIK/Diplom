"""Unit tests for backend.core.config module."""
import pytest
from backend.core.config import Settings


class TestSettings:
    """Tests for Settings class."""

    def test_settings_default_values(self):
        """Test default values of Settings."""
        settings = Settings()
        assert settings.PROJECT_NAME == "Energy Monitoring System"
        assert settings.DEBUG is False
        assert settings.API_V1_PREFIX == "/api/v1"

    def test_settings_from_env(self, monkeypatch):
        """Test Settings loads from environment variables."""
        monkeypatch.setenv("PROJECT_NAME", "Test Project")
        monkeypatch.setenv("DEBUG", "True")
        
        settings = Settings()
        assert settings.PROJECT_NAME == "Test Project"
        assert settings.DEBUG is True
