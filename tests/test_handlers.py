"""Тесты для модуля handlers."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types

from src.config import Config
from src.handlers import MessageHandler


@pytest.fixture
def config(monkeypatch):
    """Фикстура для создания тестовой конфигурации."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "test_model")
    monkeypatch.setenv("SYSTEM_PROMPT", "Test prompt")
    return Config()


@pytest.fixture
def message_handler(config):
    """Фикстура для создания MessageHandler."""
    return MessageHandler(config)


@pytest.mark.asyncio
async def test_start_command(message_handler, monkeypatch):
    """Тест обработчика команды /start."""
    # Создаем мок объект сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 456
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 123

    # Мокаем метод answer
    mock_message.answer = AsyncMock()

    # Вызываем обработчик
    await message_handler.start_command(mock_message)

    # Проверяем, что answer был вызван один раз
    mock_message.answer.assert_called_once()

    # Получаем текст, который был передан в answer
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    # Проверяем содержание ответа
    assert "Привет" in response_text
    assert "AI-ассистент" in response_text
    assert "/reset" in response_text


def test_message_handler_initialization(config):
    """Тест инициализации MessageHandler."""
    handler = MessageHandler(config)
    assert handler.config == config

