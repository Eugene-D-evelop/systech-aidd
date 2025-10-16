"""Обработчики Telegram сообщений и команд."""

import logging

from aiogram import types
from openai import APIError, APITimeoutError

from .config import Config
from .conversation import Conversation
from .database import Database
from .llm_client import LLMClient, LLMError

logger = logging.getLogger(__name__)


async def save_user_info(database: Database, user: types.User) -> None:
    """Сохранение/обновление информации о пользователе в БД.

    Args:
        database: Экземпляр Database для работы с БД
        user: Объект пользователя из Telegram
    """
    await database.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
        is_premium=user.is_premium or False,
        is_bot=user.is_bot,
    )
    logger.debug(f"User info saved: user_id={user.id}, username={user.username}")


class MessageHandler:
    """Класс для обработки сообщений и команд бота."""

    def __init__(
        self, config: Config, llm_client: LLMClient, conversation: Conversation, database: Database
    ):
        """Инициализация обработчика.

        Args:
            config: Конфигурация приложения
            llm_client: Клиент для работы с LLM
            conversation: Хранилище истории диалогов
            database: Слой работы с базой данных
        """
        self.config = config
        self.llm_client = llm_client
        self.conversation = conversation
        self.database = database
        logger.info("MessageHandler initialized")

    async def start_command(self, message: types.Message) -> None:
        """Обработчик команды /start.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user:
            return

        # Сохраняем информацию о пользователе
        await save_user_info(self.database, message.from_user)

        user_id = message.from_user.id
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        logger.info(
            f"Command /start from user {user_id} (@{message.from_user.username or 'no_username'}) "
            f"in chat {chat_id}"
        )

        welcome_text = (
            f"👋 <b>Привет, {first_name}! Я Python Code Reviewer.</b>\n\n"
            "Я помогу проверить твой Python код на соответствие PEP 8,\n"
            "найду потенциальные баги и предложу улучшения.\n\n"
            "💡 <b>Команды:</b>\n"
            "• /role - подробнее о моей роли и возможностях\n"
            "• /reset - начать новый диалог\n"
            "• /me - посмотреть свой профиль\n\n"
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

        # Сохраняем информацию о пользователе
        await save_user_info(self.database, message.from_user)

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
        if not message.from_user:
            return

        # Сохраняем информацию о пользователе
        await save_user_info(self.database, message.from_user)

        user_id = message.from_user.id
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

    async def me_command(self, message: types.Message) -> None:
        """Обработчик команды /me - отображение профиля пользователя.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user:
            return

        # Сохраняем информацию о пользователе
        await save_user_info(self.database, message.from_user)

        user_id = message.from_user.id
        chat_id = message.chat.id
        logger.info(f"Command /me from user {user_id} in chat {chat_id}")

        # Получаем информацию о пользователе из БД
        user = await self.database.get_user(user_id)
        if not user:
            error_text = "❌ Не удалось найти информацию о пользователе."
            await message.answer(error_text)
            logger.error(f"User {user_id} not found in database")
            return

        # Получаем статистику
        stats = await self.database.get_user_stats(user_id)

        # Формируем полное имя
        full_name = user["first_name"]
        if user["last_name"]:
            full_name += f" {user['last_name']}"

        # Форматируем дату регистрации
        created_date = user["created_at"].strftime("%d.%m.%Y")

        # Формируем username строку
        username_str = (
            f"@{user['username']}" if user["username"] else "<i>не указан</i>"
        )

        profile_text = (
            f"👤 <b>Ваш профиль</b>\n\n"
            f"🆔 ID: <code>{user['user_id']}</code>\n"
            f"👤 Имя: {full_name}\n"
            f"📱 Username: {username_str}\n"
            f"🌍 Язык: {user['language_code'] or '<i>не указан</i>'}\n"
            f"⭐ Premium: {'Да ✨' if user['is_premium'] else 'Нет'}\n"
            f"📅 С нами с: {created_date}\n\n"
            f"📊 <b>Статистика:</b>\n"
            f"💬 Сообщений отправлено: {stats['message_count']}\n"
            f"📝 Всего символов: {stats['total_characters']:,}\n"
        )

        # Добавляем информацию о первом сообщении, если есть
        if stats["first_message_at"]:
            first_msg_date = stats["first_message_at"].strftime("%d.%m.%Y")
            profile_text += f"🗓️ Первое сообщение: {first_msg_date}\n"

        await message.answer(profile_text)
        logger.info(f"Profile sent to user {user_id}")

    async def handle_message(self, message: types.Message) -> None:
        """Обработчик текстовых сообщений.

        Args:
            message: Сообщение от пользователя
        """
        if not message.from_user or not message.text:
            return

        # Сохраняем информацию о пользователе
        await save_user_info(self.database, message.from_user)

        user_id = message.from_user.id
        chat_id = message.chat.id
        user_message = message.text

        logger.info(
            f"Message from user {user_id} (@{message.from_user.username or 'no_username'}) "
            f"in chat {chat_id}, length: {len(user_message)}"
        )

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
