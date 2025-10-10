"""Telegram бот - инициализация и регистрация обработчиков."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    """Класс для инициализации и управления Telegram ботом."""

    def __init__(self, config: Config):
        """Инициализация бота.

        Args:
            config: Конфигурация приложения
        """
        self.config = config
        self.bot = Bot(
            token=config.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.dp = Dispatcher()
        logger.info("Telegram bot initialized")

    def register_handlers(self, message_handler):
        """Регистрация обработчиков сообщений.

        Args:
            message_handler: Экземпляр MessageHandler с обработчиками
        """
        # Регистрация обработчиков команд
        self.dp.message.register(message_handler.start_command, commands=["start"])
        logger.info("Handlers registered")

    async def start(self):
        """Запуск бота в режиме polling."""
        logger.info("Bot starting...")
        try:
            await self.dp.start_polling(self.bot)
        finally:
            await self.bot.session.close()

