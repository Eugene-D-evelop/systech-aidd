"""Тесты для модуля config."""

import pytest
from dotenv import load_dotenv
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
    # Удаляем все обязательные переменные окружения
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    monkeypatch.delenv("SYSTEM_PROMPT", raising=False)

    # Устанавливаем только часть
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_api_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test_model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")

    from src.config import Config

    with pytest.raises(ValidationError):
        Config()


def test_config_from_real_env():
    """Тест загрузки реальной конфигурации из .env файла."""
    # Загружаем реальные переменные из .env
    load_dotenv()

    from src.config import Config

    config = Config()

    # Проверяем что все обязательные поля загружены
    assert config.telegram_bot_token is not None
    assert len(config.telegram_bot_token) > 0

    assert config.openrouter_api_key is not None
    assert len(config.openrouter_api_key) > 0

    assert config.openrouter_model is not None
    assert len(config.openrouter_model) > 0

    assert config.system_prompt is not None
    assert len(config.system_prompt) > 0

    # Проверяем значения по умолчанию или кастомные
    assert config.max_history_length > 0
    assert 0.0 <= config.temperature <= 2.0
    assert config.max_tokens > 0
    assert config.timeout > 0


def test_config_telegram_token_format():
    """Тест формата Telegram токена из реальной конфигурации."""
    load_dotenv()

    from src.config import Config

    config = Config()

    # Telegram токен должен содержать двоеточие
    assert ":" in config.telegram_bot_token

    # Должен состоять из двух частей
    parts = config.telegram_bot_token.split(":")
    assert len(parts) == 2

    # Первая часть (bot ID) должна быть числом
    assert parts[0].isdigit()

    # Вторая часть должна быть не пустой
    assert len(parts[1]) > 0
