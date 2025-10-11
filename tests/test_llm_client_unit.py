"""Юнит-тесты для модуля llm_client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from openai import APIError, APITimeoutError

from src.config import Config
from src.llm_client import LLMClient, LLMError


@pytest.fixture
def config():
    """Фикстура для создания тестовой конфигурации."""
    return Config(
        telegram_bot_token="test_token",
        openrouter_api_key="test_api_key",
        openrouter_model="test/model",
        system_prompt="Test prompt",
        temperature=0.7,
        max_tokens=100,
        timeout=30,
    )


@pytest.fixture
def llm_client(config):
    """Фикстура для создания LLMClient."""
    return LLMClient(config)


def test_llm_client_initialization(llm_client, config):
    """Тест инициализации LLMClient."""
    assert llm_client.config == config
    assert llm_client.client is not None


@pytest.mark.asyncio
async def test_get_response_success(llm_client):
    """Тест успешного получения ответа от LLM."""
    # Создаем мок ответа
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Test response"

    # Мокаем метод create
    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        messages = [{"role": "user", "content": "Test"}]
        response = await llm_client.get_response(messages, system_prompt="Test prompt")

        assert response == "Test response"


@pytest.mark.asyncio
async def test_get_response_with_system_prompt(llm_client):
    """Тест что system prompt добавляется в messages."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ) as mock_create:
        messages = [{"role": "user", "content": "Hello"}]
        await llm_client.get_response(messages, system_prompt="You are helpful")

        # Проверяем что create был вызван
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        sent_messages = call_args[1]["messages"]

        # Проверяем что первое сообщение - system prompt
        assert len(sent_messages) == 2
        assert sent_messages[0]["role"] == "system"
        assert sent_messages[0]["content"] == "You are helpful"
        assert sent_messages[1] == messages[0]


@pytest.mark.asyncio
async def test_get_response_without_system_prompt(llm_client):
    """Тест без system prompt."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ) as mock_create:
        messages = [{"role": "user", "content": "Hello"}]
        await llm_client.get_response(messages, system_prompt=None)

        # Проверяем что system prompt не был добавлен
        call_args = mock_create.call_args
        sent_messages = call_args[1]["messages"]
        assert len(sent_messages) == 1
        assert sent_messages[0] == messages[0]


@pytest.mark.asyncio
async def test_get_response_empty_response_raises_llm_error(llm_client):
    """Тест что пустой ответ вызывает LLMError."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = None  # Пустой ответ

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ):
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(LLMError, match="Empty response"):
            await llm_client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_timeout_raises(llm_client):
    """Тест что APITimeoutError пробрасывается."""
    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        side_effect=APITimeoutError("Request timeout"),
    ):
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(APITimeoutError):
            await llm_client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_api_error_raises(llm_client):
    """Тест что APIError пробрасывается."""
    api_error = APIError(
        message="API Error",
        request=MagicMock(),
        body={"error": {"message": "Rate limit"}},
    )

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        side_effect=api_error,
    ):
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(APIError):
            await llm_client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_unexpected_error_raises_llm_error(llm_client):
    """Тест что неожиданная ошибка оборачивается в LLMError."""
    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        side_effect=ValueError("Unexpected error"),
    ):
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(LLMError, match="Unexpected error"):
            await llm_client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_uses_config_parameters(llm_client, config):
    """Тест что используются параметры из конфига."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Response"

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ) as mock_create:
        messages = [{"role": "user", "content": "Test"}]
        await llm_client.get_response(messages)

        # Проверяем что create был вызван с правильными параметрами
        call_args = mock_create.call_args
        assert call_args[1]["model"] == config.openrouter_model
        assert call_args[1]["temperature"] == config.temperature
        assert call_args[1]["max_tokens"] == config.max_tokens
        assert call_args[1]["timeout"] == config.timeout


@pytest.mark.asyncio
async def test_get_response_with_multiple_messages(llm_client):
    """Тест с несколькими сообщениями в истории."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Final response"

    with patch.object(
        llm_client.client.chat.completions,
        "create",
        new_callable=AsyncMock,
        return_value=mock_response,
    ) as mock_create:
        messages = [
            {"role": "user", "content": "First message"},
            {"role": "assistant", "content": "First response"},
            {"role": "user", "content": "Second message"},
        ]
        await llm_client.get_response(messages, system_prompt="Test")

        # Проверяем что все сообщения были переданы
        call_args = mock_create.call_args
        sent_messages = call_args[1]["messages"]
        assert len(sent_messages) == 4  # system + 3 messages


def test_llm_error_is_exception():
    """Тест что LLMError является исключением."""
    error = LLMError("Test error")
    assert isinstance(error, Exception)
    assert str(error) == "Test error"
