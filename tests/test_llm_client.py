"""Интеграционные тесты для модуля llm_client."""

import pytest
from dotenv import load_dotenv

from src.config import Config
from src.llm_client import LLMClient

# Все тесты в этом файле - интеграционные (требуют реального API)
pytestmark = pytest.mark.integration

# Загружаем переменные окружения из .env
load_dotenv()


@pytest.fixture
def config():
    """Фикстура для создания реальной конфигурации из .env."""
    return Config()


@pytest.fixture
def llm_client(config):
    """Фикстура для создания LLMClient."""
    return LLMClient(config)


@pytest.mark.asyncio
async def test_llm_client_initialization(llm_client, config):
    """Тест инициализации LLM клиента."""
    assert llm_client.config == config
    assert llm_client.client is not None


@pytest.mark.asyncio
async def test_get_response_simple(llm_client):
    """Тест получения простого ответа от LLM."""
    messages = [{"role": "user", "content": "Say 'hello' and nothing else"}]

    response = await llm_client.get_response(
        messages=messages, system_prompt="You are a helpful assistant."
    )

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_get_response_with_system_prompt(llm_client):
    """Тест получения ответа с системным промптом."""
    messages = [{"role": "user", "content": "What is 2+2?"}]
    system_prompt = "You are a math tutor. Answer concisely."

    response = await llm_client.get_response(messages=messages, system_prompt=system_prompt)

    assert response is not None
    assert isinstance(response, str)
    assert "4" in response or "four" in response.lower()


@pytest.mark.asyncio
async def test_get_response_with_conversation_history(llm_client):
    """Тест получения ответа с учетом истории диалога."""
    messages = [
        {"role": "user", "content": "My name is Alice"},
        {"role": "assistant", "content": "Nice to meet you, Alice!"},
        {"role": "user", "content": "What is my name?"},
    ]

    response = await llm_client.get_response(
        messages=messages, system_prompt="You are a helpful assistant."
    )

    assert response is not None
    assert isinstance(response, str)
    # LLM должен помнить имя из истории
    assert "alice" in response.lower()


@pytest.mark.asyncio
async def test_get_response_without_system_prompt(llm_client):
    """Тест получения ответа без системного промпта."""
    messages = [{"role": "user", "content": "Hello"}]

    response = await llm_client.get_response(messages=messages, system_prompt=None)

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_get_response_empty_message_list(llm_client):
    """Тест с пустым списком сообщений."""
    messages = []

    # Даже с пустым списком, если есть system_prompt, должен быть ответ
    response = await llm_client.get_response(messages=messages, system_prompt="Say hello")

    assert response is not None
    assert isinstance(response, str)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_get_response_long_conversation(llm_client):
    """Тест с длинной историей диалога."""
    messages = []

    # Создаем историю из 10 обменов
    for i in range(10):
        messages.append({"role": "user", "content": f"Message {i}"})
        messages.append({"role": "assistant", "content": f"Response {i}"})

    messages.append({"role": "user", "content": "Summarize our conversation"})

    response = await llm_client.get_response(
        messages=messages, system_prompt="You are a helpful assistant."
    )

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_get_response_special_characters(llm_client):
    """Тест с специальными символами в сообщении."""
    messages = [
        {
            "role": "user",
            "content": "Repeat this: Hello! @#$%^&*() <html> 你好",
        }
    ]

    response = await llm_client.get_response(
        messages=messages, system_prompt="Echo the user's message."
    )

    assert response is not None
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_config_parameters_used(llm_client, config):
    """Тест что параметры из конфигурации используются."""
    messages = [{"role": "user", "content": "Test"}]

    # Проверяем что можем получить ответ с параметрами из config
    response = await llm_client.get_response(messages=messages, system_prompt=config.system_prompt)

    assert response is not None
    assert isinstance(response, str)
