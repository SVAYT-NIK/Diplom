"""Unit tests for backend.core.config module."""
from backend.core.config import Settings
import os


class TestSettings:
    """Tests for Settings class."""

    def test_settings_default_values(self):
        """Test default values of Settings."""
        # Очищаем окружение, чтобы тест использовал дефолтные значения из кода
        os.environ.clear()
        settings = Settings()
        
        # Исправленные имена полей согласно backend/core/config.py
        assert settings.app_name == "Энергоэффективность МКД"
        assert settings.app_version == "1.0.0"
        assert settings.debug is False
        assert settings.environment == "development"
        assert settings.api_prefix == "/api/v1"

    def test_settings_from_env(self, monkeypatch):
        """Test Settings loads from environment variables."""
        # Монкипатчим переменные окружения с правильными именами
        monkeypatch.setenv("APP_NAME", "Test Project")
        monkeypatch.setenv("DEBUG", "True")
        monkeypatch.setenv("ENVIRONMENT", "testing")

        settings = Settings()
        
        # Проверяем, что значения подтянулись из env
        assert settings.app_name == "Test Project"
        assert settings.debug is True
        assert settings.environment == "testing"
