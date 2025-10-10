"""Обработчики Telegram сообщений и команд."""

import logging

from aiogram import types

from src.config import Config

logger = logging.getLogger(__name__)


class MessageHandler:
    """Класс для обработки сообщений и команд бота."""

    def __init__(self, config: Config):
        """Инициализация обработчика.

        Args:
            config: Конфигурация приложения
        """
        self.config = config
        logger.info("MessageHandler initialized")

    async def start_command(self, message: types.Message):
        """Обработчик команды /start.

        Args:
            message: Сообщение от пользователя
        """
        user_id = message.from_user.id if message.from_user else "unknown"
        chat_id = message.chat.id
        logger.info(f"Command /start from user {user_id} in chat {chat_id}")

        welcome_text = (
            "<b>👋 Привет! Я AI-ассистент.</b>\n\n"
            "Я могу помочь вам с различными вопросами.\n"
            "Просто напишите мне сообщение, и я отвечу!\n\n"
            "<i>Используйте /reset для сброса истории диалога.</i>"
        )

        await message.answer(welcome_text)
        logger.info(f"Welcome message sent to user {user_id}")

