"""Юнит-тесты для модуля bot."""

from unittest.mock import MagicMock

import pytest

from src.bot import TelegramBot
from src.config import Config
from src.handlers import MessageHandler


@pytest.fixture
def config():
    """Фикстура для создания тестовой конфигурации."""
    return Config(
        telegram_bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
        openrouter_api_key="test_api_key",
        openrouter_model="test/model",
        system_prompt="Test prompt",
    )


def test_telegram_bot_initialization(config):
    """Тест инициализации TelegramBot."""
    bot = TelegramBot(config)

    assert bot.config == config
    assert bot.bot is not None
    assert bot.dp is not None


def test_telegram_bot_initialization_with_token(config):
    """Тест что токен используется при инициализации."""
    bot = TelegramBot(config)

    # Проверяем что бот создан с правильным токеном
    assert bot.bot.token == config.telegram_bot_token


def test_register_handlers(config):
    """Тест регистрации обработчиков."""
    bot = TelegramBot(config)

    # Создаем мок MessageHandler
    mock_handler = MagicMock(spec=MessageHandler)
    mock_handler.start_command = MagicMock()
    mock_handler.role_command = MagicMock()
    mock_handler.me_command = MagicMock()
    mock_handler.reset_command = MagicMock()
    mock_handler.handle_message = MagicMock()

    # Мокаем dp.message.register
    bot.dp.message.register = MagicMock()

    # Регистрируем handlers
    bot.register_handlers(mock_handler)

    # Проверяем что register был вызван 5 раз
    # (start_command, role_command, me_command, reset_command, handle_message)
    assert bot.dp.message.register.call_count == 5


def test_register_handlers_order(config):
    """Тест что обработчики регистрируются в правильном порядке."""
    bot = TelegramBot(config)

    # Создаем мок MessageHandler
    mock_handler = MagicMock(spec=MessageHandler)

    # Сохраняем вызовы register
    register_calls = []

    def mock_register(handler, *args, **kwargs):
        register_calls.append((handler, args, kwargs))

    bot.dp.message.register = mock_register

    # Регистрируем handlers
    bot.register_handlers(mock_handler)

    # Проверяем порядок регистрации
    assert len(register_calls) == 5

    # Первый должен быть start_command
    assert register_calls[0][0] == mock_handler.start_command

    # Второй должен быть role_command
    assert register_calls[1][0] == mock_handler.role_command

    # Третий должен быть me_command
    assert register_calls[2][0] == mock_handler.me_command

    # Четвертый должен быть reset_command
    assert register_calls[3][0] == mock_handler.reset_command

    # Пятый должен быть handle_message (без команды - должен быть последним)
    assert register_calls[4][0] == mock_handler.handle_message


@pytest.mark.asyncio
async def test_start_polling(config):
    """Тест запуска polling."""
    bot = TelegramBot(config)

    # Создаем async функцию-мок
    async def mock_polling(bot_instance):
        pass

    bot.dp.start_polling = mock_polling

    # Мокаем session.close как AsyncMock
    from unittest.mock import AsyncMock

    bot.bot.session = MagicMock()
    bot.bot.session.close = AsyncMock()

    # Запускаем start
    await bot.start()

    # Проверяем что session.close был вызван
    bot.bot.session.close.assert_called_once()


@pytest.mark.asyncio
async def test_start_polling_with_exception(config):
    """Тест что session.close вызывается даже при ошибке."""
    bot = TelegramBot(config)

    # Мокаем start_polling чтобы вызвать ошибку
    async def mock_polling_error(bot_instance):
        raise RuntimeError("Test error")

    bot.dp.start_polling = mock_polling_error

    # Мокаем session.close как AsyncMock
    from unittest.mock import AsyncMock

    bot.bot.session = MagicMock()
    bot.bot.session.close = AsyncMock()

    # Запускаем start и ожидаем ошибку
    with pytest.raises(RuntimeError, match="Test error"):
        await bot.start()

    # Проверяем что session.close был вызван несмотря на ошибку
    bot.bot.session.close.assert_called_once()


def test_bot_default_properties(config):
    """Тест настроек бота по умолчанию."""
    bot = TelegramBot(config)

    # Проверяем что бот создан с правильными свойствами
    assert bot.bot.default is not None
    # ParseMode должен быть HTML
    from aiogram.enums import ParseMode

    assert bot.bot.default.parse_mode == ParseMode.HTML


def test_dispatcher_initialization(config):
    """Тест инициализации диспетчера."""
    bot = TelegramBot(config)

    # Проверяем что диспетчер создан
    assert bot.dp is not None

    # Проверяем что у диспетчера есть message router
    assert bot.dp.message is not None
