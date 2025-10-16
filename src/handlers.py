"""Обработчики Telegram сообщений и команд."""

import logging

from aiogram import types
from openai import APIError, APITimeoutError

from .config import Config
from .conversation import Conversation
from .llm_client import LLMClient, LLMError

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

    async def start_command(self, message: types.Message) -> None:
        """Обработчик команды /start.

        Args:
            message: Сообщение от пользователя
        """
        user_id = message.from_user.id if message.from_user else "unknown"
        chat_id = message.chat.id
        logger.info(f"Command /start from user {user_id} in chat {chat_id}")

        welcome_text = (
            "👋 <b>Привет! Я Python Code Reviewer.</b>\n\n"
            "Я помогу проверить твой Python код на соответствие PEP 8,\n"
            "найду потенциальные баги и предложу улучшения.\n\n"
            "💡 <b>Команды:</b>\n"
            "• /role - подробнее о моей роли и возможностях\n"
            "• /reset - начать новый диалог\n\n"
            "Присылай код - начнем ревью! 🚀"
        )

        await message.answer(welcome_text)
        logger.info(f"Welcome message sent to user {user_id}")

    async def reset_command(self, message: types.Message) -> None:
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
        await self.conversation.clear_history(chat_id, user_id)

        reset_text = "🔄 <b>История диалога очищена!</b>\n\nМожете начать новый разговор."

        await message.answer(reset_text)
        logger.info(f"History cleared for user {user_id}")

    async def role_command(self, message: types.Message) -> None:
        """Обработчик команды /role - отображение роли бота.

        Args:
            message: Сообщение от пользователя
        """
        user_id = message.from_user.id if message.from_user else "unknown"
        chat_id = message.chat.id
        logger.info(f"Command /role from user {user_id} in chat {chat_id}")

        role_text = (
            "🎭 <b>Моя роль:</b> Python Code Reviewer\n\n"
            "📋 <b>Специализация:</b>\n"
            "• Проверка Python кода на соответствие PEP 8\n"
            "• Поиск потенциальных багов и проблем\n"
            "• Советы по рефакторингу и улучшению кода\n"
            "• Рекомендации по производительности\n\n"
            "✅ <b>Что я умею:</b>\n"
            "• Анализировать синтаксис и стиль Python кода\n"
            "• Находить проблемы с архитектурой\n"
            "• Предлагать лучшие практики (best practices)\n"
            "• Объяснять \"почему\" за каждым замечанием\n\n"
            "❌ <b>Ограничения:</b>\n"
            "• Работаю только с Python (не другие языки)\n"
            "• Не пишу код за вас (только примеры и советы)\n"
            "• Не делаю полный редизайн архитектуры без запроса"
        )

        await message.answer(role_text)
        logger.info(f"Role description sent to user {user_id}")

    async def handle_message(self, message: types.Message) -> None:
        """Обработчик текстовых сообщений.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user or not message.text:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id
        user_message = message.text

        logger.info(f"Message from user {user_id} in chat {chat_id}, length: {len(user_message)}")

        # Сохраняем сообщение пользователя в историю
        await self.conversation.add_message(chat_id, user_id, "user", user_message)

        # Получаем историю диалога с учетом лимита
        history = await self.conversation.get_history(
            chat_id, user_id, limit=self.config.max_history_length
        )

        # Отправляем "typing..." индикатор
        if message.bot:
            await message.bot.send_chat_action(chat_id, "typing")

        try:
            # Получаем ответ от LLM
            llm_response = await self.llm_client.get_response(
                messages=history, system_prompt=self.config.system_prompt
            )

            # Сохраняем ответ ассистента в историю
            await self.conversation.add_message(chat_id, user_id, "assistant", llm_response)

            # Отправляем ответ пользователю
            await message.answer(llm_response)

            logger.info(f"Response sent to user {user_id}, length: {len(llm_response)}")

        except APITimeoutError:
            logger.error(f"LLM timeout for user {user_id}", exc_info=True)
            error_text = (
                f"⏱️ Превышено время ожидания ответа ({self.config.timeout}с).\nПопробуйте снова."
            )
            await message.answer(error_text)

        except APIError as e:
            logger.error(f"LLM API error for user {user_id}: {e}", exc_info=True)
            error_text = (
                f"❌ Ошибка API: {str(e)}\nПожалуйста, попробуйте позже или используйте /reset."
            )
            await message.answer(error_text)

        except LLMError as e:
            logger.error(f"LLM error for user {user_id}: {e}", exc_info=True)
            error_text = (
                f"❌ Ошибка LLM: {str(e)}\n"
                "Попробуйте еще раз или используйте /reset для сброса диалога."
            )
            await message.answer(error_text)

        except Exception as e:
            logger.error(
                f"Unexpected error handling message from user {user_id}: {e}",
                exc_info=True,
            )
            error_text = (
                "❌ Произошла непредвиденная ошибка.\n"
                "Попробуйте еще раз или используйте /reset для сброса диалога."
            )
            await message.answer(error_text)
