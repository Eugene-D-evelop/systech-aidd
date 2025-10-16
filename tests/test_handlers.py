"""Тесты для модуля handlers."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from openai import APIError, APITimeoutError

from src.config import Config
from src.conversation import Conversation
from src.handlers import MessageHandler
from src.llm_client import LLMClient, LLMError


@pytest.fixture
def config():
    """Фикстура для создания тестовой конфигурации."""
    return Config(
        telegram_bot_token="test_bot_token_123",
        openrouter_api_key="test_api_key_456",
        openrouter_model="test/model",
        system_prompt="You are a test assistant",
    )


@pytest.fixture
def conversation(database):
    """Фикстура для создания Conversation с БД."""
    return Conversation(database)


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
    assert "Python Code Reviewer" in response_text
    assert "/role" in response_text
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
    await conversation.add_message(123, 456, "user", "Test message 1")
    await conversation.add_message(123, 456, "assistant", "Response 1")

    # Проверяем что история есть
    assert len(await conversation.get_history(123, 456)) == 2

    # Вызываем reset
    await message_handler.reset_command(mock_message)

    # Проверяем что история очищена
    assert len(await conversation.get_history(123, 456)) == 0

    # Проверяем что был отправлен ответ
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]
    assert "очищена" in response_text.lower()


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.integration
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
    history = await conversation.get_history(456, 789)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Say 'test passed' and nothing else"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == response_text


@pytest.mark.asyncio
@pytest.mark.integration
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
    await conversation.add_message(222, 111, "user", "My name is Bob")
    await conversation.add_message(222, 111, "assistant", "Nice to meet you, Bob!")

    # Вызываем обработчик
    await message_handler.handle_message(mock_message)

    # Проверяем что ответ был отправлен
    mock_message.answer.assert_called_once()

    # Проверяем что теперь в истории 4 сообщения
    history = await conversation.get_history(222, 111)
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


@pytest.mark.asyncio
async def test_handle_message_timeout_error(message_handler, conversation):
    """Тест обработки Timeout исключения."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 999
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 888
    mock_message.text = "Test message"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Мокаем llm_client.get_response чтобы вызвать APITimeoutError
    with patch.object(
        message_handler.llm_client, "get_response", side_effect=APITimeoutError("Request timeout")
    ):
        await message_handler.handle_message(mock_message)

    # Проверяем что было отправлено сообщение об ошибке
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    assert "Превышено время ожидания" in response_text or "⏱️" in response_text
    assert str(message_handler.config.timeout) in response_text


@pytest.mark.asyncio
async def test_handle_message_api_error(message_handler, conversation):
    """Тест обработки APIError исключения."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 777
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 666
    mock_message.text = "Test message"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Создаем APIError с body
    api_error = APIError(
        message="API Error", request=MagicMock(), body={"error": {"message": "Rate limit exceeded"}}
    )

    # Мокаем llm_client.get_response чтобы вызвать APIError
    with patch.object(message_handler.llm_client, "get_response", side_effect=api_error):
        await message_handler.handle_message(mock_message)

    # Проверяем что было отправлено сообщение об ошибке
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    assert "Ошибка API" in response_text or "❌" in response_text


@pytest.mark.asyncio
async def test_handle_message_llm_error(message_handler, conversation):
    """Тест обработки LLMError исключения."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 555
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 444
    mock_message.text = "Test message"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Мокаем llm_client.get_response чтобы вызвать LLMError
    with patch.object(
        message_handler.llm_client, "get_response", side_effect=LLMError("Empty response")
    ):
        await message_handler.handle_message(mock_message)

    # Проверяем что было отправлено сообщение об ошибке
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    assert "Ошибка LLM" in response_text or "❌" in response_text


@pytest.mark.asyncio
async def test_handle_message_unexpected_error(message_handler, conversation):
    """Тест обработки неожиданного исключения."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 333
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 222
    mock_message.text = "Test message"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Мокаем llm_client.get_response чтобы вызвать неожиданную ошибку
    with patch.object(
        message_handler.llm_client, "get_response", side_effect=ValueError("Unexpected error")
    ):
        await message_handler.handle_message(mock_message)

    # Проверяем что было отправлено сообщение об ошибке
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    assert "непредвиденная ошибка" in response_text.lower() or "❌" in response_text


@pytest.mark.asyncio
async def test_handle_message_success(message_handler, conversation):
    """Тест успешной обработки сообщения с мокированным LLM."""
    # Создаем мок сообщения
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 123
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 456
    mock_message.text = "Hello"
    mock_message.answer = AsyncMock()
    mock_bot = MagicMock()
    mock_bot.send_chat_action = AsyncMock()
    mock_message.bot = mock_bot

    # Мокаем llm_client.get_response чтобы вернуть успешный ответ
    with patch.object(
        message_handler.llm_client, "get_response", return_value="Hello! How can I help you?"
    ):
        await message_handler.handle_message(mock_message)

    # Проверяем что typing action был отправлен
    mock_bot.send_chat_action.assert_called_once_with(456, "typing")

    # Проверяем что ответ был отправлен
    mock_message.answer.assert_called_once_with("Hello! How can I help you?")

    # Проверяем что сообщения сохранены в историю
    history = await conversation.get_history(456, 123)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_reset_command_without_user(message_handler):
    """Тест reset команды без пользователя."""
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = None
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 123
    mock_message.answer = AsyncMock()

    # Вызываем reset - должен просто выйти без ошибок
    await message_handler.reset_command(mock_message)

    # answer не должен быть вызван
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_role_command(message_handler):
    """Тест обработчика команды /role."""
    # Arrange
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = MagicMock(spec=types.User)
    mock_message.from_user.id = 123
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 456
    mock_message.answer = AsyncMock()

    # Act
    await message_handler.role_command(mock_message)

    # Assert
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    response_text = call_args[0][0]

    # Проверяем структуру ответа
    assert "🎭" in response_text
    assert "Моя роль" in response_text or "роль" in response_text.lower()
    assert "Специализация" in response_text or "специализация" in response_text.lower()
    assert "Python" in response_text
    assert "Что я умею" in response_text or "умею" in response_text.lower()
    assert "Ограничения" in response_text or "ограничения" in response_text.lower()


@pytest.mark.asyncio
async def test_role_command_without_user(message_handler):
    """Тест команды /role без пользователя (edge case)."""
    # Arrange
    mock_message = MagicMock(spec=types.Message)
    mock_message.from_user = None
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = 123
    mock_message.answer = AsyncMock()

    # Act - не должно быть ошибок
    await message_handler.role_command(mock_message)

    # Assert - ответ все равно должен быть отправлен
    mock_message.answer.assert_called_once()
