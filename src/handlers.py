"""Обработчики Telegram сообщений и команд."""

import logging

from aiogram import types

from src.config import Config
from src.conversation import Conversation
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)


class MessageHandler:
    """Класс для обработки сообщений и команд бота."""

    def __init__(self, config: Config, llm_client: LLMClient, conversation: Conversation):
        """Инициализация обработчика.

        Args:
            config: Конфигурация приложения
            llm_client: Клиент для работы с LLM
            conversation: Хранилище истории диалогов
        """
        self.config = config
        self.llm_client = llm_client
        self.conversation = conversation
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

    async def reset_command(self, message: types.Message):
        """Обработчик команды /reset - очистка истории диалога.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        logger.info(f"Command /reset from user {user_id} in chat {chat_id}")

        # Очищаем историю диалога
        self.conversation.clear_history(chat_id, user_id)

        reset_text = (
            "🔄 <b>История диалога очищена!</b>\n\n"
            "Можете начать новый разговор."
        )

        await message.answer(reset_text)
        logger.info(f"History cleared for user {user_id}")

    async def handle_message(self, message: types.Message):
        """Обработчик текстовых сообщений.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user or not message.text:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        user_message = message.text

        logger.info(
            f"Message from user {user_id} in chat {chat_id}, "
            f"length: {len(user_message)}"
        )

        # Сохраняем сообщение пользователя в историю
        self.conversation.add_message(chat_id, user_id, "user", user_message)

        # Получаем историю диалога с учетом лимита
        history = self.conversation.get_history(
            chat_id, user_id, limit=self.config.max_history_length
        )

        # Отправляем "typing..." индикатор
        await message.bot.send_chat_action(chat_id, "typing")

        try:
            # Получаем ответ от LLM
            llm_response = await self.llm_client.get_response(
                messages=history, system_prompt=self.config.system_prompt
            )

            # Сохраняем ответ ассистента в историю
            self.conversation.add_message(chat_id, user_id, "assistant", llm_response)

            # Отправляем ответ пользователю
            await message.answer(llm_response)

            logger.info(f"Response sent to user {user_id}, length: {len(llm_response)}")

        except Exception as e:
            logger.error(f"Error handling message from user {user_id}: {e}", exc_info=True)
            error_text = (
                "❌ Произошла ошибка при обработке сообщения.\n"
                "Попробуйте еще раз или используйте /reset для сброса диалога."
            )
            await message.answer(error_text)
