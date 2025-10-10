"""Тесты для модуля handlers."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types
from dotenv import load_dotenv

from src.config import Config
from src.conversation import Conversation
from src.handlers import MessageHandler
from src.llm_client import LLMClient

# Загружаем реальную конфигурацию
load_dotenv()


@pytest.fixture
def config():
    """Фикстура для создания реальной конфигурации из .env."""
    return Config()


@pytest.fixture
def conversation():
    """Фикстура для создания Conversation."""
    return Conversation()


@pytest.fixture
def llm_client(config):
    """Фикстура для создания LLMClient."""
    return LLMClient(config)


@pytest.fixture
def message_handler(config, llm_client, conversation):
    """Фикстура для создания MessageHandler с реальными зависимостями."""
    return MessageHandler(config, llm_client, conversation)


@pytest.mark.asyncio
async def test_start_command(message_handler):
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


@pytest.mark.asyncio
async def test_reset_command(message_handler, conversation):
    """Тест обработчика команды /reset."""
    # Создаем мок объект сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 456
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 123
    mock_message.answer = AsyncMock()

    # Добавляем сообщения в историю
    conversation.add_message(123, 456, "user", "Test message 1")
    conversation.add_message(123, 456, "assistant", "Response 1")

    # Проверяем что история есть
    assert len(conversation.get_history(123, 456)) == 2

    # Вызываем reset
    await message_handler.reset_command(mock_message)

    # Проверяем что история очищена
    assert len(conversation.get_history(123, 456)) == 0

    # Проверяем что был отправлен ответ
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]
    assert "очищена" in response_text.lower()


@pytest.mark.asyncio
@pytest.mark.slow
async def test_handle_message_real_llm(message_handler, conversation):
    """Интеграционный тест обработки сообщения с реальным LLM."""
    # Создаем мок объект сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 789
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 456
    mock_message.text = "Say 'test passed' and nothing else"
    mock_message.answer = AsyncMock()

    # Мокаем bot для send_chat_action
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Вызываем обработчик
    await message_handler.handle_message(mock_message)

    # Проверяем что typing action был отправлен
    mock_bot.send_chat_action.assert_called_once_with(456, "typing")

    # Проверяем что ответ был отправлен
    mock_message.answer.assert_called_once()

    # Получаем ответ
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    # Проверяем что ответ не пустой
    assert response_text is not None
    assert len(response_text) > 0

    # Проверяем что история сохранена (2 сообщения: user + assistant)
    history = conversation.get_history(456, 789)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Say 'test passed' and nothing else"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == response_text


@pytest.mark.asyncio
async def test_handle_message_conversation_context(message_handler, conversation):
    """Тест что handle_message использует контекст диалога."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 111
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 222
    mock_message.text = "What is my name?"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Добавляем предыдущий контекст
    conversation.add_message(222, 111, "user", "My name is Bob")
    conversation.add_message(222, 111, "assistant", "Nice to meet you, Bob!")

    # Вызываем обработчик
    await message_handler.handle_message(mock_message)

    # Проверяем что ответ был отправлен
    mock_message.answer.assert_called_once()

    # Проверяем что теперь в истории 4 сообщения
    history = conversation.get_history(222, 111)
    assert len(history) == 4


@pytest.mark.asyncio
async def test_handle_message_without_text(message_handler):
    """Тест обработки сообщения без текста."""
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 333
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 444
    mock_message.text = None  # Сообщение без текста
    mock_message.answer = AsyncMock()

    # Вызываем обработчик - не должно быть ошибок
    await message_handler.handle_message(mock_message)

    # answer не должен быть вызван
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_without_user(message_handler):
    """Тест обработки сообщения без пользователя."""
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = None  # Нет пользователя
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 555
    mock_message.text = "Test"
    mock_message.answer = AsyncMock()

    # Вызываем обработчик - не должно быть ошибок
    await message_handler.handle_message(mock_message)

    # answer не должен быть вызван
    mock_message.answer.assert_not_called()


def test_message_handler_initialization(config, llm_client, conversation):
    """Тест инициализации MessageHandler."""
    handler = MessageHandler(config, llm_client, conversation)
    assert handler.config == config
    assert handler.llm_client == llm_client
    assert handler.conversation == conversation
