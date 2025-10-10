"""Тесты для модуля config."""

import pytest
from pydantic import ValidationError


def test_config_with_valid_env(monkeypatch):
    """Тест успешной загрузки конфигурации с валидными данными."""
    # Устанавливаем переменные окружения для теста
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_api_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test_model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Test system prompt")

    from src.config import Config

    config = Config()

    assert config.telegram_bot_token == "test_bot_token"
    assert config.openrouter_api_key == "test_api_key"
    assert config.openrouter_model == "test_model"
    assert config.system_prompt == "Test system prompt"
    assert config.max_history_length == 10
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.timeout == 60


def test_config_with_custom_values(monkeypatch):
    """Тест загрузки конфигурации с кастомными значениями опциональных полей."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_bot_token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_api_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test_model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
    monkeypatch.setenv("MAX_HISTORY_LENGTH", "20")
    monkeypatch.setenv("TEMPERATURE", "0.9")
    monkeypatch.setenv("MAX_TOKENS", "2000")
    monkeypatch.setenv("TIMEOUT", "120")

    from src.config import Config

    config = Config()

    assert config.max_history_length == 20
    assert config.temperature == 0.9
    assert config.max_tokens == 2000
    assert config.timeout == 120


def test_config_missing_required_field(monkeypatch):
    """Тест ошибки при отсутствии обязательного поля."""
    # Не устанавливаем TELEGRAM_BOT_TOKEN
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_api_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test_model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")

    from src.config import Config

    with pytest.raises(ValidationError):
        Config()

