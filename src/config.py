"""Конфигурация приложения через переменные окружения."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Конфигурация бота с валидацией через Pydantic."""

    # Обязательные параметры
    telegram_bot_token: str
    openrouter_api_key: str
    openrouter_model: str
    system_prompt: str

    # Опциональные параметры с дефолтами
    max_history_length: int = 10
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
